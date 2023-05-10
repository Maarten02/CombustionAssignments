import numpy as np
import matplotlib.pyplot as plt
# Open the file and read the lines

# Get path to file, run and plot
h2_filenames = ['h2_p', 'h2_phi', 'h2_phi_600']
c2h4_filenames = ['c2h4_p', 'c2h4_phi', 'h2_phi_600']
x_vars = ['p', 'phi', 'phi']
y_vars = ['t', 't', 'NO']
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

def plot_vars(col_names, data, x_var, y_var, figname, compound, hold=False, plotin=False, fig=None, ax=None):
        temp_col=col_names.index('t')
        eq_ratio_col = col_names.index('phi')

        if not plotin:
            fig, ax = plt.subplots()
            ax.set_xlabel(x_var)
            ax.set_ylabel(y_var)

        ax.plot(data[:,eq_ratio_col], data[:,temp_col], label=y_var)
        tit = x_var + 'versus' + y_var + 'for ' + compound
        ax.set_title(tit)
        ax.legend()
        if not hold:
            plt.savefig(figname)
        else:
            return fig, ax

for compound_files, compound in zip([h2_filenames, c2h4_filenames], ['H2', 'C2H4']):
    for file, x_var, y_var in zip(compound_files, x_vars, y_vars):
        path = folder + file + extension
        figname = './figures/' + x_var + '_' + y_var + '_' + compound + '_plot.pdf'

        col_names, data = readFile(path, x_var, y_var, figname, compound)
        if file[-3:] == '600':
            fig, ax = plot_vars(col_names, data, x_var, y_var, figname, compound, True)
            y_var += '2'
            col_names, data = readFile(path, x_var, y_var, figname, compound)
            plot_vars(col_names, data, x_var, y_var, figname, compound, False, True, fig, ax)

        else:
            plot_vars(col_names, data, x_var, y_var, figname, compound)


