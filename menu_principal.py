import tkinter as tk
from tkinter import messagebox
import os
import sys

class MenuPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Menú de Juegos - Proyecto Lenguajes")
        self.root.geometry("800x800")
        self.root.configure(bg='#2c3e50')
        self.root.resizable(False, False)
        
        self.title_font = ("Arial", 28, "bold")
        self.subtitle_font = ("Arial", 16)
        self.button_font = ("Arial", 14, "bold")
        self.description_font = ("Arial", 12)
        
        self.setup_menu()
        
    def setup_menu(self):
        title_label = tk.Label(self.root, text=" MENÚ DE JUEGOS ", 
                                font=self.title_font, bg='#2c3e50', fg='#ecf0f1')
        title_label.pack(pady=30)
        
        subtitle_label = tk.Label(self.root, text="Selecciona el juego que deseas jugar", 
                                font=self.subtitle_font, bg='#2c3e50', fg='#bdc3c7')
        subtitle_label.pack(pady=10)
        
        games_frame = tk.Frame(self.root, bg='#2c3e50')
        games_frame.pack(pady=40, expand=True)
        
        sopa_frame = tk.Frame(games_frame, bg='#34495e', relief='raised', bd=3)
        sopa_frame.pack(side=tk.LEFT, padx=30, pady=20, fill='both', expand=True)
        
        sopa_title = tk.Label(sopa_frame, text="🧩 SOPA DE LETRAS", 
                                font=("Arial", 18, "bold"), bg='#34495e', fg='#3498db')
        sopa_title.pack(pady=15)
        
        sopa_desc = tk.Label(sopa_frame, text="Encuentra todas las palabras\nocultadas en la grilla de letras.\n\n• Personaliza el tamaño del tablero\n• Interfaz adaptable a tu pantalla\n• Selecciona letras secuencialmente\n• Verifica tus palabras", 
                            font=self.description_font, bg='#34495e', fg='#ecf0f1',
                            justify='center')
        sopa_desc.pack(pady=10)
        
        sopa_btn = tk.Button(sopa_frame, text="JUGAR SOPA DE LETRAS", 
                            command=self.abrir_sopa_letras,
                            font=self.button_font, bg='#3498db', fg='white',
                            activebackground='#2980b9', cursor='hand2',
                            width=20, pady=10)
        sopa_btn.pack(pady=20)
        
        ahorcado_frame = tk.Frame(games_frame, bg='#34495e', relief='raised', bd=3)
        ahorcado_frame.pack(side=tk.RIGHT, padx=30, pady=20, fill='both', expand=True)
        
        ahorcado_title = tk.Label(ahorcado_frame, text="🎯 AHORCADO", 
                                    font=("Arial", 18, "bold"), bg='#34495e', fg='#e74c3c')
        ahorcado_title.pack(pady=15)
        
        ahorcado_desc = tk.Label(ahorcado_frame, text="Adivina la palabra oculta\nantes de que se complete el dibujo.\n\n• Adivina letra por letra\n• Tienes intentos limitados\n• ¡Salva al ahorcado!", 
                                font=self.description_font, bg='#34495e', fg='#ecf0f1',
                                justify='center')
        ahorcado_desc.pack(pady=10)
        
        ahorcado_btn = tk.Button(ahorcado_frame, text="JUGAR AHORCADO", 
                                command=self.abrir_ahorcado,
                                font=self.button_font, bg='#e74c3c', fg='white',
                                activebackground='#c0392b', cursor='hand2',
                                width=20, pady=10)
        ahorcado_btn.pack(pady=20)
        
        footer_frame = tk.Frame(self.root, bg='#2c3e50')
        footer_frame.pack(side='bottom', pady=20)
        
        exit_btn = tk.Button(footer_frame, text="SALIR", 
                            command=self.salir_aplicacion,
                            font=self.button_font, bg='#95a5a6', fg='white',
                            activebackground='#7f8c8d', cursor='hand2',
                            width=10)
        exit_btn.pack()
    
    def abrir_sopa_letras(self):
        # Crear ventana de diálogo para solicitar tamaño
        size_window = tk.Toplevel(self.root)
        size_window.title("Configuración de Sopa de Letras")
        size_window.geometry("400x400")
        size_window.configure(bg='#2c3e50')
        size_window.resizable(False, False)
        size_window.transient(self.root)
        size_window.grab_set()
        
        # Centrar la ventana
        size_window.geometry("+{}+{}".format(
            self.root.winfo_rootx() + 200,
            self.root.winfo_rooty() + 150
        ))
        
        # Título
        title_label = tk.Label(size_window, text="CONFIGURAR SOPA DE LETRAS", 
                              font=("Arial", 16, "bold"), bg='#2c3e50', fg='#ecf0f1')
        title_label.pack(pady=20)
        
        # Instrucciones
        inst_label = tk.Label(size_window, text="Selecciona el tamaño del tablero:", 
                             font=("Arial", 12), bg='#2c3e50', fg='#bdc3c7')
        inst_label.pack(pady=10)
        
        # Frame para el selector
        selector_frame = tk.Frame(size_window, bg='#34495e', relief='raised', bd=2)
        selector_frame.pack(pady=20, padx=40, fill='x')
        
        # Variable para el tamaño
        size_var = tk.IntVar(value=15)
        
        # Slider para seleccionar tamaño
        size_label = tk.Label(selector_frame, text="Tamaño del tablero:", 
                             font=("Arial", 11, "bold"), bg='#34495e', fg='#ecf0f1')
        size_label.pack(pady=10)
        
        size_scale = tk.Scale(selector_frame, from_=10, to=20, orient='horizontal',
                             variable=size_var, font=("Arial", 10), bg='#34495e', fg='#ecf0f1',
                             activebackground='#3498db', highlightbackground='#34495e',
                             length=250, tickinterval=2)
        size_scale.pack(pady=10)
        
        # Label para mostrar el tamaño seleccionado
        size_display = tk.Label(selector_frame, text=f"Tablero: {size_var.get()}x{size_var.get()}", 
                               font=("Arial", 12, "bold"), bg='#34495e', fg='#3498db')
        size_display.pack(pady=5)
        
        # Función para actualizar el display
        def update_size_display(*args):
            size_display.config(text=f"Tablero: {size_var.get()}x{size_var.get()}")
        
        size_var.trace('w', update_size_display)
        
        # Botones
        button_frame = tk.Frame(size_window, bg='#2c3e50')
        button_frame.pack(pady=20)
        
        def iniciar_juego():
            selected_size = size_var.get()
            size_window.destroy()
            
            import sys
            sopa_path = os.path.join(os.path.dirname(__file__), "juego-sopa-letras", "frontend")
            sys.path.append(sopa_path)
            
            from sopa_letras_screen import SopaLetrasScreen
            
            for widget in self.root.winfo_children():
                widget.destroy()
            
            sopa_screen = SopaLetrasScreen(self.root, self.volver_al_menu, board_size=selected_size)
        
        def cancelar():
            size_window.destroy()
        
        start_btn = tk.Button(button_frame, text="INICIAR JUEGO", 
                             command=iniciar_juego,
                             font=("Arial", 12, "bold"), bg='#3498db', fg='white',
                             activebackground='#2980b9', cursor='hand2',
                             width=12, pady=5)
        start_btn.pack(side='left', padx=10)
        
        cancel_btn = tk.Button(button_frame, text="CANCELAR", 
                              command=cancelar,
                              font=("Arial", 12, "bold"), bg='#95a5a6', fg='white',
                              activebackground='#7f8c8d', cursor='hand2',
                              width=12, pady=5)
        cancel_btn.pack(side='left', padx=10)
    
    def abrir_ahorcado(self):
        import sys
        ahorcado_path = os.path.join(os.path.dirname(__file__), "juego-ahorcado", "frontend")
        sys.path.append(ahorcado_path)
        
        from ahorcado_screen import AhorcadoScreen
        
        for widget in self.root.winfo_children():
            widget.destroy()
        
        ahorcado_screen = AhorcadoScreen(self.root, self.volver_al_menu)
    
    def volver_al_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.setup_menu()
    
    def salir_aplicacion(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    menu = MenuPrincipal(root)
    root.mainloop()