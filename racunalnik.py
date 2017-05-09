import threading  # za vzporedno izvajanje

from minimax import *

######################################################################
## Igralec računalnik

class Racunalnik():
    def __init__(self, gui, algoritem):
        self.gui = gui
        self.algoritem = algoritem # Algoritem, ki izračuna potezo
        self.mislec = None # Vlakno (thread), ki razmišlja

    def igraj(self):
        """Igraj potezo, ki jo vrne algoritem."""
        # Tu sprožimo vzporedno vlakno, ki računa potezo.

        # Naredimo vlakno, ki mu podamo *kopijo* igre (da ne bo zmedel GUIja):
        self.mislec = threading.Thread(
            target=lambda: self.algoritem.izracunaj_potezo(self.gui.igra.kopija()))

        # Poženemo vlakno:
        self.mislec.start()

        # Gremo preverjat, ali je bila najdena poteza:
        self.gui.okno.after(100, self.preveri_potezo)

    def preveri_potezo(self):
        """Vsakih 100ms preveri, ali je algoritem že izračunal potezo."""
        if self.algoritem.poteza is not None:
            # Algoritem je našel potezo, povleci jo, če ni bilo prekinitve
            (izbrani, p) = self.algoritem.poteza
            if type(izbrani[0]) == int:
                self.gui.igra.izbrani = [izbrani]
            else:
                self.gui.igra.izbrani = izbrani
            self.gui.povleci_potezo(p)
            # Vzporedno vlakno ni več aktivno, zato ga "pozabimo"
            self.mislec = None
        else:
            # Algoritem še ni našel poteze, preveri še enkrat čez 100ms
            self.gui.okno.after(100, self.preveri_potezo)

    def prekini(self):
        # To metodo kliče GUI, če je treba prekiniti razmišljanje.
        if self.mislec:
            logging.debug ("Prekinjamo {0}".format(self.mislec))
            # Algoritmu sporočimo, da mora nehati z razmišljanjem
            self.algoritem.prekini()
            # Počakamo, da se vlakno ustavi
            self.mislec.join()
            self.mislec = None

    def oznaci(self, p):
        # Računalnik ignorira klike
        pass
