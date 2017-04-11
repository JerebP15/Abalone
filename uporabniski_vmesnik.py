import tkinter    # za uporabniški vmesnik


######################################################################



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
        # Če uporabnik zapre okno naj se poklice self.zapri_okno
        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))

        # Glavni menu
        menu = tkinter.Menu(master)
        master.config(menu=menu) # Dodamo glavni menu v okno

        # Podmenu za izbiro igre
        menu_igra = tkinter.Menu(menu)
        menu.add_cascade(label="Igra", menu=menu_igra)
        menu_igra.add_command(label="Nova igra",
                              command=lambda: self.zacni_igro())
        # Napis, ki prikazuje stanje igre
        self.napis = tkinter.StringVar(master, value="Dobrodošli v Abalone!")
        tkinter.Label(master, textvariable=self.napis).grid(row=0, column=0)

        # Igralno območje
        self.okno = tkinter.Canvas(master, width=11*Gui.VELIKOST_POLJA, height=11*Gui.VELIKOST_POLJA)
        self.okno.grid(row=1, column=0)

        # Črte na igralnem polju
        #self.narisi_crte()
        self.plosca = self.narisi_plosco()
        self.izbrani = []
        self.premik = False

        # Naročimo se na dogodek Button-1 na self.okno,
        self.okno.bind("<Button-1>", self.okno_klik)
        self.okno.bind("<Tab>", self.zacni_premik_krogcev)

        # Prični igro
        self.zacni_igro()

    def narisi_plosco(self):
        self.okno.delete(Gui.TAG_FIGURA)
        d = Gui.VELIKOST_POLJA
        matrika = []
        for x in range(9):
               seznam = []
               for y in range(9):
                   seznam.append(None)
               matrika.append(seznam)
        for i in range(len(matrika)):
            for j in range(len(matrika[i])):
                if (i,j) in [(0,0),(0,1),(1,0),(1,1),(2,0),(2,1),(2,2),(3,0),(3,1),(3,2),(4,0),(4,1),(4,2),(5,1)]:
                    barva = Gui.barva_igralca_1
                elif (i,j) in [(3,7),(4,6),(4,7),(4,8),(5,6),(5,7),(5,8),(6,6),(6,7),(6,8),(7,7),(7,8),(8,7),(8,8)]:
                    barva = Gui.barva_igralca_2
                elif (i,j) not in [(5,0),(6,0),(7,0),(8,0),(6,1),(7,1),(8,1),(7,2),(8,2),(8,3)] and (j,i) not in [(5,0),(6,0),(7,0),(8,0),(6,1),(7,1),(8,1),(7,2),(8,2),(8,3)]:
                    barva = Gui.barva_praznih
                else:
                    barva = None
                if barva is not None:
                    id = self.okno.create_oval((i - j*0.5)*d + 2*d, (3**0.5)*0.5*j*d, (i - j*0.5)*d + 3*d, (3**0.5)*0.5*j*d + d, fill=barva)
                    matrika[i][j] = Polje(id, i, j, barva)             
        return matrika

    def okno_klik(self, event):
        """Obdelaj klik na ploščo."""
        # Tistemu, ki je na potezi, povemo, da je uporabnik kliknil na ploščo.
        i,j = self.poisci_polje(event)
        if self.premik is False:            #Če krogcev ne premikamo jih dodajamo
            if i is not None and j is not None and self.plosca[i][j] in self.izbrani:
                self.izbrani.remove(self.plosca[i][j])
                self.odznaci_krogec((i,j))
            elif self.preveri_polje((i,j)):
                if self.plosca[i][j] not in self.izbrani:
                    self.izbrani.append(self.plosca[i][j])
                    self.oznaci_krogec((i,j))
                print("Klik na ({0}, {1}), polje ({2}, {3})".format(event.x, event.y, i, j))
        elif self.premik is True:           #Krogce premikamo
            if len(self.izbrani) == 0:
                print("Noben krogec ni izbran")
            else:
                if self.preveri_potezo((i,j)):
                    self.premakni_krogce(event)
                    self.premik = False
                    self.izbrani = []
                
                

    def poisci_polje(self, event):
        """Vrne polje, na katero smo kliknili."""
        d = Gui.VELIKOST_POLJA
        for i in range(9):
            for j in range(9):
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
        self.okno.itemconfig(self.plosca[i][j].id, fill='red')       # itemconfig izgleda uporabno.
        self.plosca[i][j].oznacen = True
        print(self.plosca[i][j])
            
    def odznaci_krogec(self, p):
        """Obratno kot označi krogec."""
        (i, j) = p         
        self.okno.itemconfig(self.plosca[i][j].id, fill=self.plosca[i][j].barva)       # itemconfig izgleda uporabno.
        self.plosca[i][j].oznacen = False
        print(self.plosca[i][j])

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
                if len(self.izbrani) == 1:
                    if p in [(I1,J1+1),(I1,J1-1),(I1+1,J1),(I1-1,J1),(I1-1,J1-1),(I1+1,J1+1)] and self.plosca[i][j].barva == B1:
                        return True
                elif len(self.izbrani) == 2:
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

    def preveri_potezo(self, p):
        """Pogleda, ali označene krogce lahko premaknemo na željeno polje."""
        (i,j) = p
        if i is not None and j is not None:     # Zagotovimo, da smo na plošči.
            if self.plosca[i][j].barva == self.izbrani[0].barva:
                print("Ni mogoče premakniti izbranih krogcev na svoje polje!")
                return False
            elif len(self.izbrani) == 1:
                return self.plosca[i][j].barva == Gui.barva_praznih
            elif len(self.izbrani) == 2:
                (I1, J1) = (self.izbrani[0].x, self.izbrani[0].y)
                (I2, J2) = (self.izbrani[1].x, self.izbrani[1].y)
                orientacija = self.orientacija_izbranih()
                if orientacija == "y":
                    if (i,j) in [(I1, max(J1, J2) + 1),(I1, min(J1, J2) - 1)]:
                        if self.plosca[i][j].barva == Gui.barva_praznih:
                            return True
                        elif self.plosca[i][j].barva == Gui.barva_igralca_2:
                            if j == max(J1, J2) + 1:
                                return self.plosca[i][j+1].barva == Gui.barva_praznih
                            elif j == min(J1, J2) - 1:
                                return self.plosca[i][j-1].barva == Gui.barva_praznih
                    return False
                elif orientacija == "x":
                    if (i,j) in [(max(I1, I2) + 1, J1),(min(I1, I2) - 1, J1)]:
                        if self.plosca[i][j].barva == Gui.barva_praznih:
                            return True
                        elif self.plosca[i][j].barva == Gui.barva_igralca_2:
                            if i == max(I1, I2) + 1:
                                return self.plosca[i+1][j].barva == Gui.barva_praznih
                            elif i == min(I1, I2) - 1:
                                return self.plosca[i-1][j].barva == Gui.barva_praznih
                    return False
                elif orientacija == "diagonala":
                    if (i,j) in [(max(I1, I2) + 1, max(J1, J2) + 1),(min(I1, I2) - 1, min(J1, J2) - 1)]:
                        if self.plosca[i][j].barva == Gui.barva_praznih:
                            return True
                        elif self.plosca[i][j].barva == Gui.barva_igralca_2:
                            if i == max(I1, I2) + 1 and j == max(J1, J2) + 1:
                                return self.plosca[i+1][j+1].barva == Gui.barva_praznih
                            elif i == min(I1, I2) - 1 and j == min(J1, J2) - 1:
                                return self.plosca[i-1][j-1].barva == Gui.barva_praznih
                    return False
            elif len(self.izbrani) == 3:
                (I1, J1) = (self.izbrani[0].x, self.izbrani[0].y)
                (I2, J2) = (self.izbrani[1].x, self.izbrani[1].y)
                (I3, J3) = (self.izbrani[2].x, self.izbrani[2].y)
                orientacija = self.orientacija_izbranih()
                if orientacija == "y":
                    if (i,j) in [(I1, max(J1, J2, J3) +1),(I1, min(J1, J2, J3) - 1)]:
                        if self.plosca[i][j].barva == Gui.barva_praznih:
                            return True
                        elif self.plosca[i][j].barva == Gui.barva_igralca_2:
                            if j == max(J1, J2, J3) + 1:
                                return self.plosca[i][j+1].barva == Gui.barva_praznih or (self.plosca[i][j+1].barva == Gui.barva_igralca_2 and self.plosca[i][j+2].barva != Gui.barva_igralca_1 and self.plosca[i][j+2].barva != Gui.barva_igralca_2)
                            elif j == min(J1, J2, J3) - 1:
                                return self.plosca[i][j-1].barva == Gui.barva_praznih or (self.plosca[i][j-1].barva == Gui.barva_igralca_2 and self.plosca[i][j-2].barva != Gui.barva_igralca_1 and self.plosca[i][j-2].barva != Gui.barva_igralca_2)
                    return False
                elif orientacija == "x":
                    if (i,j) in [(max(I1, I2, I3) + 1, J1),(min(I1, I2, I3) - 1, J1)]:
                        if self.plosca[i][j].barva == Gui.barva_praznih:
                            return True
                        elif self.plosca[i][j].barva == Gui.barva_igralca_2:
                            if i == max(I1, I2, I3) + 1:
                                return self.plosca[i+1][j].barva == Gui.barva_praznih or (self.plosca[i+1][j].barva == Gui.barva_igralca_2 and self.plosca[i+2][j].barva != Gui.barva_igralca_1 and self.plosca[i+2][j].barva != Gui.barva_igralca_2)
                            elif i == min(I1, I2, I3) - 1:
                                return self.plosca[i-1][j].barva == Gui.barva_praznih or (self.plosca[i-1][j].barva == Gui.barva_igralca_2 and self.plosca[i-2][j].barva != Gui.barva_igralca_1 and self.plosca[i-2][j].barva != Gui.barva_igralca_2)
                    return False
                elif orientacija == "diagonala":
                    if (i,j) in [(max(I1, I2, I3) + 1, max(J1, J2, J3) + 1),(min(I1, I2, I3) - 1, min(J1, J2, J3) - 1)]:
                        if self.plosca[i][j].barva == Gui.barva_praznih:
                            return True
                        elif self.plosca[i][j].barva == Gui.barva_igralca_2:
                            if i == max(I1, I2, I3) + 1 and j == max(J1, J2, J3) + 1:
                                return self.plosca[i+1][j+1].barva == Gui.barva_praznih or (self.plosca[i+1][j+1].barva == Gui.barva_igralca_2 and self.plosca[i+2][j+2].barva != Gui.barva_igralca_1 and self.plosca[i+2][j+2].barva != Gui.barva_igralca_2)
                            elif i == min(I1, I2, I3) - 1 and j == min(J1, J2, J3) - 1:
                                return self.plosca[i-1][j-1].barva == Gui.barva_praznih or (self.plosca[i-1][j-1].barva == Gui.barva_igralca_2 and self.plosca[i-2][j-2].barva != Gui.barva_igralca_1 and self.plosca[i-2][j-2].barva != Gui.barva_igralca_2)
                    return False
            return False            
        
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
            for polje in izbrani:
                self.plosca[polje.x][polje.y].oznacen = False
                self.okno.itemconfig(self.plosca[polje.x][polje.y].id, fill= Gui.barva_praznih)
                self.plosca[polje.x][polje.y].barva = Gui.barva_praznih
            novi_izbrani = []
            if orientacija == "x":
                sez = [krogec.x for krogec in izbrani]
                m = max(sez) + 1
                if i == m:
                    for krogec in izbrani:
                        id = krogec.id
                        x = krogec.x + 1
                        y = krogec.y
                        barva = krogec.barva            
                        novi_izbrani.append(Polje(id, x, y, barva))
                elif i == min([krogec.x for krogec in izbrani]) - 1:
                    for krogec in izbrani:
                        id = krogec.id
                        x = krogec.x - 1
                        y = krogec.y
                        barva = krogec.barva            
                        novi_izbrani.append(Polje(id, x, y, barva))
                    print(novi_izbrani)
            elif orientacija == "y":
                if j == max([krogec.y for krogec in izbrani]) + 1:
                    for krogec in izbrani:
                        id = krogec.id
                        x = krogec.x
                        y = krogec.y + 1
                        barva = krogec.barva            
                        novi_izbrani.append(Polje(id, x, y, barva))
                elif j == min([krogec.y for krogec in izbrani]) - 1:
                    for krogec in izbrani:
                        id = krogec.id
                        x = krogec.x
                        y = krogec.y - 1
                        barva = krogec.barva           
                        novi_izbrani.append(Polje(id, x, y, barva))
            elif orientacija == "diagonala":
                if i == max([krogec.x for krogec in izbrani]) + 1 and j == max([krogec.y for krogec in izbrani]) + 1:
                    for krogec in izbrani:
                        id = krogec.id
                        x = krogec.x + 1
                        y = krogec.y + 1
                        barva = krogec.barva            
                        novi_izbrani.append(Polje(id, x, y, barva))
                elif j == min([krogec.y for krogec in izbrani]) - 1 and i == min([krogec.x for krogec in izbrani]) - 1:
                    for krogec in izbrani:
                        id = krogec.id
                        x = krogec.x - 1
                        y = krogec.y - 1
                        barva = krogec.barva           
                        novi_izbrani.append(Polje(id, x, y, barva))
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

    def zacni_igro(self):
        """Nastavi stanje igre na zacetek igre.
           Za igralca uporabi dana igralca."""
        # Pobrišemo vse figure s polja
        self.okno.delete(Gui.TAG_FIGURA)

    def koncaj_igro(self):
        """Nastavi stanje igre na konec igre."""
        self.napis.set("Konec igre.")

    def zapri_okno(self, master):
        """Ta metoda se pokliče, ko uporabnik zapre aplikacijo."""
        # Kasneje bo tu treba še kaj narediti
        master.destroy()

    def narisi_crte(self):
        """Nariši črte v igralnem polju"""
        self.okno.delete(Gui.TAG_OKVIR)
        d = Gui.VELIKOST_POLJA
        self.okno.create_line(2.5*d, 0.1*d, 9*d, 0.1*d, tag=Gui.TAG_OKVIR)
        self.okno.create_line(2.5*d, 1*d, 9*d, 1*d, tag=Gui.TAG_OKVIR)
        self.okno.create_line(0*d, 5.5*d, 2.5*d, 1*d, tag=Gui.TAG_OKVIR)
        self.okno.create_line(9*d, 1*d, 11*d, 5.5*d, tag=Gui.TAG_OKVIR)

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
