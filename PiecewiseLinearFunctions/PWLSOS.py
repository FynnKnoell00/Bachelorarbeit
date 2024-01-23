from docplex.mp.model import Model
import matplotlib.pyplot as plt
import random


nbBreakpoints = 6

# Generate random points
lsPoints = []
for i in range (0,nbBreakpoints):
    lsPoints.append((random.randint(0,20), random.randint(0,20)))

lsPoints = sorted(lsPoints)

print(lsPoints)

# create a new model to attach piecewise
pm = Model(name='pwl')
x = pm.continuous_var_list(keys=11, lb = 0, ub = 20, name='x')
y = pm.continuous_var_list(keys=11, name='y')
#f = pm.continuous_var_list(keys=10, name='y')
k = pm.continuous_var(lb = 0, name='k')

f1 = pm.piecewise(0, [lsPoints[0], lsPoints[5]], 0)
f2 = pm.piecewise(0, [lsPoints[0], lsPoints[1], lsPoints[5]], 0)
f3 = pm.piecewise(0, [lsPoints[0], lsPoints[2], lsPoints[5]], 0)
f4 = pm.piecewise(0, [lsPoints[0], lsPoints[3], lsPoints[5]], 0)
f5 = pm.piecewise(0, [lsPoints[0], lsPoints[4], lsPoints[5]], 0)
f6 = pm.piecewise(0, [lsPoints[0], lsPoints[1], lsPoints[2], lsPoints[5]], 0)
f7 = pm.piecewise(0, [lsPoints[0], lsPoints[1], lsPoints[3], lsPoints[5]], 0)
f8 = pm.piecewise(0, [lsPoints[0], lsPoints[1], lsPoints[4], lsPoints[5]], 0)
f9 = pm.piecewise(0, [lsPoints[0], lsPoints[2], lsPoints[3], lsPoints[5]], 0)
f10 = pm.piecewise(0, [lsPoints[0], lsPoints[2], lsPoints[4], lsPoints[5]], 0)
f11 = pm.piecewise(0, [lsPoints[0], lsPoints[3], lsPoints[4], lsPoints[5]], 0)
pm.add_constraint(y[0] == f1(x[0]))
pm.add_constraint(y[1] == f2(x[1]))
pm.add_constraint(y[2] == f3(x[2]))
pm.add_constraint(y[3] == f4(x[3]))
pm.add_constraint(y[4] == f5(x[4]))
pm.add_constraint(y[5] == f6(x[5]))
pm.add_constraint(y[6] == f7(x[6]))
pm.add_constraint(y[7] == f8(x[7]))
pm.add_constraint(y[8] == f9(x[8]))
pm.add_constraint(y[9] == f10(x[9]))
pm.add_constraint(y[10] == f11(x[10]))

#f1.plot(lx=0, rx=20, k=1, color='b', marker='s', linewidth=2)
#f2.plot(lx=-0, rx=20, k=1, color='b', marker='s', linewidth=2)
#f3.plot(lx=-0, rx=20, k=1, color='b', marker='s', linewidth=2)
#f4.plot(lx=-0, rx=20, k=1, color='b', marker='s', linewidth=2)
#f5.plot(lx=-0, rx=20, k=1, color='b', marker='s', linewidth=2)
#f6.plot(lx=-0, rx=20, k=1, color='b', marker='s', linewidth=2)
#f7.plot(lx=-0, rx=20, k=1, color='b', marker='s', linewidth=2)
#f8.plot(lx=-0, rx=20, k=1, color='b', marker='s', linewidth=2)
#f9.plot(lx=-0, rx=20, k=1, color='b', marker='s', linewidth=2)
#f10.plot(lx=-0, rx=20, k=1, color='b', marker='s', linewidth=2)
#f11.plot(lx=-0, rx=20, k=1, color='b', marker='s', linewidth=2)

#for i in range (1,nbBreakpoints):
    #if (y[0][0] == lsPoints[i][0]):
        #pm.add_constraint(z == pm.abs(y[0] - lsPoints[i]))

pm.add_constraint(k == pm.max(y[i] - x[i] for i in range (0,10)))
pm.maximize(k)

solution = pm.solve()
print(pm.objective_value)
print(pm.solve_details)