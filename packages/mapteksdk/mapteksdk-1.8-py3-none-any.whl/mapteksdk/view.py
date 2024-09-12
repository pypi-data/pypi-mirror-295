"""Interaction with a view in an applicable Maptek application.

The first step is opening a new view which returns a view controller for the
new view. From there you can control the view by adding/removing objects,
hiding/showing objects and querying what objects are in the view.

>>> from mapteksdk.project import Project
>>> import mapteksdk.operations as operations
>>> project = Project()
>>> view = operations.open_new_view()
>>> view.add_objects([project.find_object('/cad')])
"""

###############################################################################
#
# (C) Copyright 2021, Maptek Pty Ltd. All rights reserved.
#
###############################################################################

from collections.abc import Iterable, Sequence
import copy
import ctypes
import enum
import logging
import pathlib
import typing
import os

from mapteksdk.capi.viewer import Viewer, ViewerErrorCodes
from mapteksdk.data import ObjectID, DataObject
from mapteksdk.geometry import Extent, Plane
from mapteksdk.overwrite_modes import OverwriteMode
from mapteksdk.internal.rotation import Rotation
import mapteksdk.internal.view as view_private
from mapteksdk.internal.comms import (
  InlineMessage,
  Message,
  Request,
  Response,
  Double,
  Int32s,
  Int16u,
  Int32u,
  CommunicationsManager,
  default_manager,
)
from mapteksdk.internal.serialisation import (
  FixedInteger32Mixin,
  FixedInteger32uMixin
)
from mapteksdk.internal.normalise_selection import normalise_selection


Point: "typing.TypeAlias" = tuple[Double, Double, Double]
"""Tuple representing a point."""


def save_to_image(
  objects: "Iterable[ObjectID | DataObject | str]",
  path: "os.PathLike | str",
  overwrite: OverwriteMode = OverwriteMode.ERROR,
) -> pathlib.Path:
  """Save the given objects to an image file as they would be seen in a view.

  The camera will either look top-down at the objects or from the front.

  Objects may obstruct other objects. This means one or more of the objects
  provided may not be seen in the resulting image.

  Parameters
  ----------
  objects
    The objects included in the image.
  path
    The path to where the image should be saved.
    This ideally should have a PNG extension.
  overwrite
    How to handle writing an image to path if a file already exists
    there.

  Returns
  ------
  pathlib.Path
    The path of the resulting image.

  Raises
  ------
  ApplicationTooOldError
    If you should use a newer version of the application as the feature is
    not available with the version connected to.
  RuntimeError
    If the view can not be opened.
  FileExistsError
    If overwrite is OverwriteMode.ERROR and path already exists.
  OSError
    If overwrite is OverwriteMode.OVERWRITE and path can't be deleted.
  """
  logger = logging.getLogger("mapteksdk.view")
  logger.info(
    "Creating an off-screen view for rendering the view to an image.")
  with view_private.ViewWindow(width=1920, height=1080,
                               logger=logger) as view_window:
    view = ViewController(view_window.view_id)
    try:
      view.add_objects(objects)

      if objects:
        _choose_better_camera_for_image(view)

      try:
        image_path = view_window.save_to_image(
          path, overwrite=overwrite)
      except FileExistsError as error:
        logger.error("Image was unable to be saved: %s", error)
        raise
    finally:
      view.close()

  return image_path


def request_no_body(
  message_name: str,
  response_type: type[Response],
  manager: CommunicationsManager,
) -> Request:
  """Create a request class with no body.

  Parameters
  ----------
  message_name
    The name of a message.
  response_type
    The type of response this request should expect.
  manager
    The manager to use to create the request

  Returns
  -------
  type[Request]
    A request with the specified message name and body.
  """
  class NoBody(Request):
    """A request without a body."""
    @classmethod
    def message_name(cls) -> str:
      return message_name

    @classmethod
    def response_type(cls) -> type[Response]:
      return response_type

  return NoBody(manager)


class ViewNoLongerExists(RuntimeError):
  """Exception for when a view is expected but it no longer exists.

  The most common occurrence for this exception is when the view has been
  closed.
  """


