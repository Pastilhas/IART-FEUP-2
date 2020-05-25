import sys
import sarsa
from levels import get_level


class Game:
    def __init__(self):
        self.run = True
        self.win = False
        self.level = 6
        self.board = []
        self.last_state = None
        self.last_action = None
        self.curr_state = []
        self.generate_board()
        self.actions = self.get_actions()
        self.ai = sarsa.Sarsa(len(self.actions), 0.2, 0.9)
        self.file = open("result.txt", "w")

    def update(self):
        reward = self.get_reward()
        move = self.get_ai_move()

        if self.last_action is not None and move is not None:
            self.ai.update_table(tuple(self.last_state), self.last_action, reward, tuple(self.curr_state), move['action'])
        elif move is None:
            self.ai.update_table(tuple(self.last_state), self.last_action, reward, tuple(self.curr_state), None)

        if move is not None:
            self.last_action = move['action']
            self.last_state = self.curr_state
            last_action = self.actions[self.last_action]
            self.file.write("    id(" + str(self.last_action) + ") => [" + str(last_action[0]) + "," + str(last_action[1]) + "] - " + str(last_action[2]) + "\n")
        else:
            last_action = [None,None,None]


        if self.win:
            self.file.write("Win\n")
            self.reset_game()
            return True
        elif self.fail():
            self.file.write("Lose\n")
            self.reset_game()
            return False
        else:
            self.make_move(move)

    def get_reward(self):
        if self.win:
            return 100
        elif self.fail():
            return -50
        else:
            return -1

    def reset_game(self):
        self.generate_board()
        self.last_state = None
        self.last_action = None
        self.curr_state = []
        self.win = False

    def generate_board(self):
        self.board = [[0]*8 for i in range(8)]
        level = get_level(self.level)
        pos = 0
        for i in range(0, 8):
            for j in range(0, 8):
                self.board[i][j] = level[pos]
                pos += 1

    def make_move(self, move):
        self.curr_state.append(move['action'])

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

    def get_actions(self):
        actions = []

        for y, line in enumerate(self.board):
            for x, cell in enumerate(line):
                if int(cell) > 0:
                    for d in range(4):
                        # each action is a tuple(x,y,d)    x,y are coords of cell and d indicates direction
                        actions.append((x, y, d))
        return actions

    def get_ai_move(self):
        possible_actions = []
        for i, line in enumerate(self.board):
            for j, cell in enumerate(line):
                if int(cell) > 0:
                    for k in range(4):
                        possible_actions.append(self.actions.index((j, i, k)))
        if not possible_actions:
            return None
        action_index = self.ai.take_action(tuple(self.curr_state), possible_actions)

        action = list(self.actions[action_index])
        move = {
            'action': action_index,
            'coords': [action[0], action[1]],
            'direction': action[2]
        }
        return move


Game = Game()
game_try = 0
total_tries = 800000

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
