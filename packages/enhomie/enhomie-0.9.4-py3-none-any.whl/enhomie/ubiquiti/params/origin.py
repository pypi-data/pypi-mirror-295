"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated

from encommon.types import BaseModel

from enconnect.ubiquiti import RouterParams

from pydantic import Field



class UbiqOriginParams(BaseModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.
    """

    router: Annotated[
        RouterParams,
        Field(...,
              description='Connection specific parameters')]
