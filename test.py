import chess

b = chess.Board()

print(b)

print(b.turn)

b.push(chess.Move.null())

print(b)
print(b.turn)