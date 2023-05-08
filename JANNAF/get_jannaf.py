import numpy as np

def get_jannaf():
    filename = 'C:/Users/maart/OneDrive/Documents/MSc/Combustion/CombustionAssignments/JANNAF/processed_jannaf.dat'

    # initialize empty lists to store data
    compounds = []
    coefs1_arr = []
    coefs2_arr = []

    # open file and read data
    with open(filename, 'r') as f:
        lines = f.readlines()

    for i in range(int(len(lines) / 3)):
        # get compound name
        compound = lines[3*i].strip()
        compounds.append(compound)

        # get cp coefficients
        coefs1 = [float(n) for n in lines[3*i+1].split()]
        coefs2 = [float(n) for n in lines[3*i+2].split()]

        coefs1_arr.append(coefs1)
        coefs2_arr.append(coefs2)

    coefs1_arr = np.array(coefs1_arr)
    coefs2_arr = np.array(coefs2_arr)

    return compounds, coefs1_arr, coefs2_arr