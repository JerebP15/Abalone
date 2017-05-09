######################################################################
## Igra

IGRALEC_1 = 1
IGRALEC_2 = 2
PRAZNO = "."
NI_KONEC = "ni konec"

def nasprotnik(igralec):
    """Vrni nasprotnika danega igralca."""
    if igralec == IGRALEC_1:
        return IGRALEC_2
    elif igralec == IGRALEC_2:
        return IGRALEC_1
    else:
        assert False, "neveljaven nasprotnik"
######################################################################################################

class Igra():

    def __init__(self):
        #Barve krogcev
        self.barva_praznih = "white"
        self.barva_igralca_1 = "yellow"
        self.barva_igralca_2 = "black"
        self.barva_izbranih = "red"

        self.plosca = self.ustvari_plosco()
        self.na_potezi = IGRALEC_2
        self.zgodovina = []
        self.izbrani = []
        self.spremembe_premik = []
        self.izpodrinjeni = [] #Pri izpodrivanju sem dodamo krogce, ki so padli iz plošče, da jih nato gui nariše v posebna stolpca

    def pripadajoca_barva(self, igralec):
        if igralec == IGRALEC_1:
            return self.barva_igralca_1
        elif igralec == IGRALEC_2:
            return self.barva_igralca_2
        else:
            assert False

    def ustvari_plosco(self):
        """Ustvari matriko z elementi iz razreda Polje (na mestih, kjer bodo polja igralne plošče)
        in None (v zgornjem desnem kotu, v spodnjem levem kotu in na robu matrike)."""
        matrika = []
        for x in range(11):
               seznam = []
               for y in range(11):
                   seznam.append(None)
               matrika.append(seznam)
        for i in range(len(matrika)):
            for j in range(len(matrika[i])):
                if (i,j) in [(1, 1), (1, 2), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 1), (4, 2), (4, 3), (5, 1), (5, 2), (5, 3), (6, 2)]:
                    barva = self.barva_igralca_1
                elif (i,j) in [(4, 8), (5, 7), (5, 8), (5, 9), (6, 7), (6, 8), (6, 9), (7, 7), (7, 8), (7, 9), (8, 8), (8, 9), (9, 8), (9, 9)]:
                    barva = self.barva_igralca_2
                elif (i,j) not in [(6, 1), (7, 1), (8, 1), (9, 1), (7, 2), (8, 2), (9, 2), (8, 3), (9, 3), (9, 4)] and (j,i) not in [(6, 1), (7, 1), (8, 1), (9, 1), (7, 2), (8, 2), (9, 2), (8, 3), (9, 3), (9, 4)] and i != 0 and j != 0 and i != 10 and j != 10:
                    barva = self.barva_praznih
                else:
                    barva = None
                if barva is not None:
                    matrika[i][j] = barva
        return matrika

    def prebarvaj_krogce(self, igralec, barva):
        """Zamenja barvo krogcev kot smo kliknili."""
        for i in range(len(self.plosca)):
            for j in range(len(self.plosca[i])):
                if self.plosca[i][j] == self.pripadajoca_barva(igralec):
                    self.plosca[i][j] = barva
        for x in range(len(self.izpodrinjeni)):
            if self.izpodrinjeni[x] == self.pripadajoca_barva(igralec):
                self.izpodrinjeni[x] = barva

    def oznacevanje(self, p, igralec):
        """Doda oznacen krogec v seznam izbranih self.izbrani. Vrne True, če je krogec možno izbrati in False sicer."""
        (i,j) = p
        if i is not None and j is not None and self.plosca[i][j] == self.pripadajoca_barva(igralec):
            if p in self.izbrani:
                self.izbrani.remove(p)
                return "odznaci"
            if p not in self.izbrani and self.preveri_polje(p):
                self.izbrani.append(p)
                return "oznaci"
        #return False

    def preveri_polje(self, p):
        """Pogleda, ali lahko izberemo krogec na mestu p. Vrne True, če je to mogoče, in False, če ni."""
        (i,j) = p
        if i is not None and j is not None and self.plosca[i][j] != self.barva_praznih:     # Zagotovimo, da smo na plošči in da nismo izbrali praznega polja.
            if len(self.izbrani) == 0:      # Prvo izbrano polje je lahko katerokoli.
                return True
            elif len(self.izbrani) == 3:      # Izbrana so lahko največ tri polja.
                return False
            else:
                (I1, J1) = (self.izbrani[0])
                B1 = self.plosca[I1][J1]
                if len(self.izbrani) == 1 and self.plosca[i][j] == B1:
                    if p in [(I1,J1+1),(I1,J1-1),(I1+1,J1),(I1-1,J1),(I1-1,J1-1),(I1+1,J1+1)]:
                        return True
                elif len(self.izbrani) == 2 and self.plosca[i][j] == B1:
                    (I2, J2) = (self.izbrani[1])
                    B2 = self.plosca[I2][J2]
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
                        if p in [(min(I1, I2) - 1, min(J1, J2) - 1),(max(I1, I2) + 1, max(J1, J2) + 1)]:
                            return True
                    elif abs(I1 - I2) == 2 and abs(J1 - J2) == 2: # Med označenima je eno prosto polje (na diagonali).
                        if i == (I1 + I2)/2 and j == (J1 + J2)/2:
                            return True
        else:
            return False

    def premikanje(self, p):
        """Pokliče preveri_potezo.
        Če je poteza dovoljena, spremeni matriko, shrani pozicijo in
        vrne seznam z dvema elementoma - seznamom premaknjenih krogcev in seznamom izpodrinjenih."""
        if len(self.izbrani) == 0:
            tkinter.messagebox.showwarning("Premik ni možen","Noben krogec ni izbran")
            return (None, None)
        else:
            self.shrani_pozicijo()
            if self.preveri_potezo(p):                
                self.premakni_krogce(p)
                spremembe = [self.spremembe_premik[:],self.izpodrinjeni[:]] 
                self.izbrani = []
                # self.shrani_pozicijo()
            else:
                spremembe = (None, None)
            self.spremembe_premik = []
            return spremembe

    def preveri_potezo(self, p):
        """Pogleda, ali označene krogce (iz self.izbrani) lahko premaknemo na željeno polje (p).
        Vrne True ali False glede na to, ali je premik mogoč.
        V primeru, da so na polju p nasprotnikovi krogci, kliče metodo potisni."""
        (i,j) = p
        if i is not None and j is not None and len(self.izbrani) != 0:     # Zagotovimo, da smo na plošči.
            (I1, J1) = (self.izbrani[0])
            B = self.plosca[I1][J1]
            if self.plosca[i][j] == B:
                tkinter.messagebox.showwarning("Premik ni možen","Ni mogoče premakniti izbranih krogcev na svoje polje!")
                return False
            elif len(self.izbrani) == 1:
                if (i,j) in [(I1, J1 + 1), (I1, J1 - 1), (I1 + 1, J1), (I1 - 1, J1), (I1 + 1, J1 + 1), (I1 - 1, J1 - 1)]: # En krogec lahko premaknemo na katerokoli sosednje prosto polje.
                    return self.plosca[i][j] == self.barva_praznih
            elif len(self.izbrani) == 2:
                (I2, J2) = (self.izbrani[1])
                orientacija = self.orientacija_izbranih()
                if abs(I1 - I2) == 1 or abs(J1 - J2) == 1 or (abs(I1 - I2) == 1 and abs(J1 - J2) == 1):
                    if orientacija == "y":
                        if (i,j) in [(I1, max(J1, J2) + 1),(I1, min(J1, J2) - 1)]:
                            if self.plosca[i][j] == self.barva_praznih:
                                return True
                            else:
                                return self.potisni(orientacija, p)
                        elif (i,j) in [(I1 + 1, min(J1, J2)),(I1 + 1, max(J1, J2) + 1)]:
                            return self.plosca[i][j] == self.barva_praznih and self.plosca[I1 + 1][max(J1,J2)] == self.barva_praznih
                        elif (i,j) in [(I1 - 1, max(J1, J2)),(I1 - 1, min(J1, J2) - 1)]:
                            return self.plosca[i][j] == self.barva_praznih and self.plosca[I1 - 1][min(J1,J2)] == self.barva_praznih
                        return False
                    elif orientacija == "x":
                        if (i,j) in [(max(I1, I2) + 1, J1),(min(I1, I2) - 1, J1)]:
                            if self.plosca[i][j] == self.barva_praznih:
                                return True
                            else:
                                return self.potisni(orientacija, p)
                        elif (i,j) in [(max(I1, I2), J1 - 1),(min(I1, I2) - 1, J1 - 1)]:
                            return self.plosca[i][j] == self.barva_praznih and self.plosca[min(I1,I2)][J1 - 1] == self.barva_praznih
                        elif (i,j) in [(max(I1, I2) + 1, J1 + 1),(min(I1, I2), J1 + 1)]:
                            return self.plosca[i][j] == self.barva_praznih and self.plosca[max(I1,I2)][J1 + 1] == self.barva_praznih
                        return False
                    elif orientacija == "diagonala":
                        if (i,j) in [(max(I1, I2) + 1, max(J1, J2) + 1),(min(I1, I2) - 1, min(J1, J2) - 1)]:
                            if self.plosca[i][j] == self.barva_praznih:
                                return True
                            else:
                                return self.potisni(orientacija, p)
                        elif (i,j) in [(min(I1,I2), min(J1,J2) - 1),(max(I1,I2) + 1, max(J1,J2))]:
                            return self.plosca[i][j] == self.barva_praznih and self.plosca[max(I1,I2)][min(J1,J2)] == self.barva_praznih
                        elif (i,j) in [(max(I1,I2), max(J1,J2) + 1),(min(I1,I2) - 1, min(J1,J2))]:
                            return self.plosca[i][j] == self.barva_praznih and self.plosca[min(I1,I2)][max(J1,J2)] == self.barva_praznih
                        return False
            elif len(self.izbrani) == 3:
                (I2, J2) = (self.izbrani[1])
                (I3, J3) = (self.izbrani[2])
                orientacija = self.orientacija_izbranih()
                if orientacija == "y":
                    if (i,j) in [(I1, max(J1, J2, J3) +1),(I1, min(J1, J2, J3) - 1)]:
                        if self.plosca[i][j] == self.barva_praznih:
                            return True
                        else:
                            return self.potisni(orientacija, p)
                    elif (i,j) in [(I1 - 1, min(J1,J2,J3) - 1),(I1 - 1, max(J1, J2, J3))]:
                        return self.plosca[i][j] == self.barva_praznih and self.plosca[I1 - 1][min(J1, J2, J3)] == self.barva_praznih and self.plosca[I1 - 1][min(J1, J2, J3) + 1] == self.barva_praznih
                    elif (i,j) in [(I1 + 1, min(J1,J2,J3)),(I1 + 1, max(J1, J2, J3) + 1)]:
                        return self.plosca[i][j] == self.barva_praznih and self.plosca[I1 + 1][max(J1, J2, J3)] == self.barva_praznih and self.plosca[I1 + 1][min(J1, J2, J3) + 1] == self.barva_praznih
                    return False
                elif orientacija == "x":
                    if (i,j) in [(max(I1, I2, I3) + 1, J1),(min(I1, I2, I3) - 1, J1)]:
                        if self.plosca[i][j] == self.barva_praznih:
                            return True
                        else:
                            return self.potisni(orientacija, p)
                    elif (i,j) in [(max(I1,I2,I3), J1 - 1),(min(I1,I2,I3) - 1, J1 - 1)]:
                        return self.plosca[i][j] == self.barva_praznih and self.plosca[max(I1,I2,I3) - 1][J1 - 1] == self.barva_praznih and self.plosca[min(I1,I2,I3) + 1][J1 - 1] == self.barva_praznih
                    elif (i,j) in [(max(I1,I2,I3) + 1, J1 + 1),(min(I1,I2,I3), J1 + 1)]:
                        return self.plosca[i][j] == self.barva_praznih and self.plosca[max(I1,I2,I3)][J1 + 1] == self.barva_praznih and self.plosca[min(I1,I2,I3) + 1][J1 + 1] == self.barva_praznih
                    return False
                elif orientacija == "diagonala":
                    if (i,j) in [(max(I1, I2, I3) + 1, max(J1, J2, J3) + 1),(min(I1, I2, I3) - 1, min(J1, J2, J3) - 1)]:
                        if self.plosca[i][j] == self.barva_praznih:
                            return True
                        else:
                            return self.potisni(orientacija, p)
                    elif (i,j) in [(min(I1, I2, I3), min(J1, J2, J3) - 1),(max(I1, I2, I3) + 1, max(J1, J2, J3))]:
                        return self.plosca[i][j] == self.barva_praznih and self.plosca[max(I1,I2,I3)][max(J1, J2, J3) - 1] == self.barva_praznih and self.plosca[min(I1,I2,I3) + 1][min(J1, J2, J3)] == self.barva_praznih
                    elif (i,j) in [(max(I1, I2, I3), max(J1, J2, J3) + 1),(min(I1, I2, I3) - 1, min(J1, J2, J3))]:
                        return self.plosca[i][j] == self.barva_praznih and self.plosca[max(I1,I2,I3) - 1][max(J1, J2, J3)] == self.barva_praznih and self.plosca[min(I1,I2,I3)][min(J1, J2, J3) + 1] == self.barva_praznih
                    return False
            return False

    def premakni_krogce(self, p):
        """Popravi matriko, da ustreza stanju po premiku krogcev. Izbriše elemente iz self.izbrani."""
        (i,j) = p
        if len(self.izbrani) == 1:
            (x,y) = self.izbrani[0]
            barva = self.plosca[x][y]
            self.plosca[x][y] = self.barva_praznih
            self.plosca[i][j] = barva
            self.spremembe_premik.append((x,y,self.barva_praznih))
            self.spremembe_premik.append((i,j,barva))
        else:
            orientacija = self.orientacija_izbranih()
            izbrani = []
            barva = self.plosca[self.izbrani[0][0]][self.izbrani[0][1]]
            for (x,y) in self.izbrani:
                izbrani.append((x,y))
            for (xx,yy) in izbrani:
                self.plosca[xx][yy] = self.barva_praznih
                self.spremembe_premik.append((xx,yy,self.barva_praznih))
            (i_max, i_min) = (max(x for (x,y) in self.izbrani), min(x for (x,y) in self.izbrani))
            (j_max, j_min) = (max(y for (x,y) in self.izbrani), min(y for (x,y) in self.izbrani))
            (I,J) = self.izbrani[0]
            novi_izbrani = []
            SLOVAR = {"x" : [(i_max, 1, J, 0), (i_max, 0, J, -1), (i_max, 1, J, 1), (i_min, -1, J, 0), (i_min, -1, J, -1), (i_min, 0, J, 1)],
                      "y" : [(I, 0, j_max, 1), (I, 1, j_max, 1), (I, -1, j_max, 0), (I, 0, j_min, -1), (I, 1, j_min, 0), (I, -1, j_min, -1),],
                      "diagonala" : [(i_max, 1, j_max, 1), (i_max, 0, j_max, 1), (i_max, 1, j_max, 0), (i_min, -1, j_min, -1), (i_min, 0, j_min, -1), (i_min, -1, j_min, 0)]}
            for parametri in SLOVAR[orientacija]:
                if i == parametri[0] + parametri[1] and j == parametri[2] + parametri[3]:
                    for (xx,yy) in izbrani:
                        x = xx + parametri[1]
                        y = yy + parametri[3]
                        novi_izbrani.append((x,y))
                    break
            for (xxx,yyy) in novi_izbrani:
                self.plosca[xxx][yyy] = barva
                self.spremembe_premik.append((xxx,yyy,barva))
        self.izbrani = []

    def orientacija_izbranih(self):
        """Vrne 'x', 'y' ali 'diagonala' glede na položaj krogcev iz self.izbrani v matriki."""
        (I1, J1) = (self.izbrani[0])
        (I2, J2) = (self.izbrani[1])
        if J1 == J2:
            return "x"
        elif I1 == I2:
            return "y"
        elif abs(I1 - I2) == 1 and abs(J1 - J2) == 1:
            return "diagonala"
        else:
            return None

    def potisni(self, orientacija, p):
        """Kliče self.stevilo_nasprotnih in preveri, ali nasprotnikove krogce lahko potisnemo s premikom na p.
        Vrne False, če potisk ni mogoč. V nasprotnem primeru vrne True in popravi matriko tako, da ustreza potezi.
        Če nasprotnikov krogec izrinemo iz plošče, ga doda v seznam izrinjenih."""
        (i,j) = p
        stevilo_izbranih = len(self.izbrani)
        (stevilo_nasprotnih, ali_izrinemo) = self.stevilo_nasprotnih(orientacija, p)
        if stevilo_nasprotnih is None:
            return False
        elif stevilo_nasprotnih >= stevilo_izbranih:
            return False
        else:
            B = self.plosca[i][j] # ta je potisnjen
            (i_max, i_min) = (max(x for (x,y) in self.izbrani), min(x for (x,y) in self.izbrani))
            (j_max, j_min) = (max(y for (x,y) in self.izbrani), min(y for (x,y) in self.izbrani))
            # Prvi izgine, potem premik kot običajno
            if i in [i_max + 1, i_min - 1] or j in [j_max + 1, j_min - 1]:
                self.plosca[i][j] == self.barva_praznih
                self.spremembe_premik.append((i,j,self.barva_praznih))
                if ali_izrinemo:
                    self.izpodrinjeni.append(B)
                    return True
                else:
                    # V bistvu dodaš krogec na konec teh, ki jih rineš.
                    SLOVAR = {"x" : [(i_max + 1, j, i_max + 1 + stevilo_nasprotnih, j), (i_min - 1, j, i_min - (1 + stevilo_nasprotnih), j)],
                              "y" : [(i, j_max + 1, i, j_max + 1 + stevilo_nasprotnih), (i, j_min - 1, i, j_min - (1 + stevilo_nasprotnih))],
                              "diagonala" : [(i_max + 1, j_max + 1, i_max + 1 + stevilo_nasprotnih, j_max + 1 + stevilo_nasprotnih),
                                             (i_min - 1, j_min - 1, i_min - (1 + stevilo_nasprotnih), j_min - (1 + stevilo_nasprotnih))]}
                    for parametri in SLOVAR[orientacija]:
                        if i == parametri[0] and j == parametri[1]:
                            self.plosca[parametri[2]][parametri[3]] = B
                            self.spremembe_premik.append((parametri[2],parametri[3],B))
                            break
                    return True

    def stevilo_nasprotnih(self, orientacija, p):
        """Vrne par - število nasprotnikovih krogcev v smeri premika in
        True oziroma False glede na to, ali je potisk krogcev mogoč. Če ni, vrne (None, None)."""
        (i,j) = p
        barva = self.plosca[i][j]
        (i_max, i_min) = (max(x for (x,y) in self.izbrani), min(x for (x,y) in self.izbrani))
        (j_max, j_min) = (max(y for (x,y) in self.izbrani), min(y for (x,y) in self.izbrani))
        SLOVAR = {"x" : [(i_max + 1, j, i + 1, j, i + 2, j),(i_min - 1, j, i - 1, j, i - 2, j)],
                  "y" : [(i, j_max + 1, i, j + 1, i, j + 2),(i, j_min - 1, i, j - 1, i, j - 2)],
                  "diagonala" : [(i_max + 1, j_max + 1, i + 1, j + 1, i + 2, j + 2),(i_min - 1, j_min - 1, i - 1, j - 1, i - 2, j - 2)]}
        for parametri in SLOVAR[orientacija]:
            if i == parametri[0] and j == parametri[1]:
                if self.plosca[parametri[2]][parametri[3]] is None:
                    return (1, True)
                elif self.plosca[parametri[2]][parametri[3]] == self.barva_praznih:
                    return (1, False)
                elif self.plosca[parametri[2]][parametri[3]] == barva:
                    if self.plosca[parametri[4]][parametri[5]] is None:
                        return (2, True)
                    elif self.plosca[parametri[4]][parametri[5]] == self.barva_praznih:
                        return (2, False)
        return None, None

    def shrani_pozicijo(self):
        """Shrani trenutno pozicijo, da se bomo lahko kasneje vrnili vanjo
           z metodo razveljavi."""
        p = [self.plosca[i][:] for i in range(11)]
        self.zgodovina.append((p, self.na_potezi, self.izpodrinjeni[:]))

    def razveljavi(self):
        """Razveljavi potezo in se vrni v prejšnje stanje."""
        (self.plosca1, self.na_potezi1, self.izpodrinjeni1) = self.zgodovina.pop()
        (self.plosca, self.na_potezi, self.izpodrinjeni) = self.zgodovina.pop()
        return (self.plosca, self.na_potezi, self.izpodrinjeni)

    def kopija(self):
        """Vrni kopijo te igre, brez zgodovine."""
        # Kopijo igre naredimo, ko poženemo na njej algoritem.
        k = Igra()
        k.plosca = [self.plosca[i][:] for i in range(11)]
        k.na_potezi = self.na_potezi
        return k

    def veljavne_poteze(self):
        """ Vrne seznam veljavnih potez v naslednji obliki: [(možni izbrani krogci), možen premik].
        Možni označeni krogci so predstavljeni s koordinatami na plošči,
        možen premik pa je polje p = (i,j), kamor se označeni krogci lahko prestavijo.
        """
        poteze = []
        slovar = self.mozni_izbrani_z_vsemi_sosedi()
        for izbor in slovar:
            # Najprej pogledamo, ali je izbran le en krogec.
            if type(izbor[0]) == int:
                (x,y) = izbor
                self.izbrani.append(izbor)
            # Sicer sta izbrana dva ali trije krogce, v tem primeru vsakega posebej dodamo v self.izbrani.
            else:
                for (x,y) in izbor:
                    self.izbrani.append((x,y))
            # Zdaj preverimo, ali lahko izbrane krogce premaknemo na katero od sosednjih polj, in veljavne poteze dodamo v slovar.
            for sosed in slovar[izbor]:
                if self.preveri_potezo(sosed):
                    poteze.append([izbor, sosed])
            # Pobrišemo self.izbrani, ker smo preverjanje za ta izbor krogcev zaključili.
            self.izbrani = []
        return poteze

    def mozni_izbrani_z_vsemi_sosedi(self):
        """ Vrne slovar, katerega ključi so vsi možni izbrani krogci (en, dva ali trije),
        vrednosti pa so vsa polja, kamor bi se lahko premaknili (ne preverimo še, ali bi bil tak premik
        veljavna poteza). Takih polj je kvečjemu 6.
        """
        nepreverjeni_sosedje = {} # Ta slovar želimo imeti.
        mozni_izbrani = self.mozni_izbrani()
        for moznost in mozni_izbrani:
            # Poiščemo 6 polj, kamor bi se teoretično lahko premaknili.
            # Če je izbran samo en krogec, so to kar vsi sosedje,
            # sicer pa so koordinate odvisne od orientacije.
            if type(moznost[0]) == int:
                # Izbran je le en krogec.
                (i,j) = moznost
                sosedi = [(i + 1, j), (i - 1, j), (i, j +1), (i, j - 1), (i + 1, j + 1), (i - 1, j - 1)]
            elif type(moznost[0]) == tuple:
                # Izbrana sta dva ali trije krogci.
                for (x,y) in moznost:
                    self.izbrani.append((x,y))
                (i_max, i_min, i) = (max(x for (x,y) in moznost), min(x for (x,y) in moznost), moznost[0][0])
                (j_max, j_min, j) = (max(y for (x,y) in moznost), min(y for (x,y) in moznost), moznost[0][1])
                slovar_sosedov = {"x" : [(i_max + 1, j), (i_min - 1, j), (i_max, j - 1), (i_max + 1, j + 1), (i_min - 1, j - 1), (i_min, j + 1)],
                                  "y" : [(i, j_max + 1), (i, j_min - 1), (i - 1, j_max), (i + 1, j_max + 1), (i - 1, j_min - 1), (i + 1, j_min)],
                                  "diagonala" : [(i_max + 1, j_max + 1), (i_max + 1, j_max), (i_max, j_max + 1), (i_min - 1, j_min - 1), (i_min - 1, j_min), (i_min, j_min - 1)]}
                orientacija = self.orientacija_izbranih()
                sosedi = slovar_sosedov[orientacija]
                self.izbrani = []
            for sosed in sosedi:
                (x,y) = sosed
                if self.plosca[x][y] is not None:
                    # V tem primeru dodamo v slovar pod ključ 'moznost' vrednost 'sosed'.
                    # Kasneje bomo preverili, ali je poteza veljavna (None moramo vseeno izločiti,
                    # ker metoda preveri_potezo ne deluje za None).
                    if moznost not in nepreverjeni_sosedje:
                        nepreverjeni_sosedje[moznost] = [sosed]
                    else:
                        nepreverjeni_sosedje[moznost] += [sosed]
        return nepreverjeni_sosedje

    def mozne_enice(self):
        """ Vrne seznam koordinat vseh posameznih krogcev igralca na potezi.
        Oblika seznama: [(x1,y1), (x2,y2), ...]
        """
        seznam = []
        for i in range(1,10):
            for j in range(1,10):
                if self.plosca[i][j] is not None:
                    if self.plosca[i][j] == self.pripadajoca_barva(self.na_potezi):
                        seznam.append((i,j))
        return seznam

    def mozne_dvojice(self):
        """ Vrne seznam koordinat vseh parov krogcev (torej brez enic), ki bi jih lahko izbral igralec na potezi.
        Vsak par nastopi samo enkrat.
        Oblika seznama: [((x1,y1),(x2,y2)), ((x3,y3),(x4,y4))...]
        """
        dvojice = []
        enice = self.mozne_enice()
        for (i,j) in enice:
            barva = self.plosca[i][j]
            sosedi = [(i + 1, j), (i - 1, j), (i, j +1), (i, j - 1), (i + 1, j + 1), (i - 1, j - 1)]
            for (x,y) in sosedi:
                if self.plosca[x][y] is not None and self.plosca[x][y] == barva:
                    par = ((i,j),(x,y))
                    obratni_par = ((x,y),(i,j))
                    if par not in dvojice and obratni_par not in dvojice:
                        dvojice.append(par)
        return dvojice

    def mozni_izbrani(self):
        """ Vrne seznam koordinat vseh možnih izborov krogcev (enega, dveh ali treh).
        Vsak izbor nastopi samo enkrat.
        Oblika seznama: [((x1,y1),(x2,y2)), ((x3,y3),(x4,y4)), (x5,y5), ((x6,y6),(x7,y7),(x8,y8))...]
        """
        trojice = []
        dvojice = self.mozne_dvojice()
        enice = self.mozne_enice()
        for (prvi,drugi) in dvojice:
            self.izbrani = []
            (I1, J1) = prvi
            (I2, J2) = drugi
            self.izbrani.append(prvi)
            self.izbrani.append(drugi)
            orientacija = self.orientacija_izbranih()
            barva = self.plosca[I1][J1]
            slovarcek = {"x" : [(min(I1,I2) - 1, J1),(max(I1, I2) + 1, J1)],
                         "y" : [(I1, min(J1,J2) - 1),(I1, max(J1,J2) + 1)],
                         "diagonala" : [(min(I1,I2) - 1, min(J1,J2) - 1),(max(I1, I2) + 1, max(J1, J2) + 1)]}
            for (x,y) in slovarcek[orientacija]:
                if self.plosca[x][y] is not None and self.plosca[x][y] == barva:
                    tretji = (x,y)
                    seznam = [(prvi,drugi,tretji),(tretji, prvi, drugi),(drugi, prvi, tretji),(tretji,drugi,prvi)]
                    if seznam[0] not in trojice and seznam[1] not in trojice and seznam[2] not in trojice and seznam[3] not in trojice:
                        trojice.append(seznam[0])
        self.izbrani = []
        return enice + dvojice + trojice

    def povleci_potezo(self, p):
        """Povleci potezo p, ne naredi nič, če je neveljavna.
           Vrne stanje_igre() po potezi ali None, če je poteza neveljavna."""
        (i,j) = p
        if self.preveri_potezo(p) == False: # Neveljavna poteza
            return None
        else:
            self.shrani_pozicijo()
            zmagovalec = self.stanje_igre()
            if zmagovalec == NI_KONEC:
                self.na_potezi = nasprotnik(self.na_potezi)
            else:
                self.na_potezi = None
            return zmagovalec

    def stanje_igre(self):
        """Ugotovi, kakšno je trenutno stanje igre. Vrne:
           - IGRALEC_1, če je igre konec in je zmagal IGRALEC_1 (izrinil je 6 nasprotnikovih kroglic s plošče),
           - IGRALEC_2, če je igre konec in je zmagal IGRALEC_2 (izrinil je 6 nasprotnikovih kroglic s plošče),
           - NI_KONEC, če igre še ni konec.
        """
        kroglice_prvega = 0
        kroglice_drugega = 0
        for barva in self.izpodrinjeni:
            if barva == self.barva_igralca_1:
                kroglice_prvega += 1
            else:
                kroglice_drugega += 1
        if kroglice_prvega == 6:
            return IGRALEC_2
        elif kroglice_drugega == 6:
            return IGRALEC_1
        else:
            return NI_KONEC
