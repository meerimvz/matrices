import os
import random

BOARD_SIZE = 7
SHIP_TYPES = {3: 1, 2: 2, 1: 4}  
HIT = "H"
MISS = "M"
SUNK = "S"

def create_board():
    return [[" " for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("  0 1 2 3 4 5 6")
    for i, row in enumerate(board):
        print(f"{i} {' '.join(row)}")
    print()
def place_ships():
    board = create_board()
    ships = []

    for ship_size, count in SHIP_TYPES.items():
        for _ in range(count):
            placed = False
            while not placed:
                x, y = random.randint(0, BOARD_SIZE-1), random.randint(0, BOARD_SIZE-1)
                orientation = random.choice(["horizontal", "vertical"])

                if orientation == "horizontal" and y + ship_size <= BOARD_SIZE:
                    if all(board[x][y + i] == " " for i in range(ship_size)):
                        for i in range(ship_size):
                            board[x][y + i] = str(ship_size)
                        ships.append(((x, y), orientation, ship_size))
                        placed = True
                elif orientation == "vertical" and x + ship_size <= BOARD_SIZE:
                    if all(board[x + i][y] == " " for i in range(ship_size)):
                        for i in range(ship_size):
                            board[x + i][y] = str(ship_size)
                        ships.append(((x, y), orientation, ship_size))
                        placed = True


