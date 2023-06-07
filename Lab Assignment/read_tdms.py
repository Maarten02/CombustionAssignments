import glob
from nptdms import TdmsFile
import numpy as np

def read_tdms(filename, standard_format=True):

    # Read the TDMS file
    tdms_file = TdmsFile.read(filename)
    const_flow = None
    eq_ratio = None

    if standard_format:
        # Get the letter ('f' or 'o') and equivalence ratio from the filename
        filename = filename.split("/")[-1]  # Extracts the filename from the full path
        letter_index = filename.index("_f_" if "_f_" in filename else "_o_") + 1
        const_flow = filename[letter_index]

        ratio_start = filename.index("_", letter_index) + 1
        ratio_end = filename.index(".tdms")
        ratio_str = filename[ratio_start:ratio_end]

        # Convert ratio_str to float with decimal separator after the first digit
        float_ratio_str = ratio_str[0] + '.' + ratio_str[1:]
        eq_ratio = float(float_ratio_str)

    return tdms_file, const_flow, eq_ratio


def print_table(data, column_names):
    # Calculate the maximum width for each column
    max_widths = [max(len(column_name), max(len('{:.5e}'.format(row[i])) for row in data)) for i, column_name in
                  enumerate(column_names)]

    # Print the table headers
    header = ' | '.join('{:<{}}'.format(column_name, max_widths[i]) for i, column_name in enumerate(column_names))
    print(header)

    # Print the separator line
    separator = '-+-'.join('-' * width for width in max_widths)
    print(separator)

    # Print the table rows
    for row in data:
        row_str = ' | '.join('{:<{}}'.format('{:.5e}'.format(value), max_widths[i]) for i, value in enumerate(row))
        print(row_str)


def get_aves(data_struc, cols, bl=False):
    aves = np.empty(len(cols))

    if bl:
        data_struc = data_struc[0]

    for i, col in enumerate(cols):
        group = data_struc['Combustor Data']
        vec = group[col]
        aves[i] = np.average(vec)

    return aves


def list_channels():
    for file in glob.glob("Group3_labview/*.tdms"):
        data, const_flow, eq_ratio = read_tdms(file)

        for channel in data['Combustor Data'].channels():
            print(channel.name)

        break


def main():
    cols = ['GA - NO', 'GA - NO2', 'GA - CO2',  'GA - O2', 'GA - CO', 'GA - CH4']
    units = ['[ppm]', '[ppm]', '[vol %]', '[vol %]', '[ppm]', '[ppm]']

    print_cols = np.empty(len(cols) + 2, dtype=str)

    # get baseline ave
    baseline_file = read_tdms("Group3_labview/baseline/2023_05_30_08_39_54_Baseline_group3.tdms", False)
    baseline_vals = get_aves(baseline_file, cols, bl=True)

    # make empty data table [len(files)xlen(cols)]
    table_data = np.empty((len(glob.glob("Group3_labview/*.tdms")), len(cols) + 2))

    # loop over the files
    for i, file in enumerate(glob.glob("Group3_labview/*.tdms")):
        data, const_flow, eq_ratio = read_tdms(file)

        if const_flow == 'f':
            const_flow = 1
        else:
            const_flow = 0

        # get ave for columns of interest
        aves = get_aves(data, cols)

        # subtract baseline from ave TODO: CHECK IF THIS IS CORRECT
        table_data[i, 0] = const_flow
        table_data[i, 1] = eq_ratio
        table_data[i, 2:] = aves - baseline_vals

    col_lbl = []
    for col, unit in zip(cols, units):
        col_lbl.append(col+ ' ' + unit)

    print_cols = ['Type [f=1, o=0]', 'Phi']
    print_cols.extend(col_lbl)
    print_table(table_data, print_cols)


main()



