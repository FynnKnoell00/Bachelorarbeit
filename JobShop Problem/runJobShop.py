"""
    This script is designed to run a series of tests for job shop scheduling models.
    It generates random data using 'createDataJobShop.py', tests the data on both 'JobShopMIP.py' (Mixed-Integer Programming model) and 'JobShopDisjunction.py' (Disjunction model), repeating the process multiple times.

    The script aims to assess and compare the performance of different job shop scheduling models.
    After each iteration, a message is printed to indicate the completion of the current iteration.
    The results are then aggregated using 'aggregateJobShop.py'.

    Usage:
    - Execute this script to perform multiple iterations of testing job shop scheduling models.
    - Ensure that the required model files ('createDataJobShop.py', 'JobShopMIP.py', 'JobShopDisjunction.py', 'aggregateJobShop.py') are present in the same directory.

    Note: This script assumes the existence and proper functioning of the mentioned model files.
    """

#imports
import os

# Amount of times the models get tested
R = range(0,100)

# The models get R times tested.
for i in R:
    # Execute the code from "createDataJobShop.py"
    with open("createDataJobShop.py") as f:
        exec(f.read())

    # Open the testData in read mode
        with open("testData.txt", 'r') as input_file:
            # Read the content
            content = input_file.read()

        # Open the save file in write mode
        with open(f"testData_{i}.txt", 'w') as output_file:
            # Write the content
            output_file.write(content)

    # Execute the code from "JobShopMIP.py"
    with open("JobShopMIP.py") as f:
        exec(f.read())

    # Execute the code from "JobShopDisjunction.py"
    with open("JobShopDisjunction.py") as f:
        exec(f.read())

    # Print a message indicating the completion of the iteration
    print("Iteration " + str(i + 1) + " is done.")

# Execute the code from "aggregateJobShop.py"
with open("aggregateJobShop.py") as f:
        exec(f.read())

# Remove testData file generated during the last test
os.remove("testData.txt")