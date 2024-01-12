def read_times(file_path):
    with open(file_path, "r") as file:
        times = [round(float(line.split('=')[1]), 3) for line in file]
    return times

def calculate_stats(times):
    lowest_time = min(times)
    highest_time = max(times)
    average_time = round(sum(times) / len(times), 3)
    total_time = round(sum(times), 3)
    return lowest_time, highest_time, average_time, total_time

def calculate_time_differences(mip_times, dis_times):
    time_differences = [abs(mip - dis) for mip, dis in zip(mip_times, dis_times)]
    biggest_difference = round(max(time_differences), 3)
    smallest_difference = round(min(time_differences), 3)
    average_difference = round(sum(time_differences) / len(time_differences), 3)
    return biggest_difference, smallest_difference, average_difference

def compare_and_save_stats(mip_times, dis_times, file_path):
    mip_lowest, mip_highest, mip_average, mip_total_time = calculate_stats(mip_times)
    dis_lowest, dis_highest, dis_average, dis_total_time = calculate_stats(dis_times)
    
    biggest_diff, smallest_diff, average_diff = calculate_time_differences(mip_times, dis_times)

    # Comparison of how many times MIP or DIS was faster
    mip_faster_count = sum(1 for mip, dis in zip(mip_times, dis_times) if mip < dis)
    dis_faster_count = sum(1 for mip, dis in zip(mip_times, dis_times) if dis < mip)

    with open(file_path, "w") as file:
        file.write("MIP Statistics:\n")
        file.write(f"Lowest Time:     {mip_lowest} sec\n")
        file.write(f"Highest Time:    {mip_highest} sec\n")
        file.write(f"Average Time:    {mip_average} sec\n")
        file.write(f"Total Time:      {mip_total_time} sec\n\n")

        file.write("DIS Statistics:\n")
        file.write(f"Lowest Time:     {dis_lowest} sec\n")
        file.write(f"Highest Time:    {dis_highest} sec\n")
        file.write(f"Average Time:    {dis_average} sec\n")
        file.write(f"Total Time:      {dis_total_time} sec\n\n")

        file.write("Time Differences:\n")
        file.write(f"Biggest Difference:  {biggest_diff} sec\n")
        file.write(f"Smallest Difference: {smallest_diff} sec\n")
        file.write(f"Average Difference:  {average_diff} sec\n\n")

        file.write("Comparison of Faster Times:\n")
        file.write(f"MIP was faster: {mip_faster_count} times\n")
        file.write(f"DIS was faster: {dis_faster_count} times\n")

# Read times from the files
mip_time_file_path = "solution_MIP.txt"
dis_time_file_path = "solution_DIS.txt"

mip_times = read_times(mip_time_file_path)
dis_times = read_times(dis_time_file_path)

# Compare and save statistics to a new file
stats_comparison_file_path = "solutionJobShop.txt"
compare_and_save_stats(mip_times, dis_times, stats_comparison_file_path)

print("Statistics saved to 'solutionJobShop.txt'")
