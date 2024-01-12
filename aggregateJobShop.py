"""
    This script assesses and compares the performance of different job shop scheduling models.

    The script includes functions to read times from a file, calculate statistics (lowest, highest, average, and total),
    calculate differences between corresponding times from two lists, and compare MIP and DIS times, along with
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
    Calculate differences between corresponding times from two lists.

    Parameters:
    - mip_times (list): List of times from the MIP (Mixed-Integer Programming) model.
    - dis_times (list): List of times from the DIS (Disjunction) model.

    Returns:
    A tuple containing the biggest difference, smallest difference, average difference
    (rounded to 3 decimal places), and a list of time differences.
    """
def calculate_time_differences(mip_times, dis_times):
    # Calculate absolute differences between corresponding times in MIP and DIS
    time_differences = [abs(mip - dis) for mip, dis in zip(mip_times, dis_times)]

    # Find the biggest and smallest differences
    biggest_difference = round(max(time_differences), 3)
    smallest_difference = round(min(time_differences), 3)

    # Calculate the average difference by dividing the sum by the number of elements
    average_difference = round(sum(time_differences) / len(time_differences), 3)

    # Return the calculated differences as a tuple
    return biggest_difference, smallest_difference, average_difference, time_differences

"""
    Compare MIP and DIS times, calculate statistics, and save the results to a file.

    Parameters:
    - mip_times (list): List of times from the MIP (Mixed-Integer Programming) model.
    - dis_times (list): List of times from the DIS (Disjunction) model.
    - file_path (str): The path to the file where the results will be saved.
    - timelimit (integer): The time limit considered for determining if the timelimit is exceeded for both problems.

    Returns:
    None
    """
def compare_and_save_stats(mip_times, dis_times, file_path, timelimit):
    # Calculate statistics for MIP times
    mip_lowest, mip_highest, mip_average, mip_total_time = calculate_stats(mip_times)

    # Calculate statistics for DIS times
    dis_lowest, dis_highest, dis_average, dis_total_time = calculate_stats(dis_times)
    
    # Calculate time differences between MIP and DIS
    average_diff, time_diffs = calculate_time_differences(mip_times, dis_times)

    # Count how many times MIP or DIS was faster
    mip_faster_count = sum(1 for mip, dis in zip(mip_times, dis_times) if mip < dis)
    dis_faster_count = sum(1 for mip, dis in zip(mip_times, dis_times) if dis < mip)

    # Count how many times the timelimit is exceeded for MIP and DIS
    mip_timelimit_exceeded_count = sum(1 for time in mip_times if time > timelimit)
    dis_timelimit_exceeded_count = sum(1 for time in dis_times if time > timelimit)

     # Write the results to the specified file
    with open(file_path, "w") as file:
        file.write("MIP Statistics:\n")
        file.write(f"Lowest Time:     {mip_lowest} sec\n")
        file.write(f"Highest Time:    {mip_highest} sec\n")
        file.write(f"Average Time:    {mip_average} sec\n")
        file.write(f"Total Time:      {mip_total_time} sec\n")
        file.write(f"Timelimit Exceeded Count: {mip_timelimit_exceeded_count} times\n\n")

        file.write("DIS Statistics:\n")
        file.write(f"Lowest Time:     {dis_lowest} sec\n")
        file.write(f"Highest Time:    {dis_highest} sec\n")
        file.write(f"Average Time:    {dis_average} sec\n")
        file.write(f"Total Time:      {dis_total_time} sec\n")
        file.write(f"Timelimit Exceeded Count: {dis_timelimit_exceeded_count} times\n\n")

        file.write("Comparison of Faster Times:\n")
        file.write(f"MIP was faster: {mip_faster_count} times\n")
        file.write(f"DIS was faster: {dis_faster_count} times\n\n")
        
        file.write("Time Differences:\n")
        file.write(f"Average Difference:  {average_diff} sec\n")

        # If MIP was faster at least once, write details
        if mip_faster_count > 0:
            file.write(f"Smallest Difference when MIP was faster: {min(time_diffs, key=lambda x: x if x > 0 else float('inf')):.3f} sec\n")
            file.write(f"Biggest Difference when MIP was faster: {max(time_diffs, key=lambda x: x if x > 0 else float('-inf')):.3f} sec\n")
        
        # If DIS was faster at least once, write details
        if dis_faster_count > 0:
            file.write(f"Smallest Difference when DIS was faster: {min(time_diffs, key=lambda x: x if x < 0 else float('inf')):.3f} sec\n")
            file.write(f"Biggest Difference when DIS was faster: {max(time_diffs, key=lambda x: x if x < 0 else float('-inf')):.3f} sec\n")

# Read times from the files
mip_time_file_path = "solution_MIP.txt"
dis_time_file_path = "solution_DIS.txt"

mip_times = read_times(mip_time_file_path)
dis_times = read_times(dis_time_file_path)


# Set timelimit to 600 seconds = 10 minutes
timelimit = 600

# Compare and save statistics to a new file
stats_comparison_file_path = "solutionJobShop.txt"
compare_and_save_stats(mip_times, dis_times, stats_comparison_file_path, 600)

# Print a message indicating that the statistics have been saved to the specified file
print("Statistics saved to 'solutionJobShop.txt'")
