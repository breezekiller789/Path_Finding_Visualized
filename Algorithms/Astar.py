from queue import PriorityQueue
import math
import pygame
from Algorithms.Reconstruct_Path import Reconstruct_Path


def Heuristic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return int(math.sqrt(pow(abs(x2-x1), 2) + pow(abs(y2-y1), 2)))


def Astar(Draw, Grid, Start, End):
    # Keep track of the time, if there are two identical f_score,
    # then we check who inserted into openset first
    time_inserted = 0
    openSet = PriorityQueue()
    # (f_score, node), f_score will be consider as key
    openSet.put((0, time_inserted, Start))
    g_Score = {node: float("inf") for row in Grid for node in row}
    f_Score = {node: float("inf") for row in Grid for node in row}
    g_Score[Start] = 0
    f_Score[Start] = Heuristic(Start.Position(), End.Position())
    openSetHash = {Start}

    # Algorithm Starts
    while not openSet.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

        currentNode = openSet.get()[2]  # Extract the node
        currentNode.updateNeighbors(Grid)

        # Found Path
        if currentNode == End:
            Reconstruct_Path(Draw, currentNode, End)
            return

        # Update Neighbors' g, f scores
        tmp_g_Score = g_Score[currentNode] + 1
        for neighbor in currentNode.neighbors:
            # Kinda like Dijkstra's relaxing
            if tmp_g_Score <= g_Score[neighbor]:
                neighbor.comefrom = currentNode
                g_Score[neighbor] = tmp_g_Score
                f_Score[neighbor] = tmp_g_Score + Heuristic(
                    neighbor.Position(), End.Position())
                # Because PriorityQueue won't let us search element in Queues
                # That's why we need openSetHash to check if this node is in
                # Queue
                if neighbor not in openSetHash:
                    time_inserted += 1  # Add time stamp
                    openSetHash.add(neighbor)
                    openSet.put((f_Score[neighbor], time_inserted, neighbor))
                    neighbor.makeOpenSet()
        Draw()
        if currentNode != Start:
            currentNode.makeClosedSet()
