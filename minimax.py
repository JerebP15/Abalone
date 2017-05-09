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

    def vrednost_pozicije(self):
        """Ocena vrednosti pozicije na plošči."""
        # Nastavimo vrednost na 0 in definiramo, kar bomo potrebovali.
        vrednost = 0
        plosca = self.igra.plosca
        izpodrinjeni = self.igra.izpodrinjeni
        moja_barva = self.igra.pripadajoca_barva(self.jaz)
        nasprotnikova_barva = self.igra.pripadajoca_barva(nasprotnik(self.jaz))
        prazno = self.igra.barva_praznih
        # Najprej preštejemo svoje in nasprotnikove izpodrinjene krogce (s tem spodbujamo agresivno igro - glej navodila)
        moji_izpodrinjeni = izpodrinjeni.count(moja_barva)
        nasprotnikovi_izpodrinjeni = izpodrinjeni.count(nasprotnikova_barva)
        vrednost += (1000 * moji_izpodrinjeni - 900 * nasprotnikovi_izpodrinjeni)
        # Naredimo seznam "smeri", v katerem bodo vse vrstice, stolpci in diagonale.
        smeri = []
        glavna_diagonala = []
        for i in range(11):
            x = []
            y = []
            if plosca[i][i] is not None:
                glavna_diagonala.append(plosca[i][i])
            for j in range(11):
                if plosca[i][j] is not None:
                    y.append(plosca[i][j])
                if plosca[j][i] is not None:
                    x.append(plosca[j][i])
            if len(x) != 0:
                smeri.append(x)
            if len(y) != 0:
                smeri.append(y)
        smeri.append(glavna_diagonala)
        zacetki_diagonal = [(1,2),(1,3),(1,4),(1,5)]
        for (i,j) in zacetki_diagonal:
            spodnja_diagonala = []
            zgornja_diagonala = []
            while plosca[i][j] is not None:
                spodnja_diagonala.append(plosca[i][j])
                zgornja_diagonala.append(plosca[j][i])
                i += 1
                j += 1
            smeri.append(spodnja_diagonala)
            smeri.append(zgornja_diagonala)

        pozicije = {
            # Pozicije, kjer nas lahko v naslednji potezi izrinejo s plošče - zelo slabo.
            (moja_barva, nasprotnikova_barva, nasprotnikova_barva) : -500,
            (moja_barva, nasprotnikova_barva, nasprotnikova_barva, nasprotnikova_barva) : -500,
            (moja_barva, moja_barva, nasprotnikova_barva, nasprotnikova_barva, nasprotnikova_barva) : -700,
            # Pozicije, kjer nas lahko v naslednji potezi potisnejo do roba - slabo, ampak ne nerešljivo.
            (prazno, moja_barva, nasprotnikova_barva, nasprotnikova_barva) : -300,
            (prazno, moja_barva, nasprotnikova_barva, nasprotnikova_barva, nasprotnikova_barva) : -300,
            (prazno, moja_barva, moja_barva, nasprotnikova_barva, nasprotnikova_barva, nasprotnikova_barva) : -400}
        # Podobno napišemo seznam ugodnih pozicij, ki pa mora imeti manjši učinek na vrednost pozicije
        # (recimo vrednost += 300?), ker se nasprotnik lahko izmakne in zato ni ziher, da ga bomo res izrinili.
        for smer in smeri:
            for pozicija in pozicije:
                # Pozicija se lahko pojavi na koncu ali pa na začetku smeri.
                na_zacetku = len(pozicija)
                na_koncu = len(pozicija)
                for i in range(len(pozicija)):
                    if smer[i] == pozicija[i]:
                        na_zacetku -= 1
                    if smer[-1-i] == pozicija[i]:
                        na_koncu -= 1
                    else:
                        break
                if na_zacetku == 0 and na_koncu == 0:
                    vrednost += 2 * pozicije[pozicija]
                elif na_zacetku == 0 or na_koncu == 0:
                    vrednost += pozicije[pozicija]
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
                        if self.igra.povleci_potezo(p) is not None:
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
