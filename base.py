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
# from statistics import stdev, mean
import statistics
from scipy.optimize import LinearConstraint, NonlinearConstraint

NUM_DAYS = 7
B = 15 * NUM_DAYS
N = 18
NP = (82 * NUM_DAYS, 136 * NUM_DAYS)
NC = (225 * NUM_DAYS, 325 * NUM_DAYS)
NF = (44 * NUM_DAYS, 78 * NUM_DAYS)
Y = (
    0.0826,
    0.0522,
    0.0624,
    0.081,
    0.02121,
    0.0736,
    0.1722,
    0.774,
    0.0165,
    0.0605,
    1.05,
    0.139,
    0.049,
    0.332,
    0.45,
    4.5,
    0.225,
    0.474,
)
C = (
    0.205,
    0.574,
    0.452,
    0.20,
    0.75,
    0.352,
    0.246,
    0.648,
    0.0315,
    0.0547,
    0.634,
    0.540,
    0.2023,
    0.345,
    0.996,
    1.135,
    0.288,
    1.06,
)
AP = (
    1,
    0,
    3,
    4,
    2,
    1,
    1,
    9,
    0,
    0,
    12,
    7,
    3,
    2,
    19,
    26,
    6,
    21,
)
AC = (
    27,
    19,
    34,
    11,
    9,
    1,
    5,
    12,
    0,
    0,
    1,
    4,
    18,
    24,
    0,
    0,
    1,
    3,
)
AF = (
    0,
    0,
    0,
    0,
    15,
    0,
    0,    
    5,
    4,
    4,
    17,
    4,
    0,
    0,
    7,
    10,
    5,
    11,
)

# Specify an upper bound on the number of servings
# X_MIN = 1
# X_MAX = 3 * NUM_DAYS
X_MIN = 0
X_MAX = None

GROUP_RANGES = [
    range(0, 1),
    range(2, 6),
    range(7, 11),
    range(12, 13),
    range(14, 17),
]

GROUP_MIN = 3

GROUP_NAMES = [
    'fruits',
    'veggies',
    'dairy',
    'grains',
    'meat'
]


NAMES = (
    'Banana',
    "Apples",
    'Potato',
    'Peas',
    'Avocado',
    'Spinach',
    'Tomatoes',
    'Milk',
    'Margarine',
    'Butter',
    'Cheese',
    'Soymilk',
    'Bread',
    'White Rice',
    'Chicken',
    'Beef',
    'Eggs',
    'Tofu',
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
Additional constraint #8-12: minimum serving per food group
    g = total servings per group >= GROUP_MIN
    e.g. g8 for fruits:
        x1 + x2 >= GROUP_MIN
"""
g8 = lambda X: sum(X[i] for i in GROUP_RANGES[0]) - GROUP_MIN
g9 = lambda X: sum(X[i] for i in GROUP_RANGES[1]) - GROUP_MIN
g10 = lambda X: sum(X[i] for i in GROUP_RANGES[2]) - GROUP_MIN
g11 = lambda X: sum(X[i] for i in GROUP_RANGES[3]) - GROUP_MIN
g12 = lambda X: sum(X[i] for i in GROUP_RANGES[4]) - GROUP_MIN

"""
Additional constraint #13 - CV of the distribution
    g = std(X)/mean(X) <= CV_MAX
"""
cv = lambda X: statistics.stdev(X) / statistics.mean(X)

"""
All constraints
"""
CONSTRAINTS = (
    g1,
    g2,
    g3,
    g4,
    g5,
    g6,
    g7,
    # g8,
    # g9,
    # g10,
    # g11,
    # g12,
    # g13,
)

"""
    Define linear constraints for trust-constr method
"""
lc1 = LinearConstraint(C, [0], [B])
lc2 = LinearConstraint(AP, [NP[0]], [NP[1]])
lc3 = LinearConstraint(AC, [NC[0]], [NC[1]])
lc4 = LinearConstraint(AF, [NF[0]], [NF[1]])
tc_constraints = [lc1, lc2, lc3, lc4]


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

    # Coefficient of variation (CV) of the results
    print(cv(X))

"""
Negate each element of an array
"""
neg = lambda arr: [-a for a in arr]

"""
Print each element of an array
"""
def print_arr(arr):
    for i in range(0, len(arr)):
        print('#{} {}: {}'.format(str(i+1).zfill(2), NAMES[i], round(arr[i], 3)))
