import pygame


def Reconstruct_Path(Draw, currentNode, Start, End):
    '''
        Trace back the path that lead us to the end node
    '''
    # currentNode = currentNode.comefrom
    comefrom_stack = []
    End.makeEnd()
    while currentNode.comefrom:
        comefrom_stack.append(currentNode.comefrom)
        currentNode = currentNode.comefrom

    while comefrom_stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
        node = comefrom_stack.pop()
        if node == Start:
            continue
        node.makePath()
        Draw()
