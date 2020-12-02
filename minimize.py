"""
SciPy minimize
"""
from base import *
from scipy.optimize import minimize

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