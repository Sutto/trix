import unittest
import trix.config
from unittest.mock import MagicMock
from trix.environment import Piece, Board, Environment
from trix.actions import Action
from trix.percept import Percept

class TestEnvironment(unittest.TestCase):

  def setUp(self):
    self.piece_a = Piece('1', ((0, 1, 0), (1, 1, 1)))
    self.piece_b = Piece('2', ((1, 0), (1, 0), (1, 1)))
    self.piece_c = Piece('3', ((1, 1, 1, 1),))
    self.config  = trix.config.Configuration()
    self.config.merge(trix.config.defaults)

  def test_initialization(self):
    env = Environment(self.config, [])
    self.assertIsInstance(env.board, Board)
    self.assertEqual(self.config.width, env.board.width)
    self.assertEqual([], env.buffer)
    self.assertEqual([], env.items)
    self.assertEqual([], env.history)

  def test_adding_to_the_buffer(self):
    piece = self.piece_a
    env = Environment(self.config, [])
    self.assertEqual([], env.buffer)
    env.add_to_buffer(piece)
    self.assertEqual([piece], env.buffer)

  def test_adding_duplicate_pieces_to_the_buffer(self):
    piece = self.piece_a
    config = self.config
    config.buffer = 3
    env = Environment(config, [])
    self.assertEqual([], env.buffer)
    env.add_to_buffer(piece)
    self.assertEqual([piece], env.buffer)
    env.add_to_buffer(piece)
    self.assertEqual([piece, piece], env.buffer)
    env.add_to_buffer(piece)
    self.assertEqual([piece, piece, piece], env.buffer)

  def test_checking_if_buffer_is_full(self):
    piece = self.piece_a
    env = Environment(self.config, [])
    self.assertFalse(env.buffer_is_full())
    for i in range(env.configuration.buffer):
      self.assertFalse(env.buffer_is_full())
      env.add_to_buffer(piece)
    self.assertTrue(env.buffer_is_full())

  def test_adding_to_a_full_buffer(self):
    piece = self.piece_a
    env = Environment(self.config, [])
    for i in range(env.configuration.buffer):
      env.add_to_buffer(piece)
    with self.assertRaises(Environment.FullBuffer):
      env.add_to_buffer(piece)

  def test_removing_items_from_the_buffer(self):
    piece_a = self.piece_a
    piece_b = self.piece_b
    config = self.config
    config.buffer = 3
    env = Environment(config, [])
    env.add_to_buffer(piece_a)
    env.add_to_buffer(piece_b)
    self.assertIn(piece_a, env.buffer)
    self.assertIn(piece_b, env.buffer)
    env.remove_from_buffer(piece_a)
    self.assertNotIn(piece_a, env.buffer)
    self.assertIn(piece_b, env.buffer)
    env.remove_from_buffer(piece_b)
    self.assertNotIn(piece_a, env.buffer)
    self.assertNotIn(piece_b, env.buffer)

  def test_removing_duplicate_items_from_buffer(self):
    piece = self.piece_a
    config = self.config
    config.buffer = 3
    env = Environment(config, [])
    env.add_to_buffer(piece)
    env.add_to_buffer(piece)
    env.add_to_buffer(piece)
    self.assertEqual([piece, piece, piece], env.buffer)
    env.remove_from_buffer(piece)
    self.assertEqual([piece, piece], env.buffer)
    env.remove_from_buffer(piece)
    self.assertEqual([piece], env.buffer)

  def test_placing_pieces_on_the_board(self):
    piece = self.piece_a
    mock  = MagicMock()
    env   = Environment(self.config, [])
    class FakeBoard(Board): place = mock
    env.board = FakeBoard(self.config.width)
    env.place_piece_at(piece, 2)
    env.board.place.assert_called_with(piece, 2)

  def test_getting_possible_left_offsets(self):
    piece_a, piece_b, piece_c = self.piece_a, self.piece_b, self.piece_c
    config       = self.config
    config.width = 10
    env          = Environment(config, [])
    self.assertEqual(range(8), env.possible_left_offsets_for(piece_a))
    self.assertEqual(range(9), env.possible_left_offsets_for(piece_b))
    self.assertEqual(range(7), env.possible_left_offsets_for(piece_c))

  def test_perceiving_the_board(self):
    piece_a, piece_b, piece_c = self.piece_a, self.piece_b, self.piece_c
    env = Environment(self.config, [piece_a, piece_c, piece_b, piece_a])
    percept = env.perceive()
    self.assertIsInstance(percept, Percept)
    self.assertEqual(piece_a, percept.piece)
    self.assertEqual([piece_a, piece_c, piece_b, piece_a], percept.pieces)
    env.consume()
    percept = env.perceive()
    self.assertIsInstance(percept, Percept)
    self.assertEqual(piece_c, percept.piece)
    self.assertEqual([piece_c, piece_b, piece_a], percept.pieces)
    env.consume()
    percept = env.perceive()
    self.assertIsInstance(percept, Percept)
    self.assertEqual(piece_b, percept.piece)
    self.assertEqual([piece_b, piece_a], percept.pieces)
    env.consume()
    percept = env.perceive()
    self.assertIsInstance(percept, Percept)
    self.assertEqual(piece_a, percept.piece)
    self.assertEqual([piece_a], percept.pieces)
    env.consume()
    percept  = env.perceive()
    self.assertEqual(None, percept)

  def test_perceiving_empty_items_lists(self):
    env = Environment(self.config, [])
    self.assertEqual(None, env.perceive())


  def test_applying_an_action(self):
    class FakeAction(Action): apply = MagicMock()
    action = FakeAction()
    env = Environment(self.config, [])
    self.assertEqual([], env.history)
    env.update(action)
    self.assertEqual([action], env.history)
    FakeAction.apply.assert_called_with(env)

  def test_copying_the_environment(self):
    piece_a, piece_b = self.piece_a, self.piece_b
    env = Environment(self.config, [piece_a, piece_b])
    env.add_to_buffer(piece_a)
    copy = env.copy()
    self.assertEqual(env.buffer, copy.buffer)
    self.assertEqual(env.board.render(), copy.board.render())
    self.assertEqual(env.items, copy.items)
    self.assertEqual(env.configuration, copy.configuration)
    env.place_piece_at(piece_a, 0)
    env.remove_from_buffer(piece_a)
    env.add_to_buffer(piece_b)
    env.consume()
    self.assertEqual(env.configuration, copy.configuration)
    self.assertNotEqual(env.board.render(), copy.board.render())
    self.assertNotEqual(env.buffer, copy.buffer)
    self.assertNotEqual(env.items, copy.items)

  def test_consuming_items(self):
    piece_a, piece_b, piece_c = self.piece_a, self.piece_b, self.piece_c
    env = Environment(self.config, [piece_a, piece_c, piece_b, piece_a])
    self.assertEqual([piece_a, piece_c, piece_b, piece_a], env.items)
    env.consume()
    self.assertEqual([piece_c, piece_b, piece_a], env.items)
    env.consume()
    self.assertEqual([piece_b, piece_a], env.items)
    env.consume()
    self.assertEqual([piece_a], env.items)
    env.consume()
    self.assertEqual([], env.items)


  def test_forking_the_environment(self):
    env = Environment(self.config, [])
    class FakeAction(Action): apply = MagicMock()
    action = FakeAction()
    self.assertEqual([], env.history)
    copy = env.fork(action)
    self.assertEqual([], env.history)
    self.assertEqual([action], copy.history)
    FakeAction.apply.assert_called_with(copy)


if __name__ == '__main__': unittest.main()