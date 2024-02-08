"""
    This script is designed to run a series of tests for an uncapacitated facility location problem.

    It tests the data on 'FLConditional.py' for the facility location problem.
    It uses the built-in functions from DOcplex to model if-then constraints.

    The script contains functions to read the input and build the optimization model.
    These models get solved and their solution gets stored in a file.
    """


#imports
from docplex.mp.model import Model
from readData import parse_data

# Get the testData
filename = "testData.txt"
nbFacilities, nbCustomers, fix_costs, max_production, demand, transport_costs = parse_data(filename)

# Create an optimization model for the facility location as linearized model
mdl = Model("flConditional")

# Define decision variables
x = mdl.binary_var_list(keys=nbFacilities, name="x")
y = mdl.continuous_var_matrix(keys1=nbFacilities, keys2=nbCustomers, name="y")

# Add Constraint for demands
for j in range(nbCustomers):
    mdl.add_constraint(mdl.sum(y[i,j] for i in range(nbFacilities)) == 1)

# Add Constraints that only opened facilities can only produce up to max_production
for i in range(nbFacilities):
    # Opened facilities can produce units
    mdl.add_constraint(mdl.if_then(x[i] == 1, mdl.sum(y[i,j] * demand[j] for j in range(nbCustomers)) <= max_production[i]))
    # Closed facilities can not produce units
    mdl.add_constraint(mdl.if_then(x[i] == 0, mdl.sum(y[i,j] * demand[j] for j in range(nbCustomers)) <= 0))

# Minimize the variable costs for each transport and the fix costs for each opened facility
mdl.minimize(mdl.sum(transport_costs[i][j] * demand[j] * y[i,j] * demand[j] for i in range(nbFacilities) for j in range(nbCustomers))
             + mdl.sum(fix_costs[i] * x[i] for i in range(nbFacilities)))

# Set timelimit to 600 seconds = 10 minutes for the model
timeLimit = 600
mdl.parameters.timelimit= timeLimit

solution = mdl.solve()
if(solution != None):
    # Check if the solution was found within the time limit
    if (timeLimit < mdl.solve_details.time):
        # Write the solution time to the file, punishment if the problem couldn't be solved (doubled solve time) 
        with open("solution_Cond.txt", "a") as solfile:
            solfile.write("time = " + str(mdl.solve_details.time * 2) + "\n")
    else:
        # Write the solution time to the file
        with open("solution_Cond.txt", "a") as solfile:
            solfile.write("time = " + str(mdl.solve_details.time) + "\n")

    # Save the objective value and if the objective value is the optimal solution
    with open("solution_Value.txt", "a") as solfile:
        solfile.write("statusCond = " + str(mdl.solve_details.status) + " = " + str(int(solution.get_objective_value())) +  ",     ")