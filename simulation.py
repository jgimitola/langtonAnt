import os

import pygame


def simulate(n, N, preferredSize):
    # Definimos la clase Cell para representar cada bloque de la grilla.
    class Cell:
        x = 0
        y = 0
        side = 0
        color = (0, 0, 0)

        def __init__(self, x, y, s):
            self.x = x
            self.y = y
            self.side = s

        def paint(self):
            pygame.draw.rect(screen, self.color, [self.x, self.y, self.side, self.side])

        def updateCell(self):
            if self.color == (0, 0, 0):
                self.color = (255, 255, 255)
            else:
                self.color = (0, 0, 0)

        def isBlack(self):
            if self.color == (0, 0, 0):
                return True

    # Definimos la clase Ant para representar a la hormiga y sus funciones.
    class Ant:
        x = 0
        y = 0
        facing = "UP"

        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.ant = pygame.image.load('images/ant_player.png')
            self.ant = pygame.transform.scale(self.ant, (BLOCK_SIZE, BLOCK_SIZE))

        def getFacing(self):
            return self.facing

        def move2(self, x, y):
            self.x = x
            self.y = y

        def nextPos(self, isBlack):
            x = self.x
            y = self.y
            if isBlack:
                if self.facing == "UP":
                    x = self.x - 1
                elif self.facing == "DOWN":
                    x = self.x + 1
                elif self.facing == "LEFT":
                    y = self.y + 1
                elif self.facing == "RIGHT":
                    y = self.y - 1
            else:
                if self.facing == "UP":
                    x = self.x + 1
                elif self.facing == "DOWN":
                    x = self.x - 1
                elif self.facing == "LEFT":
                    y = self.y - 1
                elif self.facing == "RIGHT":
                    y = self.y + 1
            return x, y

        def move(self, isBlack):
            if isBlack:
                if self.facing == "UP":
                    self.x -= 1
                elif self.facing == "DOWN":
                    self.x += 1
                elif self.facing == "LEFT":
                    self.y += 1
                elif self.facing == "RIGHT":
                    self.y -= 1
                self.rotate(90)
            else:
                if self.facing == "UP":
                    self.x += 1
                elif self.facing == "DOWN":
                    self.x -= 1
                elif self.facing == "LEFT":
                    self.y -= 1
                elif self.facing == "RIGHT":
                    self.y += 1
                self.rotate(-90)

        def paint(self):
            screen.blit(self.ant,
                        (self.x * (BLOCK_SIZE + SPACING) + CENTERING, self.y * (BLOCK_SIZE + SPACING) + CENTERING))

        def rotate(self, angle):
            self.ant = pygame.transform.rotate(self.ant, angle)
            if angle == 90:
                if self.facing == "UP":
                    self.facing = "LEFT"
                elif self.facing == "DOWN":
                    self.facing = "RIGHT"
                elif self.facing == "LEFT":
                    self.facing = "DOWN"
                elif self.facing == "RIGHT":
                    self.facing = "UP"
            else:
                if self.facing == "UP":
                    self.facing = "RIGHT"
                elif self.facing == "DOWN":
                    self.facing = "LEFT"
                elif self.facing == "LEFT":
                    self.facing = "UP"
                elif self.facing == "RIGHT":
                    self.facing = "DOWN"

        def getPos(self):
            return self.x, self.y

    # Definimos que centraremos la pantalla.
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Iniciamos pygame.
    pygame.init()

    # Damos el tamaño de pantalla, titulo e icono.
    screen = pygame.display.set_mode((preferredSize, preferredSize))
    pygame.display.set_caption("Langton's Ant")
    icon = pygame.image.load('images/ant.png')
    pygame.display.set_icon(icon)

    # Argumentos de simulación.
    SPACING = 2
    BLOCK_SIZE = preferredSize // n - SPACING
    CENTERING = (preferredSize - n * (BLOCK_SIZE + SPACING)) // 2

    # Por defecto posicionamos en el centro de la grilla.
    ant = Ant(n // 2, n // 2)

    # Creamos la grilla.
    grid = []
    for j in range(n):
        row = []
        for i in range(n):
            row.append(Cell(i * (BLOCK_SIZE + SPACING) + CENTERING, j * (BLOCK_SIZE + SPACING) + CENTERING, BLOCK_SIZE))
        grid.append(row)

    def paintGrid(grid):
        for j in range(n):
            row = grid[j]
            for i in range(n):
                row[i].paint()

    # Escogemos la posición inicial y orientación.
    clock = pygame.time.Clock()
    choosen = False
    while not choosen:
        pos = pygame.mouse.get_pos()
        posI = ((pos[0] - CENTERING) // (BLOCK_SIZE + SPACING))
        posJ = ((pos[1] - CENTERING) // (BLOCK_SIZE + SPACING))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 0 <= posI < n and 0 <= posJ < n:
                    if event.button == 1:
                        ant.move2(posI, posJ)
                        choosen = True
                    elif event.button == 4:
                        ant.rotate(-90)
                    elif event.button == 5:
                        ant.rotate(90)

        screen.fill((160, 160, 160))

        paintGrid(grid)

        if 0 <= posI < n and 0 <= posJ < n:
            ant.move2(posI, posJ)
            ant.paint()

        clock.tick(30)
        pygame.display.update()

    # Iniciamos la simulación.
    cont = 0
    state = "SHOW"
    font = pygame.font.Font('fonts/Roboto-Medium.ttf', 16)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        screen.fill((160, 160, 160))
        paintGrid(grid)

        # Actualizamos celda y hormiga.
        if cont < N:
            if state != "SHOW":
                antPos = ant.getPos()
                cell = grid[antPos[1]][antPos[0]]
                nextMove = ant.nextPos(cell.isBlack())
                if 0 <= nextMove[0] <= n and 0 <= nextMove[1] <= n:
                    ant.move(cell.isBlack())
                    cell.updateCell()
                    cont += 1
                else:
                    cont = N
                state = "SHOW"
            else:
                state = "RUNNING"
        ant.paint()

        # Actualizamos texto.
        screen.blit(font.render('Facing: ' + ant.getFacing(), True, (0, 255, 26)), (0, 0))
        screen.blit(font.render('N: ' + str(cont), True, (0, 255, 26)), (0, 20))

        clock.tick(25)
        pygame.display.update()
