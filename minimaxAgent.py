import chess
import time
import random

class Player:
    def __init__(self, board, color, time):
        self.color = color
    def move(self, board, time):
        maxVal = -10000
        moves = list(board.legal_moves)
        maxAction = random.choice(moves)
        alpha = -10000
        beta = 10000
        for move in moves:
            val = self.minimax(board, 2, True, move, alpha, beta)
            if val > maxVal:
                maxVal = val
                maxAction = move
            alpha = max(alpha, val)
            if alpha > beta:
                break
        return maxAction
    def minimax(self, board, curDepth, player, move, alpha, beta):
        if curDepth == 0 or board.is_game_over():
            return self.getScore(board, move)
        elif player == True:
            maxVal = -10000
            for newMove in list(board.legal_moves):
                val = self.minimax(board, curDepth - 1, False, newMove, alpha, beta)
                maxVal = max(maxVal, val)
                alpha = max(alpha, val)
                if alpha > beta:
                    break
            return maxVal
        elif player == False:
            minVal = 10000
            for newMove in list(board.legal_moves):
                val = self.minimax(board, curDepth - 1, True, newMove, alpha, beta)
                minVal = min(minVal, val)
                beta = min(beta, val)
                if beta < alpha:
                    break
            return minVal
    def getScore(self, board, move):
        score = 0
 
        if board.is_capture(move):
            score += 10
        
        board.push(move)
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
        score += 100 if board.is_checkmate() else 0
        
        board.pop()
 
        return score
   