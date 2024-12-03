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

def validate_input(user_input):
    if len(user_input) != 2:
        return None
    row, col = user_input[0].upper(), user_input[1]
    if row < 'A' or row > 'G' or not col.isdigit() or not (0 <= int(col) <= 6):
        return None
    return ord(row) - 65, int(col)

def is_sunk(board, ship):
    return all(board[r][c] == 'H' for r, c in ship)

def mark_sunk(board, ship):
    for r, c in ship:
        board[r][c] = 'S'

def check_victory(ships, board):
    return all(all(board[r][c] == 'S' for r, c in ship) for ship in ships)

def play_game():
    player_name = input("Enter your name: ")
    clear_screen()
    player_board = create_empty_board()
    ships = field_generation()
    shots = 0

    while not check_victory(ships, player_board):
        clear_screen()
        print(f"{name}'s Game Board:")
        display_board(player_board)

        user_input = input("Enter your shot (e.g., A3): ")
        coords = validate_input(user_input)
        if not coords:
            print("Invalid input. Try again.")
            continue

        row, col = coords
        if player_board[row][col] != '*':
            print("You already shot there. Try again.")
            continue

        shots += 1
        hit = False
        for ship in ships:
            if (row, col) in ship:
                player_board[row][col] = 'H'
                if is_sunk(player_board, ship):
                    mark_sunk(player_board, ship)
                hit = True
                break 
        if not hit:
            player_board[row][col] = 'M'

        if check_victory(ships, player_board):
            clear_screen()
            print(f"Congratulations {name}! You won in {shots} shots!")
            break

     replay = input("Do you want to play again? (yes/no): ").strip().lower()
    if replay == 'yes':
        play_game()
    else:
        print("Thanks for playing!")

if __name__ == "__main__":
    play_game()

            




