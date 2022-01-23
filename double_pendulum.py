import numpy as np
import pygame
import time

"""
Parametres xaxis:

1)
g = 0.98
t1 = np.pi / 3
t2 = np.pi / 2

2)

g = 0.98
t1 = np.pi / 3.5
t2 = np.pi / 2
v1 = 0.01
v2 = 0.01


En general seguir els següents passos:
    - Gravetat entre 0 i 1
    - Velocitat entre 0.01 i 0.1
"""

WIDTH, HEIGHT = 800, 650

fps = 60
offset = [400, 250]
white = (255, 255, 255)
gray = (150, 150, 150)
black_raro = (56,54,56)
crimson = (230, 20, 32)
blau_clar = (115, 200, 248)
fucsia = (247, 93, 249)
black = (0, 0, 0)
roig = (247, 47, 21)
blau_oscur = (21, 85, 243)

style1 = {'punts': roig, 'linia': white, 'rastre': fucsia}
style2 = {'punts': blau_oscur, 'linia': gray, 'rastre': blau_clar}

"""
Condicions inicials
"""

t1 = np.pi / 2
t2 = np.pi / 2
m1 = 5
m2 = 10
L1 = 150
L2 = 150


class Pendul:
    def __init__(self, t1, t2, m1, m2, L1, L2, v1, v2):
        self.t1 = t1
        self.t2 = t2
        self.m1 = m1
        self.m2 = m2
        self.L1 = L1
        self.L2 = L2
        self.v1 = v1
        self.v2 = v2
        self.G = - 1
        self.x1 = L1 * np.sin(t1)
        self.y1 = - L1 * np.cos(t1)
        self.x2 = self.x1 + L2 * np.sin(t2)
        self.y2 = self.y1 - L2 * np.cos(t2)
        self.passed_points = []

    def update_pos(self):
        self.calculate_angles()
        self.x1 = self.L1 * np.sin(self.t1)
        self.y1 = - self.L1 * np.cos(self.t1)
        self.x2 = self.x1 + self.L2 * np.sin(self.t2)
        self.y2 = self.y1 - self.L2 * np.cos(self.t2)
        self.passed_points.append((offset[0] + self.x2, offset[1] + self.y2))

    def primer_terme(self):
        num1 = -self.G * (2 * self.m1 + self.m2) * np.sin(self.t1) - self.G * self.m2 * np.sin(self.t1 - 2 * self.t2)
        num2 = 2 * np.sin(self.t1 - self.t2) * self.m2
        num3 = (self.v2*self.v2) * self.L2 + (self.v1*self.v1) * self.L1 * np.cos(self.t1 - self.t2)
        num4 = self.L1 * (2 * self.m1 + self.m2 - self.m2 * np.cos(2 * (self.t1  - self.t2)))
        return (num1 - num2 * num3) / num4

    def segon_terme(self):
        num1 = 2 * np.sin(self.t1 - self.t2)
        num2 = (self.v1*self.v1) * self.L1 * (self.m1 + self.m2) + self.G * (self.m1 + self.m2) * np.cos(self.t1)
        num3 = (self.v2*self.v2) * self.L2 * self.m2 * np.cos(self.t1 - self.t2)
        num4 = self.L2 * (2 * self.m1 + self.m2 - self.m2 * np.cos(2 * (self.t1  - self.t2)))
        return (num1 * (num2 + num3)) / num4 

    def calculate_angles(self):
        acc1 = self.primer_terme()
        acc2 = self.segon_terme()

        self.v1 += acc1
        self.v2 += acc2

        self.t1 += self.v1
        self.t2 += self.v2


class Screen:
    def __init__(self):
        pygame.display.set_caption('Pendul Doble')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.time = 0
        self.pendul1 = Pendul(np.pi / 2, np.pi / 2, m1, m2, L1, L2, 0, 0)
        self.pendul2 = Pendul(np.pi / 2, np.pi / 2.00001, m1, m2, L1, L2, 0 ,0)
        pygame.display.update()

    def run(self):
        run = True
        self.screen.fill(black)
        primera = True
        while run:
            self.clock.tick(fps)
            self.screen.fill(black)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key ==pygame.K_ESCAPE:
                        pygame.quit()

            self.draw_necessary(self.pendul1, style1)
            self.draw_necessary(self.pendul2, style2)

            if len(self.pendul1.passed_points) > 300:
                self.pendul1.passed_points.pop(0)
                self.pendul2.passed_points.pop(0)

            if not primera:
                self.draw_hist(self.pendul1, style1)
                self.draw_hist(self.pendul2, style2)

            pygame.display.update()
            
            if primera:
                primera = False
                time.sleep(1)
                
            self.pendul1.update_pos()
            self.pendul2.update_pos()

            time.sleep(0.02)


    def draw_circles(self, color, center, radius, n = 1):
        pygame.draw.circle(self.screen, color, center, radius, n)


    def draw_points(self, color, center, n=1):
        pygame.draw.circle(self.screen, color, center, n)
    
    def draw_line(self, color, point1, point2, n = 1):
        pygame.draw.aaline(self.screen, color, point1, point2, n)


    def draw_necessary(self, pendul, style):
        point1 = (offset[0] + pendul.x1, offset[1] + pendul.y1)
        point2 = (offset[0] + pendul.x2, offset[1] + pendul.y2)
        self.draw_line(style['linia'], offset, point1, 3)
        self.draw_points(style['punts'], point1, 5)
        self.draw_line(style['linia'], point1, point2)
        self.draw_points(style['punts'], point2, 5)

    def draw_hist(self, pendul, style):
        for i in range(len(pendul.passed_points)-1):
            self.draw_line(style['rastre'], pendul.passed_points[i], pendul.passed_points[i+1])
            

    




if __name__ == '__main__':
    pantalla = Screen()
    pantalla.run()