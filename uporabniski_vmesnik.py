import tkinter    # za uporabniški vmesnik
import argparse   # za argumente iz ukazne vrstice
import logging    # za odpravljanje napak

# Privzeta minimax globina, če je nismo podali ob zagonu v ukazni vrstici
MINIMAX_GLOBINA = 2

from logika_igre import *
from clovek import *
from racunalnik import *
from tkinter import messagebox

######################################################################

pravila_igre = """Deska je sestavljena iz 61 polj, ki so razporejena v šestkotnik.
Vsak igralec ima 14 kroglic, ki so na začetku razporejene, kot je prikazano spodaj. Igro začne spodnji igralec.

V vsaki potezi igralec premakne eno, dve ali tri svoje kroglice.
Premik je mogoč v katerokoli od šestih smeri, če nas pri tem ne ovirajo druge kroglice. Vedno se premaknemo za eno mesto.
Potisk nasprotnikovih kroglic je mogoč le naravnost (torej v smeri, ki jo določa premica skozi središča izbranih kroglic) in še to samo, če je nasprotnikovih kroglic strogo manj od naših.

Cilj igre je potisniti 6 nasprotnikovih krogclic s plošče.

OPOMBA:
Pravila načeloma omogočajo neskončno igro. Če eden od igralcev zavzame defenzivno pozicijo, lahko naprotniku prepreči vsak poskus napada, kar vodi v igro brez izrinjenih kroglic.
"""
tipke = """levi klik miške = označi/odznači krogec

desni klik miške = premanki krogce

Escape = odznači vse izbrane krogce

Ctrl + z = razveljavi potezo
"""

prevodi = {"yellow" : "rumeni", "black" : "črni", "green" : "zeleni", "red" : "rdeči", "blue" : "modri", "cyan" : "svetlo modri" , "magenta" : "roza"}

def prevod_barve(barva):
    return prevodi[barva] if barva in prevodi else "vesoljski"

def prevod_barve_menu(barva):
    return prevodi[barva] if barva in prevodi else "Vesoljski"

## Uporabniški vmesnik

