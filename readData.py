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

# Example usage
filename = "random_data.txt"
values1, values2, matrix1, matrix2 = read_from_file(filename)

print(f"Random values: {values1}, {values2}")
print("Matrix with Random Values:")
print(matrix1)
print("Matrix with Shuffled Column Indices:")
print(matrix2)
