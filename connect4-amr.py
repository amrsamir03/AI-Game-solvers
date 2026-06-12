import numpy as np
import math
import random
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.ttk import * 
import time

blue = (0,0,255)
red = (255,0,0)
yellow = (255,255,0)
white = (255,255,255)
rows = 6
columns = 7
tile = 100
player = 1 #red
ai = 2 #yellow
mode = 0 # 1 without pruning 2 with pruning 3 expectiminimax
K = 0 #depth

class Node:
    def __init__(self, value):
        self.child = []
        self.value = value
        self.level = 0
        self.type = "max"

def count_nodes(n,s):
    if n.child == []:
        return 0
    else:
        return len(n.child)+sum(count_nodes(m,s) for m in n.child)

def insertgui(tree,parent,node):
    curr=tree.insert(parent,"end",text=f"{node.value} {node.type}")
    for x in node.child:
        insertgui(tree,curr,x)

def tree(n):
    root = tkinter.Tk()
    tree = ttk.Treeview(root)
    tree.column("#0", width=200, minwidth=200)
    
    #tree.heading("#0", text="", anchor=tkinter.W)

    insertgui(tree,"",n)
    tree.pack(expand=True, fill="both")
    root.mainloop()

def change_mode(canva,num):
    global mode
    global K
    mode=num
    if depth.get()=="":
        print("Please enter depth:")
    else:
        K = int(depth.get())
        canva.destroy()

def create_board():
    board = np.zeros((rows,columns))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece
 
def is_valid_location(board, col):
    if board[0][col] != 0: #full column
        return False
    return True
 
def get_next_empty(board, col):
    for r in range(rows-1,-1,-1):
        if board[r][col] == 0:
            return r
        
def draw_board(board):
    for i in range(rows):
        for j in range(columns):
            canvas.create_oval(j*100+50-35,i*100+50-35+50,j*100+50+35,i*100+50+35+50, fill="white", outline="black")

    for i in range(rows):
        for j in range(columns):
            if board[i][j]==1:
                canvas.create_oval(j*100+50-35,i*100+50-35+50,j*100+50+35,i*100+50+35+50, fill="red", outline="black")
            elif board[i][j]==2:
                canvas.create_oval(j*100+50-35,i*100+50-35+50,j*100+50+35,i*100+50+35+50, fill="yellow", outline="black")

def final_score(board,game_over,connectfour):
    player = 0
    ai = 0
    if not game_over:
        return
    #count horizontal
    for i in range (rows):
        for j in range (4):
            if board[i][j] == board[i][j+1] == board[i][j+2] == board[i][j+3]:
                if board[i][j] == 1:
                    player = player + 1
                elif board[i][j] == 2:
                    ai = ai + 1 

    #count vertical
    for i in range (columns):
        for j in range (3):
            if board[j][i] == board[j+1][i] == board[j+2][i] == board[j+3][i]:
                if board[j][i] == 1:
                    player = player + 1
                elif board[j][i] == 2:
                    ai = ai + 1 

    #count -ve diagonal
    for i in range(3):
        for j in range(4):
            if board[i][j] == board[i+1][j+1] == board [i+2][j+2] == board[i+3][j+3]:
                if board[i][j] == 1:
                    player = player + 1
                elif board[i][j] == 2:
                    ai = ai + 1 

    #count +ve diagonal
    for i in range(3):
        for j in range(3,columns):
            if board[i][j] == board[i+1][j-1] == board [i+2][j-2] == board[i+3][j-3]:
                if board[i][j] == 1:
                    player = player + 1
                elif board[i][j] == 2:
                    ai = ai + 1 

    canvas.create_text(350, 30, text=f"Your score: {player}   AI score: {ai}   Final score: {ai-player}", font=('Ariel', 24), fill="white")


