"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated
from typing import Optional

from encommon.config import Params
from encommon.types import BaseModel

from pydantic import Field

from .aspire import HomieAspireParams
from .desire import HomieDesireParams
from .device import HomieDeviceParams
from .group import HomieGroupParams
from .origin import HomieOriginParams
from .scene import HomieSceneParams
from .service import HomieServiceParams



class HomiePrinterParams(BaseModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.
    """

    action: Annotated[
        bool,
        Field(False,
              description='Print the actions to console')]

    update: Annotated[
        bool,
        Field(False,
              description='Print the updates to console')]

    stream: Annotated[
        bool,
        Field(False,
              description='Print the streams to console')]

    desire: Annotated[
        bool,
        Field(False,
              description='Print the aspires to console')]

    aspire: Annotated[
        bool,
        Field(False,
              description='Print the aspires to console')]



class HomieParams(Params, extra='forbid'):
    """
    Process and validate the core configuration parameters.
    """

    database: Annotated[
        str,
        Field('sqlite:///:memory:',
              description='Database connection string',
              min_length=1)]

    dryrun: Annotated[
        bool,
        Field(False,
              description='Determine if changes are made')]

    potent: Annotated[
        bool,
        Field(True,
              description='Ignore idempotency in change')]

    printer: Annotated[
        HomiePrinterParams,
        Field(default_factory=HomiePrinterParams,
              description='Print the stream to console')]

    service: Annotated[
        HomieServiceParams,
        Field(default_factory=HomieServiceParams,
              description='Parameters for Homie Service')]

    origins: Annotated[
        Optional[dict[str, HomieOriginParams]],
        Field(None,
              description='Parameters for Homie origins',
              min_length=1)]

    devices: Annotated[
        Optional[dict[str, HomieDeviceParams]],
        Field(None,
              description='Parameters for Homie devices',
              min_length=1)]

    groups: Annotated[
        Optional[dict[str, HomieGroupParams]],
        Field(None,
              description='Parameters for Homie groups',
              min_length=1)]

    scenes: Annotated[
        Optional[dict[str, HomieSceneParams]],
        Field(None,
              description='Parameters for Homie scenes',
              min_length=1)]

    desires: Annotated[
        Optional[dict[str, HomieDesireParams]],
        Field(None,
              description='Parameters for Homie desires',
              min_length=1)]

    aspires: Annotated[
        Optional[dict[str, HomieAspireParams]],
        Field(None,
              description='Parameters for Homie aspires',
              min_length=1)]
