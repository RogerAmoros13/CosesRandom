import numpy as np

"""
Calcul de la transformada discreta de Fourier.
Retorna una llista de diccionaris.
Cada diccionari te la informació sobre els epicicles:
    re: part real del centre de la circumferencia
    im: part imaginaria del centre de la circumferencia
    freq: frequencia de rotació
    amp: amplitud (radi)
    fase: punt inicial de rotació

Amb les següents dades podem dibuixar "qualsevol cosa"
La idea es afegir als imputs la transformada que volem que faça, be per nom o be passant una llista
"""

class Fourier:
    def __init__(self, axis):
        self.X = []
        self.Y = []
        self.axis = axis
    def fft(self, punts):
        self.punts(punts)
        aux = []
        if self.axis == 0:
            punts = self.x
            N = len(punts)
        elif self.axis == 1:
            punts = self.y
            N = len(punts)

        for k in range(N):
            re = 0
            im = 0
            for n in range(N):
                const = (2 * np.pi * k * n) / N
                re += punts[n] * np.cos(const)
                im += punts[n] * np.sin(const)
            im = im / N
            re = re / N
            freq = k
            amp = np.sqrt(re**2 + im**2)
            fase = np.arctan2(re, im)
            aux.append({'re': re, 'im': im, 'freq': freq, 'amp': amp, 'fase': fase})
        self.X = sorted(aux, key=lambda x: x['amp'], reverse=True)

    def punts(self, punts, **kwargs):
        if punts == 'cercle':
            interval = np.linspace(0, 2*np.pi, 600)[:-1]
            a = np.sin(interval) + 2*np.cos(interval)
            b = np.cos(interval) + np.sin(interval)
        elif punts == 'buyate_interno':
            interval = np.linspace(-2*np.pi, 2*np.pi, 200)[:-1]
            a = 4 * np.cos(interval) * interval**2
            b = 3 * np.sin(interval) * interval**2

        elif punts == 'doble_buyate':
            interval = np.linspace(0, 2*np.pi, 200)[:-1]
            a = 3 * np.cos(interval) + np.cos(3*interval)
            b = 3 * np.sin(interval) + np.sin(3*interval)

        elif punts == 'hypocycloid':
            r = 8
            s = 3
            interval = np.linspace(0, 6*np.pi, 600)[:-1]
            a = (r-s) * np.cos(interval) + s * np.cos(((r-s)/s)*interval)
            b = (r-s) * np.sin(interval) - s * np.sin(((r-s)/s)*interval)

        elif punts == 'cardioide':
            interval = np.linspace(0, 2*np.pi, 200)[:-1]
            a = 2 * np.cos(interval) - np.cos(2 * interval)
            b = 2 * np.sin(interval) - np.sin(2 * interval)

        elif punts == 'signal':
            interval = np.linspace(0, 2*np.pi, 200)[:-1]
            a = np.sin(interval) - np.sin(3*interval) + np.cos(3*interval)
            b = np.sin(interval)


        else:
            raise "Nom valid pixorro"

        

        self.x = np.interp(a, (a.min(), a.max()), (0, 300))
        self.y = np.interp(b, (b.min(), b.max()), (0, 300))