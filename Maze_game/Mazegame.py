import tkinter as tk
import customtkinter as ctk
import random
from collections import deque
from CTkMessagebox import CTkMessagebox

# Global variables
GRID_SIZE = 50
CELL_SIZE =20
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
BACKGROUND_COLOR = "#0A0E26"
WALL_COLOR =  '#0A0E26' 
PATH_COLOR = '#C4E5F2' 
PLAYER_COLOR = EXIT_COLOR =  '#F728CD'

maze = [[1] * GRID_SIZE for _ in range(GRID_SIZE)]
visited = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]

for i in range(GRID_SIZE):
    maze[0][i] = 1  
    maze[GRID_SIZE - 1][i] = 1 
    maze[i][0] = 1
    maze[i][GRID_SIZE - 1] = 1 

player_x, player_y = 1, 1

exit_x, exit_y = GRID_SIZE - 2, GRID_SIZE - 2 

directions = [(-2, 0), (0, 2), (2, 0), (0, -2)]

def draw_maze():
    canvas.delete("all")
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            color = WALL_COLOR if maze[r][c] == 1 else PATH_COLOR
            canvas.create_rectangle(
                c * CELL_SIZE, r * CELL_SIZE, 
                (c + 1) * CELL_SIZE, (r + 1) * CELL_SIZE, 
                fill=color, outline="black"
            )

    canvas.create_oval(
        player_x * CELL_SIZE + 5, player_y * CELL_SIZE + 5,
        (player_x + 1) * CELL_SIZE - 5, (player_y + 1) * CELL_SIZE - 5,
        fill=PLAYER_COLOR, outline="black"
    )

    canvas.create_rectangle(
        exit_x * CELL_SIZE, exit_y * CELL_SIZE,
        (exit_x + 1) * CELL_SIZE, (exit_y + 1) * CELL_SIZE,
        fill=EXIT_COLOR, outline="black"
    )

# My head is aching its 3am help
def generate_maze(x, y):
    visited[y][x] = True
    maze[y][x] = 0

    random.shuffle(directions)

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and not visited[ny][nx]:
            maze[y + dy // 2][x + dx // 2] = 0
            generate_maze(nx, ny)

def ensure_exit():
    queue = deque([(1, 1)])
    reachable = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]
    reachable[1][1] = True
    parent = {}

    while queue:
        x, y = queue.popleft()

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and not reachable[ny][nx] and maze[ny][nx] == 0:
                reachable[ny][nx] = True
                parent[(nx, ny)] = (x, y)
                queue.append((nx, ny))

    if not reachable[exit_y][exit_x]:
        print("Exit not reachable, carving path...")
        queue = deque([(1, 1)])
        parent = {}  
        parent[(1, 1)] = None

        while queue:
            x, y = queue.popleft()

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and maze[ny][nx] == 0 and (nx, ny) not in parent:
                    parent[(nx, ny)] = (x, y)
                    queue.append((nx, ny))

                    if (nx, ny) == (exit_x, exit_y):
                        break

        path = []
        current = (exit_x, exit_y)
        while current is not None:
            path.append(current)
            current = parent.get(current, None) 

        path = path[::-1]


        for (px, py) in path:
            maze[py][px] = 0

def move_player(event):
    global player_x, player_y

    if event.keysym == "Left" and player_x > 0 and maze[player_y][player_x - 1] == 0:
        player_x -= 1
    elif event.keysym == "Right" and player_x < GRID_SIZE - 1 and maze[player_y][player_x + 1] == 0:
        player_x += 1
    elif event.keysym == "Up" and player_y > 0 and maze[player_y - 1][player_x] == 0:
        player_y -= 1
    elif event.keysym == "Down" and player_y < GRID_SIZE - 1 and maze[player_y + 1][player_x] == 0:
        player_y += 1

    draw_maze()

    if player_x == exit_x and player_y == exit_y:
        CTkMessagebox(root, title="Congratulations!", message="You Win!", icon="Maze_game/winner.png", option_1="Okay")

root = ctk.CTk()
root.geometry(f"{WIDTH}x{HEIGHT}")
root.title("Maze Game")
root.configure(bg=BACKGROUND_COLOR)
canvas = ctk.CTkCanvas(root, width=WIDTH, height=HEIGHT, bg=BACKGROUND_COLOR)
canvas.pack()

generate_maze(1, 1) 

ensure_exit()

maze[1][1] = 0

draw_maze()

root.bind("<Left>", move_player)
root.bind("<Right>", move_player)
root.bind("<Up>", move_player)
root.bind("<Down>", move_player)

# i am not sure
root.mainloop()
