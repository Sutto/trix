import unittest
from unittest.mock import MagicMock
from trix.actions import *
from trix.environment import Piece

class TestActions(unittest.TestCase):

  def setUp(self):
    class FakeEnvironment(object):
      add_to_buffer      = MagicMock()
      remove_from_buffer = MagicMock()
      place_piece_at     = MagicMock()
      consume            = MagicMock()
    self.environment = FakeEnvironment()
    self.piece_a     = Piece('1', ((0, 1, 0), (1, 1, 1)))
    self.piece_b     = Piece('2', ((1, 0), (1, 0), (1, 1)))

  def test_default_action(self):
    action = Action()
    with self.assertRaises(NotImplementedError):
      action.apply(self.environment)

  def test_do_nothing_action(self):
    env = self.environment
    env.add_to_buffer.side_effect = Exception("Called a method")
    env.place_piece_at.side_effect = Exception("Called a method")
    env.remove_from_buffer.side_effect = Exception("Called a method")
    env.consume.side_effect = Exception("Called a method")
    action = DoNothing()
    action.apply(env)

  def test_add_to_buffer(self):
    env = self.environment
    env.place_piece_at.side_effect = Exception("Called a method")
    env.remove_from_buffer.side_effect = Exception("Called a method")
    action = AddToBuffer(self.piece_a)
    action.apply(env)
    env.consume.assert_called_with()
    env.add_to_buffer.assert_called_with(self.piece_a)

  def test_place_piece(self):
    env = self.environment
    env.add_to_buffer.side_effect = Exception("Called a method")
    env.remove_from_buffer.side_effect = Exception("Called a method")
    action = PlaceNextPiece(self.piece_a, 123)
    action.apply(env)
    env.consume.assert_called_with()
    env.place_piece_at.assert_called_with(self.piece_a, 123)

  def test_place_from_buffer(self):
    env = self.environment
    env.consume.side_effect = Exception("Called a method")
    env.add_to_buffer.side_effect = Exception("Called a method")
    action = PlaceFromBuffer(self.piece_a, 123)
    action.apply(env)
    env.remove_from_buffer.assert_called_with(self.piece_a)
    env.place_piece_at.assert_called_with(self.piece_a, 123)


if __name__ == '__main__': unittest.main()