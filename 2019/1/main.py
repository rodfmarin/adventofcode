import csv



def calculate_fuel(mass):
    """
    Returns a fuel unit value depending on mass
    The algorithm is to take the mass, divide by 3, round down, and subtract 2
    :param mass:
    :return: fuel
    """
    return mass // 3 - 2

def calculate_fuel_recursively(mass):
    """
    Recursively calculates fuel needed
    :param mass:
    :return: fuel
    """
    if mass <= 0:
        return 0
    else:
        fuel = mass
        return fuel + calculate_fuel_recursively(((mass // 3) - 2))