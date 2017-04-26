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
# TODO Bug da če najprej izbereš spodnji od 2 krogcev na diagonali ju ne moreš premakniti levo navzdol


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
        self.igra = None # Kot pri profesorju
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
        self.polje_izpodrinjenih1 = tkinter.Canvas(master, width=2*Gui.VELIKOST_POLJA, height=7*Gui.VELIKOST_POLJA)
        self.polje_izpodrinjenih1.grid(row=1, column=0)
        self.polje_izpodrinjenih2 = tkinter.Canvas(master, width=2*Gui.VELIKOST_POLJA, height=7*Gui.VELIKOST_POLJA)
        self.polje_izpodrinjenih2.grid(row=1, column=2)

        # Črte na igralnem polju
        self.narisi_crte()
        #TODO to gre v Igra
        self.premik = False
        self.izpodrinjeni = []

        # Naročimo se na dogodke
        self.okno.bind("<Button-1>", self.levi_klik)
        self.okno.bind("<Button-3>", self.desni_klik)
        # self.okno.bind("<Button-2>", self.razveljavi)
        #TODO press, release
        #self.okno.bind("<ButtonPress-1>", self.okno_klik)
        #self.okno.bind("<ButtonRelease-1>", self.oznacevanje_krogcev)

        # Prični igro
        self.zacni_igro(Clovek(self), Clovek(self))


    def risi_plosco(self):
        d = Gui.VELIKOST_POLJA
        matrika = self.igra.plosca
        for i in range(len(matrika)):
             for j in range(len(matrika[i])):
                 if matrika[i][j] is not None:
                     id = self.okno.create_oval((i - j*0.5)*d + 2*d, (3**0.5)*0.5*j*d, (i - j*0.5)*d + 3*d, (3**0.5)*0.5*j*d + d, fill=matrika[i][j].barva)
                     matrika[i][j].id = id
                     
    def levi_klik(self, event):
        """Obdelamo levi klik - oznacevanje krogcev."""
        #print('GUI :: levi_klik - zacetek')
        p = self.poisci_polje(event)
        (i,j) = p
        print(self.igra.mozni_izbrani())
        if i is not None and j is not None:
            igralec = self.igra.na_potezi
            if igralec == IGRALEC_1:
                self.igralec_1.oznaci(p)
            elif igralec == IGRALEC_2:
                self.igralec_2.oznaci(p)
            else:
                pass
        #print('GUI :: levi_klik - konec')

    def oznacevanje(self, p):
        """Če smo izbrali (svoje) neoznačene krogce, se označijo.
           Če smo izbrali že označene krogce, se odznačijo in spet postanejo barvni."""
        #print('GUI :: oznacevnanje - zacetek')
        igralec = self.igra.na_potezi
        odziv = self.igra.oznacevanje(p, igralec)
        if odziv == "oznaci":
            #print('GUI :: oznacevnanje - sedaj bomo OZNACILI krogec')
            self.oznaci_krogec(p)
        elif odziv == "odznaci":
            #print('GUI :: oznacevnanje - sedaj bomo ODZNACILI krogec')
            self.odznaci_krogec(p)
        else:
            pass
        #print('GUI :: oznacevnanje - konec')

    def razveljavi(self,event):
        (plosca, izpodrinjeni) = self.igra.undo()
        print(plosca, izpodrinjeni)
        #TODO Dokončati to metodo
                
    def desni_klik(self, event):
        """Obdelamo desni klik - premikanje krogcev."""
        #print('GUI :: desni_klik - zacetek')
        p = self.poisci_polje(event)
        (i,j) = p
        if i is not None and j is not None and len(self.igra.izbrani) != 0:
            igralec = self.igra.na_potezi
            if igralec == IGRALEC_1:
                self.igralec_1.premakni(p)
            elif igralec == IGRALEC_2:
                self.igralec_2.premakni(p)
            else:
                pass

    def povleci_potezo(self, p):
        print('GUI :: povleci_potezo - zacetek')
        igralec = self.igra.na_potezi
        (premik, izrinjeni) = self.igra.premikanje(p)
        if premik is not None:
            for polje in premik:
                (x,y,barva) = polje
                self.okno.itemconfig(self.igra.plosca[x][y].id, fill = barva)
            if len(izrinjeni) != len(self.izpodrinjeni):
                self.izpodrinjeni.append(izrinjeni[-1])
                self.narisi_izpodrinjene(izrinjeni[-1])
        r = self.igra.povleci_potezo(p)
        if r is None:
            pass
        else:
            if r == NI_KONEC:
                print('V POVLECI_POTEZO v GUI smo ugotovili, da ni konec.')
                # Igra se nadaljuje
                if self.igra.na_potezi == IGRALEC_1:
                    self.napis.set("Na potezi je {}.".format(self.igra.barva_igralca_1))
                    self.igralec_1.igraj()
                elif self.igra.na_potezi == IGRALEC_2:
                    self.napis.set("Na potezi je drugi.")
                    self.igralec_2.igraj()
            else:
                # Igre je konec, koncaj
                self.koncaj_igro(r)

    def razveljavi(self,event):
        (plosca, izpodrinjeni) = self.igra.undo()
        print(plosca, izpodrinjeni)
        #TODO Dokončati to metodo

    # TODO napiši metodo Povleci potezo(zdaj to delno dela okno_klik)
    
    def poisci_polje(self, event):
        """Vrne polje, na katero smo kliknili."""
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

    def oznaci_krogec(self, p):
        """Izbrani krogec pobarva rdeče."""
        (i, j) = p
        self.okno.itemconfig(self.igra.plosca[i][j].id, fill='red')
        #print(self.plosca[i][j])


    def odznaci_krogec(self, p):
        """Obratno kot označi krogec."""
        (i, j) = p         
        self.okno.itemconfig(self.igra.plosca[i][j].id, fill=self.igra.plosca[i][j].barva)
        #print(self.plosca[i][j])

    #Mislim da se to nikjer ne uporabi in lahko izbriševa
    def zacni_premik_krogcev(self,event):
        if self.premik is False:
            self.premik = True
        else:
            self.premik = False

    def narisi_izpodrinjene(self,barva):
        d = Gui.VELIKOST_POLJA
        stevec = 0
        for barva in self.izpodrinjeni:
            if barva == self.igra.barva_igralca_1:
                stevec += 1
        if barva == self.igra.barva_igralca_1:
            h = stevec - 1
            self.polje_izpodrinjenih1.create_oval(0.15*d, (5.5 - h)*d, 1.15*d, (6.5 - h)*d, tag=Gui.TAG_FIGURA, fill = barva)
        elif barva == self.igra.barva_igralca_2:
            h = len(self.izpodrinjeni) - stevec - 1
            self.polje_izpodrinjenih2.create_oval(0.15*d, (5.5 - h)*d, 1.15*d, (6.5 - h)*d, tag=Gui.TAG_FIGURA, fill = barva)
            
            

    def zacni_igro(self, igralec_1, igralec_2):
        """Nastavi stanje igre na zacetek igre.
           Za igralca uporabi dana igralca."""
        # Ustavimo vsa vlakna, ki trenutno razmišljajo
        self.prekini_igralce()
        # Pobrišemo tiste, ki so padli dol in narišemo začetno pozicijo
        #self.plosca.delete(Gui.TAG_FIGURA)
        #self.zacetna_pozicija
        self.igra = Igra()
        self.risi_plosco()
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
            self.napis.set("Zmagal je {} igralec.".format(self.igra.barva_igralca_1))
        elif zmagovalec == IGRALEC_2:
            self.napis.set("Zmagal je {} igralec.".format(self.igra.barva_igralca_2))
        else:
            assert False # Nekdo mora zmagati, sicer je šlo nekaj narobe in se sesujemo.
        self.izpodrinjeni = []

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
        self.okno.create_line(2.5*d, 0.8*d, 0.2*d, 4.85*d, tag=Gui.TAG_OKVIR)
        self.okno.create_line(7.5*d, 0.8*d, 9.8*d, 4.85*d, tag=Gui.TAG_OKVIR)
        self.okno.create_line(0.2*d, 4.85*d, 2.5*d, 8.85*d, tag=Gui.TAG_OKVIR)
        self.okno.create_line(2.5*d, 8.85*d, 7.5*d, 8.85*d, tag=Gui.TAG_OKVIR)
        self.okno.create_line(7.5*d, 8.85*d, 9.8*d, 4.85*d, tag=Gui.TAG_OKVIR)        
        self.polje_izpodrinjenih1.create_line(0.1*d, 0.1*d, 1.2*d, 0.1*d, tag=Gui.TAG_OKVIR)
        self.polje_izpodrinjenih1.create_line(0.1*d, 0.1*d, 0.1*d, 6.5*d, tag=Gui.TAG_OKVIR)
        self.polje_izpodrinjenih1.create_line(0.1*d, 6.5*d, 1.2*d, 6.5*d, tag=Gui.TAG_OKVIR)
        self.polje_izpodrinjenih1.create_line(1.2*d, 6.5*d, 1.2*d, 0.1*d, tag=Gui.TAG_OKVIR)
        self.polje_izpodrinjenih2.create_line(0.1*d, 0.1*d, 1.2*d, 0.1*d, tag=Gui.TAG_OKVIR)
        self.polje_izpodrinjenih2.create_line(0.1*d, 0.1*d, 0.1*d, 6.5*d, tag=Gui.TAG_OKVIR)
        self.polje_izpodrinjenih2.create_line(0.1*d, 6.5*d, 1.2*d, 6.5*d, tag=Gui.TAG_OKVIR)
        self.polje_izpodrinjenih2.create_line(1.2*d, 6.5*d, 1.2*d, 0.1*d, tag=Gui.TAG_OKVIR)
        
    def prevod_barve(self, barva):
        #TODO To bova dokončala proti koncu projekta, ko bova imela čas se ukvarjati z barvami(saj je to le lepotna izboljšava)
        if barva == "yellow":
            return "rumeni"
        elif barva == "black":
            return "črni"


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
