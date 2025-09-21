# --- main_game.py ---
import tkinter as tk
import random


# --- Game settings ---
ROWS = 10
COLS = 10
NUM_MINES = 10

# --- Game state ---
buttons = []
tile_values = [[0 for _ in range(COLS)] for _ in range(ROWS)]
revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
flagged = [[False for _ in range(COLS)] for _ in range(ROWS)]
first_click_done = False
mine_positions = set()

DIRS = [(-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1),  (1, 0), (1, 1)]

def reveal_tile(row, col):
    if not (0 <= row < ROWS and 0 <= col < COLS): return
    if revealed[row][col]: return

    val = tile_values[row][col]
    buttons[row][col].config(text=str(val) if val > 0 else "", bg="lightgrey")
    buttons[row][col].config(state="disabled")
    revealed[row][col] = True

    if val == 0:
        for dr, dc in DIRS:
            reveal_tile(row + dr, col + dc)

def on_tile_click(row, col):
    global first_click_done

    if not first_click_done:
        generate_board(row, col)
        first_click_done = True
        

    if revealed[row][col]: return

    val = tile_values[row][col]

    if val == "M":
        buttons[row][col].config(text="💣", bg="red")
        revealed[row][col] = True
        reveal_all_mines()
        print("💥 Game Over!")
    else:
        reveal_tile(row, col)

def generate_board(safe_row, safe_col):
    global mine_positions

    all_cells = [(r, c) for r in range(ROWS) for c in range(COLS)]
    all_cells.remove((safe_row, safe_col))
    mine_positions = set(random.sample(all_cells, NUM_MINES))

    for r, c in mine_positions:
        tile_values[r][c] = "M"

    for r, c in mine_positions:
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and tile_values[nr][nc] != "M":
                tile_values[nr][nc] += 1

def reveal_all_mines():
    for r, c in mine_positions:
        buttons[r][c].config(text="💣", bg="red")

# --- GUI Setup ---
root = tk.Tk()
root.title("Minesweeper")

frame = tk.Frame(root)
frame.pack()

for row in range(ROWS):
    row_buttons = []
    for col in range(COLS):
        btn = tk.Button(frame, width=4, height=2,
                        command=lambda r=row, c=col: on_tile_click(r, c))
        btn.grid(row=row, column=col)
        row_buttons.append(btn)
    buttons.append(row_buttons)



root.mainloop()
