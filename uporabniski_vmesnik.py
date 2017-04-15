import tkinter    # za uporabniški vmesnik
import argparse   # za argumente iz ukazne vrstice
import logging    # za odpravljanje napak

# Privzeta minimax globina, če je nismo podali ob zagonu v ukazni vrstici
MINIMAX_GLOBINA = 3

from logika_igre import *
from clovek import *
from racunalnik import *


######################################################################


#TODO Mislim da preverjanje poteze včasih ne deluje povsem pravilno(malo "zašteka") vendar sam v kodi ne vidim napake...
# Nujno UNDO. Ali je dovolj, da se v zgodovino shrani samo matrika? Ali potrebujemo tudi seznam izbranih polj? Ta polja so rdeča, tako da se to mogoče vidi že iz matrike?




## Uporabniški vmesnik

class Gui():
    # S to oznako so označeni vsi grafični elementi v self.okno, ki se
    # pobrišejo, ko se začne nova igra (torej, križci in krožci)
    TAG_FIGURA = 'figura'

    # Oznaka za črte
    TAG_OKVIR = 'okvir'

    # Velikost polja
    VELIKOST_POLJA = 50

    #Barve krogcev
    barva_praznih = "white"
    barva_igralca_1 = "yellow"
    barva_igralca_2 = "black"
    


    def __init__(self, master):
        self.igralec_1 = None # Objekt, ki igra X (nastavimo ob začetku igre)
        self.igralec_2 = None # Objekt, ki igra O (nastavimo ob začetku igre)
        self.igra = None
        # Če uporabnik zapre okno naj se poklice self.zapri_okno
        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))

        # Glavni menu
        menu = tkinter.Menu(master)
        master.config(menu=menu) # Dodamo glavni menu v okno

        # Podmenu za izbiro igre
        menu_igra = tkinter.Menu(menu)
        menu.add_cascade(label="Igra", menu=menu_igra)
        #menu_igra.add_command(label="Nova igra",
                              #command=lambda: self.zacni_igro())
        menu_igra.add_command(label="Rumeni=Človek, Črni=Človek",
                              command=lambda: self.zacni_igro(Clovek(self),
                                                              Clovek(self)))
        menu_igra.add_command(label="Rumeni=Človek, Črni=Računalnik",
                              command=lambda: self.zacni_igro(Clovek(self),
                                                              Racunalnik(self, Minimax(MINIMAX_GLOBINA))))
        menu_igra.add_command(label="Rumeni=Računalnik, Črni=Človek",
                              command=lambda: self.zacni_igro(Racunalnik(self, Minimax(MINIMAX_GLOBINA)),
                                                              Clovek(self)))
        menu_igra.add_command(label="Rumeni=Računalnik, Črni=Računalnik",
                              command=lambda: self.zacni_igro(Racunalnik(self, Minimax(MINIMAX_GLOBINA)),
                                                              Racunalnik(self, Minimax(MINIMAX_GLOBINA))))

        
        # Napis, ki prikazuje stanje igre
        self.napis = tkinter.StringVar(master, value="Dobrodošli v Abalone!")
        tkinter.Label(master, textvariable=self.napis).grid(row=0, column=0)

        # Igralno območje
        self.okno = tkinter.Canvas(master, width=11*Gui.VELIKOST_POLJA, height=11*Gui.VELIKOST_POLJA)
        self.okno.grid(row=1, column=0)

        # Črte na igralnem polju
        #self.narisi_crte()
        self.zacetna_pozicija = self.narisi_plosco()
        self.plosca = self.narisi_plosco()[:]
        #TODO to gre v Igra
        self.izbrani = []
        self.premik = False

        # Naročimo se na dogodke
        self.okno.bind("<Button-1>", self.oznacevanje_krogcev)
        self.okno.bind("<Button-3>", self.premik_krogcev)
        #TODO press, release
        #self.okno.bind("<ButtonPress-1>", self.okno_klik)
        #self.okno.bind("<ButtonRelease-1>", self.oznacevanje_krogcev)

        # Prični igro
        self.zacni_igro(Clovek(self), Racunalnik(self, Minimax(MINIMAX_GLOBINA)))

    def narisi_plosco(self):
        self.okno.delete(Gui.TAG_FIGURA)
        d = Gui.VELIKOST_POLJA
        matrika = []
        for x in range(11):
               seznam = []
               for y in range(11):
                   seznam.append(None)
               matrika.append(seznam)
        for i in range(len(matrika)):
            for j in range(len(matrika[i])):
                if (i,j) in [(1, 1), (1, 2), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 1), (4, 2), (4, 3), (5, 1), (5, 2), (5, 3), (6, 2)]:
                    barva = Gui.barva_igralca_1
                elif (i,j) in [(4, 8), (5, 7), (5, 8), (5, 9), (6, 7), (6, 8), (6, 9), (7, 7), (7, 8), (7, 9), (8, 8), (8, 9), (9, 8), (9, 9)]:
                    barva = Gui.barva_igralca_2
                elif (i,j) not in [(6, 1), (7, 1), (8, 1), (9, 1), (7, 2), (8, 2), (9, 2), (8, 3), (9, 3), (9, 4)] and (j,i) not in [(6, 1), (7, 1), (8, 1), (9, 1), (7, 2), (8, 2), (9, 2), (8, 3), (9, 3), (9, 4)] and i != 0 and j != 0 and i != 10 and j != 10:
                    barva = Gui.barva_praznih
                else:
                    barva = None
                if barva is not None:
                    id = self.okno.create_oval((i - j*0.5)*d + 2*d, (3**0.5)*0.5*j*d, (i - j*0.5)*d + 3*d, (3**0.5)*0.5*j*d + d, fill=barva)
                    matrika[i][j] = Polje(id, i, j, barva)             
        return matrika
    
    def oznacevanje_krogcev(self, event):
        i,j = self.poisci_polje(event)
        print((i,j))
        if i is not None and j is not None: #TODO Tu manjka še pogoj, da lahko označimo le krogce igralca, ki je na potezi.
            if self.plosca[i][j].oznacen == False:
                if self.preveri_polje((i,j)):
                    self.okno.itemconfig(self.plosca[i][j].id, fill='red')
                    self.plosca[i][j].oznacen = True
                    self.izbrani.append(self.plosca[i][j])
                    print("oznacil:",self.plosca[i][j])
            elif self.plosca[i][j].oznacen == True:
                self.okno.itemconfig(self.plosca[i][j].id, fill=self.plosca[i][j].barva)
                self.plosca[i][j].oznacen = False
                self.izbrani.remove(self.plosca[i][j])
                print("odznacil:",self.plosca[i][j])

    def premik_krogcev(self, event):
        i,j = self.poisci_polje(event)
        if len(self.izbrani) == 0:
                print("Noben krogec ni izbran")
        else:
            if self.preveri_potezo((i,j)):
                self.premakni_krogce(event)
                self.izbrani = []

                
    # TODO napiši metodo Povleci potezo(zdaj to delno dela okno_klik)
    
    def poisci_polje(self, event):
        """Vrne polje, na katero smo kliknili."""
        d = Gui.VELIKOST_POLJA
        for i in range(11):
            for j in range(11):
                if self.plosca[i][j] is None:
                    continue        # Poskusi naslednji i,j
                sredisce_x = (i - j*0.5)*d + 2.5*d
                sredisce_y = (3**0.5)*0.5*j*d + 0.5*d
                r = ((event.x - sredisce_x)**2 + (event.y - sredisce_y)**2)**0.5
                if r <= d/2:
                    return i,j
        return (None, None)

    def oznaci_krogec(self, p): # Tega nikjer ne uporabiva.
        """Izbrani krogec pobarva rdeče."""
        (i, j) = p
        if i in range(9) and j in range(9):
            self.okno.itemconfig(self.plosca[i][j].id, fill='red')
            self.plosca[i][j].oznacen = True
            print(self.plosca[i][j])


    def odznaci_krogec(self, p): # Tega nikjer ne uporabiva.
        """Obratno kot označi krogec."""
        (i, j) = p         
        self.okno.itemconfig(self.plosca[i][j].id, fill=self.plosca[i][j].barva)
        self.plosca[i][j].oznacen = False
        print(self.plosca[i][j])
        
    #To bi moralo biti v logiki igre in ne tu!
    def preveri_polje(self, p):
        """Pogleda, ali ta krogec lahko izberemo."""
        (i,j) = p
        if i is not None and j is not None and self.plosca[i][j].barva != Gui.barva_praznih:     # Zagotovimo, da smo na plošči in da nismo izbrali praznega polja.
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
        
    #To bi moralo biti v logiki igre in ne tu!
    #TODO Ko pridemo do roba mormao izpodrinjeni krogec poriniti iz plošče
    def preveri_potezo(self, p):
        """Pogleda, ali označene krogce lahko premaknemo na željeno polje."""
        (i,j) = p
        if i is not None and j is not None:     # Zagotovimo, da smo na plošči.
            if self.plosca[i][j].barva == self.izbrani[0].barva:
                print("Ni mogoče premakniti izbranih krogcev na svoje polje!")
                return False
            elif len(self.izbrani) == 1:
                (I1, J1) = (self.izbrani[0].x, self.izbrani[0].y)
                if (i,j) in [(I1, J1 + 1), (I1, J1 - 1), (I1 + 1, J1), (I1 - 1, J1), (I1 + 1, J1 + 1), (I1 - 1, J1 - 1)]: # En krogec lahko premaknemo na katerokoli sosednje prosto polje.
                    return self.plosca[i][j].barva == Gui.barva_praznih
            elif len(self.izbrani) == 2:
                (I1, J1, B) = (self.izbrani[0].x, self.izbrani[0].y, self.izbrani[0].barva)
                (I2, J2) = (self.izbrani[1].x, self.izbrani[1].y)
                orientacija = self.orientacija_izbranih()
                if orientacija == "y":
                    if (i,j) in [(I1, max(J1, J2) + 1),(I1, min(J1, J2) - 1)]:
                        if self.plosca[i][j].barva == Gui.barva_praznih:
                            return True
                        else:
                            return self.potisni(orientacija, p)
                    elif (i,j) in [(I1 + 1, min(J1, J2)),(I1 + 1, max(J1, J2) + 1)]:
                        return self.plosca[i][j].barva == Gui.barva_praznih and self.plosca[I1 + 1][max(J1,J2)].barva == Gui.barva_praznih
                    elif (i,j) in [(I1 - 1, max(J1, J2)),(I1 - 1, min(J1, J2) - 1)]:
                        return self.plosca[i][j].barva == Gui.barva_praznih and self.plosca[I1 - 1][min(J1,J2)].barva == Gui.barva_praznih
                    return False
                elif orientacija == "x":
                    if (i,j) in [(max(I1, I2) + 1, J1),(min(I1, I2) - 1, J1)]:
                        if self.plosca[i][j].barva == Gui.barva_praznih:
                            return True
                        else:
                            return self.potisni(orientacija, p)
                    elif (i,j) in [(max(I1, I2), J1 - 1),(min(I1, I2) - 1, J1 - 1)]:
                        return self.plosca[i][j].barva == Gui.barva_praznih and self.plosca[min(I1,I2)][J1 - 1].barva == Gui.barva_praznih
                    elif (i,j) in [(max(I1, I2) + 1, J1 + 1),(min(I1, I2), J1 + 1)]:
                        return self.plosca[i][j].barva == Gui.barva_praznih and self.plosca[max(I1,I2)][J1 + 1].barva == Gui.barva_praznih
                    return False
                elif orientacija == "diagonala":
                    if (i,j) in [(max(I1, I2) + 1, max(J1, J2) + 1),(min(I1, I2) - 1, min(J1, J2) - 1)]:
                        if self.plosca[i][j].barva == Gui.barva_praznih:
                            return True
                        else:
                            return self.potisni(orientacija, p)
                    elif (i,j) in [(min(I1,I2), min(J1,J2) - 1),(max(I1,I2) + 1, max(J1,J2))]:
                        return self.plosca[i][j].barva == Gui.barva_praznih and self.plosca[max(I1,J2)][min(J1,J2)].barva == Gui.barva_praznih
                    elif (i,j) in [(max(I1,I2), max(J1,J2) + 1),(min(I1,I2) - 1, min(J1,J2))]:
                        #TODO Opazil sem da včasih polje nasprotnikov krogec na polju self.plosca[min(I1,J2)][max(J1,J2)] s premikom na self.plosca[i][j] kar povozimo(kar se ne sme zgoditi) vendar ne vem zakaj
                        return self.plosca[i][j].barva == Gui.barva_praznih and self.plosca[min(I1,J2)][max(J1,J2)].barva == Gui.barva_praznih
                    return False
            elif len(self.izbrani) == 3:
                (I1, J1, B) = (self.izbrani[0].x, self.izbrani[0].y, self.izbrani[0].barva)
                (I2, J2) = (self.izbrani[1].x, self.izbrani[1].y)
                (I3, J3) = (self.izbrani[2].x, self.izbrani[2].y)
                orientacija = self.orientacija_izbranih()
                if orientacija == "y":
                    if (i,j) in [(I1, max(J1, J2, J3) +1),(I1, min(J1, J2, J3) - 1)]:
                        if self.plosca[i][j].barva == Gui.barva_praznih:
                            return True
                        else:
                            return self.potisni(orientacija, p)
                    elif (i,j) in [(I1 - 1, min(J1,J2,J3) - 1),(I1 - 1, max(J1, J2, J3))]:
                        return self.plosca[i][j].barva == Gui.barva_praznih and self.plosca[I1 - 1][min(J1, J2, J3)].barva == Gui.barva_praznih and self.plosca[I1 - 1][min(J1, J2, J3) + 1].barva == Gui.barva_praznih
                    elif (i,j) in [(I1 + 1, min(J1,J2,J3)),(I1 + 1, max(J1, J2, J3) + 1)]:
                        return self.plosca[i][j].barva == Gui.barva_praznih and self.plosca[I1 + 1][max(J1, J2, J3)].barva == Gui.barva_praznih and self.plosca[I1 + 1][min(J1, J2, J3) + 1].barva == Gui.barva_praznih
                    return False
                elif orientacija == "x":
                    if (i,j) in [(max(I1, I2, I3) + 1, J1),(min(I1, I2, I3) - 1, J1)]:
                        if self.plosca[i][j].barva == Gui.barva_praznih:
                            return True
                        else:
                            return self.potisni(orientacija, p)
                    elif (i,j) in [(max(I1,I2,I3), J1 - 1),(min(I1,I2,I3) - 1, J1 - 1)]:
                        return self.plosca[i][j].barva == Gui.barva_praznih and self.plosca[max(I1,I2,I3) - 1][J1 - 1].barva == Gui.barva_praznih and self.plosca[min(I1,I2,I3) + 1][J1 - 1].barva == Gui.barva_praznih
                    elif (i,j) in [(max(I1,I2,I3) + 1, J1 + 1),(min(I1,I2,I3), J1 + 1)]:
                        return self.plosca[i][j].barva == Gui.barva_praznih and self.plosca[max(I1,I2,I3)][J1 + 1].barva == Gui.barva_praznih and self.plosca[min(I1,I2,I3) + 1][J1 + 1].barva == Gui.barva_praznih
                    return False
                elif orientacija == "diagonala":
                    if (i,j) in [(max(I1, I2, I3) + 1, max(J1, J2, J3) + 1),(min(I1, I2, I3) - 1, min(J1, J2, J3) - 1)]:
                        if self.plosca[i][j].barva == Gui.barva_praznih:
                            return True
                    elif (i,j) in [(min(I1, I2, I3), min(J1, J2, J3) - 1),(max(I1, I2, I3) + 1, max(J1, J2, J3))]:
                        return self.plosca[i][j].barva == Gui.barva_praznih and self.plosca[max(I1,I2,I3)][max(J1, J2, J3) - 1].barva == Gui.barva_praznih and self.plosca[min(I1,I2,I3) + 1][min(J1, J2, J3)].barva == Gui.barva_praznih
                    elif (i,j) in [(max(I1, I2, I3), max(J1, J2, J3) + 1),(min(I1, I2, I3) - 1, min(J1, J2, J3))]:
                        return self.plosca[i][j].barva == Gui.barva_praznih and self.plosca[max(I1,I2,I3) - 1][max(J1, J2, J3)].barva == Gui.barva_praznih and self.plosca[min(I1,I2,I3)][min(J1, J2, J3) + 1].barva == Gui.barva_praznih
                    return False
            return False

    def potisni(self, orientacija, p):
        (i,j) = p
        stevilo_oznacenih = len(self.izbrani)
        (stevilo_nasprotnih, ali_izrinemo) = self.stevilo_nasprotnih(orientacija, p)
        if stevilo_nasprotnih is None:
            return False
        elif stevilo_nasprotnih >= stevilo_oznacenih:
            return False
        else:
            B = self.plosca[i][j].barva # ta je potisnjen 
            (j_max, j_min) = (max(krogec.y for krogec in self.izbrani), min(krogec.y for krogec in self.izbrani))
            (i_max, i_min) = (max(krogec.x for krogec in self.izbrani), min(krogec.x for krogec in self.izbrani))
            # Prvi izgine, potem premik kot običajno
            if i in [i_max + 1, i_min - 1] or j in [j_max + 1, j_min - 1]:
                self.plosca[i][j].barva == Gui.barva_praznih
                self.okno.itemconfig(self.plosca[i][j].id, fill= Gui.barva_praznih)
                if ali_izrinemo:
                    return True # TODO tukaj je treba ta izrinjeni krogec dodat v nek seznam oziroma nekam ...
                else:
                    # V bistvu dodaš krogec na konec teh, ki jih rineš.
                    SLOVAR = {"x" : [(i_max + 1, j, i_max + 1 + stevilo_nasprotnih, j), (i_min - 1, j, i_min - (1 + stevilo_nasprotnih), j)],
                              "y" : [(i, j_max + 1, i, j_max + 1 + stevilo_nasprotnih), (i, j_min - 1, i, j_min - (1 + stevilo_nasprotnih))],
                              "diagonala" : [(i_max + 1, j_max + 1, i_max + 1 + stevilo_nasprotnih, j_max + 1 + stevilo_nasprotnih),
                                             (i_min - 1, j_min - 1, i_min - (1 + stevilo_nasprotnih), j_min - (1 + stevilo_nasprotnih))]}
                    for parametri in SLOVAR[orientacija]:
                        if i == parametri[0] and j == parametri[1]:
                            self.plosca[parametri[2]][parametri[3]].barva = B
                            self.okno.itemconfig(self.plosca[parametri[2]][parametri[3]].id, fill=B)
                            break
                    return True
        


    def stevilo_nasprotnih(self, orientacija, p):
        (i,j) = p
        barva = self.plosca[i][j].barva
        (j_max, j_min) = (max(krogec.y for krogec in self.izbrani), min(krogec.y for krogec in self.izbrani))
        (i_max, i_min) = (max(krogec.x for krogec in self.izbrani), min(krogec.x for krogec in self.izbrani))
        SLOVAR = {"x" : [(i_max + 1, j, i + 1, j, i + 2, j),(i_min - 1, j, i - 1, j, i - 2, j)],
                  "y" : [(i, j_max + 1, i, j + 1, i, j + 2),(i, j_min - 1, i, j - 1, i, j - 2)]} # TODO dodati za diagonalno orientacijo
        for parametri in SLOVAR[orientacija]:
            if i == parametri[0] and j == parametri[1]:
                print(parametri)
                if self.plosca[parametri[2]][parametri[3]] is None:
                    return (1, True)
                elif self.plosca[parametri[2]][parametri[3]].barva == Gui.barva_praznih:
                    return (1, False)
                elif self.plosca[parametri[2]][parametri[3]].barva == barva:
                    if self.plosca[parametri[4]][parametri[5]] is None:
                        return (2, True)
                    elif self.plosca[parametri[4]][parametri[5]].barva == Gui.barva_praznih:
                        return (2, False)
