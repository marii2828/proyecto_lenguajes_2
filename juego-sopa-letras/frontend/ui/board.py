import tkinter as tk

class Board:
    def __init__(self, root, on_verify_callback, on_clear_callback):
        self.frame = tk.Frame(root, bg='#2c3e50')
        self.frame.pack(pady=10)
        self.on_verify = on_verify_callback
        self.on_clear = on_clear_callback
        self.buttons = []
        self.size = 0
        self.selected_letters = []
        self.selection_colors = ['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71', '#3498db', '#9b59b6', '#e67e22', '#95a5a6']
        
        self.control_frame = tk.Frame(root, bg='#2c3e50')
        self.control_frame.pack(pady=5)
        
        self.verify_btn = tk.Button(self.control_frame, text="VERIFICAR", 
                                    font=("Arial", 14, "bold"), bg='#27ae60', fg='white',
                                    activebackground='#2ecc71', cursor='hand2',
                                    command=self.verify_selection)
        self.verify_btn.pack(side=tk.LEFT, padx=10)
        
        self.clear_btn = tk.Button(self.control_frame, text="LIMPIAR", 
                                    font=("Arial", 14, "bold"), bg='#e74c3c', fg='white',
                                    activebackground='#c0392b', cursor='hand2',
                                    command=self.clear_selection)
        self.clear_btn.pack(side=tk.LEFT, padx=10)
        
        self.word_label = tk.Label(root, text="Palabra: ", 
                                    font=("Arial", 16, "bold"), bg='#2c3e50', fg='#ecf0f1')
        self.word_label.pack(pady=5)

    def draw(self, grid):
        for w in self.frame.winfo_children():
            w.destroy()

        self.buttons.clear()
        self.selected_letters.clear()
        self.size = len(grid)
        
        # Ajustar tamaño de botones según el tamaño del tablero
        if self.size <= 12:
            button_width = 3
            button_height = 1
            font_size = 16
            padding = 2
        elif self.size <= 16:
            button_width = 2
            button_height = 1
            font_size = 14
            padding = 1
        else:  # 17-20
            button_width = 2
            button_height = 1
            font_size = 12
            padding = 1

        for r, row in enumerate(grid):
            row_btns = []
            for c, ch in enumerate(row):
                b = tk.Button(self.frame, text=ch, 
                            width=button_width, height=button_height,
                            font=("Consolas", font_size, "bold"),
                            bg='#ecf0f1', fg='#2c3e50',
                            activebackground='#bdc3c7',
                            relief='raised', bd=2,
                            cursor='hand2')
                
                b.bind('<Button-1>', lambda e, r=r, c=c: self.on_letter_click(r, c))
                
                b.grid(row=r, column=c, padx=padding, pady=padding)
                row_btns.append(b)
            self.buttons.append(row_btns)
        
        self.update_word_display()

    def on_letter_click(self, r, c):
        coord = {"r": r, "c": c}
        
        if coord in self.selected_letters:
            index = self.selected_letters.index(coord)
            removed_letters = self.selected_letters[index:]
            self.selected_letters = self.selected_letters[:index]
            
            for letter_coord in removed_letters:
                btn = self.buttons[letter_coord["r"]][letter_coord["c"]]
                if btn['state'] != 'disabled':
                    current_text = btn.cget('text')
                    if '\n' in current_text:
                        original_text = current_text.split('\n')[0]
                    else:
                        original_text = ''.join(char for char in current_text if char.isalpha())
                        if not original_text:
                            original_text = current_text[0] if current_text else 'A'
                    
                    btn.config(bg='#ecf0f1', fg='#2c3e50', text=original_text)
            
            self.renumber_selected_letters()
        else:
            self.selected_letters.append(coord)
            
            color_index = (len(self.selected_letters) - 1) % len(self.selection_colors)
            color = self.selection_colors[color_index]
            
            btn = self.buttons[r][c]
            original_text = btn.cget('text').split('\n')[0]
            
            number = str(len(self.selected_letters))
            display_text = f"{original_text}\n{number}"
            
            btn.config(bg=color, fg='white', text=display_text)
            
        self.update_word_display()

    def renumber_selected_letters(self):
        for i, coord in enumerate(self.selected_letters):
            if coord:
                btn = self.buttons[coord["r"]][coord["c"]]
                if btn['state'] != 'disabled':
                    current_text = btn.cget('text')
                    if '\n' in current_text:
                        original_text = current_text.split('\n')[0]
                    else:
                        original_text = ''.join(char for char in current_text if char.isalpha())
                        if not original_text:
                            original_text = current_text[0] if current_text else 'A'
                    
                    color_index = i % len(self.selection_colors)
                    color = self.selection_colors[color_index]
                    
                    number = str(i + 1)
                    display_text = f"{original_text}\n{number}"
                    
                    btn.config(bg=color, fg='white', text=display_text)

    def update_word_display(self):
        if self.selected_letters:
            word = ""
            for coord in self.selected_letters:
                btn = self.buttons[coord["r"]][coord["c"]]
                letter = btn.cget('text').split('\n')[0]
                word += letter
            self.word_label.config(text=f"Palabra: {word}")
        else:
            self.word_label.config(text="Palabra: ")

    def verify_selection(self):
        if len(self.selected_letters) < 2:
            return
        
        start = self.selected_letters[0]
        end = self.selected_letters[-1]
        
        if not self.is_straight_line(self.selected_letters):
            self.clear_with_feedback()
            return
        
        self.on_verify(start, end)

    def clear_selection(self):
        for coord in self.selected_letters:
            btn = self.buttons[coord["r"]][coord["c"]]
            if btn['state'] != 'disabled':
                current_text = btn.cget('text')
                if '\n' in current_text:
                    original_text = current_text.split('\n')[0]
                else:
                    original_text = ''.join(char for char in current_text if char.isalpha())
                    if not original_text:
                        original_text = current_text[0] if current_text else 'A'
                
                btn.config(bg='#ecf0f1', fg='#2c3e50', text=original_text)
        
        self.selected_letters.clear()
        self.update_word_display()
        self.on_clear()

    def clear_with_feedback(self):
        for coord in self.selected_letters:
            btn = self.buttons[coord["r"]][coord["c"]]
            if btn['state'] != 'disabled':
                btn.config(bg='#e74c3c', fg='white')
        
        self.word_label.after(500, self.clear_selection)

    def is_straight_line(self, coords):
        if len(coords) < 2:
            return True
        
        dr = coords[1]["r"] - coords[0]["r"]
        dc = coords[1]["c"] - coords[0]["c"]
        
        if dr != 0:
            dr = dr // abs(dr)
        if dc != 0:
            dc = dc // abs(dc)
        
        for i in range(1, len(coords)):
            expected_r = coords[0]["r"] + i * dr
            expected_c = coords[0]["c"] + i * dc
            
            if coords[i]["r"] != expected_r or coords[i]["c"] != expected_c:
                return False
        
        return True

    def highlight(self, path, color="#27ae60"):
        for coord in path:
            btn = self.buttons[coord["r"]][coord["c"]]
            btn.config(bg=color, fg='white', state='disabled')