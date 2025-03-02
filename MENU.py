import tkinter as tk
from PIL import ImageTk, Image
import customtkinter as ctk
from subprocess import call
from customtkinter import *
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

main_menu = ctk.CTk()
main_menu.iconbitmap("game.ico")
main_menu.configure(bg="#0A0E26") 
game_font = ctk.CTkFont(family="Berlin Sans FB Demi", size=28, weight="bold")
main_menu.title("Retro Realm Game Launcher")
main_menu.geometry("{}x{}+0+0".format(main_menu.winfo_screenwidth(), main_menu.winfo_screenheight()))

menu_frame = tk.Frame(main_menu,highlightbackground='#0442BF',highlightthickness=2,bd=0)
menu_frame.pack(expand=True, fill="both")  
hover_co="#00ffff"
hover_co2="#ff13f0"
text_co="#ff13f0"
bg_co="#0A0E26"
text_co2="#00ffff"

menu_frame.columnconfigure(0, weight=1)  
menu_frame.columnconfigure(4, weight=1)  
for i in range(8): 
    menu_frame.rowconfigure(i, weight=1)  
menu_frame.config(bg=bg_co)  

gaming_img = ImageTk.PhotoImage(Image.open("final.png").resize((1280,1080)))
gaming_label = tk.Label(menu_frame, image=gaming_img)
gaming_label.config(bg=bg_co)  
gaming_label.grid(row=1,column=1,columnspan=3,rowspan=3)  


def open_sudoku():
    call(["python", "Sudoku/Sukudo.py"])
def open_flappy_bird():
    call(["python", "Flappy_plane/flappy_plane.py"])
def open_Maze_game():
    call(["python", "Maze_game/Mazegame.py"])
def open_find_the_match():
    call(["python", "Find_the_Match/match_game.py"])
def open_tic_tac_toe():
    call(["python", "tic_tac_toe/tictactoe.py"])
def open_connect_four():
    call(["python", "Connect_4/Connect4.py"])

menu_g1 = ctk.CTkButton(menu_frame,text="SUDOKU", font=game_font, text_color=text_co,fg_color=bg_co,hover_color=hover_co, command=open_sudoku)
menu_g2 = ctk.CTkButton(menu_frame, text=" FLAPPY \n PLANE", font=game_font, text_color=text_co,fg_color=bg_co,hover_color=hover_co,command=open_flappy_bird)
menu_g3 = ctk.CTkButton(menu_frame, text="MAZE ESCAPE", font=game_font, text_color=text_co,fg_color=bg_co,hover_color=hover_co,command=open_Maze_game)
menu_g7 = ctk.CTkButton(menu_frame, text="MATCH THE \n PAIRS", font=game_font, text_color=text_co2,fg_color=bg_co,hover_color=hover_co2,command=open_find_the_match)
menu_g6 = ctk.CTkButton(menu_frame, text="TIC TAC TOE", font=game_font, text_color=text_co2,fg_color=bg_co,hover_color=hover_co2,command=open_tic_tac_toe)
menu_g8 = ctk.CTkButton(menu_frame, text="CONNECT 4", font=game_font, text_color=text_co2,fg_color=bg_co,hover_color=hover_co2,command=open_connect_four)

menu_g1.grid(row=1, column=0, padx=40, pady=5)
menu_g2.grid(row=2, column=0, padx=40, pady=5)
menu_g3.grid(row=3, column=0, padx=40, pady=5)
menu_g6.grid(row=1, column=4, padx=40, pady=5)
menu_g7.grid(row=2, column=4, padx=40, pady=5)
menu_g8.grid(row=3, column=4, padx=40, pady=5)

main_menu.mainloop()