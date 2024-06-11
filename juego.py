import tkinter as tk
from tkinter import messagebox
import math
import random

# --- Lógica del juego ---
def init_board():
    return [' ' for _ in range(9)]

def display_board(board):
    for i in range(3):
        for j in range(3):
            button_text = board[i * 3 + j]
            buttons[i][j].config(
                text=button_text,
                state=tk.DISABLED if button_text != ' ' else tk.NORMAL,
                fg='white' if button_text == 'X' else 'red' if button_text == 'O' else 'white'
            )

def check_winner(board, mark):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Filas
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columnas
        [0, 4, 8], [2, 4, 6]  # Diagonales
    ]
    for condition in win_conditions:
        if all(board[i] == mark for i in condition):
            return True
    return False

def check_draw(board):
    return ' ' not in board

def minimax(board, depth, alpha, beta, is_maximizing):
    if check_winner(board, 'O'):
        return 1
    if check_winner(board, 'X'):
        return -1
    if check_draw(board) or depth == 9:  # Límite de profundidad
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(board, depth + 1, alpha, beta, False)
                board[i] = ' '
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, depth + 1, alpha, beta, True)
                board[i] = ' '
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
        return best_score

def computer_move(board):
    best_score = -math.inf
    best_move = None
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(board, 0, -math.inf, math.inf, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                best_move = i

    # Si no se encontró un mejor movimiento (best_move sigue siendo None),
    # elige un movimiento aleatorio de los espacios disponibles
    if best_move is None:
        available_moves = [i for i in range(9) if board[i] == ' ']
        best_move = random.choice(available_moves)

    return best_move

# --- Funciones para la interfaz gráfica ---
def handle_click(row, col):
    global current_player, game_mode
    if board[row * 3 + col] == ' ' and current_player != ' ':
        make_move(row, col)

def make_move(row, col):
    global current_player
    board[row * 3 + col] = current_player
    buttons[row][col].config(
        text=current_player,
        state=tk.DISABLED,
        fg='white' if current_player == 'X' else 'red'
    )

    if check_winner(board, current_player):
        messagebox.showinfo("¡Fin del juego!", f"¡{'Has ganado!' if current_player == 'X' else 'La computadora ha ganado!'}")
        reset_game()
    elif check_draw(board):
        messagebox.showinfo("¡Fin del juego!", "¡Es un empate!")
        reset_game()
    else:
        switch_player()

def switch_player():
    global current_player
    current_player = 'O' if current_player == 'X' else 'X'
    if game_mode == "pc" and current_player == 'O':
        window.after(500, computer_turn)

def computer_turn():
    move = computer_move(board)
    row, col = divmod(move, 3)
    make_move(row, col)

def reset_game():
    global board, current_player
    board = init_board()
    current_player = 'X'
    display_board(board)
    if game_mode == "pc":
        ask_first_player()
    else:  # Modo de 2 jugadores
        for i in range(3):
            for j in range(3):
                buttons[i][j].config(
                    text=' ',
                    state=tk.NORMAL,
                    fg='white'
                )

def start_game(mode, first_player='X'):
    global game_mode, current_player
    game_mode = mode
    current_player = first_player
    game_screen()
    display_board(board)
    if game_mode == "pc" and current_player == 'O':
        window.after(500, computer_turn)

def ask_first_player():
    global current_player
    answer = messagebox.askyesno("Tres en Raya", "¿Quieres empezar primero?")
    if answer:
        start_game("pc", 'X')
    else:
        start_game("pc", 'O')

# --- Pantallas del juego ---
def main_menu():
    window.title("Tres en Raya")
    window.configure(bg="#242424")
    window.geometry("575x600")
    window.resizable(False, False)

    for widget in window.winfo_children():
        widget.destroy()

    title_label = tk.Label(
        window,
        text="Tres en Raya",
        font=("Arial", 32, "bold"),
        fg="white",
        bg="#242424"
    )
    title_label.pack(pady=(50, 10))

    creator_label = tk.Label(
        window,
        text="Creador: Johan Morales",
        font=("Arial", 20, "bold"),
        fg="yellow",
        bg="#242424"
    )
    creator_label.pack(pady=(0, 30))

    button_style = {
        "font": ("Arial", 24, "bold"),
        "fg": "white",
        "bg": "#3d3d3d",
        "borderwidth": 0,
        "highlightthickness": 0,
        "width": 15,
        "pady": 10
    }

    pc_button = tk.Button(
        window,
        text="Vs. Computadora",
        command=ask_first_player,
        **button_style
    )
    pc_button.pack(pady=10)

    player_button = tk.Button(
        window,
        text="2 Jugadores",
        command=lambda: start_game("2player"),
        **button_style
    )
    player_button.pack()

def game_screen():
    global buttons
    for widget in window.winfo_children():
        widget.destroy()

    window.configure(bg="#333333")

    game_frame = tk.Frame(window, bg="#333333")
    game_frame.pack(pady=20)

    buttons = [[None for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j] = tk.Button(
                game_frame,
                text=' ',
                font=("Arial", 40, "bold"),
                width=3,
                height=1,
                bg="#4d4d4d",
                fg='white',
                borderwidth=2,
                relief="groove",
                command=lambda r=i, c=j: handle_click(r, c)
            )
            buttons[i][j].grid(row=i, column=j, padx=5, pady=5)

    button_frame = tk.Frame(window, bg="#333333")
    button_frame.pack()

    reset_button = tk.Button(
        button_frame,
        text="Reiniciar",
        font=("Arial", 18),
        bg="#4CAF50",
        fg="white",
        width=10,
        command=reset_game
    )
    reset_button.pack(side=tk.LEFT, padx=10)

    back_button = tk.Button(
        button_frame,
        text="Volver",
        font=("Arial", 18),
        bg="#5c5c5c",
        fg="white",
        width=10,
        command=main_menu
    )
    back_button.pack(side=tk.LEFT, padx=10)

# --- Inicialización del juego ---
window = tk.Tk()
board = init_board()
game_mode = ""
current_player = ' '

main_menu()

window.mainloop()