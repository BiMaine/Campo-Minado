import tkinter as tk
import random

GRID_SIZE = 10
NUM_MINES = 15
BUTTON_SIZE = 60
FONT_SIZE = 20

WINDOW_WIDTH = GRID_SIZE * BUTTON_SIZE
WINDOW_HEIGHT = GRID_SIZE * BUTTON_SIZE + 80

class MineSweeper:
    def __init__(self, root):
        self.root = root
        self.root.title("Campo Minado")
        
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        
        self.root.resizable(False, False)
        
        self.buttons = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.minefield = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.generate_minefield()
        
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                self.buttons[row][col] = tk.Button(root, width=3, height=1, font=("Arial", FONT_SIZE), bg="lightgray", command=lambda row=row, col=col: self.click(row, col))
                self.buttons[row][col].grid(row=row, column=col, padx=1, pady=1)
        
        restart_button = tk.Button(root, text="Reiniciar Jogo", font=("Arial", FONT_SIZE), bg="lightgreen", command=self.restart_game)
        restart_button.grid(row=GRID_SIZE, column=0, columnspan=GRID_SIZE, sticky="nsew")

        exit_button = tk.Button(root, text="Sair", font=("Arial", FONT_SIZE), bg="tomato", command=root.quit)
        exit_button.grid(row=GRID_SIZE + 1, column=0, columnspan=GRID_SIZE, sticky="nsew")
        
        self.game_over = False

    def generate_minefield(self):
        mines_placed = 0
        while mines_placed < NUM_MINES:
            row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            if self.minefield[row][col] != -1:
                self.minefield[row][col] = -1
                mines_placed += 1
        
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.minefield[row][col] == -1:
                    continue
                count = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        r, c = row + dr, col + dc
                        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and self.minefield[r][c] == -1:
                            count += 1
                self.minefield[row][col] = count
        
    def click(self, row, col):
        if self.game_over:
            return
        
        if self.minefield[row][col] == -1:
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    if self.minefield[r][c] == -1:
                        self.buttons[r][c].config(text='*', state=tk.DISABLED, bg="red")
                    else:
                        self.buttons[r][c].config(state=tk.DISABLED)
            self.root.title("Campo Minado - Você perdeu!")
            self.game_over = True
        elif self.minefield[row][col] == 0:
            self.reveal_empty_cells(row, col)
        else:
            self.buttons[row][col].config(text=str(self.minefield[row][col]), state=tk.DISABLED, bg="lightblue")
    
    def reveal_empty_cells(self, row, col):
        if row < 0 or row >= GRID_SIZE or col < 0 or col >= GRID_SIZE or self.minefield[row][col] != 0:
            return
        if self.buttons[row][col]['state'] == tk.NORMAL:
            self.buttons[row][col].config(state=tk.DISABLED, bg="lightblue")
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    self.reveal_empty_cells(row + dr, col + dc)

    def restart_game(self):
        self.root.destroy()
        new_root = tk.Tk()
        game = MineSweeper(new_root)
        new_root.mainloop()

def main():
    root = tk.Tk()
    game = MineSweeper(root)
    root.mainloop()

if __name__ == "__main__":
    main()