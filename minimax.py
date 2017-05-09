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
                smeri.append([None] + x + [None])
            if len(y) != 0:
                smeri.append([None] + y + [None])
        smeri.append([None] + glavna_diagonala + [None])
        zacetki_diagonal = [(1,2),(1,3),(1,4),(1,5)]
        for (i,j) in zacetki_diagonal:
            spodnja_diagonala = []
            zgornja_diagonala = []
            while plosca[i][j] is not None:
                spodnja_diagonala.append(plosca[i][j])
                zgornja_diagonala.append(plosca[j][i])
                i += 1
                j += 1
            smeri.append([None] + spodnja_diagonala + [None])
            smeri.append([None] + zgornja_diagonala + [None])
        pozicije = {
            # Pozicije, kjer smo nasprotnika izrinili s plošče - zelo zelo dobro.
            (None, nasprotnikova_barva, moja_barva, moja_barva) : 3700,
            (None, nasprotnikova_barva, moja_barva, moja_barva, moja_barva) : 3700,
            (None, nasprotnikova_barva, nasprotnikova_barva, moja_barva, moja_barva, moja_barva) : 3900,
            # Pozicije, kjer lahko v naslednji potezi mi izrinemo s plošče - zelo dobro.
            (None, nasprotnikova_barva, moja_barva, moja_barva) : 1700,
            (None, nasprotnikova_barva, moja_barva, moja_barva, moja_barva) : 1700,
            (None, nasprotnikova_barva, nasprotnikova_barva, moja_barva, moja_barva, moja_barva) : 1900,
            # Pozicije, kjer lahko čez 2 potezi izrinemo nasprotnika s plošče - dobro.
            (None, prazno, nasprotnikova_barva, moja_barva, moja_barva) : 1400,
            (None, prazno, nasprotnikova_barva, moja_barva, moja_barva, moja_barva) : 1400,
            (None, prazno, nasprotnikova_barva, nasprotnikova_barva, moja_barva, moja_barva, moja_barva) : 1500,
            (None, nasprotnikova_barva, prazno, moja_barva, moja_barva) : 1400,
            (None, nasprotnikova_barva, prazno, moja_barva, moja_barva, moja_barva) : 1400,
            (None, nasprotnikova_barva, prazno, nasprotnikova_barva, moja_barva, moja_barva, moja_barva) : 1500,
            # Pozicije, kjer so nas izrinili s plošče - zelo zelo slabo.
            (None, moja_barva, nasprotnikova_barva, nasprotnikova_barva) : -3600,
            (None, moja_barva, nasprotnikova_barva, nasprotnikova_barva, nasprotnikova_barva) : -3600,
            (None, moja_barva, moja_barva, nasprotnikova_barva, nasprotnikova_barva, nasprotnikova_barva) : -3800,
           # Pozicije, kjer nas lahko v naslednji potezi izrinejo s plošče - zelo slabo.
            (None, moja_barva, nasprotnikova_barva, nasprotnikova_barva) : -1600,
            (None, moja_barva, nasprotnikova_barva, nasprotnikova_barva, nasprotnikova_barva) : -1600,
            (None, moja_barva, moja_barva, nasprotnikova_barva, nasprotnikova_barva, nasprotnikova_barva) : -1800,
            # Pozicije, kjer nas lahko čez 2 potezi izrinejo s plošče - slabo.
            (None, prazno, moja_barva, nasprotnikova_barva, nasprotnikova_barva) : -1300,
            (None, prazno, moja_barva, nasprotnikova_barva, nasprotnikova_barva, nasprotnikova_barva) : -1300,
            (None, prazno, moja_barva, moja_barva, nasprotnikova_barva, nasprotnikova_barva, nasprotnikova_barva) : -1400,
            (None, moja_barva, prazno, nasprotnikova_barva, nasprotnikova_barva) : -1300,
            (None, moja_barva, prazno, nasprotnikova_barva, nasprotnikova_barva, nasprotnikova_barva) : -1300,
            (None, moja_barva, prazno, moja_barva, nasprotnikova_barva, nasprotnikova_barva, nasprotnikova_barva) : -1400}
        for smer in smeri:
            #Mislim, da zaradi tega sploh ne pride do nekaterih potez v "pozicije". Drugi krogec je namreč prazen in zato vrednosti prišteje 10, ne gre pa v else!!
##            #Nočemo biti na robu
##            if smer[1] == prazno:
##                vrednost += 10
##            if smer[-2] == prazno:
##                vrednost += 10
            if moja_barva not in smer or nasprotnikova_barva not in smer:
                continue
            else:
                for pozicija in pozicije:
                    # Pozicija se lahko pojavi na koncu ali pa na začetku smeri.
                    na_zacetku = len(pozicija)
                    na_koncu = len(pozicija)
                    for i in range(len(pozicija)):
                        if len(pozicija) > len(smer):
                            break
                        if smer[i] == pozicija[i] or smer[-1-i] == pozicija[i]:
                            if smer[i] == pozicija[i]:
                                na_zacetku -= 1
                            elif smer[-1-i] == pozicija[i]:
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
                    print('MAX')
                    # Maksimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = -Minimax.NESKONCNO
                    najboljse_poteze = []
                    s = 0
                    for poteza in self.igra.veljavne_poteze():
                        s += 1
                        [izbrani, p] = poteza
                        if type(izbrani[0]) == int:
                                (x,y) = izbrani
                                self.igra.izbrani.append((x,y))
                        else:
                            for (x,y) in izbrani:
                                self.igra.izbrani.append((x,y))
                        #self.igra.shrani_pozicijo()
                        self.igra.povleci_potezo(p)
                        vrednost = self.minimax(globina-1, not maksimiziramo)[1]
                        #if self.igra.povleci_potezo(p) is not None:
                        self.igra.razveljavi()
                        if vrednost == vrednost_najboljse:
                            najboljse_poteze.append(poteza)
                        elif vrednost > vrednost_najboljse:
                            print('boljse!', vrednost)
                            print('max',s)
                            vrednost_najboljse = vrednost
                            najboljse_poteze = [poteza]
                        self.igra.izbrani = []
                    najboljsa_poteza = random.choice(najboljse_poteze)
                    print('NAJmax:', vrednost)
                else:
                    # Minimiziramo
                    print('MIN')
                    najboljsa_poteza = None
                    vrednost_najboljse = Minimax.NESKONCNO
                    najboljse_poteze = []
                    s = 0
                    for poteza in self.igra.veljavne_poteze():
                        s += 1
                        [izbrani, p] = poteza
                        if type(izbrani[0]) == int:
                                (x,y) = izbrani
                                self.igra.izbrani.append((x,y))
                        else:
                            for (x,y) in izbrani:
                                self.igra.izbrani.append((x,y))
                        self.igra.shrani_pozicijo()
                        self.igra.povleci_potezo(p)
                        vrednost = self.minimax(globina-1, not maksimiziramo)[1]
                        if self.igra.povleci_potezo(p) is not None:
                            self.igra.razveljavi()
                        if vrednost == vrednost_najboljse:
                            najboljse_poteze.append(poteza)
                        elif vrednost < vrednost_najboljse:
                            print('slabse!', vrednost)
                            print('min',s)
                            vrednost_najboljse = vrednost
                            najboljse_poteze = [poteza]
                        self.igra.izbrani = []
                    najboljsa_poteza = random.choice(najboljse_poteze)
                    print('NAJmin:', vrednost)
                assert (najboljsa_poteza is not None), "minimax: izračunana poteza je None"
                return (najboljsa_poteza, vrednost_najboljse)
        else:
            assert False, "minimax: nedefinirano stanje igre"
