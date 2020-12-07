"""
SciPy minimize
"""
from base import *
from scipy.optimize import minimize, NonlinearConstraint
import csv
import timeit

MAX_ITER = 500
arr2str = lambda arr: [str(int(round(x))) for x in arr]

x0 = [1 for i in range(0, N)]
bounds = [[X_MIN, X_MAX] for i in range(0, N)]
options = {'maxiter': MAX_ITER}

lower_bound = 0.2
upper_bound = 3
STEP_LENGTH = 0.1
NUM_STEPS = int(round((upper_bound - lower_bound) / STEP_LENGTH)) + 1

"""
    Configure method
    Either trust-constr or SLSQP
"""
METHOD = 'trust-constr'
rows = []
for i in range(0, NUM_STEPS):
    cv_max = lower_bound + i * STEP_LENGTH
    g13 = lambda X: cv_max - cv(X)

    if METHOD == 'trust-constr':
        # non-linear
        def cons_f(x):
            return cv(x)
        nlc1 = NonlinearConstraint(cons_f, 0, cv_max)
        cons = tc_constraints + [nlc1]
    else:
        base_cons = [{'type': 'ineq', 'fun': g} for g in CONSTRAINTS]
        cons = base_cons + [{'type': 'ineq', 'fun': g13}]

    res = minimize(f, x0, bounds=bounds, constraints=cons, options=options, method=METHOD)
    X = res.x
    # Compute the average time with timeit
    fun_str = "minimize(f, x0, bounds=bounds, constraints=cons, method=METHOD )"
    # Run many times to reduce the effect of tasks running in parallel
    # -- this takes a minute
    elapsed_time = timeit.timeit(fun_str, number=1000, setup='from __main__ import ' + ', '.join(globals())) / 1000
    print('ave. time: (s)', elapsed_time)
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
    row = [cv_max, fX, res.nit, elapsed_time] + Xstr
    print(row)
    rows.append(row)

with open('res.csv', 'w') as csvfile:
    w = csv.writer(csvfile)
    w.writerow(["CV max", "f*", "#. Iter.", "ave. time (s)"] + [str(i) for i in range(1, N+1)])
    for row in rows:
        w.writerow(row)


"""
    # Testing Various Minimize Methods
mtds = ['SLSQP', 'trust-constr']
for mtd in mtds:
    print('=============', mtd, '=============')
    res = minimize(f, x0, bounds=bounds, constraints=cons, method=mtd)
    print('f(x):', res.fun)
    print('x:', res.x)
    print('iterations:', res.nit)
    # Compute the average time with timeit
    # fun_str = "minimize(f, x0, bounds=bounds, constraints=cons, method=mtd)"
    # Run many times to reduce the effect of tasks running in parallel
    # -- this takes a minute
    elapsed_time = timeit.timeit(fun_str, number=1000, setup='from __main__ import ' + ', '.join(globals()))/1000
    print('ave. time: (s)', elapsed_time)
"""
