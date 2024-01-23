from docplex.mp.model import Model
import matplotlib.pyplot as plt


nbBreakpoints = 3

# create a new model to attach piecewise
pm = Model(name='pwl')
x = pm.continuous_var_list(keys=nbBreakpoints, lb = -5, ub = 5, name='x')
y = pm.continuous_var_list(keys=nbBreakpoints, lb = -5, ub = 5, name='y')
z = pm.continuous_var(name='z')
f = pm.continuous_var(name='f')
g = pm.continuous_var(lb = -5, ub = 5, name='g')

listBreakpoints = []
for i in range(nbBreakpoints):
    listBreakpoints.append((x[i], y[i]))


pwf = pm.piecewise(0, listBreakpoints, 0)

pm.add_constraint(z == pwf(g))
pm.add_constraint(f == pm.abs(z, g*g))
pm.minimize(f)

pwf.plot(lx=0, rx=5, k=1, color='b', marker='s', linewidth=2)
