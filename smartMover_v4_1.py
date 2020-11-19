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

class Player:

    def __init__(self, board, color, time):
        self.color = color
        self.depth = 1.5
        self.stored = np.empty((0, 2))
        self.pawnTable = [
        0,  0,  0,  0,  0,  0,  0,  0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
        5,  5, 10, 25, 25, 10,  5,  5,
        0,  0,  0, 20, 20,  0,  0,  0,
        5, -5,-10,  0,  0,-10, -5,  5,
        5, 10, 10,-20,-20, 10, 10,  5,
        0,  0,  0,  0,  0,  0,  0,  0]

        self.knightTable = [
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50,]

        self.bishopTable = [
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10, 10, 10, 10, 10, 10, 10,-10,
        -10,  5,  0,  0,  0,  0,  5,-10,
        -20,-10,-10,-10,-10,-10,-10,-20,]

        self.rookTable = [
        0,  0,  0,  0,  0,  0,  0,  0,
        5, 10, 10, 10, 10, 10, 10,  5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        0,  0,  0,  5,  5,  0,  0,  0]

        self.queenTable = [
        -20,-10,-10, -5, -5,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5,  5,  5,  5,  0,-10,
        -5,  0,  5,  5,  5,  5,  0, -5,
        0,  0,  5,  5,  5,  5,  0, -5,
        -10,  5,  5,  5,  5,  5,  0,-10,
        -10,  0,  5,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20]

        self.kingMiddleTable = [
        20, 30, 10,  0,  0, 10, 30, 20,
        20, 20,  0,  0,  0,  0, 20, 20,
        -10,-20,-20,-20,-20,-20,-20,-10,
        -20,-30,-30,-40,-40,-30,-30,-20,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30]

        self.kingEndTable = [
        -50,-40,-30,-20,-20,-30,-40,-50,
        -30,-20,-10,  0,  0,-10,-20,-30,
        -30,-10, 20, 30, 30, 20,-10,-30,
        -30,-10, 30, 40, 40, 30,-10,-30,
        -30,-10, 30, 40, 40, 30,-10,-30,
        -30,-10, 20, 30, 30, 20,-10,-30,
        -30,-30,  0,  0,  0,  0,-30,-30,
        -50,-30,-30,-30,-30,-30,-30,-50
        ]
        self.kingTable = self.kingMiddleTable
        self.start = t.time()

    #Returns the best action for the player
    def move(self, board, time):
        self.start = t.time()
        try:
            #Opening book
            return chess.polyglot.MemoryMappedReader("data/bookfish.bin").weighted_choice(board).move
        except:
            ###If checks###
            if len(board.pieces(chess.QUEEN, self.color)) == 0 and len(board.pieces(chess.QUEEN, not self.color)) == 0:
                self.kingTable = self.kingEndTable
            
            moves = list(board.legal_moves)
            bestMoveScore = float('-inf')
            alpha = float('-inf')
            beta = float('inf')
            bestMove = random.choice(moves)
            
            sortedMoves = np.empty((0, 2))
            for move in moves:
                board.push(move)
                sortedMoves = np.append(sortedMoves, np.array([[move, self.evaluate(board)]]), axis = 0)
                board.pop()
            moves = sortedMoves[sortedMoves[:,1].argsort()[::-1]][:,0]
            
            for move in moves:
                board.push(move)
                moveScore = self.getValue(board, 0, 1, alpha, beta, time)
                board.pop()
                
                if moveScore > bestMoveScore:
                    bestMoveScore = moveScore
                    bestMove = move
            return bestMove

    def evaluate(self, board):
        score = random.random()
        
        #Can include (chess.KING, 0, self.kingTable),
        #Counts every piece of each type and evaluates a score //needs improvement
        #Source for values: https://arxiv.org/pdf/2009.04374.pdf or https://en.wikipedia.org/wiki/Chess_strategy
        for (piece, value, table) in [(chess.PAWN, 100, self.pawnTable), 
                           (chess.BISHOP, 333, self.bishopTable),
                           (chess.QUEEN, 950, self.queenTable),
                           (chess.KING, 0, self.kingTable),
                           (chess.KNIGHT, 305, self.knightTable),
                           (chess.ROOK, 563, self.rookTable)]:
            score += len(board.pieces(piece, self.color)) * value
            score -= len(board.pieces(piece, not self.color)) * value
            if board.turn == chess.WHITE:
                score += sum([table[i] for i in board.pieces(piece, chess.WHITE)])
                #score -= sum([table[chess.square_mirror(i)] for i in board.pieces(piece, chess.BLACK)])
            else:
                score += sum([table[chess.square_mirror(i)] for i in board.pieces(piece, chess.BLACK)])
                #score -= sum([table[i] for i in board.pieces(piece, chess.WHITE)])
        
        #Will guarantee that the current board state will return the highest score due to a checkmate
        if board.is_checkmate():
            score += float('inf')
        
        #Stores and sorts scores in decending value
        #self.stored = np.append(self.stored, np.array([[chess.polyglot.zobrist_hash(board), score]]), axis = 0)
        return score


    #For agentIndex, 0 is the current player, 1 is the opponent.
    def getValue(self, board, currentDepth, agentIndex, alpha, beta, time):
        if t.time() - self.start >= time - 3:
            self.depth = 1
        if currentDepth == self.depth or board.is_game_over():
            return self.evaluate(board)
        elif agentIndex == 0:
            if currentDepth == self.depth + 0.5:
                return self.evaluate(board)
            return self.maxValue(board, currentDepth, alpha, beta, time)
        else:
            if currentDepth == self.depth - 0.5:
                return self.evaluate(board)
            return self.minValue(board, currentDepth, alpha, beta, time)


    def maxValue(self, board, currentDepth, alpha, beta, time):
        maxValue = float('-inf')
        moves = list(board.legal_moves)
        
        for move in moves:
            board.push(move)
            maxValue = max(maxValue, self.getValue(board, currentDepth, 1, alpha, beta, time))
            board.pop()

            if maxValue >= beta:
                return maxValue
            alpha = max(alpha, maxValue)

        return maxValue
    

    def minValue(self, board, currentDepth, alpha, beta, time):
        minValue = float('inf')
        moves = list(board.legal_moves)
        
        for move in moves:
            board.push(move)
            minValue = min(minValue, self.getValue(board, currentDepth + 1, 0, alpha, beta, time))
            board.pop()
        
            if minValue <= alpha:
                return minValue
            beta = min(beta, minValue)
        return minValue


    def quiesce(self, board, currentDepth, alpha, beta):
        stand_pat = self.evaluate(board)
        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat
        if currentDepth >= self.depth + 1:
            return alpha
        for move in self.captureMoves(board):
            board.push(move)
            score = -self.quiesce(board, currentDepth + 1, -beta, -alpha)
            board.pop()

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
        return alpha


    def captureMoves(self, board):
        a = []
        if not board.is_check:
            for move in list(board.legal_moves):
                if board.is_capture(move):
                    a.append(move)
        else:
            return list(board.legal_moves)
        return a