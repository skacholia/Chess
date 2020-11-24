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
        self.depth = 0
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
        self.nodes = 0

    #Returns the best action for the player
    def move(self, board, time):
        try:
            #Selfmade opening book using https://rebel13.nl/download/polyglot.html
            return chess.polyglot.MemoryMappedReader("data/book.bin").weighted_choice(board).move
        except:
            self.start = t.time()      
            bestMove = None
            self.depth = 2
            val = 0.25
            while t.time() - self.start <= val:
                tempTime = t.time()

                bestMoveScore, alpha, beta = float('-inf'), float('-inf'), float('inf')
                
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
        if board.turn == self.color:
            coeff = 1
        else:
            coeff = -1
        
        #Will guarantee that the current board state will return the highest score due to a checkmate
        if board.is_checkmate():
            return coeff * float('inf')
        
        score = 0

        #Source for values: https://arxiv.org/pdf/2009.04374.pdf or https://en.wikipedia.org/wiki/Chess_strategy
        pieces, square_mirror, turn, color = board.pieces, chess.square_mirror, board.turn, self.color
        pawnTable, bishopTable, queenTable, kingTable, knightTable, rookTable = self.pawnTable, self.bishopTable, self.queenTable, self.kingTable, self.knightTable, self.rookTable
        pawn, bishop, queen, king, knight, rook = chess.PAWN, chess.BISHOP, chess.QUEEN, chess.KING, chess.KNIGHT, chess.ROOK
        for (piece, value, table) in [(pawn, 100, pawnTable), 
                           (bishop, 333, bishopTable),
                           (queen, 950, queenTable),
                           (king, 0, kingTable),
                           (knight, 305, knightTable),
                           (rook, 563, rookTable)]:
            score += (len(pieces(piece, color)) - len(pieces(piece, not color))) * value
            if turn:#if board.turn == chess.WHITE
                score += sum([table[i] for i in pieces(piece, chess.WHITE)])
                #score -= sum([table[chess.square_mirror(i)] for i in board.pieces(piece, chess.BLACK)]) ----------unecessary increase in calculation time
            else:
                score += sum([table[square_mirror(i)] for i in pieces(piece, chess.BLACK)])
                #score -= sum([table[i] for i in board.pieces(piece, chess.WHITE)])

        return coeff * score


    def negamax(self, board, currentDepth, alpha, beta):
        if currentDepth == self.depth or len(list(board.legal_moves)) == 0 or board.is_game_over():
            return self.quiesce(board, alpha, beta, 1) #last term is the max quiesce depth

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