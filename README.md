# AI Game Solvers: Sudoku and Connect Four

This repository contains two Python AI projects built around classical search and reasoning algorithms:

- `sudoku.py`: a Sudoku solver and generator using Constraint Satisfaction Problem techniques
- `connect4.py`: a Connect Four AI opponent using Minimax, Alpha-Beta pruning, and Expectiminimax

Both projects include graphical interfaces built with Tkinter and are designed to demonstrate practical AI engineering concepts through interactive games.

## Project Overview

This project focuses on applying foundational Artificial Intelligence algorithms to rule-based games. Sudoku is handled as a constraint reasoning problem, while Connect Four is handled as an adversarial search problem.

As an AI engineer, this repository highlights the ability to model problems formally, design search strategies, evaluate states with heuristics, and visualize algorithm behavior through user interfaces.

## Repository Structure

```text
.
|-- sudoku.py
|-- connect4.py
`-- README.md
```

## 1. Sudoku Solver and Generator

`sudoku.py` is a Python application that models Sudoku as a Constraint Satisfaction Problem. Each cell is represented as a variable with a domain of possible values from 1 to 9.

### Key Features

- Generate Sudoku puzzles with easy, medium, and hard difficulty levels
- Solve Sudoku puzzles automatically
- Enter custom puzzles manually
- Validate user-submitted solutions
- Visualize solving progress through the GUI
- Reset the board and start again

### AI Techniques Used

- Constraint Satisfaction Problem modeling
- AC-3 arc consistency algorithm
- Domain pruning
- Recursive backtracking search
- Minimum Remaining Values style variable selection

### How It Works

The Sudoku solver first applies AC-3 to remove impossible values from each variable domain. If the puzzle is not fully solved after constraint propagation, recursive backtracking is used to assign values to remaining cells. The solver prioritizes cells with smaller domains to reduce the search space.

The puzzle generator creates a solved board, removes values according to the selected difficulty, and checks that the puzzle remains solvable.

## 2. Connect Four AI

`connect4.py` is a Tkinter-based Connect Four game where the user plays against an AI agent. The AI can run using different decision-making strategies selected before gameplay.

### Key Features

- Human vs AI Connect Four gameplay
- Depth selection for AI search
- Minimax search mode
- Alpha-Beta pruning mode
- Expectiminimax mode for probabilistic move outcomes
- Heuristic board evaluation
- Node expansion counting
- Execution time reporting
- Search tree visualization using Tkinter Treeview

### AI Techniques Used

- Adversarial search
- Minimax algorithm
- Alpha-Beta pruning
- Expectiminimax search
- Heuristic evaluation functions
- Game-tree expansion and visualization

### How It Works

The Connect Four AI evaluates possible future moves up to a selected depth. In Minimax mode, it assumes both players act optimally. In Alpha-Beta mode, it improves Minimax by pruning branches that cannot affect the final decision. In Expectiminimax mode, the AI accounts for uncertainty by assigning probabilities to nearby column outcomes.

The evaluation function scores board states based on center control, winning windows, blocking opportunities, and offensive threats.

## Requirements

Install Python 3 and NumPy:

```bash
pip install numpy
```

Tkinter is included with most standard Python installations. If Tkinter is missing, install it through your Python distribution or operating system package manager.

## How to Run

Run the Sudoku project:

```bash
python sudoku.py
```

Run the Connect Four project:

```bash
python connect4.py
```

## Usage Notes

For Sudoku:

- Use the difficulty buttons to generate a puzzle.
- Use `Set Initial Puzzle` to load a manually entered puzzle.
- Use `Solve` to let the AI solve the board.
- Use `Submit` to validate your answer.

For Connect Four:

- Enter the search depth first.
- Select one of the AI modes: Minimax, Alpha Beta, or Expectiminimax.
- Click a column on the board to make your move.
- The AI responds based on the selected algorithm.
- After each AI move, the terminal prints timing and node expansion information.

## AI Engineering Highlights

This repository demonstrates:

- Formal problem modeling
- Constraint-based reasoning
- Deterministic and probabilistic search
- Search-space optimization
- Heuristic design
- GUI-based algorithm visualization
- Runtime and node-expansion analysis

## Limitations

- Sudoku puzzle generation checks solvability but does not guarantee a unique solution.
- Connect Four search performance depends heavily on the selected depth.
- The Connect Four GUI opens an additional tree window after AI moves to display the search tree.
- Both projects are written as standalone scripts and can be further improved by separating GUI, algorithm, and utility logic into modules.

## Author

Developed by an AI engineer as a practical demonstration of classical AI algorithms, game search, constraint reasoning, and Python GUI development.
