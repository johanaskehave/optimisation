

# Settings ----------------------------------------------------------------

library("lpSolveAPI")


# The problem -------------------------------------------------------------

# http://www.durban.gov.za/documents/city_government/maths_science_Technology_Programme/mathematics-newsletter.pdf?Mobile=1

# A small business enterprise makes dresses and trousers. 

# To make a dress requires 1/2 hour of cutting and 20 minutes of sticthing. 
# To make trousers require 15 minutes of cutting and 1/2 hour of stitching. 

# The profit on a dress is R40 and on a pair of trousers R50. The business 
# operates for a maximum of 8 hours per day. 

# How many dresses and trousers should be made to maximize profit? What is the maximum profit?


# Create problem ----------------------------------------------------------

lprec <- make.lp(0,2) # We have dresses and trousers
lp.control(lprec, sense = "max") # We want to maximize profit
set.objfn(lprec, c(40, 50)) # Profit of a dress is 40 and 50 for a pair of trousers

# Constraints
add.constraint(lprec, c(2,1), "<=", 32) # Cutting time:   1/2 x + 1/4 y <= 8 --> 2x + y <= 32
add.constraint(lprec, c(2,3), "<=", 48) # Stitching time: 1/3 x + 1/2 y <= 8 --> 2x + 3y <= 48 

print(lprec)


# Solve problem -----------------------------------------------------------

solve(lprec)

# How many dresses and trousers should be made to maximise profit?
get.variables(lprec)

# What is the maximum profit?
get.objective(lprec)

#write.lp(lprec, "dresses_and_trousers.lp")

