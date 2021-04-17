# from queue import PriorityQueue
from Algorithms.Reconstruct_Path import Reconstruct_Path
import fibheap
import pygame
# Using Fibanocci Heap
# G = (V, E)
# Time = O(VlogV + E)


heap1 = fibheap.makefheap()
nums = [1, 3, 10, 2, 8, 9, 11]
for num in nums:
    fibheap.fheappush(heap1, num)


def Fibanocci_Heap_Dijkstra(Draw, Grid, Start, End):
    Time_Inserted = 0
    Visited = {Start}
    Distances = {node: float("inf") for row in Grid for node in row}
    Distances[Start] = 0
    FHeap = fibheap.makefheap()
    fibheap.fheappush(FHeap, (Distances[Start], Time_Inserted, Start))
    while FHeap.num_nodes:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
        currentNode = fibheap.fheappop(FHeap)[2]
        currentNode.updateNeighbors(Grid)

        # Found the path, so trace back the path
        if currentNode == End:
            Reconstruct_Path(Draw, currentNode, Start, End)
            return True

        temp_Distance = Distances[currentNode] + 1
        for neighbor in currentNode.neighbors:
            if neighbor not in Visited:
                # Relax
                if temp_Distance < Distances[neighbor]:
                    Time_Inserted += 1
                    neighbor.comefrom = currentNode
                    Distances[neighbor] = temp_Distance
                    if neighbor != End:
                        neighbor.makeOpenSet()
                    Visited.add(neighbor)
                    fibheap.fheappush(
                        FHeap,
                        (Distances[neighbor], Time_Inserted, neighbor)
                    )
        Draw()
        if currentNode != Start:
            currentNode.makeClosedSet()
