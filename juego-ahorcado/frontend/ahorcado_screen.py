import subprocess
import os
import tkinter as tk
from tkinter import messagebox

class HangmanClient:
    def __init__(self, backend_path):
        self.backend_path = backend_path
        self.game_id = "default"
        self.backend_available = self._check_backend()
    
    def _check_backend(self):
        if not self.backend_path or not os.path.exists(self.backend_path):
            return False
        
        try:
            result = subprocess.run(
                ["dotnet", "build"],
                capture_output=True,
                text=True,
                cwd=self.backend_path,
                timeout=10
            )
            return result.returncode == 0
        except:
            return False
    
    def run_fsharp_command(self, args):
        if not self.backend_available:
            return None
            
        command = ["dotnet", "run", "--"] + args
        
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                cwd=self.backend_path,
                check=True,
                timeout=5
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error ejecutando F#: {e}")
            print(f"Stderr: {e.stderr}")
            return None
        except Exception as e:
            print(f"Error general: {e}")
            return None
    
    def start_game(self, word=None):
        if not self.backend_available:
            return "_ _ _ _ _ _ _ _ _ _ _ _", 6, " Backend no disponible"

        
        if word:
            result = self.run_fsharp_command(["start", self.game_id, word])
        else:
            result = self.run_fsharp_command(["start", self.game_id])
        
        if result and "|" in result:
            parts = result.split("|")
            if len(parts) >= 3:
                masked_word = parts[0]
                remaining_attempts = int(parts[1])
                message = parts[2]
                return masked_word, remaining_attempts, message
        
        return "_ _ _ _ _ _ _ _ _ _ _ _", 6, " Error comunicándose con el backend"
    
    def make_guess(self, letter):
        
        if not self.backend_available:
            return "_ _ _ _ _ _ _ _ _ _ _ _", 6, " Backend F# no disponible"
        
        letter = letter.upper()
        
        if len(letter) != 1 or not letter.isalpha():
            return self.get_current_state()[0], self.get_current_state()[1], "Ingresa una sola letra"
        
        result = self.run_fsharp_command(["guess", self.game_id, letter])
        
        if result and "|" in result:
            parts = result.split("|")
            if len(parts) >= 3:
                masked_word = parts[0]
                remaining_attempts = int(parts[1])
                message = parts[2]
                return masked_word, remaining_attempts, message
        
        return self.get_current_state()[0], self.get_current_state()[1], " Error comunicándose con el backend"
    
    def get_current_state(self):
        result = self.run_fsharp_command(["state", self.game_id])
        
        if result and "|" in result:
            parts = result.split("|")
            if len(parts) >= 3:
                masked_word = parts[0]
                remaining_attempts = int(parts[1])
                message = parts[2]
                return masked_word, remaining_attempts, message
        
        return "_ _ _ _ _ _ _ _ _ _ _ _", 6, " Error obteniendo el estado del juego"

