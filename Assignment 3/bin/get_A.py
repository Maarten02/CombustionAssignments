# Z^(i) = (Z_i - Z_i,2) / (Z_i,1 - Z_i,2)
# 1 =
# Z_i same as in part a ii
# Z_i,1 is the mass fraction of i in fuel stream ?
# Z_i,2_is the mass fraction of i in oxidiser stream ?
#
# A = Z^(H) – Z^(O) and
# B = Z^(H) – Z^(N)
W_H2 = 2.016
X_H2_1 = 0.5
X_H2_2 = 0

W_O2 = 31.999
X_O2_1 = 0
X_O2_2 = 0.21

W_N2 = 28.0134
X_N2_1 = 0.5
X_N2_2 = 0.79

W_fuel = W_H2 * X_H2_1 + W_N2 * X_N2_1
W_air = W_O2 * X_O2_2 + W_N2 * X_N2_2

Z_H2_1 = (X_H2_1*W_H2)/W_fuel
Z_O2_1 = (X_O2_1*W_O2)/W_fuel
Z_N2_1 = (X_N2_1*W_N2)/W_fuel

Z_H2_2 = (X_H2_2*W_H2)/W_air
Z_O2_2 = (X_O2_2*W_O2)/W_air
Z_N2_2 = (X_N2_2*W_N2)/W_air


def get_Z_O(row):
    return row['O2'] + row['H2O']*((W_O2/2)/(W_O2/2 + W_H2))


def get_Z_H(row):
    return row['H2'] + row['H2O'] * (W_H2 / (W_O2 / 2 + W_H2))


def get_Z_super_H(row):
    return (row['Z_H'] - Z_H2_2)/ (Z_H2_1 - Z_H2_2)


def get_Z_super_O(row):
    return (row['Z_O'] - Z_O2_2)/ (Z_O2_1 - Z_O2_2)


def get_A_column(row):
    return row['Z_super_H'] - row['Z_super_O']


def get_A(df):
    df['Z_O'] = df.apply(get_Z_O, axis=1)
    df['Z_H'] = df.apply(get_Z_H, axis=1)
    df['Z_super_H'] = df.apply(get_Z_super_H, axis=1)
    df['Z_super_O'] = df.apply(get_Z_super_O, axis=1)
    df['A'] = df.apply(get_A_column, axis=1)

    return df





