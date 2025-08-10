#s10268585b sarah lim

import random

SAVE_FILENAME = 'savegame.txt'
MAP_FILENAME = 'level1.txt'

def read_map(filename):
    #open and read from the file
    try:
        with open(filename, 'r') as f:
            lines = [line.rstrip('\n') for line in f.readlines() if line.strip('') is not None]
    except Exception:
        # backup!!! if my txt isnt working :(
        lines = [
            "T CCCCC SS GGG",
            " CCCCC SSSS",
            "GGG",
            " CCCC SSSS GGG",
            " SSSSS CCC",
            " CC S CCCC",
            "CCCCCCCCC CCCCC",
            "CCCCCCCC G CCCC",
            " CCCCC GG SS",
            " CCCCC GGG",
            "SSSSSS",
            " CCC GGG",
            "SSSGGG",
        ]
    # maxw → Finds the length of the longest row.
    #Loops over every row and if it’s shorter than maxw, adds spaces at the end so all rows have equal length.
    #This ensures the map have a perfect rectangle grid 
    grid = [list(line) for line in lines]
    maxw = max(len(r) for r in grid)
    for r in grid:
        if len(r) < maxw:
            r.extend([' '] * (maxw - len(r)))
    return grid

def find_tile(grid, tile): 
    #basically finds a certain character and gives me coords
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch == tile:
                return (x, y)
    return None

def in_bounds(grid, x, y):
    #Checks if the coordinates (x, y) are within the valid boundaries of the grid.
    return 0 <= y < len(grid) and 0 <= x < len(grid[0])

def tile_at(grid, x, y):
    #Returns the tile (character) at position (x, y) in the grid if it’s within bounds.
    if in_bounds(grid, x, y):
        return grid[y][x]
    #if invaild, doesnt return anything
    return None

# ----------------------------
# Game state and defaults
# ----------------------------

def new_player(name, town_pos):
    #This function sets up the initial state of the player when starting a new game(basically default setting)
    return {
        'name': name,
        'pos': town_pos[:],  # [x,y]
        'portal': town_pos[:],
        'pickaxe': 1,  # 1=copper,2=silver,3=gold
        'capacity': 10,
        'copper': 0,
        'silver': 0,
        'gold': 0,
        'gp': 0,
        'steps': 0,
        'day': 1,
        'turns_left': 20,
    }

# ----------------------------
# Save / Load
# ----------------------------

def save_game(player, fog, filename=SAVE_FILENAME):
    #saves the current game into a file
    try:
        lines = []
        # basic player info stored
        lines.append(player['name'])
        lines.append(','.join(map(str, player['pos'])))
        lines.append(','.join(map(str, player['portal'])))
        lines.append(str(player['pickaxe']))
        lines.append(str(player['capacity']))
        lines.append(str(player['copper']))
        lines.append(str(player['silver']))
        lines.append(str(player['gold']))
        lines.append(str(player['gp']))
        lines.append(str(player['steps']))
        lines.append(str(player['day']))
        lines.append(str(player['turns_left']))

        # save fog based on whether it is visible or not
        for row in fog: