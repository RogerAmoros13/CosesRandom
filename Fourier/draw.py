import pygame
import numpy as np
from pygame import draw

"""
Una classe per a dibuixar totes les merdes que ens faran falta
"""

white = (255, 255, 255)
gray = (150, 150, 150)
black = (0,0,0)
crimson = (230, 20, 32)

class Draw:
    def __init__(self, screen):
        self.screen = screen
        self.posX = []
        self.posY = []

    def draw_circles(self, color, center, radius, n = 1):
        pygame.draw.circle(self.screen, color, center, radius, n)

    def draw_points(self, color, center, n=1):
        pygame.draw.circle(self.screen, color, center, n)
    
    def draw_line(self, color, point1, point2, n = 1):
        pygame.draw.aaline(self.screen, color, point1, point2, n)

    def draw_fourier(self, data, position, style, time):            
        if position == 'vertical':
            fase = 0
            x2 = 120
            y2 = 450
        elif position == 'horitzontal':
            fase = -np.pi / 2
            x2 = 750
            y2 = 120

        for i in range(1, len(data)-1):
            x1 = x2
            y1 = y2
            x2 += data[i]['amp'] * np.cos(time * data[i]['freq'] + data[i]['fase'] + fase)
            y2 += data[i]['amp'] * np.sin(time * data[i]['freq'] + data[i]['fase'] + fase)
            if data[i]['amp'] > 2:
                self.draw_circles(style['circle'], (x1, y1), data[i]['amp'], 2)
                self.draw_points(style['point'], (x2, y2), 1)
                self.draw_line(style['line'], (x1,y1), (x2, y2), 2)

        if position == 'vertical':
            self.posY.insert(0, y2)
        elif position == 'horitzontal':
            self.posX.insert(0, x2)
        return (x2, y2)
        

    def draw_image(self):
        if len(self.posX) > 200:
            self.posY.pop()
            self.posX.pop()

        for i in range(len(self.posX)-1):
            self.draw_line(white, (self.posX[i], self.posY[i]), (self.posX[i+1], self.posY[i+1]), 3)
        
        self.draw_points(crimson, (self.posX[0], self.posY[0]), 3)

    def draw_first_point(self):
        self.draw_points(white, (self.posX[0], self.posY[0]), 1)

    def draw_guides(self, punt):
        self.draw_line(gray, punt, (self.posX[0], self.posY[0]), 1)