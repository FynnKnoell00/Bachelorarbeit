from docplex.mp.model import Model

#input values
def parse_testdata(filename):
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


# Beispielaufruf
supply, nbSupply, demand, nbDemand, breakpoints, slopes = parse_testdata("testdata.txt")

# transport problem with pwl cost functions
mdl = Model("transportPWL")
x = mdl.integer_var_matrix(keys1 = nbSupply, keys2 = nbDemand, name ="x")

for i in range(nbSupply):
    mdl.add_constraint(mdl.sum(x[i,j] for j in range(nbDemand)) == supply[i])

for j in range(nbDemand):
    mdl.add_constraint(mdl.sum(x[i,j] for i in range(nbSupply)) == demand[j])

pwf = mdl.piecewise(0, breakpoints, 0)
#pwf = mdl.piecewise_as_slopes([(0,0), (1,250), ((3/5),500), ((1/5),1000)], 0)
#pwf.plot(lx=-0, rx=20, k=1, color='b', marker='s', linewidth=2)

mdl.minimize(mdl.sum(pwf(x[i,j]) for i in range(nbSupply) for j in range(nbDemand)))

# Set timelimit to 600 seconds = 10 minutes for the model
timeLimit = 600

solution = mdl.solve()
if(mdl.solve_status != None):
    # Check if the solution was found within the time limit
    if (timeLimit < mdl.solve_details.time):
        # Write the solution time to the file, punishment if the problem couldn't be solved (doubled solve time) 
        with open("solution_Function.txt", "a") as solfile:
            solfile.write("time = " + str(mdl.solve_details.time * 2) + "\n")
    else:
        # Write the solution time to the file
        with open("solution_Function.txt", "a") as solfile:
            solfile.write("time = " + str(mdl.solve_details.time) + "\n")

    # Save the objective value and if the objective value is the optimal solution
    with open("solution_Value.txt", "a") as solfile:
        solfile.write("statusFunction = " + str(mdl.solve_details.status) + " = " + str(int(solution.get_objective_value())) +  ",     ")