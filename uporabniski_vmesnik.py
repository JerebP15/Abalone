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
    


    def __init__(self, master):
        self.igralec_1 = None # Objekt, ki igra X (nastavimo ob začetku igre)
        self.igralec_2 = None # Objekt, ki igra O (nastavimo ob začetku igre)
        self.igra = Igra()
        # Če uporabnik zapre okno naj se poklice self.zapri_okno
        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))

        # Glavni menu
        menu = tkinter.Menu(master)
        master.config(menu=menu) # Dodamo glavni menu v okno

        # Podmenu za izbiro igre
        menu_igra = tkinter.Menu(menu)
        menu.add_cascade(label="Nova igra", menu=menu_igra)
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
        tkinter.Label(master, textvariable=self.napis).grid(row=0, column=1)

        # Igralno območje
        self.okno = tkinter.Canvas(master, width=11*Gui.VELIKOST_POLJA, height=11*Gui.VELIKOST_POLJA)
        self.okno.grid(row=1, column=1)
        self.polje_izpodrinjenih1 = tkinter.Canvas(master, width=Gui.VELIKOST_POLJA, height=6*Gui.VELIKOST_POLJA)
        self.polje_izpodrinjenih1.grid(row=1, column=0)
        self.polje_izpodrinjenih2 = tkinter.Canvas(master, width=Gui.VELIKOST_POLJA, height=6*Gui.VELIKOST_POLJA)
        self.polje_izpodrinjenih2.grid(row=1, column=2)

        # Črte na igralnem polju
        self.narisi_crte()
        self.plosca = self.igra.plosca
        #TODO to gre v Igra
        self.premik = False

        # Naročimo se na dogodke
        self.okno.bind("<Button-1>", self.oznacevanje_krogcev)
        self.okno.bind("<Button-3>", self.premik_krogcev)
        #TODO press, release
        #self.okno.bind("<ButtonPress-1>", self.okno_klik)
        #self.okno.bind("<ButtonRelease-1>", self.oznacevanje_krogcev)

        # Prični igro
        self.zacni_igro(Clovek(self), Racunalnik(self, Minimax(MINIMAX_GLOBINA)))


    def risi_plosco(self):
        d = Gui.VELIKOST_POLJA
        matrika = self.plosca
        for i in range(len(matrika)):
             for j in range(len(matrika[i])):
                 if matrika[i][j] is not None:
                     id = self.okno.create_oval((i - j*0.5)*d + 2*d, (3**0.5)*0.5*j*d, (i - j*0.5)*d + 3*d, (3**0.5)*0.5*j*d + d, fill=matrika[i][j].barva)
                     matrika[i][j].id = id
                     
    def oznacevanje_krogcev(self, event):
        i,j = self.poisci_polje(event)
        p = (i,j)
        print(p)
        odziv = self.igra.oznacevanje(p)
        if odziv == "oznaci":
            self.oznaci_krogec(p)
        elif odziv == "odznaci":
            self.odznaci_krogec(p)


    def premik_krogcev(self, event):
        i,j = self.poisci_polje(event)
        p = (i,j)
        odziv = self.igra.premikanje(p)
        if odziv is not None:
            for polje in odziv:
                (x,y,barva) = polje
                self.okno.itemconfig(self.plosca[x][y].id, fill = barva)

                
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

    def oznaci_krogec(self, p):
        """Izbrani krogec pobarva rdeče."""
        (i, j) = p
        self.okno.itemconfig(self.plosca[i][j].id, fill='red')
        print(self.plosca[i][j])


    def odznaci_krogec(self, p):
        """Obratno kot označi krogec."""
        (i, j) = p         
        self.okno.itemconfig(self.plosca[i][j].id, fill=self.igra.plosca[i][j].barva)
        print(self.plosca[i][j])
          
