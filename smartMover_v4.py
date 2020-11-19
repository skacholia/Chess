import random
import chess
import chess.polyglot
import time
#Chess AI V4
#MiniMax Agent
#November 17, 2020

class Player:

    def __init__(self, board, color, time):
        self.color = color
        self.depth = 1
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


    #Returns the best action for the player
    def move(self, board, time):
        try:
            return chess.polyglot.MemoryMappedReader("data/bookfish.bin").weighted_choice(board).move
        except:
            #If checks:#
            if len(board.pieces(chess.QUEEN, self.color)) == 0 and len(board.pieces(chess.QUEEN, not self.color)) == 0:
                self.kingTable = self.kingEndTable

            moves = list(board.legal_moves)
            bestMoveScore = float('-inf')
            alpha = float('-inf')
            beta = float('inf')
            bestMove = random.choice(moves)

            for move in moves:
                board.push(move)
                moveScore = self.getValue(board, 0, 1, alpha, beta, time)
                board.pop()
                
                if moveScore > bestMoveScore:
                    bestMoveScore = moveScore
                    bestMove = move
            
            return bestMove


    #Evaluates the current state of the board.
    #We always want to evaluate the board for self.color score.
    def evaluate(self, board, time):
        score = random.random()
        
        #Can include (chess.KING, 0),
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
               # score -= sum([table[chess.square_mirror(i)] for i in board.pieces(piece, chess.BLACK)])
            else:
                score += sum([table[chess.square_mirror(i)] for i in board.pieces(piece, chess.BLACK)])
              #  score -= sum([table[i] for i in board.pieces(piece, chess.WHITE)])
        
        #Will guarantee that the current board state will return the highest score due to a checkmate
        if board.is_checkmate():
            score += float('inf')
        
        return score


    #For agentIndex, 0 is the current player, 1 is the opponent.
    def getValue(self, board, currentDepth, agentIndex, alpha, beta, time):
        if currentDepth == self.depth or board.is_game_over():   
            return self.evaluate(board, time)
        elif agentIndex == 0:
            return self.maxValue(board, currentDepth, alpha, beta, time)
        else:
            return self.minValue(board, currentDepth, alpha, beta, time)


    def maxValue(self, board, currentDepth, alpha, beta, time):
        maxValue = float('-inf')
        
        for move in list(board.legal_moves):
            board.push(move)
            maxValue = max(maxValue, self.getValue(board, currentDepth, 1, alpha, beta, time))
            board.pop()

            if maxValue >= beta:
                return maxValue
            alpha = max(alpha, maxValue)

        return maxValue
    

    def minValue(self, board, currentDepth, alpha, beta, time):
        minValue = float('inf')
        
        for move in list(board.legal_moves):
            board.push(move)
            minValue = min(minValue, self.getValue(board, currentDepth + 1, 0, alpha, beta, time))
            board.pop()
        
            if minValue <= alpha:
                return minValue
            beta = min(beta, minValue)

        return minValue
