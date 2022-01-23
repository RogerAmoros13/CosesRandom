import pygame
import numpy as np

ALTURA, LLARG = 700, 800

incr_altura = int(ALTURA / 100)
incr_llarg = int(LLARG / 100)

theta = np.linspace(0, 2 * np.pi, 100)
phi = np.linspace(0, 2 * np.pi, 150)


A, B = 0, 0
R = 1

K2 = 5

chars = '.,-~:;=!*#$@'
dot = '·'
arrel_dos = np.sqrt(2)
arrel_tres = np.sqrt(3)

pygame.init()
pygame.display.set_caption('Donut')
screen = pygame.display.set_mode((LLARG, ALTURA))
font = pygame.font.SysFont('Arial', 10, bold=True)

def text_display(letter, x_start, y_start):
    text = font.render(letter, True, (255, 255, 255))
    screen.blit(text, (x_start, y_start))

def render_esfera(R, lightx, lighty, lightz):
    K1 = 100 * K2 * 3 / (12 * R)

    arrel = np.sqrt(lightx**2 + lighty**2 + lightz**2)

    zbuffer = {}
    output = {}

    for i in range(100):
        for j in range(100):
            zbuffer[(i, j)] = 0
            output[(i, j)] = ' '

    for i in theta:
        costheta = np.cos(i)
        sintheta = np.sin(i)

        for j in phi:
            cosphi = np.cos(j)
            sinphi = np.sin(j)

            x = R * cosphi * sintheta
            y = R * sinphi * sintheta
            z = R * costheta + K2
            ooz = 1 / z
            
            # projeccions
            xp = int(100 / 2 + K1 * ooz * x)
            yp = int(100 / 2 - K1 * ooz * y)

            #luminositat
            # (1, 1, 0)
            # L = sintheta * (sinphi - cosphi) 
            # L = L / arrel_dos
            # (1, 1, -2)
            L = - lightx * sintheta * cosphi + sinphi * sintheta * lighty - lightz * cosphi 
            # L = lightz * cosphi
            # L = - lightx * sintheta * cosphi
            # L = sinphi * sintheta * lighty
            L = L / arrel
 
            if L > 0:
                if ooz > zbuffer[(xp, yp)]:
                    zbuffer[(xp, yp)] = ooz
                    output[(xp, yp)] = chars[int(L * 8)]
                    # output[(xp, yp)] = dot
    return output


run = True
lightx, lighty, lightz = 0.5, 0, -1
# avantx = False
# avanty = False
# movex = True
# movey = False

# lightx = np.cos(theta)
# lighty = np.sin(theta)
k = 0
while run:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            elif event.key == pygame.K_UP:
                if lighty <= 1:
                    lighty += 0.05
            elif event.key == pygame.K_DOWN:
                if lighty >= -1:
                    lighty -= 0.05
            elif event.key == pygame.K_RIGHT:
                if lightx >= -1:
                    lightx -=0.05
            elif event.key == pygame.K_LEFT:
                if lightx <= 1:
                    lightx += 0.05
            elif event.key == pygame.K_w:
                if lightz <= 1:
                    lightz +=0.05
            elif event.key == pygame.K_s:
                if lightz >= -1:
                    lightz -= 0.05
            


    # a, b = lightx[k], lighty[k]
    # k += 1
    # if k == 99:
    #     k = 0
    esfera = render_esfera(R, lightx, lighty, lightz)
    for i in range(100):
        for j in range(100):
            text_display(esfera[(i,j)], i * incr_altura, j * incr_llarg)
    pygame.display.update()

    # if movex:
    #     if avantx:
    #         lightx += .05
    #         if lightx > 1:
    #             avantx = False
    #             movex = False
    #             movey = True
    #     else:
    #         lightx -= .05
    #         if lightx < -1:
    #             avantx = True
    #             movex = False
    #             movey = True

    # if movey:
    #     if avanty:
    #         lighty += .05
    #         if lighty > 1:
    #             avanty = False
    #             movey = False
    #             movex = True
    #     else:
    #         lighty -= .05
    #         if lighty < -1:
    #             avanty = True
    #             movex = True
    #             movey = False


    # if lightx <= 1 and lightx > -1:
    #     if lighty == 1:
    #         lightx -= .05
    #     if lighty == -1:
    #         lightx += .05

    # A += 0.02
    # B += 0.02