class Gui():
    # S to oznako so označeni vsi grafični elementi v self.okno, ki se
    # pobrišejo, ko se začne nova igra
    TAG_FIGURA = 'figura'

    # Oznaka za črte
    TAG_OKVIR = 'okvir'

    # Velikost polja
    VELIKOST_POLJA = 50

    def __init__(self, master):
        master.minsize(width=730, height=630)
        self.igralec_1 = None # Objekt, ki igra prvi igralec (nastavimo ob začetku igre)
        self.igralec_2 = None # Objekt, ki igra drugi igralec (nastavimo ob začetku igre)
        self.igra = None # Objekt, ki predstavlja logiko igre
        self.matrika_id = self.ustvari_matriko_id()
        # Seznam izpodrinjenih krogcev
        self.izpodrinjeni = []
        self.izpodrinjeni_id = []
        self.zacni = False #Ali smo zadovoljni z izbiro barv in se igra lahko začne
        # Če uporabnik zapre okno naj se poklice self.zapri_okno
        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))

        # Glavni menu
        menu = tkinter.Menu(master)
        master.config(menu=menu) # Dodamo glavni menu v okno

        # Napis, ki prikazuje stanje igre
        self.napis = tkinter.StringVar(master, value="Dobrodošli v Abalone!")
        tkinter.Label(master, textvariable=self.napis, font = ('Times', '15', 'bold')).grid(row=0, column=1)

        # Igralno območje
        self.okno = tkinter.Canvas(master, width=11*Gui.VELIKOST_POLJA, height=11*Gui.VELIKOST_POLJA)
        self.okno.grid(row=1, column=1)

        # Območje, kjer se rišejo krogci, ki so bili že izpodrinjeni iz plošče
        self.polje_izpodrinjenih1 = tkinter.Canvas(master, width=2*Gui.VELIKOST_POLJA, height=8*Gui.VELIKOST_POLJA)
        self.polje_izpodrinjenih1.grid(row=1, column=0)
        self.polje_izpodrinjenih2 = tkinter.Canvas(master, width=2*Gui.VELIKOST_POLJA, height=8*Gui.VELIKOST_POLJA)
        self.polje_izpodrinjenih2.grid(row=1, column=2)

        #Gumb za začetek igre
        self.gumb = tkinter.Button(master, bg="cyan", state='normal',  width=int(0.8 * Gui.VELIKOST_POLJA) ,font = ('Times', '15', 'bold'), text='Začni!', command=lambda: self.pritisk_gumba())
        self.gumb.grid(row=2, column=1)

        # Črte na igralnem polju
        self.narisi_crte()

        # Naročimo se na dogodke
        self.okno.bind("<Button-1>", self.levi_klik)
        self.okno.bind("<Button-3>", self.desni_klik)
        self.okno.bind("<Button-2>", self.desni_klik) #Da dela tudi na Mac-u
        self.okno.bind('<Escape>', self.odznaci_vse_krogce)  #Zaradi nekega razloga dela samo, če klikneš tab (ko klikneš tab se polje obrobi in od takrat naprej to dela, prej pa se ne zgodi nič)
        self.okno.bind('<Control-z>', self.undo)

        # Prični igro
        self.zacni_igro(Clovek(self), Clovek(self))

        # Podmenu za izbiro igre
        menu_igra = tkinter.Menu(menu, tearoff = 0)
        menu.add_cascade(label="Način igre", menu=menu_igra)
        menu_igra.add_command(label="Človek : Človek", command=lambda: self.zacni_igro(Clovek(self), Clovek(self)))
        menu_igra.add_command(label="Človek : Računalnik", command=lambda: self.zacni_igro(Racunalnik(self, Minimax(MINIMAX_GLOBINA)), Clovek(self)))
        menu_igra.add_command(label="Računalnik : Človek", command=lambda: self.zacni_igro(Clovek(self), Racunalnik(self, Minimax(MINIMAX_GLOBINA))))
        menu_igra.add_command(label="Računalnik : Računalnik",
                              command=lambda: self.zacni_igro(Racunalnik(self, Minimax(MINIMAX_GLOBINA)), Racunalnik(self, Minimax(MINIMAX_GLOBINA))))
        # Podmenu z navodili igre
        menu_navodila = tkinter.Menu(menu, tearoff = 0)
        menu.add_cascade(label="Informacije", menu = menu_navodila)
        menu_navodila.add_command(label = "Pravila igre", command = lambda: tkinter.messagebox.showinfo("Pravila igre", pravila_igre))
        menu_navodila.add_command(label = "Tipke", command = lambda: tkinter.messagebox.showinfo("Tipke", tipke))

        # Podmenu za izbiro barve igalcev
        menu_barve1 = tkinter.Menu(menu, tearoff = 0)
        menu.add_cascade(label="Barva spodnjega igralca", menu = menu_barve1)
        menu_barve1.add_command(label="Črna", command = lambda: self.spremeni_barvo2("black"))
        menu_barve1.add_command(label="Rumena", command = lambda: self.spremeni_barvo2("yellow"))
        menu_barve1.add_command(label="Rdeča", command = lambda: self.spremeni_barvo2("red"))
        menu_barve1.add_command(label="Zelena", command = lambda: self.spremeni_barvo2("green"))
        menu_barve1.add_command(label="Modra", command = lambda: self.spremeni_barvo2("blue"))
        menu_barve1.add_command(label="Svetlo modra", command = lambda: self.spremeni_barvo2("cyan"))
        menu_barve1.add_command(label="Roza", command = lambda: self.spremeni_barvo2("magenta"))

        menu_barve2 = tkinter.Menu(menu, tearoff = 0)
        menu.add_cascade(label="Barva zgornjega igralca", menu = menu_barve2)
        menu_barve2.add_command(label="Črna", command = lambda: self.spremeni_barvo1("black"))
        menu_barve2.add_command(label="Rumena", command = lambda: self.spremeni_barvo1("yellow"))
        menu_barve2.add_command(label="Rdeča", command = lambda: self.spremeni_barvo1("red"))
        menu_barve2.add_command(label="Zelena", command = lambda: self.spremeni_barvo1("green"))
        menu_barve2.add_command(label="Modra", command = lambda: self.spremeni_barvo1("blue"))
        menu_barve2.add_command(label="Svetlo modra", command = lambda: self.spremeni_barvo1("cyan"))
        menu_barve2.add_command(label="Roza", command = lambda: self.spremeni_barvo1("magenta"))

    def zapri_okno(self, master):
        """Ta metoda se pokliče, ko uporabnik zapre aplikacijo."""
        self.prekini_igralce()
        master.destroy()

    def prekini_igralce(self):
        """Sporoči igralcem, da morajo nehati razmišljati."""
        logging.debug ("prekinjam igralce")
        if self.igralec_1: self.igralec_1.prekini()
        if self.igralec_2: self.igralec_2.prekini()

    def ustvari_matriko_id(self):
        """Ustvari matriko id-jev, ki se ujema z matriko self.igra.plosca, vendar vsebuje id-je."""
        matrika = []
        for x in range(11):
               seznam = []
               for y in range(11):
                   seznam.append(None)
               matrika.append(seznam)
        return matrika

    def risi_plosco(self):
        """Nariše krogce na plošči (v začetni poziciji)."""
        d = Gui.VELIKOST_POLJA
        matrika = self.igra.plosca
        for i in range(len(matrika)):
             for j in range(len(matrika[i])):
                 if matrika[i][j] is not None:
                     id = self.okno.create_oval((i - j*0.5)*d + 2*d, (3**0.5)*0.5*j*d, (i - j*0.5)*d + 3*d, (3**0.5)*0.5*j*d + d, fill=matrika[i][j])
                     self.matrika_id[i][j] = id

    def narisi_crte(self):
        """Nariši črte v igralnem polju"""
        self.okno.delete(Gui.TAG_OKVIR)
        d = Gui.VELIKOST_POLJA
        self.okno.create_line(2.5*d, 0.1*d, 7.5*d, 0.1*d, tag=Gui.TAG_OKVIR)
        self.okno.create_line(2.5*d, 0.8*d, 7.5*d, 0.8*d, tag=Gui.TAG_OKVIR)
        self.okno.create_line(2.5*d, 0.8*d, 0.2*d, 4.85*d, tag=Gui.TAG_OKVIR)
        self.okno.create_line(7.5*d, 0.8*d, 9.8*d, 4.85*d, tag=Gui.TAG_OKVIR)
        self.okno.create_line(0.2*d, 4.85*d, 2.5*d, 8.85*d, tag=Gui.TAG_OKVIR)
        self.okno.create_line(2.5*d, 8.85*d, 7.5*d, 8.85*d, tag=Gui.TAG_OKVIR)
        self.okno.create_line(7.5*d, 8.85*d, 9.8*d, 4.85*d, tag=Gui.TAG_OKVIR)
        self.polje_izpodrinjenih1.create_line(0.1*d, 0.9*d, 1.3*d, 0.9*d, tag=Gui.TAG_OKVIR)
        self.polje_izpodrinjenih1.create_line(0.1*d, 0.9*d, 0.1*d, 7.5*d, tag=Gui.TAG_OKVIR)
        self.polje_izpodrinjenih1.create_line(0.1*d, 7.5*d, 1.3*d, 7.5*d, tag=Gui.TAG_OKVIR)
        self.polje_izpodrinjenih1.create_line(1.3*d, 7.5*d, 1.3*d, 0.9*d, tag=Gui.TAG_OKVIR)
        self.polje_izpodrinjenih2.create_line(0.1*d, 0.9*d, 1.3*d, 0.9*d, tag=Gui.TAG_OKVIR)
        self.polje_izpodrinjenih2.create_line(0.1*d, 0.9*d, 0.1*d, 7.5*d, tag=Gui.TAG_OKVIR)
        self.polje_izpodrinjenih2.create_line(0.1*d, 7.5*d, 1.3*d, 7.5*d, tag=Gui.TAG_OKVIR)
        self.polje_izpodrinjenih2.create_line(1.3*d, 7.5*d, 1.3*d, 0.9*d, tag=Gui.TAG_OKVIR)

    def zacni_igro(self, igralec_1, igralec_2):
        """Nastavi stanje igre na zacetek igre.
           Za igralca uporabi dana igralca."""
        # Ustavimo vsa vlakna, ki trenutno razmišljajo
        self.zacni = False
        self.izpodrinjeni = []
        self.prekini_igralce()
        self.gumb.grid()
        # Pobrišemo tiste, ki so padli dol in narišemo začetno pozicijo
        self.polje_izpodrinjenih1.delete(Gui.TAG_FIGURA)
        self.polje_izpodrinjenih2.delete(Gui.TAG_FIGURA)
        if self.igra is not None:
            barva_1 = self.igra.barva_igralca_1
            barva_2 = self.igra.barva_igralca_2
            barva_izbranih = self.igra.barva_izbranih
            self.igra = Igra()
            self.igra.barva_izbranih = barva_izbranih
            self.spremeni_barvo1(barva_1)
            self.spremeni_barvo2(barva_2)
        else:
            self.igra = Igra()
        self.risi_plosco()
        # Shranimo igralce
        self.igralec_1 = igralec_1
        self.igralec_2 = igralec_2
        self.napis.set("Igro začne {} igralec.".format(prevod_barve(self.igra.barva_igralca_2)))
        if self.zacni:
            self.igralec_2.igraj()
        else:
            self.gumb.after(1000, self.zacni_potezo)

    def zacni_potezo(self):
        """Vsakih 100ms preveri, ali je lahko računalnik že začne razmišljati."""
        if self.zacni == True:
            self.igralec_2.igraj()
        else:
            self.gumb.after(1000, self.zacni_potezo)

    def koncaj_igro(self, zmagovalec):
        """Nastavi stanje igre na konec igre."""
        if zmagovalec == IGRALEC_2:
            self.napis.set("Zmagal je {} igralec.".format(prevod_barve(self.igra.barva_igralca_1)))
            tkinter.messagebox.showinfo("Konec igre", "Igre je konec. Zmagal je {} igralec.".format(prevod_barve(self.igra.barva_igralca_1)))
        elif zmagovalec == IGRALEC_1:
            self.napis.set("Zmagal je {} igralec.".format(prevod_barve(self.igra.barva_igralca_2)))
            tkinter.messagebox.showinfo("Konec igre", "Igre je konec. Zmagal je {} igralec.".format(prevod_barve(self.igra.barva_igralca_2)))
        else:
            assert False # Nekdo mora zmagati, sicer je šlo nekaj narobe in se sesujemo.
        self.izpodrinjeni = []
        self.zacni = False

    def pritisk_gumba(self):
        """Omogoči začetek igre in odstrani gumb."""
        self.gumb.grid_remove()
        self.zacni = True

    def levi_klik(self, event):
        """Obdelamo levi klik - oznacevanje krogcev."""
        p = self.poisci_polje(event)
        (i,j) = p
        if i is not None and j is not None:
            if self.zacni == True:
                igralec = self.igra.na_potezi
                if igralec == IGRALEC_1:
                    self.igralec_1.oznaci(p)
                elif igralec == IGRALEC_2:
                    self.igralec_2.oznaci(p)
            else:
                tkinter.messagebox.showwarning("Igra se ni začela", """Igra se še ni začela. Kliknite gumb za začetek igre.
Če želite, lahko še prej spremenite barve krogcev.""")
        else:
            pass

    def poisci_polje(self, event):
        """Vrne polje, na katero smo kliknili, ali (None, None), če smo kliknili izven plošče."""
        d = Gui.VELIKOST_POLJA
        for i in range(11):
            for j in range(11):
                if self.igra.plosca[i][j] is None:
                    continue        # Poskusi naslednji i,j
                sredisce_x = (i - j*0.5)*d + 2.5*d
                sredisce_y = (3**0.5)*0.5*j*d + 0.5*d
                r = ((event.x - sredisce_x)**2 + (event.y - sredisce_y)**2)**0.5
                if r <= d/2:
                    return i,j
        return (None, None)

    def oznacevanje(self, p):
        """Če smo izbrali (svoje) neoznačene krogce, se označijo.
           Če smo izbrali že označene krogce, se odznačijo in spet postanejo barvni."""
        igralec = self.igra.na_potezi
        odziv = self.igra.oznacevanje(p, igralec)
        if odziv == "oznaci":
            self.oznaci_krogec(p)
        elif odziv == "odznaci":
            self.odznaci_krogec(p)
        else:
            pass

    def oznaci_krogec(self, p):
        """Krogec na katerega smo kliknili označi (pobarva rdeče)."""
        (i, j) = p
        self.okno.itemconfig(self.matrika_id[i][j], fill=self.igra.barva_izbranih)

    def odznaci_krogec(self, p):
        """Odznači krogec na katerega smo kliknili."""
        (i, j) = p
        self.okno.itemconfig(self.matrika_id[i][j], fill=self.igra.plosca[i][j])

    def odznaci_vse_krogce(self, p):
        """Odznači vse izbrane krogce."""
        for p in self.igra.izbrani:
            (i, j) = p
            self.okno.itemconfig(self.matrika_id[i][j], fill=self.igra.plosca[i][j])
        self.igra.izbrani = []

    def desni_klik(self, event):
        """Obdelamo desni klik - premikanje krogcev."""
        p = self.poisci_polje(event)
        (i,j) = p
        if i is not None and j is not None and len(self.igra.izbrani) != 0:
            if self.zacni == True:
                igralec = self.igra.na_potezi
                if igralec == IGRALEC_1:
                    self.igralec_1.premakni(p)
                elif igralec == IGRALEC_2:
                    self.igralec_2.premakni(p)
            else:
                tkinter.messagebox.showwarning("Igra se ni začela", """Igra se še ni začela. Kliknite gumb za začetek igre.
Če želite, lahko še prej spremenite barve krogcev.""")
        else:
            pass

    def povleci_potezo(self, p):
        """Povlece potezo in zamenja, kdo je na potezi."""
        igralec = self.igra.na_potezi
        (premik, izrinjeni,r) = self.igra.premikanje(p)
        if premik is not None:
            for polje in premik:
                (x,y,barva) = polje
                self.okno.itemconfig(self.matrika_id[x][y], fill = barva)
            if len(izrinjeni) != len(self.izpodrinjeni):
                self.izpodrinjeni.append(izrinjeni[-1])
                self.narisi_izpodrinjene(izrinjeni[-1])
        if r is None:
            pass
        else:
            if r == NI_KONEC:
                # Igra se nadaljuje
                if self.igra.na_potezi == IGRALEC_1:
                    self.napis.set("Na potezi je {}.".format(prevod_barve(self.igra.barva_igralca_1)))
                    self.igralec_1.igraj()
                elif self.igra.na_potezi == IGRALEC_2:
                    self.napis.set("Na potezi je {}.".format(prevod_barve(self.igra.barva_igralca_2)))
                    self.igralec_2.igraj()
            else:
                # Igre je konec, koncaj
                self.koncaj_igro(r)

    def narisi_izpodrinjene(self,barva):
        """Krogec, ki je bil izpodrinjen, nariše v ustrezen stolpec ob igralni plošči."""
        d = Gui.VELIKOST_POLJA
        stevec = 0
        # Prešteje krogce prvega igralca, ki so že izrinjeni.
        # Ker poznamo skupno število izrinjenih, iz tega lahko dobimo tudi število izrinjenih krogcev druge barve.
        for polje in self.izpodrinjeni:
            if polje == self.igra.barva_igralca_1:
                stevec += 1
        if barva == self.igra.barva_igralca_1:
            h = stevec - 1
            id = self.polje_izpodrinjenih2.create_oval(0.2*d, (6.45 - h)*d - 5 * h, 1.2*d, (7.45 - h)*d - 5 * h, tag=Gui.TAG_FIGURA, fill = barva)
            self.izpodrinjeni_id.append((barva,id))
        elif barva == self.igra.barva_igralca_2:
            h = len(self.izpodrinjeni) - stevec - 1
            id = self.polje_izpodrinjenih1.create_oval(0.2*d, (6.45 - h)*d - 5 * h, 1.2*d, (7.45 - h)*d - 5 * h, tag=Gui.TAG_FIGURA, fill = barva)
            self.izpodrinjeni_id.append((barva,id))

    def prebarvaj_krogce(self):
        """Prebarva krogce, ta metoda se pokliče, če zamenjamo barvo igralca."""
        for i in range(len(self.igra.plosca)):
             for j in range(len(self.igra.plosca[i])):
                 if self.igra.plosca[i][j] is not None:
                     self.okno.itemconfig(self.matrika_id[i][j], fill = self.igra.plosca[i][j])
        for x in range(len(self.igra.izpodrinjeni)):
            (barva, id) = self.izpodrinjeni_id[x]
            self.izpodrinjeni_id[x] = (self.igra.izpodrinjeni[x], id)
            if self.igra.izpodrinjeni[x] == self.igra.pripadajoca_barva(IGRALEC_1):
                self.polje_izpodrinjenih2.itemconfig(id, fill = self.igra.izpodrinjeni[x])
            else:
                self.polje_izpodrinjenih1.itemconfig(id, fill = self.igra.izpodrinjeni[x])

    def spremeni_barvo1(self, barva):
        if self.igra.plosca == self.igra.ustvari_plosco():
            if barva == self.igra.barva_igralca_2:
                tkinter.messagebox.showwarning("Menjava barve ni možna", "Ne moreta biti oba igralca iste barve!")
                pass
            else:
                mozne_barve = ["yellow", "black", "green", "red", "blue", "cyan", "magenta"]
                mozne_barve.remove(self.igra.barva_igralca_2)
                mozne_barve.remove(barva)
                self.igra.barva_izbranih = random.choice(mozne_barve)
                if "blue" in mozne_barve:
                    mozne_barve.remove("blue")
                if "black" in mozne_barve:
                    mozne_barve.remove("black")
                if "yellow" in mozne_barve:
                    mozne_barve.remove("yellow")
                self.gumb.config(bg=random.choice(mozne_barve))
                self.igra.prebarvaj_krogce(IGRALEC_1, barva)
                self.igra.barva_igralca_1 = barva
                self.prebarvaj_krogce()
                if self.igra.na_potezi == IGRALEC_1:
                    self.napis.set("Na potezi je {}.".format(prevod_barve(self.igra.barva_igralca_1)))
        else:
            tkinter.messagebox.showwarning("Menjava barve ni možna", "Menjava barve med igro ni možna!")

    def spremeni_barvo2(self, barva):
        if self.igra.plosca == self.igra.ustvari_plosco():
            if barva == self.igra.barva_igralca_1:
                tkinter.messagebox.showwarning("Menjava barve ni možna", "Ne moreta biti oba igralca iste barve!")
                pass
            else:
                mozne_barve = ["yellow", "black", "green", "red", "blue", "cyan", "magenta"]
                mozne_barve.remove(self.igra.barva_igralca_1)
                mozne_barve.remove(barva)
                self.igra.barva_izbranih = random.choice(mozne_barve)
                if "blue" in mozne_barve:
                    mozne_barve.remove("blue")
                if "black" in mozne_barve:
                    mozne_barve.remove("black")
                if "yellow" in mozne_barve:
                    mozne_barve.remove("yellow")
                self.gumb.config(bg=random.choice(mozne_barve))
                self.igra.prebarvaj_krogce(IGRALEC_2, barva)
                self.igra.barva_igralca_2 = barva
                self.prebarvaj_krogce()
                if self.igra.na_potezi == IGRALEC_2:
                    if self.igra.plosca == self.igra.ustvari_plosco():
                        self.napis.set("Igro začne {} igralec.".format(prevod_barve(self.igra.barva_igralca_2)))
                    else:
                        self.napis.set("Na potezi je {}.".format(prevod_barve(self.igra.barva_igralca_2)))
        else:
            tkinter.messagebox.showwarning("Menjava barve ni možna", "Menjava barve med igro ni možna!")

    def undo(self,event):
        if self.igra.plosca != self.igra.ustvari_plosco():
            if type(self.igralec_1) == type(self.igralec_2):
                (plosca, na_potezi, izpodrinjeni) = self.igra.razveljavi()
                for i in range(len(plosca)):
                    for j in range(len(plosca[i])):
                        if plosca[i][j] is not None:
                            self.okno.itemconfig(self.matrika_id[i][j], fill = plosca[i][j])
                self.polje_izpodrinjenih1.delete(Gui.TAG_FIGURA)
                self.polje_izpodrinjenih2.delete(Gui.TAG_FIGURA)
                stevec = 0
                d = Gui.VELIKOST_POLJA
                for krogec in izpodrinjeni:
                    if krogec == self.igra.barva_igralca_1:
                        prvi += 1
                        h = stevec - 1
                        self.polje_izpodrinjenih2.create_oval(0.2*d, (6.45 - h)*d - 5 * h, 1.2*d, (7.45 - h)*d - 5 * h, tag=Gui.TAG_FIGURA, fill = self.igra.barva_igralca_1)
                    elif krogec == self.igra.barva_igralca_2:
                        h = len(self.izpodrinjeni) - stevec - 1
                        self.polje_izpodrinjenih1.create_oval(0.2*d, (6.45 - h)*d - 5 * h, 1.2*d, (7.45 - h)*d - 5 * h, tag=Gui.TAG_FIGURA, fill = self.igra.barva_igralca_2)
                if na_potezi == 1:
                    self.igra.na_potezi = IGRALEC_1
                    self.napis.set("Na potezi je {}.".format(prevod_barve(self.igra.barva_igralca_1)))
                else:
                    self.igra.na_potezi = IGRALEC_2
                    self.napis.set("Na potezi je {}.".format(prevod_barve(self.igra.barva_igralca_2)))
        else:
            pass

######################################################################
## Glavni program

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
