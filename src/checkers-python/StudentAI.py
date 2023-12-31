from random import randint
from BoardClasses import Move
from BoardClasses import Board
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2
    def minimax_alpha_beta(self, board, depth, maximizing_player, alpha, beta):

        # if alpha > 3:
        #     return self.evaluate_board(board)
        
        if depth == 0:
            return self.evaluate_board2(board)
        if board.is_win(self.color):
            return float('inf')
        if board.is_win(self.opponent[self.color]):
            return float('-inf')
        if maximizing_player:
            max_eval = float('-inf')
            moves = board.get_all_possible_moves(self.color)
            for checker_moves in moves:
                for move in checker_moves:
                    board.make_move(move, self.color)
                    eval = self.minimax_alpha_beta(board, depth - 1, False, alpha, beta)
                    board.undo()
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    # print("MAX: move: ", move, " eval: ", eval)
                    if beta <= alpha:
                        break  # Beta cutoff
            return max_eval
        else:
            min_eval = float('inf')
            moves = board.get_all_possible_moves(self.opponent[self.color])
            for checker_moves in moves:
                for move in checker_moves:
                    board.make_move(move, self.opponent[self.color])
                    eval = self.minimax_alpha_beta(board, depth - 1, True, alpha, beta)
                    board.undo()
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    # print("min - move: ", move, " eval: ", eval)
                    if beta <= alpha:
                        break  # Alpha cutoff
            return min_eval
        
    def get_move(self,move):
        # arbitrarily set depth
        depth = 3

        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1

        moves = self.board.get_all_possible_moves(self.color)

        # #check if there are any jumps
        # for move in moves:
        #     for m in move:
        #         if (abs(m[0][0] - m[1][0]) + abs(m[0][1] - m[1][1]) ) == 4 :
        #             self.board.make_move(m,self.color)
        #             return m
                
        best_move = []
        best_score = float('-inf')

        for checker_moves in moves:
            for move in checker_moves:
                print("evaluating move: ", move)
                self.board.make_move(move, self.color)
                eval = self.minimax_alpha_beta(self.board, depth, False, float('-inf'), float('inf'))
                self.board.undo()
                if eval > best_score:
                    best_score = eval
                    best_move = move
        if len(best_move) > 0:

            # print("best score: ", best_score)
            # print("best move: ", best_move)

            self.board.make_move(best_move,self.color)
            return best_move
        
        # select random move
        index = randint(0,len(moves)-1)
        inner_index =  randint(0,len(moves[index])-1)
        move = moves[index][inner_index]

        self.board.make_move(move,self.color)
        return move

    def evaluate_board(self, board):
        # Count the number of possible jumps for the current player
        moves = board.get_all_possible_moves(self.color)
        jump_count = 0

        for move in moves:
            for m in move:
                if self.is_jump(m):
                    jump_count += 1

        return jump_count
    
    #evaluate board based on number of self colored pieces
    def evaluate_board2(self, board):
        count = 0
        checker_color = {1:'B',2:'W'}
        for row in self.board.board:
            for checker in row:
                # print(checker.color)
                if checker.color == checker_color[self.color]:
                    count += 1
                elif checker.color == checker_color[self.opponent[self.color]]:
                    count -= 1

        # self.board.show_board()
        # print("board eval: ", count)
        
        return count
    
    def is_jump(self, move):
        return (abs(move[0][0] - move[1][0]) + abs(move[0][1] - move[1][1]) ) == 4
