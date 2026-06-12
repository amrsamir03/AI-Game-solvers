import queue
import numpy as np 
import random
import tkinter as tk
from tkinter import messagebox
import time

# easy= 0.1
# intermediate = 0.3
# hard = 0.5

global counter
counter = 0
class CSP:
    def __init__(self):
        self.variables = []

class Variable:
    def __init__(self, i, j, k, val):
        self.row = i
        self.column = j
        self.block = k
        if val == 0:
            self.domain = [1,2,3,4,5,6,7,8,9]
            self.value = 0
        else:
            self.domain = [val]
            self.value = val

class Arc:
    def __init__(self, a, b):
        self.first = a
        self.second = b


def AC3(csp):
    arcs=queue.Queue()
    for i in csp.variables:
        for j in csp.variables:
            if j.value > 9 or j.value < 0:
                return False
            if i != j and (i.row == j.row or i.column == j.column or i.block == j.block):
                arcs.put(Arc(i,j))
                
    while not arcs.empty():
        arc = arcs.get()
        if revise(arc.first, arc.second):
            if(len(arc.first.domain) == 0 or len(arc.second.domain)==0):
                return False
            for xk in csp.variables:
                if xk != arc.first and xk != arc.second and (xk.row == arc.first.row or xk.column == arc.first.column or xk.block == arc.first.block):
                    arcs.put(Arc(xk,arc.first))
    return True
    
def revise(xi,xj):
    revised = False
    for x in xi.domain:
        if (len(xj.domain) == 1 and xj.domain[0] == x) or (xj.value == x):
                xi.domain.remove(x)
                print(x," removed from domain of element at row:",xi.row,"and column:",xi.column,"domain:",xi.domain)
                revised = True
    return revised

def BTS(csp):
    return backtrack({},csp)
    
def backtrack(assignment,csp):
    unassigned = []
    for var in csp.variables:
        if var.value == 0:
            unassigned.append(var)

    if len(unassigned) == 0:
        return True

    for l in range (len(unassigned)):
        smallest_dom = len(min(unassigned, key=lambda x: len(x.domain)).domain)
        var = random.choice([v for v in unassigned if len(v.domain) == smallest_dom])

        for val in var.domain[:]:
            if is_valid(csp,var.row,var.column,val):
                prevval=var.value
                old_dom=var.domain[:]
                var.value = val
                var.domain = [val]
                assignment[var] = val
                if AC3(csp):
                    if backtrack(assignment,csp):
                        return True
                var.value = prevval
                var.domain = old_dom
                #var.domain.remove(val)
                del assignment[var]

        return False

    return True

def is_valid(csp,row,col,num):
    block = row//3 * 3 + col//3 
    for var in csp.variables:
        if not(var.row == row and var.column == col):
            if var.row == row and var.value == num:
                return False
            if var.column == col and var.value == num:
                return False
            if var.block == block and var.value == num:
                return False
    return True


def BTSgui(csp):
    return backtrackgui({},csp)

def backtrackgui(assignment,csp):
    global counter
    unassigned = []
    for var in csp.variables:
        if var.value == 0:
            unassigned.append(var)

    if len(unassigned) == 0:
        return True

    for l in range (len(unassigned)):
        smallest_dom = len(min(unassigned, key=lambda x: len(x.domain)).domain)
        var = random.choice([v for v in unassigned if len(v.domain) == smallest_dom])

        for val in var.domain[:]:
            if is_valid(csp,var.row,var.column,val):
                prevval=var.value
                old_dom=var.domain[:]
                var.value = val
                var.domain = [val]
                assignment[var] = val
                entries[var.row][var.column].insert(0, val)
                root.update()
                time.sleep(0.05)
                counter += 1
                if AC3(csp):
                    if backtrackgui(assignment,csp):
                        return True
                #backtracking
                var.value = prevval
                var.domain = old_dom
                #var.domain.remove(val)
                del assignment[var]
                entries[var.row][var.column].delete(0, tk.END)
                root.update()
                time.sleep(0.05)

        return False
    return True

def random_generate(difficulty):
    start_time=time.time()
    nosol = True
    while nosol:
        puzzle = np.zeros((9,9), dtype = int)
        csp = CSP()
        for i in range(9):
            for j in range(9):
                k= i//3 *3 + j//3 
                csp.variables.append(Variable(i,j,k,puzzle[i][j]))
        if BTS(csp):
            for var in csp.variables:
                puzzle[var.row][var.column] = var.value
            safe = puzzle.copy()
            remove = [(row,col)for row in range(9) for col in range(9)]
            random.shuffle(remove)
            if difficulty == 0.1:
                removed = remove[:25]
            elif difficulty == 0.3:
                removed = remove[:45]
            elif difficulty == 0.5:
                removed = remove[:65]

            for i,j in removed:
                puzzle[i][j] = 0
                clone = CSP()
                for i in range(9):
                    for j in range(9):
                        k= i//3 *3 + j//3 
                        clone.variables.append(Variable(i,j,k,puzzle[i][j]))

                if(AC3(clone)) == False or (BTS(clone)) == False:
                    puzzle[i][j] = safe[i][j]

    
            problem = CSP()
            for i in range(9):
                for j in range(9):
                    k= i//3 *3 + j//3 
                    problem.variables.append(Variable(i,j,k,puzzle[i][j]))
            nosol = False
    end_time=time.time()
    print("Puzzle generated in",(end_time-start_time)*1000,"Milliseconds")
    return problem

