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
    def __init__(self, root, volver_callback):
        self.root = root
        self.volver_callback = volver_callback
        self.root.title("Sopa de Letras - Proyecto Lenguajes")
        self.root.geometry("1000x1100")
        self.root.configure(bg='#2c3e50')
        
        self.words = load_words()
        self.grid = []
        self.words_remaining = self.words[:]
        self.words_found = []
        self.start_time = None
        self.game_active = False
        
        self.title_font = ("Arial", 24, "bold")
        self.word_font = ("Arial", 14, "bold")
        self.button_font = ("Arial", 12, "bold")
        self.label_font = ("Arial", 12)
        self.stats_font = ("Arial", 11)
        
        self.setup_ui()
        self.new_game()

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

        self.board = Board(self.root, on_verify_callback=self.on_verify_selection, on_clear_callback=self.on_clear_selection)
        
        button_frame = tk.Frame(self.root, bg='#2c3e50')
        button_frame.pack(pady=15)
        
        self.new_game_btn = tk.Button(button_frame, text="Nuevo Juego", 
                                    command=self.new_game,
                                    font=self.button_font, bg='#e67e22', fg='white',
                                    activebackground='#d35400', width=15, cursor='hand2')
        self.new_game_btn.pack(side=tk.LEFT, padx=10)
        
        self.solve_btn = tk.Button(button_frame, text="Resolver", command=self.solve_all,
                                    font=self.button_font, bg='#9b59b6', fg='white', 
                                    activebackground='#8e44ad', width=15, cursor='hand2')
        self.solve_btn.pack(side=tk.LEFT, padx=10)
        
        self.message_label = tk.Label(self.root, text="", font=self.label_font, 
                                    bg='#2c3e50', fg='#f39c12', wraplength=600)
        self.message_label.pack(pady=8)
        
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
        resp = backend.generate(self.words, size=12)
        self.grid = resp["grid"]
        self.words_remaining = self.words[:]
        self.words_found = []
        self.start_time = time.time()
        self.game_active = True
        
        self.board.draw(self.grid)
        self.update_stats()
        self.message_label.config(text="¡Encuentra todas las palabras! Haz clic en las letras para formar palabras y presiona VERIFICAR.", fg='#f39c12')

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