class ObjectFilter(FixedInteger32uMixin, enum.IntEnum):
  """Describes different ways to filter what objects are returned by
  a ViewController."""

  DEFAULT = 0
  """Default - return all object except transient and background objects but
  ignoring visibility, and selection

  Transient objects are objects that are in the view for previewing an
  operation or providing additional clarity while a tool in the application
  is running.
  """

  VISIBLE_ONLY = 1 << 0
  """Only return objects that are visible in the view."""

  HIDDEN_ONLY = 1 << 1
  """Only return objects that are hidden in the view."""

  SELECTED_ONLY = 1 << 2
  """Only return objects that are selected and are in the view."""

  def from_bytes(
      self,
      # pylint: disable=redefined-builtin
      bytes,
      byteorder = "big",
      *,
      signed = False):
    """Return the integer represented by the given array of bytes.

    bytes
        Holds the array of bytes to convert. The argument must either
        support the buffer protocol or be an iterable object
        producing bytes. Bytes and bytearray are examples of built-in
        objects that support the buffer protocol.
    byteorder
        The byte order used to represent the integer. If byteorder is
        'big', the most significant byte is at the beginning of the
        byte array. If byteorder is 'little', the most significant
        byte is at the end of the byte array. To request the native
        byte order of the host system, use 'sys.byteorder' as the
        byte order value. Default is to use 'big'.
    signed
        Indicates whether two's complement is used to represent the integer.
    """
    # :HACK: There is a mismatched quotation mark in the docstring in the
    # standard library for this function, which results in the
    # sphinx documentation failing to build.
    # Overwrite the function to fix the docstring.
    return super().from_bytes(bytes, byteorder, signed=signed) # type: ignore

  def to_bytes(
      self,
      length = 1,
      byteorder = "big",
      *,
      signed = False):
    """Return an array of bytes representing an integer.

    Parameters
    ----------
    length
      Length of bytes object to use. An OverflowError is raised if the
      integer is not representable with the given number of bytes.
      Default is length 1.
    byteorder
      The byte order used to represent the integer.
      If byteorder is 'big', the most significant byte is at the beginning
      of the byte array. If byteorder is 'little', the most significant byte
      is at the end of the byte array. To request the native byte order of
      the host system, use 'sys.byteorder' as the byte order value.
      Default is to use 'big'.
    signed
      Determines whether two's complement is used to represent the integer.
      If signed is False and a negative integer is given, an OverflowError
      is raised.
    """
    # :HACK: There is a mismatched quotation mark in the docstring in the
    # standard library for this function, which results in the
    # sphinx documentation failing to build.
    # Overwrite the function to fix the docstring.
    return super().to_bytes(length, byteorder, signed=signed)

class SectionMode(enum.IntEnum):
  """Enumeration of the available section modes.
  """

  NO_MODE = 0
  """No section mode is active."""

  POSITIVE_HALF_SPACE = 1
  """Only show data on the normal side of the plane.

  The clip plane is defined to be the action plane in the direction
  of the plane normal.

  A section width may be defined to only show the data on the normal
  side of the plane that is at a maximum the section width away.
  """

  NEGATIVE_HALF_SPACE = 2
  """Only show data on the negative side of the plane.

  The clip plane is defined to be the action plane in the opposite
  direction of the plane normal.

  A section width may be defined to only show the data on the normal
  side of the plane that is at a maximum the section width away.
  """

  STRIP = 3
  """Show data between two parallel planes.

  The clip planes are defined to be half the section width either side of the
  plane.
  """

  def from_bytes(
      self,
      # pylint: disable=redefined-builtin
      bytes,
      byteorder = "big",
      *,
      signed = False):
    """Return the integer represented by the given array of bytes.

    bytes
        Holds the array of bytes to convert. The argument must either
        support the buffer protocol or be an iterable object
        producing bytes. Bytes and bytearray are examples of built-in
        objects that support the buffer protocol.
    byteorder
        The byte order used to represent the integer. If byteorder is
        'big', the most significant byte is at the beginning of the
        byte array. If byteorder is 'little', the most significant
        byte is at the end of the byte array. To request the native
        byte order of the host system, use 'sys.byteorder' as the
        byte order value. Default is to use 'big'.
    signed
        Indicates whether two's complement is used to represent the integer.
    """
    # :HACK: There is a mismatched quotation mark in the docstring in the
    # standard library for this function, which results in the
    # sphinx documentation failing to build.
    # Overwrite the function to fix the docstring.
    return super().from_bytes(bytes, byteorder, signed=signed) # type: ignore

  def to_bytes(
      self,
      length = 1,
      byteorder = "big",
      *,
      signed = False):
    """Return an array of bytes representing an integer.

    Parameters
    ----------
    length
      Length of bytes object to use. An OverflowError is raised if the
      integer is not representable with the given number of bytes.
      Default is length 1.
    byteorder
      The byte order used to represent the integer.
      If byteorder is 'big', the most significant byte is at the beginning
      of the byte array. If byteorder is 'little', the most significant byte
      is at the end of the byte array. To request the native byte order of
      the host system, use 'sys.byteorder' as the byte order value.
      Default is to use 'big'.
    signed
      Determines whether two's complement is used to represent the integer.
      If signed is False and a negative integer is given, an OverflowError
      is raised.
    """
    # :HACK: There is a mismatched quotation mark in the docstring in the
    # standard library for this function, which results in the
    # sphinx documentation failing to build.
    # Overwrite the function to fix the docstring.
    return super().to_bytes(length, byteorder, signed=signed)


