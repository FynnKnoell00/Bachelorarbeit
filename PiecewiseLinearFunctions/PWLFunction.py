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

for i in range(nbSupply):
    mdl.add_constraint(mdl.sum(x[i,j] for j in range(nbDemand)) == supply[i])

for j in range(nbDemand):
    mdl.add_constraint(mdl.sum(x[i,j] for i in range(nbSupply)) == demand[j])

pwf = mdl.piecewise(0, [(0,0), (250,250), (500,400), (1000,500)], 0)
#pwf = mdl.piecewise_as_slopes([(0,0), (1,250), ((3/5),500), ((1/5),1000)], 0)
#pwf.plot(lx=-0, rx=20, k=1, color='b', marker='s', linewidth=2)

mdl.minimize(mdl.sum(pwf(x[i,j]) for i in range(nbSupply) for j in range(nbDemand)))


solution = mdl.solve()
file1 = open('pwlfunc.txt', 'w')
file1.write(mdl.export_as_lp_string())
print(solution)
print(mdl.solve_details)