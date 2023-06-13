import pandas as pd


def read_sma(x, r):

    """
    :param x: x/d [-]
    :param r: r/d [-]
    :return df: pandas DataFrame containing the Raman data
    """

    x_fn = f'{int(x):02}'
    r_fn = f'{int(r*100):05}'
    file_path_no_ex = r'C:/Users/maart/OneDrive/Documents/MSc/Combustion/H3_Data/Raman Data H3/H' + x_fn + r_fn
    df = None

    try:
        file_path = file_path_no_ex + ".sma"
        # Read the file using read_csv
        df = pd.read_csv(file_path, skiprows=20, delim_whitespace=True, header=0)

        # Rename the columns
        column_names = df.columns.str.strip()
        df.columns = column_names

    except FileNotFoundError:

        try:
            file_path = file_path_no_ex+ ".SMA"
            # Read the file using read_csv
            df = pd.read_csv(file_path, skiprows=20, delim_whitespace=True, header=0)

            # Rename the columns
            column_names = df.columns.str.strip()
            df.columns = column_names

        except FileNotFoundError:
            print(file_path)
            print("No file found with .sma or .SMA extension")
            exit()

    return df
