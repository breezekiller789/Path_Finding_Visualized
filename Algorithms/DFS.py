from Algorithms.Reconstruct_Path import Reconstruct_Path
import pygame

# I encountered a problem that if currentNode has all neighbors visited, then my
# program will get stuck because it has no neighbor to visit, and my solution to
# that is, i just simply go back to previous node since i have tracked the
# previous node of each node, i go back to previous nodes until i have neighbors
# to visit, then i will go from there.


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
            Reconstruct_Path(Draw, currentNode, Start, End)
            return True

        Draw()
