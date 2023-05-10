import numpy as np

# Open the file and read the lines
with open('./../../cea-exec/C2H4.plt', 'r') as f:
    lines = f.readlines()



# Iterate over the lines
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

# Print the column names and the data
print(col_names)
print(data)
#
#
# import numpy as np
#
# # Open the file and read the lines
# with open('./../../cea-exec/C2H4.plt', 'r') as f:
#     lines = f.readlines()
#
# # Initialize the list for column names
# col_names = []
#
# # Iterate over the lines
# for line in lines:
#     # Skip the comments and empty lines
#     if line.startswith('#') or line.strip() == '':
#         continue
#
#     # Split the line into columns
#     cols = line.split()
#
#     # Store the column names
#     if not col_names:
#         col_names = cols
#         continue
#
#     # Convert the columns to floats and store the data
#     row = [float(x) for x in cols]
#     if not 'data' in locals():
#         data = np.array(row)
#     else:
#         data = np.vstack((data, row))
#
# # Print the column names and the data
# print(col_names)
# print(data)
