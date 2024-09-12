"""Low level errors thrown by the functions in the SDK.

Users of the mapteksdk package should never throw these errors. Rather,
they are made available here to enable users to catch and handle them.
"""
###############################################################################
#
# (C) Copyright 2024, Maptek Pty Ltd. All rights reserved.
#
###############################################################################
from __future__ import annotations

import typing

class ApplicationTooOldError(Exception):
  """Error raised if the application is too old to use certain functionality.

  Typically, this error indicates that the connected application is missing
  functionality which is required for the function which threw the exception
  to be used. In this case, upgrading the application to the newest version
  should resolve the error.

  The other case where this error will be raised is if the Python Script has
  connected to an application which does not officially support the Python
  SDK. In this case, switching to the newest version of an application which
  officially supports the Python SDK should resolve the error.

  Examples
  --------
  The main reason to catch this exception is if a script uses functionality
  which may not be supported by all target applications but it is still
  possible for the script to complete successfully (likely with reduced
  functionality). For example, the below fragment demonstrates how a script
  could read the edge thickness of an `EdgeNetwork`,
  defaulting to an edge thickness of 1.0 if the application doesn't support
  the property.

  >>> try:
  ...     thickness = edge_network.edge_thickness
  >>> except FunctionNotSupportedError:
  ...     # Treat the edge thickness as 1 if the application does not support
  ...     # reading it.
  ...     thickness = 1.0
  """
  @classmethod
  def with_default_message(cls, feature: str) -> typing.Self:
    """Construct a ApplicationTooOldError with the default message.

    The message will suggest that `feature` is not supported.

    Parameters
    ----------
    feature
      The feature which is not supported. This should start with a capital
      letter and not start with a full stop.
    """
    return cls(
      f"{feature} is not supported by the connected application. "
      "Updating the connected application to the newest version may resolve "
      "this error."
    )
