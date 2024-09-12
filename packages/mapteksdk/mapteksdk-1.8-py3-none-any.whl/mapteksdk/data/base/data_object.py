"""The base classes of all objects in a Project."""
###############################################################################
#
# (C) Copyright 2024, Maptek Pty Ltd. All rights reserved.
#
###############################################################################
from __future__ import annotations

import ctypes
import dataclasses
import datetime
import logging
import typing

from ..change_reasons import ChangeReasons
from ..errors import (
  CannotSaveInReadOnlyModeError,
  ReadOnlyError,
  AlreadyOpenedError
)
from ..objectid import ObjectID
from ...capi import DataEngine, Modelling
from ...internal.lock import LockType, ReadLock, WriteLock

if typing.TYPE_CHECKING:
  from collections.abc import Callable

  ObjectAttributeTypes = (
    None | ctypes.c_bool | ctypes.c_int8 | ctypes.c_uint8
    | ctypes.c_int16 | ctypes.c_uint16 | ctypes.c_int32 | ctypes.c_uint32
    | ctypes.c_int64 | ctypes.c_uint64 | ctypes.c_float | ctypes.c_double
    | ctypes.c_char_p | datetime.datetime | datetime.date
  )
  """Alias for the union of valid ctypes types for object attributes."""

  ObjectAttributeTypesWithAlias = (
    ObjectAttributeTypes | bool | str | int | float
  )
  """Object attribute types plus Python types which alias common types.

  For convenience some functions treat certain Python types as aliases
  for C types. The aliases are displayed in the following tables.

  +-------------+-----------------+
  | Python type | C type          |
  +=============+=================+
  | bool        | ctypes.c_bool   |
  +-------------+-----------------+
  | str         | ctypes.c_char_p |
  +-------------+-----------------+
  | int         | ctypes.c_int16  |
  +-------------+-----------------+
  | float       | ctypes.c_double |
  +-------------+-----------------+

  Notes
  -----
  The above table only applies for object-level attributes.
  """

  ObjectAttributeDataTypes = type[ObjectAttributeTypes] | None
  """Alias for the union of valid data types for object attributes."""


log = logging.getLogger("mapteksdk.data")

@dataclasses.dataclass
class _ObjectAttribute:
  """Holds data for an object attribute."""
  name : str
  """The name of the object attribute."""
  id : int
  """The ID of the object attribute."""
  dtype : ObjectAttributeDataTypes
  """The data type of the object attribute."""
  value : typing.Any
  """The data stored in this attribute.

  This is None by default.
  """


