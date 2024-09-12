"""Functions for importing and exporting data."""
###############################################################################
#
# (C) Copyright 2020, Maptek Pty Ltd. All rights reserved.
#
###############################################################################

from __future__ import annotations
import logging
import os
import pathlib
import typing

from ..capi import DataEngine, Vulcan, DataTransfer
from ..capi.util import (
  add_dll_directories_to_path,
  CApiError,
  CApiCorruptDataError,
)
from ..internal.import_operation import ImportOperation
from ..internal.util import default_type_error_message
from .block_model_definition import BlockModelDefinition
from .base import DataObject
from .cells import GridSurface
from .coordinate_systems import CoordinateSystem
from .errors import FileCorruptError
from .facets import Surface
from .objectid import ObjectID
from .primitives.block_properties import BlockProperties
from .units import DistanceUnit

if typing.TYPE_CHECKING:
  from collections.abc import Sequence

  from .containers import VisualContainer

  # pylint: disable=abstract-method
  class AnyBlockModel(BlockProperties, DataObject):
    """Used to type hint any block model.

    As a return type, this indicates the function returns an object which
    inherits from DataObject and BlockProperties. The type doesn't exist
    at runtime and is not fully implemented.
    """

log = logging.getLogger("mapteksdk.data.io")

def import_00t(
  path: str | pathlib.Path,
  unit: DistanceUnit=DistanceUnit.METRE) -> ObjectID[Surface]:
  """Import a Maptek Vulcan Triangulation file (00t) into the project.

  Parameters
  ----------
  path
    Path to file to import.
  unit
    The unit used when exporting the file.

  Returns
  -------
  ObjectID
    The ID of the imported object.

  Raises
  ------
  FileNotFoundError
    If the file does not exist.
  TypeError
    If path cannot be converted to a pathlib.Path.
    If the unit is not an instance of DistanceUnit.
  RuntimeError
    If there is a problem importing the file.

  Notes
  -----
  The imported object is not automatically placed inside a container.
  A call to project.add_object() is required to add it to a container.

  """
  log.info("Importing Vulcan Triangulation (00t): %s", path)

  if not isinstance(path, pathlib.Path):
    path = pathlib.Path(path)

  if not isinstance(unit, DistanceUnit):
    raise TypeError(default_type_error_message("unit", unit, DistanceUnit))

  if not path.is_file():
    raise FileNotFoundError(f"Could not find file: {path}")

  vulcan = Vulcan()

  if vulcan.version < (1, 10):
    # :HACK: Prior to API version 1.10, the DLL directory path must be on path
    # for the Vulcan DLL to correctly load the DLLs required for
    # import / export.
    add_dll_directories_to_path()
  imported_object = vulcan.Read00tFile(
    str(path).encode("utf-8"), unit.value)

  if imported_object.value == 0:
    message = vulcan.ErrorMessage().decode('utf-8')
    log.error(
      "A problem occurred when importing the 00t: %s. %s", path, message)
    raise RuntimeError(message)
  return ObjectID(imported_object)


def export_00t(
    object_id: ObjectID[Surface],
    path: str | pathlib.Path,
    unit: DistanceUnit=DistanceUnit.METRE):
  """Export a Surface to a Vulcan Triangulation (00t).

  Parameters
  ----------
  object_id
    The ID of the surface to export.
  path
    Where to save the 00t.
  unit
    Unit to use when exporting the file.

  Raises
  ------
  TypeError
    If the unit is not a DistanceUnit.
  RuntimeError
    If there was a problem exporting the file.

  Notes
  -----
  Changed in version 1.4 - This function no longer returns a value.
  Prior to 1.4, this would return True on success and raise an exception
  on failure (It could never return False).
  """
  log.info("Exporting Vulcan Triangulation (00t): %s", path)
  if not isinstance(path, pathlib.Path):
    path = pathlib.Path(path)

  if not isinstance(unit, DistanceUnit):
    raise TypeError(default_type_error_message("unit", unit, DistanceUnit))

  vulcan = Vulcan()
  if vulcan.version < (1, 10):
    # :HACK: Prior to API version 1.10, the DLL directory path must be on path
    # for the Vulcan DLL to correctly load the DLLs required for
    # import / export.
    add_dll_directories_to_path()
  result = vulcan.Write00tFile(object_id.handle,
                                 str(path).encode('utf-8'),
                                 unit.value)
  if not result:
    # This may be because the type of object can't be exported to a 00t or
    # because there was a problem trying to read the object or write to the
    # 00t.
    message = vulcan.ErrorMessage().decode('utf-8')
    log.error("The 00t could not be exported: %s. %s", path, message)
    raise RuntimeError(message)


