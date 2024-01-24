

def read_times(file_path):
    # Open the file in read mode
    with open(file_path, "r") as file:
        # Extract times from each line, convert to float, and round to 3 decimal places
        times = [round(float(line.split('=')[1]), 3) for line in file]

    # Return the list of times
    return times

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

def compare_and_save_stats(func_times, linear_times, sos_times, file_path, timelimit):
    # Calculate statistics for 
    func_lowest, func_highest, func_average, func_total_time = calculate_stats(func_times)

    # Calculate statistics for 
    linear_lowest, linear_highest, linear_average, linear_total_time = calculate_stats(linear_times)

    # Calculate statistics for 
    sos_lowest, sos_highest, sos_average, sos_total_time = calculate_stats(sos_times)
    

    # Calculate time differences between 
    result = calculate_time_differences(func_times, linear_times, sos_times)
    average_diff_funclinear = result[0][0]
    time_diffs_funclinear = result[0][1]
    average_diff_funcsos =  result[1][0]
    time_diffs_funcsos =  result[1][1]
    average_diff_linearsos =  result[2][0]
    time_diffs_linearsos = result[2][1]

    # Count how many times 
    func_faster_count = sum(1 for func, linear, sos in zip(func_times, linear_times, sos_times) if (func < linear and func < sos))
    linear_faster_count = sum(1 for func, linear, sos in zip(func_times, linear_times, sos_times) if (linear < func and linear < sos))
    sos_faster_count = sum(1 for func, linear, sos in zip(func_times, linear_times, sos_times) if (sos < func and sos < linear))
    no_fastest = sum(1 for func, linear, sos in zip(func_times, linear_times, sos_times) if (not(func < linear and func < sos) and
                                                                                             not(linear < func and linear < sos) and
                                                                                             not (sos < func and sos < linear)))

    # Count how many times the timelimit is exceeded for 
    func_timelimit_exceeded_count = sum(1 for time in func_times if time > timelimit)
    linear_timelimit_exceeded_count = sum(1 for time in linear_times if time > timelimit)
    sos_timelimit_exceeded_count = sum(1 for time in sos_times if time > timelimit)

     # Write the results to the specified file
    with open(file_path, "w") as file:
        file.write(f"Simulated {func_faster_count + linear_faster_count + sos_faster_count + no_fastest} times\n\n")

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

        file.write("Comparison of Faster Times:\n")
        file.write(f"Function was fastest: {func_faster_count} times\n")
        file.write(f"Linear was fastest: {linear_faster_count} times\n")
        file.write(f"SOS was fastest: {sos_faster_count} times\n")
        file.write(f"No fastest Model (same runtimes): {no_fastest} times\n\n")
        
        file.write("Time Differences:\n")
        file.write(f"Average Difference between Func and Linear:  {average_diff_funclinear} sec\n")
        file.write(f"Average Difference between Func and SOS:  {average_diff_funcsos} sec\n")
        file.write(f"Average Difference between Linear and SOS: {average_diff_linearsos} sec\n\n")

        # ^
        filtered_time_diffs_funclinear_pos = [time_diff for time_diff in time_diffs_funclinear if time_diff > 0]
        filtered_time_diffs_funclinear_neg = [time_diff for time_diff in time_diffs_funclinear if time_diff < 0]
        filtered_time_diffs_funcsos_pos = [time_diff for time_diff in time_diffs_funcsos if time_diff > 0]
        filtered_time_diffs_funcsos_neg = [time_diff for time_diff in time_diffs_funcsos if time_diff < 0]
        filtered_time_diffs_linearsos_pos = [time_diff for time_diff in time_diffs_linearsos if time_diff > 0]
        filtered_time_diffs_linearsos_neg = [time_diff for time_diff in time_diffs_linearsos if time_diff < 0]
        
        if func_faster_count > 0:
            file.write(f"When Function was fastest: \n")
            file.write(f"Smallest Difference to Linear when Function was fastest: {abs(max(filtered_time_diffs_funclinear_neg)):.3f} sec\n")
            file.write(f"Smallest Difference to SOS when Function was fastest: {abs(max(filtered_time_diffs_funcsos_neg)):.3f} sec\n")
            file.write(f"Biggest Difference to Linear when Function was fastest: {abs(min(filtered_time_diffs_funclinear_neg)):.3f} sec\n")
            file.write(f"Biggest Difference to SOS when Function was fastest: {abs(min(filtered_time_diffs_funcsos_neg)):.3f} sec\n\n")
        #
        if linear_faster_count > 0:
            file.write(f"When Linear was fastest: \n")
            file.write(f"Smallest Difference to Function when Linear was fastest: {min(filtered_time_diffs_funclinear_pos):.3f} sec\n")
            file.write(f"Smallest Difference to SOS when Linear was fastest: {abs(max(filtered_time_diffs_linearsos_neg)):.3f} sec\n")
            file.write(f"Biggest Difference to Function when Linear was fastest: {max(filtered_time_diffs_funclinear_pos):.3f} sec\n")
            file.write(f"Biggest Difference to SOS when Linear was fastest: {abs(min(filtered_time_diffs_linearsos_neg)):.3f} sec\n\n")
        
        # 
        if sos_faster_count > 0:
            file.write(f"When SOS was fastest: \n")
            file.write(f"Smallest Difference to Function when SOS was fastest: {min(filtered_time_diffs_funcsos_pos):.3f} sec\n")
            file.write(f"Smallest Difference to Linear when SOS was fastest: {min(filtered_time_diffs_linearsos_pos):.3f} sec\n")
            file.write(f"Biggest Difference to Function when SOS was fastest: {max(filtered_time_diffs_funcsos_pos):.3f} sec\n")
            file.write(f"Biggest Difference to Linear when SOS was fastest: {max(filtered_time_diffs_linearsos_pos):.3f} sec\n\n")


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
