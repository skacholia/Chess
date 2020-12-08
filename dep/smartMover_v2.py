import random
import chess
import time
#Chess AI V2
#MiniMax Agent
#November 11, 2020

class Player:

    def __init__(self, board, color, time):
        self.color = color
        self.depth = 1

    #Returns the best action for the player
    def move(self, board, time):
        moves = list(board.legal_moves)
        bestMoveScore = float('-inf')
        bestMove = random.choice(moves)
        
        for move in moves:
            board.turn = self.color
            board.push(move)
            moveScore = self.getValue(board, 0, 1, time)
            board.pop()
            
            if moveScore > bestMoveScore:
                bestMoveScore = moveScore
                bestMove = move
        
        return bestMove

    #Evaluates the current state of the board
    def evaluationFunction(self, board, agentIndex, time):
        #Need reasoning for why it's score = random.random() and not just score = 0
        score = random.random()
        
        #Counts every piece of each type and evaluates a score //needs improvement
        #Source for values: https://arxiv.org/pdf/2009.04374.pdf
        for (piece, value) in [(chess.PAWN, 1), 
                           (chess.BISHOP, 3.33), 
                           (chess.KING, 0), 
                           (chess.QUEEN, 9.5), 
                           (chess.KNIGHT, 3.05),
                           (chess.ROOK, 5.63)]:
            score += len(board.pieces(piece, self.color)) * value
            score -= len(board.pieces(piece, not self.color)) * value
        
        #Will guarantee that the current board state will return the highest score due to a checkmate
        if board.is_checkmate():
            score += float('inf')
        
        return score

    #For agentIndex, 0 is the current player, 1 is the opponent.
    def getValue(self, board, currentDepth, agentIndex, time):
        if currentDepth == self.depth or board.is_game_over():   
            return self.evaluationFunction(board, agentIndex, time)
        elif agentIndex == 0:
            return self.maxValue(board, currentDepth, time)
        else:
            return self.minValue(board, currentDepth, 1, time)


    def maxValue(self, board, currentDepth, time):
        maxValue = float("-inf")
        board.turn = self.color

        for move in list(board.legal_moves):
            board.turn = self.color
            board.push(move)
            maxValue = max(maxValue, self.getValue(board, currentDepth, 1, time))
            board.pop()

        return maxValue
    

    def minValue(self, board, currentDepth, agentIndex, time):
        minValue = float('inf')
        
        for move in list(board.legal_moves):
            if agentIndex == 1:
                board.turn = not self.color
                board.push(move)
                minValue = min(minValue, self.getValue(board, currentDepth + 1, 0, time))
                board.pop()
            else:
                board.turn = self.color
                board.push(move)
                minValue = min(minValue, self.getValue(board, currentDepth, 1, time))
                board.pop()

        return minValue