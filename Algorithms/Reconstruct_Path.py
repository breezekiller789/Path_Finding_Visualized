import pygame


def Reconstruct_Path(Draw, currentNode, End):
    '''
        Trace back the path that lead us to the end node
    '''
    currentNode = currentNode.comefrom
    End.makeEnd()
    while currentNode.comefrom:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
        currentNode.makePath()
        currentNode = currentNode.comefrom
        Draw()
