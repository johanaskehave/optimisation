# http://www.cvxpy.org/en/latest/tutorial/intro/

import cvxpy as cvx

# Create the problem
x = cvx.Variable()
y = cvx.Variable()

objective = cvx.Maximize(143*x + 60*y) # Objective function

constraints = [120*x + 210*y <= 15000, # Bankroll
               110*x + 30*y <= 4000, # Storage
               x + y <= 75] # Acres

prob = cvx.Problem(objective, constraints)

# Solve the problem
result = prob.solve()
print(result)
print(x.value)
print(y.value)
