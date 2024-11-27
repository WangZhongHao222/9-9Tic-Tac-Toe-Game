import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Initialize the main window
root = tk.Tk()
root.title("Tic-Tac-Toe")

# Create an empty buttons_state
buttons_state = [[' ' for _ in range(9)] for _ in range(9)]
sub_board_state = [' ' for _ in range(9)]
current_player = 'Red'  # 'Red' represents player 1, 'Blue' represents player 2
player_color = {'Red': '#FFC0C0', 'Blue': '#C0D6FF', 'Tie': '#DFCBEF'}
last_place = None

# Define alternating colors for the board (like a chessboard pattern)
light_color = '#FFFACD'
colors = ['#F0E68C', '#F7E7A9']
move_log = []  # List to store the move log
game_log = []  # List to store the game log


# Function to update the current player's label
def update_current_player():
    player_label2.config(text=f"{current_player}")
    player_button.config(bg=player_color[current_player], state='disabled')


# Function to update the possible moves on the small board
def update_possible_moves():
    if last_place is None or sub_board_state[last_place] != ' ':
        for i, small_button in enumerate(small_board):
            if sub_board_state[i] == ' ':
                small_button.config(bg=light_color, state='disabled')
            else:
                small_button.config(bg=player_color[sub_board_state[i]], state='disabled')
    else:
        for i, small_button in enumerate(small_board):
            if i == last_place:
                small_button.config(bg=light_color, state='disabled')
            elif sub_board_state[i] == ' ':
                small_button.config(bg=colors[i % 2], state='disabled')
            else:
                small_button.config(bg=player_color[sub_board_state[i]], state='disabled')


# Function to reset the game board
def reset_board():
    global buttons_state, sub_board_state, current_player, last_place, move_log, game_log
    buttons_state = [[' ' for _ in range(9)] for _ in range(9)]
    sub_board_state = [' ' for _ in range(9)]
    current_player = 'Red'
    last_place = None
    move_log = []  # List to store the move log
    game_log = []  # List to store the game log
    update_possible_moves()
    update_current_player()
    for i, sub_board in enumerate(board):
        # Reset the text and background color
        for button in sub_board:
            button.config(text=' ', bg=colors[i % 2], state='normal')


# Function to display a message and reset the game
def game_over(message):
    file_name = f"tic_tac_toe_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(file_name, 'w') as log_file:
        for entry in game_log:
            log_file.write(f"{entry},")
    messagebox.showinfo("Game Over", message + f"Game log saved to {file_name}")
    reset_board()


# Function to handle player move
def player_move(index):
    global current_player, last_place, move_log, game_log
    i, j = index
    if buttons_state[i][j] == ' ' and (last_place is None or sub_board_state[last_place] != ' ' or i == last_place):
        # Update the buttons_state and color
        buttons_state[i][j] = current_player
        board[i][j].config(bg=player_color[current_player], state='disabled')
        undo_button.config(bg=player_color[current_player])
        resign_button.config(bg=player_color['Blue' if current_player == 'Red' else 'Red'])
        move_log.append(index)
        game_log.append(index)

        # Check for a win or tie in sub_board
        if check_sub_winner(current_player, i):
            sub_board_state[i] = current_player
            for button in board[i]:
                button.config(bg=player_color[current_player], state='disabled')
            if check_winner(current_player):
                game_over(f"Player {current_player} wins!")
                return
            elif check_tie():
                game_over("It's a tie!")
                return
        elif check_sub_tie(i):
            sub_board_state[i] = 'Tie'
            if check_tie():
                game_over("It's a tie!")
                return

        # Switch players & mark the place
        current_player = 'Blue' if current_player == 'Red' else 'Red'
        last_place = j
        update_current_player()
        update_possible_moves()


