from docplex.mp.model import Model
import matplotlib.pyplot as plt
import random

#input values
supply = [1000.0, 850.0, 1250.0]
#supply = []
#nbSupply = random.randint(5,10)
#supplyValue = 0
#for i in range(nbSupply):
#    v = random.randint(0,2000)
#    supply.append(v)
#    supplyValue = supplyValue + v


demand = [900.0, 1200.0, 600.0, 400.0]
#demand = []
#nbDemand = random.randint(5,10)
#demandValue = 0
#for i in range(nbDemand):
#    ul = min(2000, supplyValue - demandValue)
#    v = random.randint(0,ul)
#    demand.append(v)
#    demandValue = demandValue + v
#
#diff = supplyValue - demandValue
#if(diff >= 0):
#    demand[0] += diff
#else:
#   supply[0] += diff

nbSupply = len(supply)
nbDemand = len(demand)


# transport problem with pwl cost functions
mdl = Model("transportPWL")
x = mdl.integer_var_matrix(keys1 = nbSupply, keys2 = nbDemand, name ="x")
c = mdl.continuous_var_matrix(keys1 = nbSupply, keys2 = nbDemand,name ="c")

for i in range(nbSupply):
    mdl.add_constraint(mdl.sum(x[i,j] for j in range(nbDemand)) == supply[i])

for j in range(nbDemand):
    mdl.add_constraint(mdl.sum(x[i,j] for i in range(nbSupply)) == demand[j])

for i in range(nbSupply):
    for j in range(nbDemand):
        y = mdl.continuous_var_list(keys=5, name="y")
        sos = mdl.add_sos2(y)
        mdl.add(x[i,j] == 0*y[0] + 250*y[1] + 500*y[2] + 1000*y[3] + 2000*y[4])
        mdl.add(y[0] + y[1] + y[2] + y[3] + y[4] == 1)
        mdl.add(c[i,j] == 0*y[0] + 250*y[1] + 400*y[2] + 500*y[3] + 500*y[4])

mdl.minimize(mdl.sum(c[i,j] for i in range(nbSupply) for j in range(nbDemand)))


solution = mdl.solve()
file1 = open('pwlsos.txt', 'w')
file1.write(mdl.export_as_lp_string())
print(mdl.objective_value)
print(mdl.solve_details)