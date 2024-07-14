import tkinter as tk
from tkinter import messagebox
import time
from collections import deque
 
 
class NQueensSolver:
    def __init__(self, n, algorithm):
        self.n = n
        self.algorithm = algorithm
        self.board = [-1] * n
        self.solutions = []
        self.time_taken = 0
 
    def solve(self):
        start_time = time.time()
 
        if self.algorithm == "DFS":
            self.dfs(0)
        elif self.algorithm == "BFS":
            self.bfs()
        elif self.algorithm == "Recursive-Backtracking":
            self.recursive_backtracking()
        elif self.algorithm == "NQueensSolver":
            self.solutions = self.solveNQueens(self.n)
 
        self.time_taken = time.time() - start_time
 
    def dfs(self, row):
        if row == self.n:
            self.solutions.append(self.board.copy())
            return
 
        for col in range(self.n):
            if self.is_safe(row, col):
                self.board[row] = col
                self.dfs(row + 1)
                self.board[row] = -1
 
    def bfs(self):
        queue = deque([(0, [])])
 
        while queue:
            row, cols = queue.popleft()
 
            if row == self.n:
                self.solutions.append(cols)
            else:
                for col in range(self.n):
                    if self.is_safe(row, col):
                        queue.append((row + 1, cols + [col]))
 
    def recursive_backtracking(self):
        def is_safe(board, row, col):
            for i in range(row):
                if board[i] == col or board[i] - i == col - row or board[i] + i == col + row:
                    return False
            return True
 
        def solve_util(board, row):
            if row == self.n:
                self.solutions.append(board.copy())
                return
            for col in range(self.n):
                if is_safe(board, row, col):
                    board[row] = col
                    solve_util(board, row + 1)
                    board[row] = -1
 
        initial_board = [-1] * self.n
        solve_util(initial_board, 0)
 
    def is_safe(self, row, col):
        for i in range(row):
            if self.board[i] == col or abs(self.board[i] - col) == row - i:
                return False
        return True
 
    def solveNQueens(self, n):
        def is_safe(board, row, col, left_diagonal, right_diagonal, column):
            return not (column[col] or left_diagonal[row - col] or right_diagonal[row + col])
 
        def update_attack_arrays(row, col, left_diagonal, right_diagonal, column, value):
            left_diagonal[row - col] = value
            right_diagonal[row + col] = value
            column[col] = value
 
        def solve_util(row, board, left_diagonal, right_diagonal, column):
            if row == n:
                return [board[:]]
 
            solutions = []
            for col in range(n):
                if is_safe(board, row, col, left_diagonal, right_diagonal, column):
                    board[row] = col
                    update_attack_arrays(row, col, left_diagonal, right_diagonal, column, True)
                    solutions.extend(solve_util(row + 1, board, left_diagonal, right_diagonal, column))
                    update_attack_arrays(row, col, left_diagonal, right_diagonal, column, False)
 
            return solutions
 
        board = [-1] * n
        left_diagonal = [False] * (2 * n - 1)
        right_diagonal = [False] * (2 * n - 1)
        column = [False] * n
 
        return solve_util(0, board, left_diagonal, right_diagonal, column)
 
 
class NQueensGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("N-Queens Game")
        self.score = 0
        self.max_score = 0
        self.algorithm_used = ""
        self.setup()
 
    def setup(self):
        self.label = tk.Label(self.root, text="Enter the size of the chessboard (N):")
        self.label.pack()
 
        self.entry = tk.Entry(self.root)
        self.entry.pack()
 
        self.algorithm_label = tk.Label(self.root, text="Choose Algorithm:")
        self.algorithm_label.pack()
 
        algorithms = ["DFS", "BFS", "Recursive-Backtracking", "NQueensSolver"]
        self.algorithm_var = tk.StringVar(value=algorithms[0])
        self.algorithm_menu = tk.OptionMenu(self.root, self.algorithm_var, *algorithms)
        self.algorithm_menu.pack()
 
        self.start_button = tk.Button(self.root, text="Start Game", command=self.start_game)
        self.start_button.pack()
 
        self.compute_button = tk.Button(self.root, text="Compute All Solutions", command=self.compute_all_solutions)
        self.compute_button.pack()
 
        self.root.mainloop()
 
    def start_game(self):
        try:
            n = int(self.entry.get())
            algorithm = self.algorithm_var.get()
 
            solver = NQueensSolver(n, algorithm)
            solver.solve()
 
            self.algorithm_used = algorithm
            self.max_score = len(solver.solutions[0]) * 10
 
            self.play_game(solver)
 
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid integer.")
 
    def compute_all_solutions(self):
        try:
            n = int(self.entry.get())
            algorithm = self.algorithm_var.get()
 
            solver = NQueensSolver(n, algorithm)
            solver.solve()
 
            self.algorithm_used = algorithm
 
            if solver.solutions:
                self.max_score = len(solver.solutions[0]) * 10
 
            self.show_solution_stats(solver)
 
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid integer.")
 
    def play_game(self, solver):
        self.root.withdraw()
 
        chessboard = tk.Toplevel()
        chessboard.title("N-Queens Chessboard")
 
        self.draw_chessboard(chessboard, solver.n)
        self.score_label = tk.Label(chessboard, text=f"Score: {self.score}")
        self.score_label.grid(row=solver.n, column=0, columnspan=solver.n, pady=10)
        self.display_user_board(chessboard, solver.n, solver)
 
        chessboard.mainloop()
 
    def draw_chessboard(self, chessboard, n):
        self.labels = [[tk.Label(chessboard, text="   ", font=("Arial", 48), borderwidth=1, relief="solid") for _ in range(n)] for _ in range(n)]
 
        for i in range(n):
            for j in range(n):
                self.labels[i][j].grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                if (i + j) % 2 == 0:
                    self.labels[i][j].configure(bg="#f0d9b5")
                else:
                    self.labels[i][j].configure(bg="#b58863")
 
    def display_user_board(self, chessboard, n, solver):
        user_board = [-1] * n
 
        def callback(event):
            nonlocal user_board
            nonlocal chessboard
 
            col = event.widget.grid_info()["column"]
 
            if self.is_placement_possible(user_board, event.widget.grid_info()["row"], col):
                user_board[event.widget.grid_info()["row"]] = col
                self.place_queen(chessboard, event.widget.grid_info()["row"], col, "#0000ff", user_board)
                self.score += 10
                self.score_label.config(text=f"Score: {self.score}")
 
                if not self.is_any_valid_spot(user_board):
                    self.show_final_score(chessboard)
 
            else:
                messagebox.showinfo("Wrong Placement", "Incorrect placement. Try again.")
                self.score -= 10
                self.score_label.config(text=f"Score: {self.score}")
 
        for i in range(n):
            for j in range(n):
                self.labels[i][j].bind("<Button-1>", callback)
 
    def is_any_valid_spot(self, user_board):
        for i in range(len(user_board)):
            for j in range(len(user_board)):
                if user_board[i] == -1 and self.is_placement_possible(user_board, i, j):
                    return True
        return False
 
    def is_placement_possible(self, user_board, row, col):
        for i in range(len(user_board)):
            if (
                (user_board[i] != -1 and user_board[i] == col)
                or (user_board[i] != -1 and abs(user_board[i] - col) == abs(i - row))
                or (user_board[i] != -1 and row == i)
            ):
                return False
        return True
 
    def place_queen(self, chessboard, row, col, color, user_board):
        self.labels[row][col].configure(text="Q", fg=color)
 
    def show_final_score(self, chessboard):
        if self.score == self.max_score:
            messagebox.showinfo("Congratulations!", f"Congratulations! You achieved the maximum score of {self.max_score} using {self.algorithm_used}.")
        else:
            difference = self.max_score - self.score
            messagebox.showinfo("Game Over", f"No further queens can be placed. Your score: {self.score}\nDifference from maximum score: {difference}")
        self.play_again()
 
    def show_solution_stats(self, solver):
        max_score = len(solver.solutions[0]) * 10
        stats_window = tk.Toplevel()
        stats_window.title("Solution Statistics")
 
        total_solutions_label = tk.Label(stats_window, text=f"Total Solutions ({self.algorithm_used}): {len(solver.solutions)}", font=("Arial", 14))
        total_solutions_label.pack(pady=10)
 
        max_queens_label = tk.Label(stats_window, text=f"Maximum Queens Placeable: {len(solver.solutions[0])}", font=("Arial", 14))
        max_queens_label.pack(pady=10)
 
        max_score_label = tk.Label(stats_window, text=f"Maximum Score Possible: {max_score}", font=("Arial", 14))
        max_score_label.pack(pady=10)
 
        time_taken_label = tk.Label(stats_window, text=f"Total Time Taken: {solver.time_taken:.4f} seconds", font=("Arial", 14))
        time_taken_label.pack(pady=10)
 
        solutions_label = tk.Label(stats_window, text="Solutions:", font=("Arial", 14))
        solutions_label.pack(pady=10)
 
        for solution in solver.solutions:
            solution_str = ", ".join(str(col) for col in solution)
            solution_label = tk.Label(stats_window, text=solution_str, font=("Arial", 12))
            solution_label.pack()
 
            view_solution_button = tk.Button(
                stats_window,
                text="View Solution",
                command=lambda s=solution: self.view_solution(stats_window, solver, s)
            )
            view_solution_button.pack()
 
        stats_window.mainloop()
 
    def view_solution(self, parent, solver, solution):
        solution_window = tk.Toplevel(parent)
        solution_window.title("View Solution")
 
        chessboard = tk.Frame(solution_window)
        chessboard.pack(pady=10)
 
        self.draw_chessboard(chessboard, solver.n)
        self.display_solution(chessboard, solution)
 
        play_again_button = tk.Button(solution_window, text="Play Again", command=self.play_again)
        play_again_button.pack(pady=10)
 
        solution_window.mainloop()
 
    def play_again(self):
        play_again_window = tk.Toplevel()
        play_again_window.title("Play Again")
 
        play_again_label = tk.Label(play_again_window, text="Do you want to play again?")
        play_again_label.pack(pady=10)
 
        yes_button = tk.Button(play_again_window, text="Yes", command=self.restart_game)
        yes_button.pack(pady=5)
 
        no_button = tk.Button(play_again_window, text="No", command=self.root.destroy)
        no_button.pack(pady=5)
 
        play_again_window.mainloop()
 
    def restart_game(self):
        self.root.deiconify()
        self.root.iconify()
        NQueensGame()
 
 
if __name__ == "__main__":
    game = NQueensGame()
 