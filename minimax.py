import logging
import random

#from logika_igre import IGRALEC_1, IGRALEC_2, NI_KONEC, nasprotnik
from logika_igre import *

######################################################################
## Algoritem minimax

class Minimax:
    # Algoritem minimax predstavimo z objektom, ki hrani stanje igre in
    # algoritma, nima pa dostopa do GUI (ker ga ne sme uporabljati, saj deluje
    # v drugem vlaknu kot tkinter).

    def __init__(self, globina):
        self.globina = globina  # do katere globine iščemo
        self.prekinitev = False # ali moramo končati
        self.igra = None # objekt, ki opisuje igro (ga dobimo kasneje)
        self.jaz = None  # katerega igralca igramo (podatek dobimo kasneje)
        self.poteza = None # sem napišemo potezo, ko jo najdemo

    def prekini(self):
        """Metoda, ki jo pokliče GUI, če je treba nehati razmišljati, ker
           je uporabnik zaprl okno ali izbral novo igro."""
        self.prekinitev = True

    def izracunaj_potezo(self, igra):
        """Izračunaj potezo za trenutno stanje dane igre."""
        # To metodo pokličemo iz vzporednega vlakna
        self.igra = igra
        self.prekinitev = False # Glavno vlakno bo to nastvilo na True, če moramo nehati
        self.jaz = self.igra.na_potezi
        self.poteza = None # Sem napišemo potezo, ko jo najdemo
        # Poženemo minimax
        (poteza, vrednost) = self.minimax(self.globina, True)
        self.jaz = None
        self.igra = None
        if not self.prekinitev:
            # Potezo izvedemo v primeru, da nismo bili prekinjeni
            logging.debug("minimax: poteza {0}, vrednost {1}".format(poteza, vrednost))
            self.poteza = poteza

    # Vrednosti igre
    ZMAGA = 100000
    NESKONCNO = ZMAGA + 1 # Več kot zmaga