class SectionStepDirection(enum.IntEnum):
  """Enumeration of the section stepping directions.

  This refers to the screen-space directions in which to move the section.

  The two compound directions (LEFT_AND_UP and RIGHT_AND_DOWN) will move the
  section in the direction of the strongest component of the section plane
  normal as seen in screen-space (horizontal or vertical).
  """

  LEFT = 0
  RIGHT = 1
  UP = 2
  DOWN = 3
  LEFT_AND_UP = 4
  RIGHT_AND_DOWN = 5

  def from_bytes(
      self,
      # pylint: disable=redefined-builtin
      bytes,
      byteorder = "big",
      *,
      signed = False):
    """Return the integer represented by the given array of bytes.

    bytes
        Holds the array of bytes to convert. The argument must either
        support the buffer protocol or be an iterable object
        producing bytes. Bytes and bytearray are examples of built-in
        objects that support the buffer protocol.
    byteorder
        The byte order used to represent the integer. If byteorder is
        'big', the most significant byte is at the beginning of the
        byte array. If byteorder is 'little', the most significant
        byte is at the end of the byte array. To request the native
        byte order of the host system, use 'sys.byteorder' as the
        byte order value. Default is to use 'big'.
    signed
        Indicates whether two's complement is used to represent the integer.
    """
    # :HACK: There is a mismatched quotation mark in the docstring in the
    # standard library for this function, which results in the
    # sphinx documentation failing to build.
    # Overwrite the function to fix the docstring.
    return super().from_bytes(bytes, byteorder, signed=signed) # type: ignore

  def to_bytes(
      self,
      length: "typing.SupportsIndex" = 1,
      byteorder: "typing.Literal['little', 'big']" = "big",
      *,
      signed: bool = False) -> bytes:
    """Return an array of bytes representing an integer.

    Parameters
    ----------
    length
      Length of bytes object to use. An OverflowError is raised if the
      integer is not representable with the given number of bytes.
      Default is length 1.
    byteorder
      The byte order used to represent the integer.
      If byteorder is 'big', the most significant byte is at the beginning
      of the byte array. If byteorder is 'little', the most significant byte
      is at the end of the byte array. To request the native byte order of
      the host system, use 'sys.byteorder' as the byte order value.
      Default is to use 'big'.
    signed
      Determines whether two's complement is used to represent the integer.
      If signed is False and a negative integer is given, an OverflowError
      is raised.
    """
    # :HACK: There is a mismatched quotation mark in the docstring in the
    # standard library for this function, which results in the
    # sphinx documentation failing to build.
    # Overwrite the function to fix the docstring.
    return super().to_bytes(length, byteorder, signed=signed)


class TransientGeometryRestrictMode(FixedInteger32Mixin, enum.IntEnum):
  """Enumeration describing the possible restrictions on transient geometry.

  The options are:

  - No restrictions (show in all picked views).
  - Only shown in the specific view (after pick in that view).
  - Only shown in views that are not the specified view (after pick in that
    view).
  """
  NO_RESTRICTIONS = 0
  ONLY_IN_VIEW = 1
  NEVER_IN_VIEW = 2

  def from_bytes(
      self,
      # pylint: disable=redefined-builtin
      bytes,
      byteorder = "big",
      *,
      signed = False):
    """Return the integer represented by the given array of bytes.

    bytes
        Holds the array of bytes to convert. The argument must either
        support the buffer protocol or be an iterable object
        producing bytes. Bytes and bytearray are examples of built-in
        objects that support the buffer protocol.
    byteorder
        The byte order used to represent the integer. If byteorder is
        'big', the most significant byte is at the beginning of the
        byte array. If byteorder is 'little', the most significant
        byte is at the end of the byte array. To request the native
        byte order of the host system, use 'sys.byteorder' as the
        byte order value. Default is to use 'big'.
    signed
        Indicates whether two's complement is used to represent the integer.
    """
    # :HACK: There is a mismatched quotation mark in the docstring in the
    # standard library for this function, which results in the
    # sphinx documentation failing to build.
    # Overwrite the function to fix the docstring.
    return super().from_bytes(bytes, byteorder, signed=signed) # type: ignore

  def to_bytes(
      self,
      length: "typing.SupportsIndex" = 1,
      byteorder: "typing.Literal['little', 'big']" = "big",
      *,
      signed: bool = False) -> bytes:
    """Return an array of bytes representing an integer.

    Parameters
    ----------
    length
      Length of bytes object to use. An OverflowError is raised if the
      integer is not representable with the given number of bytes.
      Default is length 1.
    byteorder
      The byte order used to represent the integer.
      If byteorder is 'big', the most significant byte is at the beginning
      of the byte array. If byteorder is 'little', the most significant byte
      is at the end of the byte array. To request the native byte order of
      the host system, use 'sys.byteorder' as the byte order value.
      Default is to use 'big'.
    signed
      Determines whether two's complement is used to represent the integer.
      If signed is False and a negative integer is given, an OverflowError
      is raised.
    """
    # :HACK: There is a mismatched quotation mark in the docstring in the
    # standard library for this function, which results in the
    # sphinx documentation failing to build.
    # Overwrite the function to fix the docstring.
    return super().to_bytes(length, byteorder, signed=signed)


class TransientGeometrySettings(InlineMessage):
  """Settings for transient geometry.

  These affect how an object is treated when they are transient
  geometry.
  """
  is_clippable: bool = True
  is_pickable: bool = False
  is_selectable: bool = False
  is_initially_visible: bool =  True

  restrict_mode: TransientGeometryRestrictMode = \
    TransientGeometryRestrictMode.NO_RESTRICTIONS
  restricted_views: list[ObjectID] = []

  def __repr__(self):
    # This intentionally does not include every property, it is just enough to
    # summarise the basic settings. is_initially_visible for example is only
    # relevant when it is first added to the view so not hugely important.
    return f'{self.__class__.__qualname__}(' + \
      f'is_clippable={self.is_clippable}, is_pickable={self.is_pickable}, ' + \
      f'is_selectable={self.is_selectable})'


