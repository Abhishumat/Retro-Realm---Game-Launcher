import random
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Global variables
board = [[0] * 3 for _ in range(3)]
entries = [[None] * 3 for _ in range(3)]
labels = [[None] * 3 for _ in range(3)]
move = 'x'
theme = {
        "0.Frame color": "#0F1140",
        "1.cross_bg": "#121559",
        "2.circle_bg": "#4132A6",#0E3D40
        "3.Window_bg": "#0A0E26",
    }
colors = list(theme.values())
default_font= "Helvetica"
win = ctk.CTkImage(Image.open("winner.png",'r'))
cross_img = ctk.CTkImage(Image.open("cross.png"), size=(120, 120))
circle_img = ctk.CTkImage(Image.open("circle.png"), size=(120, 120))

root = ctk.CTk()
root.title("Tic Tac Toe")
root.geometry("600x600")
root.configure(fg_color=colors[-1])

def game_grid():
    global info
    def header():
        def logo_change(event):
            logo_photo.configure(dark_image= logo_image_dark,size=(70,70))
            logo_label.configure(image=logo_photo, text="Restart")

        def logo_revert(event):
            logo_photo.configure(dark_image= logo_image_light,size=(70,70))
            logo_label.configure(image=logo_photo, text="")

        top_frame = ctk.CTkFrame(root, fg_color="transparent")
        top_frame.pack(side="top",anchor='nw')
        logo_image_light = Image.open("tic_white.png")
        logo_image_dark = Image.open("tic_black.png")
        logo_photo = ctk.CTkImage(dark_image=logo_image_light ,light_image=logo_image_light,size=(70,70))
        logo_photo.configure(Image=logo_photo)
        logo_label = ctk.CTkLabel(top_frame, image=logo_photo, text="")
        logo_label.pack(side="left",anchor='nw', padx=10)
        logo_label.bind("<Button-1>", restart)
        
        
        logo_label.bind("<Enter>",logo_change)
        logo_label.bind("<Leave>",logo_revert)
    header()

    info = ctk.CTkLabel(root,text=f"{move}'s turn",font=(default_font,30))
    info.pack(side='top')
    grid_frame = ctk.CTkFrame(root)
    grid_frame.configure(fg_color=colors[-1])
    grid_frame.pack(pady=10)
    
    for i in range(3):
        for j in range(3):
            entries[i][j] = ctk.CTkFrame(grid_frame,
                width=120,
                height=120,
                fg_color=colors[0],
                corner_radius=0,
            )
            entries[i][j].grid(row=i, column=j, padx=10, pady=10)

            entries[i][j].bind("<Button-1>", lambda event, x=i, y=j: take_input(x, y))

def take_input(x, y):
    global move,info
    if board[x][y] == 0:
        if move == 'x':
            labels[x][y] = ctk.CTkLabel(entries[x][y], image=cross_img, text="")
            labels[x][y].configure(bg_color=colors[1])
            labels[x][y].pack(expand=True)
            board[x][y] = 'x'
            move = 'o'
            info.configure(text=f"{move}'s turn")
        else:
            labels[x][y] = ctk.CTkLabel(entries[x][y], image=circle_img, text="")
            labels[x][y].configure(bg_color=colors[1])
            labels[x][y].pack(expand=True)
            board[x][y] = 'o'
            move = 'x'
            info.configure(text=f"{move}'s turn")

        check_game_status()

def check_game_status():
    winner = None
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != 0:
            winner = board[i][0]
            for y in range(3):
                labels[i][y].configure(bg_color=colors[2])
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != 0:
            winner = board[0][i]
            for y in range(3):
                labels[y][i].configure(bg_color=colors[2])
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != 0:
        winner = board[0][0]
        for y in range(3):
            labels[y][y].configure(bg_color=colors[2])
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != 0:
        winner = board[0][2]
        for y in range(3):
            labels[0+y][2-y].configure(bg_color=colors[2])

    if winner:
        result=CTkMessagebox(root,title="Game Over", message=f"Player {winner.upper()} wins!",icon="winner.png",option_1="Okay")
        result.configure(fg_color=colors[-1],bg_color=colors[0])
        if result.get()== "Okay":
            reset_game()
    elif all(all(cell != 0 for cell in row) for row in board):
        result=CTkMessagebox(title="Game Over", message="It's a draw!",option_1="Okay",icon='draw.png')
        if result.get()== "Okay":
            reset_game()

def reset_game():
    global board, move,info
    board = [[0] * 3 for _ in range(3)]
    move = 'x'
    info.configure(text=f"{move}'s turn")
    for i in range(3):
        for j in range(3):
            if labels[i][j]:
                labels[i][j].destroy()
                labels[i][j] = None
def restart(event):
    reset_game()

game_grid()
root.mainloop()
