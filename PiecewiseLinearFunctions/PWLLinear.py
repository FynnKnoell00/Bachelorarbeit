"""
    This script is designed to run a series of tests for transportation models with a piecewise linear cost function.

    It tests the data on 'PWLLinear.py' (Mixed-Integer-Programming model) for the transportation problem.
    It uses a linearisation to model piecewise linear functions.

    The script contains functions to read the input and build the optimization model.
    These models get solved and their solution gets stored in a file.
    """

# Import necessary module
from docplex.mp.model import Model

def parse_testdata(filename):
    """
    Parse test data from a file.

    Parameters:
    - filename (str): The path to the file containing test data.

    Returns:
    A tuple containing:
    - supply (list): List of supply values.
    - nbSupply (int): Number of supplies.
    - demand (list): List of demand values.
    - nbDemand (int): Number of demands.
    - breakpoints (list): List of breakpoint coordinates.
    - slopes (list): List of slopes between breakpoints.
    """
    supply = []
    nbSupply = 0
    demand = []
    nbDemand = 0
    breakpoints = []
    slopes = []

    with open(filename, "r") as file:
        lines = file.readlines()

        # Parse Supply
        supply_line = lines[0].split("[")[1].split("]")[0].split(", ")
        supply = list(map(int, supply_line))

        # Parse nbSupply
        nbSupply = int(lines[1].split(": ")[1])

        # Parse Demand
        demand_line = lines[2].split("[")[1].split("]")[0].split(", ")
        demand = list(map(int, demand_line))

        # Parse nbDemand
        nbDemand = int(lines[3].split(": ")[1])
        
        # Parse Breakpoints
        breakpoints_index = lines.index("Generated Breakpoints:\n") + 1
        while "Slopes between Breakpoints:" not in lines[breakpoints_index]:
            values = lines[breakpoints_index].strip('()\n').split(', ')
            
            if len(values) == 2:
                x, y = map(int, values)
                breakpoints.append((x, y))
            
            breakpoints_index += 1

        # Parse Slopes
        slopes_index = lines.index("Slopes between Breakpoints:\n") + 1
        while slopes_index < len(lines) and lines[slopes_index] != "\n":
            slope_info = lines[slopes_index].split(": ")[1].strip()
            slope = float(slope_info)
            slopes.append(slope)
            slopes_index += 1

    return supply, nbSupply, demand, nbDemand, breakpoints, slopes

# Example call to parse_testdata
supply, nbSupply, demand, nbDemand, breakpoints, slopes = parse_testdata("testdata.txt")


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
        solfile.write("statusLinear = " + str(mdl.solve_details.status) + " = " + str(int(solution.get_objective_value())) +  ",     ")