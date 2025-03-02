import random
from PIL import Image
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

root = ctk.CTk()
root.title("Sudoku Game")
root.geometry("900x650")
ctk.set_appearance_mode("dark")

# Global variables
difficulty = ctk.StringVar(value="Easy")
timer_running = True
elapsed_time = 0
count = 0
hint_count= 0
board = [[0] * 9 for _ in range(9)]
solution_board = None
entries = [[None] * 9 for _ in range(9)]
s_row, s_col = None, None

theme = {"0.Primary Bg Color": "#0442BF",
        "1.Secondary Bg Color":"#021859",
        "2.prebuilt number color": "#94F8F8",
        "3.Input number color": "#FF73E6",
        "4.option color":"#0F1140",
        "5.option alt color":"#5f25fe",
        "6.window bg":"#0A0E26",
        "7.Entry border color":"#242424"}

level = {"Beginner": 20,"Easy": 30,"Medium": 40,"Hard": 50,"Extreme": 60}
stage= list(level.keys())
colors = list(theme.values())
default_font= "Helvetica"
root.configure(fg_color=colors[6])

def reset_board():
    global board, entries, s_row, s_col
    board = [[0] * 9 for _ in range(9)]
    s_row, s_col = None, None
    for i in range(9):
        for j in range(9):
            entries[i][j].configure(state=ctk.NORMAL, text_color=colors[3], border_color=colors[6],border_width=2,font=(default_font,15),)
            entries[i][j].delete(0, ctk.END)
def new_game(choice=None):
    global elapsed_time, timer_running,hint_count,hint_button
    reset_board()
    initialize_board()
    hint_button.configure(text=f"Hint (0/3)")
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                entries[i][j].insert(0, str(board[i][j]))
                entries[i][j].configure(state=ctk.DISABLED, text_color=colors[2],font=(default_font,15,'bold'))
    elapsed_time = hint_count = 0
    timer_running = True
def initialize_board():
    global board, solution_board
    def initialize_empty_matrix():
        return [[0 for _ in range(9)] for _ in range(9)]
    def is_number_valid(matrix, row, col, number):
        if number in matrix[row]:
            return False
        for i in range(9):
            if matrix[i][col] == number:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if matrix[i][j] == number:
                    return False
        return True
    def fill_sudoku(matrix):
        for row in range(9):
            for col in range(9):
                if matrix[row][col] == 0:
                    numbers = list(range(1, 10))
                    random.shuffle(numbers)
                    for number in numbers:
                        if is_number_valid(matrix, row, col, number):
                            matrix[row][col] = number
                            if fill_sudoku(matrix):
                                return True
                            matrix[row][col] = 0
                    return False
        return True
    def generate_sudoku():
        matrix = initialize_empty_matrix()
        fill_sudoku(matrix)
        return matrix

    solution_board = generate_sudoku()
    board = [row[:] for row in solution_board]

    cells_to_remove = random.randrange(level.get(difficulty.get(),30)-10,level.get(difficulty.get(),30)+1)
    for _ in range(cells_to_remove):
        row, col = random.randint(0, 8), random.randint(0, 8)
        while board[row][col] == 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
        board[row][col] = 0
