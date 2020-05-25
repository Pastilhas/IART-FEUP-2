import sys
import q_learning
from levels import get_level


class Game:
    def __init__(self):
        self.run = True
        self.win = False
        self.level = 6
        self.board = []
        self.lastState = None
        self.currState = []
        self.generate_board()
        self.actions = self.getActions()
        self.ai = q_learning.Qlearning(len(self.actions), 0.2, 0.9)
        self.file = open("result.txt", "w")

    def update(self):
        move = self.getAIMove()
        self.make_move(move)


        last_action_id = self.currState[-1]
        last_action = self.actions[last_action_id]
        self.file.write("    id(" + str(last_action_id) + ") => [" + str(last_action[0]) + "," + str(last_action[1]) + "] - " + str(last_action[2]) + "\n")


        if self.win:
            reward = 100
            self.ai.update_table(tuple(self.lastState), move['action'], reward, tuple(self.currState))
            #self.print_board()
            #print('Win - New board')
            self.file.write("Win\n")
            self.generate_board()
            self.lastState = None
            self.currState = []
            self.win = False
            return True
        elif self.fail():
            reward = -50
            self.ai.update_table(tuple(self.lastState), move['action'], reward, tuple(self.currState))
            #self.print_board()
            #print('Lose - New board')
            self.file.write("Lose\n")
            self.generate_board()
            self.lastState = None
            self.currState = []
            return False
        else:
            reward = -1
            self.ai.update_table(tuple(self.lastState), move['action'], reward, tuple(self.currState))
            return None


    def generate_board(self):
        self.board = [[0]*8 for i in range(8)]
        level = get_level(self.level)
        pos = 0
        for i in range(0, 8):
            for j in range(0, 8):
                self.board[i][j] = level[pos]
                pos += 1

    def make_move(self, move):
        self.lastState = self.currState[:]
        self.currState.append(move['action'])
        coords = move['coords']
        direction = move['direction']
        #print('Move: ', coords, ' - ', direction)
        moves = int(self.board[coords[1]][coords[0]])
        self.board[coords[1]][coords[0]] = '-2'
        tile = coords
        while moves > 0:
            if direction == 0:
                tile[0] += 1
                if tile[0] > 7:
                    return
                else:
                    if self.board[tile[1]][tile[0]] == '-1':
                        self.win = True
                    elif self.board[coords[1]][coords[0]] == '0':
                        self.board[coords[1]][coords[0]] = '-2'
                        moves -= 1
            if direction == 1:
                tile[1] -= 1
                if tile[1] < 0:
                    return
                else:
                    if self.board[tile[1]][tile[0]] == '-1':
                        self.win = True
                    elif self.board[coords[1]][coords[0]] == '0':
                        self.board[coords[1]][coords[0]] = '-2'
                        moves -= 1
            if direction == 2:
                tile[0] -= 1
                if tile[0] < 0:
                    return
                else:
                    if self.board[tile[1]][tile[0]] == '-1':
                        self.win = True
                    elif self.board[coords[1]][coords[0]] == '0':
                        self.board[coords[1]][coords[0]] = '-2'
                        moves -= 1
            if direction == 3:
                tile[1] += 1
                if tile[1] > 7:
                    return
                else:
                    if self.board[tile[1]][tile[0]] == '-1':
                        self.win = True
                    elif self.board[coords[1]][coords[0]] == '0':
                        self.board[coords[1]][coords[0]] = '-2'
                        moves -= 1

    def print_board(self):
            print('+---+---+---+---+---+---+---+---+')
            for i in self.board:
                line = '| '
                for j in i:
                    if j == '-2':
                        line += 'X'
                    elif j == '-1':
                        line += 'F'
                    elif j == '0':
                        line += ' '
                    else:
                        line += str(j)
                    line += ' | '
                print(line)
                print('+---+---+---+---+---+---+---+---+')

    def fail(self):
        for i in self.board:
            for j in i:
                if int(j) > 0:
                    return False
        return True

    def getActions(self):
        actions = []

        for y,line in enumerate(self.board):
            for x,cell in enumerate(line):
                if int(cell) > 0:
                    for d in range(4):
                        actions.append((x,y,d))    # each action is a tuple(x,y,d)    x,y are coords of cell and d indicates direction
        return actions

    def getAIMove(self):
        possible_actions = []
        for i,line in enumerate(self.board):
            for j,cell in enumerate(line):
                if int(cell) > 0:
                    for k in range(4):
                        possible_actions.append(self.actions.index((j,i,k)))


        action_index = self.ai.take_action(tuple(self.currState), possible_actions)

        action = list(self.actions[action_index])
        move = {
            'action': action_index,
            'coords': [action[0],action[1]],
            'direction': action[2]
        }
        return move


Game = Game()
game_try = 0
total_tries = 10000

Game.ai.epsilon = 0.8                           # Exploring phase high epsilon
Game.file.write("Game " + str(game_try) + "\n")
while game_try < total_tries:
    result = Game.update()
    if result is not None:
        game_try += 1
        if game_try == total_tries:
            break
        Game.file.write("Game " + str(game_try) + "\n")

game_try = 0
Game.ai.epsilon = 0.2                           # Exploiting phase low epsilon
Game.file.write("Game " + str(game_try) + "\n")
while game_try < total_tries:
    result = Game.update()
    if result is not None:
        game_try += 1
        if game_try == total_tries:
            break
        Game.file.write("Game " + str(game_try) + "\n")

Game.ai.saveTo("results/txt_result.txt", [(10000, 0.2, 0.9, 0.8), (10000, 0.2, 0.9, 0.2)])
Game.ai.csvTo("results/csv_result.csv", [(10000, 0.2, 0.9, 0.8), (10000, 0.2, 0.9, 0.2)])
Game.file.close()
