"""
    This script is designed to run a series of tests for transportation models with a piecewise linear cost function.

    It tests the data on 'PWLFunction.py' (Mixed-Integer-Programming model) for the transportation problem.
    It uses the built-in functions from DOcplex to model piecewise linear functions.

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

    # Add supply constraints
    for i in range(nbSupply):
        mdl.add_constraint(mdl.sum(x[i, j] for j in range(nbDemand)) == supply[i])

    # Add demand constraints
    for j in range(nbDemand):
        mdl.add_constraint(mdl.sum(x[i, j] for i in range(nbSupply)) == demand[j])

    # Define piecewise linear cost function
    pwf = mdl.piecewise(0, breakpoints, 0)

    # Minimize the sum of the piecewise linear cost function applied to decision variables
    mdl.minimize(mdl.sum(pwf(x[i, j]) for i in range(nbSupply) for j in range(nbDemand)))

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
            with open("solution_Function.txt", "a") as solfile:
                solfile.write("time = " + str(model.solve_details.time * 2) + "\n")
        else:
            # Write the solution time to the file
            with open("solution_Function.txt", "a") as solfile:
                solfile.write("time = " + str(model.solve_details.time) + "\n")

        # Save the objective value and if the objective value is the optimal solution
        with open("solution_Value.txt", "a") as solfile:
            solfile.write("statusFunction = " + str(model.solve_details.status) + " = " + str(int(solution.get_objective_value())) +  ",     ")

# Get the testData
filename = "testData.txt"
supply, nbSupply, demand, nbDemand, breakpoints, slopes = parse_data(filename)

# Build the model
model = build_model(supply, nbSupply, demand, nbDemand, breakpoints, slopes)

# Solve and save the solution in the file
solve_and_save_solution(model)