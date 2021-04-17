import queue
import pygame
from Algorithms.Reconstruct_Path import Reconstruct_Path


def BFS(Draw, Grid, Start, End):
    Q = queue.Queue()
    Visited = {Start}
    Q.put(Start)
    while not Q.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
        currentNode = Q.get()
        # Found the path, so trace back the path
        if currentNode == End:
            Reconstruct_Path(Draw, currentNode, Start, End)
            return True

        # Update all the neighbors arround currentNode
        currentNode.updateNeighbors(Grid)

        # Visit all the neighbors
        for neighbor in currentNode.neighbors:
            if neighbor not in Visited:
                neighbor.comefrom = currentNode
                if neighbor != End:
                    neighbor.makeOpenSet()
                Q.put(neighbor)
                Visited.add(neighbor)
        Draw()
        if currentNode != Start:
            currentNode.makeClosedSet()