class ViewController:
  """Provides access onto a specified view.

  This allows for objects to be added/removed/shown and hidden.
  """
  def __init__(self, view_id: ObjectID[DataObject]):
    # In PointStudio 2020.1, there are no safe-guards in place to confirm that
    # the given view_id is infact an ID for a view and it exists. This will
    # simply crash.
    self._viewer = Viewer()
    maximum_length = 256
    server_name = ctypes.create_string_buffer(maximum_length)
    self._viewer.GetServerName(
      view_id.native_handle, server_name, maximum_length)
    if not server_name.value:
      error_message = self._viewer.ErrorMessage()
      if self._viewer.ErrorCode() == ViewerErrorCodes.VIEW_NO_LONGER_EXISTS:
        raise ViewNoLongerExists(error_message)
      raise ValueError(error_message)

    self.server_name = server_name.value.decode('utf-8')

    # Like the DataObject class provide the ability to query the ID of the
    # view controller.
    self.id = view_id
    self._manager = default_manager()

  def __repr__(self):
    return type(self).__name__ + f'({self.id}, "{self.server_name}")'

  @property
  def window_title(self) -> str:
    """Return the window title.

    This is the name of the view window as seen in the application.
    """

    class WindowTitle(Request):
      """Defines message for querying what window title of a view."""

      class WindowResponse(Response):
        """The response containing the window title."""
        title: str

      @classmethod
      def message_name(cls) -> str:
        return 'WindowTitle'

      @classmethod
      def response_type(cls) -> type[Response]:
        return cls.WindowResponse

      view_name: str

    request = WindowTitle(self._manager)
    request.view_name = self.server_name

    # The viewer server doesn't know its title as its the uiServer that
    # is responsible for that.
    response: WindowTitle.WindowResponse = request.send(
      'uiServer') # type: ignore
    return response.title

  def close(self):
    """Close the view.

    Avoid closing views that you didn't open, as such avoid closing the view
    if it came from a non-empty active view. This is because you may close a
    view that was being used by another tool in the application.

    A case where closing the view is a good idea is if the script creates one
    and is interactive and long-running. Think about when the script is done if
    the person running the script would miss seeing what is in the view, would
    find it a hassle to have to close it themself or if the content is no
    longer relevant after the script has exited.

    Examples
    --------
    Opens a new view then closes it.

    >>> import mapteksdk.operations as operations
    >>> project = Project()
    >>> view = operations.open_new_view()
    >>> input('Press enter to finish')
    >>> view.close()
    """
    class DestroyView(Message):
      """This message destroys (closes) the view."""
      @classmethod
      def message_name(cls) -> str:
        return 'DestroyView'

    DestroyView(self._manager).send(self.server_name)

  def scene_extents(self) -> Extent:
    """Return the scene extents of this view."""
    class SceneResponse(Response):
      """The response with the extents for the scene."""
      minimum: Point
      maximum: Point

    request = request_no_body('SceneExtent', SceneResponse, self._manager)
    response: SceneResponse = request.send(
      self.server_name) # type: ignore
    return Extent(response.minimum, response.maximum)

  def objects_in_view(
      self,
      object_filter: ObjectFilter=ObjectFilter.DEFAULT
      ) -> list[ObjectID]:
    """Return a list of objects that are in the the view.

    Parameters
    ----------
    object_filter : ObjectFilter
      A filter that limits what objects are returned.

    Returns
    -------
    list
      A list of object IDs of objects that are in the view that meet the filter
      criteria.
    """

    # TODO: Support filtering by object types.
    # Essentially support user providing list of type index or classes with
    # static_type function that returns a type index or a mix of both.
    #
    # This should ideally handle values of the form: [Surface, Polygon,
    # Polyline]
    # However receiving a message containing it would be problematic as its
    # not easy to map it back.

    class ObjectsInView(Request):
      """Defines message for querying what objects are in a view."""
      class InViewResponse(Response):
        """The response back with what objects are in a view."""
        objects: list[ObjectID[DataObject]]

      @classmethod
      def message_name(cls) -> str:
        return 'ObjectsInView'

      @classmethod
      def response_type(cls) -> type[Response]:
        return cls.InViewResponse

      object_filter: ObjectFilter
      type_filter: list[Int16u]

    request = ObjectsInView(self._manager)
    request.object_filter = object_filter
    request.type_filter = []

    response: ObjectsInView.InViewResponse = request.send(
      self.server_name) # type: ignore
    return response.objects

  def add_objects(
      self,
      objects: "Iterable[ObjectID | DataObject | str]"):
    """Adds the provided objects to the view.

    Parameters
    ----------
    objects
      A list of IDs of objects to add to the view.
    """

    class AddObjects(Message):
      """Message for the viewer for adding objects to it."""
      @classmethod
      def message_name(cls) -> str:
        return 'AddObjects'

      objects: list[ObjectID[DataObject]]
      drop_point: tuple[Double, Double] = (
        float('NaN'), float('NaN'))

    request = AddObjects(self._manager)
    request.objects = list(normalise_selection(objects))
    request.send(self.server_name)

  def add_object(self, object_to_add: "ObjectID | DataObject | str"):
    """Add a single object to the view.

    Parameters
    ----------
    object_to_add
      The object to add, the ObjectID of the object to add, or a path string
      for the object to add.
    """
    self.add_objects([object_to_add])

  def remove_objects(
      self,
      objects: "Iterable[ObjectID | DataObject | str]"):
    """Removes the provided objects from the view if present.

    Removing objects not in the view will do nothing.

    Parameters
    ----------
    objects
      A list of IDs of objects to remove from the view.
    """

    class RemoveObjects(Message):
      """Message for the viewer for removing objects from it."""
      @classmethod
      def message_name(cls) -> str:
        return 'RemoveObjects'

      objects: list[ObjectID[DataObject]]

    request = RemoveObjects(self._manager)
    request.objects = list(normalise_selection(objects))
    request.send(self.server_name)

  def remove_object(
      self, object_to_remove: "ObjectID | DataObject | str"):
    """Remove a single object from the view.

    Parameters
    ----------
    object_to_remove
      The object to remove, the ObjectID of the object to remove, or a path
      string for the object to remove.
    """
    self.remove_objects([object_to_remove])

  def hide_objects(
      self,
      objects: "Iterable[ObjectID | DataObject | str]"):
    """Hide the provided objects in the view.

    Hiding objects not in the view will do nothing.

    Parameters
    ----------
    objects
      A list of IDs of objects to hide.
    """

    if self._viewer.version >= (1, 1):
      class HideObjects(Message):
        """Message for the viewer for hiding objects."""
        @classmethod
        def message_name(cls) -> str:
          return 'HideObjects'

        objects: list[ObjectID[DataObject]]
        mouse: tuple[Double, Double] = (
          float('NaN'), float('NaN'))
    else:
      class HideObjects(Message):
        """Message for the viewer for hiding objects."""
        @classmethod
        def message_name(cls) -> str:
          return 'HideObjects'

        objects: list[ObjectID[DataObject]]

    request = HideObjects(self._manager)
    request.objects = list(normalise_selection(objects))
    request.send(self.server_name)

  def hide_object(
      self, object_to_hide: "ObjectID | DataObject | str"):
    """Hide a single object in the view.

    Parameters
    ----------
    object_to_hide
      The object to hide, the ObjectID of the object to hide, or a path string
      for the object to hide.
    """
    self.hide_objects([object_to_hide])

  def show_objects(
      self,
      objects: "Iterable[ObjectID | DataObject | str]"):
    """Show the provided objects in the view (if hidden).

    If the objects are not in the view then they won't be shown.

    Parameters
    ----------
    objects
      A list of IDs of objects to hide.
    """

    class ShowObjects(Message):
      """Message for the viewer for showing objects."""
      @classmethod
      def message_name(cls) -> str:
        return 'ShowObjects'

      objects: list[ObjectID[DataObject]]

    request = ShowObjects(self._manager)
    request.objects = list(normalise_selection(objects))
    request.send(self.server_name)

  def show_object(
      self, object_to_show: "ObjectID | DataObject | str"):
    """Show a single hidden object in the view.

    Parameters
    ----------
    object_to_show
      The object to show, the ObjectID of the object to show, or a path string
      for the object to show.
    """
    self.show_objects([object_to_show])

  def add_transient_object(
      self,
      object_to_add: "ObjectID | DataObject | str",
      settings: TransientGeometrySettings = TransientGeometrySettings()):
    """Add a single object to the view as a transient object.

    Transient objects by default are not pickable or selectable. They
    are typically used to show a preview of some operation.

    You are responsible for removing the object from the view when you are
    done with it (or if you opened the view then close the view). The object
    should not be left in the view after you are done with it as this will
    leave the user with only the option of closing the view to get rid of it
    themselves. If you promote the transient object then it doesn't need to
    be removed.

    Parameters
    ----------
    object_to_add
      The object to add, the ObjectID of the object to add, or a path string
      for the object to add.
    settings
      The transient geometry settings that apply to the object_to_add.

    See Also
    --------
    remove_object : To remove the object from the view.
    promote_transient_object : To promote the transient object.
    """
    self.add_transient_objects([object_to_add], settings)

  def add_transient_objects(
      self,
      objects: "Iterable[ObjectID | DataObject | str]",
      settings: TransientGeometrySettings = TransientGeometrySettings()):
    """Adds the provided objects to the view as transient objects.

    Transient objects by default are not pickable or selectable. They
    are typically used to show a preview of some operation.

    You are responsible for removing the object from the view when you are
    done with it (or if you opened the view then close the view). The object
    should not be left in the view after you are done with it as this will
    leave the user with only the option of closing the view to get rid of it
    themselves. If you promote the transient object then it doesn't need to
    be removed.

    Parameters
    ----------
    objects
      A list of IDs of objects to add to the view.
    settings
      The transient geometry settings that apply to objects.

    See Also
    --------
    remove_objects : To remove the object from the view.
    promote_transient_objects : To promote transient objects.
    """
    class AddTransientGeometry(Message):
      """Message for the viewer for adding  transient objects to it."""
      @classmethod
      def message_name(cls) -> str:
        return 'AddTransientGeometry'
      objects: list[ObjectID[DataObject]]
      settings: TransientGeometrySettings

    request = AddTransientGeometry(self._manager)
    request.objects = list(normalise_selection(objects))
    request.settings = settings
    request.send(self.server_name)

  def promote_transient_object(
      self,
      data_object: "ObjectID | DataObject | str"):
    """Promote a transient object to being a permanent object.

    This is relevant to the view only, to ensure the geometry persists it
    should be added to the project.
    """
    self.promote_transient_objects([data_object])

  def promote_transient_objects(
      self,
      objects: "Iterable[ObjectID | DataObject | str]"):
    """Promote transient objects to being permanent objects.

    This is relevant to the view only, to ensure the objects persists they
    should be added to the project.
    """
    class PromoteTransientGeometry(Message):
      """Message for the viewer for adding  transient objects to it."""
      @classmethod
      def message_name(cls) -> str:
        return 'PromoteTransientGeometry'
      objects: list[ObjectID[DataObject]]

    request = PromoteTransientGeometry(self._manager)
    request.objects = list(normalise_selection(objects))
    request.send(self.server_name)

  def transient_objects_in_view(self) -> \
      list[tuple[ObjectID[DataObject], TransientGeometrySettings]]:
    """
    Return the transient objects that are in the the view and their settings.

    Returns
    -------
    list
      A list of each transient object and their corresponding settings.
    """
    class TransientObjectsInView(Request):
      """Message for the viewer for querying transient objects in it."""
      class TransientResponse(Response):
        """The response back with what transient objects are in a view."""
        object_groups: list[list[ObjectID[DataObject]]]
        settings: list[TransientGeometrySettings]

      @classmethod
      def message_name(cls) -> str:
        return 'TransientObjectsInView'

      @classmethod
      def response_type(cls) -> type[Response]:
        return cls.TransientResponse

    request = TransientObjectsInView(self._manager)
    response: TransientObjectsInView.TransientResponse = request.send(
      self.server_name) # type: ignore

    # Flatten out the list also known as de-grouping them as the objects were
    # grouped together.
    result = []
    for objects, settings in zip(response.object_groups, response.settings):
      for transient_object in objects:
        result.append((transient_object, copy.deepcopy(settings)))
    return result

  def action_plane_section_widths(self) -> tuple[float, float]:
    """Return the widths of the section in this view."""
    class SectionWidthResponse(Response):
      """The response containing the section widths."""
      back: Double
      front: Double

    request = request_no_body('ActionPlaneSectionWidths', SectionWidthResponse, self._manager)
    response: SectionWidthResponse = request.send(
      self.server_name) # type: ignore
    return (response.back, response.front)

  def set_action_plane_section_widths(
      self, back_width: float, front_width: float):
    """Change the section width of the view.

    This will only take affect if view's section mode is not
    SectionMode.NO_MODE.

    It is typical for the same width to be given for both the front and back.

    Parameters
    ----------
    back_width
        The width of the section from the action plane to the back.
    front_width
        The width of the section from the action plane to the front.

    See Also
    --------
    action_plane_section_mode : Query the current section mode
    set_action_plane_section_mode : Set the current section modes (enable
        sectioning)
    """
    class SetActionPlaneSectionWidths(Message):
      """Message for changing the section width."""
      @classmethod
      def message_name(cls) -> str:
        return 'SetActionPlaneSectionWidths'
      back: Double
      front: Double

    message = SetActionPlaneSectionWidths(self._manager)
    message.back = back_width
    message.front = front_width
    message.send(self.server_name)

  def action_plane_section_mode(self) -> SectionMode:
    """Return the current selection mode of this view."""
    class SectionModeResponse(Response):
      """The response containing the section mode."""
      section_mode: Int32s  # vwrE_SectionMode.

    request = request_no_body('ActionPlaneSectionMode', SectionModeResponse, self._manager)
    response: SectionModeResponse = request.send(
      self.server_name) # type: ignore
    return SectionMode(response.section_mode)

  def set_action_plane_section_mode(self, section_mode: SectionMode):
    """Change the view's section mode to the mode given.

    Parameters
    ----------
    section_mode
        The section mode to change to.

    Examples
    --------
    Turn on sectioning in the current view.

    >>> from mapteksdk.project import Project
    >>> from mapteksdk.operations import active_view
    >>> from mapteksdk.view import SectionMode
    >>> project = Project()
    >>> view = active_view()
    >>> view.set_action_plane_section_mode(SectionMode.STRIP)

    Turn off sectioning in the current view.

    >>> from mapteksdk.project import Project
    >>> from mapteksdk.operations import active_view
    >>> from mapteksdk.view import SectionMode
    >>> project = Project()
    >>> view = active_view()
    >>> view.set_action_plane_section_mode(SectionMode.NO_MODE)
    """
    class SetActionPlaneSectionMode(Message):
      """Message for changing the section mode."""
      @classmethod
      def message_name(cls) -> str:
        return 'SetActionPlaneSectionMode'
      section_mode: Int32s

    message = SetActionPlaneSectionMode(self._manager)
    message.section_mode = section_mode
    message.send(self.server_name)

  def action_plane(self) -> Plane:
    """Return the action plane in this view."""
    class ActionPlaneResponse(Response):
      """The response containing the action plane and more."""
      action_plane: _ActionPlane

    request = request_no_body('ActionPlane', ActionPlaneResponse, self._manager)
    response: ActionPlaneResponse = request.send(
      self.server_name) # type: ignore

    return response.action_plane.plane

  def set_action_plane(self, plane: Plane):
    """Set the action plane in this view.

    Parameters
    ----------
    plane
      The plane to use for the action plane.
    """
    class SetActionPlane(Message):
      """The message to set the action plane of the view this is sent to."""
      @classmethod
      def message_name(cls) -> str:
        return 'SetActionPlane'

      action_plane: _ActionPlane

    message = SetActionPlane(self._manager)
    message.action_plane = _ActionPlane()
    message.action_plane.plane = plane
    message.send(self.server_name)

  def action_plane_section_step_distance(self) -> float:
    """The distance that the action plane will move if it is stepped by."""
    class StepDistanceResponse(Response):
      """The response containing the step distance."""
      step_distance: Double

    request = request_no_body(
      'ActionPlaneSectionStepDistance', StepDistanceResponse, self._manager)
    response: StepDistanceResponse = request.send(
      self.server_name) # type: ignore
    return response.step_distance

  def set_action_plane_section_step_distance(self, step_distance: float):
    """Change the section step distance of the view.

    Parameters
    ----------
    step_distance
        The distance to step forward/back with the section.

    See Also
    --------
    step_action_plane_section_forwards : Step forwards by the last distance.
    step_action_plane_section_backwards : Step backwards by the last distance.
    """
    class SetStepDistance(Message):
      """Message for changing the section step distance."""
      @classmethod
      def message_name(cls) -> str:
        return 'SetActionPlaneSectionStepDistance'
      step_distance: Double

    message = SetStepDistance(self._manager)
    message.step_distance = step_distance
    message.send(self.server_name)

  def step_action_plane_section_forwards(self):
    """Step (moves) the action plane forwards.

    The distance the plane will move is based on the last set step distance for
    the view.

    See Also
    --------
    set_action_plane_section_step_distance : Set the step distance.
    step_action_plane_section_backwards : Step in the other direction.
    """
    self._step_action_plane_section(SectionStepDirection.LEFT_AND_UP)

  def step_action_plane_section_backwards(self):
    """Step (moves) the action plane backwards.

    The distance the plane will move is based on the last set step distance for
    the view.

    See Also
    --------
    set_action_plane_section_step_distance : Set the step distance.
    step_action_plane_section_forwards : Step in the other direction.
    """
    self._step_action_plane_section(SectionStepDirection.RIGHT_AND_DOWN)

  def view_objects_by_extents(self,
                              extent: Extent,
                              look_direction: Sequence[float],
                              up_direction: Sequence[float]):
    """Change the camera such that it views all data in extent.

    Use this to move the camera to view a specific object (or objects), based on
    its (or their) extents.

    The camera will be looking at the centre of the extent from a point
    sufficiently far from the centre such that the entire extent will be visible
    in perspective projection, and a sufficiently large linear field of view to
    see the entire extent when in orthographic projection.

    The specified look_direction and up_direction will be taken into account.

    Parameters
    ----------
    extent
      The extent of the objects that the view should focus on.
    look_direction
      The look direction is in the direction the camera should be looking and
      is from the camera towards to point of interest and should be towards
      the extent.
    up_direction
      The up direction is a vector that points up relative to the camera,
      typically towards the sky and affects the camera's tilt and roll.
    """
    rotation = Rotation.create_from_look_and_up_direction(look_direction,
                                                          up_direction)

    class ViewObjectByExtents(Message):
      """A message for the viewer server to change the camera."""
      extent_minimum: Point
      extent_maximum: Point
      rotation: tuple[Double, Double, Double, Double]
      any_orientation: bool = False

      @classmethod
      def message_name(cls) -> str:
        return "ViewObjectByExtents"

    message = ViewObjectByExtents(self._manager)
    message.extent_minimum = extent.minimum
    message.extent_maximum = extent.maximum
    message.rotation = rotation.quaternion
    message.send(self.server_name)

  @property
  def background_colour(self) -> tuple[int, int, int, int]:
    """The background colour of the view window.

    This is represented as a tuple containing red, green, blue, alpha values
    of the colour.
    Each value is an integer in the range [0, 255].

    When changing the background colour, the alpha is optional and
    the colour may be given as either a tuple, list or ndarray.
    """

    class RequestBackgroundColour(Request):
      """Query background colour of a view window."""
      class BackgroundColourResponse(Response):
        """Response to a request background colour request"""
        colour: Int32u

      @classmethod
      def message_name(cls) -> str:
        return 'BackgroundColour'

      @classmethod
      def response_type(cls) -> type[BackgroundColourResponse]:
        return cls.BackgroundColourResponse

    request = RequestBackgroundColour(self._manager)
    response: RequestBackgroundColour.BackgroundColourResponse = request.send(
      self.server_name) # type: ignore

    alpha = (response.colour >> 24) & 0xFF
    blue = (response.colour >> 16) & 0xFF
    green = (response.colour >> 8) & 0xFF
    red = response.colour & 0xFF

    return (red, green, blue, alpha)

  @background_colour.setter
  def background_colour(self, new_colour: Sequence[int]):
    # This could be useful when detecting if really dark coloured objects are
    # in the view and switching the background so it is lighter colour to
    # give contrast between foreground and background.
    #
    # It could also be possible to implement a night-light like application
    # which reduces specific colours used in the background as the time of day
    # changes.

    class SetBackgroundColour(Message):
      """Sets the background colour of a view window."""
      @classmethod
      def message_name(cls) -> str:
        return 'SetBackgroundColour'

      colour: Int32u

    red, green, blue = new_colour[:3]
    if len(new_colour) == 4:
      alpha = new_colour[3]
    else:
      alpha = 255

    # Colour encoded as a 32-bit integer. This more than likely needs
    # to be packaged up as part of the comms module.
    colour = (alpha << 24) | (blue << 16) | (green << 8) | (red << 0)

    message = SetBackgroundColour(self._manager)
    message.colour = colour
    message.send(self.server_name)

  def _start_camera_transition(self, transition_time: float):
    """Enables the camera to smoothly transition to a new state

    Parameters
    ----------
    transition_time
      The time the transition should last in seconds.
    """
    class StartTransition(Message):
      """Tells the viewer that it will be transitioning the camera to a new
      location.
      """
      @classmethod
      def message_name(cls) -> str:
        return 'StartTransition'

      axes_transition_mode: Int32s = 2
      transition_time: Double

    message = StartTransition(self._manager)
    message.transition_time = transition_time
    message.send(self.server_name)

  def _step_action_plane_section(self, direction: SectionStepDirection):
    """Step the action plane section in the given direction.

    The distance the plane will move is based on the last set step distance for
    the view.

    Parameters
    ----------
    direction
      The direction to step the section.
    """
    class StepActionPlaneSection(Message):
      """Message that causes the view to step the action plane in a direction.
      """
      @classmethod
      def message_name(cls) -> str:
        return 'StepActionPlaneSection'
      step_direction: Int32s

    message = StepActionPlaneSection(self._manager)
    message.step_direction = direction
    message.send(self.server_name)

  def _scale_linear_field_of_view(self, scale: float):
    """Apply a relative linear field of view to this view.

    Parameters
    ----------
    scale
      The scaling factor to apply to the linear field of view.
    """
    class ScaleLinearFieldOfView(Message):
      """Scale the linear field of view."""
      scale: Double

      @classmethod
      def message_name(cls) -> str:
        return "ScaleLinearFieldOfView"

    message = ScaleLinearFieldOfView(self._manager)
    message.scale = scale
    message.send(self.server_name)