##    def vrednost_pozicije(self):
##        """Ocena vrednosti pozicije na plošči."""
##        notranji_krog = [(4,4),(5,4),(4,5),(6,5),(5,6),(6,6)]
##        srednji_krog = [(3,3),(4,3),(5,3),(6,3),(7,5),(7,6),(7,7),(6,7),(5,7),(4,6),(3,5),(3,4)]
##        predzadnji_krog = [(2,2),(3,2),(4,2),(5,2),(6,3),(7,4),(8,5),(8,6),(8,7),(8,8),(7,8),(6,8),(5,8),(4,7),(3,6),(2,5),(2,4),(2,3)]
##        zunanji_krog = [(1,1),(2,1),(3,1),(4,1),(5,1),(6,2),(7,3),(8,4),(9,5),(9,6),(9,7),(9,8),(9,9),(8,9),(7,9),(6,9),(5,9),(4,8),(3,7),(2,6),(1,5),(1,4),(1,3),(1,2)]
##        vrednost = 0
##        for x in range(1,10):
##            for y in range(1,10):
##                if self.igra.plosca[x][y] is not None:
##                    barva = self.igra.plosca[x][y]
##                    if barva == self.igra.pripadajoca_barva(self.jaz):
##                        predznak = 1
##                    elif barva == self.igra.pripadajoca_barva(nasprotnik(self.jaz)):
##                        predznak = -1
##                    if x ==5 and y == 5:
##                        vrednost += predznak * 100
##                    elif (x,y) in notranji_krog:
##                        vrednost += predznak * 50
##                    elif (x,y) in [(2,2),(5,8),(4,7),(3,6),(2,5),(2,4),(2,3)]:
##                        if self.igra.plosca[x+1][y] == self.igra.pripadajoca_barva(self.jaz) and self.igra.plosca[x-1][y] == self.igra.pripadajoca_barva(nasprotnik(self.jaz)):
##                            vrednost += predznak * Minimax.ZMAGA / 100
##                        else:
##                            vrednost -= predznak * 10
##                    elif (x,y) in [(2,5),(2,4),(2,3),(2,2),(3,2),(4,2),(5,2)]:
##                        if self.igra.plosca[x+1][y+1] == self.igra.pripadajoca_barva(self.jaz) and self.igra.plosca[x-1][y-1] == self.igra.pripadajoca_barva(nasprotnik(self.jaz)):
##                            vrednost += predznak * Minimax.ZMAGA / 100
##                        else:
##                            vrednost -= predznak * 10
##                    elif (x,y) in [(2,2),(3,2),(4,2),(5,2),(6,3),(7,4),(8,5)]:
##                        if self.igra.plosca[x][y+1] == self.igra.pripadajoca_barva(self.jaz) and self.igra.plosca[x][y-1] == self.igra.pripadajoca_barva(nasprotnik(self.jaz)):
##                            vrednost += predznak * Minimax.ZMAGA / 100
##                        else:
##                            vrednost -= predznak * 10
##                    elif (x,y) in [(5,2),(6,3),(7,4),(8,5),(8,6),(8,7),(8,8)]:
##                        if self.igra.plosca[x-1][y] == self.igra.pripadajoca_barva(self.jaz) and self.igra.plosca[x+1][y] == self.igra.pripadajoca_barva(nasprotnik(self.jaz)):
##                            vrednost += predznak * Minimax.ZMAGA / 100
##                        else:
##                            vrednost -= predznak * 10
##                    elif (x,y) in [(5,8),(6,8),(7,8),(8,8),(8,7),(8,6),(8,5)]:
##                        if self.igra.plosca[x-1][y-1] == self.igra.pripadajoca_barva(self.jaz) and self.igra.plosca[x+1][y+1] == self.igra.pripadajoca_barva(nasprotnik(self.jaz)):
##                            vrednost += predznak * Minimax.ZMAGA / 100
##                        else:
##                            vrednost -= predznak * 10
##                    elif (x,y) in [(8,8),(7,8),(6,8),(5,8),(4,7),(3,6),(2,5)]:
##                        if self.igra.plosca[x][y-1] == self.igra.pripadajoca_barva(self.jaz) and self.igra.plosca[x][y+1] == self.igra.pripadajoca_barva(nasprotnik(self.jaz)):
##                            vrednost += predznak * Minimax.ZMAGA / 100
##                        else:
##                            vrednost -= predznak * 10
##        return vrednost

    def vrednost_pozicije(self):
        """Ocena vrednosti pozicije na plošči."""
        vrednost = 0
        plosca = self.igra.plosca
        izpodrinjeni = self.igra.izpodrinjeni
        moja_barva = self.igra.pripadajoca_barva(self.jaz)
        nasprotnikova_barva = self.igra.pripadajoca_barva(nasprotnik(self.jaz))
        # Najprej preštejemo svoje in nasprotnikove izpodrinjene krogce (s tem spodbujamo agresivno igro)
        moji_izpodrinjeni = izpodrinjeni.count(moja_barva)
        nasprotnikovi_izpodrinjeni = izpodrinjeni.count(nasprotnikova_barva)
        vrednost += (1000 * moji_izpodrinjeni - 900 * nasprotnikovi_izpodrinjeni)
        # Naredimo seznam "smeri", v katerem bodo vse vrstice, stolpci in diagonale.
        smeri = []
        for i in range(11):
            x = []
            y = []
            diagonala = []
            for j in range(11):
                if plosca[i][j] is not None:
                    y.append(plosca[i][j])
                if plosca[j][i] is not None:
                    x.append(plosca[j][i])
            if len(x) != 0:
                smeri.append([None] + x + [None])
            if len(y) != 0:
                smeri.append([None] + y + [None])
        # Seznam pozicij, kjer nas lahko v naslednji potezi izrinejo s plošče - zelo slabo.
        usodne_pozicije = [
            [None, moja_barva, nasprotnikova_barva, nasprotnikova_barva],
            [None, moja_barva, nasprotnikova_barva, nasprotnikova_barva, nasprotnikova_barva],
            [None, moja_barva, moja_barva, nasprotnikova_barva, nasprotnikova_barva, nasprotnikova_barva],
            ]
        # Podobno napišemo seznam ugodnih pozicij, ki pa mora imeti manjši učinek na vrednost pozicije
        # (recimo vrednost += 300?), ker se nasprotnik izmakne in ni ziher, da ga bomo res izrinili.
        ugodne_pozicije = [
            ]
        # Predlagam še seznam slabe_pozicije, ki bo podoben usodnim, samo da je med mojio barvo in
        # nasprotnikovo barvo eno prazno polje - torej da se nasprotnik nevarno približuje.
        for smer in smeri:
