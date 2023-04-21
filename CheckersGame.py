# Author: Demetrios Kopatsis
# GitHub username: kopatsis
# Date: 03/08/2023
# Description: Contains the Player and Checkers classes as well as OutOfTurn, InvalidSquare, and InvalidPlayer Exception
# classes. Checkers class is not complete, however all methods described in the readme have been declared and at least
# have a descriptive docstring on how they will operate. All other methods including those from the Player class have
# been coded so far but are subject to change after completion and testing.

class OutofTurn(Exception):
    """Raised if a player attempts to make a move when it is not their turn"""
    pass


class InvalidSquare(Exception):
    """Raised when a player attempts to access a square not on the board"""
    pass


class InvalidPlayer(Exception):
    """Raised when a move is attempted for a player that is neither black nor white on this board"""
    pass


class Player:
    """Exists to represent a checkers player with a name, color, and collection of pieces"""
    def __init__(self, name, color):
        self._name = name
        self._color = color
        self._pieces = {
            "normal": 12,
            "king": 0,
            "Triple_King": 0,
            "captured": 0
        }

    def get_name(self):
        """Takes no parameters and returns the name data member of this player"""
        return self._name

    def get_color(self):
        """Takes no parameters and returns the color data member of this player"""
        return self._color

    def get_king_count(self):
        """Takes no parameters and returns the king data member of this player from the pieces dict"""
        return self._pieces["king"]

    def get_triple_king_count(self):
        """Takes no parameters and returns the triple king data member of this player from the pieces dict"""
        return self._pieces["triple_king"]

    def get_captured_pieces_count(self):
        """Takes no parameters and returns the (other pieces) captured data member from the pieces dict"""
        return self._pieces["captured"]

    def ret_pieces(self):
        """Takes no parameters and returns the whole dict of pieces. Will be used to edit pieces."""
        return self._pieces


