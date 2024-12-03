import os
import random

ships = []
freezone = set()

def create_freezone():
    global freezone
    freezone = set()
    for i in range(7):
        for j in range(7):
            freezone.add((i,j))

def random_direction():
    return random.randint(0, 1)

def del_from_freezone(coordinates):
    for coordinate in coordinates:
        freezone.discard(coordinate)
        x, y = coordinate[0], coordinate[1]
        freezone.discard((x + 1, y))
        freezone.discard((x - 1, y))
        freezone.discard((x, y + 1))
        freezone.discard((x, y - 1))
        freezone.discard((x + 1, y + 1))
        freezone.discard((x - 1, y - 1))
        freezone.discard((x + 1, y - 1))
        freezone.discard((x - 1, y + 1))

def big_ship():
    global freezone
    global ships
    if random_direction() == 1:
        first_cell = (random.randint(0,6), random.randint(0,4))
        second_cell = (first_cell[0], first_cell[1] + 1)
        third_cell = (first_cell[0], first_cell[1] + 2)
    else:
        first_cell = (random.randint(0,4), random.randint(0,6))
        second_cell = (first_cell[1] + 1, first_cell[0])
        third_cell = (first_cell[1] + 2, first_cell[0])
    ships.append([first_cell, second_cell, third_cell])
    del_from_freezone([first_cell, second_cell, third_cell])

def medium_ship():
    global ships
    global freezone
    if random_direction() == 1:
        first_cell = random.choice(list(freezone))
        if 0 <= first_cell[0] <= 6 and 0 <= first_cell[1] <= 5:
            second_cell = (first_cell[0], first_cell[1] + 1)
            if second_cell in freezone:
                ships.append([first_cell, second_cell])
                del_from_freezone([first_cell, second_cell])
            else:
                medium_ship()
    else:
        first_cell = random.choice(list(freezone))
        if 0 <= first_cell[0] <= 5 and 0 <= first_cell[1] <= 6:
            second_cell = (first_cell[0] + 1, first_cell[1])
            if second_cell in freezone:
                ships.append([first_cell, second_cell])
                del_from_freezone([first_cell, second_cell])
            else:
                medium_ship()

def one_ship():
    global ships
    global freezone
    first_cell = random.choice(list(freezone))
    ships.append([first_cell])
    del_from_freezone([first_cell])

def last_one_ship():
    global ships
    global freezone
    if len(freezone) == 0:
        ships = []
        create_freezone()
        big_ship()
        medium_ship()
        medium_ship()
        one_ship()
        one_ship()
        one_ship()
        last_one_ship()
    else:
        first_cell = random.choice(list(freezone))
        ships.append([first_cell])
        del_from_freezone([first_cell])

def field_generation():
    global ships
    create_freezone()
    big_ship()
    medium_ship()
    medium_ship()
    one_ship()
    one_ship()
    one_ship()
    last_one_ship()
    return ships

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_empty_board():
    return [['*' for _ in range(7)] for _ in range(7)]

def display_board(board):
    print("    0   1   2   3   4   5   6")
    for i, row in enumerate(board):
        print(f"{chr(65 + i)}  {'   '.join(row)}")

    
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



