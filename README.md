# Diet-Carbon-Footprint-Optimization
1. Constant definitions
2. Objective function (f)
3. Constraints (g1,g2, ..., g4)
4. Optioonal constraints - the upper bound of nutritional values (g5, g6, g7)

Install the dependencies with:
```
python -m pip install numpy scipy
```

Example usage:
```
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
```