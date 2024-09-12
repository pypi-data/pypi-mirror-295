"""Common functions used by the SDK specifically for use with C API modules.

Warnings
--------
Vendors and clients should not develop scripts or applications against
this module. The contents may change at any time without warning.

"""
###############################################################################
#
# (C) Copyright 2020, Maptek Pty Ltd. All rights reserved.
#
###############################################################################
from __future__ import annotations

import ctypes
import logging
import pathlib

from ..errors import ApplicationTooOldError
from .internal.application_dll_directory import ApplicationDllDirectory
from .internal.errors import DllDirectoryClosedError

_DLL_DIRECTORY: ApplicationDllDirectory | None = None
"""The application DLL directory to load DLLs from.

If None, the script has not connected to an application.
"""

_REMEMBERED_DLL_PATH: str | None = None
"""The path passed to register_dll_directory().

After disconnecting from one application, it is only valid for the script
to reconnect to the same application or a different instance of that application
because the SDK cannot effectively unload the DLLs from the first application
and thus would attempt to use the original applications DLLs to connect to the
second application, resulting in a crash.

This is used to detect attempts to connect to a different application and
to raise a useful error message.
"""

_HAS_ADDED_DLL_DIRECTORIES_TO_PATH: bool = False


logger = logging.getLogger("mapteksdk.capi.util")


class CApiError(Exception):
  """Base class for errors raised by the C API. This class should not be
  raised directly - raise a subclass instead.

  """


CApiFunctionNotSupportedError = ApplicationTooOldError
"""Alias for FunctionNotSupportedError.

This preserves backwards compatibility, though this is internal so no one
should have been catching this exception.
"""


class CApiDllLoadFailureError(CApiError):
  """Error raised when one of the DLLs fails to load."""


class CApiUnknownError(CApiError):
  """Error raised when an unknown error occurs in the CAPI."""


class NoConnectedApplicationError(CApiError):
  """Error raised when not connected to an application"""


class MultipleApplicationConnectionsError(CApiError):
  """Error raised when attempting to connect to two different applications.

  Connecting to two different applications within the same script is impossible
  because Python cannot effectively unload every DLL required to connect
  an application (It can't unload DLLs implicitly loaded as dependencies of
  the explicitly loaded DLLs). Thus, attempting to connect to a second
  application results in a mix of incompatible DLLs from the two
  applications.

  """



class CApiCorruptDataError(CApiError):
  """Error indicating the C API encountered corrupt data."""


class CApiWarning(Warning):
  """Base class for warnings emitted from the C APIs."""


class CApiUnknownWarning(CApiWarning):
  """A C API function returned an unknown error, but it was not fatal.

  This is emitted in place of CApiUnknownError when the error is non-fatal.
  """

def _get_application_dll_directory() -> ApplicationDllDirectory:
  """Get the ApplicationDllDirectory to use to load Dlls.

  This will raise an error if the script has yet to connect to an application,
  or if the script has disconnected from an application.

  Raises
  ------
  NoConnectedApplicationError
    If the application DLLs are not available.
  """
  dll_directory = _DLL_DIRECTORY

  if dll_directory is None:
    raise NoConnectedApplicationError(
      "This function cannot be accessed because the script has not connected "
      "to an application. Use the Project() constructor to connect to an "
      "application.")

  if dll_directory.is_closed:
    raise NoConnectedApplicationError(
      "This function cannot be accessed because the script has disconnected "
      "from the application. Ensure all functions which require a "
      "connected application are inside of the Project's `with` block.")

  return dll_directory

def _ensure_dlls_available():
  """Raises an error if the application's DLLs are not available.

  This will raise an error if the script has yet to connect to an application,
  or if the script has disconnected from an application.

  Raises
  ------
  NoConnectedApplicationError
    If the application DLLs are not available.
  """
  _ = _get_application_dll_directory()

def load_dll(dll_name: str):
  """Load a dll using the dll_path configured by connecting to an application.

  Parameters
  ----------
  dll_name : str
    The name of the dll to load.

  Raises
  ------
  NoConnectedApplicationError
    If the script has not connected to an application.
  """
  _dll_directory = _get_application_dll_directory()

  try:
    return _dll_directory.load_dll(dll_name)
  except DllDirectoryClosedError:
    raise NoConnectedApplicationError(
      "This function cannot be accessed because the script has disconnected "
      "from the application. Ensure all functions which require a "
      "connected application are inside of the Project's `with` block."
    ) from None

