# Igra Abalone

Igrica pri predmetu Programiranje 2.

## Projekt

Igrico sva Tjaša Bajc in Peter Jereb naredila pri izbirnem predmetu Programiranje 2 v drugem letniku.

### Načrt in težave

Načrt dela sva sicer napisala, ampak se je sproti precej spreminjal. Bolj kot načrt sva upoštevala `# TODO` oznake in komentarje v kodi ter si sprotne načrte beležila v `.txt` datoteke. Izbrala sva zelo zanimivo igro, ki pa je tudi precej zahtevna (tako za resno igranje kot s programerskega vidika). Igre nama ni uspelo narediti tako dobro, kot bi želela, ampak sva se pri delu veliko naučila. Če bi bilo potrebno podoben projekt ponoviti (s to ali drugo igro), bi imela veliko manj težav in delo bi šlo hitreje.

Glavna možna izboljšava bi bila bolj "pametna" igra računalniškega igralca. Zaradi kompleksnosti igre je mogočih potez zelo veliko, kar upočasnjuje razmišljanje računalnika in onemogoča večjo globino. Mogoče bi pomagalo alfa-beta rezanje, ampak nama je zmanjkalo časa za implementacijo.

Manj pomembna (ampak zanimiva) nadgradnja bi bila možnost izbire alternativne začetne pozicije (glej povezavo spodaj).

## Igra

Abalone je namizna miselna igra za dva igralca. Fizična igralna plošča ima obliko šestkotnika z 61 polji (plitve vdolbinice), po katerih premikamo črne in bele kroglice, ob robovih šestkotnika pa je žleb, v katerega se ujamejo izrinjene kroglice. Vsak igralec začne z 10 kroglicami svoje barve, za zmago pa je potrebno iz plošče izriniti 6 nasprotnikovih kroglic. Za lažjo predstavo predlagava obisk katere od spletnih strani, na primer [Wikipedije](https://en.wikipedia.org/wiki/Abalone_(board_game)). 

Začetna postavitev ni natančno določena. Najbolj standardno sva uporabila v najini igri, na turnirjih pa se uporabljajo še mnoge, mnoge druge. Na [francoski Wikipediji](https://fr.wikipedia.org/wiki/Abalone_(jeu)) so lepo prikazane številne začetne postavitve (znanje francoščine za razumevanje ni potrebno) in več informacij o igri (ki je sicer francoskega izvora). Pravila igre povzemava spodaj, na prej omenjenih straneh pa so na voljo tudi grafični prikazi mogočih potez.

### Pravila

Začne črni igralec (praviloma spodnja pozicija na plošči). Potezo sestavlja premik ene, dveh ali treh (kolinearnih) sosednih kroglic v isto smer za eno polje. Premik je mogoč v katero koli od šestih smeri, če nas ne ovirajo druge kroglice ali rob plošče. Če kroglice potiskamo vzdolž premice, ki povezuje središča kroglic, lahko potisnemo tudi nasprotnikove kroglice, pri čemer veljajo dodatne omejitve.

Potisk je mogoč le, če je nasprotnikovih kroglic, ki jih želimo premakniti, strogo manj kot naših. Torej, ali z dvema svojima potisnemo eno nasprotnikovo, ali pa s tremi svojimi potisnemo eno ali dve nasprotnikovi. Na koncu potisnjenih nasprotnikovih kroglic mora biti prazno polje, torej v situaciji (BELI, BELI, BELI, ČRNI, BELI) beli ne more potisniti črne kroglice, ker za njo ni niti prazno polje niti rob plošče.

## Datoteke

Spodaj so napisana navodila za delo z igrico in pregled datotek in njihove vsebine.

### Navodila

Odpremo datoteko `uporabniski_vmesnik.py`. Privzeti način igranja je človek proti človeku, privzete barve pa so rumena, črna (za igralca) in rdeča (za izbiranje krogcev, ki jih bomo premaknili). Če želimo spremeniti barve igralcev, lahko to storimo s pomočjo menija (izbire dveh enakih barv ne dovolimo iz očitnih razlogov). Ob izbiri barv se bo naključno izbrala barva za označevanje krogcev, tako da je igra vsakič malo drugačna. V meniju `Nova igra` lahko spremenimo tip igralcev (računalnik, človek).

Ko smo izbrali igralca in/ali spremenili barve, s klikom na gumb `Začni!` začnemo igro. Tedaj računalnik prične izbirati potezo (če je prvi na vrsti), človeškemu igralcu dovolimo izbiranje krogcev (leva miškina tipka) in premikanje (desna miškina tipka), onemogočimo pa spreminjanje barv. Napis nad ploščo pove, kdo je trenutno na potezi. Krogci, ki so bili med igro izrinjeni s plošče, se pojavijo v stranskih okvirčkih. Ko je izrinjen šesti krogec določene barve, se prikaže obvestilo o zmagovalcu.

Računalniški igralec deluje s pomočjo algoritma minimax. Privzeta globina je 2.

Povzetek navodil in seznam tipk, ki jih lahko uporabljamo, sta dostopna v meniju `Informacije`.

### Kratki opisi posameznih datotek

* `uporabniski_vmesnik.py`

Izrisuje spremembe na igralni plošči, omogoča menjavo načina igranja in barv igralcev, začne in konča igro. Poskrbi za izpis okna z opozorilom, če je to potrebno
* `logika_igre.py`

Hrani matriko, ki predstavlja igralno ploščo in jo spreminja skladno z odigranimi potezami. Vsebuje tudi seznam izbranih krogcev in zgodovino odigranih potez. Preverja različne stvari - ali je mogoče izbrati ta krogec, ali je mogoč premik krogcev na želeno polje, ali je bil krogec izrinjen s plošče in podobno, ter premembe sporoča uporabniškemu vmesniku. Naredi tudi seznam vseh mogočih potez, ki ga potrebuje računalniški igralec (oziroma algoritem minimax).
* `clovek.py` in `racunalnik.py`

Predstavljata igralca v igri. Računalnik za izbiro poteze kliče algoritem minimax. 
* `minimax.py`

Vsebuje glavno metodo minimax za iskanje najboljše poteze. Pri tem uporablja cenilko (v najinem primeru `vrednost_pozicije`), ki vzame kopijo igralne plošče in na njen preizkuša učinek različnih potez na vrednost igre. Cenilka deluje tako, da pregleda vse možne smeri na plošči in v vsaki posamezni smeri išče pomembne pozicije krogcev (dobre in slabe).


