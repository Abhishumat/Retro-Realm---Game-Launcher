import os
from PIL import ImageTk, Image
import customtkinter as ctk
import random
from CTkMessagebox import CTkMessagebox

script_dir = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(script_dir, "images")

def load_images_from_folder(folder):
    image_files = [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith(('.png', '.jpg', '.jpeg'))]
    return image_files

def on_label_click(label):
    global selected_labels, clicked_types, score
    if len(selected_labels) == 2 or label.image_clicked:
        return
    label.image_clicked = True
    img_file = label.assigned_image
    img = load_image(img_file)
    label.configure(image=img)
    label.image = img

    selected_labels.append(label)
    clicked_types.append(img_file)

    if len(selected_labels) == 2:
        root.after(1000, check_match)

def check_match():
    global selected_labels, clicked_types, score

    if clicked_types[0] == clicked_types[1]:
        score += 1
        score_label.configure(text=f"Score: {score}")
        if score == num_unique_images:
            CTkMessagebox(root, title="Congratulations!", message="You matched all the pairs!", icon="Find_the_Match/winner.png", option_1="Okay")
    else:
        for label in selected_labels:
            label.configure(image=initial_image)
            label.image = initial_image
            label.image_clicked = False

    selected_labels.clear()
    clicked_types.clear()

def restart_positions():
    global labels, shuffled_images, score

    selected_images = random.sample(image_files, num_unique_images)
    shuffled_images[:] = selected_images * 2
    random.shuffle(shuffled_images)

    for idx, label in enumerate(labels):
        row, col = divmod(idx, cols)
        label.grid(row=row, column=col, padx=5, pady=5)
        label.image_clicked = False
        label.configure(image=initial_image)
        label.image = initial_image
        label.assigned_image = shuffled_images[idx]

    score = 0
    score_label.configure(text=f"Score: {score}")

def exit_game():
    root.destroy()

def load_image(image_file):
    try:
        return ImageTk.PhotoImage(Image.open(image_file).resize((100, 100), Image.NEAREST))
    except FileNotFoundError:
        print(f"Error: File not found - {image_file}")
        return initial_image

theme = {
    "0.Frame color": "#0F1140",
    "1.cross_bg": "#121559",
    "2.circle_bg": "#4132A6",  
    "3.Window_bg": "#0A0E26",
    "4.option color": "#0F1140",
    "5.option alt color": "#5f25fe",
}
colors = list(theme.values())

root = ctk.CTk()
root.title("Memory Match Game")
root.geometry("650x570")
root.configure(fg_color=colors[3])

selected_labels = []
clicked_types = []
score = 0

image_files = load_images_from_folder(image_dir)

cols = 5  
rows = 4  
total_positions = rows * cols

num_unique_images = total_positions // 2
if len(image_files) < num_unique_images:
    raise ValueError(f"Not enough images in the folder. At least {num_unique_images} unique images are required.")
selected_images = random.sample(image_files, num_unique_images)
shuffled_images = selected_images * 2
random.shuffle(shuffled_images)

# Placeholder image (cross icon)
initial_image = ImageTk.PhotoImage(Image.open("Find_the_Match/init_img.png").resize((100, 100), Image.NEAREST))

labels = []


top_frame = ctk.CTkFrame(root, fg_color="transparent")
top_frame.pack(side="top", fill="x")

exit_box = ctk.CTkLabel(top_frame, text="X", fg_color=colors[1], text_color="white", corner_radius=5, width=40, height=40)
exit_box.pack(side="left", padx=10)
exit_box.bind("<Button-1>", lambda event: exit_game())


score_label = ctk.CTkLabel(top_frame, text=f"Score: {score}", corner_radius=10, fg_color=colors[2], width=150, height=40, font=('Helvetica', 24))
score_label.pack(side="top", pady=5, anchor="center")

# Frame for the game grid
grid_frame = ctk.CTkFrame(root, fg_color="transparent")
grid_frame.pack(expand=True, fill="both", pady=10,anchor="center",side="top")

# Add labels to the grid
for idx in range(total_positions):
    label = ctk.CTkLabel(
        grid_frame,
        text="",
        image=initial_image,
        corner_radius=10,
        fg_color=colors[1],
        width=100,
        height=100
    )
    label.image_clicked = False
    label.assigned_image = shuffled_images[idx]
    label.bind("<Button-1>", lambda event, lbl=label: on_label_click(lbl))
    labels.append(label)

# Place labels in the grid
for idx, label in enumerate(labels):
    row, col = divmod(idx, cols)
    label.grid(row=row, column=col, padx=5, pady=5)

# Add "Restart" and "Exit" buttons
button_frame = ctk.CTkFrame(root, fg_color="transparent")
button_frame.pack(side="bottom", fill="x", pady=10)

restart_button = ctk.CTkButton(
    button_frame,
    text="Restart",
    command=restart_positions,
    fg_color=colors[4],
    text_color="white"
)
restart_button.pack(side="left", padx=10)

exit_button = ctk.CTkButton(
    button_frame,
    text="Exit",
    command=exit_game,
    fg_color=colors[5],
    text_color="white"
)
exit_button.pack(side="left", padx=10)

root.mainloop()
