class Color(object):
    EMPTY = 0
    BLACK = 1
    WHITE = 2

    @classmethod
    def invert(cls, color):
        if color == cls.EMPTY:
            return color
        return cls.BLACK if color == cls.WHITE else cls.WHITE


class Empty(object):
    color = Color.EMPTY

    def get_moves(self, board, y, x):
        raise Exception("Error !")

    def __repr__(self):
        return ' . '


class ChessMan(object):
    fig = None

    def __init__(self, color):
        self.color = color

    def __str__(self):
        return self.fig[0 if self.color == Color.WHITE else 1]

    def enemy_color(self):
        return Color.invert(self.color)


class King(ChessMan):
    fig = (' K ', ' k ')

    def get_moves_pas(self, board, y, x):
        moves = []
        p = [[1, 1], [-1, 1], [-1, -1], [1, -1]]
        for k in p:
            for i in range(1, 8):
                y1, x1 = y + k[1] * i, x + k[0] * i
                if 0 <= y1 <= 7 and 0 <= x1 <= 7:
                    if board.get_color(y1, x1) == Color.EMPTY:
                        moves.append([y1, x1])
                    else:
                        break
        return moves

    def get_moves_attack(self, board, y, x):
        moves = []
        p = [[1, 1], [-1, 1], [-1, -1], [1, -1]]
        # ход срубить
        for k in p:
            fl = '0'
            for i in range(1, 8):
                y1, x1 = y + k[1] * i, x + k[0] * i
                # y2, x2 = y + k[1]*(i-1), x + k[0]*(i-1)
                if 0 <= y1 <= 7 and 0 <= x1 <= 7:
                    if board.get_color(y1, x1) == Color.EMPTY:
                        fl = fl + '0'
                        if fl.count('1') > 0:
                            moves.append([y1, x1])
                    elif board.get_color(y1, x1) != board.get_color(y, x):
                        fl = fl + '1'
                    else:
                        fl = fl + 'X'
                    if 'X' in fl or '11' in fl:
                        break

        return moves


class Checker(ChessMan):
    fig = (' O ', ' o ')

    def get_moves_pas(self, board, y, x):
        moves = []
        p = [[-1, 1], [-1, -1], [1, 1], [1, -1]]
        # просто сходить
        if self.color == Color.WHITE:
            p = [[-1, 1], [-1, -1]]
        if self.color == Color.BLACK:
            p = [[1, 1], [1, -1]]

        for k in p:
            y1, x1 = y + k[0], x + k[1]
            if 0 <= y1 <= 7 and 0 <= x1 <= 7:
                if board.get_color(y1, x1) == Color.EMPTY:
                    moves.append([y1, x1])
        return moves

    def get_moves_attack(self, board, y, x):
        moves = []
        p = [[1, 1], [-1, 1], [-1, -1], [1, -1]]
        # ход срубить
        for k in p:
            y1, x1 = y + 2 * k[1], x + 2 * k[0]
            y2, x2 = y + k[1], x + k[0]
            if 0 <= y1 <= 7 and 0 <= x1 <= 7:
                if board.get_color(y1, x1) == Color.EMPTY:
                    if board.get_color(y2, x2) == self.enemy_color():
                        moves.append([y1, x1])
        return moves


class Board(object):
    def __init__(self):
        self.board = [[Empty()] * 8 for i in range(8)]

    def start(self):
        self.board = [[Empty()] * 8 for i in range(8)]
        for i in range(8):
            for j in range(8):
                if i < 3 and (i + j) % 2 == 1:
                    self.board[i][j] = Checker(Color.BLACK)
                if i > 4 and (i + j) % 2 == 1:
                    self.board[i][j] = Checker(Color.WHITE)

    def get_color(self, y, x):
        return self.board[y][x].color

    def get_moves(self, y, x):
        mas = self.get_moves_pas(y, x)
        mas.extend(self.get_moves_attack(y, x))
        return mas

    def get_moves_pas(self, y, x):
        return self.board[y][x].get_moves_pas(self, y, x)

    def get_moves_attack(self, y, x):
        return self.board[y][x].get_moves_attack(self, y, x)

    def move(self, y1, x1, y2, x2):
        p = [[1, 1], [-1, 1], [-1, -1], [1, -1]]
        m = [int((y2 - y1) > 0), int((x2 - x1) > 0)]
        if m[0] == 0: m[0] = -1
        if m[1] == 0: m[1] = -1
        print(m)
        print(abs(y2 - y1))
        number = -1
        for i in range(len(p)):
            if m == p[i]:
                number = i
        self.board[y2][x2] = self.board[y1][x1]
        self.board[y1][x1] = Empty()
        for i in range(abs(y2 - y1)):
            self.board[y1 + p[number][0] * i][x1 + p[number][1] * i] = Empty()

    def is_empty(self, y, x):
        self.board[y][x] = Empty()

    def b_with_possibilities(self, n, y1, x1):
        c = self.board
        if self.board[y1][x1].color == Color.EMPTY:
            return c

        attack = self.get_moves_attack(y1, x1)
        pas = self.get_moves_pas(y1, x1)

        if len(attack) > 0:

            for i in attack:
                y, x = i[0], i[1]
                # c[y][x] = ' * '
                c[y][x] = f"*{str(c[y][x]).replace(' ', '')}*"

        else:
            for i in pas:
                y, x = i[0], i[1]
                # c[y][x] = ' * '
                c[y][x] = f"*{str(c[y][x]).replace(' ', '')}*"

    def __str__(self):
        res = '\n' + '  '.join(['   A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']) + '\n\n'
        for y in range(8, 0, -1):
            res = res + f"{y} {''.join(map(str, self.board[8 - y]))} {y} \n"
        res += "\n" + '  '.join(['   A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']) + '\n'
        return res


