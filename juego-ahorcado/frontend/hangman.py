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
        """Verifica si el backend F# está disponible"""
        if not self.backend_path or not os.path.exists(self.backend_path):
            return False
        
        try:
            # Intentar compilar el proyecto
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
        """Ejecuta un comando en F# y retorna el resultado"""
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
        """Inicia un nuevo juego"""
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
        """Realiza un intento de adivinar una letra usando F#"""
        
        if not self.backend_available:
            return "_ _ _ _ _ _ _ _ _ _ _ _", 6, " Backend F# no disponible"
        
        letter = letter.upper()
        
        if len(letter) != 1 or not letter.isalpha():
            return self.get_current_state()[0], self.get_current_state()[1], "Ingresa una sola letra"
        
        # Usar el comando "guess" de F# con el gameId correcto
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
        """Obtiene el estado actual del juego desde el backend"""
        if not self.backend_available:
            return "_ _ _ _ _ _ _ _ _ _ _ _", 6, []
        
        result = self.run_fsharp_command(["status", self.game_id])
        
        if result and "|" in result:
            parts = result.split("|")
            if len(parts) >= 5:
                masked_word = parts[0]
                remaining_attempts = int(parts[1])
                incorrect_letters = parts[2].split(",") if parts[2] else []
                return masked_word, remaining_attempts, incorrect_letters
        
        return "_ _ _ _ _ _ _ _ _ _ _ _", 6, []
    
    def get_guessed_letters_text(self):
        """Retorna las letras adivinadas para mostrar"""
        if not self.backend_available:
            return "Backend no disponible"
        
        _, _, incorrect_letters = self.get_current_state()
        return ", ".join(sorted(incorrect_letters)) if incorrect_letters else "Ninguna"

