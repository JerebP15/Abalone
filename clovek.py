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

    def prekini(self):
        # To metodo kliče GUI, če je treba prekiniti razmišljanje.
        # Človek jo lahko ignorira.
        pass

    def oznaci(self, p):
        # Povlečemo potezo. Če ni veljavna, se ne bo zgodilo nič.
        print('ČLOVEK :: oznaci - zacetek')
        self.gui.oznacevanje(p)
        print('ČLOVEK :: oznaci - konec')

    def premakni(self, p):
        # Povlečemo potezo. Če ni veljavna, se ne bo zgodilo nič.
        #self.gui.premikanje(p)
        print('ČLOVEK :: premakni - zacetek')
        self.gui.povleci_potezo(p)
        print('ČLOVEK :: premakni - koneco')

