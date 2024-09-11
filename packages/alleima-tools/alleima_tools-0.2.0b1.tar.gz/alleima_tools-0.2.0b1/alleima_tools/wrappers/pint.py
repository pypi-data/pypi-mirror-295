from math import acos, asin, atan, cos, sin, tan

from alleima_tools.wrappers import ureg

pint_cos = ureg.wraps(None, ureg.radian)(cos)
pint_sin = ureg.wraps(None, ureg.radian)(sin)
pint_tan = ureg.wraps(None, ureg.radian)(tan)

pint_acos = ureg.wraps(ureg.radian, None)(acos)
pint_asin = ureg.wraps(ureg.radian, None)(asin)
pint_atan = ureg.wraps(ureg.radian, None)(atan)
