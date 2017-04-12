######################################################################
## Igra

IGRALEC_1 = 1
IGRALEC_2 = 2
PRAZNO = "."
NEODLOCENO = "neodločeno"
NI_KONEC = "ni konec"

def nasprotnik(igralec):
    """Vrni nasprotnika od igralca."""
    if igralec == IGRALEC_1:
        return IGRALEC_2
    elif igralec == IGRALEC_2:
        return IGRALEC_1
    else:
        # Do sem ne smemo priti, če pridemo, je napaka v programu.
        # V ta namen ima Python ukaz assert, s katerim lahko preverimo,
        # ali dani pogoj velja. V našem primeru, ko vemo, da do sem
        # sploh ne bi smeli priti, napišemo za pogoj False, tako da
        # bo program crknil, če bo prišel do assert. Spodaj je še nekaj
        # uporab assert, kjer dejansko preverjamo pogoje, ki bi morali
        # veljati. To je zelo uporabno za odpravljanje napak.
        # Assert uporabimo takrat, ko bi program lahko deloval naprej kljub
        # napaki (če bo itak takoj crknil, potem assert ni potreben).
        assert False, "neveljaven nasprotnik"


class Igra():
    def __init__(self):
        self.plosca = [[PRAZNO, PRAZNO, PRAZNO],
                      [PRAZNO, PRAZNO, PRAZNO],
                      [PRAZNO, PRAZNO, PRAZNO]]
        self.na_potezi = IGRALEC_X
        self.zgodovina = []

    def shrani_pozicijo(self):
        """Shrani trenutno pozicijo, da se bomo lahko kasneje vrnili vanjo
           z metodo razveljavi."""
        p = [self.plosca[i][:] for i in range(3)]
        self.zgodovina.append((p, self.na_potezi))

    def kopija(self):
        """Vrni kopijo te igre, brez zgodovine."""
        # Kopijo igre naredimo, ko poženemo na njej algoritem.
        # Če bi algoritem poganjali kar na glavni igri, ki jo
        # uporablja GUI, potem bi GUI mislil, da se menja stanje
        # igre (kdo je na potezi, kdo je zmagal) medtem, ko bi
        # algoritem vlekel poteze
        k = Igra()
        k.plosca = [self.plosca[i][:] for i in range(3)]
        k.na_potezi = self.na_potezi
        return k

    def razveljavi(self):
        """Razveljavi potezo in se vrni v prejšnje stanje."""
        (self.plosca, self.na_potezi) = self.zgodovina.pop()

    def veljavne_poteze(self):
        """Vrni seznam veljavnih potez."""
        poteze = []
        for i in range(3):
            for j in range(3):
                if self.plosca[i][j] is PRAZNO:
                    poteze.append((i,j))
        return poteze

    def povleci_potezo(self, p):
        """Povleci potezo p, ne naredi nič, če je neveljavna.
           Vrne stanje_igre() po potezi ali None, ce je poteza neveljavna."""
        (i,j) = p
        if (self.plosca[i][j] != PRAZNO) or (self.na_potezi == None):
            # neveljavna poteza
            return None
        else:
            self.shrani_pozicijo()
            self.plosca[i][j] = self.na_potezi
            (zmagovalec, trojka) = self.stanje_igre()
            if zmagovalec == NI_KONEC:
                # Igre ni konec, zdaj je na potezi nasprotnik
                self.na_potezi = nasprotnik(self.na_potezi)
            else:
                # Igre je konec
                self.na_potezi = None
            return (zmagovalec, trojka)

    # Tabela vseh trojk, ki nastopajo v igralnem polju
    trojke = [
        # Vodoravne
        [(0,0), (0,1), (0,2)],
        [(1,0), (1,1), (1,2)],
        [(2,0), (2,1), (2,2)],
        # Navpične
        [(0,0), (1,0), (2,0)],
        [(0,1), (1,1), (2,1)],
        [(0,2), (1,2), (2,2)],
        # Diagonali
        [(0,0), (1,1), (2,2)],
        [(0,2), (1,1), (2,0)]
    ]

    def stanje_igre(self):
        """Ugotovi, kakšno je trenutno stanje igre. Vrne:
           - (IGRALEC_X, trojka), če je igre konec in je zmagal IGRALEC_X z dano zmagovalno trojko
           - (IGRALEC_O, trojka), če je igre konec in je zmagal IGRALEC_O z dano zmagovalno trojko
           - (NEODLOCENO, None), če je igre konec in je neodločeno
           - (NI_KONEC, None), če igre še ni konec
        """
        for t in Igra.trojke:
            ((i1,j1),(i2,j2),(i3,j3)) = t
            p = self.plosca[i1][j1]
            if p != PRAZNO and p == self.plosca[i2][j2] == self.plosca[i3][j3]:
                # Našli smo zmagovalno trojko
                return (p, [t[0], t[1], t[2]])
        # Ni zmagovalca, ali je igre konec?
        for i in range(3):
            for j in range(3):
                if self.plosca[i][j] is PRAZNO:
                    # Našli smo prazno plosca, igre ni konec
                    return (NI_KONEC, None)
        # Vsa polja so polna, rezultat je neodločen
        return (NEODLOCENO, None)
