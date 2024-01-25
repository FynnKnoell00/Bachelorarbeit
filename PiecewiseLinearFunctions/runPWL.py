"""
    This script is designed to run a series of tests for transportation problems with piecewise linear cost function.
    It generates random data using 'createDataPWL.py', tests the data on all of 'PWLFunction.py' (Model with built-in piecewise linear function),
                                                                                'PWLLinear.py' (Model with linearised piecewise linear function) and
                                                                                'PWLSOS.py' (Model with SOS2 Variables) repeating the process multiple times.

    The script aims to assess and compare the performance of the different transportation models.
    After each iteration, a message is printed to indicate the completion of the current iteration.
    The results are then aggregated using 'aggregateDataPWL.py'.

    Usage:
    - Execute this script to perform multiple iterations of testing job shop scheduling models.
    - Ensure that the required model files ('createDataPWL.py', 'PWLFunction.py', 'PWLLinear.py', 'PWLSOS.py', 'aggregateDataPWL.py') are present in the same directory.

    Note: This script assumes the existence and proper functioning of the mentioned model files.
    """

#imports
import os

# Amount of times the models get tested
R = range(0,100)

# The models get R times tested.
for i in R:
    # Execute the code from 
    with open("createDataPWL.py") as f:
        exec(f.read())

    # Open the testData in read mode
        with open("testData.txt", 'r') as input_file:
            # Read the content
            content = input_file.read()

    # Execute the code from "PWLFunction.py"
    with open("PWLFunction.py") as f:
        exec(f.read())

    # Execute the code from "PWLLinear.py"
    with open("PWLLinear.py") as f:
        exec(f.read())

    # Execute the code from "PWLSOS.py"
    with open("PWLSOS.py") as f:
        exec(f.read())

    # Print a message indicating the completion of the iteration
    print("Iteration " + str(i + 1) + " is done.")

# Execute the code from "aggregateJobShop.py"
with open("aggregateDataPWL.py") as f:
        exec(f.read())

# Remove testData file generated during the last test
os.remove("testData.txt")