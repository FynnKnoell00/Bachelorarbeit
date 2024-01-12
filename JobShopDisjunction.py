from docplex.mp.model import Model
import docplex.cp.parameters as params

def read_data(file_path):
    with open(file_path, "r") as parameters:
        amount_jobs = int(parameters.readline().strip())
        amount_machines = int(parameters.readline().strip())
        proc_time = [list(map(int, line.split(','))) for line in parameters.readline().strip().split('],')]
        machine_sequence = [list(map(int, line.split(','))) for line in parameters.readline().strip().split('],')]

    ops = []
    for i in range(amount_jobs):
        tuples = [(machine_sequence[i][j], proc_time[i][j]) for j in range(amount_machines)]
        ops.append(tuples)

    sorted_ops = [sorted(tuples) for tuples in ops]

    return amount_jobs, amount_machines, proc_time, machine_sequence, ops, sorted_ops

# optimization model
def build_JSC(amount_jobs, amount_machines, proc_time, machine_sequence):
    mdl = Model(name='MIP_Job_Shop')

    mdl.time_limit = 300

    # decision variables
    y = mdl.integer_var_matrix(amount_machines, amount_jobs, name='y')
    Cmax = mdl.integer_var(name='Cmax')

    # objective function
    mdl.minimize(Cmax)

    # constraints
    for j in range(amount_jobs):
        for m in range(amount_machines - 1):
            mdl.add_constraint(y[machine_sequence[j][m+1], j] - y[machine_sequence[j][m], j] >= proc_time[j][m])

    for j in range(amount_jobs):
        for m in range(amount_machines):
            mdl.add_constraint(Cmax - y[machine_sequence[j][m], j] >= proc_time[j][m])

    for m in range(amount_machines):
        for j in range(amount_jobs):
            for l in range(amount_jobs):
                if j != l:
                    mdl.add_constraint(
                        mdl.logical_or(
                            y[machine_sequence[j][m], j] - y[machine_sequence[j][m], l] >= proc_time[l][m],
                            y[machine_sequence[j][m], l] - y[machine_sequence[j][m], j] >= proc_time[j][m]
                        )
                    )

    return mdl

# timelimit
timeLimit = 600

def solve_JSC(model):
    model.parameters.timelimit= timeLimit
    solution = model.solve()
    return solution

def main():
    file_path = "testData.txt"
    amount_jobs, amount_machines, proc_time, machine_sequence, ops, sorted_ops = read_data(file_path)
    model = build_JSC(amount_jobs, amount_machines, proc_time, machine_sequence)
    solution = solve_JSC(model)
    if (timeLimit < model.solve_details.time):
        print("timelimit exceeded")
        print(model.solve_details.time)
    else:
        print(solution.objective_value)
        print(model.solve_details.time)
    
    with open("solution_DIS.txt", "a") as solfile:
        solfile.write("time = " + str(model.solve_details.time) + "\n")

if __name__ == "__main__":
    main()