class HangmanGame:
    def __init__(self, window):
        self.window = window
        self.client = None
        self.setup_ui()
        self.initialize_game()
    
    def setup_ui(self):
        """Configuracion la interfaz gráfica"""
        self.window.title("🎮 Juego del Ahorcado - F# Backend")
        self.window.geometry("650x750")
        self.window.configure(bg='#2c3e50')
        self.window.resizable(False, False)
        
        self.title_font = ("Arial", 24, "bold")
        self.word_font = ("Courier New", 24, "bold")
        self.button_font = ("Arial", 12, "bold")
        self.label_font = ("Arial", 14)
        self.message_font = ("Arial", 12)
        
        title_label = tk.Label(self.window, text="JUEGO DEL AHORCADO", 
                            font=self.title_font, bg='#2c3e50', fg='#ecf0f1')
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(self.window, text="", 
                                font=("Arial", 10), bg='#2c3e50', fg='#bdc3c7')
        subtitle_label.pack(pady=0)
        
        self.hangman_canvas = tk.Canvas(self.window, width=300, height=300, 
                                    bg='#ecf0f1', highlightthickness=2, highlightbackground='#34495e')
        self.hangman_canvas.pack(pady=10)

        self.word_label = tk.Label(self.window, text="", font=self.word_font, 
                                bg='#2c3e50', fg='#3498db')
        self.word_label.pack(pady=15)

        self.attempts_label = tk.Label(self.window, text="", 
                                    font=self.label_font, bg='#2c3e50', fg='#27ae60')
        self.attempts_label.pack(pady=5)

        input_frame = tk.Frame(self.window, bg='#2c3e50')
        input_frame.pack(pady=15)
        
        tk.Label(input_frame, text="Introduce una letra:", font=self.label_font, 
                bg='#2c3e50', fg='#ecf0f1').pack()
        
        self.letter_entry = tk.Entry(input_frame, font=("Arial", 18), width=4, 
                                justify='center', bg='#ecf0f1', fg='#2c3e50', 
                                insertbackground='#2c3e50')
        self.letter_entry.pack(pady=8)

        self.letter_entry.bind('<Return>', lambda event: self.process_guess())
 
        button_frame = tk.Frame(self.window, bg='#2c3e50')
        button_frame.pack(pady=10)

        self.guess_button = tk.Button(button_frame, text=" Adivinar Letra", 
                                    command=self.process_guess,
                                    font=self.button_font, bg='#3498db', fg='white', 
                                    activebackground='#2980b9', width=15, cursor='hand2')
        self.guess_button.pack(side=tk.LEFT, padx=8)
        
        # Botón Nuevo Juego
        self.reset_button = tk.Button(button_frame, text="🔄 Nuevo Juego", 
                                    command=self.reset_game,
                                    font=self.button_font, bg='#e67e22', fg='white',
                                    activebackground='#d35400', width=15, cursor='hand2')
        self.reset_button.pack(side=tk.LEFT, padx=8)

        self.message_label = tk.Label(self.window, text="", font=self.message_font, 
                                    bg='#2c3e50', fg='#f39c12', wraplength=500)
        self.message_label.pack(pady=8)

        self.guessed_label = tk.Label(self.window, text="", font=("Arial", 11), 
                                    bg='#2c3e50', fg='#bdc3c7', justify='center')
        self.guessed_label.pack(pady=5)

        self.backend_status = tk.Label(self.window, text="", font=("Arial", 9), 
                                    bg='#2c3e50', fg='#95a5a6')
        self.backend_status.pack(pady=5)
    
    def initialize_game(self):
        """Inicializa el juego"""
        backend_path = r"juego-ahorcado\backend"
        
        self.client = HangmanClient(backend_path)

        if self.client.backend_available:
            self.backend_status.config(text="Backend F# fucnionao", fg='#27ae60')
        else:
            self.backend_status.config(text="Backend F# no fucniona", fg='#e74c3c')
        
        self.reset_game()
    
    def reset_game(self):
        """Reinicia el juego"""
        if self.client:
            masked_word, remaining_attempts, message = self.client.start_game()
            self.update_display(masked_word, remaining_attempts, message)
            self.letter_entry.config(state='normal')
            self.letter_entry.delete(0, tk.END)
            self.letter_entry.focus()
    
    def process_guess(self):
        """Procesa un intento de adivinar"""
        if not self.client:
            return
        
        letter = self.letter_entry.get().strip()
        if not letter:
            return
        
        if len(letter) != 1 or not letter.isalpha():
            self.message_label.config(text="Por favor ingresa una sola letra valida", fg='#e74c3c')
            self.letter_entry.delete(0, tk.END)
            return
        
        masked_word, remaining_attempts, message = self.client.make_guess(letter)
        self.update_display(masked_word, remaining_attempts, message)
        self.letter_entry.delete(0, tk.END)

        if "Ganaste" in message or "Perdiste" in message:
            if "Ganaste" in message:
                messagebox.showinfo("¡Felicidades!", message)
            else:
                messagebox.showwarning("Game Over", message)
    
    def update_display(self, masked_word, remaining_attempts, message):
        """Actualiza toda la interfaz"""
        
        self.word_label.config(text=masked_word)

        self.attempts_label.config(text=f"Intentos restantes: {remaining_attempts}")

        color = '#27ae60' if "Bien" in message or "Ganaste" in message else '#e74c3c' if "incorrecta" in message.lower() or "Perdiste" in message else '#f39c12'
        self.message_label.config(text=message, fg=color)

        if self.client:
            guessed_text = self.client.get_guessed_letters_text()
            self.guessed_label.config(text=f"Letras incorrectas: {guessed_text}")

        wrong_attempts = 6 - remaining_attempts
        self.draw_hangman(wrong_attempts)
    
    def draw_hangman(self, wrong_attempts):
        """Dibuja el estado del ahorcado"""
        self.hangman_canvas.delete("all")
        

        self.hangman_canvas.create_line(50, 280, 200, 280, width=4, fill='#8b4513')

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

def main():
    window = tk.Tk()
    game = HangmanGame(window)
    window.mainloop()

if __name__ == "__main__":
    main()