def create_widgets(root):
    global entries
    global timer_label
    global count
    def create_button_with_hover(parent, text, command, image, hover_image, **kwargs):
            button_image = ctk.CTkImage(dark_image=image, size=(30, 30))
            hover_button_image = ctk.CTkImage(dark_image=hover_image, size=(30, 30))
            button = ctk.CTkButton(parent,
                text=text,
                command=command,
                image=button_image,
                compound="top",
                fg_color=colors[4],
                corner_radius=5,
                **kwargs)
            button.bind("<Enter>", lambda event: button.configure(image=hover_button_image))
            button.bind("<Leave>", lambda event: button.configure(image=button_image))
            return button
    def header():
        global timer_label, logo_image_dark, logo_image_light, hint_count, hint_button, exit_button

        top_frame = ctk.CTkFrame(root, fg_color="transparent")
        top_frame.pack(side="top", anchor='nw')

        # Logo setup
        logo_image_light = Image.open("sudoku_logo.png")
        logo_image_dark = Image.open("sudoku_logo_v2.png")
        logo_photo = ctk.CTkImage(dark_image=logo_image_light, light_image=logo_image_light, size=(70, 70))
        logo_label = ctk.CTkLabel(top_frame, image=logo_photo, text="")
        logo_label.pack(side="left", anchor='nw', padx=10)
        logo_label.bind("<Button-1>", pause_game)
        logo_label.bind("<Enter>", lambda event: logo_label.configure(image=ctk.CTkImage(dark_image=logo_image_dark, size=(70, 70)), text="Menu"))
        logo_label.bind("<Leave>", lambda event: logo_label.configure(image=logo_photo, text=""))

        # Timer
        time_frame = ctk.CTkFrame(root, fg_color="transparent")
        time_frame.pack(side="top", in_=top_frame, padx=297)
        timer_label = ctk.CTkLabel(time_frame, text="Time: 00:00", font=(default_font, 24), justify='center')
        timer_label.pack(pady=5, side='top', anchor='nw')

        button_config = [
            {"text": "Exit", "command": root.destroy, "image": Image.open("exit.png"), "hover_image": Image.open("exit_bk.png")},
            {"text": "Hint (0/3)", "command": hint, "image": Image.open("hint.png"), "hover_image": Image.open("hint_bk.png")},
            {"text": "Restart", "command": restart_game, "image": Image.open("restart.png"), "hover_image": Image.open("restart_bk.png")},
            {"text": "Auto Solve", "command": auto_solve, "image": Image.open("solve.png"), "hover_image": Image.open("solve_bk.png")},]

        # Create Buttons Dynamically
        for i, config in enumerate(button_config):
            button = create_button_with_hover(
                top_frame,
                text=config["text"],
                command=config["command"],
                image=config["image"],
                hover_image=config["hover_image"])
            button.pack(side='right', anchor='ne')

            if config["text"] == "Hint (0/3)":
                hint_button = button
            elif config["text"] == "Exit":
                exit_button = button
            elif config["text"] == "Restart":
                restart_button = button
    header()
    def soduku_grid():
        grid_frame = ctk.CTkFrame(root)
        grid_frame.pack(pady=10)
        grid_frame.configure(fg_color=colors[6])

        for i in range(9):
            for j in range(9):
                bg_color = colors[0] if (i // 3 + j // 3) % 2 == 0 else colors[1]
                entries[i][j] = ctk.CTkEntry(grid_frame,width=40,height=40,
                    font=(default_font,15),justify="center",
                    fg_color=bg_color,text_color=colors[3],bg_color=colors[6],
                    corner_radius=5,
                    border_color=colors[6],border_width=2)

                entries[i][j].grid(row=i, column=j, padx=1, pady=1)
                if board[i][j] != 0:
                    entries[i][j].insert(0, str(board[i][j]))
                    entries[i][j].configure(state=ctk.DISABLED, text_color=colors[2],font=(default_font,15,'bold'))
                entries[i][j].bind("<FocusIn>", lambda e, row=i, col=j: highlight_cell(row, col))
    soduku_grid()
    def difficulty_menu():
        difficulty_menu = ctk.CTkOptionMenu(root, values=stage,variable=difficulty,command=new_game,)
        difficulty_menu.pack(pady=10)
        difficulty_menu.configure(width=200,height=40,corner_radius=50,fg_color=colors[4],dropdown_fg_color=colors[4],
                                button_hover_color=colors[0],
                                button_color=colors[4],
                                dropdown_hover_color=colors[0],
                                font=(default_font,14))
    difficulty_menu()
    def footer():
        button_frame = ctk.CTkFrame(root)
        button_frame.pack(pady=10,side='top')
        button_frame.configure(fg_color=colors[6])

        new_game_button = ctk.CTkButton(button_frame, text="New Game", command=new_game,font=(default_font,17,'bold'),corner_radius=5,fg_color=colors[4],width=150,height=50)
        new_game_button.grid(row=0, column=1, padx=8)

        submit_button = ctk.CTkButton(button_frame, text="Submit" ,font=(default_font,17,'bold'), command=check_win, corner_radius=5, fg_color=colors[4],width=150,height=50)
        submit_button.grid(row=0, column=2, padx=8)
    footer()

def highlight_cell(row, col):
    global s_row, s_col
    if s_row is not None and s_col is not None:
        entries[s_row][s_col].configure(border_color=colors[6],border_width=2)
    s_row, s_col = row, col
    entries[row][col].configure(border_color=colors[3],border_width=5)
def update_timer():
    global elapsed_time
    if timer_running:
        elapsed_time += 1
        minutes, seconds = divmod(elapsed_time, 60)
        timer_label.configure(text=f"Time: {minutes:02}:{seconds:02}")
    root.after(1000, update_timer)
def hint():
    global entries,hint_count,timer_running,hint_button
    hint_count += 1
    if hint_count > 3 :
        timer_running=False
        hint_error=CTkMessagebox(title="Maximum Hints Used", message="You've used all your hints. Solve the puzzle with the revealed numbers",
                      option_1="Okay",icon='warning')
        if hint_error.get()=="Okay":
            timer_running=True
    else:
        hint_button.configure(text=f"Hint ({hint_count}/3)")
        while True:
            x = random.randint(0,8)
            y = random.randint(0,8)
            if board[x][y] == 0:
                entries[x][y].insert(0, str(solution_board[x][y]))
                board[x][y]='0'
                return False
#---------------------------------------------------- PAUSE--------------------------------------------------------------
def pause_game(event):
    global timer_running, count,pause_window
    timer_running = False
    count+=1
    pause_menu()
def pause_menu():
    global pause_window
    pause_window = ctk.CTkToplevel(root)
    pause_window.title("Game Paused")
    pause_window.geometry("300x200")
    pause_window.resizable(False, False)
    pause_window.configure(fg_color=colors[6])
    ctk.CTkLabel(pause_window, text="Game Paused", font=(default_font, 20)).pack(pady=20)

    pause_window.lift()
    pause_window.attributes("-topmost", True)
    pause_window.focus_force()

    resume_button = ctk.CTkButton(pause_window, text="Resume", command=resume_game,corner_radius=5,fg_color=colors[4])
    resume_button.pack(pady=5)

    restart_button = ctk.CTkButton(pause_window, text="Restart", command=restart_game,corner_radius=5,fg_color=colors[4])
    restart_button.pack(pady=5)

    exit_button = ctk.CTkButton(pause_window, text="Exit", command=root.destroy,corner_radius=5,fg_color=colors[4])
    exit_button.pack(pady=5)
def resume_game():
    global timer_running,pause_window
    timer_running = True
    pause_window.attributes("-topmost", False)
    pause_window.destroy()
def restart_game():
    global entries,s_col,s_row
    s_row, s_col = None, None
    for i in range(9):
        for j in range(9):
            if board[i][j]  == 0 or board[i][j] == '0':
                entries[i][j].delete(0,ctk.END)
    try:
        resume_game()
    except NameError:
        return False
#---------------------------------------------------- SUBMIT--------------------------------------------------------------
def validate_sudoku():
    # rows and columns
    for i in range(9):
        row_values = {}
        col_values = {}
        for j in range(9):
            row_value = entries[i][j].get()
            col_value = entries[j][i].get()

            # row 
            if row_value != "":
                if not row_value.isdigit() or int(row_value) < 1 or int(row_value) > 9:
                    CTkMessagebox(title="Invalid Entry", message=f"Invalid value in row {i + 1}, column {j + 1}. Only digits 1-9 are allowed.", option_1="Okay", icon='warning')
                    highlight_cell(i, j)
                    return False
                if row_value in row_values:
                    CTkMessagebox(title="Invalid Entry", message=f"Duplicate value '{row_value}' found in row {i + 1}.", option_1="Okay", icon='warning')
                    highlight_cell(i, j)  
                    return False
                row_values[row_value] = j  

            # col
            if col_value != "":
                if col_value in col_values:
                    CTkMessagebox(title="Invalid Entry", message=f"Duplicate value '{col_value}' found in column {i + 1}.", option_1="Okay", icon='warning')
                    highlight_cell(j, i)
                    return False
                col_values[col_value] = j

    # Validate 3x3 subgrids
    for row_start in range(0, 9, 3):
        for col_start in range(0, 9, 3):
            subgrid_values = {}
            for i in range(row_start, row_start + 3):
                for j in range(col_start, col_start + 3):
                    subgrid_value = entries[i][j].get()
                    if subgrid_value != "":
                        if subgrid_value in subgrid_values:
                            CTkMessagebox(title="Invalid Entry", message=f"Duplicate value '{subgrid_value}' found in the subgrid starting at row {row_start + 1}, column {col_start + 1}.", option_1="Okay", icon='warning')
                            highlight_cell(*subgrid_values[subgrid_value])
                            return False
                        subgrid_values[subgrid_value] = (i, j)

    return True
def check_win():
    if validate_sudoku():
        if all(entries[i][j].get() == str(solution_board[i][j]) for i in range(9) for j in range(9)):
            global timer_running
            timer_running = False
            CTkMessagebox(title="Congratulations!", message="You've completed the Sudoku puzzle!",option_1="Okay",icon='check')
        else:
            CTkMessagebox(title="Not Yet", message="The Sudoku puzzle is not solved correctly.",option_1="Okay",icon='cancel')
def is_valid(lst):
    lst = [x for x in lst if x != 0]
    return len(lst) == len(set(lst))
def get_square(row, col):
    return [board[i][j] for i in range(row, row + 3) for j in range(col, col + 3)]

def auto_solve():
    global timer_running
    for i in range(9):
        for j in range(9):
            entries[i][j].delete(0, ctk.END)
            entries[i][j].insert(0, str(solution_board[i][j]))
            entries[i][j].configure(state=ctk.NORMAL)
    timer_running = False
    CTkMessagebox(title="Auto Solve", message="The puzzle has been solved!",option_1="Okay",icon='check')
initialize_board()
create_widgets(root)
update_timer()
root.mainloop()
