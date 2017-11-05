import cvxpy as cvx

x = cvx.Variable()
y = cvx.Variable()
objective = cvx.Maximize(40*x + 50*y)
constraints = [2*x + y <= 32, 2*x + 3*y <= 48]
prob = cvx.Problem(objective, constraints)
result = prob.solve()
print(result)
print(x.value)
print(y.value)