##            # Nežno spodbujamo premike proti sredini ?
##            if smer[1] == self.igra.barva_praznih and smer[-2] != self.igra.barva_praznih: 
##                vrednost += 50
##            elif smer[1] != self.igra.barva_praznih and smer[-2] == self.igra.barva_praznih: 
##                vrednost += 50
##            elif smer[1] == self.igra.barva_praznih and smer[-2] == self.igra.barva_praznih:
##                vrednost += 30
            for usodna in usodne_pozicije:
                # Pozicija se lahko pojavi na koncu ali pa na začetku smeri, zato jo še obrnemo
                if len(usodna) <= len(smer) and (smer[:len(usodna)] == usodna or smer[len(smer)-len(usodna):] == usodna[::-1]):
                    vrednost -= 500
                    break
        #print(plosca)
        print(88888888888888888888888888888888888888)
        print(000, 0, vrednost, 0, 000)
        return vrednost

    def minimax(self, globina, maksimiziramo):
        """Glavna metoda minimax."""
        if self.prekinitev:
            # Sporočili so nam, da moramo prekiniti
            logging.debug ("Minimax prekinja, globina = {0}".format(globina))
            return (None, 0)
        zmagovalec = self.igra.stanje_igre()
        if zmagovalec in (IGRALEC_1, IGRALEC_2):
            # Igre je konec, vrnemo njeno vrednost
            if zmagovalec == self.jaz:
                return (None, Minimax.ZMAGA)
            elif zmagovalec == nasprotnik(self.jaz):
                return (None, -Minimax.ZMAGA)
            else:
                return (None, 0)
        elif zmagovalec == NI_KONEC:
            # Igre ni konec
            if globina == 0:
                return (None, self.vrednost_pozicije())
            else:
                # Naredimo eno stopnjo minimax
                if maksimiziramo:
                    # Maksimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = -Minimax.NESKONCNO
                    najboljse_poteze = []
                    for poteza in self.igra.veljavne_poteze():
                        [izbrani, p] = poteza
                        if type(izbrani[0]) == int:
                                (x,y) = izbrani
                                self.igra.izbrani.append((x,y))
                        else:
                            for (x,y) in izbrani:
                                self.igra.izbrani.append((x,y))
                        self.igra.povleci_potezo(p)
                        vrednost = self.minimax(globina-1, not maksimiziramo)[1]
                        self.igra.razveljavi()
                        if vrednost == vrednost_najboljse:
                            najboljse_poteze.append(poteza)
                        elif vrednost > vrednost_najboljse:
                            vrednost_najboljse = vrednost
                            najboljse_poteze = [poteza]
                        self.igra.izbrani = []
                    najboljsa_poteza = random.choice(najboljse_poteze)
                else:
                    # Minimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = Minimax.NESKONCNO
                    for poteza in self.igra.veljavne_poteze():
                        [izbrani, p] = poteza
                        if type(izbrani[0]) == int:
                                (x,y) = izbrani
                                self.igra.izbrani.append((x,y))
                        else:
                            for (x,y) in izbrani:
                                self.igra.izbrani.append((x,y))
                        self.igra.povleci_potezo(p)
                        vrednost = self.minimax(globina-1, not maksimiziramo)[1]
                        self.igra.razveljavi()
                        if vrednost == vrednost_najboljse:
                            najboljse_poteze.append(poteza)
                        elif vrednost < vrednost_najboljse:
                            vrednost_najboljse = vrednost
                            najboljse_poteze = [poteza]
                        self.igra.izbrani = []
                    najboljsa_poteza = random.choice(najboljse_poteze)

                assert (najboljsa_poteza is not None), "minimax: izračunana poteza je None"
                return (najboljsa_poteza, vrednost_najboljse)
        else:
            assert False, "minimax: nedefinirano stanje igre"
