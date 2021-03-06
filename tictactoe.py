"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """

    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    X_counter = 0
    O_counter = 0
    #empty board means player X turn
    if board == EMPTY:
        return X
    elif terminal(board) == True:
        return None

    #count how many X and O's on board to determine player turn
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                X_counter += 1
            if board[i][j] == O:
                O_counter += 1
    if X_counter > O_counter:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    if terminal(board) == True:
        return "Game Over"
    else:
        #find empty spaces available for move on board
        actions_set = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    actions_set.append((i,j))
        return actions_set




def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    #copy of game board
    copy_board = copy.deepcopy(board)
    #action returned in (i,j) form, must convert for list
    x = action[0]
    y = action[1]
    for i in range(3):
        for j in range(3):
            if board[x][y] != EMPTY:
                raise Exception("Invalid action")
            elif player(board) == O:
                copy_board[x][y] = O
            elif player(board) == X:
                copy_board[x][y] = X
    return copy_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #convert board into list of columns rather than rows
    columns = list(zip(*board))
    # checking each row/column for 3 straight
    for i in range(3):
        if board[i].count(X) == 3:
            return X
        elif columns[i].count(X) == 3:
            return X
        elif board[i].count(O) == 3:
            return O
        elif columns[i].count(O) == 3:
            return O
    #check diagonals
    if board[0][0] == X and board[1][1] == X and board[2][2] == X:
        return X
    elif board[2][0] == X and board[1][1] == X and board[0][2] == X:
        return X
    elif board[0][0] == O and board[1][1] == O and board[2][2] == O:
        return O
    elif board[2][0] == O and board[1][1] == O and board[0][2] == O:
        return O

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    #counter for full board
    full_board = 0
    if winner(board) is not None:
        return True

    for i in range(3):
        for j in range(3):
            if board[i][j] != EMPTY:
                full_board += 1
                if full_board == 9:
                    return True

    return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board) == True:
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    optimal_move = []
    if terminal(board) == True:
        return None

    if player(board) == X:
        v = -math.inf
        for action in actions(board):
            #for alpha beta pruning
            if action != actions(board)[0]:
                temp_v = min_value(result(board, action), False)
            else:
                temp_v = min_value(result(board,action), True)
            if temp_v > v:
                v = temp_v
                optimal_move = action

        return optimal_move
    else:
        v = math.inf
        for action in actions(board):
            #for alpha beta pruning
            if action != actions(board)[0]:
                temp_v = max_value(result(board,action), False)
            else:
                temp_v = max_value(result(board,action), True)
            if temp_v < v:
                v = temp_v
                optimal_move = action
        return optimal_move

#is_first_action used for alpha beta pruning, once first action finished, we can use the solution from first action to determine whether we can skip possible following actions
def max_value(board, is_first_action):
    v = -math.inf
    #compare used as cpu picked value for first possible action made, all other actions following are compared to compare to determine if we can skip iterations (or possible actions)
    global compare
    if terminal(board):
        return utility(board)

    if is_first_action:
        for action in actions(board):
            temp_value = min_value(result(board,action), True)
            v = max(v,temp_value)
            compare = v
    else:
        for action in actions(board):
            #need to atleast investigate first action to get a value-->else:-->after that we can compare the other actions and skip if necessary
            if action != actions(board)[0]:
                if v > compare:
                    #do not need to check an action, skip
                    continue
                else:
                    temp_value = min_value(result(board,action), False)
            else:
                temp_value = min_value(result(board,action), False)
            v = max(v, temp_value)

    return v

#is_first_action used for alpha beta pruning, once first action finished, we can use the solution from first action to determine whether we can skip possible following actions
def min_value(board, is_first_action):
    v = math.inf
    global compare
    if terminal(board):
        return utility(board)
    if is_first_action:
        for action in actions(board):
            temp_value = max_value(result(board,action), True)
            v = min(v, temp_value)
            compare = v

    else:
        for action in actions(board):
            #need to atleast investigate first action to get a value-->else:-->after that we can compare the other actions and skip if necessary
            if action != actions(board)[0]:
                if v < compare:
                    #do not need to check action, skip
                    continue
                else:
                    temp_value = max_value(result(board,action), False)

            else:
                temp_value = max_value(result(board,action), False)
            v = min(v, temp_value)
    return v











