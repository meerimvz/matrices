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

        return booard, ships

def make_shot(board, ships, x, y):
    if board[x][y] != " " and board[x][y] != HIT and board[x][y] != MISS:
        board[x][y] = HIT
        for ship in ships:
            if ship[0] == (x, y):  
                ship[2] -= 1  
                if ship[2] == 0:  
                    mark_sunk(board, ship)
        return HIT
    else:
        board[x][y] = MISS
        return MISS

def mark_sunk(board, ship):
    for i in range(ship[2]):
        x, y = ship[0]
        if ship[1] == "horizontal":
            board[x][y + i] = SUNK
        elif ship[1] == "vertical":
            board[x + i][y] = SUNK

def play_game():
    player_name = input("Enter your name: ")
    board, ships = place_ships()
    shots_taken = 0
    
while True:
        display_board(board)
        print(f"Ships left: {sum(s[2] for s in ships)}")
        
        coordinates = input("Enter coordinates (x y): ").split()
        if len(coordinates) != 2:
            print("Invalid input. Please enter two numbers separated by space.")
            continue
        
        x, y = coordinates
        if not x.isdigit() or not y.isdigit():
            print("Invalid input. Coordinates must be numbers.")
            continue
        
        x, y = int(x), int(y)
        if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
            result = make_shot(board, ships, x, y)
            print(f"You {result}!")
            shots_taken += 1
        else:
            print("Invalid coordinates. Try again.")
            continue
        
        if all(ship[2] == 0 for ship in ships):
            print(f"Congratulations {player_name}, you won!")
            print(f"It took you {shots_taken} shots.")
            return shots_taken
        else:
            input("Press Enter to continue.")

def main():
    players_scores = []
    while True:
        shots_taken = play_game()
        players_scores.append(shots_taken)
        
        play_again = input("Do you want to play again? (y/n): ").lower()
        if play_again != "y":
            break
    
    players_scores.sort()
    print("\nPlayer Scores:")
    for i, score in enumerate(players_scores, 1):
        print(f"Rank {i}: {score} shots")