def import_bmf(
    path: str | pathlib.Path,
    unit: DistanceUnit=DistanceUnit.METRE
    ) -> ObjectID[AnyBlockModel]:
  """Import a Maptek Block Model File (bmf) into the project.

  Parameters
  ----------
  path
    Path to file to import.
  unit
    Unit to use when importing the file.

  Returns
  -------
  ObjectID
    The ID of the imported object.

  Raises
  ------
  TypeError
    If path could not be converted to a pathlib.Path.
    If the unit is not an instance of DistanceUnit.
  FileNotFoundError
    If the file does not exist.
  RuntimeError
    If there is a problem importing the file.

  Notes
  -----
  The ObjectID returned by this function is type hinted as
  ObjectID[BlockProperties, DataObject] because all supported block models are
  expected to inherit from BlockProperties and DataObject. This means
  autocompletion should only suggest properties which are shared by all
  block models. The type hint may be incorrect if the bmf contains a block model
  not supported by the SDK.

  """
  log.info("Importing Vulcan Block Model (bmf): %s", path)

  if not isinstance(path, pathlib.Path):
    path = pathlib.Path(path)

  if not isinstance(unit, DistanceUnit):
    raise TypeError(default_type_error_message("unit", unit, DistanceUnit))

  if not path.is_file():
    raise FileNotFoundError(f"Could not find file: {path}")

  vulcan = Vulcan()
  if vulcan.version < (1, 10):
    # :HACK: Prior to API version 1.10, the DLL directory path must be on path
    # for the Vulcan DLL to correctly load the DLLs required for
    # import / export.
    add_dll_directories_to_path()
  imported_object = vulcan.ReadBmfFile(str(path).encode('utf-8'),
                                         unit.value)
  if imported_object.value == 0:
    message = vulcan.ErrorMessage().decode('utf-8')
    log.error("A problem occurred when importing the BMF: %s", message)
    raise RuntimeError(message)
  return ObjectID(imported_object)


def export_bmf(
    object_id: ObjectID[BlockProperties | DataObject],
    path: str | pathlib.Path,
    unit: DistanceUnit=DistanceUnit.METRE):
  """Export a block model to a Maptek Block Model File (bmf).

  Parameters
  ----------
  object_id
    The ID of the block model to export as a bmf.
  path
    Where to save the bmf file.
  unit
    Unit to use when exporting the file.

  Returns
  -------
  bool
    True if the export was a success. This never returns false - if
    the import fails an exception will be raised.

  Raises
  ------
  TypeError
    If unit is not a DistanceUnit.
  RuntimeError
    If there was a problem exporting the file.

  Notes
  -----
  Changed in version 1.4 - This function no longer returns a value.
  Prior to 1.4, this would return True on success and raise an exception
  on failure (It could never return False).
  """
  log.info("Exporting Vulcan Block Model (bmf): %s", path)
  if not isinstance(path, pathlib.Path):
    path = pathlib.Path(path)

  if not isinstance(unit, DistanceUnit):
    raise TypeError(default_type_error_message("unit", unit, DistanceUnit))

  vulcan = Vulcan()
  if vulcan.version < (1, 10):
    # :HACK: Prior to API version 1.10, the DLL directory path must be on path
    # for the Vulcan DLL to correctly load the DLLs required for
    # import / export.
    add_dll_directories_to_path()
  result = vulcan.WriteBmfFile(object_id.handle,
                                 str(path).encode('utf-8'),
                                 unit.value)
  if not result:
    # This may be because the type of object can't be exported to a bmf or
    # because there was a problem trying to read the object or write to the
    # bmf.
    message = vulcan.ErrorMessage().decode('utf-8')
    log.error("The BMF could not be exported to %s. %s", path, message)
    raise RuntimeError(message)