##    def preveri_potezo(self, p):
##        """Pogleda, ali označene krogce lahko premaknemo na željeno polje."""
##        (i,j) = p
##        if i is not None and j is not None:     # Zagotovimo, da smo na plošči.
##            if self.plosca[i][j].barva == self.igra.izbrani[0].barva:
##                print("Ni mogoče premakniti izbranih krogcev na svoje polje!")
##                return False
##            elif len(self.igra.izbrani) == 1:
##                (I1, J1) = (self.igra.izbrani[0].x, self.igra.izbrani[0].y)
##                if (i,j) in [(I1, J1 + 1), (I1, J1 - 1), (I1 + 1, J1), (I1 - 1, J1), (I1 + 1, J1 + 1), (I1 - 1, J1 - 1)]: # En krogec lahko premaknemo na katerokoli sosednje prosto polje.
##                    return self.plosca[i][j].barva == self.igra.barva_praznih
##            elif len(self.igra.izbrani) == 2:
##                (I1, J1, B) = (self.igra.izbrani[0].x, self.igra.izbrani[0].y, self.igra.izbrani[0].barva)
##                (I2, J2) = (self.igra.izbrani[1].x, self.igra.izbrani[1].y)
##                orientacija = self.orientacija_izbranih()
##                if abs(I1 - I2) == 1 or abs(J1 - J2) == 1 or (abs(I1 - I2) == 1 and abs(J1 - J2) == 1):
##                    if orientacija == "y":
##                        if (i,j) in [(I1, max(J1, J2) + 1),(I1, min(J1, J2) - 1)]:
##                            if self.plosca[i][j].barva == self.igra.barva_praznih:
##                                return True
##                            else:
##                                return self.potisni(orientacija, p)
##                        elif (i,j) in [(I1 + 1, min(J1, J2)),(I1 + 1, max(J1, J2) + 1)]:
##                            return self.plosca[i][j].barva == self.igra.barva_praznih and self.plosca[I1 + 1][max(J1,J2)].barva == self.igra.barva_praznih
##                        elif (i,j) in [(I1 - 1, max(J1, J2)),(I1 - 1, min(J1, J2) - 1)]:
##                            return self.plosca[i][j].barva == self.igra.barva_praznih and self.plosca[I1 - 1][min(J1,J2)].barva == self.igra.barva_praznih
##                        return False
##                    elif orientacija == "x":
##                        if (i,j) in [(max(I1, I2) + 1, J1),(min(I1, I2) - 1, J1)]:
##                            if self.plosca[i][j].barva == self.igra.barva_praznih:
##                                return True
##                            else:
##                                return self.potisni(orientacija, p)
##                        elif (i,j) in [(max(I1, I2), J1 - 1),(min(I1, I2) - 1, J1 - 1)]:
##                            return self.plosca[i][j].barva == self.igra.barva_praznih and self.plosca[min(I1,I2)][J1 - 1].barva == self.igra.barva_praznih
##                        elif (i,j) in [(max(I1, I2) + 1, J1 + 1),(min(I1, I2), J1 + 1)]:
##                            return self.plosca[i][j].barva == self.igra.barva_praznih and self.plosca[max(I1,I2)][J1 + 1].barva == self.igra.barva_praznih
##                        return False
##                    elif orientacija == "diagonala":
##                        if (i,j) in [(max(I1, I2) + 1, max(J1, J2) + 1),(min(I1, I2) - 1, min(J1, J2) - 1)]:
##                            if self.plosca[i][j].barva == self.igra.barva_praznih:
##                                return True
##                            else:
##                                return self.potisni(orientacija, p)
##                        elif (i,j) in [(min(I1,I2), min(J1,J2) - 1),(max(I1,I2) + 1, max(J1,J2))]:
##                            return self.plosca[i][j].barva == self.igra.barva_praznih and self.plosca[max(I1,J2)][min(J1,J2)].barva == self.igra.barva_praznih
##                        elif (i,j) in [(max(I1,I2), max(J1,J2) + 1),(min(I1,I2) - 1, min(J1,J2))]:    
##                            return self.plosca[i][j].barva == self.igra.barva_praznih and self.plosca[min(I1,J2)][max(J1,J2)].barva == self.igra.barva_praznih
##                        return False
##            elif len(self.igra.izbrani) == 3:
##                (I1, J1, B) = (self.igra.izbrani[0].x, self.igra.izbrani[0].y, self.igra.izbrani[0].barva)
##                (I2, J2) = (self.igra.izbrani[1].x, self.igra.izbrani[1].y)
##                (I3, J3) = (self.igra.izbrani[2].x, self.igra.izbrani[2].y)
##                orientacija = self.orientacija_izbranih()
##                if orientacija == "y":
##                    if (i,j) in [(I1, max(J1, J2, J3) +1),(I1, min(J1, J2, J3) - 1)]:
##                        if self.plosca[i][j].barva == self.igra.barva_praznih:
##                            return True
##                        else:
##                            return self.potisni(orientacija, p)
##                    elif (i,j) in [(I1 - 1, min(J1,J2,J3) - 1),(I1 - 1, max(J1, J2, J3))]:
##                        return self.plosca[i][j].barva == self.igra.barva_praznih and self.plosca[I1 - 1][min(J1, J2, J3)].barva == self.igra.barva_praznih and self.plosca[I1 - 1][min(J1, J2, J3) + 1].barva == self.igra.barva_praznih
##                    elif (i,j) in [(I1 + 1, min(J1,J2,J3)),(I1 + 1, max(J1, J2, J3) + 1)]:
##                        return self.plosca[i][j].barva == self.igra.barva_praznih and self.plosca[I1 + 1][max(J1, J2, J3)].barva == self.igra.barva_praznih and self.plosca[I1 + 1][min(J1, J2, J3) + 1].barva == self.igra.barva_praznih
##                    return False
##                elif orientacija == "x":
##                    if (i,j) in [(max(I1, I2, I3) + 1, J1),(min(I1, I2, I3) - 1, J1)]:
##                        if self.plosca[i][j].barva == self.igra.barva_praznih:
##                            return True
##                        else:
##                            return self.potisni(orientacija, p)
##                    elif (i,j) in [(max(I1,I2,I3), J1 - 1),(min(I1,I2,I3) - 1, J1 - 1)]:
##                        return self.plosca[i][j].barva == self.igra.barva_praznih and self.plosca[max(I1,I2,I3) - 1][J1 - 1].barva == self.igra.barva_praznih and self.plosca[min(I1,I2,I3) + 1][J1 - 1].barva == self.igra.barva_praznih
##                    elif (i,j) in [(max(I1,I2,I3) + 1, J1 + 1),(min(I1,I2,I3), J1 + 1)]:
##                        return self.plosca[i][j].barva == self.igra.barva_praznih and self.plosca[max(I1,I2,I3)][J1 + 1].barva == self.igra.barva_praznih and self.plosca[min(I1,I2,I3) + 1][J1 + 1].barva == self.igra.barva_praznih
##                    return False
##                elif orientacija == "diagonala":
##                    if (i,j) in [(max(I1, I2, I3) + 1, max(J1, J2, J3) + 1),(min(I1, I2, I3) - 1, min(J1, J2, J3) - 1)]:
##                        if self.plosca[i][j].barva == self.igra.barva_praznih:
##                            return True
##                    elif (i,j) in [(min(I1, I2, I3), min(J1, J2, J3) - 1),(max(I1, I2, I3) + 1, max(J1, J2, J3))]:
##                        return self.plosca[i][j].barva == self.igra.barva_praznih and self.plosca[max(I1,I2,I3)][max(J1, J2, J3) - 1].barva == self.igra.barva_praznih and self.plosca[min(I1,I2,I3) + 1][min(J1, J2, J3)].barva == self.igra.barva_praznih
##                    elif (i,j) in [(max(I1, I2, I3), max(J1, J2, J3) + 1),(min(I1, I2, I3) - 1, min(J1, J2, J3))]:
##                        return self.plosca[i][j].barva == self.igra.barva_praznih and self.plosca[max(I1,I2,I3) - 1][max(J1, J2, J3)].barva == self.igra.barva_praznih and self.plosca[min(I1,I2,I3)][min(J1, J2, J3) + 1].barva == self.igra.barva_praznih
##                    return False
##            return False

