import numpy as np
import matplotlib.pyplot as plt
# Open the file and read the lines

# Get path to file, run and plot
h2_filenames = ['c2h4_p', 'c2h4_phi', 'h2_p', 'h2_phi']
x_vars = ['p', 'phi']
y_vars = ['']
folder = './CEA_plt/'
extension = '.plt'

def readFile(path, x_var, y_var):
    with open(path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        # Skip the comments and empty lines
        if line.startswith('#'):
            col_names = [str(x) for x in line.split()[1:]]
            continue
        # Split the line into columns

        cols = line.split()

        # Convert the columns to floats and store the data
        row = [float(x) for x in cols]

        if not 'data' in locals():
            data = np.array(row)
        else:
            data = np.vstack((data, row))


    # # TODO: plot and save figure
    # temp_col=col_names.index('t')
    # eq_ratio_col = col_names.index('phi')
    #
    # plt.plot(data[:,eq_ratio_col], data[:,temp_col])
    # plt.show()
