"""
    import numpy and minimize solver
    can install with:
    python -m pip install numpy scipy
"""
import numpy as np
from scipy.optimize import minimize

"""
Constants
    B - budget
    N - number of food items under analysis
    NP - (Pmin, Pmax) minimum & maximum daily consumption of protein
    NC - (Cmin, Cmax) minimum & maximum daily consumption of carbohydrates
    NF - (Fmin, Fmax) minimum & maximum daily consumption of fat
    Y - GHG of food items (y1, y2, ..., yn)
    C - cost of food items (c1, c2, ..., cn)
    AP - amount of protein of food items (AP1, AP2, ..., APn)
    AC - amount of carbohydrates of food items (AP1, AP2, ..., APn)
    AF - amount of fat of food items (AP1, AP2, ..., APn)
"""
B = 5
N = 11
NP = (27.33, 45.33)
NC = (75, 108.33)
NF = (14.67, 26)
Y = (
    0.0826,
    0.0522,
    0.0624,
    0.774,
    1.05,
    0.139,
    0.049,
    0.332,
    0.45,
    4.5,
    0.225,
)
C = (
    0.205,
    0.574,
    0.452,
    0.648,
    0.634,
    0.540,
    0.2023,
    0.345,
    0.996,
    1.135,
    0.288,
)
AP = (
    1,
    0,
    3,
    9,
    12,
    7,
    3,
    2,
    19,
    26,
    6,
)

AC = (
    27,
    19,
    34,
    12,
    1,
    4,
    18,
    24,
    0,
    0,
    1,
)

AF = (
    0,
    0,
    0,
    5,
    17,
    4,
    0,
    0,
    7,
    10,
    5,
)

"""
Objective function
    Input: X - (x1, x2, ..., xn)
    Output: f(X) = SUM(xi * yi)
"""
f = lambda X: sum(X[i] * Y[i] for i in range(0, N))

"""
Constraint #1: budget limit
    g1 = budget - total cost >= 0
    Input: X - (x1, x2, ..., xn)
    Output: B - SUM(xi * ci)
"""
g1 = lambda X: B - sum(X[i] * C[i] for i in range(0, N))

"""
Constraint #2-4: nutritional values (lower bounds)  
    g = total amount - recommended amount >= 0
    e.g. g2 for protein:
    Input: X - (x1, x2, ..., xn)
    Output: SUM(xi * Ap,i) - NPmin
"""
g2 = lambda X: sum(X[i] * AP[i] for i in range(0, N)) - NP[0]
g3 = lambda X: sum(X[i] * AC[i] for i in range(0, N)) - NC[0]
g4 = lambda X: sum(X[i] * AF[i] for i in range(0, N)) - NF[0]

"""
Optional
Constraint #5-7: nutritional values (upper bounds)
    g = recommended amount - total amount >= 0
    e.g. g5 for protein:
    Input: X - (x1, x2, ..., xn)
    Output: NPmax - SUM(xi * Ap,i)
"""
g5 = lambda X: NP[1] - sum(X[i] * AP[i] for i in range(0, N))
g6 = lambda X: NC[1] - sum(X[i] * AC[i] for i in range(0, N))
g7 = lambda X: NF[1] - sum(X[i] * AF[i] for i in range(0, N))

"""
    Set Up for SciPy Solver
    * May want to comment if using "Playground" below
"""
x0 = [0 for i in range(0, N)]
b = [0, None]
bs = [b for i in range(0, N)]
con1 = {'type': 'ineq', 'fun': g1}
con2 = {'type': 'ineq', 'fun': g2}
con3 = {'type': 'ineq', 'fun': g3}
con4 = {'type': 'ineq', 'fun': g4}
con5 = {'type': 'ineq', 'fun': g5}
con6 = {'type': 'ineq', 'fun': g6}
con7 = {'type': 'ineq', 'fun': g7}
cons = [con1, con2, con3, con4, con5, con6, con7]
solution = minimize(f, x0, bounds=bs, constraints=cons)
print(solution)

"""
Playground
"""

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

# Compute & print the corresponding constraint values
# (g >= 0 means the constraint is met)

# Budget constraint
print(g1(X)) # 4.712 - aaaand it's within our budget :D

# Nutritional constraints - lower bounds
print(g2(X), g3(X), g4(X)) # (-21.33, -74, -9.67) - looks like we're not gonna have enough of any of the macronutrient tho:(

# Nutritional constraints - upper bounds (this is optional)
print(g5(X), g6(X), g7(X)) # (39.33, 107.33, 21) - well at least we're not gonna consume too much of anything


