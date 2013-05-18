from trix.environment import Piece

Pieces = {}
def addPiece(number, shape): Pieces[number] = Piece(number, shape)
addPiece('1', ((1,), (1,), (1,), (1,)))
addPiece('2', ((1, 1), (1, 1)))
addPiece('3', ((1, 0), (1, 1), (1, 0)))
addPiece('4', ((1, 1), (1, 0), (1, 0)))
addPiece('5', ((1, 1), (0, 1), (0, 1)))
addPiece('6', ((1, 0), (1, 1), (0, 1)))
addPiece('7', ((0, 1), (1, 1), (1, 0)))

TotalCount     = 4 * len(Pieces)
PieceFrequency = 1 / len(Pieces)
Frequencies    = {}

# Calculate the per-rotation frequency for a given sequence of items.
for name, piece in Pieces.items():
  rotations = piece.rotations()
  # The frequency of each item is proportional to
  individualOccurences = 4 / len(rotations)
  frequencyWithinPiece = individualOccurences / 4
  Frequencies[piece] = (frequencyWithinPiece * PieceFrequency)

# Given a file, reads in the sequence of pieces to be processed for the given game.
# Note that this will return a list of pieces, normalized according to the game details.
def readPieces(file):
  pieces = []
  with open(file) as f:
    for line in f:
      for character in line:
        if character in Pieces: pieces.append(Pieces[character])
  return pieces