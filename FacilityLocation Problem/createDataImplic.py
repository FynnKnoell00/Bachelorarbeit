"""
    Data Generation Script for capacitated facility location problem Models
    """
#imports
import random

"""
    Generates two random variables between the input values

    Parameters:
    - minValue: Minimum value for the random integers.
    - maxValue: Maximum value for the random integers.

    Returns:
    A random integers.
    """
def generate_random_value(minValue, maxValue):
    # Generates a random value within the specified range [minValue, maxValue]
    value1 = random.randint(minValue, maxValue)

    # Returns the generated value
    return value1

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
    matrix = [[generate_random_value(minValue, maxValue) for _ in range(cols)] for _ in range(rows)]

    # Return the generated matrix
    return matrix

"""
    Generate a random list with specified number of entries and values within a given range.

    Parameters:
    - entries: Number of entries in the list.
    - minValue: Minimum value for the random integers.
    - maxValue: Maximum value for the random integers.

    Returns:
    A list filled with random integers.
    """
def generate_random_list(entries, minValue, maxValue):
    # Use list comprehension to generate a list with random integers
    list = [generate_random_value(minValue, maxValue) for _ in range(entries)]

    # Returns the generated list
    return list

"""
    Write data to a file with a specific format.

    Parameters:
    - value1: First value to be written at the beginning of the file.
    - value2: Second value to be written at the beginning of the file.
    - data1: list to be written as the first part.
    - data2: list to be written as the second part.
    - data3: list to be written as the third part.
    - data4: matrix to be written as the third part.
    - filename: Name of the file to be created or overwritten.

    Returns:
    None
    """
def write_to_file(value1, value2, data1, data2, data3, data4, filename):
    with open(filename, 'w') as file:
        # Write the first and second values at the beginning of the file
        file.write(f"nbFacilities = {value1}\tnbCustomers = {value2}\n\n")

        # Write all lists of values
        file.write("Fix costs for the facilities:\n")
        file.write(str(data1) + '\n')

        file.write("Maximum production for the facilities:\n")
        file.write(str(data2) + '\n')

        file.write("Demand of the customers:\n")
        file.write(str(data3) + '\n\n')

        # Write the second matrix
        file.write("Matrix with transport costs:\n")
        for row in data4:
            file.write('\t'.join(map(str, row)) + '\n')


# Generate random values for the amount of Facilities and Customers
amountFacilities = generate_random_value(1200,1500)
amountCustomers = generate_random_value(4500,6000)

# Generate fix costs for facilities and production of facilities
fixCostFacilities = generate_random_list(amountFacilities, 900, 1200)
maximumProduction = generate_random_list(amountFacilities, 75, 150)

# Generate demand of customers
demandCustomer = generate_random_list(amountCustomers, 5, 35)

# Generate matrice with random values (Transportation Cost for each Customer)
transportCosts = generate_random_matrix(amountFacilities, amountCustomers, 5, 25)

# Store the data in a text file
file_name = "testData.txt"
write_to_file(amountFacilities, amountCustomers, fixCostFacilities, maximumProduction, demandCustomer, transportCosts, file_name)