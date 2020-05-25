import sys
from levels import get_level


class Game:
    def __init__(self):
        self.run = True
        self.win = False
        self.level = 6
        self.board = []

    def play(self):
        self.generate_board()
        while self.run:
            self.print_board()
            coords = self.get_tile()
            direction = self.get_direction()
            self.make_move(coords, direction)
            fail = self.fail()
            if self.win:
                self.print_board()
                print('You win')
                sys.exit()
            elif fail:
                self.print_board()
                print('No moves left')
                sys.exit()

    def generate_board(self):
        self.board = [[0]*8 for i in range(8)]
        level = get_level(self.level)
        pos = 0
        for i in range(0, 8):
            for j in range(0, 8):
                self.board[i][j] = level[pos]
                pos += 1

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

    def get_tile(self):
        while True:
            answer = input('Choose a tile (x/y): ')
            coords = answer.split('/')
            coords = [int(n) for n in coords]
            if(coords[0] >= 0 and coords[0] <= 7 and coords[1] >= 0 and coords[1] <= 7 and self.board[coords[1]][coords[0]] > '0'):
                return coords

    def get_direction(self):
        while True:
            d = input('Choose a direction [0-3]: ')
            d = int(d)
            if(d >= 0 and d <= 3):
                return d

    def make_move(self, coords, direction):
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
                    elif self.board[coords[1]][coords[0]] == 0:
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

    def fail(self):
        for i in self.board:
            for j in i:
                if int(j) > 0:
                    return False
        return True

Game = Game()
Game.play()
