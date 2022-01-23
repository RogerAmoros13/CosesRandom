import pygame
from fourier import Fourier
from draw import Draw
import numpy as np

WIDTH, HEIGHT = 1200, 650

fps = 60
offset = 600
white = (255, 255, 255)
gray = (150, 150, 150)
black_raro = (56,54,56)
crimson = (230, 20, 32)
blau_clar = (115, 200, 248)
fucsia = (247, 93, 249)
black = (0, 0, 0)
roig = (247, 47, 21)
blau_oscur = (21, 85, 243)

style1 = {'circle': black_raro, 'line': black_raro, 'point': crimson}
style2 = {'punts': blau_oscur, 'line': gray, 'rastre': blau_clar}

class Screen:
    def __init__(self, imatge):
        pygame.display.set_caption('Fourier Series Transform')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.time = 0
        self.fourierx = Fourier(0)
        self.fouriery = Fourier(1)
        self.draw = Draw(self.screen)
        self.fourierx.fft(imatge)
        self.fouriery.fft(imatge)
        self.dim = len(self.fourierx.X)
    def run(self):
        run = True
        primera = True
        self.screen.fill(black)
        while run:
            self.clock.tick(fps)
            self.screen.fill(black)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key ==pygame.K_ESCAPE:
                        pygame.quit()

            puntX = self.draw.draw_fourier(self.fourierx.X, 'horitzontal', style1, self.time)
            puntY = self.draw.draw_fourier(self.fouriery.X, 'vertical', style1, self.time)
            self.draw.draw_guides(puntX)
            self.draw.draw_guides(puntY)

            if primera:
                self.draw.draw_first_point()
                primera = False
            else:
                self.draw.draw_image()
            pygame.display.update()
            self.time += (2*np.pi) / self.dim


if __name__ == '__main__':
    pantalla = Screen('signal')
    pantalla.run()