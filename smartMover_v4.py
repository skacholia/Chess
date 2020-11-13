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
        self. pawntable = [
        0,  0,  0,  0,  0,  0,  0,  0,
        5, 10, 10,-20,-20, 10, 10,  5,
        5, -5,-10,  0,  0,-10, -5,  5,
        0,  0,  0, 20, 20,  0,  0,  0,
        5,  5, 10, 25, 25, 10,  5,  5,
        10, 10, 20, 30, 30, 20, 10, 10,
        50, 50, 50, 50, 50, 50, 50, 50,
        0,  0,  0,  0,  0,  0,  0,  0]

        self.knightstable = [
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50]

        self.bishopstable = [
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10,  5,  0,  0,  0,  0,  5,-10,
        -10, 10, 10, 10, 10, 10, 10,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -20,-10,-10,-10,-10,-10,-10,-20]

        self.rookstable = [
        0,  0,  0,  5,  5,  0,  0,  0,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        5, 10, 10, 10, 10, 10, 10,  5,
        0,  0,  0,  0,  0,  0,  0,  0]

        self.queenstable = [
        -20,-10,-10, -5, -5,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  5,  5,  5,  5,  5,  0,-10,
        0,  0,  5,  5,  5,  5,  0, -5,
        -5,  0,  5,  5,  5,  5,  0, -5,
        -10,  0,  5,  5,  5,  5,  0,-10,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20]

        self.kingstable = [
        20, 30, 10,  0,  0, 10, 30, 20,
        20, 20,  0,  0,  0,  0, 20, 20,
        -10,-20,-20,-20,-20,-20,-20,-10,
        -20,-30,-30,-40,-40,-30,-30,-20,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30]

    #Returns the best action for the player
    def move(self, board, time):
        moves = list(board.legal_moves)
        bestMoveScore = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        bestMove = random.choice(moves)
        
        for move in moves:
            board.turn = self.color
            board.push(move)
            moveScore = self.getValue(board, 0, 1, alpha, beta, time)
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
        for piece in [chess.PAWN, chess.BISHOP, chess.KING, chess.QUEEN, chess.KNIGHT, chess.ROOK]:
            score += sum([self.pawntable[i] for i in board.pieces(piece, self.color)])
            score -= sum([self.pawntable[i] for i in board.pieces(piece, not self.color)])
        #Will guarantee that the current board state will return the highest score due to a checkmate
        if board.is_checkmate():
            score += float('inf')
       
        return score

    #For agentIndex, 0 is the current player, 1 is the opponent.
    def getValue(self, board, currentDepth, agentIndex, alpha, beta, time):
        if currentDepth == self.depth or board.is_game_over():   
            return self.evaluationFunction(board, agentIndex, time)
        elif agentIndex == 0:
            return self.maxValue(board, currentDepth, alpha, beta, time)
        else:
            return self.minValue(board, currentDepth, 1, alpha, beta, time)


    def maxValue(self, board, currentDepth, alpha, beta, time):
        maxValue = float("-inf")
        
        #NOTICE: Check to see if board.turn = self.color is required. Chance to reduce calculation time here.
        for move in list(board.legal_moves):
            board.turn = self.color
            board.push(move)
            maxValue = max(maxValue, self.getValue(board, currentDepth, 1, alpha, beta, time))
            board.pop()

            if maxValue > beta:
                return maxValue
            alpha = max(alpha, maxValue)

        return maxValue
    

    def minValue(self, board, currentDepth, agentIndex, alpha, beta, time):
        minValue = float('inf')
        
        for move in list(board.legal_moves):
            if agentIndex == 1:
                board.turn = not self.color
                board.push(move)
                minValue = min(minValue, self.getValue(board, currentDepth + 1, 0, alpha, beta, time))
                board.pop()
            else:
                board.turn = self.color
                board.push(move)
                minValue = min(minValue, self.getValue(board, currentDepth, 1, alpha, beta, time))
                board.pop()

            if minValue < alpha:
                return minValue
            beta = min(beta, minValue )

        return minValue