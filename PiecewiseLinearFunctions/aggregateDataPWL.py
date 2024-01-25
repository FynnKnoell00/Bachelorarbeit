"""
    This script assesses and compares the performance of different transportation models with piecewise linear cost function.

    The script includes functions to read times from a file, calculate statistics (lowest, highest, average, and total),
    calculate differences between corresponding times from two lists, and compare Function, Linear and SOS model times, along with
    saving the results to a file.
    """

"""
    Read the value for the times from a file and return them as a list.

    Parameters:
    - file_path (str): The path to the file containing time data.

    Returns:
    A list of times read from the file, rounded to 3 decimal places.
    """
def read_times(file_path):
    # Open the file in read mode
    with open(file_path, "r") as file:
        # Extract times from each line, convert to float, and round to 3 decimal places
        times = [round(float(line.split('=')[1]), 3) for line in file]

    # Return the list of times
    return times

"""
    Calculate statistics (lowest, highest, average, and total) for a list of times.

    Parameters:
    - times (list): A list of times for which statistics are calculated.

    Returns:
    A tuple containing the lowest time, highest time, average time (rounded to 3 decimal places),
    and total time (rounded to 3 decimal places).
    """
def calculate_stats(times):
    # Find the lowest and highest times in the list
    lowest_time = min(times)
    highest_time = max(times)

    # Calculate the average time by dividing the sum by the number of elements
    average_time = round(sum(times) / len(times), 3)

    # Calculate the total time as the sum of all times
    total_time = round(sum(times), 3)

    # Return the calculated statistics as a tuple
    return lowest_time, highest_time, average_time, total_time

"""
    Calculate differences between corresponding times from three lists.

    Parameters:
    - func_times (list): List of times from the Function model.
    - linear_times (list): List of times from the Linear model.
    - sos_times (list): List of times from the SOS model.
    
    Returns:
    A list of tuples containing the average difference (rounded to 3 decimal places) and  the time differences.
    """
def calculate_time_differences(func_times, linear_times, sos_times):
    # Calculate absolute differences between corresponding times in lists
    differences1_2 = [(t1 - t2) for t1, t2 in zip(func_times, linear_times)]
    differences1_3 = [(t1 - t3) for t1, t3 in zip(func_times, sos_times)]
    differences2_3 = [(t2 - t3) for t2, t3 in zip(linear_times, sos_times)]
    abs_differences1_2 = [abs(t1 - t2) for t1, t2 in zip(func_times, linear_times)]
    abs_differences1_3 = [abs(t1 - t3) for t1, t3 in zip(func_times, sos_times)]
    abs_differences2_3 = [abs(t2 - t3) for t2, t3 in zip(linear_times, sos_times)]

    # Calculate the average differences by dividing the sum by the number of elements
    avg_diff_1_2 = round(sum(abs_differences1_2) / len(abs_differences1_2), 3)
    avg_diff_1_3 = round(sum(abs_differences1_3) / len(abs_differences1_3), 3)
    avg_diff_2_3 = round(sum(abs_differences2_3) / len(abs_differences2_3), 3)

    # Return the calculated differences as a tuple
    return (avg_diff_1_2, differences1_2), (avg_diff_1_3, differences1_3), (avg_diff_2_3, differences2_3)

"""
    Compare the three model times, calculate statistics, and save the results to a file.

    Parameters:
    - func_times (list): List of times from the Function model.
    - linear_times (list): List of times from the Linear model.
    - sos_times (list): List of times from the SOS model.
    - file_path (str): The path to the file where the results will be saved.
    - timelimit (integer): The time limit considered for determining if the timelimit is exceeded for both problems.

    Returns:
    None
    """
