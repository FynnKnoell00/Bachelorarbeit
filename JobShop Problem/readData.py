import re

"""
    Read problem data from a file and parse the necessary information.

    Parameters:
    - filename (str): The path to the file containing problem data.

    Returns:
    A tuple containing:
    - jobs (int): The number of jobs in the problem.
    - machines (int): The number of machines in the problem.
    - matrix_procTime (list): A 2D list representing the processing time matrix.
    - matrix_machineSequence (list): A 2D list representing the machine sequence matrix.
    - transposed_matrix_procTime(list): A 2D list representing the transposed processing time matrix.
    """
def parse_data(filename):
    # Open the file in read mode
    with open(filename, 'r') as file:
        # Read all lines from the file
        lines = file.readlines()

        # Parse the values for jobs and machines (the first line)
        values_line = lines[0].strip().split('\t')
        jobs =  int(re.search(r'\d+', values_line[0]).group())
        machines = int(re.search(r'\d+', values_line[1]).group())

        # Parse matrix for Processing time
        matrix_procTime = []
        start_index = lines.index("Matrix with Random Values:\n") + 1
        end_index = lines.index("Matrix with Shuffled Column Indices:\n") - 1
        for line in lines[start_index:end_index]:
            row = list(map(int, line.strip().split('\t')))
            matrix_procTime.append(row)

        # Transpose the matrix using zip and *
        transposed_matrix_procTime = list(map(list, zip(*matrix_procTime)))

        # Parse matrix for Job arrangement / Machine Sequence
        matrix_machineSequence = []
        start_index = lines.index("Matrix with Shuffled Column Indices:\n") + 1
        for line in lines[start_index:]:
            row = list(map(int, line.strip().split('\t')))
            matrix_machineSequence.append(row)

        # Return the parsed information as a tuple
        return jobs, machines, matrix_procTime, matrix_machineSequence, transposed_matrix_procTime