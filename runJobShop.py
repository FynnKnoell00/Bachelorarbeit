"""
    This script is designed to run a series of tests for job shop scheduling models.
    It generates random data using 'createDataJobShop.py', tests the data on both 'JobShopMIP.py' (Mixed-Integer Programming model) and 'JobShopDisjunction.py' (Disjunction model), repeating the process multiple times.

    The script aims to assess and compare the performance of different job shop scheduling models.
    After each iteration, a message is printed to indicate the completion of the current iteration.
    The results are then aggregated using 'aggregateJobShop.py'.
    Temporary files generated during testing, namely 'solution_MIP.txt', 'solution_DIS.txt', and 'testData.txt', are removed at the end.

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

# Remove temporary files generated during testing
os.remove("solution_MIP.txt")
os.remove("solution_DIS.txt")
os.remove("testData.txt")