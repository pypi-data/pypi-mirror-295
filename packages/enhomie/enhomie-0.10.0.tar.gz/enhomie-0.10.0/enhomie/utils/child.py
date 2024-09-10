"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Literal
from typing import TYPE_CHECKING
from typing import Union

if TYPE_CHECKING:
    from ..homie.childs import HomieChild



_PHASE = Literal[
    'initial',
    'runtime']



class InvalidChild(Exception):
    """
    Exception for when the child could not be instantiated.

    :param child: Name or child that is determined invalid.
    :param phase: From which phase child was found invalid.
    """

    child: str
    phase: _PHASE


    def __init__(
        self,
        child: Union[str, 'HomieChild'],
        phase: _PHASE,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        if hasattr(child, 'name'):
            child = child.name

        message = (
            f'Child ({child}) '
            'invalid within '
            f'phase ({phase})')

        self.child = child

        super().__init__(message)
