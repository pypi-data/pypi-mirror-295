"""Interface for the MDF data transfer library.

Warnings
--------
Vendors and clients should not develop scripts or applications against
this module. The contents may change at any time without warning.

"""
###############################################################################
#
# (C) Copyright 2024, Maptek Pty Ltd. All rights reserved.
#
###############################################################################
from __future__ import annotations

# pylint: disable=line-too-long
# pylint: disable=invalid-name;reason=Names match C++ names.
import ctypes
import typing

from pyproj.enums import WktVersion

from .types import T_ObjectHandle
from .util import (
  singleton,
  raise_if_version_too_old,
  CApiUnknownError,
  CApiError,
)
from .wrapper_base import WrapperBase

if typing.TYPE_CHECKING:
  from ..data import DistanceUnit, CoordinateSystem


class CApiInputNotSupportedError(CApiError):
  """Error indicating an input to an import operation is not supported."""

class dtfS_ImportOperation(ctypes.c_void_p):
  """Struct representing an import operation.

  This is an opaque object which can be passed to C API functions.
  """

@singleton
class DataTransfer(WrapperBase):
  """DataTransfer - wrapper for mdf_datatransfer.dll"""
  def __init__(self):
    super().__init__("mdf_datatransfer", "mapteksdk.capi.datatransfer")

  @staticmethod
  def method_prefix():
    return "DataTransfer"

  def capi_functions(self):
    return [
      # Functions changed in version 0.
      # Format:
      # "name" : (return_type, arg_types)
      {},
      # Functions changed in version 1.
      {"DataTransferCApiVersion" : (ctypes.c_uint32, None),
       "DataTransferCApiMinorVersion" : (ctypes.c_uint32, None),
       "DataTransferImporterFor" : (dtfS_ImportOperation, [ctypes.c_char_p, ]),
       "DataTransferDeleteImporter" : (ctypes.c_void_p, [dtfS_ImportOperation, ]),
       "DataTransferIsAtEndOfFile" : (ctypes.c_bool, [dtfS_ImportOperation, ]),
       "DataTransferGetNextObject" : (T_ObjectHandle, [dtfS_ImportOperation, ]),
       "DataTransferSupplyFileUnit" : (ctypes.c_uint8, [dtfS_ImportOperation, ctypes.c_uint32, ]),
       "DataTransferSupplyCoordinateSystem" : (ctypes.c_uint8, [dtfS_ImportOperation, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double), ]),
      }
    ]

  def CApiVersion(self):
    """Returns the API version for the datatransfer DLL."""
    raise_if_version_too_old("Data transfer", self.version, (1, 12))

    return self.dll.DataTransferCApiVersion()

  def CApiMinorVersion(self):
    """Returns the minor API version for the datatransfer DLL."""
    raise_if_version_too_old("Data transfer", self.version, (1, 12))

    return self.dll.DataTransferCApiMinorVersion()

  def ImporterFor(self, path: str) -> dtfS_ImportOperation:
    """Get an import operation for the file at path.

    Raises
    ------
    ValueError
      If importing the file at path is not supported.
    """
    raise_if_version_too_old("Data transfer", self.version, (1, 12))
    result: dtfS_ImportOperation = self.dll.DataTransferImporterFor(path.encode("utf-8"))
    if result.value in (0, None):
      raise ValueError(f"Importing file at {path} is not supported.")
    return result

  def DeleteImporter(self, importer: dtfS_ImportOperation):
    """Delete an import operation."""
    raise_if_version_too_old("Data transfer", self.version, (1, 12))
    self.dll.DataTransferDeleteImporter(importer)

  def IsAtEndOfFile(self, importer: dtfS_ImportOperation):
    """True if there are no more objects to import from `importer`."""
    raise_if_version_too_old("Data transfer", self.version, (1, 12))
    return self.dll.DataTransferIsAtEndOfFile(importer)

  def GetNextObject(self, importer: dtfS_ImportOperation) -> T_ObjectHandle:
    """Import the next object from `importer`"""
    raise_if_version_too_old("Data transfer", self.version, (1, 12))
    return self.dll.DataTransferGetNextObject(importer)

  def SupplyFileUnit(self, importer: dtfS_ImportOperation, unit: DistanceUnit):
    """Supply `unit` as the unit for `importer`."""
    raise_if_version_too_old("Data transfer", self.version, (1, 12))
    result = self.dll.DataTransferSupplyFileUnit(
      importer,
      unit.value
    )

    if result == 3:
      raise ValueError(
        f"The application does not support: {unit}."
      )
    if result == 6:
      raise CApiInputNotSupportedError(
        "The import operation does not require a unit."
      )
    if result != 0:
      self.log.info("Failed to supply file unit. Error: %s", result)
      raise CApiUnknownError(
        "Failed to supply file unit."
      )

  def SupplyCoordinateSystem(self, importer: dtfS_ImportOperation, coordinate_system: CoordinateSystem | None):
    """Supply `coordinate_system` as the coordinate system for `importer`."""
    raise_if_version_too_old("Data transfer", self.version, (1, 12))
    try:
      if coordinate_system is not None:
        wkt = coordinate_system.crs.to_wkt(WktVersion.WKT2_2019).encode("utf-8")
        local_transform = (ctypes.c_double * 11)()
        local_transform[:] = coordinate_system.local_transform.to_numpy()
      else:
        wkt = None
        local_transform = None
    except AttributeError:
      raise TypeError(
        "Coordinate system was not a coordinate system"
      ) from None
    result = self.dll.DataTransferSupplyCoordinateSystem(
      importer,
      wkt,
      local_transform
    )

    if result == 3:
      raise ValueError(
        "The application could not parse the coordinate system."
      )
    if result == 4:
      raise CApiUnknownError(
        "Failed to find PROJ. The application may not support coordinate "
        "systems or the installation may be corrupt."
      )
    if result == 6:
      raise CApiInputNotSupportedError(
        "The import operation does not require a coordinate system."
      )
    if result != 0:
      self.log.info("Failed to supply coordinate system. Error: %s", result)
      raise CApiUnknownError(
        "Failed to supply coordinate system."
      )
