"""
    Data Generation Script for Job Shop Scheduling Models
    """

import random

"""
    Generates two random variables between the input values

    Parameters:
    - minValue: Minimum value for the random integers.
    - maxValue: Maximum value for the random integers.

    Returns:
    A Tuple with random integers.
    """
def generate_random_values(minValue, maxValue):
    # Generate random values within the specified range [minValue, maxValue]
    value1 = random.randint(minValue, maxValue)
    value2 = random.randint(minValue, maxValue)

    # Return the generated values as a tuple
    return value1, value2

"""
    Generate a random matrix with specified dimensions and values within a given range.

    Parameters:
    - rows: Number of rows in the matrix.
    - cols: Number of columns in the matrix.
    - minValue: Minimum value for the random integers.
    - maxValue: Maximum value for the random integers.

    Returns:
    A 2D matrix (list of lists) filled with random integers.
    """
def generate_random_matrix(rows, cols, minValue, maxValue):
    # Use nested list comprehension to generate a matrix with random integers
    matrix = [[random.randint(minValue, maxValue) for _ in range(cols)] for _ in range(rows)]

    # Return the generated matrix
    return matrix

"""
    Generate a matrix with shuffled column indices for each row.

    Parameters:
    - rows: Number of rows in the matrix.
    - cols: Number of columns in the matrix.

    Returns:
    A 2D matrix (list of lists) with shuffled column indices for each row.
    """
def generate_shuffled_indices_matrix(rows, cols):
    # Create a matrix with column indices
    matrix = [[j for j in range(cols)] for _ in range(rows)]
    
    # Shuffle column values for each row
    for row in matrix:
        random.shuffle(row)

    # Return the matrix with shuffled column indices
    return matrix

"""
    Write data to a file with a specific format.

    Parameters:
    - data1: Matrix to be written as the first part.
    - data2: Matrix to be written as the second part.
    - value1: First value to be written at the beginning of the file.
    - value2: Second value to be written at the beginning of the file.
    - filename: Name of the file to be created or overwritten.

    Returns:
    None
    """
def write_to_file(data1, data2, value1, value2, filename):
    with open(filename, 'w') as file:
        # Write the first and second values at the beginning of the file
        file.write(f"{value1}\t{value2}\n")

        # Write the first matrix
        file.write("Matrix with Random Values:\n")
        for row in data1:
            file.write('\t'.join(map(str, row)) + '\n')

        # Write the second matrix
        file.write("\nMatrix with Shuffled Column Indices:\n")
        for row in data2:
            file.write('\t'.join(map(str, row)) + '\n')

# Generate random values for the amount of Jobs and Machines
amountJobs, amountMachines = generate_random_values(9,11)

# Generate matrices with random values (Processing Time for each Job) and shuffled column indices (machine Sequence for each Job)
matrix_data_random_values = generate_random_matrix(amountJobs, amountMachines, 1, 9)
matrix_data_shuffled_indices = generate_shuffled_indices_matrix(amountJobs, amountMachines)

# Store the data in a text file
file_name = "testData.txt"
write_to_file(matrix_data_random_values, matrix_data_shuffled_indices, amountJobs, amountMachines, file_name)
