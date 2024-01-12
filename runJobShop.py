import os

# amount of times the models get tested
R = range(0,5)

for i in R:
    with open("createDataJobShop.py") as f:
        exec(f.read())

    with open("JobShopMIP.py") as f:
        exec(f.read())

    with open("JobShopDisjunction.py") as f:
        exec(f.read())

    print("Iteration " + str(i) + " is done.")

with open("aggregateJobShop.py") as f:
        exec(f.read())

os.remove("solution_MIP.txt")
os.remove("solution_DIS.txt")
os.remove("testData.txt")