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
y0 = mdl.integer_var_matrix(keys1 = nbSupply, keys2 = nbDemand, name="y_0")
y1 = mdl.integer_var_matrix(keys1 = nbSupply, keys2 = nbDemand, name="y_1")
y2 = mdl.integer_var_matrix(keys1 = nbSupply, keys2 = nbDemand, name="y_2")
y3 = mdl.integer_var_matrix(keys1 = nbSupply, keys2 = nbDemand, name="y_3")
z1 = mdl.binary_var_matrix(keys1 = nbSupply, keys2 = nbDemand, name="z_1")
z2 = mdl.binary_var_matrix(keys1 = nbSupply, keys2 = nbDemand, name="z_2")
z3 = mdl.binary_var_matrix(keys1 = nbSupply, keys2 = nbDemand, name="z_3")
c = mdl.continuous_var_matrix(keys1 = nbSupply, keys2 = nbDemand,name ="c")

for i in range(nbSupply):
    mdl.add_constraint(mdl.sum(x[i,j] for j in range(nbDemand)) == supply[i])

for j in range(nbDemand):
    mdl.add_constraint(mdl.sum(x[i,j] for i in range(nbSupply)) == demand[j])


mdl.add(c[i,j] == slopes[0]*y0[i,j] + slopes[1]*y1[i,j] + slopes[2]*y2[i,j] + slopes[3]*y3[i,j] for i in range(nbSupply) for j in range(nbDemand))
mdl.add(x[i,j] == y0[i,j] + y1[i,j] + y2[i,j] + y3[i,j] for i in range(nbSupply) for j in range(nbDemand))

mdl.add(breakpoints[1][0]*z1[i,j] <= y0[i,j] for i in range(nbSupply) for j in range(nbDemand))
mdl.add(y0[i,j] <= breakpoints[1][0]for i in range(nbSupply) for j in range(nbDemand))

mdl.add((breakpoints[2][0]-breakpoints[1][0])*z2[i,j] <= y1[i,j] for i in range(nbSupply) for j in range(nbDemand))
mdl.add(y1[i,j] <= (breakpoints[2][0]-breakpoints[1][0])*z1[i,j] for i in range(nbSupply) for j in range(nbDemand))

mdl.add((breakpoints[3][0]-breakpoints[2][0])*z3[i,j] <= y2[i,j] for i in range(nbSupply) for j in range(nbDemand))
mdl.add(y2[i,j] <= (breakpoints[3][0]-breakpoints[2][0])*z2[i,j] for i in range(nbSupply) for j in range(nbDemand))

mdl.add(0 <= y3[i,j] for i in range(nbSupply) for j in range(nbDemand))
mdl.add(y3[i,j] <= (breakpoints[4][0]-breakpoints[3][0])*z3[i,j] for i in range(nbSupply) for j in range(nbDemand))

mdl.minimize(mdl.sum(c[i,j] for i in range(nbSupply) for j in range(nbDemand)))


solution = mdl.solve()
if(mdl.solve_status != None):
    print(mdl.objective_value)
    print(mdl.solve_details)