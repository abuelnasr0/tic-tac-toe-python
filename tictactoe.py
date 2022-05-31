"""
Tic Tac Toe Player
"""
import copy

X = "X"
O = "O"
inf = 10000
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
    num_of_Xs = 0
    num_of_Os = 0
    for rows in board :
        for D in rows :
            if D == X :
                num_of_Xs+=1
            elif D == O :
                num_of_Os+=1
    if num_of_Xs == num_of_Os :
        return X
    elif num_of_Os < num_of_Xs :
        return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = []
    for i in range(3) :
        for j in range(3)  :
            if board[i][j] == None :
                action = (i,j)
                actions.append(action)

    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    player_turn = player(board)
    board_copy = copy.deepcopy(board)
    i = action[0]
    j = action[1]
    board_copy[i][j] = player_turn

    return board_copy

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if ((board[0][0] == board[0][1] == board[0][2] != EMPTY) or (board[1][0] == board[1][1] == board[1][2] != EMPTY) or (board[2][0] == board[2][1] == board[2][2] != EMPTY) or
        (board[0][0] == board[1][0] == board[2][0] != EMPTY) or (board[0][1] == board[1][1] == board[2][1] != EMPTY) or (board[0][2] == board[1][2] == board[2][2] != EMPTY) or
        (board[0][0] == board[1][1] == board[2][2] != EMPTY) or (board[0][2] == board[1][1] == board[2][0] != EMPTY)):

        if player(board) == X :
            return O
        elif player(board) == O :
            return X
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    def moves_allowed(B):
        for r in B :
            for c in r :
                if c == EMPTY :
                    return True
        return False
    if (winner(board)==X or winner(board)==O):
        return True
    elif not(moves_allowed(board)):
        return True
    else:
        return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board)==X :
        return 1
    if winner(board)==O :
        return -1
    else :
        return 0

def evaluation(board):
    pos_actions = actions(board)
    if player(board) == X :
        for action in pos_actions :
            if winner(result(board,action)) == X:
                return 1
    elif player(board) == O :
        for action in pos_actions :
            if winner(result(board,action)) == O:
                return -1

    return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    best_action = None

    if player(board) == O :
        min = inf
        actions_set = actions(board)
        for action in actions_set :
            new_min = maxvalue(result(board,action),min,0)
            if (min > new_min ):
                min = new_min
                best_action = action

    elif player(board) == X:
        max = -inf
        actions_set = actions(board)
        for action in actions_set:
            new_max = minvalue(result(board, action),max,0)
            if (max < new_max):
                max = new_max
                best_action = action

    return best_action


def minvalue(board,V,depth):
    #The termination condition of the recursion
    if terminal(board):
        return utility(board)

    # depth limited minimax
    if depth >=6:
        # to make a depth limit you must make evaluation function that estimate the expected utility
        return evaluation(board)

    #initial value of the utility
    u = inf
    #looping on actions and choosing the min of the maximums
    for action in actions(board) :
        new_u = maxvalue(result(board,action),u,depth+1)
        if u > new_u:
            u = new_u
        #Alpha peta Pruning
        if u < V:
            #If the utility of a new action (AN) in minvalue function which is the child of the peresent action((AX2) in maxvalue function) is smaller than
            #the expected utility of the previous action((AX1 the brother of (AX2)) in maxvalue function)
            #then no need to continue looping on the brothers of (AN) in minvalue function
            #because the utility deriven from minvalue function must be less than or equal to the current utility (minvalue function chooses minimum)
            #and this will be less than the previous utility chosen by the maxvalue
            #and we know the maxvalue function will choose the max of minimums
            #so the utility will remain the same in maxvalue function with continue looping or without
            #so no need to consume time
            break
    return u

def maxvalue(board,V,depth):
    #The termination condition of the recursion
    if terminal(board) :
        return utility(board)

    # depth limited minimax
    if depth >=6:
        # to make a depth limit you must make evaluation function that estimate the expected utility
        return evaluation(board)

    #initial value of the utility
    u = -inf
    # looping in the actions and choosing the max of the minimums
    for action in actions(board) :
        new_u = minvalue(result(board,action),u,depth+1)
        if u < new_u :
            u = new_u
        # Alpha peta Pruning
        if u > V :
            break
    return u
