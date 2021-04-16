from queue import PriorityQueue
from Algorithms.Reconstruct_Path import Reconstruct_Path
import pygame
# Using Heap
# G = (V, E)
# Time = O(ElogV)


def Dijkstra(Draw, Grid, Start, End):
    Time_Inserted = 0
    Visited = {Start}
    Distances = {node: float("inf") for row in Grid for node in row}
    Distances[Start] = 0
    Q = PriorityQueue()
    Q.put((Distances[Start], Time_Inserted, Start))
    while not Q.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
        currentNode = Q.get()[2]
        currentNode.updateNeighbors(Grid)

        # Found the path, so trace back the path
        if currentNode == End:
            Reconstruct_Path(Draw, currentNode, End)
            return True

        temp_Distance = Distances[currentNode] + 1
        for neighbor in currentNode.neighbors:
            if neighbor not in Visited:
                # Relax
                if temp_Distance < Distances[neighbor]:
                    Time_Inserted += 1
                    neighbor.comefrom = currentNode
                    Distances[neighbor] = temp_Distance
                    neighbor.makeOpenSet()
                    Visited.add(neighbor)
                    Q.put((Distances[neighbor], Time_Inserted, neighbor))
        Draw()
        if currentNode != Start:
            currentNode.makeClosedSet()
