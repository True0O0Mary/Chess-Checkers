


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


class Pawn(ChessMan):
    fig = (' P ', ' p ')

    def get_moves(self, board, y, x):
        moves = []
        if self.color == Color.BLACK and y < 7:
            if board.get_color(y + 1, x) == Color.EMPTY:
                moves.append([y + 1, x])
            if y == 1 and board.get_color(y + 2, x) == Color.EMPTY:
                moves.append([y + 2, x])
            if x < 7 and board.get_color(y + 1, x + 1) == self.enemy_color():
                moves.append([y + 1, x + 1])
            if x > 1 and board.get_color(y + 1, x - 1) == self.enemy_color():
                moves.append([y + 1, x - 1])

        elif self.color == Color.WHITE and y > 0:
            moves = []
            if board.get_color(y - 1, x) == Color.EMPTY:
                moves.append([y - 1, x])
            if y == 6 and board.get_color(y - 2, x) == Color.EMPTY:
                moves.append([y - 2, x])
            if x < 7 and board.get_color(y - 1, x + 1) == self.enemy_color():
                moves.append([y - 1, x + 1])
            if x > 1 and board.get_color(y - 1, x - 1) == self.enemy_color():
                moves.append([y - 1, x - 1])

        return moves


class King(ChessMan):
    fig = (' K ', ' k ')

    def get_moves(self, board, y, x):
        moves = []
        for y2 in range(y - 1, y + 2):
            for x2 in range(x - 1, x + 2):
                if not y2 == x2 == 0:
                    if board.get_color(y2, x2) != board.get_color(y, x):
                        moves.append([y2, x2])

        return moves


class Knight(ChessMan):
    fig = (' N ', ' n ')

    def get_moves(self, board, y, x):
        moves = []
        for y2 in range(y - 2, y + 3):
            for x2 in range(x - 2, x + 3):
                if (y2 - y) ** 2 + (x2 - x) ** 2 == 5 and 0 <= y2 <= 7 and 0 <= x2 <= 7:
                    if board.get_color(y2, x2) != board.get_color(y, x):
                        moves.append([y2, x2])

        return moves


class Templar(ChessMan):
    fig = (' T ', ' t ')

    def get_moves(self, board, y, x):
        moves = []
        for y2 in range(y - 3, y + 4):
            for x2 in range(x - 3, x + 4):
                if (y2 - y) ** 2 + (x2 - x) ** 2 == 5 and 0 <= y2 <= 7 and 0 <= x2 <= 7:
                    if board.get_color(y2, x2) != board.get_color(y, x):
                        moves.append([y2, x2])
                if (y2 - y) ** 2 + (x2 - x) ** 2 == 13 and 0 <= y2 <= 7 and 0 <= x2 <= 7:
                    if board.get_color(y2, x2) == Color.EMPTY:
                        moves.append([y2, x2])

        return moves


class Champion(ChessMan):
    fig = (' C ', ' c ')

    def get_moves(self, board, y, x):
        moves = []
        for y2 in range(y - 2, y + 3):
            for x2 in range(x - 2, x + 3):
                if 0 <= y2 <= 7 and 0 <= x2 <= 7:
                    s = (x2 - x) ** 2 + (y2 - y) ** 2
                    if s == 1 or s == 4 or s == 8:
                        if board.get_color(y2, x2) != board.get_color(y, x):
                            moves.append([y2, x2])

        return moves


class Wizard(ChessMan):
    fig = (' W ', ' w ')

    def get_moves(self, board, y, x):
        moves = []
        for y2 in range(y - 3, y + 4):
            for x2 in range(x - 3, x + 4):
                if 0 <= y2 <= 7 and 0 <= x2 <= 7:
                    if board.get_color(y2, x2) != board.get_color(y, x):
                        d_y, d_x = abs(y2 - y), abs(x2 - x)
                        if (d_y, d_x) == (1, 3) or (d_y, d_x) == (3, 1) or (d_x, d_y) == (1, 3) or (d_x, d_y) == (
                                3, 1) or (x2 - x) ** 2 + (y2 - y) ** 2 == 1:
                            moves.append([y2, x2])

        return moves


class Bishop(ChessMan):
    fig = (' B ', ' b ')

    def get_moves(self, board, y, x):
        moves = []
        p = [[1, 1], [-1, 1], [-1, -1], [1, -1]]
        for k in p:
            for i in range(1, 8):
                y1, x1 = y + i * k[1], x + i * k[0]
                if not (0 <= y1 <= 7) or not (0 <= x1 <= 7):
                    break
                else:
                    if board.get_color(y, x) != board.get_color(y1, x1):
                        moves.append([y1, x1])
                    if board.get_color(y1, x1) != Color.EMPTY:
                        break

        return moves


