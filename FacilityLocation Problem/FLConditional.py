#imports
from docplex.mp.model import Model

nbFacilities = 3
nbCustomer = 3

fixCostFacilities = [10, 20, 15]
transportCosts = [[5,10,20], [10,20,5], [10,10,10]]
demandCustomer = [20,15,10]
maximumProduction = [30,30,30]

mdl = Model("flConditional")

# Define decision variables
x = mdl.binary_var_list(keys=nbFacilities, name="x")
y = mdl.continuous_var_matrix(keys1=nbFacilities, keys2=nbCustomer, name="y")

for j in range(nbCustomer):
    mdl.add_constraint(mdl.sum(y[i,j] for i in range(nbFacilities)) == 1)

for i in range(nbFacilities):
    mdl.add_constraint(mdl.if_then(x[i] == 1, mdl.sum(y[i,j] * demandCustomer[j] for j in range(nbCustomer)) <= maximumProduction[i]))
    mdl.add_constraint(mdl.if_then(x[i] == 0, mdl.sum(y[i,j] * demandCustomer[j] for j in range(nbCustomer)) <= 0))

mdl.minimize(mdl.sum(transportCosts[i][j] * demandCustomer[j] * y[i,j] * demandCustomer[j] for i in range(nbFacilities) for j in range(nbCustomer))
             + mdl.sum(fixCostFacilities[i] * x[i] for i in range(nbFacilities)))

# Set timelimit to 600 seconds = 10 minutes for the model
timeLimit = 600
mdl.parameters.timelimit= timeLimit

solution = mdl.solve()
print(solution)