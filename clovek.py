######################################################################
## Igralec človek

class Clovek():
    def __init__(self, gui):
        self.gui = gui

    def igraj(self):
        # Smo na potezi. Zaenkrat ne naredimo nič, ampak
        # čakamo, da bo uporanik kliknil na ploščo. Ko se
        # bo to zgodilo, nas bo Gui obvestil preko metode
        # klik.
        pass

    def preveri_potezo(self):
        # Človek ne uporablja minimaxa
        pass

    def prekini(self):
        # To metodo kliče GUI, če je treba prekiniti razmišljanje.
        # Človek jo lahko ignorira.
        pass

    def oznaci(self, p):
        # Označimo krogce. Če to označevanje ni veljavno, se ne bo zgodilo nič.
        self.gui.oznacevanje(p)

    def premakni(self, izbrani, p):
        # Povlečemo potezo. Če ni veljavna, se ne bo zgodilo nič.
        self.gui.povleci_potezo(izbrani, p)
