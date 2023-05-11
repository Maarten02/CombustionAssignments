from ..JANNAF_C2H4.get_cp_mix import get_cp_mix as get_cp_mix_c2h4
from ..JANNAF_H2.get_cp_mix import get_cp_mix as get_cp_mix_h2

def deqdt(t, phi, compound):

    if compound == 'c2h4':
        cpreac, cpprod = get_cp_mix_c2h4(phi, t)

    elif compound == 'h2':
        cpreac, cpprod = get_cp_mix_h2(phi, t)

    return cpprod

