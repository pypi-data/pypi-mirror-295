import codecs  # dla kodowania utf-8
import datetime  # do pobierania daty
import os  # do tworzenia katalogów
import random
import sys  # do wysyłania komunikatów w czerwonym kolorze
import textwrap
from pathlib import Path  # do obsługi plików

import babel.dates  # do ładnego generowania daty
from tqdm import trange

import generatory

kierunek = 'generuj'  # domyślnie zestaw_sekcje
semestr = ''  # w stylu 'semestr 1'
przedmiot = 'Test_zadania'
kolokwium = ''  # w stylu 'kolokwium 1'
# grupa = 1
data = ''  # w stylu: 01 grudnia 2022 - będzie w nagłówku wydruku
# ile_zestawow = 1  # niepotrzebne
kolor_odpowiedzi = 'blue'


def dodaj_zadanie(plik, zadanie, warstwa):
    polecenie, rozwiazanie = zadanie
    polecenie = '\\tcbitem ' + polecenie + '\n'
    polecenie = textwrap.indent(polecenie, prefix='\t\t')
    rozwiazanie = f'\\zOdpowiedziami{{\\kolorodpowiedzi}}{{ocg{warstwa}}}\n\t{{{rozwiazanie}}}\n\n'
    rozwiazanie = textwrap.indent(rozwiazanie, prefix='\t\t\t')
    plik.write(polecenie + rozwiazanie)
    global nr_warstwy
    nr_warstwy += 1


if not os.path.exists('wygenerowane'):
    os.makedirs('wygenerowane')
    print(" ! Tworzę katalog wygenerowane ", file=sys.stderr)
plik = Path(
    'wygenerowane//' + kierunek + '-' + przedmiot + semestr + kolokwium + '.tex')