class Rook(ChessMan):
    fig = (' R ', ' r ')

    def get_moves(self, board, y, x):
        moves = []
        for x1 in range(x + 1, 8):
            if board.get_color(y, x) != board.get_color(y, x1):
                moves.append([y, x1])
            if board.get_color(y, x1) != Color.EMPTY:
                break
        for x1 in range(x - 1, -1, -1):
            if board.get_color(y, x) != board.get_color(y, x1):
                moves.append([y, x1])
            if board.get_color(y, x1) != Color.EMPTY:
                break
        for y1 in range(y + 1, 8):
            if board.get_color(y, x) != board.get_color(y1, x):
                moves.append([y1, x])
            if board.get_color(y1, x) != Color.EMPTY:
                break
        for y1 in range(y - 1, -1, -1):
            if board.get_color(y, x) != board.get_color(y1, x):
                moves.append([y1, x])
            if board.get_color(y1, x) != Color.EMPTY:
                break
        return moves


class Queen(ChessMan):
    fig = (' Q ', ' q ')

    def get_moves(self, board, y, x):
        moves = []

        p = [[1, 1], [-1, 1], [-1, -1], [1, -1], [1, 0], [0, 1], [-1, 0], [0, -1]]
        for k in p:
            for i in range(1, 8):
                y1, x1 = y + i * k[1], x + i * k[0]
                if not (0 <= y1 <= 7) or not (0 <= x1 <= 7):
                    break
                else:
                    if board.get_color(y, x) != board.get_color(y1, x1):
                        moves.append([y1, x1])
                    if board.get_color(y1, x1) != Color.EMPTY:
                        break
        return moves


class Board(object):
    def __init__(self):
        self.board = [[Empty()] * 8 for i in range(8)]

    def start(self):
        self.board = [[Empty()] * 8 for i in range(8)]
        for i in range(8):
            self.board[1][i] = Pawn(Color.BLACK)
            self.board[6][i] = Pawn(Color.WHITE)
        self.board[0][0] = Rook(Color.BLACK)
        self.board[7][0] = Rook(Color.WHITE)
        self.board[0][1] = Knight(Color.BLACK)
        self.board[7][1] = Knight(Color.WHITE)
        self.board[0][2] = Bishop(Color.BLACK)
        self.board[7][2] = Bishop(Color.WHITE)
        self.board[0][3] = Queen(Color.BLACK)
        self.board[7][3] = Queen(Color.WHITE)
        self.board[0][4] = King(Color.BLACK)
        self.board[7][4] = King(Color.WHITE)
        self.board[0][5] = Bishop(Color.BLACK)
        self.board[7][5] = Bishop(Color.WHITE)
        self.board[0][6] = Knight(Color.BLACK)
        self.board[7][6] = Knight(Color.WHITE)
        self.board[0][7] = Rook(Color.BLACK)
        self.board[7][7] = Rook(Color.WHITE)
        # self.board[4][4] = Champion(Color.WHITE)
        # self.board[5][5] = Wizard(Color.WHITE)
        # self.board[4][6] = Templar(Color.WHITE)
        # self.board[4][4] = Queen(Color.WHITE)

    def get_color(self, y, x):
        return self.board[y][x].color

    def get_moves(self, y, x):
        return self.board[y][x].get_moves(self, y, x)

    def move(self, y1, x1, y2, x2):
        self.board[y2][x2] = self.board[y1][x1]
        self.board[y1][x1] = Empty()

    def is_empty(self, y, x):
        self.board[y][x] = Empty()

    def b_with_possibilities(self, y1, x1):
        c = self.board
        if self.board[y1][x1].color == Color.EMPTY:
            return c
        pos = self.get_moves(y1, x1)

        for i in pos:
            y, x = i[0], i[1]
            c[y][x] = f"*{str(c[y][x]).replace(' ', '')}*"

        return c

    def __str__(self):
        res = '\n' + '  '.join(['   A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']) + '\n\n'
        for y in range(8, 0, -1):
            res = res + f"{y} {''.join(map(str, self.board[8 - y]))} {y} \n"
        res += "\n" + '  '.join(['   A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']) + '\n'
        return res


class Game(Board):
    def __init__(self):
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
                c.b_with_possibilities(y, x)
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

                    n.read(y1, x1, y2, x2)
                    b.move(y1, x1, y2, x2)

                    print(b)
                    if self.player_color == Color.WHITE:
                        self.movies += 1
                        self.player_color = Color.BLACK
                    else:
                        self.player_color = Color.WHITE
                else:
                    print(checks)

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
        return [y2, x2] in b.get_moves(y1, x1)
        # or SpecialRules().get_moves_spec(b, n, y1, x1)

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

    # def b_with_possibilities(self, b, y1, x1):
    #     c = b.board
    #     pos = b.get_moves(y1, x1)
    #     for i in pos:
    #         y, x = i[0], i[1]
    #         c[y][x] = f'*{c[y][x]}*'
    #     return c


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
