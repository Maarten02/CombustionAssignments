from Bin.NewtonRaphson.NR import NR
from Bin.NewtonRaphson.dEQdT import deqdt
from Bin.NewtonRaphson.EQ import func
from functools import partial

dfdx = partial(deqdt, phi=1, compound='c2h4')
f = partial(func, phi=1, compound='c2h4', T0=298.15, Tr=600)

Tad = NR(f, dfdx, 1500, 1e-3)
print(Tad)