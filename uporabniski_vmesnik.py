import tkinter    # za uporabniški vmesnik

######################################################################


# Za premikanje krogcev je potrebno naredit še:
#   ko naslednjič klikneš in vlečeš, se premaknejo
#   ali je moteče, da je treba krogce izbirat po vrsti?


# Nujno UNDO. Ali je dovolj, da se v zgodovino shrani samo matrika? Ali potrebujemo tudi seznam izbranih polj? Ta polja so rdeča, tako da se to mogoče vidi že iz matrike?




## Uporabniški vmesnik

class Gui():
    # S to oznako so označeni vsi grafični elementi v self.okno, ki se
    # pobrišejo, ko se začne nova igra (torej, križci in krožci)
    TAG_FIGURA = 'figura' #?

    # Oznaka za črte
    TAG_OKVIR = 'okvir' #?

    # Velikost polja
    VELIKOST_POLJA = 50


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

        # Naročimo se na dogodek Button-1 na self.okno,
        self.okno.bind("<Button-1>", self.okno_klik)

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
                    barva = 'yellow'
                elif (i,j) in [(3,7),(4,6),(4,7),(4,8),(5,6),(5,7),(5,8),(6,6),(6,7),(6,8),(7,7),(7,8),(8,7),(8,8)]:
                    barva ='black'
                elif (i,j) not in [(5,0),(6,0),(7,0),(8,0),(6,1),(7,1),(8,1),(7,2),(8,2),(8,3)] and (j,i) not in [(5,0),(6,0),(7,0),(8,0),(6,1),(7,1),(8,1),(7,2),(8,2),(8,3)]:
                    barva = 'white'
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
        if self.preveri_polje((i,j)):   # Pomožna funkcija
            self.izbrani.append(self.plosca[i][j])     # Seznam izbranih (za zgodovino?)
            self.pobarvaj_krogec((i,j))
            print("Klik na ({0}, {1}), polje ({2}, {3})".format(event.x, event.y, i, j))

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
        return None, None

    def pobarvaj_krogec(self, p):
        """Izbrani krogec pobarva rdeče."""
        d = Gui.VELIKOST_POLJA
        (i, j) = p
        if i in range(9) and j in range(9):
            self.okno.itemconfig(self.plosca[i][j].id, fill='red')       # itemconfig izgleda uporabno.
            self.plosca[i][j].barva = 'red'
            print(self.plosca[i][j])

    def preveri_polje(self, p):
        """Pogleda, ali ta krogec lahko izberemo."""
        # !!! Deluje samo, če izbiramo po vrsti. !!!
        (i,j) = p
        if i is not None and j is not None and self.plosca[i][j].barva != 'white':     # Zagotovimo, da smo na plošči in da nismo izbrali praznega polja.
            polje = self.plosca[i][j]
            if len(self.izbrani) == 0:      # Prvo izbrano polje je lahko katerokoli.
                return True
            elif len(self.izbrani) == 3:      # Izbrana so lahko največ tri polja.
                return False
            else:
                (I, J, B) = (self.izbrani[0].x, self.izbrani[0].y, self.izbrani[0].barva)     # Koordinate in barva prvega izbranega krogca
                k = len(self.izbrani)
                #TODO loči možnosti za 2. in 3. izbrani krogec
                if p in [(I,J+k),(I,J-k),(I+k,J),(I-k,J),(I-k,J-k),(I+k,J+k)] and polje.barva != B: # "Sosedni" krogci druge barve - za 1 ali 2 oddaljeni od prvega izbranega.
                    return True
        else:
            return False

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

    def narisi_X(self, p):
        """Nariši križec v polje (i, j)."""
        x = p[0] * 100
        y = p[1] * 100
        sirina = 3
        self.okno.create_line(x+5, y+5, x+95, y+95, width=sirina, tag=Gui.TAG_FIGURA)
        self.okno.create_line(x+95, y+5, x+5, y+95, width=sirina, tag=Gui.TAG_FIGURA)

    def narisi_O(self, p):
        """Nariši krožec v polje (i, j)."""
        x = p[0] * 100
        y = p[1] * 100
        sirina = 3
        self.okno.create_oval(x+5, y+5, x+95, y+95, width=sirina,tag=Gui.TAG_FIGURA)





    def ustvari_matriko(self):
        #Ustvari 9x9 matriko
        matrika = []
        for x in range(9):
            seznam = []
            for y in range(9):
                seznam.append(0)
            matrika.append(seznam)
        for i in range(9):              # Ustreza x-kooordinati, torej pove (poševni) stolpec.
            for j in range(9):          # Ustreza y-kooordinati, torej pove vrstico (od zgoraj dol).
                if (i,j) in [(5,0),(6,0),(7,0),(8,0),(6,1),(7,1),(8,1),(7,2),(8,2),(8,3)]:  
                    matrika[i][j] = None    # Ta polja ne obstajajo
                elif (j,i) in [(5,0),(6,0),(7,0),(8,0),(6,1),(7,1),(8,1),(7,2),(8,2),(8,3)]:
                    matrika[i][j] = None    # Ta polja ne obstajajo
                elif (i,j) in [(0,0),(0,1),(1,0),(1,1),(2,0),(2,1),(2,2),(3,0),(3,1),(3,2),(4,0),(4,1),(4,2),(5,0),(5,1)]:
                    matrika[i][j] = 'B'     # Začetna postavitev belega.
                elif (i,j) in [(3,7),(4,6),(4,7),(4,8),(5,6),(5,7),(5,8),(6,6),(6,7),(6,8),(7,7),(7,8),(8,7),(8,8)]:
                    matrika[i][j] = 'C'     # Začetna postavitev črnega.
        #print(matrika)
        return matrika

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
