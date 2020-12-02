"""
SciPy minimize
"""
from base import *
from scipy.optimize import minimize
import timeit

x0 = [0 for i in range(0, N)]
bounds = [[X_MIN, X_MAX] for i in range(0, N)]
con1 = {'type': 'ineq', 'fun': g1}
con2 = {'type': 'ineq', 'fun': g2}
con3 = {'type': 'ineq', 'fun': g3}
con4 = {'type': 'ineq', 'fun': g4}
con5 = {'type': 'ineq', 'fun': g5}
con6 = {'type': 'ineq', 'fun': g6}
con7 = {'type': 'ineq', 'fun': g7}
cons = [con1, con2, con3, con4, con5, con6, con7]
res = minimize(f, x0, bounds=bounds, constraints=cons)
print_arr(res.x)
print(res)

"""
    Testing Various Minimize Methods
    * Currently Failing methods: 'Nelder-Mead', 'Powell', 'CG',
    'BFGS', 'Newton-CG', 'L-BFGS-B', 'TNC', 'COBYLA',
    'dogleg', 'trust-ncg', 'trust-exact', 'trust-krylov'
"""
mtds = ['SLSQP', 'trust-constr']
for mtd in mtds:
    print('=============', mtd, '=============')
    res = minimize(f, x0, bounds=bounds, constraints=cons, method=mtd)
    print('f(x):', res.fun)
    print('x:', res.x)
    print('iterations:', res.nit)
    # Compute the average time with timeit
    fun_str = "minimize(f, x0, bounds=bounds, constraints=cons, method=mtd)"
    # Run many times to reduce the effect of tasks running in parallel
    # -- this takes a minute
    elapsed_time = timeit.timeit(fun_str, number=1000, setup='from __main__ import ' + ', '.join(globals()))/1000
    print('ave. time: (s)', elapsed_time)
