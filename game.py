import chess
import chess.pgn
import time
import test as player1
import smartMover_v6_1 as player2

game = chess.pgn.Game()
node = game
board = chess.Board()
board1 = board.copy()
board2 = board.copy()
playerTime = 10000000
p1_time = playerTime
p2_time = playerTime

start = time.time()
p1 = player1.Player(board1,chess.WHITE,p1_time)
end = time.time()
p1_time -= end-start

start = time.time()
p2 = player2.Player(board2,chess.BLACK,p2_time)
end = time.time()
p2_time -= end-start
moveNumber = 0
legal_move = True
print(board)

while p1_time>0 and p2_time>0 and not board.is_game_over() and legal_move:
    board_copy = board.copy()
    if board.turn == chess.WHITE:
        start = time.time()
        move = p1.move(board_copy,p1_time)
        end = time.time()
        p1_time -= end-start
    else:
        start = time.time()
        move = p2.move(board_copy,p2_time)
        end = time.time()
        p2_time -= end-start
    
    if move in board.legal_moves:
        board.push(move)
        print(move)
        print(board)
        print("------" + str(moveNumber/2 + 1) + "------")
        moveNumber += 1
        node = node.add_variation(move)
    else:
        legal_move = False

print("Number of Moves: ",moveNumber)
print("Player 1 Time: ",(playerTime - p1_time),"-----Player 1 Move Time: ",(playerTime - p1_time)/(moveNumber/2))
print("Player 2 Time: ",(playerTime - p2_time),"-----Player 2 Move Time: ",(playerTime - p2_time)/(moveNumber/2))

if not legal_move:
    if board.turn == chess.WHITE:
        print("Black wins - illegal move by white")
    else:
        print("White wins - illegal move by black")
elif p1_time <= 0:
    print("Black wins on time")
    board.pop()
elif p2_time <= 0:
    print("White wins on time")
    board.pop()
elif board.is_checkmate():
    if board.turn==chess.WHITE:
        print("Black wins - Checkmate!")
    else:
        print("White wins - Checkmate!")
elif board.is_stalemate():
    print("Draw - Stalemate")
elif board.is_insufficient_material():
    print("Draw - Insufficient Material")
elif board.is_seventyfive_moves():
    print("Draw - 75 moves without capture/pawn advancement")
elif board.is_fivefold_repetition():
    print("Draw - position repeated 5 times")
print(game)