class Game(Board):
    def __init__(self):
        can_attack = 0
        # can_white_attack = 0
        b = Board()
        b.start()
        n = Note()
        # spec = SpecialRules()
        # self.board = b.board
        self.movies = 1
        self.player_color = Color.WHITE
        print(b)
        while True:
            if self.player_color == Color.WHITE and self.movies == 1:
                b.start()
            print(f"Ход {'белых' if self.player_color == Color.WHITE else 'черных'}")
            s = input()

            if len(s) == 0:
                break

            elif s == 'сначала':
                b.start()
                self.player_color = Color.WHITE
                print(b)

            elif s == 'запись':
                print(n.pretty_write())

            elif 'вернуть на' in s:
                moves = int(s.split()[2])
                b = n.annul(b, moves)
                print(b)
                if moves % 2 != 0: self.player_color = Color.invert(self.player_color)

            elif 'возможные ходы' in s:
                motion1 = self.inp_coord(s.split()[2])
                y, x = motion1[0], motion1[1]
                c = b
                # c = self.b_with_possibilities(b, y, x)
                c.b_with_possibilities(n, y, x)
                print(c)
                b = n.annul(b, 0)



            else:

                motion1, motion2 = s.split()
                print(f"Ход от {self.inp_coord(motion1)} в {self.inp_coord(motion2)}")
                # print(b.get_moves(*self.inp_coord(motion1)))
                checks = self.check(b, motion1, motion2)

                if checks == 'Можно':
                    xy_from = self.inp_coord(motion1)
                    xy_to = self.inp_coord(motion2)
                    y1, x1 = xy_from[0], xy_from[1]
                    y2, x2 = xy_to[0], xy_to[1]
                    if len(b.get_moves_attack(y1, x1)) > 0:
                        can_attack = 1

                    n.read(y1, x1, y2, x2)
                    b.move(y1, x1, y2, x2)
                    self.check_king(b, y2, x2)
                    print(b)

                else:
                    print(checks)
                self.change_color(b, can_attack, y2, x2)

    def change_color(self, b, can_attack, y2, x2):
        if can_attack and len(b.get_moves_attack(y2, x2)) > 0:
            return 0

        if self.player_color == Color.WHITE:
            self.movies += 1
            self.player_color = Color.BLACK
        else:
            self.player_color = Color.WHITE
        return 1

    def check(self, b, xy_from, xy_to):
        if self.check_inp(b, xy_from, xy_to):
            motion1, motion2 = xy_from, xy_to
            xy_from = self.inp_coord(xy_from)
            xy_to = self.inp_coord(xy_to)
            y1, x1 = xy_from[0], xy_from[1]
            y2, x2 = xy_to[0], xy_to[1]
            if self.check_color(b, y1, x1, y2, x2):
                if self.check_move(b, y1, x1, y2, x2):
                    return 'Можно'
                else:
                    moves = ', '.join(self.return_coords(b.get_moves(y1, x1)))
                    return f'У фигуры на {motion1} хода на {motion2} нет. Возможные ходы из {motion1}: {moves}'
            else:
                return 'Нельзя ходить пустой клеткой и чужой фигурой'
        else:
            return 'Такой клетки не существует'

    def check_inp(self, b, xy_from, xy_to):
        if xy_from[0] in 'abcdefgh' and xy_from[1] in '12345678':
            if xy_to[0] in 'abcdefgh' and xy_to[1] in '12345678':
                return True
        return False

    def check_color(self, b, y1, x1, y2, x2):
        return b.board[y1][x1].color == self.player_color and b.board[y2][x2].color != self.player_color

    def check_move(self, b, y1, x1, y2, x2):
        if len(b.get_moves_attack(y1, x1)) > 0:
            return [y2, x2] in b.get_moves_attack(y1, x1)
        return [y2, x2] in b.get_moves(y1, x1)

    def inp_coord(self, xy):
        s = "abcdefgh"
        return [8 - int(xy[1]), s.index(xy[0])]

    def return_coord(self, y, x):
        y = 8 - y
        return f'{"abcdefgh"[x]}{y}'

    def return_coords(self, m):
        k = []
        for i in m:
            k.append(self.return_coord(i[0], i[1]))
        return k

    def check_king(self, b, y2, x2):
        if b.board[y2][x2].color == Color.WHITE:
            if y2 == 0:
                b.board[y2][x2] = King(Color.WHITE)

        if b.board[y2][x2].color == Color.BLACK:
            if y2 == 0:
                b.board[y2][x2] = King(Color.BLACK)


class Note(Game):
    def __init__(self):
        self.notes = []

    def read(self, y1, x1, y2, x2):
        self.notes.append([[y1, x1], [y2, x2]])

    def coords(self, y, x):
        y = 8 - y
        return f'{"abcdefgh"[x]}{y}'

    def pretty_write(self):
        k = ''
        n = self.notes
        for i in range(len(n)):
            ki = ''
            for j in range(2):
                xy = self.coords(n[i][j][0], n[i][j][1])
                ki += xy
            if i % 2 == 0:
                k = f"{k}{str((i + 2) // 2)}. {ki} |"
            else:
                k = f'{k} {ki} \n'
        return k

    def annul(self, b, moves):
        n = self.notes
        b.start()
        for i in range(len(n) - moves):
            y1, x1, y2, x2 = n[i][0][0], n[i][0][1], n[i][1][0], n[i][1][1]
            b.move(y1, x1, y2, x2)

        return b


Game()
