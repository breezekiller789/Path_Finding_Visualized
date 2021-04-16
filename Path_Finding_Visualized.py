import pygame
import Colors
# from Algorithms import Astar
from Algorithms.BFS import BFS
from Algorithms.DFS import DFS
from Algorithms.Astar import Astar
pygame.init()

WIDTH = 800
screen = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")


class Node(object):

    def __init__(self, row, col, Gap, total_rows):
        self.row = row
        self.col = col
        self.x_start = col*Gap
        self.y_start = row*Gap
        self.width = Gap
        self.color = Colors.WHITE
        self.neighbors = []
        self.total_rows = total_rows
        self.comefrom = None

    def Position(self):
        return self.row, self.col

    def isWall(self):
        return self.color == Colors.BLACK

    def isStart(self):
        return self.color == Colors.ORANGE

    def isEnd(self):
        return self.color == Colors.RED

    def Reset(self):
        self.color = Colors.WHITE

    def makeStart(self):
        self.color = Colors.ORANGE

    def makeEnd(self):
        self.color = Colors.RED

    def makeWall(self):
        self.color = Colors.BLACK

    def makeOpenSet(self):
        self.color = Colors.GREEN

    def makeClosedSet(self):
        self.color = Colors.TIFFANY

    def makePath(self):
        self.color = Colors.PURPLE

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            (self.x_start, self.y_start, self.width, self.width)
        )

    def updateNeighbors(self, Grid):
        # Up
        if self.row >= 1 and not Grid[self.row-1][self.col].isWall():
            self.neighbors.append(Grid[self.row-1][self.col])
        # Right
        if self.col < self.total_rows-1 and \
                not Grid[self.row][self.col+1].isWall():
            self.neighbors.append(Grid[self.row][self.col+1])
        # Down
        if self.row < self.total_rows-1 and \
                not Grid[self.row+1][self.col].isWall():
            self.neighbors.append(Grid[self.row+1][self.col])
        # Left
        if self.col >= 1 and not Grid[self.row][self.col-1].isWall():
            self.neighbors.append(Grid[self.row][self.col-1])

    def __lt__(self, other):
        return False


def MakeGrid(Rows, width):
    Gap = width // Rows
    Grid = []
    for i in range(Rows):
        Grid.append([])
        for j in range(Rows):
            node = Node(i, j, Gap, Rows)
            # Set boundry, don't let the algorithm to go out of boundry
            if i == 0 or i == Rows-1 or j == 0 or j == Rows-1:
                node.makeWall()
            Grid[i].append(node)
    return Grid


def MakeScreenGrid(screen, Rows, width):
    Gap = width // Rows
    for i in range(Rows):
        pygame.draw.line(screen, Colors.GREY, (0, i*Gap), (width, i*Gap), 1)
    for i in range(Rows):
        pygame.draw.line(screen, Colors.GREY, (i*Gap, 0), (i*Gap, width), 1)


def Draw(screen, Grid, ROW, width):
    screen.fill(Colors.WHITE)
    for row in Grid:
        for node in row:
            node.draw(screen)
    MakeScreenGrid(screen, ROW, width)
    pygame.display.update()


def MouseClickPosition_To_Grid_Position(mousePosition, ROW, width):
    Gap = width // ROW
    x, y = mousePosition
    row = y // Gap
    col = x // Gap
    return row, col


def ClearBoard(Grid):
    for row in Grid:
        for node in row:
            node.Reset()


def Left_Clicked_Add_Wall(Grid, Start, End, ROW, width):
    mousePosition = pygame.mouse.get_pos()
    row, col = MouseClickPosition_To_Grid_Position(mousePosition, ROW, width)
    nodeClicked = Grid[row][col]
    if not Start:
        Start = nodeClicked
        nodeClicked.makeStart()
    # Don't let End to override Start, so added the AND statement
    elif not End and nodeClicked != Start:
        End = nodeClicked
        nodeClicked.makeEnd()
    elif nodeClicked != Start and nodeClicked != End:
        nodeClicked.makeWall()
    return Start, End


def Right_Clicked_Erase(Grid, Start, End, ROW, width):
    mousePosition = pygame.mouse.get_pos()
    row, col = MouseClickPosition_To_Grid_Position(mousePosition, ROW, width)
    nodeClicked = Grid[row][col]
    nodeClicked.Reset()
    if nodeClicked == Start:
        Start = None
    elif nodeClicked == End:
        End = None
    return Start, End


def main():
    ROW = 50
    Grid = MakeGrid(ROW, WIDTH)
    run = True
    Start = None
    End = None
    while run:
        Draw(screen, Grid, ROW, WIDTH)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.KEYDOWN:
                # Press key c to clean the board
                if event.key == pygame.K_c:
                    ClearBoard(Grid)
                    Start = None
                    End = None
                    Grid = MakeGrid(ROW, WIDTH)

                # Press key b to visualize BFS algorithm
                elif event.key == pygame.K_b:
                    BFS(
                        lambda: Draw(screen, Grid, ROW, WIDTH),
                        Grid,
                        Start,
                        End
                    )

                # Press key d to visualize DFS algorithm
                elif event.key == pygame.K_d:
                    DFS(
                        lambda: Draw(screen, Grid, ROW, WIDTH),
                        Grid,
                        Start,
                        End
                    )

                # Press key a to visualize A* algorithm
                elif event.key == pygame.K_a:
                    Astar(
                        lambda: Draw(screen, Grid, ROW, WIDTH),
                        Grid,
                        Start,
                        End
                    )

            # Left click to add wall
            if pygame.mouse.get_pressed()[0]:
                Start, End = Left_Clicked_Add_Wall(Grid, Start, End, ROW, WIDTH)

            # Right click to reset node
            elif pygame.mouse.get_pressed()[2]:
                Start, End = Right_Clicked_Erase(Grid, Start, End, ROW, WIDTH)


if __name__ == "__main__":
    main()
