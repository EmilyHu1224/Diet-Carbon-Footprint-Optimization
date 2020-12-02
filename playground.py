from base import *

# Define the 11-dimentional design variable
# e.g. let's see what happens if we only eat an egg for a meal
X = (
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    1,
)

# Compute & print the corresponding objective function value
print(f(X)) # 0.225 - hey that's a pretty low carbon footprint!

# Compute & print the corresponding constraint values (>=0 for meeting the constraints)
print(g1(X)) # 4.712 - aaaand it's within our budget :D
print(g2(X), g3(X), g4(X)) # (-21.33, -74, -9.67) - looks like we're not gonna have enough of any of the macronutrient tho:(
print(g5(X), g6(X), g7(X)) # (39.33, 107.33, 21) - well at least we're not gonna consume too much of anything

"""
Textbook LP problem
"""

from scipy.optimize import linprog
c = [-2, -1]
N = 2
f = lambda X: sum(c[i] * X[i] for i in range(0, N))
A_ub = [[4, 3], [2, 1], [1, 2]]
b_ub = [12, 4, 4]
bounds = [(0, None), (0, None)]
res = linprog(c=c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='simplex')
print(res)
print(f(res.x))
print(f([2, 0]))