"""Interface for the MDF vulcan library.

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

# pylint: disable=line-too-long
# pylint: disable=invalid-name
import ctypes
import pathlib
import typing

from .types import T_ObjectHandle, T_TypeIndex, T_ReadHandle
from .util import (
  singleton,
  CApiUnknownError,
  CApiCorruptDataError,
  raise_if_version_too_old,
)
from .wrapper_base import WrapperBase

if typing.TYPE_CHECKING:
  from ..data import ObjectID, DistanceUnit
  from ..data.block_model_definition import BlockModelDefinition


SUCCESS = 0
"""Error code indicating the function call was successful."""
BUFFER_TOO_SMALL = 6
"""Error code indicating the buffer was too small."""

@singleton
class Vulcan(WrapperBase):
  """Vulcan - wrapper for mdf_vulcan.dll"""
  def __init__(self):
    super().__init__("mdf_vulcan", "mapteksdk.capi.vulcan")

  @staticmethod
  def method_prefix():
    return "Vulcan"

  def capi_functions(self):
    return [
      # Functions changed in version 0.
      # Format:
      # "name" : (return_type, arg_types)
      {"VulcanErrorMessage" : (ctypes.c_char_p, []),
       "VulcanRead00tFile" : (T_ObjectHandle, [ctypes.c_char_p, ctypes.c_int32]),
       "VulcanWrite00tFile" : (ctypes.c_bool, [T_ObjectHandle, ctypes.c_char_p, ctypes.c_int32]),
       "VulcanReadBmfFile" : (T_ObjectHandle, [ctypes.c_char_p, ctypes.c_int32]),
       "VulcanWriteBmfFile" : (ctypes.c_bool, [T_ObjectHandle, ctypes.c_char_p, ctypes.c_int32]),},
      # Functions changed in version 1.
      {"VulcanCApiVersion" : (ctypes.c_uint32, None),
       "VulcanCApiMinorVersion" : (ctypes.c_uint32, None),

       # New in version 1.11
       "VulcanBlockModelDefinitionType" : (T_TypeIndex, None),
       "VulcanNewBlockModelDefinition" : (T_ObjectHandle, None),
       "VulcanImportBlockModelDefinition" : (ctypes.c_uint8, [ctypes.POINTER(T_ObjectHandle), ctypes.c_char_p, ctypes.c_int32, ]),
       "VulcanExportBlockModelDefinition" : (ctypes.c_uint8, [T_ObjectHandle, ctypes.c_char_p, ctypes.c_int32, ]),
       "VulcanReadBlockModelDefinitionJson" : (ctypes.c_uint8, [ctypes.POINTER(T_ReadHandle), ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint32), ]),
       "VulcanWriteBlockModelDefinitionJson" : (ctypes.c_uint8, [ctypes.POINTER(T_ReadHandle), ctypes.c_char_p, ]),
       }
    ]

  def BlockModelDefinitionType(self) -> T_TypeIndex:
    """Get the static type for a block model definition."""
    raise_if_version_too_old(
      "Checking if an object is a block model definition",
      self.version,
      (1, 11)
    )
    return self.dll.VulcanBlockModelDefinitionType()

  def NewBlockModelDefinition(self) -> T_ObjectHandle:
    """Create a new block model definition."""
    raise_if_version_too_old(
      "Creating a block model definition",
      self.version,
      (1, 11)
    )
    return self.dll.VulcanNewBlockModelDefinition()

  def ImportBlockModelDefinition(
    self,
    path: pathlib.Path,
    unit: DistanceUnit
  ) -> T_ObjectHandle:
    """Import a block model definition from `path`.

    Parameters
    ----------
    path
      The path to the bdf file to import.
    unit
      The unit to import the block model definition in.

    Returns
    -------
    T_ObjectHandle
      The handle of the imported block model definition.

    Raises
    ------
    FileNotFoundError
      If the file at `path` could not be found.
    CApiCorruptDataError
      If the file at `path` is corrupt.
    CApiUnknownError
      If an unknown error occurs.
    """
    raise_if_version_too_old(
      "Import block model definition",
      self.version,
      (1, 11)
    )
    handle = T_ObjectHandle()
    error_code = self.dll.VulcanImportBlockModelDefinition(
      ctypes.byref(handle),
      str(path).encode('utf-8'),
      unit.value
    )

    if error_code == 2:
      message = self.dll.VulcanErrorMessage().decode('utf-8')
      raise FileNotFoundError(
        f"Failed to import '{path}' due to the following error:\n"
        f"{message}")
    if error_code == 3:
      message = self.dll.VulcanErrorMessage().decode('utf-8')
      raise CApiCorruptDataError(
        f"Failed to import '{path}' due to the following error:\n"
        f"{message}"
      )
    if error_code != 0:
      message = self.dll.VulcanErrorMessage().decode('utf-8')
      raise CApiUnknownError(
        f"Failed to import {path} due to the following unknown error:\n"
        f"{message}")
    return handle

  def ExportBlockModelDefinition(
    self,
    definition_id: ObjectID[BlockModelDefinition],
    path: pathlib.Path,
    unit: DistanceUnit
  ):
    """Export a block model definition to `path`.

    Parameters
    ----------
    definition_id
      Object ID of the block model definition to export.
    path
      Path to export the block model definition to.
    unit
      The unit to export the block model definition using.

    Raises
    ------
    CApiUnknownError
      If an unknown error occurs.
    """
    raise_if_version_too_old(
      "Import block model definition",
      self.version,
      (1, 11)
    )
    error_code = self.dll.VulcanExportBlockModelDefinition(
      definition_id.handle,
      str(path).encode('utf-8'),
      unit.value
    )

    if error_code == 7:
      raise ValueError(
        "The connected application does not support exporting block model "
        "definitions with a unit which is not metres."
      )
    if error_code != 0:
      message = self.dll.VulcanErrorMessage().decode('utf-8')
      raise CApiUnknownError(
        f"Failed to export to {path} due to the following unknown error:\n"
        f"{message}")

  def ReadBlockModelDefinitionJson(self, read_handle: T_ReadHandle) -> str:
    """Read the block model definition json for `read_handle`."""
    raise_if_version_too_old(
      "Import block model definition",
      self.version,
      (1, 11)
    )

    buffer = ctypes.create_string_buffer(0)
    buffer_length = ctypes.c_uint32(0)

    result = self.dll.VulcanReadBlockModelDefinitionJson(
      read_handle,
      buffer,
      ctypes.byref(buffer_length)
    )

    if result != BUFFER_TOO_SMALL:
      # This should be unreachable.
      raise CApiUnknownError(
        "Failed to read block model definition."
      )

    # Buffer length should have been updated to contain the required buffer
    # length. Try again with a correctly sized buffer.
    buffer = ctypes.create_string_buffer(buffer_length.value)
    result = self.dll.VulcanReadBlockModelDefinitionJson(
      read_handle,
      buffer,
      buffer_length
    )

    if result != SUCCESS:
      message = self.dll.VulcanErrorMessage().decode('utf-8')
      raise CApiUnknownError(
        f"Failed to read block model definition due to the following unknown error:\n"
        f"{message}")

    return bytearray(buffer).decode('utf-8')

  def WriteBlockModelDefinitionJson(self, edit_handle: T_ReadHandle, json: str):
    """Set the block model definition json for `edit_handle`."""
    raise_if_version_too_old(
      "Import block model definition",
      self.version,
      (1, 11)
    )

    result = self.dll.VulcanWriteBlockModelDefinitionJson(edit_handle, json.encode('utf-8'))
    if result != SUCCESS:
      message = self.dll.VulcanErrorMessage().decode('utf-8')
      raise CApiUnknownError(
        f"Failed to read block model definition due to the following unknown error:\n"
        f"{message}")
