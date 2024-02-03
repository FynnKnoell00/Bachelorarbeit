"""
    This script is designed to run a series of tests for an uncapacitated facility location problem.

    It tests the data on 'FLLinear.py' for the facility location problem.

    The script contains functions to read the input and build the optimization model.
    These models get solved and their solution gets stored in a file.
    """

#imports
from docplex.mp.model import Model
import re

"""
    Read problem data from a file and parse the necessary information.

    Parameters:
    - filename (str): The path to the file containing problem data.

    Returns:
    A tuple containing:
    - nbFacilities (int): The number of facilities in the problem.
    - nbCustomers (int): The number of customers in the problem.
    - fix_costs (list): A list representing the fix-cost for each facility.
    - max_production (list): A list representing the maximum amount of production for each facility.
    - demand (list): A list representing the demand for each customer.
    - transport_costs (list): A 2D list representing the transport costs between a facility and a customer.
    """
def parse_data(filename):
    with open(filename, 'r') as file:
        # Read all lines from the file
        lines = file.readlines()

        # Parse the values for jobs and machines (the first line)
        values_line = lines[0].strip().split('\t')
        nbFacilities =  int(re.search(r'\d+', values_line[0]).group())
        nbCustomers = int(re.search(r'\d+', values_line[1]).group())

        # Parse Fix costs for the facilities
        fix_costs_line = lines[3].split("[")[1].split("]")[0].split(", ")
        fix_costs = list(map(int, fix_costs_line))

        # Parse Maximum production for the facilities
        max_production_line = lines[5].split("[")[1].split("]")[0].split(", ")
        max_production = list(map(int, max_production_line))

        # Parse Demand of the customers
        demand_line = lines[7].split("[")[1].split("]")[0].split(", ")
        demand = list(map(int, demand_line))

        # Parse Matrix with transport costs
        transport_costs = []
        for line in lines[10:]:
            row = list(map(int, line.strip().split('\t')))
            transport_costs.append(row)

    return nbFacilities, nbCustomers, fix_costs, max_production, demand, transport_costs

# Example call
filename = "testData.txt"
nbFacilities, nbCustomers, fix_costs, max_production, demand, transport_costs = parse_data(filename)

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

# Set timelimit to 600 seconds = 10 minutes for the model
timeLimit = 600
mdl.parameters.timelimit= timeLimit

solution = mdl.solve()
if(solution != None):
    # Check if the solution was found within the time limit
    if (timeLimit < mdl.solve_details.time):
        # Write the solution time to the file, punishment if the problem couldn't be solved (doubled solve time) 
        with open("solution_Linear.txt", "a") as solfile:
            solfile.write("time = " + str(mdl.solve_details.time * 2) + "\n")
    else:
        # Write the solution time to the file
        with open("solution_Linear.txt", "a") as solfile:
            solfile.write("time = " + str(mdl.solve_details.time) + "\n")

    # Save the objective value and if the objective value is the optimal solution
    with open("solution_Value.txt", "a") as solfile:
        solfile.write("statusLinear = " + str(mdl.solve_details.status) + " = " + str(int(solution.get_objective_value())) +  ",     " + "\n")