##        if orientacija == "x":
##            if i == i_max + 1:
##                if self.plosca[i + 1][j] is None or i + 1 >= 9:
##                    return (1, True)
##                elif self.plosca[i + 1][j].barva == Gui.barva_praznih:
##                    return (1, False)
##                elif self.plosca[i + 1][j].barva == barva:
##                    if self.plosca[i + 2][j].barva is None or i + 2 >= 9:
##                        return (2, True)
##                    elif self.plosca[i + 2][j].barva == Gui.barva_praznih:
##                        return (2, False)
        return None, None
                
                      
         
    
    def premakni_krogce(self, event):
        i,j = self.poisci_polje(event)
        if len(self.izbrani) == 1:
            x = self.izbrani[0].x
            y = self.izbrani[0].y
            barva = self.izbrani[0].barva
            self.plosca[x][y].oznacen = False
            self.okno.itemconfig(self.plosca[x][y].id, fill= Gui.barva_praznih)
            self.plosca[x][y].barva = Gui.barva_praznih
            self.okno.itemconfig(self.plosca[i][j].id, fill= barva)
            self.plosca[i][j].barva = barva
        else:      
            orientacija = self.orientacija_izbranih()
            izbrani = []
            for polje in self.izbrani:
                izbrani.append(Polje(polje.id, polje.x, polje.y, polje.barva))
            for krogec in izbrani:
                self.plosca[krogec.x][krogec.y].oznacen = False
                self.okno.itemconfig(self.plosca[krogec.x][krogec.y].id, fill= Gui.barva_praznih)
                self.plosca[krogec.x][krogec.y].barva = Gui.barva_praznih
            (j_max, j_min, J) = (max(krogec.y for krogec in self.izbrani), min(krogec.y for krogec in self.izbrani), izbrani[0].y)
            (i_max, i_min, I) = (max(krogec.x for krogec in self.izbrani), min(krogec.x for krogec in self.izbrani), izbrani[0].x)
            novi_izbrani = []
            # Ta slovar je nadomestil 18 if-stavkov, ki so si bili zelo podobni. Te if-stavke zdaj pokrije spodnja for-zanka.
            SLOVAR = {"x" : [(i_max, 1, J, 0), (i_max, 0, J, -1), (i_max, 1, J, 1), (i_min, -1, J, 0), (i_min, -1, J, -1), (i_min, 0, J, 1)],
                      "y" : [(I, 0, j_max, 1), (I, 1, j_max, 1), (I, -1, j_max, 0), (I, 0, j_min, -1), (I, 1, j_min, 0), (I, -1, j_min, -1),],
                      "diagonala" : [(i_max, 1, j_max, 1), (i_max, 0, j_max, 1), (i_max, 1, j_max, 0), (i_min, -1, j_min, -1), (i_min, 0, j_min, -1), (i_min, -1, j_min, 0)]}
            for parametri in SLOVAR[orientacija]: 
                if i == parametri[0] + parametri[1] and j == parametri[2] + parametri[3]:
                    for krogec in izbrani:
                        id = krogec.id
                        x = krogec.x + parametri[1]
                        y = krogec.y + parametri[3]
                        barva = krogec.barva
                        novi_izbrani.append(Polje(id, x, y, barva))
                    break
            for krogec in novi_izbrani:
                self.plosca[krogec.x][krogec.y].oznacen = False
                self.okno.itemconfig(self.plosca[krogec.x][krogec.y].id, fill= krogec.barva)
                self.plosca[krogec.x][krogec.y].barva = krogec.barva
        self.oznaceni = []           

    def orientacija_izbranih(self):
        """Pove orientacijo izbranih krogcev. Možne smeri so x, y in diagonala."""
        (I1, J1) = (self.izbrani[0].x, self.izbrani[0].y)
        (I2, J2) = (self.izbrani[1].x, self.izbrani[1].y)
        if J1 == J2:
            return "x"
        elif I1 == I2:
            return "y"
        elif abs(I1 - I2) == 1 and abs(J1 - J2) == 1:
            return "diagonala"
        else:
            return None
        

    def zacni_premik_krogcev(self,event):
        if self.premik is False:
            self.premik = True
        else:
            self.premik = False

    def zacni_igro(self, igralec_1, igralec_2):
        """Nastavi stanje igre na zacetek igre.
           Za igralca uporabi dana igralca."""
        # Ustavimo vsa vlakna, ki trenutno razmišljajo
        #self.prekini_igralce()
        # Pobrišemo tiste, ki so padli dol in narišemo začetno pozicijo
        #self.plosca.delete(Gui.TAG_FIGURA)
        self.zacetna_pozicija
        # Ustvarimo novo igro
        #self.igra = Igra()
        # Shranimo igralce
        #self.igralec_1 = igralec_1
        #self.igralec_2 = igralec_2
        self.napis.set("Na potezi je igralec 1.")
        #self.igralec_1.igraj()

    def koncaj_igro(self, zmagovalec):
        """Nastavi stanje igre na konec igre."""
        if zmagovalec == IGRALEC_1:
            #TODO Prevod barve
            #TODO Nekako bolj razvidno povedati, da je konec igre
            self.napis.set("Zmagal je {} igralec.".format(barva_igralca_1))
        elif zmagovalec == IGRALEC_O:
            self.napis.set("Zmagal je {} igralec.".format(barva_igralca_2))

    def prekini_igralce(self):
        """Sporoči igralcem, da morajo nehati razmišljati."""
        logging.debug ("prekinjam igralce")
        if self.igralec_1: self.igralec_1.prekini()
        if self.igralec_2: self.igralec_3.prekini()


    def zapri_okno(self, master):
        """Ta metoda se pokliče, ko uporabnik zapre aplikacijo."""
        # Kasneje bo tu treba še kaj narediti
        # self.prekini_igralce()
        master.destroy()

    def narisi_crte(self):
        """Nariši črte v igralnem polju"""
        self.okno.delete(Gui.TAG_OKVIR)
        d = Gui.VELIKOST_POLJA
        self.okno.create_line(2.5*d, 0.1*d, 9*d, 0.1*d, tag=Gui.TAG_OKVIR)
        self.okno.create_line(2.5*d, 1*d, 9*d, 1*d, tag=Gui.TAG_OKVIR)
        self.okno.create_line(0*d, 5.5*d, 2.5*d, 1*d, tag=Gui.TAG_OKVIR)
        self.okno.create_line(9*d, 1*d, 11*d, 5.5*d, tag=Gui.TAG_OKVIR)
        
    def prevod_barve(self, barva):
        #TODO To bova dokončala proti koncu projekta, ko bova imela čas se ukvarjati z barvami(saj je to le lepotna izboljšava)
        if barva == "yellow":
            return "rumeni"
        elif barva == "black":
            return "črni"

