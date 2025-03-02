import customtkinter as ctk


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue") 

class ConnectFour(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Connect Four")
        self.geometry("700x750")
        self.resizable(False, False)
        self.configure(fg_color="#0A0E26")

        self.rows = 6
        self.columns = 7
        self.grid = [[None for _ in range(self.columns)] for _ in range(self.rows)]
        self.current_player = "Red"
        self.red_score = 0
        self.yellow_score = 0

        self.create_widgets()
    def create_widgets(self):
        self.ask_name_frame = ctk.CTkFrame(self, width=650, height=700, fg_color="gray20")
        self.ask_name_frame.pack(expand=True, pady=10)
        self.ask_name_frame.configure(fg_color="#0F1140")

        self.name_label = ctk.CTkLabel(self.ask_name_frame, text="Enter Player Names", font=("Arial", 20), text_color="white")
        self.name_label.pack(pady=20)

        self.red_name_label = ctk.CTkLabel(self.ask_name_frame, text="Red Player Name:", font=("Arial", 14), text_color="white")
        self.red_name_label.pack(pady=5)
        self.red_name_entry = ctk.CTkEntry(self.ask_name_frame, width=300)
        self.red_name_entry.pack(pady=5)

        self.yellow_name_label = ctk.CTkLabel(self.ask_name_frame, text="Yellow Player Name:", font=("Arial", 14), text_color="white")
        self.yellow_name_label.pack(pady=5)
        self.yellow_name_entry = ctk.CTkEntry(self.ask_name_frame, width=300)
        self.yellow_name_entry.pack(pady=5)

        self.start_button = ctk.CTkButton(self.ask_name_frame, text="Start Game", command=self.start_game,fg_color="#0A0E26")
        self.start_button.pack(pady=20)
    def start_game(self):
        self.red_player_name = self.red_name_entry.get()
        self.yellow_player_name = self.yellow_name_entry.get()

        if not self.red_player_name or not self.yellow_player_name:
            return 
        self.ask_name_frame.destroy()

        # Create the game UI
        self.create_game_ui()
    def create_game_ui(self):
        self.turn_label = ctk.CTkLabel(
            self,
            text=f"{self.current_player}'s Turn",
            font=("Arial", 18),
            text_color="white"
        )
        self.turn_label.pack(pady=10)
        self.score_label = ctk.CTkLabel(
            self,
            text=f"Score - {self.red_player_name} (Red): {self.red_score} | {self.yellow_player_name} (Yellow): {self.yellow_score}",
            font=("Arial", 14),
            text_color="white"
        )
        self.score_label.pack(pady=5)

        self.main_frame = ctk.CTkFrame(self, width=650, height=700, fg_color="transparent")
        self.main_frame.pack(expand=True, pady=10)

        self.buttons = []
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.grid(row=0, column=0, pady=5)
        for col in range(self.columns):
            button = ctk.CTkButton(
                self.button_frame,
                text=f"↓ {col + 1}",
                command=lambda c=col: self.drop_piece(c),
                width=70,
                height=35,
                fg_color="#5f25fe",
            )
            button.grid(row=0, column=col, padx=5)
            self.buttons.append(button)

        self.grid_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.grid_frame.grid(row=1, column=0, pady=10)
        self.cells = [[None for _ in range(self.columns)] for _ in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.columns):
                cell = ctk.CTkLabel(
                    self.grid_frame, text="", width=70, height=70, fg_color="gray30"
                )
                cell.grid(row=row, column=col, padx=4, pady=4)
                cell.configure(fg_color="#0F1140")
                self.cells[row][col] = cell
    def drop_piece(self, column):
        for row in reversed(range(self.rows)):
            if self.grid[row][column] is None:
                self.grid[row][column] = self.current_player
                self.cells[row][column].configure(fg_color=self.current_player.lower())
                if self.check_winner(row, column):
                    self.end_game(row, column)
                else:
                    self.switch_player()
                return
    def switch_player(self):
        self.current_player = "Yellow" if self.current_player == "Red" else "Red"
        self.turn_label.configure(text=f"{self.current_player}'s Turn")
    def check_winner(self, row, column):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dr, dc in directions:
            winning_positions = [(row, column)]
            winning_positions += self.get_positions(row, column, dr, dc)
            winning_positions += self.get_positions(row, column, -dr, -dc)
            if len(winning_positions) >= 4:
                self.highlight_winner(winning_positions)
                return True
        return False
    def get_positions(self, row, col, dr, dc):
        positions = []
        r, c = row + dr, col + dc
        while (
            0 <= r < self.rows
            and 0 <= c < self.columns
            and self.grid[r][c] == self.current_player
        ):
            positions.append((r, c))
            r += dr
            c += dc
        return positions

    def highlight_winner(self, positions):
        for r, c in positions:
            self.cells[r][c].configure(fg_color="purple")

    def end_game(self, row, column):
        for button in self.buttons:
            button.configure(state="disabled")

        winner_text = f"{self.red_player_name if self.current_player == 'Red' else self.yellow_player_name} Wins!"
        self.turn_label.configure(text=winner_text)
        
        if self.current_player == "Red":
            self.red_score += 1
        else:
            self.yellow_score += 1
        self.score_label.configure(text=f"Score - {self.red_player_name} (Red): {self.red_score} | {self.yellow_player_name} (Yellow): {self.yellow_score}")

        self.play_again_button = ctk.CTkButton(self.main_frame, text="Play Again", command=self.reset_game)
        self.play_again_button.grid(row=self.rows + 1, column=0, columnspan=self.columns, pady=10)

        self.close_button = ctk.CTkButton(self.main_frame, text="Close", command=self.quit)
        self.close_button.grid(row=self.rows + 2, column=0, columnspan=self.columns, pady=10)

    def reset_game(self):
        for row in range(self.rows):
            for col in range(self.columns):
                self.grid[row][col] = None
                self.cells[row][col].configure(fg_color="gray30", text="")

        for button in self.buttons:
            button.configure(state="normal")

        self.current_player = "Red"
        self.turn_label.configure(text=f"{self.current_player}'s Turn")
        self.play_again_button.grid_forget()
        self.close_button.grid_forget()

if __name__ == "__main__":
    app = ConnectFour()
    app.mainloop()