def import_bdf(
  path: os.PathLike | str,
  unit: DistanceUnit = DistanceUnit.METRE
) -> ObjectID[BlockModelDefinition]:
  """Import a block model definition from a bdf file.

  Parameters
  ----------
  path
    The path to the bdf file to import.

  Returns
  -------
  ObjectID[BlockModelDefinition]
    Object ID of the imported block model definition. This will not be placed
    in the project. Use `Project.add_object()` to set its path in the project.
  unit
    The unit to read the imported bdf in. This is metres by default.

  Raises
  ------
  FileNotFoundError
    If the file does not exist or is a directory.
  FileCorruptError
    If the file is not a bdf file or the file is corrupt.
  RuntimeError
    If an unknown error occurs.
  """
  if not isinstance(path, pathlib.Path):
    path = pathlib.Path(path)

  try:
    return ObjectID(Vulcan().ImportBlockModelDefinition(path, unit))
  except CApiCorruptDataError as error:
    raise FileCorruptError(str(error)) from None
  except CApiError as error:
    # Suppress the internal C API errors from appearing in the stack trace
    # but reuse the error message.
    raise RuntimeError(str(error)) from None

def export_bdf(
  oid: ObjectID[BlockModelDefinition],
  path: os.PathLike | str,
  unit: DistanceUnit= DistanceUnit.METRE
):
  """Export a block model definition into a bdf file.

  Parameters
  ----------
  oid
    Object ID of the block model definition to export.
  path
    Path to the file to export the block model definition to.
  unit
    Unit to export the BDF in. This is metres by default.

  Raises
  ------
  TypeError
    If `oid` is not a block model definition object.
  RuntimeError
    If an unknown error occurs.
  ValueError
    If `unit` is not supported by the connected application.
  """
  if not isinstance(path, pathlib.Path):
    path = pathlib.Path(path)

  try:
    if not oid.is_a(BlockModelDefinition):
      raise TypeError(f"Cannot export a {oid.type_name} to a bdf file.")
    Vulcan().ExportBlockModelDefinition(oid, path, unit)
  except ValueError:
    # Re-raise the exception with additional information regarding what the
    # unsupported unit was.
    raise ValueError(
      "The connected application does not support exporting block model "
      f"definitions with unit: '{unit}'."
    ) from None
  except CApiError as error:
    # Suppress the internal C API errors from appearing in the stack trace
    # but reuse the error message.
    raise RuntimeError(str(error)) from None


def import_maptekobj(path: str | pathlib.Path
    ) -> ObjectID[DataObject]:
  """Import a Maptek Object file (maptekobj) into the project.

  Parameters
  ----------
  path
    Path to file to import.

  Returns
  -------
  ObjectID
    The ID of the imported object.

  Raises
  ------
  FileNotFoundError
    If the file does not exist.
  RuntimeError
    If there is a problem importing the file.
  TypeError
    If path cannot be converted to a pathlib.Path object.

  """
  log.info("Importing Maptek Object file (maptekobj): %s", path)

  if not isinstance(path, pathlib.Path):
    path = pathlib.Path(path)

  if not path.is_file():
    raise FileNotFoundError(f"Could not find file: {path}")

  data_engine = DataEngine()
  imported_object = data_engine.ReadMaptekObjFile(
    str(path).encode('utf-8'))
  if imported_object.value == 0:
    last_error = data_engine.ErrorMessage().decode("utf-8")
    log.error("A problem occurred (%s) when importing %s", last_error, path)
    raise RuntimeError(last_error)

  return ObjectID(imported_object)


