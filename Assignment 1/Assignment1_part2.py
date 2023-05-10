import numpy as np
import matplotlib.pyplot as plt
# Open the file and read the lines

# Get path to file, run and plot
h2_filenames = ['h2_p', 'h2_phi', 'h2_phi_600', 'h2_phi_600']
c2h4_filenames = ['c2h4_p', 'c2h4_phi', 'c2h4_phi_600', 'c2h4_phi_600']
x_vars = ['p', 'phi', 'phi', 'phi']
y_vars = ['t', 't', 'NO', 'NO2']
x_units = [' [Bar]', ' [-]', ' [-]', ' [-]']
y_units = [' [K]', ' [K]', ' [-]', ' [-]']
folder = './CEA_plt/'
extension = '.plt'

def readFile(path, x_var, y_var, figname, compound):
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

    return col_names, data

def plot_vars(col_names, h2_data, c2h4_data, x_var, x_unit, y_var, y_unit, figname):
        x_col = col_names.index(x_var)
        y_col = col_names.index(y_var)

        fig, ax = plt.subplots()
        xlab = x_var.upper() + x_unit
        ax.set_xlabel(xlab)
        ylab = y_var.upper() + y_unit
        ax.set_ylabel(ylab)

        ax.plot(h2_data[:,x_col], h2_data[:,y_col], label='H2')
        ax.plot(c2h4_data[:,x_col], c2h4_data[:,y_col], label='C2H4')

        tit = y_var.upper() + ' versus ' + x_var.upper() + ' for H2 and C2H4'
        ax.set_title(tit)
        ax.legend()
        ax.grid()
        plt.savefig(figname)


for x_var, y_var, h2_file, c2h4_file, x_unit, y_unit in zip(x_vars, y_vars, h2_filenames, c2h4_filenames, x_units, y_units):
        h2_path = folder + h2_file + extension
        c2h4_path = folder + c2h4_file + extension
        figname = './figures/' + x_var + '_' + y_var + '_plot.pdf'

        col_names, h2_data = readFile(h2_path, x_var, y_var, figname, 'H2')
        col_names, c2h4_data = readFile(c2h4_path, x_var, y_var, figname, 'C2H4')

        plot_vars(col_names, h2_data, c2h4_data, x_var, x_unit, y_var, y_unit, figname)