def evaluate(board, piece):
    score = 0
    center=3

    for i in range(rows):
        if board[i][center] == 2:
            score=score+100
        elif board[i][center]==1:
            score=score-100

    for i in range(rows):
        for j in range(columns):
            if board[i][j] == piece:
                score += 100 * (3-(abs(j-3)))/5

    for i in range(rows):
        for j in range(4):
            window = [board[i][j+k] for k in range(4)]
            if window.count(2) == 4:
                score = score + 600
            elif window.count(1) == 4:
                score = score - 1000

    for i in range(columns):
        for j in range(3):
            window = [board[j+k][i] for k in range(4)]
            if window.count(2) == 4:
                score = score + 600
            elif window.count(1) == 4:
                score = score - 1000

    for i in range(rows):
        for j in range(4):
            window = [board[i][j+k] for k in range(4)]
            player = window.count(1)
            empty = window.count(0)
            ai = window.count(2)
            if ai == 3 and empty == 1:
                score = score + 100
            elif ai == 2 and empty == 2:
                score = score + 50
            elif player == 3 and empty == 1:
                score = score - 500
            elif player == 2 and empty == 2:
                score = score - 100
            elif player == 3 and ai == 1:
                score = score + 500

    for i in range(columns):
        for j in range(3):
            window = [board[j+k][i] for k in range(4)]
            player = window.count(1)
            empty = window.count(0)
            ai = window.count(2)
            if ai == 3 and empty == 1:
                score = score + 100
            elif ai == 2 and empty == 2:
                score = score + 50
            elif player == 3 and empty == 1:
                score = score - 500
            elif player == 2 and empty == 2:
                score = score - 100
            elif player == 3 and ai == 1:
                score = score + 500

    for i in range(3):
        for j in range(4):
            window = [board[i+k][j+k] for k in range(4)]
            player = window.count(1)
            empty = window.count(0)
            ai = window.count(2)
            if ai == 3 and empty == 1:
                score = score + 100
            elif ai == 2 and empty == 2:
                score = score + 50
            elif player == 3 and empty == 1:
                score = score - 500
            elif player == 2 and empty == 2:
                score = score - 100
            elif player == 3 and ai == 1:
                score = score + 500

            window = [board[i+k][j+3-k] for k in range(4)]
            if ai == 3 and empty == 1:
                score = score + 100
            elif ai == 2 and empty == 2:
                score = score + 50
            elif player == 3 and empty == 1:
                score = score - 500
            elif player == 2 and empty == 2:
                score = score - 100
            elif player == 3 and ai == 1:
                score = score + 500
    return score

    

def minimax(board, depth, max, piece,level,nn):
    available = [col for col in range(columns) if is_valid_location(board, col)]
    if depth == 0 or len(available) == 0:
        evaluation = evaluate(board, piece)
        nn.value=evaluation
        return evaluation, None
    best = random.choice(available)

    if max == True:
        max_score = -math.inf
        for col in available:
            row = get_next_empty(board,col)
            clone = board.copy()
            drop_piece(clone,row,col,ai)
            n=Node(0)
            nn.child.append(n)
            n.level=level+1
            n.type = "min"
            score = minimax(clone,depth-1,False,piece,level+1,n)[0]
            n.value=score
            if score > max_score:
                max_score = score
                best = col
        return max_score, best

    elif max == False:
        min_score = math.inf
        for col in available:
            row = get_next_empty(board,col)
            clone = board.copy()
            drop_piece(clone,row,col,player)
            n=Node(0)
            nn.child.append(n)
            n.level=level+1
            n.type = "max"
            score = minimax(clone,depth-1,True,piece,level+1,n)[0]
            n.value=score
            if score < min_score:
                min_score = score
                best = col
        return min_score, best

