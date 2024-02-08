"""
    This script is designed to run a series of tests for transportation models with a piecewise linear cost function.

    It tests the data on 'PWLLinear.py' (Mixed-Integer-Programming model) for the transportation problem.
    It uses a linearisation to model piecewise linear functions.

    The script contains functions to read the input and build the optimization model.
    These models get solved and their solution gets stored in a file.
    """

# Import necessary module
from docplex.mp.model import Model
from testData import parse_data

"""
    Build an optimization model for a Transportation Problem with piecewise linear cost function.

    Parameters:
    - supply (list): A list representing the amount of supplies for each supplier.
    - nbSupply (int): The number of supplier in the problem.
    - demand (list): A list representing the demand for each customer.
    - nbDemand (int): The number of supplier in the problem.
    - breakpoints (list): A list representing the breakpoints for the piecewise linear function.
    - slopes (list):  A list representing the slopes for the piecewise linear function.

    Returns:
    An optimization model configured for a Transportation Problem with piecewise linear cost function.
    """
def build_model(supply, nbSupply, demand, nbDemand, breakpoints, slopes):
    # Create an optimization model for the transport problem with PWL cost functions
    mdl = Model("transportPWL")

    # Define decision variables
    x = mdl.integer_var_matrix(keys1=nbSupply, keys2=nbDemand, name="x")
    y0 = mdl.integer_var_matrix(keys1=nbSupply, keys2=nbDemand, name="y_0")
    y1 = mdl.integer_var_matrix(keys1=nbSupply, keys2=nbDemand, name="y_1")
    y2 = mdl.integer_var_matrix(keys1=nbSupply, keys2=nbDemand, name="y_2")
    y3 = mdl.integer_var_matrix(keys1=nbSupply, keys2=nbDemand, name="y_3")
    z1 = mdl.binary_var_matrix(keys1=nbSupply, keys2=nbDemand, name="z_1")
    z2 = mdl.binary_var_matrix(keys1=nbSupply, keys2=nbDemand, name="z_2")
    z3 = mdl.binary_var_matrix(keys1=nbSupply, keys2=nbDemand, name="z_3")
    c = mdl.continuous_var_matrix(keys1=nbSupply, keys2=nbDemand, name="c")

    # Add supply constraints
    for i in range(nbSupply):
        mdl.add_constraint(mdl.sum(x[i, j] for j in range(nbDemand)) == supply[i])

    # Add demand constraints
    for j in range(nbDemand):
        mdl.add_constraint(mdl.sum(x[i, j] for i in range(nbSupply)) == demand[j])

    # Define cost and assignment constraints
    mdl.add(c[i, j] == slopes[0]*y0[i, j] + slopes[1]*y1[i, j] + slopes[2]*y2[i, j] + slopes[3]*y3[i, j] 
            for i in range(nbSupply) for j in range(nbDemand))
    mdl.add(x[i, j] == y0[i, j] + y1[i, j] + y2[i, j] + y3[i, j] for i in range(nbSupply) for j in range(nbDemand))

    # Add constraints for each breakpoint and corresponding binary variables
    mdl.add(breakpoints[1][0]*z1[i, j] <= y0[i, j] for i in range(nbSupply) for j in range(nbDemand))
    mdl.add(y0[i, j] <= breakpoints[1][0] for i in range(nbSupply) for j in range(nbDemand))

    mdl.add((breakpoints[2][0] - breakpoints[1][0])*z2[i, j] <= y1[i, j] for i in range(nbSupply) for j in range(nbDemand))
    mdl.add(y1[i, j] <= (breakpoints[2][0] - breakpoints[1][0])*z1[i, j] for i in range(nbSupply) for j in range(nbDemand))

    mdl.add((breakpoints[3][0] - breakpoints[2][0])*z3[i, j] <= y2[i, j] for i in range(nbSupply) for j in range(nbDemand))
    mdl.add(y2[i, j] <= (breakpoints[3][0] - breakpoints[2][0])*z2[i, j] for i in range(nbSupply) for j in range(nbDemand))

    mdl.add(0 <= y3[i, j] for i in range(nbSupply) for j in range(nbDemand))
    mdl.add(y3[i, j] <= (breakpoints[4][0] - breakpoints[3][0])*z3[i, j] for i in range(nbSupply) for j in range(nbDemand))

    # Minimize the sum of costs
    mdl.minimize(mdl.sum(c[i, j] for i in range(nbSupply) for j in range(nbDemand)))

    return mdl

# Set timelimit to 600 seconds = 10 minutes for the model
timeLimit = 600

"""
    Solve the given model and print the solution to a file.

    Parameters:
    - model: The optimization model to be solved.
    - timeLimit (integer): The time limit for solving the model.

    Returns:
    None
    """
def solve_and_save_solution(model):
    # Set the time limit for solving the model
    model.parameters.timelimit= timeLimit
    # Solve the model
    solution = model.solve()

    if(solution != None):
        # Check if the solution was found within the time limit
        if (timeLimit < model.solve_details.time):
            # Write the solution time to the file, punishment if the problem couldn't be solved (doubled solve time) 
            with open("solution_Linear.txt", "a") as solfile:
                solfile.write("time = " + str(model.solve_details.time * 2) + "\n")
        else:
            # Write the solution time to the file
            with open("solution_Linear.txt", "a") as solfile:
                solfile.write("time = " + str(model.solve_details.time) + "\n")

        # Save the objective value and if the objective value is the optimal solution
        with open("solution_Value.txt", "a") as solfile:
            solfile.write("statusLinear = " + str(model.solve_details.status) + " = " + str(int(solution.get_objective_value())) +  ",     ")

# Get the testData
filename = "testData.txt"
supply, nbSupply, demand, nbDemand, breakpoints, slopes = parse_data(filename)

# Build the model
model = build_model(supply, nbSupply, demand, nbDemand, breakpoints, slopes)

# Solve and save the solution in the file
solve_and_save_solution(model)