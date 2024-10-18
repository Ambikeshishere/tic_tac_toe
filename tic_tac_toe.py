import tkinter as tk
from tkinter import messagebox
import pygame
import time

# Initialize the game board
board = [" " for _ in range(9)]  # A list to hold the 3x3 grid, initially empty
current_player = "X"  # X starts first
player_X = ""  # Name of Player X
player_O = ""  # Name of Player O

# Initialize pygame mixer for sound
pygame.mixer.init()

# Load sound files
x_sound = pygame.mixer.Sound("x.mp3")  # Replace with your X sound file
o_sound = pygame.mixer.Sound("o.mp3")  # Replace with your O sound file
win_sound = pygame.mixer.Sound("onicha.mp3")  # Replace with your winning sound file

# Function to check if a player has won
def check_winner():
    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)  # Diagonals
    ]
    
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != " ":
            return board[combo[0]], combo  # Return the winner and the winning combination
    
    return None, None

# Function to highlight winning buttons
def highlight_winning_buttons(winning_combo):
    for index in winning_combo:
        buttons[index].config(bg='green')  # Change color to green for winning buttons

# Function to handle player's move
def make_move(index, button):
    global current_player

    if board[index] == " ":
        board[index] = current_player
        button.config(text=current_player)

        # Disable button during sound playback
        button.config(state=tk.DISABLED)

        # Play sound based on the current player
        if current_player == "X":
            x_sound.play()
            button.config(bg='red')  # Change button color to red for X
            sound_duration = x_sound.get_length()
        else:
            o_sound.play()
            button.config(bg='blue')  # Change button color to blue for O
            sound_duration = o_sound.get_length()
        
        # Animate button press
        button.after(100, lambda: button.config(bg=''))  # Reset color after 100ms
        
        # Wait for the sound to finish before allowing the next move
        button.after(int(sound_duration * 1000), lambda: button.config(state=tk.NORMAL))  # Re-enable button

        winner, winning_combo = check_winner()
        if winner:
            winning_player = player_X if winner == "X" else player_O
            win_sound.play()  # Play the winning sound
            highlight_winning_buttons(winning_combo)  # Highlight winning buttons
            display_winner(winning_player, winner)  # Display the winner on the screen
            reset_game()  # Reset game after a delay
        elif " " not in board:
            display_winner("No one", "draw")  # Display draw message
            reset_game()
        else:
            # Switch the player
            current_player = "O" if current_player == "X" else "X"
            update_turn_label()

# Function to display the winner on the screen
def display_winner(winning_player, winner):
    if winner == "draw":
        winner_label.config(text="It's a draw!", font=('Arial', 24), bg='black', fg='white')
    else:
        winner_label.config(text=f"{winning_player} ({winner}) wins!", font=('Arial', 24), bg='black', fg='white')

# Function to update turn label
def update_turn_label():
    current_player_name = player_X if current_player == "X" else player_O
    turn_label.config(text=f"Turn: {current_player_name} ({current_player})")

# Function to reset the game
def reset_game():
    global board, current_player
    board = [" " for _ in range(9)]
    current_player = "X"
    for btn in buttons:
        btn.config(text=" ", state=tk.NORMAL, bg='')  # Reset button state and color
    winner_label.config(text="")  # Clear winner label
    update_turn_label()

# Function to handle exit
def exit_game():
    pygame.mixer.quit()  # Quit pygame mixer
    root.quit()

# Start the game after getting player names
def start_game():
    global player_X, player_O

    # Get player names from the entry fields
    player_X = player_X_entry.get()
    player_O = player_O_entry.get()

    # Ensure player names are not empty
    if not player_X or not player_O:
        messagebox.showwarning("Input Error", "Please enter both player names!")
        return

    # Hide the player entry screen
    player_frame.pack_forget()

    # Show the game board
    game_frame.pack()

    # Update the turn label
    update_turn_label()

# Create the main Tkinter window
root = tk.Tk()
root.title("Tic Tac Toe")

# Set the window to full screen when it opens
root.attributes("-fullscreen", True)
root.configure(bg='black')

# Bind the Escape key to exit full-screen mode
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

# Create player name entry screen
player_frame = tk.Frame(root, bg='black')
player_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

tk.Label(player_frame, text="Enter Player Names", font=('Arial', 24), bg='black', fg='white').pack(pady=20)

# Player X name entry
tk.Label(player_frame, text="Player X Name:", font=('Arial', 18), bg='black', fg='white').pack(pady=5)
player_X_entry = tk.Entry(player_frame, font=('Arial', 18))
player_X_entry.pack(pady=10)

# Player O name entry
tk.Label(player_frame, text="Player O Name:", font=('Arial', 18), bg='black', fg='white').pack(pady=5)
player_O_entry = tk.Entry(player_frame, font=('Arial', 18))
player_O_entry.pack(pady=10)

# Start button
start_button = tk.Button(player_frame, text="Start Game", font=('Arial', 18), command=start_game)
start_button.pack(pady=20)

# Create the game board
game_frame = tk.Frame(root, bg='black')

# Turn label
turn_label = tk.Label(game_frame, text="Turn: ", font=('Arial', 24), bg='black', fg='white')
turn_label.grid(row=0, column=0, columnspan=3, pady=20)

# Winner label
winner_label = tk.Label(game_frame, text="", font=('Arial', 24), bg='black', fg='white')
winner_label.grid(row=1, column=0, columnspan=3, pady=20)

# Create Tic-Tac-Toe buttons
buttons = []
for i in range(9):
    btn = tk.Button(game_frame, text=" ", width=10, height=3, font=('Arial', 24),
                    command=lambda i=i: make_move(i, buttons[i]))
    btn.grid(row=(i // 3) + 2, column=i % 3, padx=10, pady=10)
    buttons.append(btn)

# Create Restart and Exit buttons
restart_button = tk.Button(game_frame, text="Restart", font=('Arial', 18), command=reset_game)
restart_button.grid(row=5, column=0, columnspan=3, pady=20)

exit_button = tk.Button(game_frame, text="Exit", font=('Arial', 18), command=exit_game)
exit_button.grid(row=6, column=0, columnspan=3, pady=10)

# Initially, only the player name entry screen is visible
player_frame.pack()

# Start the Tkinter main loop
root.mainloop()
