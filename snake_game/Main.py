import pygame
from random import randint
pygame.init()

def comandos(comando_de_entrada):
    if comando_de_entrada == pygame.K_UP and direcao_de_movimento != 'baixo':
        return 'cima'
    elif comando_de_entrada == pygame.K_DOWN and direcao_de_movimento != 'cima':
        return 'baixo'
    elif comando_de_entrada == pygame.K_LEFT and direcao_de_movimento != 'direita':
        return 'esquerda'
    elif comando_de_entrada ==  pygame.K_RIGHT and direcao_de_movimento != 'esquerda':
        return 'direita'
    else:
        return direcao_de_movimento

def analisador(filtro):
    while True:
        i = randint(10, 480)
        if i%filtro == 0:
            break
    return i

def update_corpo():
    if len(corpo) >= 1:
        corpo[0] = [pygame.Rect(x_head, y_head, 10,  10), [x_head, y_head]]
        for index in range(-1, (len(corpo)*-1), -1):
            corpo[index] = [pygame.Rect(corpo[index-1][1][0], corpo[index-1][1][1], 10, 10), [corpo[index-1][1][0], corpo[index-1][1][1]]]

x_tela, y_tela = (500, 500)
tela = pygame.display.set_mode((x_tela, y_tela))
pygame.display.set_caption("Sanke")

pygame.mixer.music.load('midia/musicaFundo.mp3')
fps = pygame.time.Clock()

imagemIntroducao = pygame.transform.scale(pygame.image.load('midia/wallpaperSnake.png'), (x_tela, y_tela))
chao = pygame.transform.scale(pygame.image.load('midia/chao.png'), (x_tela, y_tela))
somMastigar = pygame.mixer.Sound('midia/somMastigar.mp3')

loopPrincipal = True
loopMenu = True
loopGame = False

while loopPrincipal:
    x_head, y_head = (100, 100)
    velocidade = 4
    direcao_de_movimento = 'direita'
    comeu_maca = False
    corpo = [[pygame.Rect(x_head, y_head, 10,  10), [x_head, y_head]]]
    maca = pygame.Rect(analisador(int(velocidade)), analisador(int(velocidade)), 10, 10)
    pygame.mixer.music.play(10)

    # Tela menu inicial
    while loopMenu:
        fps.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loopGame, loopMenu, loopPrincipal = (False, False, False)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    loopGame = True
                    loopMenu = False

        tela.blit(imagemIntroducao, (0,0))
        pygame.display.flip()

    #Tela do jogo
    while loopGame:
        fps.tick(20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loopGame, loopMenu, loopPrincipal = (False, False, False)

            elif event.type == pygame.KEYDOWN:  # Recolhendo entrada de dados pelo teclado
                direcao_de_movimento = comandos(event.key)

        head = pygame.Rect(x_head, y_head, 10, 10) # Constante verificação das posicoes x e y

        # Gerando maçãs aleatórias
        if comeu_maca:
            maca = pygame.Rect(analisador(int(velocidade)), analisador(int(velocidade)), 10, 10)
            comeu_maca = False

        # Comendo maçãs
        if head.colliderect(maca):
            comeu_maca = True
            corpo.append('bloco') # Adiciona nova parte do corpo
            somMastigar.play()
            if velocidade < 13:
                velocidade += 0.2

        # Constante movimentação do corpo
        update_corpo()

        # Constante movimentação do personagem
        if direcao_de_movimento == 'direita':
            x_head += int(velocidade)
        elif direcao_de_movimento == 'esquerda':
            x_head -= int(velocidade)
        elif direcao_de_movimento == 'cima':
            y_head -= int(velocidade)
        elif direcao_de_movimento == 'baixo':
            y_head += int(velocidade)

        # Movendo o personagem de uma extremidade a outra
        if x_head < 0:
            x_head = x_tela
        elif x_head > x_tela:
            x_head = 0
        if y_head < 0:
            y_head = y_tela
        elif y_head > y_tela:
            y_head = 0

        #Detecção da colisão da cabeça com o corpo
        if len(corpo) > 5:
            for i in range(5, len(corpo)):
                if head.colliderect(corpo[i][0]):
                    loopMenu = True
                    loopGame = False

        # Desenhos na tela
        tela.fill('green')
        tela.blit(chao, (0, 0))
        pygame.draw.rect(tela, 'red', maca)
        pygame.draw.rect(tela, 'black', head)
        if len(corpo) > 0:
            for elemento in corpo:
                pygame.draw.rect(tela, 'black', elemento[0])

        pygame.display.flip()

pygame.quit()
