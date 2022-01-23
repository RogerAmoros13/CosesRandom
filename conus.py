import pygame
import numpy as np

ALTURA, LLARG = 700, 700

incr_altura = int(ALTURA / 150)
incr_llarg = int(LLARG / 150)

phi = np.linspace(0, 2 * np.pi, 40)

A, B = 0, 0
# R, alt = 1
R1, R2 = 1, 2

K2 = 9
K1 = 100 * K2 * 3 / (12 * (R1 + R2))

chars = '.,-~:;=!*#$@'
dot = '·'

pygame.init()
pygame.display.set_caption('Donut')
screen = pygame.display.set_mode((LLARG, ALTURA))
font1 = pygame.font.SysFont('Arial', 10, bold=True)
font2 = pygame.font.SysFont('Arial', 15, bold=True)


def info_pantalla(lightx, lighty, lightz, moveA, moveB, A, B):
    info_llum = font2.render(f"LLUM: {round(lightx, 2)}, {round(lighty, 2)}, {round(lightz, 2)}", False, (255, 255, 255))
    info_movimentA = font2.render(f"Rotacio eix x: {moveA} --> {round(A, 2)}", False, (255, 255, 255))
    info_movimentB = font2.render(f"Rotacio eix z: {moveB} --> {round(B, 2)}", False, (255, 255, 255))
    screen.blit(info_llum, (500, 20))
    screen.blit(info_movimentA, (500, 40))
    screen.blit(info_movimentB, (500, 60))


def text_display(letter, x_start, y_start):
    text = font1.render(letter, True, (255, 255, 255))
    screen.blit(text, (x_start, y_start))

def render_cono(R1, R2, A, B, lightx, lighty, lightz):
    light = np.array([lightx, lighty, lightz])
    cosA = np.cos(A)
    sinA = np.sin(A)
    cosB = np.cos(B)
    sinB = np.sin(B)
    
    zbuffer = {}
    output = {}
    for i in range(150):
        for j in range(150):
            zbuffer[(i, j)] = 0
            output[(i, j)] = ' '

    prod1 = R2 * cosA * sinB

    theta = np.linspace(0, R2, 40)

    for i in theta:
        R1i = R1 * i
        for j in phi:
            cosphi = np.cos(j)
            sinphi = np.sin(j)

            x = i * (R1 * (cosphi * cosB + sinphi * sinA * sinB) + prod1)
            y = i * (R1 * sinphi * cosA - R2 * sinA)
            z = i * (R1 * (sinphi * sinA * cosB - cosphi * sinB) + prod1) + K2

            a1 = R1i * (cosphi * sinB * sinA - sinphi * cosB)
            a2 = R1i * (sinphi * sinB - cosphi * sinA * cosB)
            a3 = R1i * cosphi * cosA

            b1 = R1 * (cosphi * cosB + sinphi * sinA * sinB) + prod1
            b2 = R1 * (sinB * cosphi + sinphi * sinA * cosB) + prod1
            b3 = R1 * sinphi * cosA - R2 * sinA

            vect1 = np.array([a1, a2, a3])
            vect2 = np.array([b1, b2, b3])

            vect_norm = np.cross(vect1, vect2)
            vect_norm = vect_norm / np.linalg.norm(vect_norm)

            ooz = 1 / z
            
            xp = int(x*75*ooz + K1) 
            yp = int(y*75*ooz + K1)
            
            L = np.dot(vect_norm, light)
            
            if L > 0:
                if xp > 150 or xp < 0 or yp > 150 or yp < 0:
                    pass
                else:
                    if ooz > zbuffer[(xp, yp)]:
                        zbuffer[(xp, yp)] = ooz
                        output[(xp, yp)] = chars[int(L * 10)]
                        # output[(xp, yp)] = dot
    return output


run = True
lightx, lighty, lightz = 0, 1, 0
rotarA = True
rotarB = True

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
            elif event.key == pygame.K_a:
                if rotarA:
                    rotarA = False
                else:
                    rotarA = True
            elif event.key == pygame.K_b:
                if rotarB:
                    rotarB = False
                else:
                    rotarB = True
            
    cono = render_cono(R1, R2, A, B, lightx, lighty, lightz)
    for i in range(150):
        for j in range(150):
            text_display(cono[(i,j)], i * incr_altura, j * incr_llarg)
    info_pantalla(lightx, lighty, lightz, rotarA, rotarB, A, B)
    pygame.display.update()
    if rotarA:
        A += 0.05
    if rotarB:
        B += 0.05


