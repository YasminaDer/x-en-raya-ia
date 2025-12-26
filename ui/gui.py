import tkinter as tk
from tkinter import ttk, messagebox

from model.board import Board
from model.game import Game
from players.human_player import HumanPlayer
from players.ai_player import AIPlayer

from ai.minimax import MinimaxAgent
from ai.alphabeta import AlphaBetaAgent


class GameGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("X en Raya - IA (Investigación)")
        self.game = None

        # Notebook con pestañas
        self.notebook = ttk.Notebook(root)
        self.tab_game = ttk.Frame(self.notebook)
        self.tab_info = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_game, text="Juego")
        self.notebook.add(self.tab_info, text="Información (IA)")
        self.notebook.pack(fill="both", expand=True)

        # Contenedores principales por pestaña
        self.game_frame = tk.Frame(self.tab_game)
        self.game_frame.pack(fill="both", expand=True)

        self.info_frame = tk.Frame(self.tab_info)
        self.info_frame.pack(fill="both", expand=True)

        # Variables del panel de info
        self.info_algo = tk.StringVar(value="Algoritmo: -")
        self.info_move = tk.StringVar(value="Jugada IA: -")
        self.info_reason = tk.StringVar(value="Motivo (heurística): -")
        self.info_prunes = tk.StringVar(value="Podas (Alpha-Beta): -")
        self.info_stoch = tk.StringVar(value="Estocástico: -")
        self.info_nodes = tk.StringVar(value="Nodos: -")
        self.info_time = tk.StringVar(value="Tiempo (ms): -")

        self.build_info_panel()
        self.show_config_screen()

    # ---------------- INFO PANEL ----------------

    def build_info_panel(self):
        tk.Label(self.info_frame, text="Panel didáctico (sin árbol)", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.info_frame, textvariable=self.info_algo, font=("Arial", 12)).pack(anchor="w", padx=12, pady=4)
        tk.Label(self.info_frame, textvariable=self.info_move, font=("Arial", 12)).pack(anchor="w", padx=12, pady=4)

        tk.Label(
            self.info_frame,
            textvariable=self.info_reason,
            font=("Arial", 12),
            wraplength=420,
            justify="left"
        ).pack(anchor="w", padx=12, pady=4)

        tk.Label(self.info_frame, textvariable=self.info_prunes, font=("Arial", 12)).pack(anchor="w", padx=12, pady=4)
        tk.Label(self.info_frame, textvariable=self.info_nodes, font=("Arial", 12)).pack(anchor="w", padx=12, pady=4)
        tk.Label(self.info_frame, textvariable=self.info_time, font=("Arial", 12)).pack(anchor="w", padx=12, pady=4)
        tk.Label(self.info_frame, textvariable=self.info_stoch, font=("Arial", 12)).pack(anchor="w", padx=12, pady=4)

        ttk.Separator(self.info_frame, orient="horizontal").pack(fill="x", pady=10)

        tk.Label(
            self.info_frame,
            text="Se muestra:\n"
                 "• qué jugada eligió la IA\n"
                 "• por qué (explicación basada en heurística)\n"
                 "• cuántas podas hizo (si Alpha-Beta)\n"
                 "• si hubo estocasticidad (ε)\n"
                 "Sin mostrar árboles (pueden ser enormes).",
            justify="left"
        ).pack(anchor="w", padx=12)

        tk.Button(
            self.info_frame,
            text="Ver razonamiento (top jugadas)",
            command=self.show_reasoning_popup
        ).pack(pady=12)

    def reset_info_panel(self):
        self.info_algo.set("Algoritmo: -")
        self.info_move.set("Jugada IA: -")
        self.info_reason.set("Motivo (heurística): -")
        self.info_prunes.set("Podas (Alpha-Beta): -")
        self.info_nodes.set("Nodos: -")
        self.info_time.set("Tiempo (ms): -")
        self.info_stoch.set("Estocástico: -")

    def update_info_panel(self, decision):
        """
        decision puede ser:
        - objeto con atributos (DecisionInfo)
        - dict
        - None
        """
        if decision is None:
            self.reset_info_panel()
            return

        def get_field(name, default="-"):
            if isinstance(decision, dict):
                return decision.get(name, default)
            return getattr(decision, name, default)

        algo = get_field("algorithm", "-")
        move = get_field("move", "-")
        reason = get_field("reason", "-")
        prunes = get_field("prunes", "-")
        nodes = get_field("nodes", "-")
        time_ms = get_field("time_ms", "-")

        stochastic = get_field("stochastic", False)
        epsilon = get_field("epsilon", None)
        exploration_taken = get_field("exploration_taken", False)

        self.info_algo.set(f"Algoritmo: {algo}")
        self.info_move.set(f"Jugada IA: {move}")
        self.info_reason.set(f"Motivo (heurística): {reason}")

        if prunes in ("-", None):
            self.info_prunes.set("Podas (Alpha-Beta): -")
        else:
            self.info_prunes.set(f"Podas (Alpha-Beta): {prunes}")

        self.info_nodes.set(f"Nodos: {nodes}")
        self.info_time.set(f"Tiempo (ms): {time_ms}")

        if stochastic:
            extra = "exploración" if exploration_taken else "óptima"
            self.info_stoch.set(f"Estocástico: Sí | ε={epsilon} | decisión: {extra}")
        else:
            self.info_stoch.set("Estocástico: No")

    def show_reasoning_popup(self):
        if self.game is None:
            messagebox.showinfo("Info", "No hay partida en curso.")
            return

        decision = getattr(self.game.ai, "last_decision", None)
        if decision is None:
            messagebox.showinfo("Info", "Aún no hay decisión registrada.")
            return

        def get_field(name, default="-"):
            if isinstance(decision, dict):
                return decision.get(name, default)
            return getattr(decision, name, default)

        lines = []
        lines.append(f"Algoritmo: {get_field('algorithm')}")
        lines.append(f"Jugada: {get_field('move')}")
        lines.append(f"Score: {get_field('score', '-')}")
        lines.append(f"Motivo: {get_field('reason')}")
        lines.append(f"Podas: {get_field('prunes', '-')}")
        lines.append(f"Nodos: {get_field('nodes', '-')}")
        lines.append(f"Tiempo (ms): {get_field('time_ms', '-')}")
        if get_field("stochastic", False):
            lines.append(f"Estocástico: Sí | ε={get_field('epsilon', '-')}, exploración={get_field('exploration_taken', False)}")
        else:
            lines.append("Estocástico: No")

        top_moves = get_field("top_moves", None)
        if top_moves:
            lines.append("\nTop jugadas (raíz):")
            for m, sc in top_moves:
                lines.append(f"  {m} -> {sc}")
        else:
            lines.append("\nTop jugadas: (no disponible todavía)")

        messagebox.showinfo("Razonamiento IA", "\n".join(lines))

    # ---------------- CONFIGURACIÓN ----------------

    def show_config_screen(self):
        self.clear_game_screen()

        tk.Label(self.game_frame, text="Configuración del juego", font=("Arial", 16)).pack(pady=10)

        # Tamaño tablero
        size_frame = tk.Frame(self.game_frame)
        size_frame.pack(pady=5)
        tk.Label(size_frame, text="Tamaño del tablero:").pack(side=tk.LEFT)
        self.size_var = tk.IntVar(value=3)
        tk.Entry(size_frame, textvariable=self.size_var, width=5).pack(side=tk.LEFT)

        # Dificultad
        diff_frame = tk.Frame(self.game_frame)
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

        # Estocasticidad
        stoch_frame = tk.Frame(self.game_frame)
        stoch_frame.pack(pady=8)

        self.use_stochastic_var = tk.BooleanVar(value=False)
        self.epsilon_var = tk.DoubleVar(value=0.10)

        tk.Checkbutton(stoch_frame, text="Estocasticidad", variable=self.use_stochastic_var).pack(side=tk.LEFT, padx=8)
        tk.Label(stoch_frame, text="ε:").pack(side=tk.LEFT)
        ttk.Spinbox(
            stoch_frame,
            from_=0.0, to=1.0, increment=0.05,
            textvariable=self.epsilon_var,
            width=6
        ).pack(side=tk.LEFT, padx=6)

        tk.Button(self.game_frame, text="Empezar partida", command=self.start_game).pack(pady=15)

        self.reset_info_panel()

    # ---------------- INICIO DEL JUEGO ----------------

    def start_game(self):
        size = self.size_var.get()
        difficulty = self.difficulty_var.get()

        if size < 3:
            messagebox.showerror("Error", "El tamaño mínimo es 3")
            return

        use_stochastic = self.use_stochastic_var.get()
        epsilon = float(self.epsilon_var.get())

        if difficulty == "Fácil":
            agent = MinimaxAgent(depth=1)
            algo_name = "Minimax"
        elif difficulty == "Medio":
            agent = AlphaBetaAgent(depth=3)
            algo_name = "AlphaBeta"
        else:
            agent = AlphaBetaAgent(depth=5)
            algo_name = "AlphaBeta"

        board = Board(size)
        human = HumanPlayer('X')

        # IMPORTANTE: lo ideal es que tu AIPlayer acepte estos params (y guarde last_decision)
        try:
            ai = AIPlayer('O', agent, use_stochastic=use_stochastic, epsilon=epsilon)
        except TypeError:
            # compatibilidad si aún no cambiaste AIPlayer
            ai = AIPlayer('O', agent)
            ai.use_stochastic = use_stochastic
            ai.epsilon = epsilon
            ai.last_decision = None

        self.game = Game(board, human, ai)

        # Info inicial
        self.update_info_panel({
            "algorithm": algo_name,
            "move": "-",
            "reason": "-",
            "prunes": "-" if algo_name != "AlphaBeta" else 0,
            "stochastic": use_stochastic,
            "epsilon": epsilon,
            "exploration_taken": False,
            "nodes": "-",
            "time_ms": "-"
        })

        self.show_game_screen()

    # ---------------- PANTALLA DE JUEGO ----------------

    def show_game_screen(self):
        self.clear_game_screen()

        self.status_label = tk.Label(self.game_frame, text="Turno de X", font=("Arial", 14))
        self.status_label.pack(pady=5)

        self.board_frame = tk.Frame(self.game_frame)
        self.board_frame.pack()

        self.buttons = []
        size = self.game.board.size

        for r in range(size):
            row_buttons = []
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
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        tk.Button(self.game_frame, text="Reiniciar partida", command=self.show_config_screen).pack(pady=10)

    # ---------------- LÓGICA DEL JUEGO ----------------

    def on_click(self, row, col):
        if self.game.finished:
            return

        if self.game.current_player == 'X' and self.game.board.is_empty(row, col):
            self.make_move(row, col, 'X')
            if not self.game.finished:
                self.root.after(200, self.ai_move)

    def ai_move(self):
        move = self.game.ai.choose_move(self.game.board)
        if move:
            self.make_move(move[0], move[1], 'O')

            decision = getattr(self.game.ai, "last_decision", None)
            if decision is not None:
                self.update_info_panel(decision)
            else:
                # fallback si backend aún no está adaptado
                self.update_info_panel({
                    "algorithm": type(getattr(self.game.ai, "agent", None)).__name__,
                    "move": move,
                    "reason": "Pendiente: backend debe devolver DecisionInfo con explicación/podas",
                    "prunes": "Pendiente",
                    "stochastic": getattr(self.game.ai, "use_stochastic", False),
                    "epsilon": getattr(self.game.ai, "epsilon", None),
                    "exploration_taken": False,
                    "nodes": "-",
                    "time_ms": "-"
                })

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

    def clear_game_screen(self):
        for widget in self.game_frame.winfo_children():
            widget.destroy()
