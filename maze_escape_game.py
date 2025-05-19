# Maze Escape Game with DFS Maze Generation

try:
    import tkinter as tk
except ImportError:
    print("Error: tkinter is not installed. Please install it using 'sudo apt-get install python3-tk' on Ubuntu or 'brew install python-tk' on macOS.")
    exit(1)

import numpy as np
import random
from collections import deque


class MazeEscapeGame:
    def __init__(self, size=15, cell_size=30):
        self.size = size
        self.cell_size = cell_size
        self.window = tk.Tk()
        self.window.title("Maze Escape Game ")
        self.title_frame = tk.Frame(self.window, bg='#333366', pady=10)
        self.title_frame.pack(fill='x')
        self.title_label = tk.Label(
            self.title_frame, 
            text=' Maze Escape Game ', 
            font=('Comic Sans MS', 22, 'bold'), 
            fg='white', 
            bg='#333366'
        )
        self.title_label.pack()
        self.canvas = tk.Canvas(self.window, width=size * cell_size, height=size * cell_size, bg='white')
        self.canvas.pack()
        self.maze = self.generate_maze()
        self.draw_maze()
        
        self.player_pos = (0, 0)
        self.target_pos = (size - 1, size - 1)
        self.player = self.canvas.create_oval(
            5, 5,
            self.cell_size - 5, self.cell_size - 5,
            fill='blue'
        )
        self.window.bind('<KeyPress>', self.on_key_press)
        self.window.mainloop()

    def generate_maze(self):
        maze = np.ones((self.size, self.size), dtype=int)
        stack = [(0, 0)]
        maze[0, 0] = 0
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        while stack:
            x, y = stack[-1]
            neighbors = []
            for dx, dy in directions:
                nx, ny = x + dx * 2, y + dy * 2
                if 0 <= nx < self.size and 0 <= ny < self.size and maze[nx, ny] == 1:
                    neighbors.append((nx, ny, dx, dy))
            if neighbors:
                nx, ny, dx, dy = random.choice(neighbors)
                maze[nx, ny] = 0
                maze[x + dx, y + dy] = 0
                stack.append((nx, ny))
            else:
                stack.pop()
        return maze

    def draw_maze(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.maze[x, y] == 1:
                    self.canvas.create_rectangle(
                        y * self.cell_size, x * self.cell_size,
                        (y + 1) * self.cell_size, (x + 1) * self.cell_size,
                        fill='black'
                    )

    def on_key_press(self, event):
        direction_map = {'Up': (-1, 0), 'Down': (1, 0), 'Left': (0, -1), 'Right': (0, 1)}
        if event.keysym in direction_map:
            dx, dy = direction_map[event.keysym]
            nx, ny = self.player_pos[0] + dx, self.player_pos[1] + dy
            if 0 <= nx < self.size and 0 <= ny < self.size and self.maze[nx, ny] == 0:
                self.player_pos = (nx, ny)
                self.canvas.move(self.player, dy * self.cell_size, dx * self.cell_size)
                if self.player_pos == self.target_pos:
                    self.canvas.create_rectangle(
                        self.target_pos[1] * self.cell_size, self.target_pos[0] * self.cell_size,
                        (self.target_pos[1] + 1) * self.cell_size, (self.target_pos[0] + 1) * self.cell_size,
                        fill='limegreen', outline=''
                    )
                    self.canvas.create_text(
                        self.size * self.cell_size // 2, 
                        self.size * self.cell_size // 2 - 30, 
                        text='🎉 You Escaped! 🎉', font=('Comic Sans MS', 26, 'bold'), fill='green'
                    )
                    self.canvas.create_text(
                        self.size * self.cell_size // 2, 
                        self.size * self.cell_size // 2 + 20, 
                        text='Press any key to restart', font=('Arial', 16), fill='gray'
                    )
                    self.window.unbind('<KeyPress>')
                    self.window.bind('<KeyPress>', self.restart_game)

    def restart_game(self, event):
        self.canvas.delete('all')
        self.maze = self.generate_maze()
        self.draw_maze()
        self.player_pos = (0, 0)
        self.player = self.canvas.create_oval(
            3, 3,
            self.cell_size - 5, self.cell_size - 5,
            fill='blue'
        )
        self.window.bind('<KeyPress>', self.on_key_press)

if __name__ == '__main__':
    MazeEscapeGame(size=15)
