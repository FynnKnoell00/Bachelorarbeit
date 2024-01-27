"""
    Data Generation Script for the Transportation Models with piecewise linear cost functions
    """
#imports
import random
import math

"""
Generates random supply and demand lists.

Returns:
Two lists representing supply and demand.
"""
def generate_supply_demand():
    # Generate random supply values between 0 and 2000 for a random number of elements (between 10 and 13)
    supply = [random.randint(0, 2000) for _ in range(random.randint(10,13))]
    
    # Generate random demand values between 0 and the minimum of 2000 and the sum of supply for a random number of elements (between 10 and 13)
    demand = [random.randint(0, min(2000, sum(supply))) for _ in range(random.randint(10,13))]
    
    # Return the generated supply and demand lists
    return supply, demand

"""
Equalizes the sum of supply and demand by adjusting their values.

Parameters:
- supply (list): List representing supply values.
- demand (list): List representing demand values.

Returns:
Equalized supply and demand lists.
"""
def equalize_supply_demand(supply, demand):
    # Calculate the difference between the sum of supply and demand
    diff = sum(supply) - sum(demand)
    
    # While there is a difference, adjust the values to make the sums equal
    while diff != 0:
        if diff > 0:
            # If there's a surplus in supply, decrease values in supply list
            supply, diff = decrease_values(supply, diff)
        else:
            # If there's a surplus in demand, decrease values in demand list
            demand, diff = decrease_values(demand, -diff)
    
    # Return the equalized supply and demand lists
    return supply, demand

"""
Decreases values in a list by a specified amount.

Parameters:
- values (list): List of values to be decreased.
- amount (int): Amount to be decreased.

Returns:
List with decreased values and remaining amount to decrease.
"""
def decrease_values(values, amount):
    # Iterate through the values and decrease each by 1 until the specified amount is reached
    while(amount > 0):
        for i in range(len(values)):
            if values[i] > 0:
                values[i] = min(2000, values[i] - 1)
                amount -= 1
                if amount == 0:
                    break
    
    # Return the updated values list and remaining amount to decrease
    return values, amount

"""
Generates random breakpoints for a piecewise linear function.

Returns:
List of tuples representing breakpoints.
"""
def generate_breakpoints():
    # Initialize breakpoints list with the starting point (0, 0)
    breakpoints = [(0, 0)]
    
    # Generate 3 additional random breakpoints within specified ranges
    for _ in range(3):
        ulx = min(2000, breakpoints[-1][0] + 750)
        llx = breakpoints[-1][0] + 1
        x = random.randint(llx, ulx)

        uly = min(1000, breakpoints[-1][1] + 400)
        lly = breakpoints[-1][1] + 1
        y = random.randint(lly , uly)
        
        # Append the new breakpoint to the list
        breakpoints.append((x, y))
    
    # Add the final breakpoint (2000, 1000)
    breakpoints.append((2000, 1000))
    
    # Return the generated list of breakpoints
    return breakpoints

"""
Adjusts breakpoints of a piecewise linear function.

Parameters:
- breakpoints (list): List of tuples representing breakpoints.

Returns:
Adjusted list of tuples representing breakpoints.
"""
def adjust_breakpoints(breakpoints):
    # Iterate through the breakpoints and adjust them to ensure slopes are not decreasing
    for i in range(1, len(breakpoints) - 1):
        slope_prev = (breakpoints[i][1] - breakpoints[i-1][1]) / (breakpoints[i][0] - breakpoints[i-1][0])
        slope_next = (breakpoints[i+1][1] - breakpoints[i][1]) / (breakpoints[i+1][0] - breakpoints[i][0])

        # While the slope is not decreasing, increment the y-value of the current breakpoint
        while slope_prev <= slope_next:
            y_increment = random.uniform(0, min(1000 - breakpoints[i][1], 500))
            y_increment = math.ceil(y_increment)
            breakpoints[i] = (breakpoints[i][0], breakpoints[i][1] + y_increment)

            # Recalculate slopes for the updated breakpoints
            slope_prev = (breakpoints[i][1] - breakpoints[i-1][1]) / (breakpoints[i][0] - breakpoints[i-1][0])
            slope_next = (breakpoints[i+1][1] - breakpoints[i][1]) / (breakpoints[i+1][0] - breakpoints[i][0])

    # Return the adjusted list of breakpoints
    return breakpoints

"""
Writes supply, demand, and breakpoints to a text file.

Parameters:
- supply (list): List representing supply values.
- demand (list): List representing demand values.
- breakpoints (list): List of tuples representing breakpoints.

Returns:
None
"""
def write_to_file(supply, demand, breakpoints):
    # Open a text file for writing
    with open("testdata.txt", "w") as file:
        # Write supply and demand details to the file
        file.write("Supply: {}\n".format(supply))
        file.write("nbSupply: {}\n".format(len(supply)))
        file.write("Demand: {}\n".format(demand))
        file.write("nbDemand: {}\n".format(len(demand)))

        # Write breakpoints to the file
        file.write("\nGenerated Breakpoints:\n")
        for point in breakpoints:
            file.write("({}, {})\n".format(point[0], point[1]))

        # Write slopes to the file
        file.write("\nSlopes between Breakpoints:\n")
        for i in range(1, len(breakpoints)):
            slope = (breakpoints[i][1] - breakpoints[i-1][1]) / (breakpoints[i][0] - breakpoints[i-1][0])
            file.write("Between {} and {}: {}\n".format(breakpoints[i-1], breakpoints[i], slope))

"""
Generate initial supply, demand, and breakpoints

Returns:
- test (boolean) : value that represents if data is valid
- supply (list): List representing supply values.
- demand (list): List representing demand values.
- breakpoints (list): List of tuples representing breakpoints.
"""
def createData():
    # Generate initial supply, demand, and breakpoints
    supply, demand = generate_supply_demand()
    supply, demand = equalize_supply_demand(supply, demand)
    breakpoints = generate_breakpoints()
    breakpoints = adjust_breakpoints(breakpoints)

    # Calculate initial slopes between breakpoints
    slopes = [(breakpoints[i+1][1] - breakpoints[i][1]) / (breakpoints[i+1][0] - breakpoints[i][0]) for i in range(len(breakpoints) - 1)]

    return (slopes == sorted(slopes, reverse=True)), supply, demand, breakpoints


"""
Main function that orchestrates the entire process.

Returns:
None
"""
def main():
    # Generate initial supply, demand, and breakpoints
    test, supply, demand, breakpoints = createData()
    while (not test):
        test, supply, demand, breakpoints = createData()
    
    # Write generated data to a text file
    write_to_file(supply, demand, breakpoints)      


# Check if the script is being run directly
if __name__ == "__main__":
    # Execute the main function
    main()
