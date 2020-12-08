import random
import chess
import time
#Chess AI V1
#Simple Reflex Agent AI
#November 9, 2020

class Player:

    def __init__(self, board, color, time):
        self.color = color
        

    def move(self, board, time):
        moves = list(board.legal_moves)
        bestMove = random.choice(moves)
        bestMoveScore = 0
        
        for move in moves:
            board.push(move)
            moveScore = self.getScore(board, move, time)
            board.pop()

            if moveScore > bestMoveScore:
                bestMoveScore = moveScore
                bestMove = move
        
        return bestMove


    def getScore (self, board, move, time):
        score = random.random()

        #Counts every piece of each type and evaluates a score
        #Source for values: https://arxiv.org/pdf/2009.04374.pdf
        for (piece, value) in [(chess.PAWN, 1), 
                           (chess.BISHOP, 3.33), 
                           (chess.KING, 0), 
                           (chess.QUEEN, 9.5), 
                           (chess.KNIGHT, 3.05),
                           (chess.ROOK, 5.63)]:
            score += len(board.pieces(piece, self.color)) * value
            score -= len(board.pieces(piece, not self.color)) * value
        score += float('inf') if board.is_checkmate() else 0
        
        return score