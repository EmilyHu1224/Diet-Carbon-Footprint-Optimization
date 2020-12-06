"""
SciPy minimize
"""
from base import *
from scipy.optimize import minimize
import csv
import timeit

MAX_ITER = 500
arr2str = lambda arr: [str(int(round(x))) for x in arr]

x0 = [1 for i in range(0, N)]
bounds = [[X_MIN, X_MAX] for i in range(0, N)]
base_cons = [{'type': 'ineq', 'fun': g} for g in CONSTRAINTS]
options = {'maxiter': MAX_ITER}
# print(res)
# print_arr(res.x)
# print_arr_raw(res.x, 0)
# test(res.x)

lower_bound = 0.2
upper_bound = 3
STEP_LENGTH = 0.1
NUM_STEPS = int(round((upper_bound - lower_bound) / STEP_LENGTH)) + 1
rows = []
for i in range(0, NUM_STEPS):
    cv_max = lower_bound + i * STEP_LENGTH
    g13 = lambda X: cv_max - cv(X)
    cons = base_cons + [{'type': 'ineq', 'fun': g13}]
    res = minimize(f, x0, bounds=bounds, constraints=cons, options=options)
    X = res.x
    print("-------------CV_MAX={}-----------------".format(cv_max))
    if not res.success:
        print("UH OH")
        print(res)
        continue
    fX = round(f(X), 4)
    Xstr = arr2str(X)
    print("#. iters: {}".format(res.nit))
    print("f*: {}".format(fX))
    print("x*: {}".format(' '.join(Xstr)))
    print("CV: {}".format(round(cv(X), 4)))
    row = [cv_max, fX, res.nit] + Xstr
    print(row)
    rows.append(row)

with open('res.csv', 'w') as csvfile:
    w = csv.writer(csvfile)
    w.writerow(["CV max", "f*", "#. Iter."] + [str(i) for i in range(1, N+1)])
    for row in rows:
        w.writerow(row)


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
