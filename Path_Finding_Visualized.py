import pygame
import Colors
# import time
from Algorithms.BFS import BFS
from Algorithms.DFS import DFS
from Algorithms.Astar import Astar
from Algorithms.Dijkstra import Dijkstra
from Algorithms.Fibanocci_Heap_Dijkstra import Fibanocci_Heap_Dijkstra
from MazeGenerator.RandomizedDFS import RandomizedDFS
pygame.init()

WIDTH = 1000
screen = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path Finding Algorithm Visualized")


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
        self.neighbors = []
        self.comefrom = None

    def makeStart(self):
        self.color = Colors.YELLOW

    def makeEnd(self):
        self.color = Colors.RED

    def makeWall(self):
        self.color = Colors.BLACK

    def makeWeightedWall(self):
        self.color = Colors.CONCRETE

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


def ResetBoard_Leave_Walls_Start_End(Grid, Start):
    for row in Grid:
        for node in row:
            if not node.isWall() and not node.isStart() and not node.isEnd():
                node.Reset()

    # Added this because Start node's neighbors will not be updated properly, it
    # will keep on appending to the neighbors list and cause issues when user
    # want to add walls arround Start node
    Start.Reset()
    Start.makeStart()


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
    if nodeClicked == Start:
        Start.Reset()
        Start = None
    elif nodeClicked == End:
        End.Reset()
        End = None
    else:
        nodeClicked.Reset()
    return Start, End


def Add_Weighted_Wall(Grid, Start, End, ROW, width):
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
        nodeClicked.makeWeightedWall()
    return Start, End


def Keydown_Events(event, ROW, width, Grid, Start, End, screen):

    # Press key c to clean the board
    if event.key == pygame.K_c:
        ClearBoard(Grid)
        Start = None
        End = None
        Grid = MakeGrid(ROW, width)

    # Press key r to clean board but leave walls, start, end nodes
    elif event.key == pygame.K_r:
        ResetBoard_Leave_Walls_Start_End(Grid, Start)

    # Press key b to visualize BFS algorithm
    elif event.key == pygame.K_b:
        ResetBoard_Leave_Walls_Start_End(Grid, Start)
        BFS(
            lambda: Draw(screen, Grid, ROW, width),
            Grid,
            Start,
            End
        )

    # Press key d to visualize DFS algorithm
    elif event.key == pygame.K_d:
        ResetBoard_Leave_Walls_Start_End(Grid, Start)
        DFS(
            lambda: Draw(screen, Grid, ROW, width),
            Grid,
            Start,
            End
        )

    # Press key a to visualize A* algorithm
    elif event.key == pygame.K_a:
        ResetBoard_Leave_Walls_Start_End(Grid, Start)
        Astar(
            lambda: Draw(screen, Grid, ROW, width),
            Grid,
            Start,
            End
        )

    # Press key j to visualize Dijkstra algorithm
    elif event.key == pygame.K_j:
        ResetBoard_Leave_Walls_Start_End(Grid, Start)
        Dijkstra(
            lambda: Draw(screen, Grid, ROW, width),
            Grid,
            Start,
            End
        )
    # Press key f to visualize Fibonacci Heap Dijkstra algorithm
    elif event.key == pygame.K_f:
        ResetBoard_Leave_Walls_Start_End(Grid, Start)
        Fibanocci_Heap_Dijkstra(
            lambda: Draw(screen, Grid, ROW, width),
            Grid,
            Start,
            End
        )

    # Press w to add weighted wall
    elif event.key == pygame.K_w:
        Start, End = Add_Weighted_Wall(Grid, Start, End, ROW, width)

    elif event.key == pygame.K_g:
        Start, End = RandomizedDFS(lambda: Draw(screen, Grid, ROW, width), Grid)

    return Start, End, Grid


def main():
    ROW = 20    # Modify this to change size
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

                Start, End, Grid = Keydown_Events(
                    event,
                    ROW,
                    WIDTH,
                    Grid,
                    Start,
                    End,
                    screen
                )

            # Left click to add wall
            elif pygame.mouse.get_pressed()[0]:
                Start, End = Left_Clicked_Add_Wall(Grid, Start, End, ROW, WIDTH)

            # Right click to reset node
            elif pygame.mouse.get_pressed()[2]:
                Start, End = Right_Clicked_Erase(Grid, Start, End, ROW, WIDTH)


if __name__ == "__main__":
    main()
