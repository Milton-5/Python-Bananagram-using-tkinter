import tkinter as tk
import random
from tkinter import messagebox

import nltk


try:
    from nltk.corpus import words as nltk_words
except LookupError:
    nltk.download('words')
    from nltk.corpus import words as nltk_words

english_words = set(word.upper() for word in nltk_words.words())



tile_distribution = {
    "A": 99, "B": 99, "C": 99, "D": 99, "E": 99, "F": 99, "G": 99,
    "H": 99, "I": 99, "J": 99, "K": 99, "L": 99, "M": 99, "N": 99,
    "O": 99, "P": 99, "Q": 99, "R": 99, "S": 99, "T": 99, "U": 99,
    "V": 99, "W": 99, "X": 99, "Y": 99, "Z": 99
}


all_tiles = [letter for letter, count in tile_distribution.items() for _ in range(count)]
random.shuffle(all_tiles)

cell_size = 30
grid_size = 25
canvas_width = 450
canvas_height = 450
small_canvas_width = 630
small_canvas_height = cell_size
selected_letter = None
placed_letters = []
matched_words = set()
score = 0
more_character_count = 0
max_more_character_uses = 4
total_letters_on_board = 0
max_letters_on_board = 144
game_over = False

root = tk.Tk()
root.title("Bananagram Game")
root.configure(bg="#BEE8F5")

title_label = tk.Label(root, text="\U0001F34C Bananagram \U0001F34C", font=("Comic Sans MS", 28, "bold"), bg="#BEE8F5", fg="#3B2F2F")
title_label.pack(pady=10)

canvas_frame = tk.Frame(root, bg="#F7F1E5")
canvas_frame.pack()

canvas = tk.Canvas(canvas_frame, width=canvas_width, height=canvas_height,
                   bg="#F7F9A0", highlightthickness=2, highlightbackground="black")
canvas.pack()

prompt_label = tk.Label(root, text="Drag and place letters to form words", font=("Verdana", 16, "italic"), bg="#BEE8F5")
prompt_label.pack(pady=5)

small_canvas = tk.Canvas(root, width=small_canvas_width, height=small_canvas_height,
                         bg="#FDEBD0", highlightthickness=2, highlightbackground="#8B7E66")
small_canvas.pack(pady=5)

score_var = tk.StringVar(value="Score: 0")
score_label = tk.Label(root, textvariable=score_var, font=("Arial", 16, "bold"), bg="#BEE8F5", fg="#5D3A00")
score_label.pack(pady=10)

time_left = 120 
time=time_left
timer_var = tk.StringVar(value="Time Left: 02:00")
timer_label = tk.Label(root, textvariable=timer_var, font=("Arial", 16, "bold"), bg="#BEE8F5", fg="#D32F2F")
timer_label.pack(pady=5)
timer_id = None

def update_timer():
    global time_left, game_over, timer_id
    if time_left > 0 and not game_over:
        time_left -= 1
        minutes = time_left // 60
        seconds = time_left % 60
        timer_var.set(f"Time Left: {minutes:02}:{seconds:02}")
        timer_id = root.after(1000, update_timer)
    elif not game_over:
        timer_var.set("Time Left: 00:00")
        match_words()

 

def draw_grid(canvas, width, height, grid_size):
    for i in range(0, width, grid_size):
        canvas.create_line([(i, 0), (i, height)], fill='#C4A484')
    for i in range(0, height, grid_size):
        canvas.create_line([(0, i), (width, i)], fill='#C4A484')

def draw_small_grid(canvas, width, height, grid_size):
    for i in range(0, width, grid_size):
        canvas.create_line(i, 0, i, height, fill='#8B7E66')


def populate_small_grid():
    global more_character_count
    if more_character_count >= max_more_character_uses:
        messagebox.showwarning("Limit Reached", f"You've used all {max_more_character_uses} More Character chances!")

        return

    small_canvas.delete("all")
    draw_small_grid(small_canvas, small_canvas_width, small_canvas_height, cell_size)

    if not all_tiles:
        messagebox.showinfo("No More Tiles", "You've used up all the tiles!")
        return

    more_character_count += 1
    update_more_character_button_text()

    max_tiles = small_canvas_width // cell_size
    tiles_to_draw = min(max_tiles, len(all_tiles))

    for i in range(tiles_to_draw):
        letter = all_tiles.pop()
        x = i * cell_size + cell_size // 2
        y = small_canvas_height // 2
        small_canvas.create_text(x, y, text=letter, font=("Arial", 14, "bold"), tags=f"letter_{i}", fill="#3B2F2F")

def update_more_character_button_text():
    more_char_button.config(text=f"More Character ({more_character_count}/{max_more_character_uses})")

