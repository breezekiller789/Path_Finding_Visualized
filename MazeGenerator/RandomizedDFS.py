import random
import pygame


def MakeGridAllWalls(Grid):
    for row in Grid:
        for node in row:
            node.makeWall()


def RandomizedDFS(Draw, Grid):
    Rows = len(Grid[0])
    lists = [num for num in range(1, Rows-1)]
    MakeGridAllWalls(Grid)
    Start = Grid[random.choice(lists)][random.choice(lists)]
    End = Grid[random.choice(lists)][random.choice(lists)]
    Start.makeStart()
    End.makeEnd()
    count = 0
    Walls = (Rows**2) * 3 // 5
    while count < Walls:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        currentNode = Grid[random.choice(lists)][random.choice(lists)]
        if currentNode.isWall() and not currentNode.isStart() and \
                not currentNode.isEnd():
            currentNode.Reset()
            count += 1
    Draw()
    return Start, End
