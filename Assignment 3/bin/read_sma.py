import pandas as pd


def read_sma(x, r):

    """
    :param x: x/d [-]
    :param r: r/d [-]
    :return df: pandas DataFrame containing the Raman data
    """

    x_fn = f'{int(x):02}'
    r_fn = f'{int(r*1000):05}'
    file_path_no_ex = 'C:\Users\maart\OneDrive\Documents\MSc\Combustion\H3_Data\Raman Data H3/H' + x_fn + r_fn
    df = None

    try:
        file_path = file_path_no_ex + ".sma"
        df = pd.read_csv(file_path, skiprows=20, delim_whitespace=True)
        df.columns = df.iloc[0]
        df = df[1:].reset_index(drop=True)

    except FileNotFoundError:

        try:
            file_path = file_path_no_ex+ ".SMA"
            df = pd.read_csv(file_path, skiprows=20, delim_whitespace=True)
            df.columns = df.iloc[0]
            df = df[1:].reset_index(drop=True)

        except FileNotFoundError:
            print("No file found with .sma or .SMA extension")
            exit()

    return df
