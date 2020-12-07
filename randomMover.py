import random
import chess

class Player:
    def __init__(self, board, color, time):
        self.color = color
    
    def move(self, board, time):
        return random.choice(list(board.legal_moves))