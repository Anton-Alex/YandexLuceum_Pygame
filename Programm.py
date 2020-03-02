import sys, pygame, random, os
from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    return image


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.password = ''
        self.Button_cross_zero.clicked.connect(self.cross_zero)
        self.Button_tag.clicked.connect(self.tag)
        self.show()

    def cross_zero(self):
        pygame.init()
        w = 500
        screen = pygame.display.set_mode((w, w))
        board = Board(3, 3, screen)
        running = True
        screen.blit(load_image("table.png"), (0, 0))
        board.begin()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    board.get_click(event.pos)
            board.render()
            board.check()
            pygame.display.flip()
        pygame.quit()

    def tag(self):
        pygame.init()
        w = 500
        screen = pygame.display.set_mode((w, w))
        board = Board_Tag(4, 4, screen)
        running = True
        screen.blit(load_image("table.png"), (0, 0))
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    board.get_click(event.pos)
            board.render()
            board.check()
            pygame.display.flip()
        pygame.quit()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        quit()


class Board:
    def __init__(self, width, height, screen):
        self.plaer = 1
        self.victories = 0
        self.screen = screen
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 100
        self.top = 100
        self.cell_size = 100

    def begin(self):
        self.plaer = 1
        self.victories = 0
        self.board = [[0] * self.width for _ in range(self.height)]
        a = 0
        for i in range(self.height):
            b = 0
            for i in range(self.width):
                self.screen.fill((255, 255, 255), ((self.left + self.cell_size * b),
                                                   (self.top + a * self.cell_size), self.cell_size,
                                                   self.cell_size))
                pygame.draw.rect(self.screen, (0, 0, 0), ((self.left + self.cell_size * b),
                                                   (self.top + a * self.cell_size), self.cell_size,
                                                   self.cell_size), 1)
                b += 1
            a += 1

    def render(self):
        a = 0
        for i in range(self.height):
            b = 0
            for i in range(self.width):
                if self.board[a][b] == 1:
                    pygame.draw.line(self.screen, (0, 0, 255), (self.left + b * self.cell_size,
                                                                self.top + a * self.cell_size),
                                     (self.left + (b + 1) * self.cell_size, self.top + (a + 1) * self.cell_size), 5)
                    pygame.draw.line(self.screen, (0, 0, 255),
                                     (self.left + (b + 1) * self.cell_size, self.top + a * self.cell_size),
                                     (self.left + b * self.cell_size, self.top + (a + 1) * self.cell_size), 5)
                elif self.board[a][b] == 2:
                    pygame.draw.circle(self.screen, (255, 0, 0), (self.left + b * self.cell_size + self.cell_size // 2,
                                                                  self.top + a * self.cell_size + self.cell_size // 2),
                                       self.cell_size // 2, 2)

                b += 1
            a += 1
        if self.plaer == 0:
            if self.victories == 0:
                font = pygame.font.Font(None, 100)
                text = font.render("Ничья", 1, (255, 0, 255))
                text_x = 150
                text_y = 200
                self.screen.blit(text, (text_x, text_y))
                font = pygame.font.Font(None, 30)
                text = font.render("Нажмите, чтобы продолжить", 1, (255, 0, 255))
                text_x = 100
                text_y = 300
                self.screen.blit(text, (text_x, text_y))
            elif self.victories == 1:
                font = pygame.font.Font(None, 100)
                text = font.render("Победа", 1, (0, 0, 255))
                text_x = 120
                text_y = 200
                self.screen.blit(text, (text_x, text_y))
                font = pygame.font.Font(None, 30)
                text = font.render("Нажмите, чтобы продолжить", 1, (0, 0, 255))
                text_x = 100
                text_y = 300
                self.screen.blit(text, (text_x, text_y))
            elif self.victories == 2:
                font = pygame.font.Font(None, 70)
                text = font.render("Поражение", 1, (255, 0, 0))
                text_x = 110
                text_y = 200
                self.screen.blit(text, (text_x, text_y))
                font = pygame.font.Font(None, 30)
                text = font.render("Нажмите, чтобы продолжить", 1, (255, 0, 0))
                text_x = 100
                text_y = 300
                self.screen.blit(text, (text_x, text_y))

    def get_cell(self, mouse_pos):
        upper_limit = self.top
        lower_limit = self.top + self.cell_size
        for i in range(self.height):
            right_limit = self.left + self.cell_size
            lef_limit = self.left
            for j in range(self.width):
                if (mouse_pos[0] >= lef_limit) and (mouse_pos[0] <= right_limit) and \
                        (mouse_pos[1] >= upper_limit) and (mouse_pos[1] <= lower_limit):
                    return (j, i)
                else:
                    lef_limit = right_limit
                    right_limit = right_limit + self.cell_size
            upper_limit = lower_limit
            lower_limit = lower_limit + self.cell_size
        return None

    def on_click(self, cell):
        if cell != None:
            if self.plaer == 1:
                if self.board[cell[1]][cell[0]] == 0:
                    self.board[cell[1]][cell[0]] = 1
                    self.plaer = 2
            elif self.plaer == 0:
                self.begin()

    def check(self):
        if ((self.board[0][0] == 1) and (self.board[1][0] == 1) and (self.board[2][0] == 1)) or \
                ((self.board[0][1] == 1) and (self.board[1][1] == 1) and (self.board[2][1] == 1)) or \
                ((self.board[0][2] == 1) and (self.board[1][2] == 1) and (self.board[2][2] == 1)) or \
                ((self.board[0][0] == 1) and (self.board[0][1] == 1) and (self.board[0][2] == 1)) or \
                ((self.board[1][0] == 1) and (self.board[1][1] == 1) and (self.board[1][2] == 1)) or \
                ((self.board[2][0] == 1) and (self.board[2][1] == 1) and (self.board[2][2] == 1)) or \
                ((self.board[0][0] == 1) and (self.board[1][1] == 1) and (self.board[2][2] == 1)) or \
                ((self.board[0][2] == 1) and (self.board[1][1] == 1) and (self.board[2][0] == 1)):
            self.plaer = 0
            self.victories = 1
        elif ((self.board[0][0] == 2) and (self.board[1][0] == 2) and (self.board[2][0] == 2)) or \
                ((self.board[0][1] == 2) and (self.board[1][1] == 2) and (self.board[2][1] == 2)) or \
                ((self.board[0][2] == 2) and (self.board[1][2] == 2) and (self.board[2][2] == 2)) or \
                ((self.board[0][0] == 2) and (self.board[0][1] == 2) and (self.board[0][2] == 2)) or \
                ((self.board[1][0] == 2) and (self.board[1][1] == 2) and (self.board[1][2] == 2)) or \
                ((self.board[2][0] == 2) and (self.board[2][1] == 2) and (self.board[2][2] == 2)) or \
                ((self.board[0][0] == 2) and (self.board[1][1] == 2) and (self.board[2][2] == 2)) or \
                ((self.board[0][2] == 2) and (self.board[1][1] == 2) and (self.board[2][0] == 2)):
            self.plaer = 0
            self.victories = 2
        else:
            if (self.board[0][0] != 0) and (self.board[1][0] != 0) and (self.board[2][0] != 0) and \
                    (self.board[0][1] != 0) and (self.board[1][1] != 0) and (self.board[2][1] != 0) and \
                    (self.board[0][2] != 0) and (self.board[1][2] != 0) and (self.board[2][2] != 0):
                self.plaer = 0
        if self.plaer == 2:
            self.enemy()

    def enemy(self):
        if self.plaer == 2:
            if (self.board[0][0] == 2) and (self.board[0][1] == 2) \
                    and (self.board[0][2] == 0):
                self.board[0][2] = 2
            elif (self.board[0][0] == 2) and (self.board[0][2] == 2) \
                    and (self.board[0][1] == 0):
                self.board[0][1] = 2
            elif (self.board[0][2] == 2) and (self.board[0][1] == 2) \
                    and (self.board[0][0] == 0):
                self.board[0][0] = 2
                #
            elif (self.board[1][0] == 2) and (self.board[1][1] == 2) \
                    and (self.board[1][2] == 0):
                self.board[1][2] = 2
            elif (self.board[1][2] == 2) and (self.board[1][1] == 2) \
                    and (self.board[1][0] == 0):
                self.board[1][0] = 2
            elif (self.board[1][0] == 2) and (self.board[1][2] == 2) \
                    and (self.board[1][1] == 0):
                self.board[1][1] = 2
                #
            elif (self.board[2][0] == 2) and (self.board[2][1] == 2) \
                    and (self.board[2][2] == 0):
                self.board[2][2] = 2
            elif (self.board[2][2] == 2) and (self.board[2][1] == 2) \
                    and (self.board[2][0] == 0):
                self.board[2][0] = 2
            elif (self.board[2][0] == 2) and (self.board[2][2] == 2) \
                    and (self.board[2][1] == 0):
                self.board[2][1] = 2
                #
            elif (self.board[0][0] == 2) and (self.board[1][0] == 2) \
                    and (self.board[2][0] == 0):
                self.board[2][0] = 2
            elif (self.board[0][0] == 2) and (self.board[2][0] == 2) \
                    and (self.board[1][0] == 0):
                self.board[1][0] = 2
            elif (self.board[1][0] == 2) and (self.board[2][0] == 2) \
                    and (self.board[0][0] == 0):
                self.board[0][0] = 2
                #
            elif (self.board[0][1] == 2) and (self.board[1][1] == 2) \
                    and (self.board[2][1] == 0):
                self.board[2][1] = 2
            elif (self.board[0][1] == 2) and (self.board[2][1] == 2) \
                    and (self.board[1][1] == 0):
                self.board[1][1] = 2
            elif (self.board[1][1] == 2) and (self.board[2][1] == 2) \
                    and (self.board[0][1] == 0):
                self.board[0][1] = 2
                #
            elif (self.board[0][2] == 2) and (self.board[1][2] == 2) \
                    and (self.board[2][2] == 0):
                self.board[2][2] = 2
            elif (self.board[0][2] == 2) and (self.board[2][2] == 2) \
                    and (self.board[1][2] == 0):
                self.board[1][2] = 2
            elif (self.board[1][2] == 2) and (self.board[2][2] == 2) \
                    and (self.board[0][2] == 0):
                self.board[0][2] = 2
                #
            elif (self.board[0][0] == 2) and (self.board[1][1] == 2) \
                    and (self.board[2][2] == 0):
                self.board[2][2] = 2
            elif (self.board[0][0] == 2) and (self.board[2][2] == 2) \
                    and (self.board[1][1] == 0):
                self.board[1][1] = 2
            elif (self.board[1][1] == 2) and (self.board[2][2] == 2) \
                    and (self.board[0][0] == 0):
                self.board[0][0] = 2
                #
            elif (self.board[0][2] == 2) and (self.board[1][1] == 2) \
                    and (self.board[2][0] == 0):
                self.board[2][0] = 2
            elif (self.board[2][0] == 2) and (self.board[1][1] == 2) \
                    and (self.board[0][2] == 0):
                self.board[0][2] = 2
            elif (self.board[2][0] == 2) and (self.board[0][2] == 2) \
                    and (self.board[1][1] == 0):
                self.board[1][1] = 2
            else:
                if (self.board[0][0] == 1) and (self.board[0][1] == 1) \
                        and (self.board[0][2] == 0):
                    self.board[0][2] = 2
                elif (self.board[0][0] == 1) and (self.board[0][2] == 1) \
                        and (self.board[0][1] == 0):
                    self.board[0][1] = 2
                elif (self.board[0][2] == 1) and (self.board[0][1] == 1) \
                        and (self.board[0][0] == 0):
                    self.board[0][0] = 2
                    #
                elif (self.board[1][0] == 1) and (self.board[1][1] == 1) \
                        and (self.board[1][2] == 0):
                    self.board[1][2] = 2
                elif (self.board[1][2] == 1) and (self.board[1][1] == 1) \
                        and (self.board[1][0] == 0):
                    self.board[1][0] = 2
                elif (self.board[1][0] == 1) and (self.board[1][2] == 1) \
                        and (self.board[1][1] == 0):
                    self.board[1][1] = 2
                    #
                elif (self.board[2][0] == 1) and (self.board[2][1] == 1) \
                        and (self.board[2][2] == 0):
                    self.board[2][2] = 2
                elif (self.board[2][2] == 1) and (self.board[2][1] == 1) \
                        and (self.board[2][0] == 0):
                    self.board[2][0] = 2
                elif (self.board[2][0] == 1) and (self.board[2][2] == 1) \
                        and (self.board[2][1] == 0):
                    self.board[2][1] = 2
                    #
                elif (self.board[0][0] == 1) and (self.board[1][0] == 1) \
                        and (self.board[2][0] == 0):
                    self.board[2][0] = 2
                elif (self.board[0][0] == 1) and (self.board[2][0] == 1) \
                        and (self.board[1][0] == 0):
                    self.board[1][0] = 2
                elif (self.board[1][0] == 1) and (self.board[2][0] == 1) \
                        and (self.board[0][0] == 0):
                    self.board[0][0] = 2
                    #
                elif (self.board[0][1] == 1) and (self.board[1][1] == 1) \
                        and (self.board[2][1] == 0):
                    self.board[2][1] = 2
                elif (self.board[0][1] == 1) and (self.board[2][1] == 1) \
                        and (self.board[1][1] == 0):
                    self.board[1][1] = 2
                elif (self.board[1][1] == 1) and (self.board[2][1] == 1) \
                        and (self.board[0][1] == 0):
                    self.board[0][1] = 2
                    #
                elif (self.board[0][2] == 1) and (self.board[1][2] == 1) \
                        and (self.board[2][2] == 0):
                    self.board[2][2] = 2
                elif (self.board[0][2] == 1) and (self.board[2][2] == 1) \
                        and (self.board[1][2] == 0):
                    self.board[1][2] = 2
                elif (self.board[1][2] == 1) and (self.board[2][2] == 1) \
                        and (self.board[0][2] == 0):
                    self.board[0][2] = 2
                    #
                elif (self.board[0][0] == 1) and (self.board[1][1] == 1) \
                        and (self.board[2][2] == 0):
                    self.board[2][2] = 2
                elif (self.board[0][0] == 1) and (self.board[2][2] == 1) \
                        and (self.board[1][1] == 0):
                    self.board[1][1] = 2
                elif (self.board[1][1] == 1) and (self.board[2][2] == 1) \
                        and (self.board[0][0] == 0):
                    self.board[0][0] = 2
                    #
                elif (self.board[0][2] == 1) and (self.board[1][1] == 1) \
                        and (self.board[2][0] == 0):
                    self.board[2][0] = 2
                elif (self.board[2][0] == 1) and (self.board[1][1] == 1) \
                        and (self.board[0][2] == 0):
                    self.board[0][2] = 2
                elif (self.board[2][0] == 1) and (self.board[0][2] == 1) \
                        and (self.board[1][1] == 0):
                    self.board[1][1] = 2
                else:
                    if self.board[1][1] == 0:
                        self.board[1][1] = 2
                    else:
                        variants = []
                        if self.board[0][0] == 0:
                            variants.append((0, 0))
                        if self.board[0][1] == 0:
                            variants.append((0, 1))
                        if self.board[0][2] == 0:
                            variants.append((0, 2))
                        if self.board[1][0] == 0:
                            variants.append((1, 0))
                        if self.board[1][1] == 0:
                            variants.append((1, 1))
                        if self.board[1][2] == 0:
                            variants.append((1, 2))
                        if self.board[2][0] == 0:
                            variants.append((2, 0))
                        if self.board[2][1] == 0:
                            variants.append((2, 1))
                        if self.board[2][2] == 0:
                            variants.append((2, 2))
                        if len(variants) > 0:
                            r = random.choice(variants)
                            self.board[r[0]][r[1]] = 2
            self.plaer = 1

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


class Board_Tag:
    def __init__(self, width, height, screen):
        self.play = False
        self.victory = False
        self.screen = screen
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        for i in range(self.width):
            for j in range(self.height):
                self.board[i][j] = j + i * 4
        self.left = 50
        self.top = 50
        self.cell_size = 100

    def begin(self):
        a = 0
        self.victory = False
        self.numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        random.shuffle(self.numbers)
        q = 0
        k = 1 + self.numbers.index(15) // 4
        for i in range(16):
            if self.numbers[i] != 15:
                for j in range(i):
                    if self.numbers[j] != 15:
                        if self.numbers[i] < self.numbers[j]:
                            q += 1
        if (q + k) % 2 == 1:
            self.begin()
        else:
            for i in range(self.width):
                for j in range(self.height):
                    self.board[i][j] = self.numbers[a]
                    a += 1

    def render(self):
        a = 0
        for i in range(self.height):
            b = 0
            for i in range(self.width):
                self.screen.blit(load_image("picture" + str(self.board[a][b]) + ".png"),
                                 (self.left + b * self.cell_size, self.top + a * self.cell_size))
                b += 1
            a += 1
        if self.victory:
            font = pygame.font.Font(None, 100)
            text = font.render("Победа", 1, (255, 0, 255))
            text_x = 110
            text_y = 200
            self.screen.blit(text, (text_x, text_y))
            font = pygame.font.Font(None, 30)
            text = font.render("Нажмите, чтобы заново", 1, (255, 0, 255))
            text_x = 120
            text_y = 300
            self.screen.blit(text, (text_x, text_y))

    def check(self):
        if self.play:
            a = 0
            for i in range(self.width):
                for j in range(self.height):
                    if self.board[i][j] == j + i * 4:
                        a += 1
            if a == self.width * self.height:
                print("Victory")
                self.play = False
                self.victory = True

    def get_cell(self, mouse_pos):
        upper_limit = self.top
        lower_limit = self.top + self.cell_size
        for i in range(self.height):
            right_limit = self.left + self.cell_size
            lef_limit = self.left
            for j in range(self.width):
                if (mouse_pos[0] >= lef_limit) and (mouse_pos[0] <= right_limit) and \
                        (mouse_pos[1] >= upper_limit) and (mouse_pos[1] <= lower_limit):
                    return (j, i)
                else:
                    lef_limit = right_limit
                    right_limit = right_limit + self.cell_size
            upper_limit = lower_limit
            lower_limit = lower_limit + self.cell_size
        return None

    def on_click(self, cell):
        if cell != None:
            if not self.play:
                self.play = True
                self.begin()
            else:
                if self.board[cell[1]][cell[0]] != 15:
                    if cell == (0, 0):
                        if self.board[0][1] == 15:
                          self.board[0][0], self.board[0][1] = self.board[0][1], self.board[0][0]
                        elif self.board[1][0] == 15:
                          self.board[0][0], self.board[1][0] = self.board[1][0], self.board[0][0]
                    elif cell == (3, 0):
                        if self.board[0][2] == 15:
                          self.board[0][3], self.board[0][2] = self.board[0][2], self.board[0][3]
                        elif self.board[1][3] == 15:
                          self.board[0][3], self.board[1][3] = self.board[1][3], self.board[0][3]
                    elif cell == (0, 3):
                        if self.board[2][0] == 15:
                            self.board[3][0], self.board[2][0] = self.board[2][0], self.board[3][0]
                        elif self.board[3][1] == 15:
                            self.board[3][0], self.board[3][1] = self.board[3][1], self.board[3][0]
                    elif cell == (3, 3):
                        if self.board[3][2] == 15:
                            self.board[3][3], self.board[3][2] = self.board[3][2], self.board[3][3]
                        elif self.board[2][3] == 15:
                            self.board[3][3], self.board[2][3] = self.board[2][3], self.board[3][3]
                            #
                    elif cell == (1, 0):
                        if self.board[0][0] == 15:
                          self.board[0][0], self.board[0][1] = self.board[0][1], self.board[0][0]
                        elif self.board[1][1] == 15:
                          self.board[0][1], self.board[1][1] = self.board[1][1], self.board[0][1]
                        elif self.board[0][2] == 15:
                          self.board[0][1], self.board[0][2] = self.board[0][2], self.board[0][1]
                    elif cell == (2, 0):
                        if self.board[0][3] == 15:
                          self.board[0][3], self.board[0][2] = self.board[0][2], self.board[0][3]
                        elif self.board[1][2] == 15:
                          self.board[0][2], self.board[1][2] = self.board[1][2], self.board[0][2]
                        elif self.board[0][1] == 15:
                          self.board[0][1], self.board[0][2] = self.board[0][2], self.board[0][1]
                    elif cell == (1, 3):
                        if self.board[3][0] == 15:
                          self.board[3][0], self.board[3][1] = self.board[3][1], self.board[3][0]
                        elif self.board[2][1] == 15:
                          self.board[3][1], self.board[2][1] = self.board[2][1], self.board[3][1]
                        elif self.board[3][2] == 15:
                          self.board[3][1], self.board[3][2] = self.board[3][2], self.board[3][1]
                    elif cell == (2, 3):
                        if self.board[3][3] == 15:
                          self.board[3][3], self.board[3][2] = self.board[3][2], self.board[3][3]
                        elif self.board[2][2] == 15:
                          self.board[3][2], self.board[2][2] = self.board[2][2], self.board[3][2]
                        elif self.board[3][1] == 15:
                          self.board[3][1], self.board[3][2] = self.board[3][2], self.board[3][1]
                            #
                    elif cell == (0, 1):
                        if self.board[0][0] == 15:
                          self.board[0][0], self.board[1][0] = self.board[1][0], self.board[0][0]
                        elif self.board[1][1] == 15:
                          self.board[1][0], self.board[1][1] = self.board[1][1], self.board[1][0]
                        elif self.board[2][0] == 15:
                          self.board[1][0], self.board[2][0] = self.board[2][0], self.board[1][0]
                    elif cell == (0, 2):
                        if self.board[1][0] == 15:
                          self.board[1][0], self.board[2][0] = self.board[2][0], self.board[1][0]
                        elif self.board[2][1] == 15:
                          self.board[2][0], self.board[2][1] = self.board[2][1], self.board[2][0]
                        elif self.board[3][0] == 15:
                          self.board[3][0], self.board[2][0] = self.board[2][0], self.board[3][0]
                    elif cell == (3, 2):
                        if self.board[3][3] == 15:
                          self.board[3][3], self.board[2][3] = self.board[2][3], self.board[3][3]
                        elif self.board[2][2] == 15:
                          self.board[2][3], self.board[2][2] = self.board[2][2], self.board[2][3]
                        elif self.board[1][3] == 15:
                          self.board[1][3], self.board[2][3] = self.board[2][3], self.board[1][3]
                    elif cell == (3, 1):
                        if self.board[0][3] == 15:
                          self.board[0][3], self.board[1][3] = self.board[1][3], self.board[0][3]
                        elif self.board[1][2] == 15:
                          self.board[1][3], self.board[1][2] = self.board[1][2], self.board[1][3]
                        elif self.board[2][3] == 15:
                          self.board[1][3], self.board[2][3] = self.board[2][3], self.board[1][3]
                            #
                    elif cell == (1, 1):
                        if self.board[0][1] == 15:
                          self.board[0][1], self.board[1][1] = self.board[1][1], self.board[0][1]
                        elif self.board[1][2] == 15:
                          self.board[1][1], self.board[1][2] = self.board[1][2], self.board[1][1]
                        elif self.board[2][1] == 15:
                          self.board[1][1], self.board[2][1] = self.board[2][1], self.board[1][1]
                        elif self.board[1][0] == 15:
                          self.board[1][1], self.board[1][0] = self.board[1][0], self.board[1][1]
                    elif cell == (2, 1):
                        if self.board[0][2] == 15:
                          self.board[0][2], self.board[1][2] = self.board[1][2], self.board[0][2]
                        elif self.board[1][1] == 15:
                          self.board[1][1], self.board[1][2] = self.board[1][2], self.board[1][1]
                        elif self.board[2][2] == 15:
                          self.board[1][2], self.board[2][2] = self.board[2][2], self.board[1][2]
                        elif self.board[1][3] == 15:
                          self.board[1][2], self.board[1][3] = self.board[1][3], self.board[1][2]
                    elif cell == (1, 2):
                        if self.board[1][1] == 15:
                          self.board[1][1], self.board[2][1] = self.board[2][1], self.board[1][1]
                        elif self.board[2][2] == 15:
                          self.board[2][1], self.board[2][2] = self.board[2][2], self.board[2][1]
                        elif self.board[3][1] == 15:
                          self.board[2][1], self.board[3][1] = self.board[3][1], self.board[2][1]
                        elif self.board[2][0] == 15:
                          self.board[2][1], self.board[2][0] = self.board[2][0], self.board[2][1]
                    elif cell == (2, 2):
                        if self.board[1][2] == 15:
                          self.board[1][2], self.board[2][2] = self.board[2][2], self.board[1][2]
                        elif self.board[2][3] == 15:
                          self.board[2][2], self.board[2][3] = self.board[2][3], self.board[2][2]
                        elif self.board[3][2] == 15:
                          self.board[2][2], self.board[3][2] = self.board[3][2], self.board[2][2]
                        elif self.board[2][1] == 15:
                          self.board[2][1], self.board[2][2] = self.board[2][2], self.board[2][1]

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


app = QApplication(sys.argv)
ex = MainWindow()
sys.exit(app.exec_())
