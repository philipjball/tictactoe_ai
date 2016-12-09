# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 01:20:02 2016

@author: philip.ball
"""

import random
import numpy as np

def drawBoard(board):
    # This function prints out the board that it was passed.

    # "board" is a list of 9 strings representing the board
    print('   |   |')
    print(' ' + board[0] + ' | ' + board[1] + ' | ' + board[2])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[3] + ' | ' + board[4] + ' | ' + board[5])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[6] + ' | ' + board[7] + ' | ' + board[8])
    print('   |   |')

# this function generates our starting point (in this case, just a blank board)
def Generator():
    board = np.array([' ']*9)
    return(board)
    
class PerfSyst:
    # this class runs the games with our latest trained AI (represented by weights)
    
    def __init__(self, board, weights):
        self.board = board
        self.weights = weights
            
    # function which plays a game (note that AI starts 1st and chooses 'X')
    def play_game(self):
        board_trace = np.empty((12,self.board.size), dtype=np.str)
        board_trace[0,:] = self.board   # initial empty board
        i = 1
        while True:
            self.board = self.make_a_move('X', self.board, weights)    # AI move
            board_trace[i,:] = self.board
            i += 1
            if self.over_check():
                break
            self.board = self.random_play('O', self.board)    # random move
            board_trace[i,:] = self.board
            if self.over_check():
                break
            i += 1
        #drawBoard(self.board)
        board_trace = board_trace[~np.all(board_trace == '', axis = 1)]    # remove rows with all 0s
        return(board_trace)
    
    # checks if the board is over
    def over_check(self):
        board_array = np.reshape(self.board,(3,3))  # create the array form
        if in_a_row('O',board_array) or in_a_row('X',board_array) or (self.board != ' ').all(): # if there are 3 in a row or a full board
            return(True)    # game is over
        else:
            return(False)   # otherwise play on
        
    # our AI which makes a move based on the best next board according to its weights
    def make_a_move(self, Sym, board, weights):
        V = np.zeros(board.size)  # initialise the array where we hold the scores
        for i in range(0,board.size):    # go through each entry on the board
            if board[i] == ' ': # if it's a blank
                board_test = np.array(board[:])  # set a test board (need to re-array to make it a copy, not a pointer)
                board_test[i] = Sym  # assign the symbol to the 'i'th blank
                x = extract_feat(board_test)   # extract the features of this test board
                V[i] = np.dot(x, weights)   # calculate the V score
            else:   # if it isn't a blank
                V[i] = float('-inf')   # set the V score to be - infinity (so we don't choose it)
        bestPlay = V.argmax()   # get the max V score's index
        board[bestPlay] = Sym  # set the appropriate symbol to make the best play
        return(board)
       
    # a dumb AI which makes a random play, returning an updated board
    def random_play(self, Sym, board):
        while True:
            b_rand = random.randint(0,8)
            if board[b_rand] == ' ':
                break
        board[b_rand] = Sym     # fill a random place with the symbol allocated
        return(board)        

    # oppotunity to play a human
    def human_play(self, Sym, board):
        while True:
        a = input('Type in your cell number (1-9): ')
        a = a - 1
        
        
# function which extracts the features of a board
def extract_feat(board):
    board_array = np.reshape(board,(3,3))   # reshape into grid form for easier checking
    x = np.zeros(7)
    x[0] = 1
    cols = np.transpose(board_array)
    diag = np.row_stack((np.diag(board_array),np.diag(cols)))
    final = np.row_stack((board_array,cols,diag))
    for i in range(0,8):
        blank = np.count_nonzero(final[i,:] == ' ')
        X_cnt = np.count_nonzero(final[i,:] == 'X')
        O_cnt = np.count_nonzero(final[i,:] == 'O')
        if X_cnt == 2 and blank == 1:
            x[1] += 1
        elif O_cnt == 2 and blank == 1:
            x[2] += 1
        elif X_cnt == 1 and blank == 2:
            x[3] += 1
        elif O_cnt == 1 and blank == 2:
            x[4] += 1
        elif X_cnt == 3:
            x[5] += 1
        elif O_cnt == 3:
            x[6] += 1
    return(x)

def myturn(StartSym, MySym, board_array):
    #print(board_array)
    if iseven(9 - num_of(' ', board_array)) and StartSym == MySym:
        return(1)
    elif isodd(9 - num_of(' ', board_array)) and StartSym != MySym:
        return(1)
    else:
        return(0)
        
def isodd(Num):
    if Num % 2 == 0:
        return(False)
    else:
        return(True)
        
def iseven(Num):
    if Num % 2 == 0:
        return(True)
    else:
        return(False)
    
# function which counts the number of a nought or cross
def num_of(Sym, board):
    return((board == Sym).sum())   

# function which determines if there are three in a row
def in_a_row(Sym, board_array):
    inarow_cnt = 0
    inarow_cnt += np.apply_along_axis(lambda x: (x == Sym).all(), 0, board_array).sum() # find the number of columns with 3 in a row
    inarow_cnt += np.apply_along_axis(lambda x: (x == Sym).all(), 1, board_array).sum() # find the number of rows with 3 in a row
    inarow_cnt += (np.diag(board_array) == Sym).all() + (np.diag(np.fliplr(board_array)) == Sym).all()    # check diagonals in a row
    if inarow_cnt == 0:
        return(0)
    else:
        return(1)

# function which counts how many rows have two of a symbol 'Sym' a blank (ie: finishing moves possible)
def x_and_blank(Sym, board_array, check_x):
    two_cnt = 0
    two_cnt += np.apply_along_axis(lambda x: check_x(Sym,x), 0, board_array).sum() # find the number of cols with 2 and blank
    two_cnt += np.apply_along_axis(lambda x: check_x(Sym,x), 1, board_array).sum() # find the number of cols with 2 and blank
    two_cnt += check_x(Sym, np.diag(board_array)) + check_x(Sym, np.diag(np.fliplr(board_array)))
    return(two_cnt)

# function which, for a given row, checks if there are two of the same symbol and a blank
def check_two(Sym, r_c_d):
    s_cnt = (r_c_d == Sym).sum()
    blnk_cnt = (r_c_d == ' ').sum()
    if (s_cnt == 2) and (blnk_cnt == 1):
        return(1)
    else:
        return(0)       
        
def check_one(Sym, r_c_d):
    s_cnt = (r_c_d == Sym).sum()
    blnk_cnt = (r_c_d == ' ').sum()
    if (s_cnt == 1) and (blnk_cnt == 2):
        return(1)
    else:
        return(0)
        
# this function creates the training data given our past games (the trace)
def Critic(board_trace, weights):
    r,c = board_trace.shape
    y = np.zeros(r)
    feat = np.zeros((r,weights.size))
    for i in range(0,r):
        feat[i,:] = extract_feat(board_trace[i,:])
    for i in range(0,r):
        board = board_trace[i,:]
        board_array = shapeBoard(board)
        #print(board_array)
        if in_a_row('X', board_array):     # if we hit an end game that we won
            y[i] = 100
        elif in_a_row('O', board_array):    # if we hit an end game that we lost
            y[i] = -100
        elif i == r - 1:   # if it's the last game and we didn't win or lose
            y[i] = 0
        elif i == r - 2:   # otherwise it's an intermediary game, check if it's the penultimate play
            if in_a_row('X', shapeBoard(board_trace[i+1,:])):
                y[i] = 100
            elif in_a_row('O', shapeBoard(board_trace[i+1,:])):
                y[i] = -100
            else:
                y[i] = 0
        else:   # otherwise we estimate the V-score with our current estimated function
            y[i] = np.dot(weights,feat[i+2,:])    # calculate the V estiamte from it
    return(y, feat)

def shapeBoard(board):
    return(np.reshape(board,(3,3)))
    
class Generalizer:
    # this class takes our training examples and adjusts the weights of our latest AI accordingly
    
    # set the learning rate upon initialisation
    def __init__(self, l_rate):
        self.l_rate = l_rate
    
    # stochastic grad-desc on all board types for the last game to get the new weights
    def update_w(self, V_train, feat, weights):
        for i in range(0,V_train.size):
            V_est = np.dot(weights, feat[i,:])
            weights += self.l_rate * (V_train[i] - V_est) * feat[i,:]   # using vector operations, update all weights simultaneously
        return(weights)
        
        
    def mse(self, V_train, board_trace, weights):
        num = V_train.size
        err_sq_sum = 0
        for i in range(0,V_train.size):
            x = extract_feat(board_trace[i,:])
            V_est = np.dot(weights, x)
            error = V_train[i] - V_est
            err_sq_sum += error**2
        return(err_sq_sum/num)
            

# function which runs the entire learning ecosystem, returning the weights, having played N times
def LearningEcoSyst(N, l_rate):
    
    weights = np.array([25.0]*7) # initial weights
        
    for i in range(0,N):
        board = Generator() # generate the board
        game = PerfSyst(board,weights)  # instantiate a new game with said board and current weights
        trace = game.play_game()    # play a game and return the trace of that game
        V_train,feat = Critic(trace, weights)    # create training data based on those games using the predifined algorithm
        G = Generalizer(l_rate)    # instantiate the generaliser/weight modifier with the learning rate
        weights = G.update_w(V_train, feat, weights)   # update the weights based on the training data
    return(weights)

# function which plays the opponent N times with input weights and counts of win lose draw
def playOpponent(N, weights):
    WLD = np.zeros(3)
    for i in range(0,N):
        board_init = Generator()    # generate the blank board
        game = PerfSyst(board_init,weights)
        trace = game.play_game()
        last_b = trace[-1:,:]
        WLD += outcome(last_b)
    return(WLD)

def outcome(board_end):
    x = extract_feat(board_end)
    if x[1] == 1:
        WLD = np.array([1,0,0])
    elif x[2] == 1:
        WLD = np.array([0,1,0])
    else:
        WLD = np.array([0,0,1])
    return(WLD)

def playHooman(weights):
    
        
trains = [10000]
weights = np.zeros(7)
weights_comp = []

for t in trains:
    weights = LearningEcoSyst(t,0.01)
    WLD = playOpponent(100,weights)
    print('For '+ str(t) + ' training games, WLD is ' + str(WLD))
    #print('Weights are: ' + str(weights))

#train(trains, weights)