class DataObject:
  """The basic unit of data in a Project.

  Each object can be referenced (opened/loaded) from its ID, see `ObjectID`,
  `Project.read()` and `Project.edit()`.
  """

  # This corresponds to C++ type called mdf::deC_Object.

  _object_attribute_table: dict[int, ObjectAttributeDataTypes] = {
    0: None, 1: type(None), 2: ctypes.c_bool, 3: ctypes.c_int8,
    4: ctypes.c_uint8, 5: ctypes.c_int16, 6: ctypes.c_uint16,
    7: ctypes.c_int32, 8: ctypes.c_uint32, 9: ctypes.c_int64,
    10: ctypes.c_uint64, 11: ctypes.c_float, 12: ctypes.c_double,
    13: ctypes.c_char_p, 14: datetime.datetime, 15: datetime.date,
  }
  """Dictionary which maps object attribute type ids to Python types."""

  def __init__(self, object_id: ObjectID, lock_type: LockType, *,
               rollback_on_error: bool = False):
    """Opens the object for read or read-write.

    It is recommended to go through `Project.read()` and `Project.edit()`
    instead of constructing this object directly.

    Parameters
    ----------
    object_id
      The ID of the object to open for read or read-write.
    lock_type
      Specify read/write operation intended for the
      lifespan of this object instance.
    rollback_on_error
      When true, changes should be rolled back if there is an error.
    """
    assert object_id
    self.__id: ObjectID = object_id
    self.__lock_type: LockType = lock_type
    self.__object_attributes: dict[
      str, _ObjectAttribute] | None = None
    self.__lock_opened = False
    self._lock: ReadLock | WriteLock = self.__begin_lock(rollback_on_error)

  @classmethod
  def static_type(cls):
    """Return this type as stored in a Project."""
    raise NotImplementedError(
      "Static type must be implemented on child classes.")

  @property
  def id(self) -> ObjectID[typing.Self]:
    """Object ID that uniquely references this object in the project.

    Returns
    -------
    ObjectID
      The unique id of this object.
    """
    return self.__id

  @property
  def closed(self) -> bool:
    """If this object has been closed.

    Attempting to read or edit a closed object will raise an ObjectClosedError.
    Such an error typically indicates an error in the script and should not
    be caught.

    Examples
    --------
    If the object was opened with the Project.new(), Project.edit() or
    Project.read() in a "with" block, this will be True until the with
    block is closed and False afterwards.

    >>> with project.new("cad/point_set", PointSet) as point_set:
    >>>     point_set.points = [[1, 2, 3], [4, 5, 6]]
    >>>     print("closed?", point_set.closed)
    >>> print("closed?", point_set.closed)
    closed? False
    closed? True
    """
    return self._lock.is_closed

  @property
  def is_read_only(self) -> bool:
    """If this object is read-only.

    This will return True if the object was open with Project.read()
    and False if it was open with Project.edit() or Project.new().
    Attempting to edit a read-only object will raise an error.
    """
    return self.lock_type is not LockType.READWRITE

  @property
  def lock_type(self) -> LockType:
    """Indicates whether operating in read-only or read-write mode.

    Use the is_read_only property instead for checking if an object
    is open for reading or editing.

    Returns
    -------
    LockType
      The type of lock on this object. This will be LockType.ReadWrite
      if the object is open for editing and LockType.Read if the object
      is open for reading.
    """
    return self.__lock_type

  @staticmethod
  def _modelling_api() -> Modelling:
    """Access the modelling C API."""
    return Modelling()

  @staticmethod
  def _data_engine_api() -> DataEngine:
    """Access the DataEngine C API."""
    return DataEngine()

  def _invalidate_properties(self):
    """Invalidates the properties of the object.

    The next time a property is requested, its values will be loaded from the
    project.
    """
    self._extra_invalidate_properties()

  def _extra_invalidate_properties(self):
    """Invalidate properties defined by the child class.

    This is called during _invalidate_properties() and should never
    be called directly.
    Child classes must implement this to invalidate the properties
    they define. They must not overwrite _invalidate_properties().
    """
    raise NotImplementedError(
      "_extra_invalidate_properties must be implemented on child classes"
    )

  # Child classes should place their child-specific function in _save()
  # instead of overwriting or overriding save().
  @typing.final
  def save(self) -> ChangeReasons:
    """Save the changes made to the object.

    Generally a user does not need to call this function, because it is called
    automatically at the end of a with block using Project.new() or
    Project.edit().

    Returns
    -------
    ChangeReasons
      The change reasons for the operation. This depends on what changes
      to the object were saved.
      If the api_version is less than 1.9, this always returns
      ChangeReasons.NO_CHANGE.
    """
    self._raise_if_save_in_read_only()
    self._save()
    self._invalidate_properties()
    return self._checkpoint()

  def _save(self):
    """Save the properties defined by the child class.

    This is called during save() and should never be called directly.
    Child classes must implement this to save the properties they define.
    They must not overwrite save().
    """
    raise NotImplementedError("_save() must be implemented on child classes")

  def close(self):
    """Closes the object.

    This should be called as soon as you are finished working with an object.
    To avoid needing to remember to call this function, open the object using
    a with block and project.read(), project.new() or project.edit().
    Those functions automatically call this function at the end of the with
    block.

    A closed object cannot be used for further reading or writing. The ID of
    a closed object may be queried and this can then be used to re-open the
    object.
    """
    self.__end_lock()

  def _checkpoint(self) -> ChangeReasons:
    """Checkpoint the saved changes to the object.

    This makes the changes to the object saved by save() visible to
    readers of the lock.
    """
    self._raise_if_read_only("Save changes")
    return ChangeReasons(self._data_engine_api().Checkpoint(self._lock.lock))

  def _raise_if_read_only(self, operation: str):
    """Raise a ReadOnlyError if this object is open for read-only.

    The message is: "Cannot {operation} in read-only mode".

    Parameters
    ----------
    operation
      The operation which cannot be done in read-only mode.
      This should not start with a capital letter and should describe
      what operation cannot be performed in read-only mode.

    Raises
    ------
    ReadOnlyError
      If this object is open for read-only.
    """
    if self.is_read_only:
      raise ReadOnlyError(f"Cannot {operation} in read-only mode.")

  def _raise_if_save_in_read_only(self):
    """Raise a CannotSaveInReadOnlyModeError if open for read-only.

    This should be called in the save() function of child classes.

    Raises
    ------
    CannotSaveInReadOnlyModeError
      If this object is open for read-only.
    """
    if self.is_read_only:
      error = CannotSaveInReadOnlyModeError()
      log.error(error)
      raise error

  def __begin_lock(self, rollback_on_error: bool) -> ReadLock | WriteLock:
    if self.__lock_opened:
      raise AlreadyOpenedError(
        "This object has already been opened. After closing the object, you "
        "should start a new context manager using the with statement.")
    self.__lock_opened = True
    lock: ReadLock | WriteLock
    if self.__lock_type is LockType.READWRITE:
      lock = WriteLock(
        self.__id.handle,
        self._data_engine_api(),
        rollback_on_error=rollback_on_error
      )
      log.debug("Opened object for writing: %s of type %s",
                self.__id, self.__derived_type_name)
    else:
      lock = ReadLock(self.__id.handle, self._data_engine_api())
      log.debug("Opened object for reading: %s of type %s",
                self.__id, self.__derived_type_name)
    return lock

  def __end_lock(self):
    if not self.closed:
      self._lock.close()
      if self.__lock_type is LockType.READWRITE:
        log.debug("Closed object for writing: %s of type %s",
                  self.__id, self.__derived_type_name)
      else:
        log.debug("Closed object for reading: %s of type %s",
                  self.__id, self.__derived_type_name)

  def __enter__(self) -> typing.Self:
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    """Close the object. See close()"""
    self.close()

  @property
  def __derived_type_name(self) -> str:
    """Return qualified name of the derived object type."""
    return type(self).__qualname__

  def __repr__(self) -> str:
    return f'{self.__derived_type_name}({self.__id})'

  # =========================================================================
  # Properties of the underlying object in the project.
  # =========================================================================

  @property
  def created_date(self) -> datetime.datetime:
    """The date and time (in UTC) of when this object was created.

    Returns
    -------
    datetime.datetime:
      The date and time the object was created.
      0:0:0 1/1/1970 if the operation failed.
    """
    value = ctypes.c_int64() # value provided in microseconds
    success = self._data_engine_api().GetObjectCreationDateTime(
      self._lock.lock, ctypes.byref(value))
    if success:
      try:
        return datetime.datetime.fromtimestamp(float(value.value) / 1000000,
                                               datetime.timezone.utc).replace(
                                                 tzinfo=None)
      except (OSError, OverflowError) as error:
        message = str(error)
    else:
      message = self._data_engine_api().ErrorMessage().decode('utf-8')

    log.warning(
      'Failed to determine the creation date of object %s because %s',
      self.id, message)
    return datetime.datetime.fromtimestamp(0, datetime.timezone.utc).replace(
      tzinfo=None)

  @property
  def modified_date(self) -> datetime.datetime:
    """The date and time (in UTC) of when this object was last modified.

    Returns
    -------
    datetime.datetime
      The date and time this object was last modified.
      0:0:0 1/1/1970 if the operation failed.
    """
    value = ctypes.c_int64() # value provided in microseconds
    success = self._data_engine_api().GetObjectModificationDateTime(
      self._lock.lock, ctypes.byref(value))
    if success:
      return datetime.datetime.fromtimestamp(float(value.value) / 1000000,
                                             datetime.timezone.utc).replace(
                                               tzinfo=None)

    message = self._data_engine_api().ErrorMessage().decode('utf-8')
    log.warning(
      'Failed to determine the last modified date of object %s because %s',
      self.id, message)
    return datetime.datetime.fromtimestamp(0, datetime.timezone.utc).replace(
      tzinfo=None)

  @property
  def _revision_number(self) -> int:
    """The revision number of the object.

    This is incremented when save() is called or when the object is closed
    by project.edit() (assuming a change was made).

    If the application is too old to support this, the revision number
    will always be zero.

    Warnings
    --------
    The revision number is not stored persistently. If a maptekdb is
    closed and reopened, the revision number for each object will reset
    to one.
    """
    return self._data_engine_api().GetObjectRevisionNumber(self._lock.lock) or 0

  @property
  def _object_attributes(self) -> dict[str, _ObjectAttribute]:
    """Property for accessing the object attributes.

    When first called, the names of all object attributes are cached.
    """
    if self.__object_attributes is None:
      self.__object_attributes = self.__construct_attribute_dictionary()
    return self.__object_attributes

  @typing.overload
  def set_attribute(
      self,
      name: str,
      dtype: type[datetime.date],
      data: datetime.date | tuple[float, float, float]):
    ...

  @typing.overload
  def set_attribute(
      self,
      name: str,
      dtype: type[datetime.datetime],
      data: datetime.datetime | str):
    ...

  @typing.overload
  def set_attribute(
      self,
      name: str,
      dtype: type[int],
      data: int):
    ...

  @typing.overload
  def set_attribute(
      self,
      name: str,
      dtype: type[float],
      data: float):
    ...

  @typing.overload
  def set_attribute(
      self,
      name: str,
      dtype: type[bool],
      data: bool):
    ...

  @typing.overload
  def set_attribute(
      self,
      name: str,
      dtype: type[str],
      data: str):
    ...

  @typing.overload
  def set_attribute(
      self,
      name: str,
      dtype: ObjectAttributeDataTypes,
      data: ObjectAttributeTypesWithAlias):
    ...

  def set_attribute(
      self,
      name: str,
      dtype: ObjectAttributeDataTypes | type[
        datetime.datetime | datetime.date | bool |
        int | float | str],
      data: typing.Any):
    """Sets the value for the object attribute with the specified name.

    This will overwrite any existing attribute with the specified name.

    Parameters
    ----------
    name
      The name of the object attribute for which the value should be set.
    dtype
      The type of data to assign to the attribute. This should be
      a type from the ctypes module or datetime.datetime or datetime.date.
      Passing bool is equivalent to passing ctypes.c_bool.
      Passing str is equivalent to passing ctypes.c_char_p.
      Passing int is equivalent to passing ctypes.c_int16.
      Passing float is equivalent to passing ctypes.c_double.
    data
      The value to assign to object attribute `name`.
      For `dtype` = datetime.datetime this can either be a datetime
      object or timestamp which will be passed directly to
      datetime.fromtimestamp().
      For `dtype` = datetime.date this can either be a date object or a
      tuple of the form: (year, month, day).

    Raises
    ------
    ValueError
      If `dtype` is an unsupported type.
    TypeError
      If `value` is an inappropriate type for object attribute `name`.
    ValueError
      If `name` starts or ends with whitespace or is empty.
    RuntimeError
      If a different error occurs.

    Notes
    -----
    If an error occurs after adding a new object attribute or editing
    an existing object attribute resulting in save() not being called,
    the changes to the object attributes can only be undone if
    the application's API version is 1.6 or greater.

    Prior to mapteksdk 1.6:
    Adding new object attributes, or editing the values of object
    attributes, will not be undone if an error occurs.

    Examples
    --------
    Create an object attribute on an object at "target" and then read its
    value.

    >>> import ctypes
    >>> from mapteksdk.project import Project
    >>> project = Project()
    >>> with project.edit("target") as edit_object:
    ...     edit_object.set_attribute("count", ctypes.c_int16, 0)
    ... with project.read("target") as read_object:
    ...     print(read_object.get_attribute("count"))
    0
    """
    self._raise_if_read_only("set object attributes")
    if name.strip() != name:
      raise ValueError(
        "Attribute names must not contain leading or trailing whitespace. "
        f"Invalid attribute name: '{name}'."
      )
    if name == "":
      raise ValueError(
        "Attribute name must not be empty."
      )
    attribute_id = self._data_engine_api().GetAttributeId(name.encode("utf-8"))

    actual_dtype: ObjectAttributeDataTypes
    if dtype is bool:
      actual_dtype = ctypes.c_bool
    elif dtype is str:
      actual_dtype = ctypes.c_char_p
    elif dtype is int:
      actual_dtype = ctypes.c_int16
    elif dtype is float:
      actual_dtype = ctypes.c_double
    else:
      # Pylance is only type narrowing on the if and ignoring the intermediate
      # elif blocks resulting in a false positive for static type checking here.
      actual_dtype = dtype # type: ignore

    if (actual_dtype is datetime.datetime
        and not isinstance(data, datetime.datetime)):
      data = datetime.datetime.fromtimestamp(data, datetime.timezone.utc)
      data = data.replace(tzinfo=None)  # Remove timezone awareness.

    if actual_dtype is datetime.date and not isinstance(data, datetime.date):
      data = datetime.date(data[0], data[1], data[2])

    try:
      result = self.__save_attribute(attribute_id,
                                     actual_dtype,
                                     data)
    except ctypes.ArgumentError as exception:
      raise TypeError(f"Cannot convert {data} of type {type(data)} to "
                      f"type: {dtype}.") from exception
    except AttributeError as exception:
      raise TypeError(f"Cannot convert {data} of type {type(data)} to "
                      f"type: {dtype}.") from exception

    if not result:
      message = self._data_engine_api().ErrorMessage().decode('utf-8')
      raise RuntimeError(f"Failed to save attribute: '{name}' on object "
                         f"'{self.id}'. {message}")

    if name in self._object_attributes:
      self._object_attributes[name].value = data
      self._object_attributes[name].dtype = actual_dtype
      self._object_attributes[name].id = attribute_id
    else:
      self._object_attributes[name] = _ObjectAttribute(name, attribute_id,
                                                       actual_dtype, data)

  def attribute_names(self) -> list[str]:
    """Returns a list containing the names of all object-level attributes.

    Use this to iterate over the object attributes.

    Returns
    -------
    list
      List containing the attribute names.

    Examples
    --------
    Iterate over all object attributes of the object stared at "target"
    and print their values.

    >>> from mapteksdk.project import Project
    >>> project = Project()
    >>> with project.read("target") as read_object:
    ...     for name in read_object.attribute_names():
    ...         print(name, ":", read_object.get_attribute(name))
    """
    return list(self._object_attributes.keys())

  def get_attribute(self, name: str) -> ObjectAttributeTypes:
    """Returns the value for the attribute with the specified name.

    Parameters
    ----------
    name
      The name of the object attribute to get the value for.

    Returns
    -------
    ObjectAttributeTypes
      The value of the object attribute `name`.
      For `dtype` = datetime.datetime this is an integer representing
      the number of milliseconds since 1st Jan 1970.
      For `dtype` = datetime.date this is a tuple of the form:
      (year, month, day).

    Raises
    ------
    KeyError
      If there is no object attribute called `name`.

    Warnings
    --------
    In the future this function may be changed to return datetime.datetime
    and datetime.date objects instead of the current representation for
    object attributes of type datetime.datetime or datetime.date.
    """
    attribute = self._object_attributes[name]
    # If value is None and the type is not NoneType, the value will
    # need to be loaded from the DataEngine.
    if attribute.value is None and attribute.dtype is not type(None):
      attribute.value = self.__load_attribute_value(attribute.id,
                                                    attribute.dtype)
    return attribute.value

  def get_attribute_type(self, name: str) -> ObjectAttributeDataTypes:
    """Returns the type of the attribute with the specified name.

    Parameters
    ----------
    name
      Name of the attribute whose type should be returned.

    Returns
    -------
    ObjectAttributeDataTypes
      The type of the object attribute `name`.

    Raises
    ------
    KeyError
      If there is no object attribute called `name`.
    """
    return self._object_attributes[name].dtype

  def delete_all_attributes(self):
    """Delete all object attributes attached to an object.

    This only deletes object attributes and has no effect
    on PrimitiveAttributes.

    Raises
    ------
    RuntimeError
      If all attributes cannot be deleted.
    """
    result = self._data_engine_api().DeleteAllAttributes(self._lock.lock)

    if not result:
      message = self._data_engine_api().ErrorMessage().decode('utf-8')
      raise RuntimeError(f"Failed to delete all attributes on object: "
                         f"'{self.id}'. {message}")

    self.__object_attributes = None

  def delete_attribute(self, attribute: str) -> bool:
    """Deletes a single object-level attribute.

    Deleting a non-existent object attribute will not raise an error.

    Parameters
    ----------
    attribute : str
      Name of attribute to delete.

    Returns
    -------
    bool
      True if the object attribute existed and was deleted;
      False if the object attribute did not exist.

    Raises
    ------
    RuntimeError
      If the attribute cannot be deleted.
    """
    # Get the attribute id from the attribute name
    if attribute not in self._object_attributes:
      # If the attribute doesn't exist, no need to delete it.
      return False
    attribute_id = self._object_attributes[attribute].id
    result = self._data_engine_api().DeleteAttribute(
      self._lock.lock, attribute_id)

    if not result:
      message = self._data_engine_api().ErrorMessage().decode('utf-8')
      raise RuntimeError(f"Failed to delete attribute '{attribute}' on "
                         f"object '{self.id}'. {message}.")

    self._object_attributes.pop(attribute)
    return result

  def __construct_attribute_dictionary(self) -> dict[
      str, _ObjectAttribute]:
    """Constructs the object attribute dictionary.

    This constructs a blank dictionary containing the name, id and type
    of every object attribute on this object.

    Returns
    -------
    dict
      Dictionary of object attributes. Key is the name, value is
      a __ObjectAttribute containing the name, id, type and a None
      value for the object attribute.

    """
    attributes: dict[str, _ObjectAttribute] = {}
    # Get the attribute id list
    # Get size of list
    attr_list_size = self._data_engine_api().GetAttributeList(
      self._lock.lock,
      None,
      0)
    id_buf = ctypes.c_uint32 * attr_list_size # Create buffer type
    attribute_buffer = id_buf() # Create buffer
    # Get the list of attributes
    self._data_engine_api().GetAttributeList(self._lock.lock,
                                  attribute_buffer,
                                  attr_list_size)

    for attribute in attribute_buffer:
      # Get the attribute name
      char_sz = self._data_engine_api().GetAttributeName(attribute, None, 0)
      # Create string buffer to hold path
      str_buffer = ctypes.create_string_buffer(char_sz)
      self._data_engine_api().GetAttributeName(attribute, str_buffer, char_sz)
      name = str_buffer.value.decode("utf-8")

      # Get the attribute data type
      dtype_id = self._data_engine_api().GetAttributeValueType(
        self._lock.lock,
        attribute)

      dtype = self._object_attribute_table[dtype_id.value]

      attributes[name] = _ObjectAttribute(name, attribute, dtype, None)

    return attributes

  def __save_attribute(
      self,
      attribute_id: int,
      dtype: ObjectAttributeDataTypes,
      data: ObjectAttributeTypes) -> bool:
    """Saves an attribute to the project.

    Parameters
    ----------
    attribute_id
      Attribute ID for the object attribute the value should be set for.
    dtype
      The data type of the object attribute.
    data
      The value to assign to the object attribute. This can be any type
      which can be trivially converted to dtype.
    """
    result = False
    if dtype is None:
      pass
    elif dtype is type(None):
      result = self._data_engine_api().SetAttributeNull(
        self._lock.lock,
        attribute_id)
    elif dtype is ctypes.c_char_p or dtype is str:
      try:
        result = self._data_engine_api().SetAttributeString(
          self._lock.lock,
          attribute_id,
          data.encode("utf-8")) # type: ignore
      except AttributeError:
        raise TypeError(
          f"Could not convert {data} to UTF-8 string.") from None
    elif dtype is datetime.datetime:
      assert isinstance(data, datetime.datetime)
      data = data.replace(tzinfo=datetime.timezone.utc)
      result = self._data_engine_api().SetAttributeDateTime(
        self._lock.lock,
        attribute_id,
        int(data.timestamp() * 1000000))
    elif dtype is datetime.date:
      assert isinstance(data, datetime.date)
      result = self._data_engine_api().SetAttributeDate(
        self._lock.lock,
        attribute_id,
        data.year,
        data.month,
        data.day)
    else:
      if isinstance(dtype, str):
        raise TypeError(f"Invalid dtype \"{dtype}\". Pass the type directly, "
                         "not a string containing the name of the type.")
      try:
        # Try to handle the 'easy' data types. The data types in the
        # dictionary don't require any extra handling on the Python side.
        # :TRICKY: This dictionary can't be a property of the class because
        # self._data_engine_api() will raise an error if there is no connected
        # application.
        dtype_to_c_api_function: dict[
            type, Callable] = {
          ctypes.c_bool : self._data_engine_api().SetAttributeBool,
          bool : self._data_engine_api().SetAttributeBool,
          ctypes.c_int8 : self._data_engine_api().SetAttributeInt8s,
          ctypes.c_uint8 : self._data_engine_api().SetAttributeInt8u,
          ctypes.c_int16 : self._data_engine_api().SetAttributeInt16s,
          ctypes.c_uint16 : self._data_engine_api().SetAttributeInt16u,
          ctypes.c_int32 : self._data_engine_api().SetAttributeInt32s,
          ctypes.c_uint32 : self._data_engine_api().SetAttributeInt32u,
          ctypes.c_int64 : self._data_engine_api().SetAttributeInt64s,
          ctypes.c_uint64 : self._data_engine_api().SetAttributeInt64u,
          ctypes.c_float : self._data_engine_api().SetAttributeFloat32,
          ctypes.c_double : self._data_engine_api().SetAttributeFloat64,
        }
        result = dtype_to_c_api_function[dtype](
          self._lock.lock, attribute_id, data)
      except KeyError:
        raise TypeError(f"Unsupported dtype: \"{dtype}\".") from None

    return result

  def __load_attribute_value(
      self, attribute_id: int, dtype: ObjectAttributeDataTypes
      ) -> ObjectAttributeTypes:
    """Loads the value of an object attribute.

    This loads the value of the object attribute with the specified
    id and type from the Project.

    Parameters
    ----------
    attribute_id
      ID of the attribute to load.
    dtype
      The type of the attribute to load.

    Returns
    -------
    ObjectAttributeTypes
      The value of the attribute.
    """
    if dtype is None:
      raise KeyError(f"Object attribute: {attribute_id} does not exist.")
    if dtype is type(None):
      # The type was null so there is no data here but there is still an
      # attribute.
      return None

    type_to_function: dict[type, Callable] = {
      ctypes.c_bool: self._data_engine_api().GetAttributeValueBool,
      ctypes.c_int8: self._data_engine_api().GetAttributeValueInt8s,
      ctypes.c_uint8: self._data_engine_api().GetAttributeValueInt8u,
      ctypes.c_int16: self._data_engine_api().GetAttributeValueInt16s,
      ctypes.c_uint16: self._data_engine_api().GetAttributeValueInt16u,
      ctypes.c_int32: self._data_engine_api().GetAttributeValueInt32s,
      ctypes.c_uint32: self._data_engine_api().GetAttributeValueInt32u,
      ctypes.c_int64: self._data_engine_api().GetAttributeValueInt64s,
      ctypes.c_uint64: self._data_engine_api().GetAttributeValueInt64u,
      ctypes.c_float: self._data_engine_api().GetAttributeValueFloat32,
      ctypes.c_double: self._data_engine_api().GetAttributeValueFloat64,

      # The following types need special handling.
      ctypes.c_char_p: self._data_engine_api().GetAttributeValueString,
      datetime.datetime: self._data_engine_api().GetAttributeValueDateTime,
      datetime.date: self._data_engine_api().GetAttributeValueDate,
    }

    function = type_to_function.get(dtype)
    if function is None:
      raise ValueError(
        f'The type of the attribute ({dtype}) is an unsupported type.')

    value: typing.Any
    if dtype is datetime.datetime:
      # Convert timestamp from the project to a datetime object.
      c_value = ctypes.c_int64()
      got_result = function(
        self._lock.lock, attribute_id, ctypes.byref(c_value))
      value = datetime.datetime.fromtimestamp(c_value.value / 1000000,
                                              datetime.timezone.utc)
      value = value.replace(tzinfo=None)  # Remove timezone awareness.
    elif dtype is datetime.date:
      # Convert date tuple from the project to a date object.
      year = ctypes.c_int32()
      month = ctypes.c_uint8()
      day = ctypes.c_uint8()
      got_result = function(
        self._lock.lock,
        attribute_id,
        ctypes.byref(year),
        ctypes.byref(month),
        ctypes.byref(day)
        )
      value = datetime.date(year.value, month.value, day.value)
    elif dtype is ctypes.c_char_p:
      # Get attribute value as text string
      value_sz = function(self._lock.lock, attribute_id, None, 0)

      # Create string buffer to hold path
      value_buffer = ctypes.create_string_buffer(value_sz)
      got_result = function(self._lock.lock, attribute_id, value_buffer,
                            value_sz)
      value = value_buffer.value.decode("utf-8")
    else:
      # Define a value of the given type.
      # mypy cannot determine that dtype cannot possibly be None, date or
      # datetime in this branch so ignore type checking.
      value = dtype() # type: ignore
      got_result = function(self._lock.lock, attribute_id, ctypes.byref(value))
      value = value.value

    if not got_result:
      raise KeyError(f"Object attribute: {attribute_id} does not exist.")

    return value
