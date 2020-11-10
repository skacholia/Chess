import random
import chess
import time
#Chess AI V1
#MiniMax Agent
 
class Player:
 
    def __init__(self, board, color, time):
        self.color = color    
 
    def move(self, board, time):
        moves = list(board.legal_moves)
        bestMove = moves[0]
        bestMoveScore = 0
        
        for move in moves:
            boardCopy = board.copy()
 
            # go through board and return a score
            moveScore = self.getScore(boardCopy, move, time)
            
            if moveScore >= bestMoveScore:
                bestMoveScore = moveScore
                bestMove = move
        
        return bestMove
 
    def getScore (self, board, move, time):
        board.push(move)
 
        #why random.random() instead of score = 0
        score = random.random()
 
        #Counts every piece of each type and evaluates a score
        for (piece, value) in [(chess.PAWN, 2), 
                           (chess.BISHOP, 5), 
                           (chess.KING, 25), 
                           (chess.QUEEN, 10), 
                           (chess.KNIGHT, 3),
                           (chess.ROOK, 5)]:
            score += len(board.pieces(piece, self.color)) * value
            score -= len(board.pieces(piece, not self.color)) * value
        score += 100 if board.is_checkmate() else 0
        
        return score