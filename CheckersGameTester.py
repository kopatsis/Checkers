import unittest
import CheckersGame as check


class CheckersGameTest(unittest.TestCase):
    """Series of 5 increasingly complex tests that ensure that CheckersGame.py can operate as described."""

    def test_Player_Assignment(self):
        """Test that ensures that the player for the designated color is created and assigned properly."""
        test_game = check.Checkers()
        test_game.create_player('Rod', 'Black')
        test_game.create_player('James', 'White')
        self.assertEqual(test_game.get_black().get_name() + test_game.get_black().get_color(), "RodBlack")

    def test_No_Capturing_Gameplay(self):
        """Test that ensures that a move that captures no pieces can be made without errors and returns 0 correctly"""
        test_game = check.Checkers()
        test_game.create_player('Rod', 'Black')
        test_game.create_player('James', 'White')
        pieces_captured = test_game.play_game('Rod', (5, 0), (4, 1))
        self.assertIs(pieces_captured, 0)

    def test_Black_Capturing_Gameplay(self):
        """Test that ensures that both capturing moves and non-capturing can be played without errors and that the
        correct number of captured pieces is returned + noted in the pieces dictionary"""
        test_game = check.Checkers()
        test_game.create_player('Rod', 'Black')
        test_game.create_player('James', 'White')
        test_game.play_game('Rod', (5, 0), (4, 1))
        test_game.play_game('James', (2, 3), (3, 2))
        pieces_captured = test_game.play_game('Rod', (4, 1), (2, 3))
        self.assertIs(pieces_captured, 1)
        self.assertEqual(test_game.get_black().get_captured_pieces_count(), 1)

    def test_White_Capturing_Gameplay(self):
        """Test that ensures that all moves leading up to and including creating a king are correct and error free and
        that the pieces dictionary + board are correctly updated."""
        test_game = check.Checkers()
        test_game.create_player('Rod', 'Black')
        test_game.create_player('James', 'White')
        test_game.play_game('Rod', (5, 0), (4, 1))
        test_game.play_game('James', (2, 3), (3, 2))
        test_game.play_game('Rod', (4, 1), (2, 3))
        pieces_captured = test_game.play_game('James', (1, 4), (3, 2))
        self.assertIs(pieces_captured, 1)
        self.assertEqual(test_game.get_white().get_captured_pieces_count(), 1)

    def test_Black_King_Gameplay(self):
        """Test that ensures that many moves up to and including the creation of a triple king can be executed error
        free while still maintaining the board and pieces dictionary as up to date."""
        test_game = check.Checkers()
        test_game.create_player('Rod', 'Black')
        test_game.create_player('James', 'White')
        test_game.play_game('Rod', (5, 0), (4, 1))
        test_game.play_game('James', (2, 3), (3, 2))
        test_game.play_game('Rod', (4, 1), (2, 3))
        test_game.play_game('James', (1, 4), (3, 2))
        test_game.play_game('Rod', (5, 2), (4, 3))
        test_game.play_game('James', (2, 5), (3, 4))
        test_game.play_game('Rod', (6, 1), (5, 0))
        test_game.play_game('James', (0, 3), (1, 4))
        test_game.play_game('Rod', (4, 3), (2, 5))
        test_game.play_game('Rod', (2, 5), (0, 3))
        self.assertEqual(test_game.get_board()[0][3], "Black_king")
        self.assertIs(test_game.get_black().get_king_count(), 1)
        self.assertIs(test_game.get_black().get_captured_pieces_count(), 3)


if __name__ == '__main__':
    unittest.main()