def register_dll_directory(base_path: str):
  """Registers a DLL directory.

  This handles the differences between installed applications versus
  applications compiled from source.
  """
  # pylint: disable=global-statement
  global _REMEMBERED_DLL_PATH
  global _DLL_DIRECTORY

  existing_dll_directory = _DLL_DIRECTORY
  if existing_dll_directory is not None:
    if not existing_dll_directory.is_closed:
      raise MultipleApplicationConnectionsError(
        "Cannot connect to an application because the script is already "
        "connected to an application."
      )
    if _REMEMBERED_DLL_PATH != base_path:
      raise MultipleApplicationConnectionsError(
      "Cannot connect to multiple different applications in one script")

  logger.debug("Loading dlls from %s", base_path)
  _DLL_DIRECTORY = ApplicationDllDirectory(pathlib.Path(base_path))
  _REMEMBERED_DLL_PATH = base_path

def disable_dll_loading():
  """Disable loading DLLs from the application.

  This should be called when disconnecting from an application.
  """
  dll_directory = _DLL_DIRECTORY
  if dll_directory is not None:
    dll_directory.close()

def add_dll_directories_to_path():
  """Add the DLL directories to the PATH environment variable.

  This is used used to work around bugs in DLLs where they do not
  use the DLL search directories to load DLLs.

  This will only add the DLL directories to PATH once.
  """
  # pylint: disable=global-statement
  global _HAS_ADDED_DLL_DIRECTORIES_TO_PATH
  if _HAS_ADDED_DLL_DIRECTORIES_TO_PATH:
    return
  _HAS_ADDED_DLL_DIRECTORIES_TO_PATH = True
  try:
    dll_directory = _get_application_dll_directory()
    dll_directory.add_to_path()
  except DllDirectoryClosedError:
    raise NoConnectedApplicationError(
      "This function cannot be accessed because the script has disconnected "
      "from the application. Ensure all functions which require a "
      "connected application are inside of the Project's `with` block."
    ) from None

def singleton(class_reference):
  """Provides an implementation of the singleton pattern.

  This should only be used for the C API singletons. It includes additional
  functionality to disable accessing the DLLs after disconnecting from
  the application.

  Notes
  -----
  Usage: @singleton above class

  """
  instances = {}
  def get_instance():
    """Gets (or creates) the only instance of a singleton class."""
    # Disallow accessing the DLLs if there is no connected application.
    _ensure_dlls_available()
    if class_reference not in instances:
      instances[class_reference] = class_reference()
    return instances[class_reference]
  return get_instance

def get_string(target_handle, dll_function) -> str | None:
  """Read a string from a C API function.

  This works for C API functions which return a string
  and have a function signature of the form: Tint32u (handle, *buffer, size).

  Parameters
  ----------
  target_handle : c_uint64, T_ObjectHandle, T_NodePathHandle, etc
    Suitable type of native handle (), supporting
    a *.value property.
  dll_function : function
    A function of Tint32u (handle, *buffer, size).

  Returns
  -------
  str
    Result as string or None on failure (e.g. not supported by dll).

  """
  try:
    value_size = 64
    while value_size > 0:
      value_buffer = ctypes.create_string_buffer(value_size)
      result_size = dll_function(target_handle, value_buffer, value_size)
      if result_size is None:
        # probably not supported by dll version
        return None
      value_size = -1 if result_size <= value_size else result_size
    return value_buffer.value.decode("utf-8")
  except OSError:
    result = None
  return result

def raise_if_version_too_old(feature, current_version, required_version):
  """Raises a CapiVersionNotSupportedError if current_version is less
  than required_version.

  Parameters
  ----------
  feature : str
    The feature name to include in the error message.
  current_version : tuple
    The current version of the C Api.
  required_version : tuple
    The version of the C Api required to access the new feature.

  Raises
  ------
  ApplicationTooOldError
    If current_version < required_version.

  """
  if current_version < required_version:
    logger.info(
      "%s is not supported in C Api version: %s. Requires version: %s.",
      feature,
      current_version,
      required_version
    )
    raise ApplicationTooOldError.with_default_message(feature)