def solve_sudoku():
    global counter
    start_time=time.time()
    global test
    if AC3(test):
        if BTSgui(test):
            for i in range(9):
                for j in range(9):
                    entries[i][j].delete(0, tk.END)
                    entries[i][j].insert(0, test.variables[i * 9 + j].value)
            messagebox.showinfo("Sudoku Solved", "Sudoku solved successfully!")
            end_time=time.time()
            print("Puzzle solved in",(end_time-start_time-0.5*counter)*1000,"Milliseconds")
        else:
            messagebox.showerror("No Solution", "No solution exists for the given Sudoku.")
    else:
        messagebox.showerror("Invalid State", "The initial Sudoku puzzle state is invalid.")

def submit():
    global counter
    global test
    solution = np.zeros((9,9),dtype = int)
    if AC3(test):
        if BTS(test):
            for i in range(9):
                for j in range(9):
                    solution[i][j] = test.variables[i * 9 + j].value

    puzzle = np.zeros((9, 9), dtype=int)
    for i in range(9):
        for j in range(9):
            value = entries[i][j].get()
            if value.isdigit():
                puzzle[i, j] = int(value)
            else:
                puzzle[i, j] = 0
    for i in range(9):
        for j in range(9):
            entries[i][j].config(bg="white")
    incorrect = False
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != solution[i][j]:
                entries[i][j].config(bg="red")
                incorrect = True
            else:
                entries[i][j].config(bg="green")

    if incorrect:
        messagebox.showerror("Incorrect Solution", "The solution entered is incorrect.")
    else:
        messagebox.showinfo("Correct Solution", "The solution entered is correct.")

def generate_puzzle(difficulty):
    global test
    test = random_generate(difficulty)
    for i in range(9):
        for j in range(9):
            entries[i][j].delete(0, tk.END)
            val = test.variables[i * 9 + j].value
            if val != 0:
                entries[i][j].insert(0, val)
                entries[i][j].config(state="disabled")
            else:
                entries[i][j].config(state="normal")

def set_initial_puzzle():
    global test
    puzzle = np.zeros((9, 9), dtype=int)
    for i in range(9):
        for j in range(9):
            value = entries[i][j].get()
            if value.isdigit():
                puzzle[i, j] = int(value)
            else:
                puzzle[i, j] = 0

    test = CSP()
    for i in range(9):
        for j in range(9):
            k = i // 3 * 3 + j // 3
            test.variables.append(Variable(i, j, k, puzzle[i, j]))
    
    if AC3(test):
        messagebox.showinfo("Initial Puzzle Set", "Initial puzzle has been set successfully.")
    else:
        messagebox.showerror("Invalid State", "The initial Sudoku puzzle state is invalid.")

def reset_board():
    for i in range(9):
        for j in range(9):
            entries[i][j].config(state="normal")
            entries[i][j].config(bg="white")
            entries[i][j].delete(0, tk.END)

# Initialize the main window
root = tk.Tk()
root.title("Sudoku Solver")
canvas = tk.Canvas(root, width=400, height=400)
canvas.grid(row=0,column=0,rowspan=9,columnspan=9)
canvas.create_line(135, 0, 135, 400, fill="grey", width=10) #Vertical 1
canvas.create_line(0, 135, 400, 135, fill="grey", width=10) #Horizontal 1
canvas.create_line(270, 0, 270, 400, fill="grey", width=10) #Vertical 2
canvas.create_line(0, 270, 400, 270, fill="grey", width=10) #Horizontal 2

# Create a grid of entry widgets
entries = [[tk.Entry(root, width=2, font=("Arial", 18), justify="center") for _ in range(9)] for _ in range(9)]

for i in range(9):
    for j in range(9):
        entries[i][j].grid(row=i, column=j, padx=5, pady=5)


# Difficulty selection buttons
button_frame = tk.Frame(root)
button_frame.grid(row=9, column=0, columnspan=9, pady=10)

easy_button = tk.Button(button_frame, text="Easy", command=lambda: generate_puzzle(0.1))
easy_button.pack(side="left", padx=10)

medium_button = tk.Button(button_frame, text="Medium", command=lambda: generate_puzzle(0.3))
medium_button.pack(side="left", padx=10)

hard_button = tk.Button(button_frame, text="Hard", command=lambda: generate_puzzle(0.5))
hard_button.pack(side="left", padx=10)

set_initial_button = tk.Button(button_frame, text="Set Initial Puzzle", command=set_initial_puzzle)
set_initial_button.pack(side="left", padx=10)

# Solve and Reset buttons
solve_button = tk.Button(root, text="Solve", command=solve_sudoku)
solve_button.grid(row=10, column=0, columnspan=4, pady=10)

submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.grid(row=10, column=2, columnspan=4, pady=10)

reset_button = tk.Button(root, text="Reset", command=reset_board)
reset_button.grid(row=10, column=4, columnspan=4, pady=10)

# Run the GUI
root.mainloop()