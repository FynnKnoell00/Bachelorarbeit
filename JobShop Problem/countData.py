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
        times = [round(float(line.split('=')[1]), 1) for line in file]

    # Return the list of times
    return times



def calculate_stats(times):

    zeroToFive = 0
    fivetoThirty = 0
    thirtyToSixty = 0
    SixtyToOnetw = 0
    onetwToThreeh = 0
    ThreehToSixh = 0
    sixhPlus = 0

    for i in times:
        if (i < 5):
            zeroToFive += 1
        else:

            if (i < 30):
                fivetoThirty += 1
            else:

                if (i < 60):
                    thirtyToSixty += 1
                else:

                    if (i < 120):
                        SixtyToOnetw += 1
                    else:

                        if (i < 300):
                            onetwToThreeh += 1
                        else:
        
                            if (i < 600):
                                ThreehToSixh += 1
                            else:

                                sixhPlus += 1

    return zeroToFive, fivetoThirty, thirtyToSixty, SixtyToOnetw, onetwToThreeh, ThreehToSixh, sixhPlus


mip_time_file_path = "solution_MIP.txt"
dis_time_file_path = "solution_DIS.txt"

mip_times = read_times(mip_time_file_path)
dis_times = read_times(dis_time_file_path)

a1, b1, c1, d1, e1, f1, g1 = calculate_stats(mip_times)
a2, b2, c2, d2, e2, f2, g2 = calculate_stats(dis_times)

stats_comparison_file_path = "countData.txt"
with open(stats_comparison_file_path, "w") as file:
        file.write("MIP: \n")
        file.write(f"0-5: {a1} \n")
        file.write(f"5-30: {b1} \n")
        file.write(f"30-60: {c1} \n")
        file.write(f"60-120: {d1} \n")
        file.write(f"120-300: {e1} \n")
        file.write(f"300-600: {f1} \n")
        file.write(f"600+: {g1} \n\n")

        file.write( "DIS: \n")
        file.write(f"0-5: {a2} \n")
        file.write(f"5-30: {b2} \n")
        file.write(f"30-60: {c2} \n")
        file.write(f"60-120: {d2} \n")
        file.write(f"120-300: {e2} \n")
        file.write(f"300-600: {f2} \n")
        file.write(f"600+: {g2} \n\n")

combined_tuple = list(zip(mip_times, dis_times))
combined_tuple = sorted(combined_tuple)

stats_comparison_file_path = "diffData.txt"
with open(stats_comparison_file_path, "w") as file:
    j = 1
    for i in combined_tuple:
        file.write(str(j) + ";" + str(i[0]) + ";" + str(i[1]) + "\n")
        j = j+1

print(combined_tuple)