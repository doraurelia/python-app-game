from typing import Optional


class Stanje:
    def __init__(self, ploca, x, o):
        self.ploca = ploca
        self.x = x
        self.o = o


class Potez:
    def __init__(self, polaziste, odrediste, zrtva: Optional[int] = None):
        self.polaziste = polaziste
        self.odrediste = odrediste
        self.zrtva = zrtva
