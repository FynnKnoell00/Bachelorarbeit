"""
    This script is designed to run a series of tests for uncapacitated facility location models.
    It generates random data using 'createDataImplic.py', tests the data on all of
    'FLConditional.py' (Conditional Constraint), 'FLIndicator.py' (Indicator Constraint) and 'FLLinear.py' (Indicator Constraint), repeating the process multiple times.

    The script aims to assess and compare the performance of different uncapacitated facility location models.
    After each iteration, a message is printed to indicate the completion of the current iteration.
    The results are then aggregated using 'aggregateDataFL.py'.

    Usage:
    - Execute this script to perform multiple iterations of testing uncapacitated facility location models.
    - Ensure that the required model files ('createDataImplic.py', 'FLConditional.py', 'FLIndicator.py', 'FLLinear.py', 'aggregateDataFL.py') are present in the same directory.

    Note: This script assumes the existence and proper functioning of the mentioned model files.
    """

#imports
import os

# Amount of times the models get tested
R = range(0,100)

# The models get R times tested.
for i in R:
    # Execute the code from "createDataimplic.py"
    with open("createDataimplic.py") as f:
        exec(f.read())

    # Open the testData in read mode
        with open("testData.txt", 'r') as input_file:
            # Read the content
            content = input_file.read()

        # Open the save file in write mode
        with open(f"testData_{i}.txt", 'w') as output_file:
            # Write the content
            output_file.write(content)

    # Execute the code from "FLConditional.py"
    with open("FLConditional.py") as f:
        exec(f.read())

    # Execute the code from "FLIndicator.py"
    with open("FLIndicator.py") as f:
        exec(f.read())

    # Execute the code from "FLLinear.py"
    with open("FLLinear.py") as f:
        exec(f.read())

    # Print a message indicating the completion of the iteration
    print("Iteration " + str(i + 1) + " is done.")

# Execute the code from "aggregateDataFL.py"
with open("aggregateDataFL.py") as f:
        exec(f.read())

# Remove testData file generated during the last test
os.remove("testData.txt")