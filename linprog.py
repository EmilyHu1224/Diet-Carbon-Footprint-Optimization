"""
Scipy Linear Programming
"""
from base import *
from scipy.optimize import linprog

c = Y
A_ub = [C, neg(AP), neg(AC), neg(AF), AP, AC, AF]
b_ub = [B, -NP[0], -NC[0], -NF[0], NP[1], NC[1], NF[1]]
bounds = [(0, X_MAX) for i in range(0, N)]
res = linprog(c=c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='simplex')
# print(res)
# test(res.x)
print_arr(res.x)