plik.touch(exist_ok=True)
plik = codecs.open(plik, "w", "utf8")
plik.write(('% !TeX spellcheck = pl_PL-Polish\n'
            '\\documentclass[a4paper,10pt]{article}\n'  # można zmieniać rozmiar czcionki
            '\\linespread{1.3} %odstepy miedzy liniami\n'
            '\\usepackage[a4paper, lmargin=2cm, rmargin=2cm, tmargin=2cm, bmargin=2cm]{geometry}\n'
            '\\usepackage{amsfonts}\n'
            '\\usepackage{amsmath}\n'
            '\\usepackage{animate}\n'
            '\\usepackage{color}\n'
            '\\usepackage{enumitem}\n'
            '\\usepackage{fancyhdr}\n'
            '\\usepackage{float}\n'
            '\\usepackage{graphicx}\n'  # do pdf
            '\\usepackage[colorlinks=true,linkcolor=blue]{hyperref}\n'
            '\\usepackage{ifthen}\n'
            '\\usepackage[utf8]{inputenc}\n'
            '\\usepackage{lmodern}\n'
            # '\\def\\pdftexversion{120}'  # eliminacja problemów przy kompilowaniu - niepotrzebne przy pdf-ach
            '\\usepackage{ocgx}\n'
            # '\\usepackage{pgf}\n'  # niepotrzebne gdy importujemy pdf-y
            '\\usepackage{polski}\n\n'
            '\\usepackage{tcolorbox}\n'
            '\\tcbuselibrary{most}\n'
            '\\tcbuselibrary{skins}\n'
            '\\tcbuselibrary{raster}\n'
            '% brak - bez odpowiedzi i bez miejsca, white - bez odpowiedzi z miejscem, red = odpowiedzi ukryte ale dostepne\n'
            f'\\newcommand{{\\kolorodpowiedzi}}{{{kolor_odpowiedzi}}}\n\n'
            '\\renewcommand{\\footrulewidth}{0.4pt}% linia pozioma na końcu strony - default is 0pt\n'
            '\\DeclareFontShape{OMX}{cmex}{m}{n}\n'
            '    {<-7.5> cmex7\n'
            '    <7.5-8.5> cmex8\n'
            '    <8.5-9.5> cmex9\n'
            '    <9.5-> cmex10}{}\n'
            '\\DeclareSymbolFont{largesymbols}{OMX}{cmex}{m}{n}\n\n'
            '\n'
            '\\newcommand{\\ukryte}{1}  % domyślnie odpowiedzi są do pokazywania po kliknięciu\n'
            '\\ifthenelse{\\equal{\\kolorodpowiedzi}{red}}  % ukrywamy od pokazywania gdy kolor jest red\n'
            '\t{\\renewcommand{\\ukryte}{0}}{}\n\n'
            '\\newcommand{\\zOdpowiedziami}[3]{\n'
            '\t\\ifthenelse{\\equal{#1}{brak}}{}{\n'
            '\t\t\\ifthenelse{\\equal{#1}{white}}{\\vphantom{#3}}{\\tcbox[rozwiazanie]{\n'
            '\t\t\t\\switchocg{#2}{\\textcolor{\\kolorodpowiedzi}{Rozwiązanie: }}\n'
            '\t\t\t\t\\begin{ocg}{Odp. \\thesubsection.\\thetcbrasternum}{#2}{\\ukryte}\n'  # warstwy nazywane numerem
            '\t\t\t\t\t\\textcolor{\\kolorodpowiedzi}{#3}\n'
            '\t\t\t\t\\end{ocg}}}}}\n\n'
            '\\tcbset{\n'
            '\tzadanie/.style={size=small,\n'
            '\t\traster columns=1,\n'
            '\t\tcolframe=green!50!black,\n'
            '\t\tcolback=green!2!white,\n'
            '\t\tcolbacktitle=green!40!black,\n'
            '\ttitle={Zadanie \\thesubsection.\\thetcbrasternum}}\n}\n'
            '\\tcbset{\n'
            '\trozwiazanie/.style={size=small, capture=minipage}\n}\n'
            '\\graphicspath{{../pics}}\n'
            '\\begin{document}\n'
            '    \\author{\\tcbox[colframe=blue!50!black,colback=blue!2!white,colbacktitle=blue!40!black]\n'
            '        {\\Large Adam Bohonos}}\n'
            '    \\title{\\tcbox[colframe=green!50!black,colback=green!2!white,colbacktitle=green!40!black]\n'
            '        {\\Huge Analiza - zadania uzupełniające}}\n'
            '    \\date{\\tcbox[colframe=green!50!black,colback=green!2!white,colbacktitle=green!40!black]\n'
            '        {\\small ' +
            babel.dates.format_datetime(datetime.datetime.now(), "d MMMM yyyy", locale='pl_PL') + '}}\n'
                                                                                                  '    \\maketitle\n'
                                                                                                  '    \\pagestyle{fancy}\n'
                                                                                                  '    \\setlength{\\headheight}{27.29453pt}\n'
                                                                                                  '    \\fancyfoot[R]{\\tiny\\textbf{ ' +
            babel.dates.format_datetime(datetime.datetime.now(), "d MMMM yyyy, HH:mm", locale='pl_PL') + '}}\n' +
            # '    \\hspace{1cm}' + '\n\n'
            '    \\tableofcontents'
            ))

ile_zadan = 20
nr_warstwy = 0  # do ukrywania odpowiedzi - w każdej funkcji musi być o jeden większy
Fourier_bez_wykresu = True

plik.write('\n\t\\section{Funkcje wielu zmiennych}\n')
plik.write('\t\\subsection{Całka podwójna}\n')
plik.write(r'    \begin{tcbitemize}[zadanie] ' + '\n')
for _ in trange(ile_zadan, desc='Całka podwójna z wykresami'):
    dodaj_zadanie(plik, generatory.calka_podwojna(typ=2, nr_zadania=nr_warstwy), nr_warstwy)
    # dodaj_zadanie(plik, generatory.szereg_Fouriera(typ_l=random.randint(0,4), typ_p=random.randint(0,4), nr_zadania=nr_warstwy), nr_warstwy)
# dodaj_zadanie(plik, generatory.styczna_normalna(typ=1), nr_warstwy)
plik.write(r'    \end{tcbitemize}' + '\n')

plik.write(r'\end{document}' + '\n')
plik.close()

# \usepackage{animate}
# \graphicspath{{../pics}}
# \animategraphics[height=6cm,controls=true,autoplay,loop]{1}
# 	{szereg_Fouriera_1}{0}{10}
