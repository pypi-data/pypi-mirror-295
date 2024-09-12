"""Wrapper around the DataTransfer C API."""
###############################################################################
#
# (C) Copyright 2024, Maptek Pty Ltd. All rights reserved.
#
###############################################################################
from __future__ import annotations

from contextlib import AbstractContextManager
import pathlib
import typing

from ..data import ObjectID, CoordinateSystem, DistanceUnit
from ..internal.util import default_type_error_message

if typing.TYPE_CHECKING:
  from collections.abc import Sequence

  from ..capi import DataTransfer

class ImportOperation(AbstractContextManager):
  """Represents an operation which imports objects from a single file.

  This should always be used in a context manager to ensure that the file
  is closed and to prevent memory leaks.

  Parameters
  ----------
  path
    The path to the file to import objects from.

  Raises
  ------
  ValueError
    If importing the file at `path` is not supported.
  FileNotFoundError
    If there is no file at `path`.
  """
  def __init__(
    self,
    path: pathlib.Path,
    *,
    data_transfer: DataTransfer
  ) -> None:
    if not path.exists():
      # The import framework treats a non-existent file as a file which
      # contains no objects. To get a file not found error this looks
      # before it leaps.
      raise FileNotFoundError(
        f"The file '{path}' cannot be accessed or does not exist."
      )
    self.__deleted = False
    self.__data_transfer = data_transfer
    try:
      self.__import_operation = self.__data_transfer.ImporterFor(str(path))
    except ValueError:
      raise ValueError(
        f"Cannot import file with extension: {path.suffix}"
      ) from None

  def __enter__(self) -> typing.Self:
    return self

  def __exit__(
    self,
    exc_type: type[BaseException] | None,
    exc_value: BaseException | None,
    traceback
  ) -> bool | None:
    if self.__deleted:
      return
    self.__deleted = True
    self.__data_transfer.DeleteImporter(self.__import_operation)

  def supply_coordinate_system(
    self,
    coordinate_system: CoordinateSystem | None
  ):
    """Supply coordinate system to this import operation.

    This only marks the imported objects as being in the specified coordinate
    system. It does not perform any transformation on the object.
    If coordinate system is None, the importer will not set any coordinate
    system to the imported objects.

    Raises
    ------
    TypeError
      If coordinate_system is not a coordinate system.
    ValueError
      If the application does not support coordinate system.
    CApiInputNotSupportedError
      If this import operation does not support coordinate systems.
      This typically indicates developer mistakes.
    """
    if not isinstance(coordinate_system, (CoordinateSystem, type(None))):
      raise TypeError(
        default_type_error_message(
          "coordinate_system", coordinate_system, CoordinateSystem
        )
      )
    self.__data_transfer.SupplyCoordinateSystem(
      self.__import_operation,
      coordinate_system
    )

  def supply_unit(self, unit: DistanceUnit):
    """Supply unit to this import operation."""
    if not isinstance(unit, DistanceUnit):
      raise TypeError(
        default_type_error_message(
          "unit", unit, DistanceUnit
        )
      )
    self.__data_transfer.SupplyFileUnit(self.__import_operation, unit)

  def import_all_objects(self) -> Sequence[ObjectID[typing.Any]]:
    """Import all objects from the file."""
    oids = []
    while not self.__data_transfer.IsAtEndOfFile(self.__import_operation):
      handle = self.__data_transfer.GetNextObject(self.__import_operation)
      if handle.value == 0:
        # A null handle means the import has failed.
        break
      oids.append(ObjectID(handle))
    return oids
