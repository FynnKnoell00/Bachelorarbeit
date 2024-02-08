import re

"""
    Read problem data from a file and parse the necessary information.

    Parameters:
    - filename (str): The path to the file containing problem data.

    Returns:
    A tuple containing:
    - nbFacilities (int): The number of facilities in the problem.
    - nbCustomers (int): The number of customers in the problem.
    - fix_costs (list): A list representing the fix-cost for each facility.
    - max_production (list): A list representing the maximum amount of production for each facility.
    - demand (list): A list representing the demand for each customer.
    - transport_costs (list): A 2D list representing the transport costs between a facility and a customer.
    """
def parse_data(filename):
    with open(filename, 'r') as file:
        # Read all lines from the file
        lines = file.readlines()

        # Parse the values for jobs and machines (the first line)
        values_line = lines[0].strip().split('\t')
        nbFacilities =  int(re.search(r'\d+', values_line[0]).group())
        nbCustomers = int(re.search(r'\d+', values_line[1]).group())

        # Parse Fix costs for the facilities
        fix_costs_line = lines[3].split("[")[1].split("]")[0].split(", ")
        fix_costs = list(map(int, fix_costs_line))

        # Parse Maximum production for the facilities
        max_production_line = lines[5].split("[")[1].split("]")[0].split(", ")
        max_production = list(map(int, max_production_line))

        # Parse Demand of the customers
        demand_line = lines[7].split("[")[1].split("]")[0].split(", ")
        demand = list(map(int, demand_line))

        # Parse Matrix with transport costs
        transport_costs = []
        for line in lines[10:]:
            row = list(map(int, line.strip().split('\t')))
            transport_costs.append(row)

    return nbFacilities, nbCustomers, fix_costs, max_production, demand, transport_costs