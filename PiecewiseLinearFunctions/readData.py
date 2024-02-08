"""
    Parse test data from a file.

    Parameters:
    - filename (str): The path to the file containing test data.

    Returns:
    A tuple containing:
    - supply (list): List of supply values.
    - nbSupply (int): Number of supplies.
    - demand (list): List of demand values.
    - nbDemand (int): Number of demands.
    - breakpoints (list): List of breakpoint coordinates.
    - slopes (list): List of slopes between breakpoints.
    """
def parse_data(filename):
    
    supply = []
    nbSupply = 0
    demand = []
    nbDemand = 0
    breakpoints = []
    slopes = []

    with open(filename, "r") as file:
        lines = file.readlines()

        # Parse Supply
        supply_line = lines[0].split("[")[1].split("]")[0].split(", ")
        supply = list(map(int, supply_line))

        # Parse nbSupply
        nbSupply = int(lines[1].split(": ")[1])

        # Parse Demand
        demand_line = lines[2].split("[")[1].split("]")[0].split(", ")
        demand = list(map(int, demand_line))

        # Parse nbDemand
        nbDemand = int(lines[3].split(": ")[1])
        
        # Parse Breakpoints
        breakpoints_index = lines.index("Generated Breakpoints:\n") + 1
        while "Slopes between Breakpoints:" not in lines[breakpoints_index]:
            values = lines[breakpoints_index].strip('()\n').split(', ')
            
            if len(values) == 2:
                x, y = map(int, values)
                breakpoints.append((x, y))
            
            breakpoints_index += 1

        # Parse Slopes
        slopes_index = lines.index("Slopes between Breakpoints:\n") + 1
        while slopes_index < len(lines) and lines[slopes_index] != "\n":
            slope_info = lines[slopes_index].split(": ")[1].strip()
            slope = float(slope_info)
            slopes.append(slope)
            slopes_index += 1

    return supply, nbSupply, demand, nbDemand, breakpoints, slopes