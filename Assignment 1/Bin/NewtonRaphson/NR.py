def NR(f, dfdx, x_0, tol_y):
    print('Begin Newton-Raphson\n--------------------------')
    running = True
    it = 0
    x_i = x_0
    while running:
        x_i_plus_1 = x_i - f(x_i) / dfdx(x_i)
        print(f'Iteration {it:03d} finished with adiabatic flame temperature = {x_i_plus_1:04.2f} [K]')
        curf = f(x_i_plus_1)
        grad = dfdx(x_i_plus_1)
        if abs(f(x_i_plus_1)) < tol_y:
            running = False
            print(f'Newton-Raphson converged to TAD = {x_i_plus_1:04.2f} [K]\n')
        x_i = x_i_plus_1

        it += 1

        if it > 20:
            running = False
            raise Exception('Newton-Raphson not converged')


    return x_i_plus_1