# Function to handle undoing the last move
def undo_last_move():
    global current_player, last_place, move_log, game_log
    if last_place is not None:
        i, j = move_log.pop()
        game_log.append((-1, -1))

        if sub_board_state[i] == ' ':
            # Reset the button and enable it again
            buttons_state[i][j] = ' '
            board[i][j].config(state='normal', bg=colors[i % 2])
        elif sub_board_state[i] == 'Tie':
            # Reset the button and enable it again then Reset the sub board
            buttons_state[i][j] = ' '
            board[i][j].config(state='normal', bg=colors[i % 2])
            sub_board_state[i] = ' '
        else:
            # Reset the button and Reset the sub board
            buttons_state[i][j] = ' '
            sub_board_state[i] = ' '
            for k in range(9):
                if buttons_state[i][k] == ' ':
                    board[i][k].config(state='normal', bg=colors[i%2])
                else:
                    board[i][k].config(state='disabled', bg=player_color[buttons_state[i][k]])

        undo_button.config(bg=player_color['Blue' if current_player == 'Red' else 'Red'])
        resign_button.config(bg=player_color[current_player])
        # Switch back to the previous player
        current_player = 'Red' if current_player == 'Blue' else 'Blue'
        if move_log:
            last_place = move_log[-1][1]
        else:
            last_place = None
        update_current_player()
        update_possible_moves()

# Function to handle resigning game
def resign_game():
    global current_player
    winner = 'Blue' if current_player == 'Red' else 'Red'  # The other player wins
    game_log.append((-2, -2))
    game_over(f"Player {current_player} resigned. Player {winner} wins!")


# Function to check if there's a winner in sub_board
def check_sub_winner(player, i):
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
                      (0, 4, 8), (2, 4, 6)]  # Diagonals
    for condition in win_conditions:
        if buttons_state[i][condition[0]] == buttons_state[i][condition[1]] == buttons_state[i][condition[2]] == player:
            return True
    return False


# Function to check if there's a tie in sub_board
def check_sub_tie(i):
    return ' ' not in buttons_state[i]


# Function to check if there's a winner
def check_winner(player):
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
                      (0, 4, 8), (2, 4, 6)]  # Diagonals
    for condition in win_conditions:
        if sub_board_state[condition[0]] == sub_board_state[condition[1]] == sub_board_state[condition[2]] == player:
            return True
    return False


# Function to check for a tie
def check_tie():
    return ' ' not in sub_board_state


# Create a 3x3 grid of 3x3 grid buttons with background colors
board = []
for i in range(9):
    sub_board = []
    for j in range(9):
        button = tk.Button(root, font=('normal', 20), width=5, height=2,
                           bg=colors[i % 2], command=lambda p=(i, j): player_move(p))
        button.grid(row=i // 3 * 3 + j // 3, column=i % 3 * 3 + j % 3)
        sub_board.append(button)
    board.append(sub_board)

# Create a frame for the side panel (to hold the label and small board)
side_panel = tk.Frame(root)
side_panel.grid(row=0, column=9, rowspan=10, padx=20, sticky="n")

# Create a frame for the current player
player_frame = tk.Frame(side_panel)
player_frame.grid(row=0, column=0, pady=30, sticky="w")
# Create a label and a button to show the current player
player_label1 = tk.Label(player_frame, text="Player:", font=('normal', 20))
player_label1.grid(row=0, column=0)
player_label2 = tk.Label(player_frame, text=f"{current_player}", font=('normal', 20))
player_label2.grid(row=1, column=1)
player_button = tk.Button(player_frame, font=('normal', 20), width=5, height=2,
                          bg=player_color[current_player], state='disabled')
player_button.grid(row=1, column=2)

# Create a frame for the small board (to show possible moves or info)
small_board_frame = tk.Frame(side_panel)
small_board_frame.grid(row=2, column=0, pady=30, sticky="w")
# Create a label to show the playable button
button_label = tk.Label(small_board_frame, text="Play Zone:", font=('normal', 20))
button_label.grid(row=0, column=0)
# Create a small 3x3 grid to display possible moves or relevant info
small_board = []
for i in range(9):
    small_button = tk.Button(small_board_frame, font=('normal', 20), width=5, height=2,
                             bg=light_color, state='disabled')
    small_button.grid(row=1 + i // 3, column=1 + i % 3)
    small_board.append(small_button)

# Create a frame for the current player
button_frame = tk.Frame(side_panel)
button_frame.grid(row=3, column=0, pady=30, sticky="w")
# Create an Undo button
undo_button = tk.Button(button_frame, text="Undo", font=('normal', 20),
                        bg=player_color['Red' if current_player == 'Blue' else 'Blue'], command=undo_last_move)
undo_button.grid(row=0, column=0, padx=30, sticky="w")
# Create a Resign button
resign_button = tk.Button(button_frame, text="Resign", font=('normal', 20),
                          bg=player_color[current_player], command=resign_game)
resign_button.grid(row=0, column=1, padx=60, sticky="e")

# Start the GUI event loop
root.mainloop()
