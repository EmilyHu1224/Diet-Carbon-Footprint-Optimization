"""
Import numpy and minimize solver
    install with:
    python -m pip install numpy scipy
"""
import numpy as np
from scipy.optimize import minimize
from scipy.optimize import linprog

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
#B = 5
B = 15
N = 11
# NP = (27.33, 45.33)
# NC = (75, 108.33)
# NF = (14.67, 26)
NP = (82, 136)
NC = (225, 325)
NF = (44, 78)
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
SciPy Solver
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
#print(solution)

"""
Scipy Linear Programming
"""

c = np.array(Y)
neg_AP = [element * -1 for element in AP]
neg_AC = [element * -1 for element in AC]
neg_AF = [element * -1 for element in AF]
lincons = np.array([C, neg_AP, neg_AC, neg_AF, AP, AC, AF])
B = np.array([B, NP[0], NC[0], NF[0], NP[1], NC[1], NF[1]])

linsoln = linprog(c=c, A_ub=lincons, b_ub=B) #, A_eq=None, b_eq=None, bounds=) #, method='interior-point', callback=None, options=None, x0=None)
#print(linsoln)

print('Optimal value:', linsoln.fun,
      '\nx values:', linsoln.x,
      '\nNumber of iterations performed:', linsoln.nit,
      '\nStatus:', linsoln.message)

"""
Playground
"""
def playground(linsoln):
    # Define the 11-dimentional design variable
    # e.g. let's see what happens if we only eat an egg for a meal
    X = linsoln.x
    
    """
    budget of $5 X values with linprog
    X = (
        8.62884858e-11,
        5.13805680e-11,
        1.95124527e-10,
        3.20702547e-12,
        2.68186648e-12,
        6.92533560e-12,
        4.04571075e-11,
        4.98268439e-12,
        5.85192330e-12,
        6.43568664e-13,
        1.17984902e-11,
    )
    """

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

playground(linsoln)
