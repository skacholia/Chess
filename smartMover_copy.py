import random
import chess
import chess.polyglot
import numpy as np
#MUST INSTALL numpy version 1.19.3#
#pip install numpy==1.19.3#
import time as t
#Chess AI V5
#MiniMax Agent
#November 18, 2020

#Did everything except grid and pawn stuff

class Player:

    def __init__(self, board, color, time):
        self.color = color
        self.depth = 0
        self.poseval = [[],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5, 0.5, -0.5, 1.0, 0.0, 0.0, -1.0, -0.5, 0.5, 0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0, 0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5, 1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0, 3, 4, 4, 4, 4, 4, 4, 3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0, -4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0, -3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0, -3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0, -3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0, -3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0, -4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0, -5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
            [-2, -1, -1, -1, -1, -1, -1, -2, -1, 0.5, 0, 0, 0, 0, 0.5, -1,  -1, 1, 1, 1, 1, 1, 1, -1, -1, 0, 1, 1, 1, 1, 0, -1, -1, 0.5, 0.5, 1, 1, 0.5, 0.5, -1, -1, 0, 0.5, 1, 1, 0.5, 0, -1, -1, 0, 0, 0, 0, 0, 0, -1, -2, -1, -1, -1, -1, -1, -1, -2],
            [0, 0, 1, 3, 3, 1, 0, 0, -.5, 0, 0, 0, 0, 0, 0, -.5,-.5, 0, 0, 0, 0, 0, 0, -.5,-.5, 0, 0, 0, 0, 0, 0, -.5,-.5, 0, 0, 0, 0, 0, 0, -.5,-.5, 0, 0, 0, 0, 0, 0, -.5, .5, 1, 1, 1, 1, 1, 1, .5, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [-2, -1, -1, -.5, -.5, -1, -1, -2, -1, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1, -1, .5, .5, .5, .5, .5, 0.0, -1, 0, 0, 0.5, .5, .5, .5, 0.0, -.5, -.5, 0, .5, .5, .5, .5, 0, -.5, -1, 0, .5, .5, .5, .5, 0, -1, -1, 0, 0, 0, 0, 0, 0, -1, -2, -1, -1, -.5, -.5, -1, -1, -2],
            [6, 7, 4, 0, 0, 4, 7, 6, 2, 2, 0, 0, 0, 0, 2, 2, -1, -2, -2, -2, -2, -2, -2, -1,-2, -3, -3, -4, -4, -3, -3, -2, -3, -4, -4, -5, -5, -4, -4, -3,-3, -4, -4, -5, -5, -4, -4, -3,-3, -4, -4, -5, -5, -4, -4, -3,-3, -4, -4, -5, -5, -4, -4, -3]]
        self.mateval = [0, 10, 30, 30, 50, 90, 200]
        self.start = t.time()
        self.nodes = 0

    #Returns the best action for the player
    def move(self, board, time):
        try:
            #Selfmade opening book using https://rebel13.nl/download/polyglot.html
            return chess.polyglot.MemoryMappedReader("data/book.bin").weighted_choice(board).move
        except:
            self.start = t.time()      
            bestMove = None
            bestMoveScore = float('-inf')
            
            self.depth = 2
            while t.time() - self.start <= 0.2:
                tempTime = t.time()

                alpha, beta = float('-inf'), float('inf')
                
                #If there are no queens, the game is set as End Game
                if len(board.pieces(chess.QUEEN, self.color)) == 0 and len(board.pieces(chess.QUEEN, not self.color)) == 0:
                    self.kingTable = self.kingEndTable

                push, pop, negamax = board.push, board.pop, self.negamax
                for move in self.sortMoves(board, list(board.legal_moves)):
                    push(move)
                    score = -negamax(board, 0, -beta, -alpha)#Implementation of minimax
                    pop()

                    if score > alpha:
                        alpha = score
                        if score > bestMoveScore:
                            bestMoveScore = score
                            bestMove = move

                    self.kingTable = self.kingMiddleTable
                
                self.depth += 1
                time -= t.time() - tempTime
    
            return bestMove

        
    def evaluate(self, board):
        total = 0
        for square in board:
            total += matheuristic(square)
        return total
   
    def matheuristic(self, square):
        piece = self.grid[square]
        if (piece > 0):
            return self.mateval[piece] + self.poseval[piece][square]
        return -self.mateval[-piece] - self.poseval[-piece][(7 - square // 8) * 8 + square % 8]


    def negamax(self, board, currentDepth, alpha, beta):
        if currentDepth >= self.depth or len(list(board.legal_moves)) == 0 or board.is_game_over():
            return self.quiesce(board, alpha, beta, 0) #last term is the max quiesce depth

        push, pop, negamax = board.push, board.pop, self.negamax
        for move in self.sortMoves(board, list(board.legal_moves)):
            push(move)
            score = -negamax(board, currentDepth + 1, -beta, -alpha)
            pop()
            
            #Alpha-Beta Pruning
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
        
        return alpha

    def quiesce(self, board, alpha, beta, depthLeft):
        stand_pat = self.evaluate(board)

        #Alpha-Beta Pruning in Quiescence
        if depthLeft == 0:
            return stand_pat
        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat
        
        #Loop will output capture moves
        moves = []
        is_capture = board.is_capture
        append = moves.append
        for move in list(board.legal_moves):
            if is_capture(move):
                append(move)

        push, pop, quiesce = board.push, board.pop, self.quiesce
        for move in moves:
            push(move)
            score = -quiesce(board, -beta, -alpha, depthLeft - 1)
            pop()

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
            
        return alpha


    def sortMoves(self, board, moves):
        sortedMoves = np.empty((0, 2))
        
        push, pop, array, append, miniEval = board.push, board.pop, np.array, np.append, self.miniEval
        for move in moves:
            push(move)
            sortedMoves = append(sortedMoves, array([[move, miniEval(board)]]), axis = 0)
            pop()

        if board.turn == self.color:
            return sortedMoves[sortedMoves[:,1].argsort()[::-1]][:,0]
        else:
            return sortedMoves[sortedMoves[:,1].argsort()][:,0]
    
    
    def miniEval(self, board):
        if board.is_checkmate():
            return float('inf')
        
        score = 0

        #Don't include (chess.KING, 0),
        pieces, color = board.pieces, self.color
        pawn, bishop, queen, knight, rook = chess.PAWN, chess.BISHOP, chess.QUEEN, chess.KNIGHT, chess.ROOK
        for (piece, value) in [(pawn, 100),
                           (bishop, 333),
                           (queen, 950),
                           (knight, 305),
                           (rook, 563)]:
            score += (len(pieces(piece, color)) - len(pieces(piece, not color))) * value
        
        return score