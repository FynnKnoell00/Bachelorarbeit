"""
    This script is designed to run a series of tests for an capacitated facility location problem.

    It tests the data on 'FLLinear.py' for the facility location problem.

    The script contains functions to read the input and build the optimization model.
    These models get solved and their solution gets stored in a file.
    """

#imports
from docplex.mp.model import Model
from readData import parse_data

"""
    Build an optimization model for the Facility Location Problem.

    Parameters:
    - nbFacilities (int): The number of faciilities in the problem.
    - nbCustomers (int): The number of customers in the problem.
    - max_production (list): A list representing the maximum amount of products for each facility.
    - demand (list):  A list representing the demand for each customer.
    - transport_costs(list): A 2D list representing transport costs for each facility to each customer.

    Returns:
    An optimization model configured for the Facility Location Problem.
    """
def build_model(nbFacilities, nbCustomers, fix_costs, max_production, demand, transport_costs):
    # Create an optimization model for the facility location as linearized model
    mdl = Model("flLinear")

    # Define decision variables
    x = mdl.binary_var_list(keys=nbFacilities, name="x")
    y = mdl.continuous_var_matrix(keys1=nbFacilities, keys2=nbCustomers, name="y")

    # Add Constraint for demands
    for j in range(nbCustomers):
        mdl.add_constraint(mdl.sum(y[i,j] for i in range(nbFacilities)) == 1)

    # Add Constraint that opened facilities can only produce up to max_production
    for i in range(nbFacilities):
        mdl.add_constraint(mdl.sum(y[i,j] * demand[j] for j in range(nbCustomers)) <= max_production[i] * x[i])

    # Minimize the variable costs for each transport and the fix costs for each opened facility
    mdl.minimize(mdl.sum(transport_costs[i][j] * demand[j] * y[i,j] * demand[j] for i in range(nbFacilities) for j in range(nbCustomers))
                + mdl.sum(fix_costs[i] * x[i] for i in range(nbFacilities)))
    
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
            solfile.write("statusLinear = " + str(model.solve_details.status) + " = " + str(int(solution.get_objective_value())) +  ",     " + "\n")

# Get the testData
filename = "testData.txt"
nbFacilities, nbCustomers, fix_costs, max_production, demand, transport_costs = parse_data(filename)

# Build the model
model = build_model(nbFacilities, nbCustomers, fix_costs, max_production, demand, transport_costs)

# Solve and save the solution in the file
solve_and_save_solution(model)