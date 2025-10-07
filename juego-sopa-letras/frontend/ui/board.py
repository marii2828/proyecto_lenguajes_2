import tkinter as tk

class Board:
    def __init__(self, parent_frame, on_verify_callback, on_clear_callback, on_word_update_callback=None):
        self.parent_frame = parent_frame
        self.frame = tk.Frame(parent_frame, bg='#2c3e50')
        self.on_verify = on_verify_callback
        self.on_clear = on_clear_callback
        self.on_word_update = on_word_update_callback
        self.buttons = []
        self.size = 0
        self.selected_letters = []
        self.selection_colors = ['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71', '#3498db', '#9b59b6', '#e67e22', '#95a5a6']

    def get_frame(self):
        return self.frame

    def get_screen_dimensions(self):
        try:
            screen_width = self.parent_frame.winfo_screenwidth()
            screen_height = self.parent_frame.winfo_screenheight()
        except:
            screen_width, screen_height = 1920, 1080  # Default
        return screen_width, screen_height

    def calculate_responsive_dimensions(self, grid_size):
        screen_width, screen_height = self.get_screen_dimensions()
        
        available_width = int(screen_width * 0.75)
        available_height = int(screen_height * 0.65)
        
        max_button_space = min(available_width // grid_size, available_height // grid_size)
        
        base_size = max(15, min(60, max_button_space))
        
        button_width = max(1, base_size // 12)
        button_height = max(1, base_size // 24)
        
        if grid_size <= 12:
            font_size = max(8, min(16, base_size // 3))
            padding = max(1, base_size // 12)
        elif grid_size <= 16:
            font_size = max(6, min(14, base_size // 4))
            padding = max(1, base_size // 15)
        else:
            font_size = max(5, min(12, base_size // 5))
            padding = max(1, base_size // 18)
        
        return button_width, button_height, font_size, padding

    def draw(self, grid):
        for w in self.frame.winfo_children():
            w.destroy()

        self.buttons.clear()
        self.selected_letters.clear()
        self.size = len(grid)
        
        button_width, button_height, font_size, padding = self.calculate_responsive_dimensions(self.size)
        
        for r, row in enumerate(grid):
            row_btns = []
            for c, ch in enumerate(row):
                b = tk.Button(self.frame, text=ch, 
                            width=button_width, 
                            height=button_height,
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
            display_text = f"Palabra: {word}"
        else:
            display_text = "Palabra: "
        
        if self.on_word_update:
            self.on_word_update(display_text)

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