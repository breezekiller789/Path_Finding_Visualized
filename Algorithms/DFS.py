from Algorithms.Reconstruct_Path import Reconstruct_Path
import pygame


def DFS(Draw, Grid, Start, End):
    Visited = {Start}
    currentNode = Start
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

        # Update all the neighbors of current node
        currentNode.updateNeighbors(Grid)

        # if currentNode's neighbor hasn't been visited, visit it!
        for neighbor in currentNode.neighbors:
            if neighbor in Visited:
                continue
            else:
                tmp = currentNode           # temp currentNode because we want
                currentNode = neighbor      # it to be our previous node
                currentNode.comefrom = tmp
                currentNode.makeClosedSet()
                Visited.add(currentNode)
                break
        # if all currentNode's neighbors are visited, back to previous node to
        # see if it has neighbor that hasn't been visited yet
        else:
            currentNode = currentNode.comefrom
            continue

        # Found Path
        if currentNode == End:
            Reconstruct_Path(Draw, currentNode, End)
            return True

        Draw()
