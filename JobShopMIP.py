from docplex.mp.model import Model

def read_problem_data(file_path):
    with open(file_path, "r") as parameters:
        amount_jobs = int(parameters.readline().rstrip())
        jobs = range(amount_jobs)
        amount_machines = int(parameters.readline().rstrip())
        machines = range(amount_machines)

        proc_time_lines = parameters.readline().rstrip().split('],')
        proc_times = [[int(item) for item in line.split(',')] for line in proc_time_lines]

        machine_seq_lines = parameters.readline().rstrip().split('],')
        machine_sequences = [[int(item) for item in line.split(',')] for line in machine_seq_lines]

    ops = [list(zip(machine_sequences[i], proc_times[i])) for i in jobs]
    list_ops = [sorted(tuples) for tuples in ops]

    return amount_jobs, amount_machines, jobs, machines, proc_times, machine_sequences, ops, list_ops

def read_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

        # Parse random values
        values_line = lines[0].strip().split('\t')
        value1 = int(values_line[0])
        value2 = int(values_line[1])

        # Parse matrix with random values
        matrix_random_values = []
        start_index = lines.index("Matrix with Random Values:\n") + 1
        end_index = lines.index("Matrix with Shuffled Column Indices:\n") - 1
        for line in lines[start_index:end_index]:
            row = list(map(int, line.strip().split('\t')))
            matrix_random_values.append(row)

        # Parse matrix with shuffled column indices
        matrix_shuffled_indices = []
        start_index = lines.index("Matrix with Shuffled Column Indices:\n") + 1
        for line in lines[start_index:]:
            row = list(map(int, line.strip().split('\t')))
            matrix_shuffled_indices.append(row)

        return value1, value2, matrix_random_values, matrix_shuffled_indices


def build_model(amount_jobs, amount_machines, machine_sequences, proc_times):
    mdl = Model(name='MIP_Job_Shop')

    # Decision variables
    y = mdl.integer_var_matrix(amount_machines, amount_jobs, name='y')
    f = [(m1, j, m2, l) for m1 in range(amount_machines)
                        for j in range(amount_jobs)
                        for m2 in range(amount_machines)
                        for l in range(amount_jobs)]
    b = mdl.binary_var_dict(f, name='b')
    Cmax = mdl.integer_var(name='Cmax')

    # Objective function
    mdl.minimize(Cmax)

    # Constraints
    for j in range(amount_jobs):
        for m in range(amount_machines - 1):
            mdl.add_constraint(y[machine_sequences[j][m + 1], j] - y[machine_sequences[j][m], j] >= proc_times[j][m])

    for j in range(amount_jobs):
        for m in range(amount_machines):
            mdl.add_constraint(Cmax - y[machine_sequences[j][m], j] >= proc_times[j][m])

    bigM = 9999
    for m1 in range(amount_machines):
        for j in range(amount_jobs):
            for l in range(amount_jobs):
                if j != l:
                    mdl.add_constraint(y[machine_sequences[j][m1], j] + proc_times[j][m1]
                                       - bigM * (1 - b[machine_sequences[j][m1], j, machine_sequences[j][m1], l])
                                       <= y[machine_sequences[j][m1], l])
                    mdl.add_constraint(y[machine_sequences[j][m1], l] + proc_times[l][m1]
                                       - bigM * b[machine_sequences[j][m1], j, machine_sequences[j][m1], l]
                                       <= y[machine_sequences[j][m1], j])

    return mdl

# timelimit
timeLimit = 600

def solve_and_print_solution(model):
    model.parameters.timelimit= timeLimit
    solution = model.solve()
    print(solution.objective_value)
    print(model.solve_details.time)
    with open("solution_MIP.txt", "a") as solfile:
            solfile.write("time = " + str(model.solve_details.time) + "\n")

# Initialize the problem data
#file_path = "testData.txt"
#amountJobs, amountMachines, Jobs, Mchs, procTime, mS, Ops, listOps = read_problem_data(file_path)
            
# Example usage
filename = "random_data.txt"
amountJobs, amountMachines, procTime, mS = read_from_file(filename)

# Build the model
model = build_model(amountJobs, amountMachines, mS, procTime)

# Solve and print the solution
solve_and_print_solution(model)
