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
            buttons[i][j].config(text=button_text, state=tk.DISABLED if button_text != ' ' else tk.NORMAL)

def check_winner(board, mark):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Filas
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columnas
        [0, 4, 8], [2, 4, 6]              # Diagonales
    ]
    for condition in win_conditions:
        if all(board[i] == mark for i in condition):
            return True
    return False

def check_draw(board):
    return ' ' not in board

def minimax(board, depth, is_maximizing):
    if check_winner(board, 'O'):
        return 1
    if check_winner(board, 'X'):
        return -1
    if check_draw(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(board, depth + 1, False)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, depth + 1, True)
                board[i] = ' '
                best_score = min(score, best_score)
        return best_score

def computer_move(board):
    if board.count(' ') == 9:
        return random.choice(range(9))
    
    best_score = -math.inf
    best_move = None
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(board, 0, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                best_move = i
    return best_move

# --- Funciones para la interfaz gráfica ---

def handle_click(row, col):
    global current_player
    if board[row * 3 + col] == ' ' and current_player == 'X':
        board[row * 3 + col] = 'X'
        buttons[row][col].config(text='X', state=tk.DISABLED, disabledforeground="white")
        if check_winner(board, 'X'):
            messagebox.showinfo("¡Fin del juego!", "¡Has ganado!")
            reset_game()
        elif check_draw(board):
            messagebox.showinfo("¡Fin del juego!", "¡Es un empate!")
            reset_game()
        else:
            current_player = 'O'
            computer_turn()

def computer_turn():
    global current_player
    move = computer_move(board)
    row, col = divmod(move, 3)  # Obtiene fila y columna a partir del índice
    board[move] = 'O'
    buttons[row][col].config(text='O', state=tk.DISABLED, disabledforeground="red")
    if check_winner(board, 'O'):
        messagebox.showinfo("¡Fin del juego!", "¡El ordenador ha ganado!")
        reset_game()
    elif check_draw(board):
        messagebox.showinfo("¡Fin del juego!", "¡Es un empate!")
        reset_game()
    else:
        current_player = 'X'

def reset_game():
    global board, current_player
    board = init_board()
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text=' ', state=tk.NORMAL)
    ask_first_player()

def ask_first_player():
    global current_player
    answer = messagebox.askyesno("¿Quieres jugar primero?", "¿Quieres jugar primero?")
    if answer:
        current_player = 'X'
    else:
        current_player = 'O'
        computer_turn()

# --- Configuración de la ventana principal ---

window = tk.Tk()
window.title("Tres en Raya")
window.configure(bg="#242424")  # Fondo oscuro
window.geometry("575x800")  # Tamaño de la ventana
window.resizable(False, False)  # Deshabilita la capacidad de redimensionar

# --- Creación de los botones ---

buttons = [[None for _ in range(3)] for _ in range(3)]
for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(
            window,
            text=' ',
            font=("Arial", 50, "bold"),
            width=4,
            height=2,
            bg="#3d3d3d",  # Fondo gris oscuro para los botones
            fg="white",    # Texto blanco
            borderwidth=0,  # Sin borde
            highlightthickness=0,  # Sin resalte al hacer clic
            command=lambda r=i, c=j: handle_click(r, c)
        )
        buttons[i][j].grid(row=i, column=j, padx=10, pady=10)

# --- Botón para reiniciar el juego ---

reset_button = tk.Button(
    window,
    text="Reiniciar",
    font=("Arial", 20, "bold"),
    bg="#4CAF50",  # Verde para el botón de reinicio
    fg="white",
    width=10,
    command=reset_game
)
reset_button.grid(row=3, column=0, columnspan=3, pady=20)

# --- Inicialización del juego ---

board = init_board()

def start_game():
    ask_first_player()

start_game()

window.mainloop()