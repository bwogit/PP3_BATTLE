import random
import gspread
from google.oauth2.service_account import Credentials
from colorama import Fore


def authenticate():
    """
    authentication function.
    """

    # Set up Google Sheets credentials.
    SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
        ]
    CREDS = Credentials.from_service_account_file('creds.json')
    SCOPED_CREDS = CREDS.with_scopes(SCOPE)
    GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
    SHEET = GSPREAD_CLIENT.open('Battleship')

    # Get the auth_dict worksheet

    auth_dict_worksheet = SHEET.worksheet('auth_dict')
    return auth_dict_worksheet


def login(username, password):
    """
    Authenticate with Google Sheets and get the auth_dict worksheet. 
    Input Validation. 
    """
    if not username.strip() or not password.strip():
        print('Invalid username or password! Cannot be empty')
        return False
    if len(username.strip()) < 5:
        print('Invalid username! Must be at least 5 characters long')
        return False
    if len(password.strip()) < 5:
        print('Invalid password! Must be at least 5 characters long')
        return False

    auth_dict_worksheet = authenticate()
    # Get all the rows in the worksheet as a list of dictionaries
    rows = auth_dict_worksheet.get_all_records()
    # Check if there's a row with the given username and password
    for row in rows:
        if row['username'] == username and row['password'] == password:
            # Return True if the username and password match
            return True
    # Return False if the username and password don't match
    return False


class Board:
    """
    Main board class.
    """

    def __init__(self, size, player_name, board_type):
        """
        initializing the grid with '.' characters for each tile
        """
        self.size = size
        self.grid = [['.' for _ in range(size)] for _ in range(size)]
        self.ships = []
        self.computer_ships = []
        self.player_name = player_name
        self.board_type = board_type

    def __str__(self):
        """
        returns a string representation of the board,
        which is printed when the board needs to be displayed
        """
        s = f'{self.player_name} {self.board_type}\n'
        s += '   ' + ' '.join(str(i) for i in range(self.size)) + '\n'
        for i in range(self.size):
            s += f'{i} |{"|".join(self.grid[i])}|\n'
        return s

    def mark_ship(self, x, y):
        """
        adds a ship at on the board by
        setting the corresponding tile on the grid to 'O'
        """
        self.ships.append((x, y))
        self.grid[x][y] = 'O'

    def place_computer_ships(self):
        """
        Randomly places ships on the computer's grid.
        """
        for i in range(3):
            while True:
                x = random.randint(0, self.size - 1)
                y = random.randint(0, self.size - 1)
                if self.is_valid(x, y):
                    self.computer_ships.append((x, y))
                    self.grid[x][y] = 'O'
                    break

    def has_ship(self, x, y):
        """
        returns true if has a ship on it
        """
        return (x, y) in self.ships

    def is_valid(self, x, y):
        """
        returns true if location is witihn bounds
        """
        return 0 <= x < self.size and 0 <= y \
            < self.size and self.grid[x][y] == '.'

    def fire(self, x, y):
        """
        returns True if there is a ship at that location, otherwise False.
        if ship present at location displays 'X'.
        Otherwise, it sets the tile to '-'.
        """
        if (x, y) in self.ships:
            self.ships.remove((x, y))
            if self.board_type == "Computer":
                self.grid[x][y] = Fore.RED + 'X' + Fore.RESET
            else:
                self.grid[x][y] = Fore.YELLOW + 'X' + Fore.RESET
            return True
        else:
            self.grid[x][y] = Fore.YELLOW + '-' + Fore.RESET
            return False
        if self.grid[x][y] == Fore.YELLOW + '-' + Fore.RESET:
            print("That coordinate is already taken.")
            return False

    def get_grid_coords(self, x, y):
        """
        Convert coordinates from shot_grid to grid
        """
        return y, x


def get_valid_coordinate(prompt, board):
    """
    function takes a prompt and a board and repeatedly \
    prompts the user to enter valid coordinates\
    until valid coordinates are entered.\
    It returns the coordinates as a tuple.
    """
    while True:
        try:
            x, y = input(prompt).split(',')
            x, y = int(x), int(y)
            if x < 0 or x >= board.size or y < 0 or y >= board.size:
                print(f"Invalid coordinates. Please enter 2 integers "
                      f"between 0 and {board.size - 1}.")
            elif not board.is_valid(x, y):
                print("That coordinate is already taken."
                      " Please enter a different coordinate.")
                return x, y
            else:
                return x, y
        except ValueError:
            print(f"Invalid coordinates. Please enter 2 integers "
                  f"between 0 and {board.size - 1} separated by a comma")


