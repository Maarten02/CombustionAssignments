import numpy as np

def readchem1d(fname):
    y = []
    t = None
    a = []
    y = np.genfromtxt(fname, skip_header=24)
    y = y[:, 1:]

    with open(fname, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            if line == '[TIME]':
                line = next(file).strip()
                t = float(line)
            elif line == '[FILE_STRUCTURE_COLUMNS_CONTAINING]':
                line = next(file).strip()
                a = line.split()
                break

    return y, t, a
