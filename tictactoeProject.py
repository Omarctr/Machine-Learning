from math import inf
import random
import tkinter as tk
from tkinter import messagebox

def checkWinner(board, player):
    # 0 | 1 | 2
    # 3 | 4 | 5
    # 6 | 7 | 8
    # visualizing for me
    wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    return any(board[a] == board[b] == board[c] == player for a, b, c in wins)

def miniMax(board, mimax):
    if checkWinner(board, 'X'):
        return 1
    if checkWinner(board, 'O'):
        return -1
    if ' ' not in board:
        return 0
    
    best = -inf if mimax else inf

    for i in range(9):
        if board[i] == ' ':
            board[i] = 'X' if mimax else 'O'
            score = miniMax(board, not mimax)
            board[i] = ' '
            best = max(best, score) if mimax else min(best, score)
    return best
    
def miniMax_move(board):
    best, move = -inf, None

    for i in range(9):
        if board[i] == ' ':
            board[i] = 'X'
            score = miniMax(board, False)
            board[i] = ' '

            if score > best:
                best, move = score, i
    return move
    

def greedy(board):
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'X'
            if checkWinner(board, 'X'):
                return i
            board[i] = ' '
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            if checkWinner(board, 'O'):
                board[i] = ' '
                return i
            board[i] = ' '
    empty = [i for i in range(9) if board[i] == ' ']
    return random.choice(empty) if empty else None
    

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("TicTacToe (اكس او)")
        self.root.resizable(False, False)
        self.mode = tk.StringVar(value = 'minimax')
        self.board = [' '] * 9
        self.buttons = []
        self.aiFirst = random.choice([True, False])
        self.buildUI()
        self.startGame()

    def buildUI(self):
        top = tk.Frame(self.root, pady = 8)
        top.pack()
        tk.Label(top, text = 'AI mode: ', font = ('Arial', 11)).pack(side  = 'left', padx = 5)
        for text,  val in [('Minimax', 'minimax'), ('Greedy', 'greedy')]:
            tk.Radiobutton(top, text = text, variable = self.mode, value = val).pack(side='left')

        self.status = tk.Label(self.root, text = 'AI is thinking...', font = ('Arial', 12), fg = 'gray')
        self.status.pack(pady = 4)

        frame = tk.Frame(self.root)
        frame.pack(padx=20, pady=10)
        for i in range(9):
            btn = tk.Button(frame, text = ' ', font = ('Arial', 28, 'bold'), width = 4, height = 2, bg = 'white', command = lambda i=i : self.humanMove(i))
            btn.grid(row = i // 3, column = i % 3, padx = 4, pady = 4)
            self.buttons.append(btn)
            
        tk.Button(self.root, text = 'New game', font = ('Arial', 11), command = self.reset, padx = 10).pack(pady = 8)

    def changeStatus(self, msg , color = 'gray'):
        self.status.config(text = msg, fg = color)
        
    def startGame(self):
        if self.aiFirst:
            self.changeStatus('AI is thinking...')
            self.root.after(300, self.aiTurn)
        else:
            self.changeStatus('Your turn (O)')
        
    def humanMove(self, i):
        if self.board[i] != ' ':
            return
        self.board[i] = 'O'
        self.buttons[i].config(text = 'O', fg = 'green', state = 'disabled')
        if self.endCheck():
            return
        self.changeStatus('Ai is thinking...')
        self.root.after(300, self.aiTurn)

    def aiTurn(self):
        move = miniMax_move(self.board) if self.mode.get() == 'minimax' else greedy(self.board)
        if move is None:
            return
        self.board[move] = 'X'
        self.buttons[move].config(text = 'X', fg = 'blue', state = 'disabled')
        if self.endCheck():
            return
        self.changeStatus('Your turn (O)')
        
    def endCheck(self):
        if checkWinner(self.board, 'X'):
            self.changeStatus('Ai wins', 'red')
            self.disableAll()
            messagebox.showinfo('Game Over', 'AI wins')
            return True
        if checkWinner(self.board, 'O'):
            self.changeStatus('you win', 'blue')
            self.disableAll()
            messagebox.showinfo('Game over', 'You win :)')
            return True
        if ' ' not in self.board:
            self.changeStatus('Its a Draw')
            self.disableAll()
            messagebox.showinfo('Game over', 'its a draw')
            return True
        return False
        
    def disableAll(self):
        for btn in self.buttons:
            btn.config(state = 'disabled')
        
    def reset(self):
        self.board = [' '] * 9 
        for btn in self.buttons:
            btn.config(text = ' ', fg = 'black', bg = 'white', state = 'normal')
        self.aiFirst = random.choice([True, False])
        self.startGame()

root = tk.Tk()
TicTacToe(root)
root.mainloop()
        
    





    
