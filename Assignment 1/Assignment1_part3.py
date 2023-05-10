#retrieve adiabatic flame temperature from CAE
#Compute (RHS) e^-(delG/(R0*T))
    # delG = delH^R - T delS
    # Get delH from reaction formation
    # get delS from engineeringtoolbox or something
#LHS: p_no^2 / (p_n2 * p_o2)
#--> n_no^2 / (n_n2*n_o2)
# compute n_no as we know n_n2 and n_o2 from complete combustion equation
# compute n_tot (products from combustion)
# now we have X_no  (n_no/n_tot)
