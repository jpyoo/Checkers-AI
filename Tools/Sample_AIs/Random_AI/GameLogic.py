from BoardClasses import *
import sys
sys.path.append("./AI_Extensions/")
from AI_Extensions import *
#from StudentAI import StudentAI
from StudentAI import StudentAI
from ManualAI import ManualAI

import json
NODES_FILE_PATH = "monte_carlo_nodes_"

def is_game_over(board):
    if board.is_win(1) or board.is_win(2) or board.tie_counter >= 40:
        return True
    return False

class GameLogic:

    def __init__(self,col,row,p,mode,debug):
        self.col = col
        self.row = row
        self.p = p
        self.mode = mode
        self.debug = debug
        self.ai_list = []

    def gameloop(self,fh=None):
        player = 1
        winPlayer = 0
        move = Move([])
        board = Board(self.col,self.row,self.p)
        board.initialize_game()
        board.show_board(fh)
        while True:
            try:
                move = self.ai_list[player-1].get_move(move)
            except:
                import traceback
                print("Player",player,"crashed!",file=fh)
                traceback.print_exc(file=fh)
                if player == 1:
                    winPlayer = 2
                else:
                    winPlayer = 1
                break
            try:
                board.make_move(move,player)
            except InvalidMoveError:
                print("Invalid Move!",file=fh)
                if player == 1:
                    winPlayer = 2
                else:
                    winPlayer = 1
                break
            winPlayer = board.is_win(player)
            board.show_board(fh)
            if(winPlayer != 0):
                if self.mode == 'n':#Communate with peer to tell the result.
                    if player == 1:
                        temp_player = 2
                    else:
                        temp_player = 1
                    if type(self.ai_list[temp_player - 1]) is NetworkAI:
                        self.ai_list[temp_player - 1].sent_final_result(move)
                break
            if player == 1:
                player = 2
            else:
                player = 1
        if winPlayer == -1:
            print("Tie",file=fh)
        else:
            print('player',winPlayer,'wins',file=fh)
        if self.mode == 'n' or self.mode == 'network' or self.mode == 'l' or self.mode == 'local':
            for AI in self.ai_list:
                if type(AI) is IOAI:
                    AI.close()
        #if not keyboard inturupt, saev mcts
        
        self.save_mcts(winPlayer, board)

        return winPlayer

    def TournamentInterface(self):
        ai = StudentAI(self.col,self.row,self.p)
        while True:
            move = Move.from_str(input().rstrip())
            result = ai.get_move(move)
            print(result)

    '''
    The parameters should be changed DURING/AFTER the implementation of Board.
    '''

    def Run(self,fh=None,**kwargs):
        if self.mode == 'n' or self.mode == 'network' :
            if kwargs['mode'] == 'host':
                self.ai_list.append(
                    IOAI(self.col, self.row, self.p, ai_path=kwargs['ai_path'], time=kwargs['time']))
                self.ai_list.append(
                    NetworkAI(self.col, self.row, self.p, mode=kwargs['mode'], info=kwargs['info']))

            else:
                self.ai_list.append(
                    NetworkAI(self.col, self.row, self.p, mode=kwargs['mode'], info=kwargs['info']))
                self.ai_list.append(
                    IOAI(self.col, self.row, self.p, ai_path=kwargs['ai_path'], time=kwargs['time']))


            self.gameloop(fh)
        elif self.mode == 'm' or self.mode == 'manual' :
            if kwargs['order'] == '1':
                self.ai_list.append(
                    ManualAI(self.col, self.row, self.p))
                self.ai_list.append(
                    StudentAI(self.col, self.row, self.p))
            else:
                self.ai_list.append(
                    StudentAI(self.col, self.row, self.p))
                self.ai_list.append(
                    ManualAI(self.col, self.row, self.p))
            self.gameloop(fh)
        elif self.mode == 's' or self.mode == 'self':
            if kwargs['order'] == '1':
                self.ai_list.append(
                    StudentAI(self.col, self.row, self.p))
                self.ai_list.append(
                    StudentAI(self.col, self.row, self.p))
            else:
                self.ai_list.append(
                    StudentAI(self.col, self.row, self.p))
                self.ai_list.append(
                    StudentAI(self.col, self.row, self.p))
            self.gameloop(fh)
        elif self.mode == 'l' or self.mode == 'local' :
            self.ai_list.append(
                IOAI(self.col, self.row, self.p, ai_path=kwargs['ai_path_1'], time=kwargs['time']))
            self.ai_list.append(
                IOAI(self.col, self.row, self.p, ai_path=kwargs['ai_path_2'], time=kwargs['time']))
            return self.gameloop(fh)
        elif self.mode == 't':
            self.TournamentInterface()

    def save_mcts(self, winner, board):
        opponent = {1: 2, 2: 1}
        # update nodes
        if winner != -1:
            filepath = NODES_FILE_PATH + str(winner) + ".json"
            loser_filepath = NODES_FILE_PATH + str(opponent[winner]) + ".json"
        else:
            filepath = NODES_FILE_PATH + "1.json"
            loser_filepath = NODES_FILE_PATH + "2.json"
        
        json_data = self.load_nodes_from_file(filepath)
        loser_jason_data = self.load_nodes_from_file(loser_filepath)
        while board.saved_move:
            k = ''
            for i in range(board.col):
                for j in range(board.row):
                    k += str(board.board[i][j].color)
            if k not in json_data.keys():
                json_data.update({k : {'wins': 0, 'visits': 0}})
            if k not in loser_jason_data.keys():
                loser_jason_data.update({k : {'wins': 0, 'visits': 0}})
            if winner != -1:
                json_data[k]['wins'] += 1
            json_data[k]['visits'] += 1
            loser_jason_data[k]['visits'] += 1
            board.undo()
        self.save_nodes_to_file(json_data, filepath)
        self.save_nodes_to_file(loser_jason_data, loser_filepath)
        print('mcts saved')

    def load_nodes_from_file(self, path):
        filepath = path
        try:
            with open(filepath, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_nodes_to_file(self, nodes, path):
        filepath = path
        try:
            with open(filepath, 'w') as file:
                json.dump(nodes, file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}