class AhorcadoScreen:
    def __init__(self, root, volver_callback):
        self.root = root
        self.volver_callback = volver_callback
        self.client = None
        self.root.title("Juego del Ahorcado - Proyecto Lenguajes")
        self.root.geometry("650x750")
        self.root.configure(bg='#2c3e50')
        
        self.title_font = ("Arial", 24, "bold")
        self.word_font = ("Courier New", 24, "bold")
        self.button_font = ("Arial", 12, "bold")
        self.label_font = ("Arial", 14)
        self.message_font = ("Arial", 12)
        
        self.setup_ui()
        self.initialize_game()
    
    def setup_ui(self):
        header_frame = tk.Frame(self.root, bg='#2c3e50')
        header_frame.pack(fill='x', pady=5)
        
        back_btn = tk.Button(header_frame, text="← VOLVER AL MENÚ", 
                            command=self.volver_al_menu,
                            font=("Arial", 10, "bold"), bg='#95a5a6', fg='white',
                            activebackground='#7f8c8d', cursor='hand2')
        back_btn.pack(side='left', padx=10, pady=5)
        
        title_label = tk.Label(self.root, text="JUEGO DEL AHORCADO", 
                            font=self.title_font, bg='#2c3e50', fg='#ecf0f1')
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(self.root, text="Backend F# + Frontend Python", 
                                font=("Arial", 10), bg='#2c3e50', fg='#bdc3c7')
        subtitle_label.pack(pady=0)
        
        self.hangman_canvas = tk.Canvas(self.root, width=300, height=300, 
                                    bg='#ecf0f1', highlightthickness=2, highlightbackground='#34495e')
        self.hangman_canvas.pack(pady=10)

        self.word_label = tk.Label(self.root, text="", font=self.word_font, 
                                bg='#2c3e50', fg='#3498db')
        self.word_label.pack(pady=15)

        self.attempts_label = tk.Label(self.root, text="", 
                                    font=self.label_font, bg='#2c3e50', fg='#27ae60')
        self.attempts_label.pack(pady=5)

        input_frame = tk.Frame(self.root, bg='#2c3e50')
        input_frame.pack(pady=15)
        
        tk.Label(input_frame, text="Introduce una letra:", font=self.label_font, 
                bg='#2c3e50', fg='#ecf0f1').pack()
        
        self.letter_entry = tk.Entry(input_frame, font=("Arial", 18), width=4, 
                                justify='center', bg='#ecf0f1', fg='#2c3e50', 
                                insertbackground='#2c3e50')
        self.letter_entry.pack(pady=8)

        button_frame = tk.Frame(self.root, bg='#2c3e50')
        button_frame.pack(pady=10)

        self.guess_button = tk.Button(button_frame, text="ADIVINAR", 
                                    command=self.make_guess,
                                    font=self.button_font, bg='#3498db', fg='white',
                                    activebackground='#2980b9', cursor='hand2', width=12)
        self.guess_button.pack(side=tk.LEFT, padx=5)

        self.new_game_button = tk.Button(button_frame, text="NUEVO JUEGO", 
                                        command=self.new_game,
                                        font=self.button_font, bg='#e67e22', fg='white',
                                        activebackground='#d35400', cursor='hand2', width=12)
        self.new_game_button.pack(side=tk.LEFT, padx=5)

        self.message_label = tk.Label(self.root, text="", font=self.message_font, 
                                    bg='#2c3e50', fg='#f39c12', wraplength=500, justify='center')
        self.message_label.pack(pady=15)

        self.letter_entry.bind('<Return>', lambda e: self.make_guess())
        self.letter_entry.focus()

    def initialize_game(self):
        backend_path = os.path.join(os.path.dirname(__file__), "..", "backend")
        
        if os.path.exists(backend_path):
            self.client = HangmanClient(backend_path)
            if self.client.backend_available:
                self.new_game()
                self.message_label.config(text="Backend F# conectado correctamente. ¡Comienza a jugar!", fg='#27ae60')
            else:
                self.message_label.config(text="⚠️ Backend F# no disponible. Compilando...", fg='#f39c12')
                self.root.after(2000, self.retry_backend)
        else:
            self.message_label.config(text="❌ No se encontró el backend F#", fg='#e74c3c')

    def retry_backend(self):
        if self.client:
            self.client.backend_available = self.client._check_backend()
            if self.client.backend_available:
                self.new_game()
                self.message_label.config(text="✅ Backend F# ahora disponible. ¡Comienza a jugar!", fg='#27ae60')
            else:
                self.message_label.config(text="❌ Backend F# aún no disponible", fg='#e74c3c')

    def new_game(self):
        if not self.client or not self.client.backend_available:
            self.message_label.config(text="❌ Backend no disponible", fg='#e74c3c')
            return

        try:
            masked_word, attempts, message = self.client.start_game()
            self.update_display(masked_word, attempts, message.strip())
            self.letter_entry.config(state='normal')
            self.guess_button.config(state='normal')
            self.letter_entry.focus()
            
        except Exception as e:
            self.message_label.config(text=f"Error iniciando juego: {str(e)}", fg='#e74c3c')

    def make_guess(self):
        if not self.client or not self.client.backend_available:
            self.message_label.config(text="❌ Backend no disponible", fg='#e74c3c')
            return

        letter = self.letter_entry.get().strip().upper()
        
        if not letter:
            self.message_label.config(text="⚠️ Ingresa una letra", fg='#f39c12')
            return
        
        if len(letter) != 1 or not letter.isalpha():
            self.message_label.config(text="⚠️ Ingresa solo una letra válida", fg='#f39c12')
            self.letter_entry.delete(0, tk.END)
            return

        try:
            masked_word, attempts, message = self.client.make_guess(letter)
            self.update_display(masked_word, attempts, message.strip())
            self.letter_entry.delete(0, tk.END)
            
            if "ganaste" in message.lower() or "perdiste" in message.lower():
                self.letter_entry.config(state='disabled')
                self.guess_button.config(state='disabled')
                
        except Exception as e:
            self.message_label.config(text=f"Error procesando intento: {str(e)}", fg='#e74c3c')

    def update_display(self, masked_word, attempts, message):
        self.word_label.config(text=masked_word)
        self.attempts_label.config(text=f"Intentos restantes: {attempts}")
        
        if "ganaste" in message.lower():
            self.message_label.config(text=f"🎉 {message}", fg='#27ae60')
        elif "perdiste" in message.lower():
            self.message_label.config(text=f"💀 {message}", fg='#e74c3c')
        elif "incorrecto" in message.lower() or "incorrecta" in message.lower():
            self.message_label.config(text=f"❌ {message}", fg='#e74c3c')
        elif "correcto" in message.lower() or "correcta" in message.lower():
            self.message_label.config(text=f"✅ {message}", fg='#27ae60')
        else:
            self.message_label.config(text=message, fg='#f39c12')
        
        wrong_attempts = 6 - attempts
        self.draw_hangman(wrong_attempts)

    def draw_hangman(self, wrong_attempts):
        self.hangman_canvas.delete("all")
        
        self.hangman_canvas.create_line(50, 280, 150, 280, width=6, fill='#34495e')
        
        self.hangman_canvas.create_line(100, 280, 100, 50, width=4, fill='#8b4513')
        
        self.hangman_canvas.create_line(100, 50, 180, 50, width=4, fill='#8b4513')
        
        self.hangman_canvas.create_line(180, 50, 180, 80, width=3, fill='#654321')
        
        
        if wrong_attempts >= 1:
            self.hangman_canvas.create_oval(165, 80, 195, 110, outline='#2c3e50', width=3)
          
            self.hangman_canvas.create_oval(172, 88, 176, 92, fill='#2c3e50')
            self.hangman_canvas.create_oval(184, 88, 188, 92, fill='#2c3e50')
        
        if wrong_attempts >= 2:
            self.hangman_canvas.create_line(180, 110, 180, 180, width=3, fill='#2c3e50')

        if wrong_attempts >= 3:
            self.hangman_canvas.create_line(180, 130, 155, 155, width=3, fill='#2c3e50')

        if wrong_attempts >= 4:
            self.hangman_canvas.create_line(180, 130, 205, 155, width=3, fill='#2c3e50')

        if wrong_attempts >= 5:
            self.hangman_canvas.create_line(180, 180, 160, 210, width=3, fill='#2c3e50')

        if wrong_attempts >= 6:
            self.hangman_canvas.create_line(180, 180, 200, 210, width=3, fill='#2c3e50')
            self.hangman_canvas.create_arc(172, 95, 188, 105, start=0, extent=180, width=2, outline='#e74c3c')

    def volver_al_menu(self):
        if self.volver_callback:
            self.volver_callback()