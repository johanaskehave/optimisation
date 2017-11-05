


# Settings ----------------------------------------------------------------

library("lpSolveAPI")


# The problem -------------------------------------------------------------

# Suppose a farmer has 75 acres on which to plant two crops: wheat and barley. 
# To produce these crops, it costs the farmer (for seed, fertilizer, etc.) $120 per acre for the wheat and $210 per acre for the barley. 
# The farmer has $15000 available for expenses. But after the harvest, the farmer must store the crops while awaiting favourable market conditions. 
# The farmer has storage space for 4000 bushels. Each acre yields an average of 110 bushels of wheat or 30 bushels of barley.  
# If the net profit per bushel of wheat (after all expenses have been subtracted) is $1.30 and for barley is $2.00, how should the farmer plant the 75 acres to maximize profit?

# Costs of production per acre
wheat_prod_costs <- 120
barley_prod_costs <- 210

# Available expenses
bankroll <- 15000

# Corn storage capacity (no. of bushels)
storage_capacity <- 4000

# Corn yields (no. of bushels per acrre of land)
wheat_marginal_yield <- 110
barley_marginal_yield <- 30

# net profit per bushel
wheat_marginal_profit <- 1.3
barley_marginal_profit <- 2

# Available acres
available_acres <- 75


# Create the problem ------------------------------------------------------

lprec <- make.lp(0,2) # 2 because ncol should be 2. ncol is the number of decision variables (it is two because we have two types of corn)
lp.control(lprec, sense = "max") # we want to maximize our objective function
set.objfn(lprec, c(wheat_marginal_yield*wheat_marginal_profit, barley_marginal_yield*barley_marginal_profit)) # Objective is to maximise profit: (110*1.3)x + (30*2)y 

# Constraints
add.constraint(lprec, c(wheat_prod_costs, barley_prod_costs), "<=", bankroll) # Bankroll: 120x + 210y <= 15000
add.constraint(lprec, c(wheat_marginal_yield, barley_marginal_yield), "<=", storage_capacity) # Storage: 110x + 30y <= 4000
add.constraint(lprec, c(1,1), "<=", available_acres) # Acres: x + y <= 75

solve(lprec)

# Get maximum profit
get.objective(lprec)

# get the solution
get.variables(lprec)

# Thus, to achieve the maximum profit ($6315.625), the farmer should plant 21.875 acres of wheat and 53.125 acres of barley.