##    def potisni(self, orientacija, p):
##        (i,j) = p
##        stevilo_oznacenih = len(self.igra.izbrani)
##        (stevilo_nasprotnih, ali_izrinemo) = self.stevilo_nasprotnih(orientacija, p)
##        if stevilo_nasprotnih is None:
##            return False
##        elif stevilo_nasprotnih >= stevilo_oznacenih:
##            return False
##        else:
##            B = self.plosca[i][j].barva # ta je potisnjen 
##            (j_max, j_min) = (max(krogec.y for krogec in self.igra.izbrani), min(krogec.y for krogec in self.igra.izbrani))
##            (i_max, i_min) = (max(krogec.x for krogec in self.igra.izbrani), min(krogec.x for krogec in self.igra.izbrani))
##            # Prvi izgine, potem premik kot običajno
##            if i in [i_max + 1, i_min - 1] or j in [j_max + 1, j_min - 1]:
##                self.plosca[i][j].barva == self.igra.barva_praznih
##                self.okno.itemconfig(self.plosca[i][j].id, fill= self.igra.barva_praznih)
##                if ali_izrinemo:
##                    return True # TODO tukaj je treba ta izrinjeni krogec dodat v nek seznam oziroma nekam ...
##                else:
##                    # V bistvu dodaš krogec na konec teh, ki jih rineš.
##                    SLOVAR = {"x" : [(i_max + 1, j, i_max + 1 + stevilo_nasprotnih, j), (i_min - 1, j, i_min - (1 + stevilo_nasprotnih), j)],
##                              "y" : [(i, j_max + 1, i, j_max + 1 + stevilo_nasprotnih), (i, j_min - 1, i, j_min - (1 + stevilo_nasprotnih))],
##                              "diagonala" : [(i_max + 1, j_max + 1, i_max + 1 + stevilo_nasprotnih, j_max + 1 + stevilo_nasprotnih),
##                                             (i_min - 1, j_min - 1, i_min - (1 + stevilo_nasprotnih), j_min - (1 + stevilo_nasprotnih))]}
##                    for parametri in SLOVAR[orientacija]:
##                        if i == parametri[0] and j == parametri[1]:
##                            self.plosca[parametri[2]][parametri[3]].barva = B
##                            self.okno.itemconfig(self.plosca[parametri[2]][parametri[3]].id, fill=B)
##                            break
##                    return True
##        
##
##
##    def stevilo_nasprotnih(self, orientacija, p):
##        (i,j) = p
##        barva = self.plosca[i][j].barva
##        (j_max, j_min) = (max(krogec.y for krogec in self.igra.izbrani), min(krogec.y for krogec in self.igra.izbrani))
##        (i_max, i_min) = (max(krogec.x for krogec in self.igra.izbrani), min(krogec.x for krogec in self.igra.izbrani))
##        SLOVAR = {"x" : [(i_max + 1, j, i + 1, j, i + 2, j),(i_min - 1, j, i - 1, j, i - 2, j)],
##                  "y" : [(i, j_max + 1, i, j + 1, i, j + 2),(i, j_min - 1, i, j - 1, i, j - 2)],
##                  "diagonala" : [(i_max + 1, j_max + 1, i + 1, j + 1, i + 2, j + 2),(i_min - 1, j_min - 1, i - 1, j - 1, i - 2, j - 2)]}
##        for parametri in SLOVAR[orientacija]:
##            if i == parametri[0] and j == parametri[1]:
##                print(parametri)
##                if self.plosca[parametri[2]][parametri[3]] is None:
##                    return (1, True)
##                elif self.plosca[parametri[2]][parametri[3]].barva == self.igra.barva_praznih:
##                    return (1, False)
##                elif self.plosca[parametri[2]][parametri[3]].barva == barva:
##                    if self.plosca[parametri[4]][parametri[5]] is None:
##                        return (2, True)
##                    elif self.plosca[parametri[4]][parametri[5]].barva == self.igra.barva_praznih:
##                        return (2, False)
##        return None, None               
##                      
##         
##    
##    def premakni_krogce(self, event):
##        i,j = self.poisci_polje(event)
##        if len(self.igra.izbrani) == 1:
##            x = self.igra.izbrani[0].x
##            y = self.igra.izbrani[0].y
##            barva = self.igra.izbrani[0].barva
##            self.plosca[x][y].oznacen = False
##            self.okno.itemconfig(self.plosca[x][y].id, fill= self.igra.barva_praznih)
##            self.plosca[x][y].barva = self.igra.barva_praznih
##            self.okno.itemconfig(self.plosca[i][j].id, fill= barva)
##            self.plosca[i][j].barva = barva
##        else:      
##            orientacija = self.orientacija_izbranih()
##            izbrani = []
##            for polje in self.igra.izbrani:
##                izbrani.append(Polje(polje.id, polje.x, polje.y, polje.barva))
##            for krogec in izbrani:
##                self.plosca[krogec.x][krogec.y].oznacen = False
##                self.okno.itemconfig(self.plosca[krogec.x][krogec.y].id, fill= self.igra.barva_praznih)
##                self.plosca[krogec.x][krogec.y].barva = self.igra.barva_praznih
##            (j_max, j_min, J) = (max(krogec.y for krogec in self.igra.izbrani), min(krogec.y for krogec in self.igra.izbrani), izbrani[0].y)
##            (i_max, i_min, I) = (max(krogec.x for krogec in self.igra.izbrani), min(krogec.x for krogec in self.igra.izbrani), izbrani[0].x)
##            novi_izbrani = []
##            SLOVAR = {"x" : [(i_max, 1, J, 0), (i_max, 0, J, -1), (i_max, 1, J, 1), (i_min, -1, J, 0), (i_min, -1, J, -1), (i_min, 0, J, 1)],
##                      "y" : [(I, 0, j_max, 1), (I, 1, j_max, 1), (I, -1, j_max, 0), (I, 0, j_min, -1), (I, 1, j_min, 0), (I, -1, j_min, -1),],
##                      "diagonala" : [(i_max, 1, j_max, 1), (i_max, 0, j_max, 1), (i_max, 1, j_max, 0), (i_min, -1, j_min, -1), (i_min, 0, j_min, -1), (i_min, -1, j_min, 0)]}
##            for parametri in SLOVAR[orientacija]: 
##                if i == parametri[0] + parametri[1] and j == parametri[2] + parametri[3]:
##                    for krogec in izbrani:
##                        id = krogec.id
##                        x = krogec.x + parametri[1]
##                        y = krogec.y + parametri[3]
##                        barva = krogec.barva
##                        novi_izbrani.append(Polje(id, x, y, barva))
##                    break
##            for krogec in novi_izbrani:
##                self.plosca[krogec.x][krogec.y].oznacen = False
##                self.okno.itemconfig(self.plosca[krogec.x][krogec.y].id, fill= krogec.barva)
##                self.plosca[krogec.x][krogec.y].barva = krogec.barva
##        self.oznaceni = []           
##
##    def orientacija_izbranih(self):
##        """Pove orientacijo izbranih krogcev. Možne smeri so x, y in diagonala."""
##        (I1, J1) = (self.igra.izbrani[0].x, self.igra.izbrani[0].y)
##        (I2, J2) = (self.igra.izbrani[1].x, self.igra.izbrani[1].y)
##        if J1 == J2:
##            return "x"
##        elif I1 == I2:
##            return "y"
##        elif abs(I1 - I2) == 1 and abs(J1 - J2) == 1:
##            return "diagonala"
##        else:
##            return None
        
    #Mislim da se to nikjer ne uporabi in lahko izbriševa
    def zacni_premik_krogcev(self,event):
        if self.premik is False:
            self.premik = True
        else:
            self.premik = False

    def zacni_igro(self, igralec_1, igralec_2):
        """Nastavi stanje igre na zacetek igre.
           Za igralca uporabi dana igralca."""
        # Ustavimo vsa vlakna, ki trenutno razmišljajo
        self.prekini_igralce()
        # Pobrišemo tiste, ki so padli dol in narišemo začetno pozicijo
        #self.plosca.delete(Gui.TAG_FIGURA)
        #self.zacetna_pozicija
        self.risi_plosco()
        # Ustvarimo novo igro
        self.igra = Igra()
        # Shranimo igralce
        self.igralec_1 = igralec_1
        self.igralec_2 = igralec_2
        self.napis.set("Na potezi je igralec 1.")
        self.igralec_1.igraj()

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
        if self.igralec_2: self.igralec_2.prekini()


    def zapri_okno(self, master):
        """Ta metoda se pokliče, ko uporabnik zapre aplikacijo."""
        # Kasneje bo tu treba še kaj narediti
        # self.prekini_igralce()
        master.destroy()

    def narisi_crte(self):
        """Nariši črte v igralnem polju"""
        self.okno.delete(Gui.TAG_OKVIR)
        d = Gui.VELIKOST_POLJA
        self.okno.create_line(2.5*d, 0.1*d, 7.5*d, 0.1*d, tag=Gui.TAG_OKVIR)
        self.okno.create_line(2.5*d, 0.8*d, 7.5*d, 0.8*d, tag=Gui.TAG_OKVIR)
        self.okno.create_line(2.5*d, 0.8*d, 0.2*d, 4.9*d, tag=Gui.TAG_OKVIR)
        self.okno.create_line(7.5*d, 0.8*d, 9.8*d, 4.9*d, tag=Gui.TAG_OKVIR)
        self.okno.create_line(0.2*d, 4.9*d, 2.5*d, 8.9*d, tag=Gui.TAG_OKVIR)
        self.okno.create_line(2.5*d, 8.9*d, 7.5*d, 8.9*d, tag=Gui.TAG_OKVIR)
        self.okno.create_line(7.5*d, 8.9*d, 9.8*d, 4.9*d, tag=Gui.TAG_OKVIR)        
        self.polje_izpodrinjenih1.create_line(0.1*d, 0.1*d, 0.9*d, 0.1*d, tag=Gui.TAG_OKVIR)
        self.polje_izpodrinjenih1.create_line(0.1*d, 0.1*d, 0.1*d, 5.9*d, tag=Gui.TAG_OKVIR)
        self.polje_izpodrinjenih1.create_line(0.1*d, 5.9*d, 0.9*d, 5.9*d, tag=Gui.TAG_OKVIR)
        self.polje_izpodrinjenih1.create_line(0.9*d, 5.9*d, 0.9*d, 0.1*d, tag=Gui.TAG_OKVIR)
        self.polje_izpodrinjenih2.create_line(0.1*d, 0.1*d, 0.9*d, 0.1*d, tag=Gui.TAG_OKVIR)
        self.polje_izpodrinjenih2.create_line(0.1*d, 0.1*d, 0.1*d, 5.9*d, tag=Gui.TAG_OKVIR)
        self.polje_izpodrinjenih2.create_line(0.1*d, 5.9*d, 0.9*d, 5.9*d, tag=Gui.TAG_OKVIR)
        self.polje_izpodrinjenih2.create_line(0.9*d, 5.9*d, 0.9*d, 0.1*d, tag=Gui.TAG_OKVIR)
        
    def prevod_barve(self, barva):
        #TODO To bova dokončala proti koncu projekta, ko bova imela čas se ukvarjati z barvami(saj je to le lepotna izboljšava)
        if barva == "yellow":
            return "rumeni"
        elif barva == "black":
            return "črni"

##class Polje:
##
##    def __init__(self, id, x, y, barva=None, oznacen=False):
##        self.id = id
##        self.x = x
##        self.y = y
##        self.barva = barva
##        self.oznacen = oznacen
##
##    def __repr__(self):
##        return 'Polje({0}, ({1}, {2}), {3}, {4})'.format(self.id, self.x, self.y, self.barva, self.oznacen)
##    

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
