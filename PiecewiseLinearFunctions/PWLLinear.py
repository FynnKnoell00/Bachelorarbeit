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


mdl.add(c[i,j] == y0[i,j] + 0.6*y1[i,j] + 0.2*y2[i,j] + 0*y3[i,j] for i in range(nbSupply) for j in range(nbDemand))
mdl.add(x[i,j] == y0[i,j] + y1[i,j] + y2[i,j] + y3[i,j] for i in range(nbSupply) for j in range(nbDemand))

mdl.add(250*z1[i,j] <= y0[i,j] for i in range(nbSupply) for j in range(nbDemand))
mdl.add(y0[i,j] <= 250 for i in range(nbSupply) for j in range(nbDemand))
mdl.add(250*z2[i,j] <= y1[i,j] for i in range(nbSupply) for j in range(nbDemand))
mdl.add(y1[i,j] <= 250*z1[i,j] for i in range(nbSupply) for j in range(nbDemand))
mdl.add(500*z3[i,j] <= y2[i,j] for i in range(nbSupply) for j in range(nbDemand))
mdl.add(y2[i,j] <= 500*z2[i,j] for i in range(nbSupply) for j in range(nbDemand))
mdl.add(0 <= y3[i,j] for i in range(nbSupply) for j in range(nbDemand))
mdl.add(y3[i,j] <= 1000*z3[i,j] for i in range(nbSupply) for j in range(nbDemand))

mdl.minimize(mdl.sum(c[i,j] for i in range(nbSupply) for j in range(nbDemand)))


solution = mdl.solve()
print(mdl.objective_value)
print(mdl.solve_details)