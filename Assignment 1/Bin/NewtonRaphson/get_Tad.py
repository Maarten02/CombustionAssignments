from .NR import NR
from .dEQdT import deqdt
from .EQ import func
from functools import partial

def get_T_ad(phi_arg, compound_arg, Treac):

    T_zero = 1800
    tol = 1e-6

    dfdx = partial(deqdt, phi=phi_arg, compound=compound_arg)
    f = partial(func, phi=phi_arg, compound=compound_arg, T0=298.15, Tr=Treac)

    Tad = NR(f, dfdx, T_zero, tol)

    return Tad