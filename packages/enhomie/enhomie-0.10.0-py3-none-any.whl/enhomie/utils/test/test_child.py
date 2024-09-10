"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

from ..child import InvalidChild

if TYPE_CHECKING:
    from ...homie import Homie



def test_InvalidChild() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    raises = InvalidChild(
        child='invalid',
        phase='initial')


    attrs = lattrs(raises)

    assert attrs == ['child']


    assert inrepr(
        'InvalidChild',
        raises)

    assert hash(raises) > 0

    assert instr(
        'Child (invalid)',
        raises)


    assert str(raises) == (
        'Child (invalid) '
        'invalid within '
        'phase (initial)')



def test_InvalidChild_cover(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """

    childs = homie.childs
    devices = childs.devices

    device = devices[
        'jupiter_motion']


    raises = InvalidChild(
        child=device,
        phase='runtime')


    assert str(raises) == (
        'Child (jupiter_motion) '
        'invalid within '
        'phase (runtime)')
