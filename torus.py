import pygame
import numpy as np

ALTURA, LLARG = 700, 800

incr_altura = int(ALTURA / 100)
incr_llarg = int(LLARG / 100)

theta = np.linspace(0, 2 * np.pi + 0.01, 100)
phi = np.linspace(0, 2 * np.pi + 0.01, 150)


A, B = 0, 0

R1 = 1
R2 = 2
K2 = 5
K1 = 99 * K2 * 3 / (12 * (R1 + R2))

chars = '.,-~:;=!*#$@'
dot = '·'
arrel = np.sqrt(2)

pygame.init()
pygame.display.set_caption('Donut')
screen = pygame.display.set_mode((LLARG, ALTURA))
font = pygame.font.SysFont('Arial', 10, bold=True)

def text_display(letter, x_start, y_start):
    text = font.render(letter, True, (255, 255, 255))
    screen.blit(text, (x_start, y_start))

def render_donut(A, B):
    zbuffer = {}
    output = {}
    cosA, sinA = np.cos(A), np.sin(A)
    cosB, sinB = np.cos(B), np.sin(B)

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

            circlex = R2 + R1 * costheta
            circley = R1 * sintheta

            x = circlex * (cosB * cosphi + sinA * sinB * sinphi) - circley * cosA * sinB
            y = circlex * (sinB * cosphi - sinA * cosB * sinphi) + circley * cosA + cosB
            z = cosA * circlex * sinphi + circley * sinA + K2
            ooz = 1 / z
            
            # projeccions
            xp = int(100 / 2 + K1 * ooz * x)
            yp = int(100 / 2 - K1 * ooz * y)

            #luminositat
            L = cosphi * costheta * sinB - cosA * costheta * sinphi - sinA * sintheta + cosB * ( cosA * sintheta - costheta * sinA * sinphi)

            if L >= 0:
                if ooz > zbuffer[(xp, yp)]:
                    zbuffer[(xp, yp)] = ooz
                    output[(xp, yp)] = chars[int(L * 8)]
                    # output[(xp, yp)] = dot
    return output


run = True

while run:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()

    donut = render_donut(A, B)
    # print(donut)
    for i in range(100):
        for j in range(100):
            # print(i, j)
            # print(incr_altura * i, incr_llarg * j)
            # print(donut[(i, j)])
            text_display(donut[(i,j)], i * incr_altura, j * incr_llarg)
    pygame.display.update()
    A -= 0.02
    B += 0.02


