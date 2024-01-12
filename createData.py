import random

def generate_random_values():
    value1 = random.randint(8, 10)
    value2 = random.randint(8, 10)
    return value1, value2

def generate_random_matrix(rows, cols):
    return [[random.randint(1, 9) for _ in range(cols)] for _ in range(rows)]

def generate_shuffled_indices_matrix(rows, cols):
    # Create a matrix with column indices
    matrix = [[j for j in range(cols)] for _ in range(rows)]
    
    # Shuffle column values for each row
    for row in matrix:
        random.shuffle(row)

    return matrix

def write_to_file(data1, data2, value1, value2, filename):
    with open(filename, 'w') as file:
        file.write(f"{value1}\t{value2}\n")
        file.write("Matrix with Random Values:\n")
        for row in data1:
            file.write('\t'.join(map(str, row)) + '\n')
        file.write("\nMatrix with Shuffled Column Indices:\n")
        for row in data2:
            file.write('\t'.join(map(str, row)) + '\n')

# Generate random values
param1, param2 = generate_random_values()

# Generate matrices with random values and shuffled column indices
matrix_data_random_values = generate_random_matrix(int(param1), int(param2))
matrix_data_shuffled_indices = generate_shuffled_indices_matrix(int(param1), int(param2))

# Store the data in a text file
file_name = "random_data.txt"
write_to_file(matrix_data_random_values, matrix_data_shuffled_indices, param1, param2, file_name)

print(f"Random values: {param1}, {param2}")
print(f"Data stored in {file_name}")