def compare_and_save_stats(func_times, linear_times, sos_times, file_path, timelimit):
    # Calculate statistics for function model
    func_lowest, func_highest, func_average, func_total_time = calculate_stats(func_times)

    # Calculate statistics for linear model
    linear_lowest, linear_highest, linear_average, linear_total_time = calculate_stats(linear_times)

    # Calculate statistics for sos model
    sos_lowest, sos_highest, sos_average, sos_total_time = calculate_stats(sos_times)
    

    # Calculate time differences between all times
    result = calculate_time_differences(func_times, linear_times, sos_times)
    average_diff_funclinear = result[0][0]
    time_diffs_funclinear = result[0][1]
    average_diff_funcsos =  result[1][0]
    time_diffs_funcsos =  result[1][1]
    average_diff_linearsos =  result[2][0]
    time_diffs_linearsos = result[2][1]

    # Count how many times the timelimit is exceeded for every model
    func_timelimit_exceeded_count = sum(1 for time in func_times if time > timelimit)
    linear_timelimit_exceeded_count = sum(1 for time in linear_times if time > timelimit)
    sos_timelimit_exceeded_count = sum(1 for time in sos_times if time > timelimit)

     # Write the results to the specified file
    with open(file_path, "w") as file:
        file.write(f"Simulated " + str(len(time_diffs_funclinear)) + " times\n\n")

        file.write("Function Statistics:\n")
        file.write(f"Lowest Time:     {func_lowest} sec\n")
        file.write(f"Highest Time:    {func_highest} sec\n")
        file.write(f"Average Time:    {func_average} sec\n")
        file.write(f"Total Time:      {func_total_time} sec\n")
        file.write(f"Timelimit Exceeded: {func_timelimit_exceeded_count} times\n\n")

        file.write("Linear Statistics:\n")
        file.write(f"Lowest Time:     {linear_lowest} sec\n")
        file.write(f"Highest Time:    {linear_highest} sec\n")
        file.write(f"Average Time:    {linear_average} sec\n")
        file.write(f"Total Time:      {linear_total_time} sec\n")
        file.write(f"Timelimit Exceeded: {linear_timelimit_exceeded_count} times\n\n")

        file.write("SOS Statistics:\n")
        file.write(f"Lowest Time:     {sos_lowest} sec\n")
        file.write(f"Highest Time:    {sos_highest} sec\n")
        file.write(f"Average Time:    {sos_average} sec\n")
        file.write(f"Total Time:      {sos_total_time} sec\n")
        file.write(f"Timelimit Exceeded: {sos_timelimit_exceeded_count} times\n\n")

        # caclulate the time differences for easier handling
        filtered_time_diffs_funclinear_pos = [time_diff for time_diff in time_diffs_funclinear if time_diff > 0]
        filtered_time_diffs_funclinear_neg = [time_diff for time_diff in time_diffs_funclinear if time_diff < 0]
        filtered_time_diffs_funcsos_pos = [time_diff for time_diff in time_diffs_funcsos if time_diff > 0]
        filtered_time_diffs_funcsos_neg = [time_diff for time_diff in time_diffs_funcsos if time_diff < 0]
        filtered_time_diffs_linearsos_pos = [time_diff for time_diff in time_diffs_linearsos if time_diff > 0]
        filtered_time_diffs_linearsos_neg = [time_diff for time_diff in time_diffs_linearsos if time_diff < 0]

        file.write("Comparison of Faster Times:\n")
        file.write(f"Function was faster than Linear: " + str(len(filtered_time_diffs_funclinear_neg)) + " times\n")
        file.write(f"Function was faster than SOS: " + str(len(filtered_time_diffs_funcsos_neg)) + " times\n")
        file.write(f"Linear was faster than Linear: " + str(len(filtered_time_diffs_funclinear_pos)) + " times\n")
        file.write(f"Linear was faster than SOS: " + str(len(filtered_time_diffs_linearsos_neg)) + " times\n")
        file.write(f"SOS was faster than Function: " + str(len(filtered_time_diffs_funcsos_pos)) + " times\n")
        file.write(f"SOS was faster than Linear: " + str(len(filtered_time_diffs_linearsos_pos)) + " times\n")
        file.write(f"No single fastest Model (same runtimes): " + str(3*len(time_diffs_funclinear)
                    - (len(filtered_time_diffs_funclinear_pos)
                    + len(filtered_time_diffs_funclinear_neg)
                    + len(filtered_time_diffs_funcsos_pos)
                    + len(filtered_time_diffs_funcsos_neg)
                    + len(filtered_time_diffs_linearsos_pos)
                    + len(filtered_time_diffs_linearsos_neg))) + " times\n\n")
        
        file.write("Time Differences:\n")
        file.write(f"Average Difference between Func and Linear:  {average_diff_funclinear} sec\n")
        file.write(f"Average Difference between Func and SOS:  {average_diff_funcsos} sec\n")
        file.write(f"Average Difference between Linear and SOS: {average_diff_linearsos} sec\n\n")


        
        # if function model was the faster, write extra information
        if len(filtered_time_diffs_funclinear_neg) > 0 or len(filtered_time_diffs_funcsos_neg) > 0:
            file.write(f"When Function was faster: \n")
            if len(filtered_time_diffs_funclinear_neg) > 0:
                file.write(f"Smallest Difference to Linear when Function was faster: {abs(max(filtered_time_diffs_funclinear_neg)):.3f} sec\n")
                file.write(f"Biggest Difference to Linear when Function was faster: {abs(min(filtered_time_diffs_funclinear_neg)):.3f} sec\n")
                
            if len(filtered_time_diffs_funcsos_neg) > 0:
                file.write(f"Smallest Difference to SOS when Function was faster: {abs(max(filtered_time_diffs_funcsos_neg)):.3f} sec\n")
                file.write(f"Biggest Difference to SOS when Function was faster: {abs(min(filtered_time_diffs_funcsos_neg)):.3f} sec\n\n")

        # if linear model was the faster, write extra information
        if len(filtered_time_diffs_funclinear_pos) > 0 or len(filtered_time_diffs_linearsos_neg) > 0:
            file.write(f"When Linear was faster: \n")
            if len(filtered_time_diffs_funclinear_pos) > 0:
                file.write(f"Smallest Difference to Function when Linear was faster: {min(filtered_time_diffs_funclinear_pos):.3f} sec\n")
                file.write(f"Biggest Difference to Function when Linear was faster: {max(filtered_time_diffs_funclinear_pos):.3f} sec\n")
            
            if len(filtered_time_diffs_linearsos_neg) > 0:
                file.write(f"Smallest Difference to SOS when Linear was faster: {abs(max(filtered_time_diffs_linearsos_neg)):.3f} sec\n")
                file.write(f"Biggest Difference to SOS when Linear was faster: {abs(min(filtered_time_diffs_linearsos_neg)):.3f} sec\n\n")

        # if sos model was the faster, write extra information
        if len(filtered_time_diffs_funcsos_pos) > 0 or len(filtered_time_diffs_linearsos_pos) > 0:
            file.write(f"When SOS was faster: \n")
            if len(filtered_time_diffs_funcsos_pos) > 0:
                file.write(f"Smallest Difference to Function when SOS was faster: {min(filtered_time_diffs_funcsos_pos):.3f} sec\n")
                file.write(f"Biggest Difference to Function when SOS was faster: {max(filtered_time_diffs_funcsos_pos):.3f} sec\n")
            
            if len(filtered_time_diffs_linearsos_pos) > 0:
                file.write(f"Smallest Difference to Linear when SOS was faster: {min(filtered_time_diffs_linearsos_pos):.3f} sec\n")
                file.write(f"Biggest Difference to Linear when SOS was faster: {max(filtered_time_diffs_linearsos_pos):.3f} sec\n\n")


# filepaths
func_time_file_path = "solution_Function.txt"
linear_time_file_path = "solution_Linear.txt"
sos_time_file_path = "solution_SOS.txt"

func_times = read_times(func_time_file_path)
linear_times = read_times(linear_time_file_path)
sos_times = read_times(sos_time_file_path)


# Set timelimit to 600 seconds = 10 minutes
timelimit = 600

# Compare and save statistics to a new file
stats_comparison_file_path = "solutionPWL.txt"
compare_and_save_stats(func_times, linear_times, sos_times, stats_comparison_file_path, timelimit)

# Print a message indicating that the statistics have been saved to the specified file
print("Statistics saved to 'solutionPWL.txt'")
