from ..JANNAF_C2H4.get_LHS_ethylene import get_LHS_ethylene
from ..JANNAF_C2H4.get_RHS import get_RHS as get_RHS_ethylene
from ..JANNAF_H2.get_LHS_H2 import get_LHS_h2 as get_LHS_H2
from ..JANNAF_H2.get_RHS import get_RHS as get_RHS_H2
from .intcp_c2h4 import intcpc2h4

def func(x, phi, compound, T0, Tr):

    if compound == 'c2h4':

        LHS = get_LHS_ethylene(phi)
        intP, intR = intcpc2h4(phi, T0, x, Tr)
        RHS = intP - intR

    elif compound == 'h2':

        LHS = get_LHS_H2(phi)
        RHS = get_RHS_H2(phi, x)

    return RHS - LHS