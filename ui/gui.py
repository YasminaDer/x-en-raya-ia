import tkinter as tk
from tkinter import ttk, messagebox

from model.board import Board
from model.game import Game
from players.human_player import HumanPlayer
from players.ai_player import AIPlayer

from ai.minimax import MinimaxAgent
from ai.alphabeta import AlphaBetaAgent


class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("X en Raya - IA")

        self.main_frame = tk.Frame(root)
        self.main_frame.pack()

        self.show_config_screen()

    # ---------------- CONFIGURACIÓN ----------------

    def show_config_screen(self):
        self.clear_screen()

        tk.Label(self.main_frame, text="Configuración del juego", font=("Arial", 16)).pack(pady=10)

        # Tamaño tablero
        size_frame = tk.Frame(self.main_frame)
        size_frame.pack(pady=5)
        tk.Label(size_frame, text="Tamaño del tablero:").pack(side=tk.LEFT)
        self.size_var = tk.IntVar(value=3)
        tk.Entry(size_frame, textvariable=self.size_var, width=5).pack(side=tk.LEFT)

        # Dificultad
        diff_frame = tk.Frame(self.main_frame)
        diff_frame.pack(pady=5)
        tk.Label(diff_frame, text="Dificultad:").pack(side=tk.LEFT)

        self.difficulty_var = tk.StringVar(value="Medio")
        self.difficulty_combo = ttk.Combobox(
            diff_frame,
            textvariable=self.difficulty_var,
            values=["Fácil", "Medio", "Difícil"],
            state="readonly",
            width=10
        )
        self.difficulty_combo.pack(side=tk.LEFT)

        tk.Button(
            self.main_frame,
            text="Empezar partida",
            command=self.start_game
        ).pack(pady=15)

    # ---------------- INICIO DEL JUEGO ----------------

    def start_game(self):
        size = self.size_var.get()
        difficulty = self.difficulty_var.get()

        if size < 3:
            messagebox.showerror("Error", "El tamaño mínimo es 3")
            return

        # Selección de dificultad
        if difficulty == "Fácil":
            agent = MinimaxAgent(depth=1)
        elif difficulty == "Medio":
            agent = AlphaBetaAgent(depth=3)
        else:
            agent = AlphaBetaAgent(depth=5)

        board = Board(size)
        human = HumanPlayer('X')
        ai = AIPlayer('O', agent)
        self.game = Game(board, human, ai)

        self.show_game_screen()

    # ---------------- PANTALLA DE JUEGO ----------------

    def show_game_screen(self):
        self.clear_screen()

        self.status_label = tk.Label(self.main_frame, text="Turno de X", font=("Arial", 14))
        self.status_label.pack(pady=5)

        self.board_frame = tk.Frame(self.main_frame)
        self.board_frame.pack()

        self.buttons = []
        size = self.game.board.size

        for r in range(size):
            row = []
            for c in range(size):
                btn = tk.Button(
                    self.board_frame,
                    text=" ",
                    font=("Arial", 20),
                    width=4,
                    height=2,
                    command=lambda r=r, c=c: self.on_click(r, c)
                )
                btn.grid(row=r, column=c)
                row.append(btn)
            self.buttons.append(row)

        tk.Button(
            self.main_frame,
            text="Reiniciar partida",
            command=self.show_config_screen
        ).pack(pady=10)

    # ---------------- LÓGICA DEL JUEGO ----------------

    def on_click(self, row, col):
        if self.game.finished:
            return

        if self.game.current_player == 'X' and self.game.board.is_empty(row, col):
            self.make_move(row, col, 'X')

            if not self.game.finished:
                self.root.after(300, self.ai_move)

    def ai_move(self):
        move = self.game.ai.choose_move(self.game.board)
        if move:
            self.make_move(move[0], move[1], 'O')

    def make_move(self, row, col, symbol):
        self.game.board.place(row, col, symbol)
        self.buttons[row][col].config(text=symbol, state="disabled")

        result = self.game.check_end()
        if result:
            if result == "Draw":
                messagebox.showinfo("Resultado", "Empate")
            else:
                messagebox.showinfo("Resultado", f"Gana {result}")
        else:
            self.game.switch_turn()
            self.status_label.config(text=f"Turno de {self.game.current_player}")

    # ---------------- UTILIDAD ----------------

    def clear_screen(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