def alphabeta(board, depth, max, alpha, beta, piece,level,nn):
    available = [col for col in range(columns) if is_valid_location(board, col)]
    if depth == 0 or len(available) == 0:
        evaluation = evaluate(board, piece)
        nn.value=evaluation
        return evaluation, None
    best = random.choice(available)

    if max:
        max_score = -math.inf
        for col in available:
            row = get_next_empty(board,col)
            clone = board.copy()
            drop_piece(clone,row,col,ai)
            n=Node(0)
            nn.child.append(n)
            n.level=level+1
            n.type = "min"
            score = alphabeta(clone,depth-1,False,alpha,beta,piece,level+1,n)[0]
            n.value=score
            if score > max_score:
                max_score = score
                best = col
            alpha = alpha if alpha > score else score
            if beta <= alpha:
                break
        return max_score, best

    else:
        min_score = math.inf
        for col in available:
            row = get_next_empty(board,col)
            clone = board.copy()
            drop_piece(clone,row,col,player)
            n=Node(0)
            nn.child.append(n)
            n.level=level+1
            n.type = "max"
            score = alphabeta(clone,depth-1,True,alpha,beta,piece,level+1,n)[0]
            n.value=score
            if score < min_score:
                min_score = score
                best = col
            beta = beta if beta < score else score
            if beta <= alpha:
                break
        return min_score, best
    
def expectiminimax(board, depth, max, piece, level, nn):
    available = [col for col in range(columns) if is_valid_location(board, col)]
    if depth == 0 or len(available) == 0:
        evaluation = evaluate(board, piece)
        nn.value=evaluation
        return evaluation, None
    best = random.choice(available)

    if max:
        score1=-math.inf
        score2=-math.inf
        score3=-math.inf
        max_score= -math.inf
        for column in range(columns):
            ch=Node(0)
            nn.child.append(ch)
            ch.type="chance"
            ch.level=level+1
            if column in available:
                row = get_next_empty(board,column)
                clone = board.copy()
                drop_piece(clone,row,column,ai)
                n=Node(0)
                ch.child.append(n)
                n.level=level+2
                n.type="min"
                score1 = expectiminimax(clone,depth-1,False,piece,level+1,n)[0]
                n.value=score1
            if column+1 < 7 and column+1 in available:
                row2 = get_next_empty(board,column+1)
                clone2 = board.copy()
                drop_piece(clone2,row2,column+1,ai)
                n2=Node(0)
                ch.child.append(n2)
                n2.level=level+2
                n2.type="min"
                score2 = expectiminimax(clone2,depth-1,False,piece,level+1,n2)[0]
                n2.value=score2
            if column-1>=0 and column-1 in available:
                row3 = get_next_empty(board,column-1)
                clone3 = board.copy()
                drop_piece(clone3,row3,column-1,ai)
                n3=Node(0)
                ch.child.append(n3)
                n3.level=level+2
                n3.type="min"
                score3 = expectiminimax(clone3,depth-1,False,piece,level+1,n3)[0]
                n3.value=score3
            
            if column+1 in available and column-1 in available:
                score = score1 * 0.6 + score2 * 0.2 + score3 * 0.2
            elif column + 1 in available:
                score = score1 * 0.75 + score2 * 0.25
            elif column-1 in available:
                score = score1 * 0.75 + score3 * 0.25
            else:
                score = score1
            if score > max_score:
                max_score = score
                best = column
        return max_score, best
    
    if not max:
        score1=-math.inf
        score2=-math.inf
        score3=-math.inf
        min_score=math.inf
        for column in range(columns):
            ch=Node(0)
            nn.child.append(ch)
            ch.type="chance"
            ch.level=level+1
            if column in available:
                row = get_next_empty(board,column)
                clone = board.copy()
                drop_piece(clone,row,column,player)
                n=Node(0)
                ch.child.append(n)
                n.level=level+2
                n.type="max"
                score1 = expectiminimax(clone,depth-1,True,piece,level+1,n)[0]
                n.value=score1
            if column+1 < 7 and column+1 in available:
                row2 = get_next_empty(board,column+1)
                clone2 = board.copy()
                drop_piece(clone2,row2,column+1,player)
                n2=Node(0)
                ch.child.append(n2)
                n2.level=level+2
                n2.type="max"
                score2 = expectiminimax(clone2,depth-1,True,piece,level+1,n2)[0]
                n2.value=score2
            if column-1>=0 and column-1 in available:
                row3 = get_next_empty(board,column-1)
                clone3 = board.copy()
                drop_piece(clone3,row3,column-1,player)
                n3=Node(0)
                ch.child.append(n3)
                n3.level=level+2
                n3.type="max"
                score3 = expectiminimax(clone3,depth-1,True,piece,level+1,n3)[0]
                n3.value=score3
            
            if column+1 in available and column-1 in available:
                score = score1 * 0.6 + score2 * 0.2 + score3 * 0.2
            elif column+1 in available:
                score=score1*0.75+score2*0.25
            elif column-1 in available:
                score=score1*0.75+score3*0.25
            else:
                score=score1
            if score < min_score:
                min_score = score
                best = column
        return min_score, best


