"""
    This script is designed to run a series of tests for job shop scheduling models.

    It tests the data on 'JobShopDisjunction.py' (Disjunction model) for the Job-Shop-Scheduling problem.

    The script contains functions to read the input and build the optimization model.
    These models get solved and their solution gets stored in a file.
"""
#imports
from docplex.mp.model import Model
from readData import parse_data

"""
    Build an optimization model for the Job Shop Scheduling Problem.

    Parameters:
    - amount_jobs (int): The number of jobs in the problem.
    - amount_machines (int): The number of machines in the problem.
    - machine_sequences (list): A 2D list representing machine sequences for each job.
    - proc_times (list): A 2D list representing processing times for each job on each machine.
    - transposed_matrix_procTime(list): A 2D list representing processing times for each job on each machine.

    Returns:
    An optimization model configured for the Job Shop Scheduling Problem.
    """
#optimization model
def build_model(amount_jobs, amount_machines, machine_sequences, proc_times, transposed_matrix_procTime):
    # Create an optimization model instance
    mdl = Model(name='MIP_Job_Shop')

    # Define decision variables
        # Job assignment matrix
    y = mdl.integer_var_matrix(amount_machines, amount_jobs, name='y')
        # Makespan variable
    Cmax = mdl.integer_var(name='Cmax')

    # Set the objective function to minimize makespan
    mdl.minimize(Cmax)

     # Add constraints to the model
    for j in range(amount_jobs):
        for m in range(amount_machines - 1):
            # Parsing the values that they look like the original constraints
            i = machine_sequences[j][m]
            k = machine_sequences[j][m+1]

            # The starting time of a job that starts on machine i and then goes on machine k can only start after the processing time 
            mdl.add_constraint(y[k, j] - y[i, j] >= transposed_matrix_procTime[m][j])

    for j in range(amount_jobs):
        for m in range(amount_machines):
            # Parsing the values that they look like the original constraints
            i = machine_sequences[j][m]
            # The makespan variable has to be at least as high, as every starting time and the corresponding processing time
            mdl.add_constraint(Cmax - y[i, j] >= transposed_matrix_procTime[m][j])

    for m in range(amount_machines):
        for j in range(amount_jobs):
            for l in range(amount_jobs):
                if j != l:
                    # Parsing the values that they look like the original constraints
                    i = machine_sequences[j][m]

                    # These constraints ensure that some ordering exists among operations of different jobs that have to be processed on the same machine
                    mdl.add_constraint(
                        mdl.logical_or(
                            y[i, j] - y[i, l] >= transposed_matrix_procTime[m][l],
                            y[i, l] - y[i, j] >= transposed_matrix_procTime[m][j]
                        )
                    )

    return mdl

# Set timelimit to 600 seconds = 10 minutes for the model
timeLimit = 600

"""
    Solve the given model and print the solution to a file.

    Parameters:
    - model: The optimization model to be solved.
    - timeLimit (integer): The time limit for solving the model.

    Returns:
    None
    """
def solve_and_save_solution(model):
    # Set the time limit for solving the model
    model.parameters.timelimit= timeLimit
    # Solve the model
    solution = model.solve()

    # Check if the solution was found within the time limit
    if (timeLimit < model.solve_details.time):
        # Write the solution time to the file, punishment if the problem couldn't be solved (doubled solve time) 
        with open("solution_DIS.txt", "a") as solfile:
            solfile.write("time = " + str(model.solve_details.time * 2) + "\n")

    else:
        # Write the solution time to the file
        with open("solution_DIS.txt", "a") as solfile:
            solfile.write("time = " + str(model.solve_details.time) + "\n")

    # Save the objective value and if the objective value is the optimal solution
    with open("solution_Value.txt", "a") as solfile:
        solfile.write("statusDIS = " + str(model.solve_details.status) + " = " + str(solution.get_objective_value()) + "\n")

            
# Initialize the problem data
filename = "testData.txt"
amountJobs, amountMachines, procTime, mS, transProcTime = parse_data(filename)

# Build the model
model = build_model(amountJobs, amountMachines, mS, procTime, transProcTime)

# Solve and save the solution in the file
solve_and_save_solution(model)