def play_game():
    """
    Main function. Setys up and plays. Initialises player and board\
    Adds ships to the board gane and enters a loop where comuter\
    and player take turns unil no more ships
    """
    size = 5

    # Menu with 2 options: Sign In and Sign Up
    print("Welcome to Battleship!")
    print('')
    print(Fore.RED + "        ___|")
    print(Fore.RED + "    _____|_____")
    print(Fore.RED + " ~~~~[_________]")
    print(Fore.RED + "      \\~~~~~~~/")
    print(Fore.RED + "        \\~~~/")
    print(Fore.RED + "         \\_/\n" + Fore.RESET)
    print('')
    print("Please select an option:")
    print("1. Sign In")
    print("2. Sign Up")

    # Prompt user to select an option and handle user input
    while True:
        choice = input("Enter the corresponding number to select an option: ")
        if choice == "1":
            # Ask for username and password
            username = input('Please enter your username: \n ')
            password = input('Please enter your password: \n')
            # Authenticate user
            if login(username, password):
                print('Login successful! Starting the game...')
                player_name = username
                break
            print('Invalid credentials. Try again later.')
        elif choice == "2":
            username = input('Enter a new username (at least 5 char) \n ')
            if not username:
                print('Username cannot be empty!')
                continue
            if len(username) < 5:
                print('Invalid username! must be at least 5 characters.')
                continue
            password = input('Enter new password (at least 5 char): \n')
            # Check password length
            if len(password) < 5:
                print('Invalid password! must be at least 5 characters.')
                continue
            # Authenticate user
            auth_dict_worksheet = authenticate()
            rows = auth_dict_worksheet.get_all_records()
            for row in rows:
                if row['username'] == username:
                    print('Username already taken.Choose a different username')
                    break
            else:
                auth_dict_worksheet.append_row([username, password])
                print('Account created successfully! Starting the game...')
                player_name = username
                break
        else:
            print('Invalid choice. Please enter 1 or 2.')
        # Prompt user to select the board size and handle user input

    while True:
        size_choice = input("Select a board size (enter 1 for 5x5, 2 for 6x6, "
                            "or 3 for 7x7): ")
        if size_choice == '1':
            size = 5
            break
        elif size_choice == '2':
            size = 6
            break
        elif size_choice == '3':
            size = 7
            break
        else:
            print("Invalid input. Please enter 1, 2, or 3.")

    player_board = Board(size, player_name, 'player board')
    computer_board = Board(size, 'Computer', 'computer board')

    # add player's ships
    for i in range(5):
        while True:
            x, y = random.randint(0, size-1), random.randint(0, size-1)
            if player_board.is_valid(x, y):
                break
        player_board.mark_ship(x, y)

    # add computer's ships
    for i in range(5):
        while True:
            x, y = random.randint(0, size-1), random.randint(0, size-1)
            if computer_board.is_valid(x, y):
                break
        computer_board.mark_ship(x, y)
        computer_board.computer_ships.append((x, y))

    # Place ships on computer's board
    print("Placing ships on computer's board...")
    computer_board.place_computer_ships()

    player_turn = True
    while player_board.ships and computer_board.ships:
        if player_turn:
            print(player_board)
            x, y = get_valid_coordinate(f'{player_name},your shot (row,col):',
                                        computer_board)
            hit = computer_board.fire(x, y)
            if hit:
                print("You hit a ship!")
            else:
                print("You missed.")
        else:
            x, y = random.randint(0, size-1), random.randint(0, size-1)
            hit = player_board.fire(x, y)
            if hit:
                print(f"Your ship was hit at ({x},{y}).")
            else:
                print(f"The computer missed at ({x},{y}).")

        player_turn = not player_turn

    if not computer_board.ships:
        print("Congratulations! You won!")
    else:
        print("Sorry, you lost. Better luck next time!")
    print("Game over.")


authenticate()
play_game()
