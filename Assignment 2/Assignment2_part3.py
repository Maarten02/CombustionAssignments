from read_chem1d import readchem1d
import numpy as np
import matplotlib.pyplot as plt
"""Questions
1. equivalence ratio is specified to be 0.6 both at the left and right boundary
2. The flame thickness; should this be total thickness, diffusion thickness or the thickness from temperature gradients?
3. what is consumption speed? (m/s) or mol/s  or kg/s?
Sc in slides: m/s
4. what is a normal order or magnitude for mass flux (unit: kg/m2 s)

"""



# TODO:
# strained, reactants to products flamelets
# Treac= 300 K
# pressure = 1 bar
# 1 step complete combustion
# AFT from freely propagating flame
# no curvature


#a) For a methane/air case at equivalence ratio 0.6, compute the flamelet solution in Chem1d for strain
# rate values of 100 s-1, 200 s-1, 500 s-1, 1000 s-1, 5000 s-1 and 10000 s-1. Plot the peak reaction rate of
# water, consumption speed and flame thickness with varying strain. Use a logarithmic scale for the x-
# axis (strain). Explain the behaviour observed

# test
file = r'C:\Users\maart\OneDrive\Documents\MSc\Combustion\CHEM1D\CHEM1D\yiend.dat'
y, t, a = readchem1d(file)

y = np.array(y)

var = 'H2O'
idx = a.index(var) - 1

data = y[:, idx]
x_pos = y[:, 0]

# print(y.shape)
dydx = np.empty(len(data) - 2)
for i in range(1, len(dydx) + 1):
    dydx[i-1] = (data[i+1] - data[i-1]) / (x_pos[i+1] - x_pos[i-1])

# print(dydx)


x_pos_plot = x_pos[1:-1]
plt.plot(x_pos_plot, dydx)
plt.show()
#total thickness
varT = 'Temp'
idxT = a.index(varT) - 1
data_T = y[:, idxT]
T_b = data_T[-1]
T_u = data_T[0]
flame_end = 0.99 * T_b
flame_start = 0.01 * T_b # WRONG!!!!!!!!!!!!!11
a = data_T[data_T > flame_end]
b = data_T[data_T > flame_start]
flame_thickness = x_pos[np.where(data_T == a[0])] - x_pos[np.where(data_T == b[0])] #WRONG!!!!!!!!!!!!1
print('flame', flame_thickness)
#
# print(y)
# print(t)
# print(a)
# Consumption speed
# determine dot{omega_f} from omega_f


# b) Now for the same conditions at strain rates, compute the solutions for hydrogen/air flamelets. Plot
# the results of peak reaction rate, consumption speed and flame thickness (add the curves on the same
# plots used for point a)). Comment on the differences

# find peak reaction rate
#

#c) Compute the Markstein length ℒ = − 𝑑𝑠𝑐/𝑑𝐾, where 𝐾 is the stretch rate and 𝑠𝑐 is the consumption
# speed, for the two mixtures of points a) and b). Explain the differences observed in the results.


# d) Now for the same strain rates compute, non-premixed flamelets in a methane to air opposite jet
# configuration. Plot the peak reaction rate of water, and the stoichiometric scalar dissipation rate of
# mixture fraction versus strain. Now also plot the variation of flame temperature versus mixture fraction
# for the different strain rates. Comment on

#