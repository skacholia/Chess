import chess
import chess.pgn
import time
import smartMover_v4 as player1
import smartMover_v4_1_1 as player2

whiteWins = 0
blackWins = 0
games = 0
p1_moveTime = 0
p2_moveTime = 0
iterations = 100
graphics = False
timeWhite = 0
timeBlack = 0
timeStart = time.time()

for var in range(iterations):
    game = chess.pgn.Game()
    node = game
    
    board = chess.Board()
    board1 = board.copy()
    board2 = board.copy()
    playerTime = 1000
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

    legal_move = True

    moveNumber = 1
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
            node = node.add_variation(move)
            moveNumber += 1
        else:
            legal_move = False
    timeWhite += (playerTime - p1_time)
    timeBlack += (playerTime - p2_time)
    if not legal_move:
        if board.turn == chess.WHITE:
            msg = "Black wins - illegal move by white"
            blackWins += 1
        else:
            msg = "White wins - illegal move by black"
            whiteWins += 1
    elif p1_time <= 0:
        msg = "Black wins on time"
        blackWins += 1
        board.pop()
    elif p2_time <= 0:
        msg = "White wins on time"
        whiteWins += 1
        board.pop()
    elif board.is_checkmate():
        if board.turn==chess.WHITE:
            msg = "Black wins - Checkmate!"
            blackWins += 1
        else:
            msg = "White wins - Checkmate!"
            whiteWins += 1
    elif board.is_stalemate():
        msg = "Draw - Stalemate"
    elif board.is_insufficient_material():
        msg = "Draw - Insufficient Material"
    elif board.is_seventyfive_moves():
        msg = "Draw - 75 moves without capture/pawn advancement"
    elif board.is_fivefold_repetition():
        msg = "Draw - position repeated 5 times"



    games += 1
    p1_moveTime += (playerTime - p1_time)/(moveNumber/2)
    p2_moveTime += (playerTime - p2_time)/(moveNumber/2)
    if graphics == True:
        print("--------------------","Game:",games,"--------------------")
        print ("Time: ", time.time() - timeStart, "s")
        print("White WinRate:", whiteWins/games * 100,"% ", "----White Game Time: ", timeWhite/games, "----White Move Time:",p1_moveTime/(games))
        print("Black WinRate:", blackWins/games * 100,"% ", "----Black Game Time: ", timeBlack/games, "----Black Move Time:",p2_moveTime/(games))
        print(game)
    else:
            print(str(games) + "/" + str(iterations))

if graphics == False:
    print ("Time: ", time.time() - timeStart, "s")
    print("White WinRate:", whiteWins/games * 100,"% ", "----White Game Time: ", timeWhite/games, "----White Move Time:",p1_moveTime/(games))
    print("Black WinRate:", blackWins/games * 100,"% ", "----Black Game Time: ", timeBlack/games, "----Black Move Time:",p2_moveTime/(games))