from decimal import Decimal

from pint.registry import Quantity, UnitRegistry


def arc_ratio(angle: Quantity, registry: UnitRegistry) -> float | Decimal:
    if not isinstance(angle, Quantity):
        msg = "The angle must be a pint.Quantity object."
        raise TypeError(msg)

    divisor_value = Decimal("360") if isinstance(angle.magnitude, Decimal) else 360.0

    simple_ratio = angle / Quantity(value=divisor_value, units=registry["degree"])
    return simple_ratio.magnitude
