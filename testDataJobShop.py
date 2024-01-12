import random

# ----------------------------------------------------------------------------
# Initialize the problem data
# ----------------------------------------------------------------------------

# amount of Jobs in Job Shop Scheduling Problem
amountJobs = random.randint(8,8)
# amount of Machines in Job Shop Scheduling Problem
amountMachines = random.randint(8,8)

# function that generates a machein sequence for a job
def generate_machineSequence(amountMachines):
    machineSequence = []
    for i in range(0,amountMachines):
        machineSequence.append(i) 

    random.shuffle(machineSequence)

    return machineSequence

# array that stores all jobs and their machine sequences
mS = []
for i in range(0,amountJobs):
    mS.append(generate_machineSequence(amountMachines))

strmS = str(mS)[0:len(str(mS)) - 2].replace('[', '').replace(' ', '')


# array that stores the processing time of all jobs
procTime = ''
for char in strmS:
    if(char.isdigit()):
        procTime += str(random.randint(1,9))
    else:
        procTime += char

with open("testData.txt", "w") as solfile:
    solfile.write(str(amountJobs) + "\n")
    solfile.write(str(amountMachines) + "\n")
    solfile.write(str(procTime) + "\n")
    solfile.write(strmS + "\n")


