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
B = 15
N = 11
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
X_MAX = 3


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
Test
    X - the 11-dimentional design variable
"""
def test(X):
    # Compute & print the corresponding objective function value
    print(f(X))

    # Compute & print the corresponding constraint values
    # (g >= 0 means the constraint is met)

    # Budget constraint
    print(g1(X))

    # Nutritional constraints - lower bounds
    print(g2(X), g3(X), g4(X))

    # Nutritional constraints - upper bounds (this is optional)
    print(g5(X), g6(X), g7(X))

"""
Negate each element of an array
"""
neg = lambda arr: [-a for a in arr]

"""
Print each element of an array
"""
def print_arr(arr):
    for a in arr:
        print(round(a, 3))