class Polje:

    def __init__(self, id, x, y, barva=None, oznacen=False):
        self.id = id
        self.x = x
        self.y = y
        self.barva = barva
        self.oznacen = oznacen

    def __repr__(self):
        return 'Polje({0}, ({1}, {2}), {3}, {4})'.format(self.id, self.x, self.y, self.barva, self.oznacen)
    

######################################################################
## Glavni program

# Glavnemu oknu rečemo "root" (koren), ker so grafični elementi
# organizirani v drevo, glavno okno pa je koren tega drevesa

# Ta pogojni stavek preveri, ali smo datoteko pognali kot glavni program in v tem primeru
# izvede kodo. (Načeloma bi lahko datoteko naložili z "import" iz kakšne druge in v tem
# primeru ne bi želeli pognati glavne kode. To je standardni idiom v Pythonu.)

if __name__ == "__main__":
    # Naredimo glavno okno in nastavimo ime
    root = tkinter.Tk()
    root.title("Abalone - Bajc in Jereb")

    # Naredimo objekt razreda Gui in ga spravimo v spremenljivko,
    # sicer bo Python mislil, da je objekt neuporabljen in ga bo pobrisal
    # iz pomnilnika.
    aplikacija = Gui(root)

    # Kontrolo prepustimo glavnemu oknu. Funkcija mainloop neha
    # delovati, ko okno zapremo.
    root.mainloop()
