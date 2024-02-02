#imports
from docplex.mp.model import Model
import re

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

# Example usage
filename = "testData.txt"
nbFacilities, nbCustomers, fix_costs, max_production, demand, transport_costs = parse_data(filename)

mdl = Model("flConditional")

# Define decision variables
x = mdl.binary_var_list(keys=nbFacilities, name="x")
y = mdl.continuous_var_matrix(keys1=nbFacilities, keys2=nbCustomers, name="y")

for j in range(nbCustomers):
    mdl.add_constraint(mdl.sum(y[i,j] for i in range(nbFacilities)) == 1)

for i in range(nbFacilities):
    mdl.add_constraint(mdl.indicator_constraint(x[i], mdl.sum(y[i,j] * demand[j] for j in range(nbCustomers)) <= max_production[i]))
    mdl.add_constraint(mdl.indicator_constraint(x[i], mdl.sum(y[i,j] * demand[j] for j in range(nbCustomers)) <= 0, active_value=0))

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
        with open("solution_Indi.txt", "a") as solfile:
            solfile.write("time = " + str(mdl.solve_details.time * 2) + "\n")
    else:
        # Write the solution time to the file
        with open("solution_Indi.txt", "a") as solfile:
            solfile.write("time = " + str(mdl.solve_details.time) + "\n")

    # Save the objective value and if the objective value is the optimal solution
    with open("solution_Value.txt", "a") as solfile:
        solfile.write("statusIndi = " + str(mdl.solve_details.status) + " = " + str(int(solution.get_objective_value())) +  ",     ")