class _ActionPlane(InlineMessage):
  """An action plane is a plane set in a view.

  It is used for digitising points and describing the plane to use for
  quickly setting up clip plane sectioning data.
  """
  plane_coefficient_a: Double
  plane_coefficient_b: Double
  plane_coefficient_c: Double
  plane_coefficient_d: Double

  visualisation_centroid_x: Double = float('NaN')
  visualisation_centroid_y: Double = float('NaN')
  visualisation_centroid_z: Double = float('NaN')

  grid_orientation_x: Double = float('NaN')
  grid_orientation_y: Double = float('NaN')
  grid_orientation_z: Double = float('NaN')

  @property
  def plane(self) -> Plane:
    """The plane portion of the action plane."""
    return Plane(self.plane_coefficient_a,
                 self.plane_coefficient_b,
                 self.plane_coefficient_c,
                 self.plane_coefficient_d)

  @plane.setter
  def plane(self, plane: Plane):
    """The plane portion of the action plane."""
    self.plane_coefficient_a = plane.coefficient_a
    self.plane_coefficient_b = plane.coefficient_b
    self.plane_coefficient_c = plane.coefficient_c
    self.plane_coefficient_d = plane.coefficient_d


def _choose_better_camera_for_image(view: ViewController):
  """Choose a better camera based on the data given.

  The default camera is top-down which works well for data that should be
  viewed in plan view. However, other data doesn't look great from that view.

  The idea is to choose a better camera orientation based on the data. If the
  object was the Standford Bunny then rather than top-down it will be front
  on.

  Parameters
  ----------
  view
    The view controller to apply the better camera to for taking an image.
  """
  extent = view.scene_extents()
  span_x, span_y, span_z = extent.span

  if span_z < 0.00001 and span_z > -0.00001:
    return

  ratio_xz = span_x / span_z
  ratio_yz = span_y / span_z

  if ratio_xz < 10 or ratio_yz < 10:
    # Use a different orientation.
    look_vector = (1.0, 1.0, -0.5)
    up_vector = (0.25, 0.25, 1)

    view.view_objects_by_extents(extent, look_vector, up_vector)

    # Since this is for an image rather than an interactive view, it can be
    # zoomed in as it doesn't need to allow the data to fit in the view
    # after it has been rotated, which is what view_objects_by_extents()
    # does.
    view._scale_linear_field_of_view(0.8)
