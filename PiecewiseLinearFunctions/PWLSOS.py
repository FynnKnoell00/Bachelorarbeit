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
y0 = mdl.continuous_var_matrix(keys1 = nbSupply, keys2 = nbDemand, name ="y0")
y1 = mdl.continuous_var_matrix(keys1 = nbSupply, keys2 = nbDemand, name ="y1")
y2 = mdl.continuous_var_matrix(keys1 = nbSupply, keys2 = nbDemand, name ="y2")
y3 = mdl.continuous_var_matrix(keys1 = nbSupply, keys2 = nbDemand, name ="y3")
y4 = mdl.continuous_var_matrix(keys1 = nbSupply, keys2 = nbDemand, name ="y4")

for i in range(nbSupply):
    mdl.add_constraint(mdl.sum(x[i,j] for j in range(nbDemand)) == supply[i])

for j in range(nbDemand):
    mdl.add_constraint(mdl.sum(x[i,j] for i in range(nbSupply)) == demand[j])

for i in range(nbSupply):
    for j in range(nbDemand):
        ls = [y0[i,j] ,y1[i,j] , y2[i,j] , y3[i,j] , y4[i,j]]
        sos = mdl.add_sos2(ls)
        mdl.add(y0[i,j] + y1[i,j] + y2[i,j] + y3[i,j] + y4[i,j] == 1)
        mdl.add(c[i,j] == 0*y0[i,j] + 250*y1[i,j] + 400*y2[i,j] + 500*y3[i,j] + 500*y4[i,j])
        mdl.add(x[i,j] == 0*y0[i,j] + 250*y1[i,j] + 500*y2[i,j] + 1000*y3[i,j] + 2000*y4[i,j])


mdl.minimize(mdl.sum(c[i,j] for i in range(nbSupply) for j in range(nbDemand)))


solution = mdl.solve()
file1 = open('pwlsos.txt', 'w')
file1.write(mdl.export_as_lp_string())
print(mdl.objective_value)
print(mdl.solve_details)