class Checkers:
    """Used to represent a checkers board, initialized to having a board with the exact configuration as designated
    upon start, with no players to represent black or white, and the starting turn being black."""
    def __init__(self):
        self._board = self.create_board()
        self._black = None
        self._white = None
        self._last_turn_jump = False
        self._white_turn = False

    def create_board(self):
        """Creates a board with the required specifications as 8 arrays of 8 item arrays, which are passed to the init
        function when called. Not meant to be called by outside user and takes no parameters"""
        temp = []
        for i in range(8):
            added = []
            for j in range(8):
                added.append(None)
            temp.append(added)
        for i in range(3):
            for j in range(8):
                if (i % 2 == 0 and j % 2 == 1) or (i % 2 == 1 and j % 2 == 0):
                    temp[i][j] = "White"
        for i in range(5, 8):
            for j in range(8):
                if (i % 2 == 0 and j % 2 == 1) or (i % 2 == 1 and j % 2 == 0):
                    temp[i][j] = "Black"
        return temp

    def get_board(self):
        """Takes no parameters, returns the whole board to an outside user. Used primarily for testing."""
        return self._board

    def create_player(self, name, color):
        """Creates a player which is assigned to the correct color as the player for this board.
        Has parameters of the name and color of the player and returns nothing"""
        if color == "Black":
            self._black = Player(name, color)
        else:
            self._white = Player(name, color)

    def get_white(self):
        """Takes no parameters, returns the player assigned to white. Used primarily for testing purposes."""
        return self._white

    def get_black(self):
        """Takes no parameters, returns the player assigned to black. Used primarily for testing purposes."""
        return self._black

    def play_game(self, player_name, starting_square_location, destination_square_location):
        """Takes the name of a player, starting location, and ending location as parameters and first validates that
        the move is allowed by raising any exceptions if needed. Then calls on make_move to alter the board for the
        move designated. Returns the number of pieces captured, 0 if none."""
        if self._white.get_name() == player_name:
            color = "White"
        elif self._black.get_name() == player_name:
            color = "Black"
        else:
            raise InvalidPlayer
        if (color == "White" and not self._white_turn) or (color == "Black" and self._white_turn):
            if not self._last_turn_jump:
                raise OutofTurn
            else:
                self._white_turn = not self._white_turn
                self._last_turn_jump = False
        if 0 > starting_square_location[0] or 7 < starting_square_location[0]:
            raise InvalidSquare
        if 0 > starting_square_location[1] or 7 < starting_square_location[1]:
            raise InvalidSquare
        if not self._board[starting_square_location[0]][starting_square_location[1]]:
            raise InvalidSquare
        if self._board[starting_square_location[0]][starting_square_location[1]][0:5] != color:
            raise InvalidSquare
        if self._board[starting_square_location[0]][starting_square_location[1]][6:] == "":
            piece = "normal"
        else:
            piece = self._board[starting_square_location[0]][starting_square_location[1]][6:]
        return self.make_move(color, piece, starting_square_location, destination_square_location)

    def make_move(self, color, piece, start, end):
        """Not meant for outside users. Takes 4 parameters of the color, type of piece moved, and start and end
        locations. Makes the move and edits the board+players involved and returns to play_game the number of captured
        pieces, if any."""
        capturing = True
        if abs(end[0]-start[0]) == 1 and abs(end[1]-start[1]) == 1:
            capturing = False
        if piece == "normal":
            if not capturing:
                if self._last_turn_jump:
                    raise OutofTurn
                self._board[end[0]][end[1]] = color
                self._board[start[0]][start[1]] = None
                self._white_turn = not self._white_turn
            else:
                self._board[end[0]][end[1]] = color
                self._board[start[0]][start[1]] = None
                skipped_pos = (int((start[0]+end[0])/2), int((start[1]+end[1])/2))
                if self._board[skipped_pos[0]][skipped_pos[1]][6:] == "":
                    taken_piece = "normal"
                else:
                    taken_piece = self._board[skipped_pos[0]][skipped_pos[1]][6:]
                if color == "White":
                    self._black.ret_pieces()[taken_piece] -= 1
                    self._white.ret_pieces()['captured'] += 1
                else:
                    self._white.ret_pieces()[taken_piece] -= 1
                    self._black.ret_pieces()['captured'] += 1
                self._board[skipped_pos[0]][skipped_pos[1]] = None
                self._last_turn_jump = True
            if (color == "Black" and end[0] == 0) or (color == "White" and end[0] == 7):
                self._board[end[0]][end[1]] = color + "_king"
                if color == "White":
                    self._white.ret_pieces()['normal'] -= 1
                    self._white.ret_pieces()['king'] += 1
                else:
                    self._black.ret_pieces()['normal'] -= 1
                    self._black.ret_pieces()['king'] += 1
            return 1 if capturing else 0
        elif piece == "king":
            if not capturing:
                if self._last_turn_jump:
                    raise OutofTurn
                self._board[end[0]][end[1]] = color + "_king"
                self._board[start[0]][start[1]] = None
                self._white_turn = not self._white_turn
            else:
                direction = [None, None]
                direction[0] = "-" if end[0] < start[0] else "+"
                direction[1] = "-" if end[1] < start[1] else "+"
                current_pos = [None, None]
                for i in range(1, abs(end[0]-start[0])):
                    current_pos[0] = start[0] + i if direction[0] == "+" else start[0] - i
                    current_pos[1] = start[1] + i if direction[1] == "+" else start[1] - i
                    if self._board[current_pos[0]][current_pos[1]] and self._board[current_pos[0]][current_pos[1]][0:5] != color:
                        if self._board[current_pos[0]][current_pos[1]][6:] == "":
                            taken_piece = "normal"
                        else:
                            taken_piece = self._board[current_pos[0]][current_pos[1]][6:]
                        if color == "White":
                            self._black.ret_pieces()[taken_piece] -= 1
                            self._white.ret_pieces()['captured'] += 1
                        else:
                            self._white.ret_pieces()[taken_piece] -= 1
                            self._black.ret_pieces()['captured'] += 1
                        self._board[current_pos[0]][current_pos[1]] = None
                self._board[end[0]][end[1]] = color + "_king"
                self._board[start[0]][start[1]] = None
                self._last_turn_jump = True
            if (color == "Black" and end[0] == 7) or (color == "White" and end[0] == 0):
                self._board[end[0]][end[1]] = color + "_Triple_King"
                if color == "White":
                    self._white.ret_pieces()['king'] -= 1
                    self._white.ret_pieces()['Triple_King'] += 1
                else:
                    self._black.ret_pieces()['king'] -= 1
                    self._black.ret_pieces()['Triple_King'] += 1
            return 1 if capturing else 0
        else:
            direction = [None, None]
            direction[0] = "-" if end[0] < start[0] else "+"
            direction[1] = "-" if end[1] < start[1] else "+"
            current_pos = [None, None]
            for i in range(1, abs(end[0] - start[0])):
                current_pos[0] = start[0] + i if direction[0] == "+" else start[0] - i
                current_pos[1] = start[1] + i if direction[1] == "+" else start[1] - i
                if self._board[current_pos[0]][current_pos[1]] and self._board[current_pos[0]][current_pos[1]][0:5] != color:
                    capturing = True
                elif self._board[current_pos[0]][current_pos[1]] and self._board[current_pos[0]][current_pos[1]][0:5] == color:
                    capturing = False
            ret = 0
            if not capturing:
                if self._last_turn_jump:
                    raise OutofTurn
                self._board[end[0]][end[1]] = color + "_Triple_King"
                self._board[start[0]][start[1]] = None
                self._white_turn = not self._white_turn
            else:
                direction = [None, None]
                direction[0] = "-" if end[0] < start[0] else "+"
                direction[1] = "-" if end[1] < start[1] else "+"
                current_pos = [None, None]
                for i in range(1, abs(end[0] - start[0])):
                    current_pos[0] = start[0] + i if direction[0] == "+" else start[0] - i
                    current_pos[1] = start[1] + i if direction[1] == "+" else start[1] - i
                    if self._board[current_pos[0]][current_pos[1]] and self._board[current_pos[0]][current_pos[1]][0:5] != color:
                        ret += 1
                        if self._board[current_pos[0]][current_pos[1]][6:] == "":
                            taken_piece = "normal"
                        else:
                            taken_piece = self._board[current_pos[0]][current_pos[1]][6:]
                        if color == "White":
                            self._black.ret_pieces()[taken_piece] -= 1
                            self._white.ret_pieces()['captured'] += 1
                        else:
                            self._white.ret_pieces()[taken_piece] -= 1
                            self._black.ret_pieces()['captured'] += 1
                        self._board[current_pos[0]][current_pos[1]] = None
                self._board[end[0]][end[1]] = color + "_Triple_King"
                self._board[start[0]][start[1]] = None
                self._last_turn_jump = True
            return ret

    def get_checker_details(self, square_location):
        """Takes 1 parameter of a square location on board. Validates this is a possible location and raises an
        exception if not. Returns the color and type of piece on the board if any."""
        if 0 > square_location[0] or 7 < square_location[0] or 0 > square_location[1] or 7 < square_location[1]:
            raise InvalidSquare
        return self._board[square_location[0]][square_location[1]]

    def game_winner(self):
        """Takes no parameters. Checks win conditions of number of pieces left and returns which color won, if any."""
        if self._black.get_captured_pieces_count() == 12:
            return "Black"
        if self._white.get_captured_pieces_count() == 12:
            return "White"
        return None

    def print_board(self):
        """Takes no parameters and returns nothing. Prints each position in an 18 space bubble so that they are all
        neatly aligned and easily readable."""
        for i in range(8):
            for j in range(8):
                if not self._board[i][j]:
                    print(self._board[i][j], end="")
                    print("              ", end="")
                elif self._board[i][j][6:] == "":
                    print(self._board[i][j], end="")
                    print("             ", end="")
                elif self._board[i][j][6:] == "king":
                    print(self._board[i][j], end="")
                    print("        ", end="")
                else:
                    print(self._board[i][j], end=" ")
            print()
        print()
