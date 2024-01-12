from docplex.mp.model import Model
import docplex.cp.parameters as params

def read_problem_data(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

        # Parse random values
        values_line = lines[0].strip().split('\t')
        jobs = int(values_line[0])
        machines = int(values_line[1])

        # Parse matrix for Processing time
        matrix_procTime = []
        start_index = lines.index("Matrix with Random Values:\n") + 1
        end_index = lines.index("Matrix with Shuffled Column Indices:\n") - 1
        for line in lines[start_index:end_index]:
            row = list(map(int, line.strip().split('\t')))
            matrix_procTime.append(row)

        # Parse matrix for Job arrangement / Machine Sequence
        matrix_machineSequence = []
        start_index = lines.index("Matrix with Shuffled Column Indices:\n") + 1
        for line in lines[start_index:]:
            row = list(map(int, line.strip().split('\t')))
            matrix_machineSequence.append(row)

        return jobs, machines, matrix_procTime, matrix_machineSequence

# optimization model
def build_model(amount_jobs, amount_machines, machine_sequences, proc_times):
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
            mdl.add_constraint(y[machine_sequences[j][m+1], j] - y[machine_sequences[j][m], j] >= proc_times[j][m])

    for j in range(amount_jobs):
        for m in range(amount_machines):
            mdl.add_constraint(Cmax - y[machine_sequences[j][m], j] >= proc_times[j][m])

    for m in range(amount_machines):
        for j in range(amount_jobs):
            for l in range(amount_jobs):
                if j != l:
                    mdl.add_constraint(
                        mdl.logical_or(
                            y[machine_sequences[j][m], j] - y[machine_sequences[j][m], l] >= proc_times[l][m],
                            y[machine_sequences[j][m], l] - y[machine_sequences[j][m], j] >= proc_times[j][m]
                        )
                    )

    return mdl

# timelimit
timeLimit = 600

def solve_and_print_solution(model):
    model.parameters.timelimit= timeLimit
    solution = model.solve()
    #if (timeLimit < model.solve_details.time):
        #print("timelimit exceeded")
        #print(model.solve_details.time)
    #else:
        #print(solution.objective_value)
        #print(model.solve_details.time)
    with open("solution_DIS.txt", "a") as solfile:
            solfile.write("time = " + str(model.solve_details.time) + "\n")

            
# Initialize the problem data
filename = "testData.txt"
amountJobs, amountMachines, procTime, mS = read_problem_data(filename)

# Build the model
model = build_model(amountJobs, amountMachines, mS, procTime)

# Solve and print the solution
solve_and_print_solution(model)
