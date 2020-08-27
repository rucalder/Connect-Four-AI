import numpy as np

class Board:
    def __init__(self):
        self.prev_action = None


class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        if player_number == 1:
            self.opponent_number = 2
        else:
            self.opponent_number = 1
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.prev_move = None
        self.prev_opp = None
        self.depth = 4


    def max_value1(self, board, alpha, beta, t):

        #print("Board in max_value1: " + str(board))

        # Calculate number of available moves as list of columns
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        print("t = " + str(t))
        print("Board in max_value1: \n" + str(board))

        return_action = None 
        if t == 0 or game_completed(board, self.opponent_number):
            return self.evaluation_function(board, self.player_number)
        if game_completed(board, self.player_number):
            return self.evaluation_function(board, self.player_number)

        t -= 1
        v = -9999999

        temp_board = None
        # For every action a, create new tree
        for a in valid_cols:
            #temp_board = board
            update_row, move = update_board(a, self.player_number, board)
            #print("Board in max_value1: " + str(board))
            v1 = self.min_value(board, alpha, beta, t)
            v = max(v, v1)
            reset_board(board, update_row, move)
            if v >= beta:
                return v
            alpha = max(alpha, v)

        return v

    def min_value(self, board, alpha, beta, t):

        print("t = " + str(t))
        print("Board in min_value: \n" + str(board))

        # Calculate number of available moves as list of columns
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        return_action = None
        if t == 0 or game_completed(board, self.player_number):
            return self.evaluation_function(board, self.player_number)
        if game_completed(board, self.opponent_number):
            return self.evaluation_function(board, self.player_number)

        t -= 1
        v = 9999999

        temp_board = None
        # For every action a, create new tree 
        for a in valid_cols:
            #temp_board = board
            update_row, move = update_board(a, self.opponent_number, board)
            v1 = self.max_value1(board, alpha, beta, t)
            v = min(v, v1)
            reset_board(board, update_row, move)
            if v <= alpha:
                return v
            beta = min(beta, v)
            

        return v

    def get_alpha_beta_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the alpha-beta pruning algorithm

        This will play against either itself or a human player

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        player_num = self.player_number
        opponent_num = self.opponent_number
        print("Board in alphaBeta: " + str(board))
        #v, action = self.max_value1(board, -9999999, 9999999, 3)

        return_action = None
        v = -9999999
        alpha = -9999999
        beta = 9999999

        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        for action in valid_cols:
            #temp_board = board
            update_row, move = update_board(action, player_num, board)
            v1 = self.min_value(board, alpha, beta, self.depth)
            if v1 > v:
                return_action = action
            v = max(v, v1)
            reset_board(board, update_row, move)
            if v >= beta:
                pass
            alpha = max(alpha, v)

        
        return return_action

    def max_value2(self, board, t):

        # Calculate number of available moves as list of columns
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        return_action = None 
        if t == 0 or game_completed(board, self.player_number):
            return self.evaluation_function(board, self.player_number)
        if game_completed(board, self.opponent_number):
            return self.evaluation_function(board, self.player_number)

        t -= 1
        v = -9999999

        # For every action a, create new tree
        for a in valid_cols:
            #temp_board = board
            update_row, move = update_board(a, self.player_number, board)

            v1 = self.exp_value(board, t)
            v = max(v, v1)
            reset_board(board, update_row, move)

        return v

    def exp_value(self, board, t):

        # Calculate number of available moves as list of columns
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        return_action = None
        if t == 0 or game_completed(board, self.player_number):
            return self.evaluation_function(board, self.player_number)
        if game_completed(board, self.opponent_number):
            return self.evaluation_function(board, self.player_number)

        t -= 1
        v = 0

         # Calculate number of available moves as list of columns
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        for a in valid_cols:
            p = 1 / len(valid_cols)
            #temp_board = board
            update_row, move = update_board(a, self.opponent_number, board)
            value = self.max_value2(board, t)
            v += p * value
            reset_board(board, update_row, move)

        return v


    def get_expectimax_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the expectimax algorithm.

        This will play against the random player, who chooses any valid move
        with equal probability

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

        player_num = self.player_number
        opponent_num = self.opponent_number
        v= -9999999

        return_action = None

        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        for action in valid_cols:
            #temp_board = board
            update_row, move = update_board(action, player_num, board)
            v1 = self.exp_value(board, self.depth)
            if v1 > v:
                return_action = action
            v = max(v, v1)
            reset_board(board, update_row, move)

        return return_action



    def evaluation_function(self, board, player_num):
        """
        Given the current stat of the board, return the scalar value that 
        represents the evaluation function for the current player
       
        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The utility value for the current board
        """
        UTILITY_VALUE = 0
        if game_completed(board, self.player_number):
           return 999
        if game_completed(board, self.opponent_number):
            return -999

        #Iterate through every cell on the board
        for row in range(5):
            for col in range(6):
                # Iterate through 2x2 space around cell to see if there's
                # same pieces in line
                for y in range(-2, 2):
                    for x in range(-2, 2):
                        # Pass situations that are invalid
                        if x == 0 and y == 0:
                            pass
                        if row + y < 0 or row + y > 5:
                            pass
                        if col + x < 0 or col + x > 6:
                            pass

                        #Horizontal check
                        if x == 0:
                            if board[row + x][col + y] == self.player_number:
                                UTILITY_VALUE += 4
                                
                            elif board[row + x][col + y] == 0:
                                UTILITY_VALUE += 0
                            else:
                                UTILITY_VALUE -= 4
                            
                        #Vertical check
                        
                        if y == 0:
                            if board[row + x][col + y] == self.player_number:
                                UTILITY_VALUE += 4
                            
                            elif board[row + x, col + y] == 0:
                                UTILITY_VALUE += 0
                            else:
                                UTILITY_VALUE -= 4
                            

                        #Diagonal check
                        if abs(x) - abs(y) == 0:
                            if board[row + x][col + y] == self.player_number:
                                UTILITY_VALUE += 4
                            
                            elif board[row + x, col + y] == 0:
                                UTILITY_VALUE += 0
                            else:
                                UTILITY_VALUE -= 4


                        #Other checks
                        
                        # Prioritizes center board
                        if x == 2 or x == 3 or x == 4:
                            UTILITY_VALUE += 4
                            
                        

       
        return UTILITY_VALUE