def select_letter(event):
    global selected_letter
    if game_over:
        return 
    if selected_letter:
        messagebox.showwarning("Letter Already Selected", "Place the current letter on the board before picking another.")
        return
    canvas_item = small_canvas.find_closest(event.x, event.y)
    tags = small_canvas.gettags(canvas_item)
    if tags and tags[0].startswith("letter_"):
        selected_letter = small_canvas.itemcget(canvas_item, "text")
        small_canvas.delete(canvas_item)


def place_letter(event):
    global selected_letter, total_letters_on_board
    if game_over:
        return
    if selected_letter:
        if total_letters_on_board >= max_letters_on_board:
            messagebox.showinfo("Limit Reached", "Maximum 144 letters placed!")
            return
        x_grid = event.x // grid_size
        y_grid = event.y // grid_size
        x = x_grid * grid_size + grid_size // 2
        y = y_grid * grid_size + grid_size // 2
        overlapping_items = canvas.find_overlapping(x - grid_size // 2 + 1, y - grid_size // 2 + 1, x + grid_size // 2 - 1, y + grid_size // 2 - 1)
        for item in overlapping_items:
            if "placed_letter" in canvas.gettags(item):
                messagebox.showwarning("Cell Occupied", "This cell already has a letter!")
                return
        letter_id = canvas.create_text(x, y, text=selected_letter, font=("Arial", 15, "bold"), tags="placed_letter", fill="#2F4F4F")
        placed_letters.append((letter_id, selected_letter))
        selected_letter = None
        total_letters_on_board += 1


def withdraw_letter(event):
    global selected_letter, total_letters_on_board
    if game_over:
        return
    clicked_items = canvas.find_overlapping(event.x, event.y, event.x, event.y)
    for item in clicked_items:
        if "placed_letter" in canvas.gettags(item):
            letter = canvas.itemcget(item, "text")
            for i in range(small_canvas_width // cell_size):
                x = i * cell_size + cell_size // 2
                y = small_canvas_height // 2
                items = small_canvas.find_overlapping(x - 10, y - 10, x + 10, y + 10)
                if not items:
                    canvas.delete(item)
                    small_canvas.create_text(x, y, text=letter, font=("Arial", 14, "bold"), tags=f"letter_{i}", fill="#3B2F2F")
                    total_letters_on_board -= 1
                    return
            messagebox.showinfo("No Space", "No empty slot available to restore the letter.")

def dump_tile():
    global selected_letter
    if not selected_letter:
        messagebox.showinfo("No Letter", "Select a letter to dump first.")
        return
    if len(all_tiles) == 0:
        messagebox.showinfo("No Tiles Left", "No tiles left to draw.")
        return

 
    empty_slots = 0
    for i in range(small_canvas_width // cell_size):
        x = i * cell_size + cell_size // 2
        y = small_canvas_height // 2
        items = small_canvas.find_overlapping(x - 10, y - 10, x + 10, y + 10)
        if not items:
            empty_slots += 1

    if empty_slots < 2:
        messagebox.showwarning("Not Enough Space", "You need at least 2 empty slots in the rack to dump a tile.")
        return

 
    new_tiles = []
    for _ in range(3):
        if all_tiles:
            new_tiles.append(all_tiles.pop())
        else:
            break

    selected_letter = None
    add_tiles_to_small_canvas(new_tiles)


def peel_tile():

    rack_items = small_canvas.find_all()
    if rack_items:
        
        for item in rack_items:
            if small_canvas.type(item) == "text":
                messagebox.showinfo("Finish Rack", "Use all rack letters before peeling!")
                return

    if all_tiles:
        letter = all_tiles.pop()
        add_tiles_to_small_canvas(letter)
    else:
        messagebox.showinfo("Game Over", "No more tiles left! Game finished.")

def add_tiles_to_small_canvas(letters):
    for letter in letters:
        for i in range(small_canvas_width // cell_size):
            x = i * cell_size + cell_size // 2
            y = small_canvas_height // 2
            items = small_canvas.find_overlapping(x - 10, y - 10, x + 10, y + 10)
            if not items:
                small_canvas.create_text(x, y, text=letter, font=("Arial", 14, "bold"), tags=f"letter_{len(small_canvas.find_all())}", fill="#3B2F2F")
                break

def match_words():
    global score
    canvas.delete("highlight")  

    big_grid_letters = {}
    for item in canvas.find_withtag("placed_letter"):
        coords = canvas.coords(item)
        x, y = int(coords[0] // grid_size), int(coords[1] // grid_size)
        letter = canvas.itemcget(item, "text")
        big_grid_letters[(x, y)] = letter

    found_words = []
    matched_coords = []
    max_cols = canvas_width // grid_size
    max_rows = canvas_height // grid_size

    # Check horizontally
    for y in range(max_rows):
        word = ""
        coords = []
        for x in range(max_cols):
            if (x, y) in big_grid_letters:
                word += big_grid_letters[(x, y)]
                coords.append((x, y))
            else:
                if len(word) > 1 and word in english_words and word not in matched_words:
                    matched_words.add(word)
                    found_words.append(word)
                    matched_coords.append(coords.copy())
                word = ""
                coords = []
        if len(word) > 1 and word in english_words and word not in matched_words:
            matched_words.add(word)
            found_words.append(word)
            matched_coords.append(coords.copy())

    # Check vertically
    for x in range(max_cols):
        word = ""
        coords = []
        for y in range(max_rows):
            if (x, y) in big_grid_letters:
                word += big_grid_letters[(x, y)]
                coords.append((x, y))
            else:
                if len(word) > 1 and word in english_words and word not in matched_words:
                    matched_words.add(word)
                    found_words.append(word)
                    matched_coords.append(coords.copy())
                word = ""
                coords = []
        if len(word) > 1 and word in english_words and word not in matched_words:
            matched_words.add(word)
            found_words.append(word)
            matched_coords.append(coords.copy())

    if found_words:
      
        for word_coords in matched_coords:
            for x, y in word_coords:
                x0, y0 = x * grid_size, y * grid_size
                x1, y1 = x0 + grid_size, y0 + grid_size
                canvas.create_rectangle(x0, y0, x1, y1, outline="#B22222", width=2, tags="highlight")

        total_letters = sum(len(w) for w in found_words)
        score += total_letters
        score_var.set(f"Score: {score}")
        messagebox.showinfo("Match Found", f"Matched Words: {', '.join(found_words)}\n+{total_letters} points!")
    else:
        messagebox.showinfo("No Match", "No new words matched!")

    global game_over
    game_over = True
    messagebox.showinfo("Game Over", "Banana submitted! No more letters can be placed.")
    peel_button.config(state="disabled")
    dump_button.config(state="disabled")
    banana_button.config(state="disabled")
    more_char_button.config(state="disabled")

def reset_game():
    global selected_letter, placed_letters, matched_words, score, more_character_count
    global total_letters_on_board, game_over, all_tiles, time_left, timer_id

    if timer_id:
        root.after_cancel(timer_id)  # ⬅️ Cancel old timer if running

    selected_letter = None
    placed_letters.clear()
    matched_words.clear()
    score = 0
    more_character_count = 0
    total_letters_on_board = 0
    game_over = False

    all_tiles = [letter for letter, count in tile_distribution.items() for _ in range(count)]
    random.shuffle(all_tiles)

    canvas.delete("all")
    draw_grid(canvas, canvas_width, canvas_height, grid_size)

    small_canvas.delete("all")
    draw_small_grid(small_canvas, small_canvas_width, small_canvas_height, cell_size)

    score_var.set("Score: 0")
    update_more_character_button_text()

    peel_button.config(state="normal")
    dump_button.config(state="normal")
    banana_button.config(state="normal")
    more_char_button.config(state="normal")

    time_left = time
    timer_var.set(f"Time Left: 02:00")
    update_timer()

    root.after(100, populate_small_grid)

canvas.bind("<Button-1>", place_letter)
canvas.bind("<Button-3>", withdraw_letter)
small_canvas.bind("<Button-1>", select_letter)

button_frame = tk.Frame(root, bg="#BEE8F5")
button_frame.pack(pady=10)
reset_button = tk.Button(button_frame, text="Reset", font=("Arial", 14), command=reset_game, bg="#F4D03F", width=10)
reset_button.pack(side=tk.LEFT, padx=10)

peel_button = tk.Button(button_frame, text="Peel", font=("Arial", 14), command=peel_tile, bg="#85C1E9", width=10)
peel_button.pack(side=tk.LEFT, padx=10)

dump_button = tk.Button(button_frame, text="Dump", font=("Arial", 14), command=dump_tile, bg="#F1948A", width=10)
dump_button.pack(side=tk.LEFT, padx=10)

banana_button = tk.Button(button_frame, text="Banana", font=("Arial", 14), command=match_words, bg="#58D68D", width=10)
banana_button.pack(side=tk.LEFT, padx=15)

more_char_button = tk.Button(button_frame, text="More Character (0/7)", font=("Arial", 14), command=populate_small_grid, bg="#EBB373", width=18)
more_char_button.pack(side=tk.LEFT, padx=10)

update_timer()

draw_grid(canvas, canvas_width, canvas_height, grid_size)
root.after(100, populate_small_grid)
root.mainloop()
