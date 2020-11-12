import chess
import time

class Player:
    """
    Prompts user input, sanitizes, and returns a move
    """
    def __init__(self, board, color, time):
        self.color = color

    def move(self, board, time):
        color_str = None
        if self.color == chess.WHITE:
            color_str = "White"
        else:
            color_str = "Black"

        # Print legal moves for player reference
        print("\n\nLegal moves for " + color_str)
        
        for move in board.legal_moves:
            print(move.uci(), end=" ")

        # Input parser loop
        while(True):
            uci = input("\n\n" + color_str + ", type a move \n>")
            try:
                move = chess.Move.from_uci(uci)

                if move in list(board.legal_moves):
                    return move
                else:
                    print("Illegal move \nLegal moves for " + color_str)
                    self.printLegalMoves(board)
            except:
                print("Not recognized as a move \nLegal moves for " + color_str + ":")
                self.printLegalMoves(board)


    def printLegalMoves(self, board):
        print("(", end=" ")

        for move in list(board.legal_moves):
            print(move.uci(), end=", ")
        print(")")
        print(board)