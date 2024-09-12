"""
Description:
The cellularautomata module implements a cellularautomata model for analyzing the distribution of population and other resources within a study area based on grid data.
"""

import random

# Get coordinates of neighbors in eight directions
def get_neighbors(row_now, col_now, data_list, direction_num=4):
    """
    Get neighboring valid coordinates given a row and column index in a 2D data list.

    Args:
        row_now (int): The current row index.
        col_now (int): The current column index.
        data_list (list): A 2D array representing the data converted from raster data.
        direction_num (int): The number of migration directions (default: 4). Only two values, 4 and 8, are allowed; if any other value is entered, it is recognized as the default 4 direction.

    Returns:
        list: A list of neighboring valid coordinates.
    """

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    if direction_num == 8:
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    
    neighbors = []
    for dr, dc in directions:
        new_row, new_col = row_now + dr, col_now + dc
        if 0 <= new_row < len(data_list) and 0 <= new_col < len(data_list[0]) and data_list[new_row][new_col] is not None:
            neighbors.append((new_row, new_col))
    return neighbors

# Migrate population function
def migrate_population_focus(data_list, population, direction_num=4, proportion=1):
    """
    The population is focused towards the most suitable nearby migration areas based on the raster pixel values.

    Args:
        data_list (list): A list converted from raster data that elements are raster pixel values.
        population (list): A list storing the initial population count of each pixel.
        direction_num (int): The number of migration directions (default: 4). Only two values, 4 and 8, are allowed; if any other value is entered, it is recognized as the default 4 direction.
        proportion (float): The proportion of population to migrate (default: 1). The proportion ranges from 0 to 1, with a proportion of 1 for complete migration and 0.5 for 50 percent migration.

    Returns:
        list: A 2D list representing the new population distribution after migration.
    """
    new_population = [[0 for _ in range(len(data_list[0]))] for _ in range(len(data_list))]
    
    for row in range(len(data_list)):
        for col in range(len(data_list[0])):
            if not data_list[row][col]:
                continue  # Skip invalid regions
            neighbors = get_neighbors(row, col, data_list, direction_num)
            if not neighbors:
                continue  # Skip if no valid neighbors
            
            max_value = max([data_list[r][c] for r, c in neighbors])
            highest_neighbors = [(r, c) for r, c in neighbors if data_list[r][c] == max_value]

            target_row, target_col = random.choice(highest_neighbors)
            
            if not population[row][col]:
                continue  # Skip invalid regions
            migrated_population = int(population[row][col] * proportion)
            
            new_population[target_row][target_col] += migrated_population
            new_population[row][col] += population[row][col] - migrated_population
    
    return new_population

# Migrate population function
def migrate_population_disperse(data_list, population, direction_num=4, proportion=[0.5, 0.25, 0.15, 0.05]):
    """
    The population is dispersed and migrates to the neighborhood based on the raster pixel values.

    Args:
        data_list (list): A list converted from raster data that elements are raster pixel values.
        population (list): A list storing the initial population count of each pixel.
        direction_num (int): The number of migration directions (default: 4). Only two values, 4 and 8, are allowed; if any other value is entered, it is recognized as the default 4 direction.
        proportion (list): A list of the proportion of the population that migrated to each neighboring pixel, ordered from highest to lowest suitability for migration. The proportion ranges from 0 to 1, with a proportion of 1 for complete migration and 0.5 for 50 percent migration.

    Returns:
        list: A 2D list representing the new population distribution after migration.
    """
    new_population = [[0 for _ in range(len(data_list[0]))] for _ in range(len(data_list))]
    
    for row in range(len(data_list)):
        for col in range(len(data_list[0])):
            if not data_list[row][col]:
                continue  # Skip invalid regions
            neighbors = get_neighbors(row, col, data_list, direction_num)
            if not neighbors:
                continue  # Skip if no valid neighbors
            
            # Sort neighbors based on the pixel value, in descending order
            sorted_neighbors = sorted(neighbors, key=lambda n: data_list[n[0]][n[1]], reverse=True)

            migrated_population = 0
            if not population[row][col]:
                continue  # Skip invalid regions
            
            # Distribute the population based on the given proportions
            for i in range(min(len(sorted_neighbors), len(proportion)-1)):
                target_row, target_col = sorted_neighbors[i]
                distributed_value = population[row][col] * proportion[i]
                new_population[target_row][target_col] += int(distributed_value)
                # new_population[target_row][target_col] += int(population[row][col] * proportion[i])
                migrated_population += new_population[target_row][target_col]
            
            # Remaining population stays
            if migrated_population < population[row][col]:
                new_population[row][col] += population[row][col] - migrated_population
    
    return new_population

def run_iterations_num(iterations, data_list, population_num=10, direction_num=4, type_migration="focus", migration_proportion=1):
    """
    Running a cellular automata using a uniform initial population count to simulate population migration based on a raster of environmental data.

    Args:
        iterations (int): The number of iterations to run the simulation.
        data_list (list): A 2D array converted from a raster of environmental data.
        population_num (int): The initial population count at each pixel (default: 10).
        direction_num (int): The number of migration directions (default: 4). Only two values, 4 and 8, are allowed; if any other value is entered, it is recognized as the default 4 direction.
        type_migration (str): The type of migration to use, either "focus" or "disperse" (default: "focus").
        migration_proportion (float or list): The proportion of population to migrate (default: 1). The proportion ranges from 0 to 1, with a proportion of 1 for complete migration and 0.5 for 50 percent migration.

    Returns:
        list: A 2D list representing the population distribution after running the simulation.
    """
    population = [[population_num for _ in range(len(data_list[0]))] for _ in range(len(data_list))]

    for i in range(iterations):
        if type_migration == "focus":
            population = migrate_population_focus(data_list, population, direction_num, migration_proportion)
        elif type_migration == "disperse":
            population = migrate_population_disperse(data_list, population, direction_num, migration_proportion)
        print(f"Iteration {i + 1} is complete.")

    return population

def run_iterations_pop(iterations, data_list, population_list, direction_num=4, type_migration="focus", migration_proportion=1):
    """
    Running a cellular automata using an initial population size raster to simulate population migration based on a raster of environmental data.

    Args:
        iterations (int): The number of iterations to run the simulation.
        data_list (list): A 2D array converted from a raster of environmental data.
        population_list (list): A 2D array converted from an initial population size raster.
        direction_num (int): The number of migration directions (default: 4). Only two values, 4 and 8, are allowed; if any other value is entered, it is recognized as the default 4 direction.
        type_migration (str): The type of migration to use, either "focus" or "disperse" (default: "focus").
        migration_proportion (float or list): The proportion of population to migrate (default: 1). The proportion ranges from 0 to 1, with a proportion of 1 for complete migration and 0.5 for 50 percent migration.

    Returns:
        list: A 2D list representing the population distribution after running the simulation.
    """

    for i in range(iterations):
        if type_migration == "focus":
            population_list = migrate_population_focus(data_list, population_list, direction_num, migration_proportion)
        elif type_migration == "disperse":
            population_list = migrate_population_disperse(data_list, population_list, direction_num, migration_proportion)
        print(f"Iteration {i + 1} is complete.")

    return population_list
