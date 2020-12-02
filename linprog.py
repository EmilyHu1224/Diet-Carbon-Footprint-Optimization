"""
Scipy Linear Programming
"""
from base import *
from scipy.optimize import linprog
import timeit

c = Y
A_ub = [C, neg(AP), neg(AC), neg(AF), AP, AC, AF]
b_ub = [B, -NP[0], -NC[0], -NF[0], NP[1], NC[1], NF[1]]
bounds = [(X_MIN, X_MAX) for i in range(0, N)]
res = linprog(c=c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='simplex')
# print(res)
# test(res.x)
print_arr(res.x)

"""
    Testing Various Lin Prog Methods
"""
mtds = ['interior-point', 'revised simplex', 'simplex']
for mtd in mtds:
    print('=============', mtd, '=============')
    res = linprog(c=c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method=mtd)
    print('f(x):', res.fun)
    print('x:', res.x)
    print('iterations:', res.nit)
    # Compute the average time with timeit
    fun_str = "linprog(c=c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method=mtd)"
    # Run many times to reduce the effect of tasks running in parallel
    # -- this takes a minute
    elapsed_time = timeit.timeit(fun_str, number=1000, setup='from __main__ import ' + ', '.join(globals()))/1000
    print('ave. time: (s)', elapsed_time)
