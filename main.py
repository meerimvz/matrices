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

