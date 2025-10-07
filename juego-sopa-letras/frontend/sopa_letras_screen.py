import tkinter as tk
from tkinter import messagebox
import os
import time

from services import backend
from ui.board import Board

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "words.txt")

def load_words():
    with open(DATA_PATH, encoding="utf-8") as f:
        return [line.strip().upper() for line in f if line.strip()]

class SopaLetrasScreen:
    def __init__(self, root, volver_callback, board_size=15):
        self.root = root
        self.volver_callback = volver_callback
        self.board_size = board_size
        
        self.setup_responsive_layout()
        
        self.words = load_words()
        self.grid = []
        self.words_remaining = self.words[:]
        self.words_found = []
        self.start_time = None
        self.game_active = False
        
        self.setup_fonts()
        self.setup_ui()
        self.new_game()

    def get_screen_dimensions(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        return screen_width, screen_height

    def setup_responsive_layout(self):
        screen_width, screen_height = self.get_screen_dimensions()
        
        board_factor = max(1.0, (self.board_size - 10) / 10)
        
        # Optimizar para pantallas Full HD y superiores
        if screen_width >= 1920:
            window_width_percent = min(0.95, 0.75 + (board_factor * 0.1))
            window_height_percent = min(0.9, 0.8 + (board_factor * 0.05))
        else:
            window_width_percent = min(0.9, 0.6 + (board_factor * 0.15))
            window_height_percent = min(0.9, 0.7 + (board_factor * 0.1))
        
        window_width = int(screen_width * window_width_percent)
        window_height = int(screen_height * window_height_percent)
        
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.title(f"Sopa de Letras {self.board_size}x{self.board_size} - Proyecto Lenguajes")
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.configure(bg='#2c3e50')

    def setup_fonts(self):
        screen_width, screen_height = self.get_screen_dimensions()
        base_font_size = min(screen_width, screen_height) // 60
        
        board_factor = 1 + (self.board_size - 15) * 0.02
        
        self.title_font = ("Arial", max(16, int(base_font_size * 1.5 * board_factor)), "bold")
        self.word_font = ("Arial", max(10, int(base_font_size * 0.9 * board_factor)), "bold")
        self.button_font = ("Arial", max(9, int(base_font_size * 0.8 * board_factor)), "bold")
        self.label_font = ("Arial", max(9, int(base_font_size * 0.8 * board_factor)))
        self.stats_font = ("Arial", max(8, int(base_font_size * 0.7 * board_factor)))

    def setup_ui(self):
        header_frame = tk.Frame(self.root, bg='#2c3e50')
        header_frame.pack(fill='x', pady=5)
        
        back_btn = tk.Button(header_frame, text="← VOLVER AL MENÚ", 
                            command=self.volver_al_menu,
                            font=("Arial", 10, "bold"), bg='#95a5a6', fg='white',
                            activebackground='#7f8c8d', cursor='hand2')
        back_btn.pack(side='left', padx=10, pady=5)
        
        title_label = tk.Label(self.root, text="SOPA DE LETRAS", 
                            font=self.title_font, bg='#2c3e50', fg='#ecf0f1')
        title_label.pack(pady=10)
        
        self.stats_frame = tk.Frame(self.root, bg='#34495e', relief='raised', bd=2)
        self.stats_frame.pack(pady=10, padx=20, fill='x')
        
        self.words_found_label = tk.Label(self.stats_frame, text="", 
                                        font=self.stats_font, bg='#34495e', fg='#27ae60')
        self.words_found_label.pack(pady=5)
        
        self.timer_label = tk.Label(self.stats_frame, text="",font=self.stats_font, bg='#34495e', fg='#3498db')
        self.timer_label.pack(pady=2)
        
        self.words_frame = tk.Frame(self.stats_frame, bg='#34495e')
        self.words_frame.pack(pady=5, fill='x')
        
        words_title = tk.Label(self.words_frame, text="Palabras a buscar:",font=self.label_font, bg='#34495e', fg='#ecf0f1')
        words_title.pack(anchor='w')
        
        self.words_scroll_frame = tk.Frame(self.words_frame, bg='#34495e')
        self.words_scroll_frame.pack(fill='both', expand=True, pady=2)
        
        self.words_canvas = tk.Canvas(self.words_scroll_frame, bg='#34495e', height=80,highlightthickness=0)
        self.words_canvas.pack(side='left', fill='both', expand=True)
        
        self.words_scrollbar = tk.Scrollbar(self.words_scroll_frame, orient='horizontal', command=self.words_canvas.xview)
        self.words_scrollbar.pack(side='right', fill='y')
        
        self.words_canvas.configure(xscrollcommand=self.words_scrollbar.set)
        
        self.words_inner_frame = tk.Frame(self.words_canvas, bg='#34495e')
        self.words_canvas.create_window((0, 0), window=self.words_inner_frame, anchor='nw')
        
        self.words_canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.words_canvas.bind("<Button-4>", self._on_mousewheel)
        self.words_canvas.bind("<Button-5>", self._on_mousewheel)
        
        self.words_canvas.bind("<Enter>", lambda e: self.words_canvas.focus_set())
        self.words_canvas.bind("<Leave>", lambda e: self.root.focus_set())

        # Crear frame principal horizontal para board y controles
        main_game_frame = tk.Frame(self.root, bg='#2c3e50')
        main_game_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Frame izquierdo para el board
        board_frame = tk.Frame(main_game_frame, bg='#2c3e50')
        board_frame.pack(side='left', fill='both', expand=True)
        
        # Frame derecho para los controles
        controls_frame = tk.Frame(main_game_frame, bg='#34495e', relief='raised', bd=3)
        controls_frame.pack(side='right', fill='y', padx=(20, 0))
        controls_frame.config(width=200)  # Ancho fijo para el panel de controles
        
        # Título de controles
        controls_title = tk.Label(controls_frame, text="CONTROLES", 
                                 font=("Arial", 14, "bold"), bg='#34495e', fg='#ecf0f1')
        controls_title.pack(pady=15)
        
        # Botones de verificación y limpieza
        verify_btn = tk.Button(controls_frame, text="VERIFICAR", 
                              font=("Arial", 12, "bold"), bg='#27ae60', fg='white',
                              activebackground='#2ecc71', cursor='hand2',
                              command=self.on_verify_selection, width=15)
        verify_btn.pack(pady=8, padx=15)
        
        clear_btn = tk.Button(controls_frame, text="LIMPIAR", 
                             font=("Arial", 12, "bold"), bg='#e74c3c', fg='white',
                             activebackground='#c0392b', cursor='hand2',
                             command=self.on_clear_selection, width=15)
        clear_btn.pack(pady=8, padx=15)
        
        # Separador
        separator = tk.Frame(controls_frame, bg='#2c3e50', height=2)
        separator.pack(fill='x', pady=15, padx=10)
        
        # Botones de juego
        self.new_game_btn = tk.Button(controls_frame, text="NUEVO JUEGO", 
                                     command=self.new_game,
                                     font=("Arial", 12, "bold"), bg='#e67e22', fg='white',
                                     activebackground='#d35400', width=15, cursor='hand2')
        self.new_game_btn.pack(pady=8, padx=15)
        
        self.solve_btn = tk.Button(controls_frame, text="RESOLVER", command=self.solve_all,
                                  font=("Arial", 12, "bold"), bg='#9b59b6', fg='white', 
                                  activebackground='#8e44ad', width=15, cursor='hand2')
        self.solve_btn.pack(pady=8, padx=15)
        
        # Información de la palabra actual
        word_info_frame = tk.Frame(controls_frame, bg='#34495e')
        word_info_frame.pack(fill='x', pady=15, padx=10)
        
        word_info_title = tk.Label(word_info_frame, text="PALABRA ACTUAL:", 
                                  font=("Arial", 10, "bold"), bg='#34495e', fg='#bdc3c7')
        word_info_title.pack()
        
        # Crear el board con el nuevo frame
        self.board = Board(board_frame, 
                          on_verify_callback=self.on_verify_selection, 
                          on_clear_callback=self.on_clear_selection,
                          on_word_update_callback=self.update_word_display)
        self.board.get_frame().pack(expand=True)
        
        # Label de palabra actual en el panel de controles
        self.word_display_label = tk.Label(word_info_frame, text="", 
                                          font=("Arial", 12, "bold"), bg='#34495e', fg='#3498db',
                                          wraplength=150)
        self.word_display_label.pack(pady=5)
        
        # Mensaje de estado en el panel de controles
        message_frame = tk.Frame(controls_frame, bg='#34495e')
        message_frame.pack(fill='x', pady=10, padx=10)
        
        self.message_label = tk.Label(message_frame, text="", font=("Arial", 9), 
                                    bg='#34495e', fg='#f39c12', wraplength=140)
        self.message_label.pack()
        
        self.update_timer()

    def _on_mousewheel(self, event):
        if event.delta:
            self.words_canvas.xview_scroll(int(-1*(event.delta/120)), "units")
        else:
            if event.num == 4:
                self.words_canvas.xview_scroll(-1, "units")
            elif event.num == 5:
                self.words_canvas.xview_scroll(1, "units")

    def update_timer(self):
        try:
            if self.game_active and self.start_time:
                elapsed = int(time.time() - self.start_time)
                minutes = elapsed // 60
                seconds = elapsed % 60
                if hasattr(self, 'timer_label') and self.timer_label.winfo_exists():
                    self.timer_label.config(text=f"Tiempo: {minutes:02d}:{seconds:02d}")
            if hasattr(self, 'root') and self.root.winfo_exists():
                self.root.after(1000, self.update_timer)
        except tk.TclError:
            pass

    def new_game(self):
        resp = backend.generate(self.words, size=self.board_size)
        self.grid = resp["grid"]
        self.words_remaining = self.words[:]
        self.words_found = []
        self.start_time = time.time()
        self.game_active = True
        
        self.board.draw(self.grid)
        self.update_stats()
        self.message_label.config(text=f"¡Encuentra todas las palabras en el tablero {self.board_size}x{self.board_size}! Haz clic en las letras para formar palabras y presiona VERIFICAR.", fg='#f39c12')

    def update_stats(self):
        found_count = len(self.words_found)
        total_count = len(self.words)
        
        self.words_found_label.config(text=f"Encontradas: {found_count}/{total_count}")
        self.update_words_display()
        
        if found_count == total_count:
            self.game_active = False
            elapsed = int(time.time() - self.start_time) if self.start_time else 0
            minutes = elapsed // 60
            seconds = elapsed % 60
            self.message_label.config(text=f"¡Felicitaciones! Completaste la sopa en {minutes:02d}:{seconds:02d}", fg='#27ae60')
            messagebox.showinfo("¡Completado!", f"¡Felicitaciones! Completaste la sopa de letras en {minutes:02d}:{seconds:02d}")

    def update_words_display(self):
        for widget in self.words_inner_frame.winfo_children():
            widget.destroy()
        
        for word in self.words:
            if word in self.words_found:
                bg_color = '#27ae60'
                fg_color = 'white'
                text = f"✓ {word}"
                relief = 'sunken'
            else:
                bg_color = '#34495e'
                fg_color = '#ecf0f1'
                text = word
                relief = 'raised'
            
            word_label = tk.Label(self.words_inner_frame, text=text,
                                font=("Arial", 10, "bold"), bg=bg_color, fg=fg_color,
                                relief=relief, bd=1, padx=8, pady=2)
            word_label.pack(side='left', padx=2, pady=2)
        
        self.words_inner_frame.update_idletasks()
        self.words_canvas.configure(scrollregion=self.words_canvas.bbox("all"))
        
        canvas_width = self.words_canvas.winfo_width()
        if canvas_width > 1:
            self.words_canvas.configure(scrollregion=self.words_canvas.bbox("all"))

    def on_verify_selection(self, start, end):
        if not self.game_active:
            return
            
        result = backend.validate(self.grid, self.words_remaining, start, end)
        if result["found"]:
            word = result["word"]
            self.words_found.append(word)
            self.words_remaining = [w for w in self.words_remaining if w != word]
            self.board.highlight(result["path"], color="#27ae60")
            self.board.clear_selection()
            self.message_label.config(text=f"¡Excelente! Encontraste '{word}'", fg='#27ae60')
            self.update_stats()
            
            if not self.words_remaining:
                self.message_label.config(text="¡Felicitaciones! ¡Has encontrado todas las palabras!", fg='#27ae60')
                self.game_active = False
        else:
            self.board.clear_with_feedback()
            self.message_label.config(text="No es una palabra válida. Intenta de nuevo.", fg='#e74c3c')

    def on_clear_selection(self):
        self.message_label.config(text="Selección limpiada. Haz clic en las letras para formar una palabra.", fg='#95a5a6')

    def solve_all(self):
        if not self.game_active:
            return
            
        self.message_label.config(text="Resolviendo automáticamente...", fg='#f39c12')
        
        res = backend.solve(self.grid, self.words_remaining)
        for sol in res["solutions"]:
            self.board.highlight(sol["path"], color="#3498db")
            if sol["word"] not in self.words_found:
                self.words_found.append(sol["word"])
        
        self.root.after(2000, self.complete_auto_solve)
    
    def complete_auto_solve(self):
        self.words_found = self.words[:]
        self.words_remaining = []
        
        self.update_stats()
        self.game_active = False
        
        if self.start_time:
            elapsed = int(time.time() - self.start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            self.message_label.config(text=f"¡Juego completado automáticamente en {minutes:02d}:{seconds:02d}!", fg='#3498db')
        else:
            self.message_label.config(text="¡Todas las palabras han sido encontradas automáticamente!", fg='#3498db')

    def volver_al_menu(self):
        self.game_active = False
        if self.volver_callback:
            self.volver_callback()

    def update_word_display(self, text):
        """Callback para actualizar la palabra actual mostrada"""
        if hasattr(self, 'word_display_label'):
            self.word_display_label.config(text=text)