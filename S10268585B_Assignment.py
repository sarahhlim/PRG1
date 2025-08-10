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
            #1=visible, 0=not visible 
            lines.append(''.join('1' if v else '0' for v in row))
        #open the file and writes 
        with open(filename, 'w') as f:
            f.write('\n'.join(lines))
        print('Game saved.')
    except Exception as e:
        print('Failed to save game:', e)

def load_game(grid, filename=SAVE_FILENAME):
    try:
        #open the saved file
        with open(filename, 'r') as f:
            lines = [ln.rstrip('\n') for ln in f.readlines()]
    except Exception as e:
        print('No save file found.')
        return None, None
    try:
        #read player data
        count = 0
        name = lines[count]; count += 1
        pos = list(map(int, lines[count].split(','))); count += 1
        portal = list(map(int, lines[count].split(','))); count += 1
        pickaxe = int(lines[count]); count += 1
        capacity = int(lines[count]); count += 1
        copper = int(lines[count]); count += 1
        silver = int(lines[count]); count += 1
        gold = int(lines[count]); count += 1
        gp = int(lines[count]); count += 1
        steps = int(lines[count]); count += 1
        day = int(lines[count]); count += 1
        turns_left = int(lines[count]); count += 1

        # remaining lines are fog
        fog_lines = lines[count:]
        fog = []
        for r in fog_lines:
            fog.append([c == '1' for c in r])

        
        # checks if the loaded fog grid size matches the size of the current game map (grid).
        if len(fog) != len(grid) or any(len(fog[r]) != len(grid[0]) for r in range(len(grid))):
            fog = [[False] * len(grid[0]) for _ in range(len(grid))]
            # reveal town and portal and player position

            #It bundles all loaded player info into a dictionary to use in the game.
        player = {
            'name': name,
            'pos': pos,
            'portal': portal,
            'pickaxe': pickaxe,
            'capacity': capacity,
            'copper': copper,
            'silver': silver,
            'gold': gold,
            'gp': gp,
            'steps': steps,
            'day': day,
            'turns_left': turns_left,
        }
        print('Game loaded.')
        return player, fog
    except Exception as e:
        print('Failed to load save:', e)
        return None, None

# ----------------------------
# Shop
# ----------------------------

def shop_menu(player):
    while True:
        print('\n----------------------- Shop Menu -------------------------')
        if player['pickaxe'] < 2:
            print('(P)ickaxe upgrade to Level 2 to mine silver ore for 50 GP')
        elif player['pickaxe'] < 3:
            print('(P)ickaxe upgrade to Level 3 to mine gold ore for 150 GP')
            #calculates the price of the new backpack
        cap_upgrade_price = player['capacity'] * 2
        #prints the backpack update option
        print('(B)ackpack upgrade to carry {} items for {} GP'.format(player['capacity'] + 2, cap_upgrade_price))
        print('(L)eave shop')
        print('-----------------------------------------------------------')
        print('GP: {}'.format(player['gp']))
        choice = input('Your choice? ').strip().upper()
        if choice == 'P':
            if player['pickaxe'] == 1:
                price = 50
                #check whether it has enough money
                if player['gp'] >= price:
                    #minus the money
                    player['gp'] -= price
                    player['pickaxe'] = 2
                    print('Pickaxe upgraded to Level 2! You can now mine silver.')
                else:
                    print('Not enough GP.')
            elif player['pickaxe'] == 2:
                price = 150
                if player['gp'] >= price:
                    player['gp'] -= price
                    player['pickaxe'] = 3
                    print('Pickaxe upgraded to Level 3! You can now mine gold.')
                else:
                    print('Not enough GP.')
            else:
                #no more pickaxe to buy
                print('You already have the best pickaxe.')