class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state select a random column from the available
        valid moves.

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        return np.random.choice(valid_cols)


class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state returns the human input for next move

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move

def update_board(move, player_num, board):
        if 0 in board[:,move]:
            update_row = -1
            for row in range(1, board.shape[0]):
                update_row = -1
                if board[row, move] > 0 and board[row-1, move] == 0:
                    update_row = row-1
                elif row==board.shape[0]-1 and board[row, move] == 0:
                    update_row = row

                if update_row >= 0:
                    board[update_row, move] = player_num
                    return update_row, move
                    break
        else:
            err = 'Invalid move by player {}. Column {}'.format(player_num, move)
            #break
            #raise Exception(err)

def reset_board(board, row, col):
    board[row][col] = 0


def game_completed(board, player_num):
    player_win_str = '{0}{0}{0}{0}'.format(player_num)
    #board = self.board
    temp_board = board
    to_str = lambda a: ''.join(a.astype(str))

    def check_horizontal(b):
        for row in b:
            if player_win_str in to_str(row):
                return True
        return False

    def check_verticle(b):
        return check_horizontal(b.T)

    def check_diagonal(b):
        for op in [None, np.fliplr]:
            op_board = op(b) if op else b
            
            root_diag = np.diagonal(op_board, offset=0).astype(np.int)
            if player_win_str in to_str(root_diag):
                return True

            for i in range(1, b.shape[1]-3):
                for offset in [i, -i]:
                    diag = np.diagonal(op_board, offset=offset)
                    diag = to_str(diag.astype(np.int))
                    if player_win_str in diag:
                        return True

        return False

    return (check_horizontal(temp_board) or
            check_verticle(temp_board) or
            check_diagonal(temp_board))
