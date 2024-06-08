import tkinter as tk
import random

class Game2048(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("2048 Game")
        self.score = 0
        self.high_score = 0

        self.game_score = tk.StringVar(value="0")
        self.highest_score = tk.StringVar(value="0")

        self.init_ui()
        self.bind_all("<Key>", self.handle_moves)
        self.new_game()

    def init_ui(self):
        button_frame = tk.Frame(self)
        button_frame.pack(side="top")

        tk.Button(button_frame, text="New Game", font=("times new roman", 15), command=self.new_game).grid(row=0, column=0)
        tk.Label(button_frame, text="Score: ", font=("times new roman", 15)).grid(row=0, column=1)
        tk.Label(button_frame, textvariable=self.game_score, font=("times new roman", 15)).grid(row=0, column=2)
        tk.Label(button_frame, text="Record: ", font=("times new roman", 15)).grid(row=0, column=3)
        tk.Label(button_frame, textvariable=self.highest_score, font=("times new roman", 15)).grid(row=0, column=4)

        self.canvas = tk.Canvas(self, width=410, height=410, borderwidth=5, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand=False)

    def new_game(self):
        self.game_board = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.update_score()
        self.add_random_tile()
        self.add_random_tile()
        self.draw_board()

    def add_random_tile(self):
        if not self.is_full():
            x, y = random.choice([(i, j) for i in range(4) for j in range(4) if self.game_board[i][j] == 0])
            self.game_board[x][y] = random.choice([2] * 6 + [4])
            self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        cellwidth = 105
        cellheight = 105
        for row in range(4):
            for col in range(4):
                x1 = col * cellwidth
                y1 = row * cellheight
                x2 = x1 + cellwidth - 5
                y2 = y1 + cellheight - 5
                num = self.game_board[row][col]
                self.draw_tile(x1, y1, x2, y2, num)

    def draw_tile(self, x1, y1, x2, y2, num):
        bg_color = {
            '0': '#f5f5f5', '2': '#eee4da', '4': '#ede0c8', '8': '#edc850', '16': '#edc53f', '32': '#f67c5f',
            '64': '#f65e3b', '128': '#edcf72', '256': '#edcc61', '512': '#f2b179', '1024': '#f59563', '2048': '#edc22e'
        }
        text_color = {
            '2': '#776e65', '4': '#776e65', '8': '#f9f6f2', '16': '#f9f6f2', '32': '#f9f6f2', '64': '#f9f6f2',
            '128': '#f9f6f2', '256': '#f9f6f2', '512': '#f9f6f2', '1024': '#f9f6f2', '2048': '#f9f6f2'
        }
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=bg_color.get(str(num), "#cdc1b4"), outline="")
        if num:
            self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, font=("Arial", 36),fill=text_color.get(str(num), "#776e65"), text=str(num))

    def handle_moves(self, event):
        moves = {
            'Up': self.move_up,
            'Down': self.move_down,
            'Left': self.move_left,
            'Right': self.move_right
        }
        if event.keysym in moves:
            moves[event.keysym]()
            self.add_random_tile()
            self.check_game_over()

    def move_up(self):
        self.slide_and_merge(direction='up')
        self.draw_board()

    def move_down(self):
        self.slide_and_merge(direction='down')
        self.draw_board()

    def move_left(self):
        self.slide_and_merge(direction='left')
        self.draw_board()

    def move_right(self):
        self.slide_and_merge(direction='right')
        self.draw_board()

    def slide_and_merge(self, direction):
        original_board = [row[:] for row in self.game_board]
        for _ in range(4):
            if direction in ('up', 'down'):
                self.game_board = [list(col) for col in zip(*self.game_board)]
            if direction in ('down', 'right'):
                self.game_board = [row[::-1] for row in self.game_board]
            for i in range(4):
                self.slide_and_merge_row(self.game_board[i])
            if direction in ('down', 'right'):
                self.game_board = [row[::-1] for row in self.game_board]
            if direction in ('up', 'down'):
                self.game_board = [list(col) for col in zip(*self.game_board)]
        if self.game_board != original_board:
            self.update_score()

    def slide_and_merge_row(self, row):
        filtered_row = [num for num in row if num != 0]
        for i in range(len(filtered_row) - 1):
            if filtered_row[i] == filtered_row[i + 1]:
                filtered_row[i] *= 2
                self.score += filtered_row[i]
                filtered_row[i + 1] = 0
        filtered_row = [num for num in filtered_row if num != 0]
        row[:] = filtered_row + [0] * (4 - len(filtered_row))

    def is_full(self):
        return all(all(row) for row in self.game_board)

    def check_game_over(self):
        if self.is_full():
            for i in range(4):
                for j in range(4):
                    if (i < 3 and self.game_board[i][j] == self.game_board[i + 1][j]) or \
                            (j < 3 and self.game_board[i][j] == self.game_board[i][j + 1]):
                        return
            self.canvas.create_text(205, 205, text="Game Over", font=("Arial", 36), fill="red")

    def update_score(self):
        self.game_score.set(str(self.score))
        if self.score > self.high_score:
            self.high_score = self.score
            self.highest_score.set(str(self.high_score))

if __name__ == "__main__":
    game = Game2048()
    game.mainloop()
