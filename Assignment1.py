import matplotlib.pyplot as plt

from JANNAF.get_cp import get_cp
from JANNAF.get_jannaf import get_jannaf
import numpy as np

compounds, coefs1, coefs2 = get_jannaf()
fig, ax = plt.subplots()


for compound, coef1, coef2 in zip(compounds, coefs1, coefs2):
    cp_list = np.empty(50)
    temp_list = np.empty(50)
    for i, temp in enumerate(np.linspace(600, 2500, 50)):
        cp_list[i] = get_cp(coef1, coef2, temp)
        temp_list[i] = temp
    ax.plot(temp_list, cp_list, label=compound)

plt.legend()
plt.grid()
ax.set_xlabel('Temperature [K]')
ax.set_ylabel('$C_p$ [x]')
ax.set_title('$C_p$ variation with temperature for different compounds')
plt.show()