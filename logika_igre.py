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
    #Barve krogcev
    barva_praznih = "white"
    barva_igralca_1 = "yellow"
    barva_igralca_2 = "black"
    
    def __init__(self):
        self.plosca = self.ustvari_plosco()
        self.na_potezi = IGRALEC_1
        self.zgodovina = []
        self.izbrani = []

    def ustvari_plosco(self):
        #self.okno.delete(gui.TAG_FIGURA)
        matrika = []
        for x in range(11):
               seznam = []
               for y in range(11):
                   seznam.append(None)
               matrika.append(seznam)
        for i in range(len(matrika)):
            for j in range(len(matrika[i])):
                if (i,j) in [(1, 1), (1, 2), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 1), (4, 2), (4, 3), (5, 1), (5, 2), (5, 3), (6, 2)]:
                    barva = Igra.barva_igralca_1
                elif (i,j) in [(4, 8), (5, 7), (5, 8), (5, 9), (6, 7), (6, 8), (6, 9), (7, 7), (7, 8), (7, 9), (8, 8), (8, 9), (9, 8), (9, 9)]:
                    barva = Igra.barva_igralca_2
                elif (i,j) not in [(6, 1), (7, 1), (8, 1), (9, 1), (7, 2), (8, 2), (9, 2), (8, 3), (9, 3), (9, 4)] and (j,i) not in [(6, 1), (7, 1), (8, 1), (9, 1), (7, 2), (8, 2), (9, 2), (8, 3), (9, 3), (9, 4)] and i != 0 and j != 0 and i != 10 and j != 10:
                    barva = Igra.barva_praznih
                else:
                    barva = None
                if barva is not None:
                    matrika[i][j] = Polje(None, i, j, barva)             
        return matrika
    
    def oznacevanje(self, p):
        (i,j) = p
        if i is not None and j is not None: #TODO Tu manjka še pogoj, da lahko označimo le krogce igralca, ki je na potezi.
            if self.plosca[i][j].oznacen == False:
                if self.preveri_polje((i,j)):
                    self.plosca[i][j].oznacen = True
                    self.izbrani.append(self.plosca[i][j])
                    print("oznacil:",self.plosca[i][j])
                    return "oznaci"
            elif self.plosca[i][j].oznacen == True:
                self.plosca[i][j].oznacen = False
                self.izbrani.remove(self.plosca[i][j])
                print("odznacil:",self.plosca[i][j])
                return "odznaci"
            
    def preveri_polje(self, p):
        """Pogleda, ali ta krogec lahko izberemo."""
        (i,j) = p
        if i is not None and j is not None and self.plosca[i][j].barva != Igra.barva_praznih:     # Zagotovimo, da smo na plošči in da nismo izbrali praznega polja.
            if len(self.izbrani) == 0:      # Prvo izbrano polje je lahko katerokoli.
                return True
            elif len(self.izbrani) == 3:      # Izbrana so lahko največ tri polja.
                return False
            else:
                (I1, J1, B1) = (self.izbrani[0].x, self.izbrani[0].y, self.izbrani[0].barva)
                if len(self.izbrani) == 1 and self.plosca[i][j].barva == B1:
                    if p in [(I1,J1+1),(I1,J1-1),(I1+1,J1),(I1-1,J1),(I1-1,J1-1),(I1+1,J1+1)]:
                        return True
                elif len(self.izbrani) == 2 and self.plosca[i][j].barva == B1:
                    (I2, J2, B2) = (self.izbrani[1].x, self.izbrani[1].y, self.izbrani[1].barva)
                    if I1 == I2:
                        if abs(J1 - J2) == 2:
                            if i == I1 and j == (J1 + J2)/2:
                                return True
                        elif p in [(I1, min(J1, J2) - 1),(I1, max(J1, J2) + 1)]:
                            return True
                    elif J1 == J2:
                        if abs(I1 - I2) == 2:
                            if j == J1 and i == (I1 + I2)/2:
                                return True
                        elif p in [(min(I1, I2) - 1 ,J1),(max(I1, I2) + 1,J1)]:
                            return True
                    elif abs(I1 - I2) == 1 and abs(J1 - J2) == 1: # Torej sta sosednja (na diagonali).
                        #if i == (I1 + I2)/2 and j == (J1 + J2)/2:
                        #    return True
                        if p in [(min(I1, I2) - 1, min(J1, J2) - 1),(max(I1, I2) + 1, max(J1, J2) + 1)]:
                            return True
                    elif abs(I1 - I2) == 2 and abs(J1 - J2) == 2: # Med označenima je eno prosto polje (na diagonali).
                        if i == (I1 + I2)/2 and j == (J1 + J2)/2:
                            return True
        else:
            return False

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
    
class Polje:

    def __init__(self, id, x, y, barva=None, oznacen=False):
        self.id = id
        self.x = x
        self.y = y
        self.barva = barva
        self.oznacen = oznacen

    def __repr__(self):
        return 'Polje({0}, ({1}, {2}), {3}, {4})'.format(self.id, self.x, self.y, self.barva, self.oznacen)
    