def click(event,canvas,turn,game_over):
    start_time=time.time()
    if mode < 1 or mode > 3 or K == 0:
        print("Please select mode and depth")
        return

    if turn == player and not game_over:
            col=event.x//tile
            if is_valid_location(board,col):
                row=get_next_empty(board,col)
                drop_piece(board,row,col,1)
                draw_board(board)
                turn = ai
    if turn == ai and not game_over:
        if mode == 1:
            n = Node(0)
            n.level = 0
            val, col = minimax(board, K, True, 2,0,n)
            n.value = val
            if col is not None:
                row = get_next_empty(board, col)
                drop_piece(board, row, col, ai)
                turn = player
                draw_board(board)
                game_over = True
            for i in range(columns):
                if(get_next_empty(board,i))!=None:
                    game_over = False
            final_score(board,game_over,Connect_Four)
            end_time=time.time()
            print("Time:",(end_time-start_time)*1000,"Milliseconds")
            print("Nodes expanded:",count_nodes(n,0))
            tree(n)
        elif mode == 2:
            n=Node(0)
            n.level=0
            val, col = alphabeta(board, K, True, -math.inf, math.inf, 2,0,n)
            n.value = val
            if col is not None:
                row = get_next_empty(board, col)
                drop_piece(board, row, col, ai)
                turn = player
                draw_board(board)
                game_over = True
            for i in range(columns):
                if(get_next_empty(board,i))!=None:
                    game_over = False
            final_score(board,game_over,Connect_Four)
            end_time=time.time()
            print("Time:",(end_time-start_time)*1000,"Milliseconds")
            print("Nodes expanded:",count_nodes(n,0))
            tree(n)
        elif mode == 3:
            n=Node(0)
            n.level=0
            val, col = expectiminimax(board, K, True, 2, 0, n)
            n.value = val
            if col is not None:
                row = get_next_empty(board, col)
                drop_piece(board, row, col, ai)
                turn = player
                draw_board(board)
                game_over = True
            for i in range(columns):
                if(get_next_empty(board,i))!=None:
                    game_over = False
            final_score(board,game_over,Connect_Four)
            end_time=time.time()
            print("Time:",(end_time-start_time)*1000,"Milliseconds")
            print("Nodes expanded:",count_nodes(n,0))
            tree(n)

board = create_board()
game_over = False
turn = player
Connect_Four = Tk()
Connect_Four.title("Connect Four")

mode_frame = Tk()
canvas= tkinter.Canvas(mode_frame,width=0,height=0,bg="blue")
canvas.pack()
depth_label = tkinter.Label(mode_frame, text="Enter max depth:", font=("times new roman", 12))
depth_label.pack(side=tkinter.TOP,pady=5)
depth = tkinter.Entry(mode_frame, font=("times new roman", 12), width=10)
depth.pack(side=tkinter.TOP,pady=20)
btn1 = tkinter.Button(mode_frame, text="Minmax",command=lambda:change_mode(mode_frame,1))
btn1.pack(side=tkinter.TOP,pady=20) 
btn2 = tkinter.Button(mode_frame, text="Alpha Beta",command=lambda:change_mode(mode_frame,2))
btn2.pack(side=tkinter.TOP,pady=20) 
btn3 = tkinter.Button(mode_frame, text="Expecti",command=lambda:change_mode(mode_frame,3))
btn3.pack(side=tkinter.TOP,pady=20)

canvas= tkinter.Canvas(Connect_Four,width=700,height=700,bg="blue")
canvas.pack()
draw_board(board)
canvas.bind("<Button-1>", lambda event: click(event, canvas, turn,game_over))
Connect_Four.mainloop()