def export_maptekobj(
    object_id: ObjectID[DataObject],
    path: str | pathlib.Path):
  """Export an object to a Maptek Object file (maptekobj).

  Unlike 00t and bmf any object (even containers) can be exported to a maptekobj
  file.

  Parameters
  ----------
  object_id
    The ID of the object to export.
  path
    Where to save the maptekobj file.

  Returns
  -------
  bool
    True if the export was a success. This never returns false - if
    the import fails an exception will be raised.

  Raises
  ------
  RuntimeError
    If there was a problem exporting the file.

  Notes
  -----
  Changed in version 1.4 - This function no longer returns a value.
  Prior to 1.4, this would return True on success and raise an exception
  on failure (It could never return False).
  """
  log.info("Exporting Maptek Object file (maptekobj): %s", path)
  if not isinstance(path, pathlib.Path):
    path = pathlib.Path(path)

  data_engine = DataEngine()
  result = data_engine.CreateMaptekObjFile(
    str(path).encode('utf-8'), object_id.handle)
  if not result:
    last_error = data_engine.ErrorMessage().decode("utf-8")
    log.error("A problem occurred (%s) when importing %s", last_error, path)
    raise RuntimeError(last_error)

def _import_hgt(path: str | pathlib.Path) -> ObjectID[GridSurface]:
  """Import a HGT file.

  This format was used by NASA's Shuttle Radar Topography Mission.

  Parameters
  ----------
  path
    The path to the HGT file to read.

  Returns
  -------
  ObjectID[GridSurface]
    The Object ID of a grid surface imported from the hgt file.

  Raises
  ------
  ValueError
    If `path` is not to a HGT file.
  FileNotFoundError
    If there is no file at `path`.
  RuntimeError
    If there was an error importing `path`.
  """
  if not isinstance(path, pathlib.Path):
    path = pathlib.Path(path)
  if path.suffix.casefold() != ".hgt":
    raise ValueError(
      f"Cannot import {path}. It is not a HGT file."
    )
  with ImportOperation(path, data_transfer=DataTransfer()) as operation:
    oids = operation.import_all_objects()
  if len(oids) == 0:
    raise RuntimeError(
      f"Failed to import: {path}"
    )
  # There should only be one object per hgt file.
  return oids[0]

def _import_kml(path: str | pathlib.Path) -> ObjectID[VisualContainer]:
  """Import a KML file.

  KML stands for Keyhole Markup Language.

  Parameters
  ----------
  path
    The path to the KML file to read.

  Returns
  -------
  ObjectID[VisualContainer]
    A container containing all of the imported objects.

  Raises
  ------
  ValueError
    If `path` is not to a KML file.
  FileNotFoundError
    If there is no file at `path`.
  RuntimeError
    If there was an error importing `path`.
  """
  if not isinstance(path, pathlib.Path):
    path = pathlib.Path(path)
  if path.suffix.casefold() != ".kml":
    raise ValueError(
      f"Cannot import {path}. It is not a KML file."
    )
  with ImportOperation(path, data_transfer=DataTransfer()) as operation:
    oids = operation.import_all_objects()
  if len(oids) == 0:
    raise RuntimeError(
      f"Failed to import: {path}"
    )
  # There should only be one object per KML file which is the container.
  return oids[0]

def _import_obj(
  path: str | pathlib.Path,
  coordinate_system: CoordinateSystem | None=None,
  unit: DistanceUnit=DistanceUnit.METRE,
) -> Sequence[ObjectID[DataObject]]:
  """Import from an .obj file.

  This file type is used to exchange 3D models intended for visualization,
  3D printing, and extended reality applications. The data consists of sets
  of adjacent triangles that together define a tessellated geometric surface.

  More details can be found on the US Library of Congress Reference page for
  the format here:
  https://www.loc.gov/preservation/digital/formats/fdd/fdd000507.shtml

  Parameters
  ----------
  path
    The path to the .obj file to read.
  coordinate_system
    The coordinate system to use for the import. This does not change the
    geometry of the imported objects. It only marks them as being in the
    specified in this coordinate system.
    This is no coordinate system by default.
  unit
    The unit the file is stored in. This is metres by default.

  Returns
  -------
  ObjectID[VisualContainer]
    Container containing the imported objects.
  """
  if not isinstance(path, pathlib.Path):
    path = pathlib.Path(path)
  if path.suffix.casefold() != ".obj":
    raise ValueError(
      f"Cannot import {path}. It is not a OBJ file."
    )

  with ImportOperation(path, data_transfer=DataTransfer()) as operation:
    operation.supply_unit(unit)
    operation.supply_coordinate_system(coordinate_system)
    return operation.import_all_objects()
