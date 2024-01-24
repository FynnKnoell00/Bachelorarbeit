#imports
import os

# Amount of times the models get tested
R = range(0,5)

# The models get R times tested.
for i in R:
    # Execute the code from 
    with open("createDataPWL.py") as f:
        exec(f.read())

    # Open the testData in read mode
        with open("testData.txt", 'r') as input_file:
            # Read the content
            content = input_file.read()

        # Open the save file in write mode
        with open(f"testData_{i}.txt", 'w') as output_file:
            # Write the content
            output_file.write(content)

    # Execute the code from 
    with open("PWLFunction.py") as f:
        exec(f.read())

    # Execute the code from 
    with open("PWLLinear.py") as f:
        exec(f.read())

    # Execute the code from 
    with open("PWLSOS.py") as f:
        exec(f.read())

    # Print a message indicating the completion of the iteration
    print("Iteration " + str(i + 1) + " is done.")

# Execute the code from "aggregateJobShop.py"
with open("aggregateDataWPL.py") as f:
        exec(f.read())

# Remove testData file generated during the last test
os.remove("testData.txt")