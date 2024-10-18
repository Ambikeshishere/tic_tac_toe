import tkinter as tk
from tkinter import messagebox
import pygame
import time

board = [" " for _ in range(9)]
current_player = "X"
player_X = ""
player_O = ""

pygame.mixer.init()
x_sound = pygame.mixer.Sound("x_sound.wav")
o_sound = pygame.mixer.Sound("o_sound.wav")
win_sound = pygame.mixer.Sound("win_sound.wav")

def check_winner():
    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != " ":
            return board[combo[0]], combo
    return None, None

def highlight_winning_buttons(winning_combo):
    for index in winning_combo:
        buttons[index].config(bg='green')

def make_move(index, button):
    global current_player
    if board[index] == " ":
        board[index] = current_player
        button.config(text=current_player)
        button.config(state=tk.DISABLED)
        if current_player == "X":
            x_sound.play()
            button.config(bg='red')
            sound_duration = x_sound.get_length()
        else:
            o_sound.play()
            button.config(bg='blue')
            sound_duration = o_sound.get_length()
        button.after(100, lambda: button.config(bg=''))
        button.after(int(sound_duration * 1000), lambda: button.config(state=tk.NORMAL))
        winner, winning_combo = check_winner()
        if winner:
            winning_player = player_X if winner == "X" else player_O
            win_sound.play()
            highlight_winning_buttons(winning_combo)
            display_winner(winning_player, winner)
            reset_game()
        elif " " not in board:
            display_winner("No one", "draw")
            reset_game()
        else:
            current_player = "O" if current_player == "X" else "X"
            update_turn_label()

def display_winner(winning_player, winner):
    if winner == "draw":
        winner_label.config(text="It's a draw!", font=('Arial', 24), bg='black', fg='white')
    else:
        winner_label.config(text=f"{winning_player} ({winner}) wins!", font=('Arial', 24), bg='black', fg='white')

def update_turn_label():
    current_player_name = player_X if current_player == "X" else player_O
    turn_label.config(text=f"Turn: {current_player_name} ({current_player})")

def reset_game():
    global board, current_player
    board = [" " for _ in range(9)]
    current_player = "X"
    for btn in buttons:
        btn.config(text=" ", state=tk.NORMAL, bg='')
    winner_label.config(text="")
    update_turn_label()

def exit_game():
    pygame.mixer.quit()
    root.quit()

def start_game():
    global player_X, player_O
    player_X = player_X_entry.get()
    player_O = player_O_entry.get()
    if not player_X or not player_O:
        messagebox.showwarning("Input Error", "Please enter both player names!")
        return
    player_frame.pack_forget()
    game_frame.pack()
    update_turn_label()

root = tk.Tk()
root.title("Tic Tac Toe")
root.attributes("-fullscreen", True)
root.configure(bg='black')
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

player_frame = tk.Frame(root, bg='black')
player_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
tk.Label(player_frame, text="Enter Player Names", font=('Arial', 24), bg='black', fg='white').pack(pady=20)
tk.Label(player_frame, text="Player X Name:", font=('Arial', 18), bg='black', fg='white').pack(pady=5)
player_X_entry = tk.Entry(player_frame, font=('Arial', 18))
player_X_entry.pack(pady=10)
tk.Label(player_frame, text="Player O Name:", font=('Arial', 18), bg='black', fg='white').pack(pady=5)
player_O_entry = tk.Entry(player_frame, font=('Arial', 18))
player_O_entry.pack(pady=10)
start_button = tk.Button(player_frame, text="Start Game", font=('Arial', 18), command=start_game)
start_button.pack(pady=20)

game_frame = tk.Frame(root, bg='black')
turn_label = tk.Label(game_frame, text="Turn: ", font=('Arial', 24), bg='black', fg='white')
turn_label.grid(row=0, column=0, columnspan=3, pady=20)
winner_label = tk.Label(game_frame, text="", font=('Arial', 24), bg='black', fg='white')
winner_label.grid(row=1, column=0, columnspan=3, pady=20)

buttons = []
for i in range(9):
    btn = tk.Button(game_frame, text=" ", width=10, height=3, font=('Arial', 24),
                    command=lambda i=i: make_move(i, buttons[i]))
    btn.grid(row=(i // 3) + 2, column=i % 3, padx=10, pady=10)
    buttons.append(btn)

restart_button = tk.Button(game_frame, text="Restart", font=('Arial', 18), command=reset_game)
restart_button.grid(row=5, column=0, columnspan=3, pady=20)
exit_button = tk.Button(game_frame, text="Exit", font=('Arial', 18), command=exit_game)
exit_button.grid(row=6, column=0, columnspan=3, pady=10)

player_frame.pack()
root.mainloop()
