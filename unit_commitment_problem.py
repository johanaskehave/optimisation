
import cvxpy as cvx

import numpy as np


# SPECIFICATIONS

maximum_power_output = [350, 200, 140] # p-_j
minimum_power_output = [50, 80, 40] # P__j
rampup_limit = [200, 100, 100] # S_j
rampdown_limit = [300, 150, 100] # T_j
variable_cost = [0.100, 0.125, 0.150] # A_j
fixed_cost = [5, 7, 6] # B_j
startup_cost = [20, 18, 5] # C_j
shutdown_cost =  [5, 3, 1] # E_j

power_output_t0 = [0, 0, 0] # the power output of the three units just before the first period of the planning horizon
online_t0 = [0, 0, 0] # a binary constant that is equal to 1; if unit j is online in the period preceding the first period of the planning horizon, and 0, otherwise.
startup_t0 = [0, 0, 0] # a binary constant that is equal to 1; if unit j is started up in the period preceding the first period of the planning horizon, and 0 otherwise (is used in the minimum uptime constraint).
shutdown_t0 = [0, 0, 0] # a binary constant that is equal to 1; if unit j is shutn down in the period preceding the first period of the planning horizon, and 0 otherwise (is used in the minimum down time constraint).

power_demand = [150, 500, 400] # each vector element represents the demand in each of the three hours
required_reserve = [15, 50, 40] # the amount of required reserve (over demand) in each of the three hours

assets = [0, 1, 2] # There are three assets
hours = [0, 1, 2] # There are three hours
no_of_assets = len(assets)
no_of_hours = len(hours)


# VARIABLES

# 1) p_jk: the output power of unit j during period k
# 2) y_jk: a binary variable that is equal to 1, if unit j is started up at the beginnig of period k and 0, otherwise
# 3) z_jk: a binary variable that is equal to 1, if unit j is shut down at the beginning of period k, and 0, otherwise
# 4) v_jk: a binary variable that is equal to 1, if unit j is online during period k and 0, otherwise

p_jk = cvx.Variable(no_of_assets, no_of_hours)
y_jk = cvx.Int(no_of_assets, no_of_hours)
z_jk = cvx.Int(no_of_assets, no_of_hours)
v_jk = cvx.Int(no_of_assets, no_of_hours)


# OBJECTIVE

# For each hour, for each unit, minimise: p_jk*B_j +  y_jk*C_j + z_jk*E_j + v_jk*A_j
# where,
# p_jk: the output power of unit j during period k
# B_j: the variable cost of unit j
# y_jk: a binary variable that is equal to 1, if unit j is started up at the beginnig of period k and 0, otherwise
# C_j: the startup cost of unit j
# z_jk: a binary variable that is equal to 1, if unit j is shut down at the beginning of period k, and 0, otherwise
# E_j: the shutdown cost of unit j
# v_jk: a binary variable that is equal to 1, if unit j is online during period k and 0, otherwise
# A_j: the fixed cost of unit j

objective = 0
for k in hours:
    for j in assets:
        objective += fixed_cost[j] * v_jk[j, k] + variable_cost[j] * p_jk[j, k] + startup_cost[j] * y_jk[j, k] + shutdown_cost[j] * z_jk[j, k]


# CONSTRAINTS

# 1) Minimum power output for the three assets cannot be below minimum_power_ouput.
# 2) Maximum power output for the three assets cannot exceed maximum_power_ouput.
# 3) Maximum rampup.
# 4) Maximum rampdown.
# 5) Any unit that is online can be shut down but not started up.
# 6) Demand should be satisfied in every period.
# 7) For security reasons, the total output power available online should be larger than the actual demand by a specified amount.

constraint_minimum_power_output = []
constraint_maximum_power_output = []
constraint_power_demand = []
constraint_maximum_rampup = []
constraint_maximum_rampdown = []
constraint_power_reserve = []
constraint_online = []
constraint_y_jk = []
constraint_z_jk = []
constraint_v_jk = []

for k in hours:
    constraint_power_demand.append( sum(p_jk[:, k]) >= power_demand[k] ) # constraint 6: power demand
    constraint_power_reserve.append( sum(np.array(maximum_power_output) * v_jk[:, k]) >=  power_demand[k] + required_reserve[k] ) # constraint 7: power reserve

    for j in assets:
        constraint_minimum_power_output.append( 1 / minimum_power_output[j] * p_jk[j, k] - v_jk[j , k] >= 0 ) # constraint 1: minimum power output
        constraint_maximum_power_output.append( 1 / maximum_power_output[j] * p_jk[j, k] - v_jk[j , k] <= 0 ) # constraint 2: maximum power output


        if(k == 0): #if we are in the first hour
            constraint_maximum_rampup.append( p_jk[j, k] - power_output_t0[j] <= rampup_limit[j] ) # constraint 4: Maximum rampup
            constraint_maximum_rampdown.append( power_output_t0[j] - p_jk[j, k] <= rampdown_limit[j] ) # constriant 5: Maximum rampdown
            constraint_online.append( y_jk[j, k] - z_jk[j, k] - v_jk[j, k] == - online_t0[k] ) # constraint 4: online units can be shutdown but not started

        else:
            constraint_maximum_rampup.append( p_jk[j, k] - p_jk[j, k - 1] <= rampup_limit[j] ) # Maximum rampup
            constraint_maximum_rampdown.append( p_jk[j, k - 1] - p_jk[j, k] <= rampdown_limit[j] )  # Maximum rampdown
            constraint_online.append( y_jk[j, k] - z_jk[j, k] - v_jk[j, k] + v_jk[j, k - 1] == 0 )

        # y_jk, z_jk and v_jk are integers between 0 and 1.
        constraint_y_jk.append(y_jk[j, k] <= 1)
        constraint_y_jk.append(y_jk[j, k] >= 0)
        constraint_z_jk.append(z_jk[j, k] <= 1)
        constraint_z_jk.append(z_jk[j, k] >= 0)
        constraint_v_jk.append(v_jk[j, k] <= 1)
        constraint_v_jk.append(v_jk[j, k] >= 0)

constraints = []
constraints.extend(constraint_minimum_power_output)
constraints.extend(constraint_maximum_power_output)
constraints.extend(constraint_maximum_rampup)
constraints.extend(constraint_maximum_rampdown)
constraints.extend(constraint_online)
constraints.extend(constraint_power_demand)
constraints.extend(constraint_power_reserve)
constraints.extend(constraint_y_jk)
constraints.extend(constraint_z_jk)
constraints.extend(constraint_v_jk)


# OPTIMISE

# Create problem
prob = cvx.Problem(cvx.Minimize(objective), constraints)
print(prob)

# Solve problem
result = prob.solve()

# Display results
print(result)
print(p_jk.value)
#print(y_jk.value)
#print(z_jk.value)
#print(v_jk.value)