import random
import chess
import time
import multiprocessing as mp
import numpy as np


pawnTable = [
0,  0,  0,  0,  0,  0,  0,  0,
50, 50, 50, 50, 50, 50, 50, 50,
10, 10, 20, 30, 30, 20, 10, 10,
5,  5, 10, 25, 25, 10,  5,  5,
0,  0,  0, 20, 20,  0,  0,  0,
5, -5,-10,  0,  0,-10, -5,  5,
5, 10, 10,-20,-20, 10, 10,  5,
0,  0,  0,  0,  0,  0,  0,  0]

knightTable = [
-50,-40,-30,-30,-30,-30,-40,-50,
-40,-20,  0,  0,  0,  0,-20,-40,
-30,  0, 10, 15, 15, 10,  0,-30,
-30,  5, 15, 20, 20, 15,  5,-30,
-30,  0, 15, 20, 20, 15,  0,-30,
-30,  5, 10, 15, 15, 10,  5,-30,
-40,-20,  0,  5,  5,  0,-20,-40,
-50,-40,-30,-30,-30,-30,-40,-50,]

bishopTable = [
-20,-10,-10,-10,-10,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  5, 10, 10,  5,  0,-10,
-10,  5,  5, 10, 10,  5,  5,-10,
-10,  0, 10, 10, 10, 10,  0,-10,
-10, 10, 10, 10, 10, 10, 10,-10,
-10,  5,  0,  0,  0,  0,  5,-10,
-20,-10,-10,-10,-10,-10,-10,-20,]

rookTable = [
0,  0,  0,  0,  0,  0,  0,  0,
5, 10, 10, 10, 10, 10, 10,  5,
-5,  0,  0,  0,  0,  0,  0, -5,
-5,  0,  0,  0,  0,  0,  0, -5,
-5,  0,  0,  0,  0,  0,  0, -5,
-5,  0,  0,  0,  0,  0,  0, -5,
-5,  0,  0,  0,  0,  0,  0, -5,
0,  0,  0,  5,  5,  0,  0,  0]

queenTable = [
-20,-10,-10, -5, -5,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  5,  5,  5,  5,  0,-10,
-5,  0,  5,  5,  5,  5,  0, -5,
0,  0,  5,  5,  5,  5,  0, -5,
-10,  5,  5,  5,  5,  5,  0,-10,
-10,  0,  5,  0,  0,  0,  0,-10,
-20,-10,-10, -5, -5,-10,-10,-20]

kingMiddleTable = [
20, 30, 10,  0,  0, 10, 30, 20,
20, 20,  0,  0,  0,  0, 20, 20,
-10,-20,-20,-20,-20,-20,-20,-10,
-20,-30,-30,-40,-40,-30,-30,-20,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30]

kingEndTable = [
-50,-40,-30,-20,-20,-30,-40,-50,
-30,-20,-10,  0,  0,-10,-20,-30,
-30,-10, 20, 30, 30, 20,-10,-30,
-30,-10, 30, 40, 40, 30,-10,-30,
-30,-10, 30, 40, 40, 30,-10,-30,
-30,-10, 20, 30, 30, 20,-10,-30,
-30,-30,  0,  0,  0,  0,-30,-30,
-50,-30,-30,-30,-30,-30,-30,-50
]

board = chess.Board()
color = chess.WHITE
nodes = 0

#bestMove = None

def move(move, color = False):
    global board

    alpha, beta = float('-inf'), float('inf')

    board.push(move)
    moveScore = negamax(board, 5, alpha, beta)
    board.pop()
    
    return moveScore

def evaluate(board):
    if board.turn == color:
        coeff = 1
    else:
        coeff = -1

    score = 0

    if len(board.pieces(chess.QUEEN, color)) == 0 and len(board.pieces(chess.QUEEN, not color)) == 0:
        kingTable = kingEndTable
    else:
        kingTable = kingMiddleTable


    mirroredBoard = board.mirror()
    for (piece, value, table) in [(chess.PAWN, 100, pawnTable), 
                        (chess.BISHOP, 333, bishopTable),
                        (chess.QUEEN, 950, queenTable),
                        (chess.KING, 0, kingTable),
                        (chess.KNIGHT, 305, knightTable),
                        (chess.ROOK, 563, rookTable)]:
        score += (len(board.pieces(piece, color)) - len(board.pieces(piece, not color))) * value

        if board.turn:#if board.turn == chess.WHITE
            score += sum([table[i] for i in board.pieces(piece, chess.WHITE)]) - sum([table[i] for i in mirroredBoard.pieces(piece, chess.BLACK)])
        else:
            score += sum([table[i] for i in mirroredBoard.pieces(piece, chess.BLACK)]) - sum([table[i] for i in board.pieces(piece, chess.WHITE)])
    
    if board.is_checkmate():
        score += 20000

    return coeff * score

def negamax(board, currentDepth, alpha, beta):
    if currentDepth <= 0 or board.is_game_over():
        return quiesce(board, alpha, beta)

    push, pop = board.push, board.pop
    for move in board.legal_moves:#Move ordering here takes more time than it saves
        push(move)
        score = -negamax(board, currentDepth - 1, -beta, -alpha)
        pop()
        
        #Alpha-Beta Pruning
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
    
    return alpha

def quiesce(board, alpha, beta):
    stand_pat = evaluate(board)

    #Alpha-Beta Pruning in Quiescence
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat
    

    push, pop = board.push, board.pop
    for move in captureMoves(board):#Move Ordering yields an unecessary increase in time --- self.sortMoves(board, self.captureMoves(board))
        push(move)
        score = -quiesce(board, -beta, -alpha)
        pop()

        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
        
    return alpha

def sortMoves(board, moves):
    sortedMoves = np.empty((0, 2))
    
    push, pop = board.push, board.pop
    for move in moves:
        push(move)
        sortedMoves = np.append(sortedMoves, np.array([[move, miniEval(board)]]), axis = 0)
        pop()
    

    if board.turn == color:
        return sortedMoves[sortedMoves[:,1].argsort()[::-1]][:,0]
    else:
        return sortedMoves[sortedMoves[:,1].argsort()][:,0]


def captureMoves(board):
    moves = []

    for move in board.legal_moves:
        if board.is_capture(move):
            moves.append(move)
    return moves


def miniEval(board):
    if board.turn == color:
        coeff = 1
    else:
        coeff = -1
    score = 0

    #Does not include (chess.KING, 0), for a faster evaluation loop
    for (piece, value) in [(chess.PAWN, 100),
                        (chess.BISHOP, 333),
                        (chess.QUEEN, 950),
                        (chess.KNIGHT, 305),
                        (chess.ROOK, 563)]:
        score += (len(board.pieces(piece, color)) - len(board.pieces(piece, not color))) * value

    return coeff * score


if __name__ == "__main__":
    start = time.time()
    
    print(board)

    moves = sortMoves(board, board.legal_moves)
    
    pool = mp.Pool(mp.cpu_count())
    results = pool.map(move, moves)
    bestMoveScore = max(results)
    index = results.index(bestMoveScore)
    bestMove = list(moves)[index]
    
    board.push(bestMove)
    print("-----New-----")
    print(bestMove)
    print(board)
    print(bestMove, bestMoveScore)
    print("Nodes:", nodes)

    print(time.time() - start, "s")