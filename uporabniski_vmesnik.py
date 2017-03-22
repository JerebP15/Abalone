import tkinter    # za uporabniški vmesnik

######################################################################
## Uporabniški vmesnik

class Gui():
    # S to oznako so označeni vsi grafični elementi v self.plosca, ki se
    # pobrišejo, ko se začne nova igra (torej, križci in krožci)
    TAG_FIGURA = 'figura' #?

    # Oznaka za črte
    TAG_OKVIR = 'okvir' #?

    # Velikost polja
    VELIKOST_POLJA = 50

    def __init__(self, master):
        # Če uporabnik zapre okno naj se poklice self.zapri_okno
        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))

        self.matrika = self.ustvari_matriko()

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
        self.plosca = tkinter.Canvas(master, width=11*Gui.VELIKOST_POLJA, height=11*Gui.VELIKOST_POLJA)
        self.plosca.grid(row=1, column=0)

        # Črte na igralnem polju
        self.narisi_crte()
        self.narisi_krogce()

        # Naročimo se na dogodek Button-1 na self.plosca,
        self.plosca.bind("<Button-1>", self.plosca_klik)

        # Prični igro
        self.zacni_igro()

    def ustvari_matriko(self):
        #Ustvari 9x9 matriko
        matrika = []
        for x in range(9):
            seznam = []
            for y in range(9):
                seznam.append(0)
            matrika.append(seznam)
        for i in range(9):
            for j in range(9):
                if (i,j) in [(0,5),(0,6),(0,7),(0,8),(1,6),(1,7),(1,8),(2,7),(2,8),(3,8)]:
                    matrika[i][j] = None
                elif (j,i) in [(0,5),(0,6),(0,7),(0,8),(1,6),(1,7),(1,8),(2,7),(2,8),(3,8)]:
                    matrika[i][j] = None
        return matrika


    def zacni_igro(self):
        """Nastavi stanje igre na zacetek igre.
           Za igralca uporabi dana igralca."""
        # Pobrišemo vse figure s polja
        self.plosca.delete(Gui.TAG_FIGURA)

    def koncaj_igro(self):
        """Nastavi stanje igre na konec igre."""
        self.napis.set("Konec igre.")

    def zapri_okno(self, master):
        """Ta metoda se pokliče, ko uporabnik zapre aplikacijo."""
        # Kasneje bo tu treba še kaj narediti
        master.destroy()

    def narisi_crte(self):
        """Nariši črte v igralnem polju"""
        self.plosca.delete(Gui.TAG_OKVIR)
        d = Gui.VELIKOST_POLJA
        self.plosca.create_line(2.5*d, 0.1*d, 9*d, 0.1*d, tag=Gui.TAG_OKVIR)
        self.plosca.create_line(2.5*d, 1*d, 9*d, 1*d, tag=Gui.TAG_OKVIR)
        self.plosca.create_line(0*d, 5.5*d, 2.5*d, 1*d, tag=Gui.TAG_OKVIR)
        self.plosca.create_line(9*d, 1*d, 11*d, 5.5*d, tag=Gui.TAG_OKVIR)

    def narisi_krogce(self):
        self.plosca.delete(Gui.TAG_FIGURA)
        for i in range(len(self.matrika)):
            for j in self.matrika[i]:
                if matrika[i][j] is not None:
                    self.plosca.create_oval()

    def narisi_X(self, p):
        """Nariši križec v polje (i, j)."""
        x = p[0] * 100
        y = p[1] * 100
        sirina = 3
        self.plosca.create_line(x+5, y+5, x+95, y+95, width=sirina, tag=Gui.TAG_FIGURA)
        self.plosca.create_line(x+95, y+5, x+5, y+95, width=sirina, tag=Gui.TAG_FIGURA)

    def narisi_O(self, p):
        """Nariši krožec v polje (i, j)."""
        x = p[0] * 100
        y = p[1] * 100
        sirina = 3
        self.plosca.create_oval(x+5, y+5, x+95, y+95, width=sirina,tag=Gui.TAG_FIGURA)

    def plosca_klik(self, event):
        """Obdelaj klik na ploščo."""
        # Tistemu, ki je na potezi, povemo, da je uporabnik kliknil na ploščo.
        # Podamo mu potezo p.
        i = event.x // 100
        j = event.y // 100
        print ("Klik na ({0}, {1}), polje ({2}, {3})".format(event.x, event.y, i, j))
        self.povleci_potezo((i,j))

    def povleci_potezo(self, p):
        """Povleci potezo p, če je veljavna. Če ni veljavna, ne naredi nič."""
        (i, j) = p
        # Da vidimo, ali se prav riše, včasih narišemo X in včasih O
        if (i + j) % 2 == 0:
            self.narisi_X(p)
        else:
            self.narisi_O(p)

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
    root.title("Tri v vrsto")

    # Naredimo objekt razreda Gui in ga spravimo v spremenljivko,
    # sicer bo Python mislil, da je objekt neuporabljen in ga bo pobrisal
    # iz pomnilnika.
    aplikacija = Gui(root)

    # Kontrolo prepustimo glavnemu oknu. Funkcija mainloop neha
    # delovati, ko okno zapremo.
    root.mainloop()
