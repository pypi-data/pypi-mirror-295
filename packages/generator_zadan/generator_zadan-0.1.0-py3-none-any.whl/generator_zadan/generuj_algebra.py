# noinspection PyUnresolvedReferences
import generatory

import babel.dates  # do ładnego generowania daty
import codecs  # dla kodowania utf-8
import datetime  # do pobierania daty
import multiprocessing
import os
from pathlib import Path  # do obsługi plików
import sys  # do wysyłania komunikatów w czerwonym kolorze
import textwrap
import time
# noinspection PyUnresolvedReferences
import random

# Todo: zmienić arg na zadanie: str, licznik: int zamiast art[0] i arg[1]
def zadanie(arg):  # Śmieszne to przekazywanie funkcji jako stringa. eval nie działa wewnątrz pool (zasięg zmiennych)
    start = time.time()
    # print('Początek', arg)
    kolor = (((arg[1] % 13) // 7) * 10 + ((arg[1] % 13) % 7))
    print(
        ' |'*(kolor if kolor < 7 else kolor - 3),
        f'\33[{31 + kolor }m{arg[1]} - Start:  '
        + f'{arg[0]}'.replace('generatory.', '') + '\033[0m')
    wynik = eval(
        arg[0])  # bez tego eval funkcja się kopiuje a nie uruchamia. I początek i koniec wyświetlają się razem.
    # print(wynik)
    # print('Koniec', arg[0])
    dlugosc_polecenia = len(
        f'zadanie nr {arg[1]} - {arg[0]}'.replace('generatory.', ''))
    # print(dlugosc_polecenia)
    print(
        ' |' * (kolor if kolor < 7 else kolor - 3),
        f'\33[{31 + kolor}m{arg[1]} - Koniec: '
        + f'{arg[0]}'.replace('generatory.', '')
        + '-'*(100-dlugosc_polecenia) + '--'*(12-(kolor if kolor < 7 else kolor - 3))
        + f': {(time.time() - start):.3f} sekund' + '\033[0m')
    return wynik


def tekst(arg):  # może wystarczy print w pool.map_async? Ale tu można ewentualnie modyfikować wszystkie.
    # print(arg)
    return arg


def dodaj_zadanie(plik, zadanie, warstwa):
    polecenie, rozwiazanie = zadanie
    polecenie = '\\tcbitem ' + polecenie + '\n'
    polecenie = textwrap.indent(polecenie, prefix='\t\t')
    rozwiazanie = f'\\zOdpowiedziami{{\\kolorodpowiedzi}}{{ocg{warstwa}}}\n\t{{{rozwiazanie}}}\n\n'
    rozwiazanie = textwrap.indent(rozwiazanie, prefix='\t\t\t')
    plik.write(polecenie + rozwiazanie)


def generuj_algebra(nazwa_pliku: str = 'Algebra',
                    ile_zadan: int = 10,
                    kolor_odpowiedzi: str = 'red',
                    gotowiec: bool = True):

    wyniki = list(range(ile_zadan * 100))  # tu jest duży zapas - dopracować - 50 oznacza ile mogłoby być typów zadań
    print('\33[31m' + f'Używamy {multiprocessing.cpu_count() - 1} wątków' + '\33[0m')
    n = iter(wyniki)
    licznik = 1

    pool = multiprocessing.Pool(multiprocessing.cpu_count() - 1)
    wyniki[next(n)] = pool.map_async(tekst, ['\n\t\\section{Liczby zespolone}\n', ])

    wyniki[next(n)] = pool.map_async(tekst, ['\t\\subsection{Równanie liniowe}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(
        zadanie, [('generatory.rownanie_liniowe()', licznik + i)
                  for i in range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\subsection{Równanie ze sprzężeniem}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(
        zadanie, [('generatory.rownanie_ze_sprzezeniem(calkowite=True, kwadratowe=False)', licznik + i)
                  for i in range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(
        zadanie,
        [('generatory.rownanie_ze_sprzezeniem(calkowite=random.choice([False, True]), kwadratowe=False)', licznik + i)
         for i in range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(
        zadanie,
        [('generatory.rownanie_ze_sprzezeniem(calkowite=random.choice([False, True]), kwadratowe=True)', licznik + i)
         for i in range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\subsection{Obszar na płaszczyźnie zespolonej}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.obszar_zespolony(typ=1, nr_zadania={licznik + i})', licznik + i)
                  for i in range(ile_zadan // 2)])
    licznik += ile_zadan // 2
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.obszar_zespolony(typ=2, nr_zadania={licznik + i})', licznik + i)
                  for i in range(ile_zadan // 2)])
    licznik += ile_zadan // 2
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.obszar_zespolony(typ=3, nr_zadania={licznik + i})', licznik + i)
                  for i in range(ile_zadan // 2)])
    licznik += ile_zadan // 2
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.obszar_zespolony(typ=5, nr_zadania={licznik + i})', licznik + i)
                  for i in range(ile_zadan // 2)])
    licznik += ile_zadan // 2
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.obszar_zespolony(typ=4, nr_zadania={licznik + i})', licznik + i)
                  for i in range(ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\subsection{Równanie kwadratowe}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(
        zadanie, [('generatory.rownanie_kwadratowe()', licznik + i)
                  for i in range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\subsection{Pierwiastek zespolony}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(
        zadanie, [('generatory.pierwiastek_zespolony(stopien=random.choice(([3] * 1 + [4] * 1)))', licznik + i)
                  for i in range(0, 2 * ile_zadan)])
    licznik += 2 * ile_zadan
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])

    wyniki[next(n)] = pool.map_async(tekst, ['\n\t\\section{Macierze}\n', ])

    wyniki[next(n)] = pool.map_async(tekst, ['\t\\subsection{Wyznacznik z parametrem}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.wyznacznik_parametr(wymiar=2)', licznik + i)
                  for i in range(0, ile_zadan // 2)])
    licznik += ile_zadan // 2
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.wyznacznik_parametr(wymiar=3, gotowiec={gotowiec})', licznik + i)
                  for i in range(ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.wyznacznik_parametr(wymiar=4, gotowiec={gotowiec})', licznik + i)
                  for i in range(ile_zadan // 2)])
    licznik += ile_zadan // 2
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\subsection{Macierz odwrotna z parametrem}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.macierz_odwrotna_parametr(wymiar=2)', licznik + i)
                  for i in range(0, ile_zadan // 2)])
    licznik += ile_zadan // 2
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.macierz_odwrotna_parametr(wymiar=3, gotowiec={gotowiec})', licznik + i)
                  for i in range(ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.macierz_odwrotna_parametr(wymiar=4, gotowiec={gotowiec})', licznik + i)
                  for i in range(ile_zadan // 2)])
    licznik += ile_zadan // 2
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\subsection{Równanie macierzowe}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.rownanie_macierzowe()', licznik + i)
                  for i in range(ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\subsection{Rząd macierzy}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.rzad_macierzy()', licznik + i)
                  for i in range(ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\subsection{Wartości własne i wektory własne}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.wartosci_wlasne(wymiar=2, zespolone=random.choice(([True, False])))', licznik + i)
                  for i in range(ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.wartosci_wlasne(wymiar=3, zespolone=random.choice(([True, False])))', licznik + i)
                  for i in range(ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.wartosci_wlasne(wymiar=4, zespolone=False)', licznik + i)
                  for i in range(ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\subsection{Diagonalizacja macierzy}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.diagonalizacja_macierzy(wymiar=2)', licznik + i)
                  for i in range(ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.diagonalizacja_macierzy(wymiar=3)', licznik + i)
                  for i in range(ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.diagonalizacja_macierzy(wymiar=4)', licznik + i)
                  for i in range(ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.diagonalizacja_macierzy_z_wielokrotnym_wartosciami_wlasnymi(wymiar=3)', licznik + i)
                  for i in range(ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])

    wyniki[next(n)] = pool.map_async(tekst, ['\n\t\\section{Układy równań}\n', ])

    wyniki[next(n)] = pool.map_async(tekst, ['\t\\subsection{Układy Cramera}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.uklad_Cramera(wymiar=2)', licznik + i)
                  for i in range(0, ile_zadan // 2)])
    licznik += ile_zadan // 2
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.uklad_Cramera(wymiar=3)', licznik + i)
                  for i in range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.uklad_Cramera(wymiar=4)', licznik + i)
                  for i in range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.uklad_Cramera(wymiar=5)', licznik + i)
                  for i in range(0, ile_zadan // 2)])
    licznik += ile_zadan // 2
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.uklad_Cramera(wymiar=6, gotowiec={gotowiec})', licznik + i)
                  for i in range(0, ile_zadan // 2)])
    licznik += ile_zadan // 2
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.uklad_Cramera(wymiar=7, gotowiec={gotowiec})', licznik + i)
                  for i in range(0, ile_zadan // 2)])
    licznik += ile_zadan // 2
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\subsection{Metoda Gaussa}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.uklad_rownan_nieoznaczony()', licznik + i)
                  for i in range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])

    wyniki[next(n)] = pool.map_async(tekst, ['\n\t\\section{Geometria analityczna}\n', ])

    wyniki[next(n)] = pool.map_async(tekst, ['\t\\subsection{Kąty w trójkącie}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.katy_w_trojkacie(prosty=False, calkowite=True)', licznik + i)
                  for i in range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.katy_w_trojkacie(prosty=True, calkowite=False)', licznik + i)
                  for i in range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.katy_w_trojkacie(prosty=False, calkowite=False)', licznik + i)
                  for i in range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\subsection{Pole trójkąta i wysokości}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.pole_trojkata(calkowite=random.choice([False, True]))', licznik + i)
                  for i in range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\subsection{Równanie prostej}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.rownanie_prostej()', licznik + i)
                  for i in range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\subsection{Równanie płaszczyzny}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.rownanie_plaszczyzny()', licznik + i)
                  for i in range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\subsection{Punkt symetryczny względem płaszczyzny}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.punkt_symetryczny_do_plaszczyzny()', licznik + i)
                  for i in range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\subsection{Punkt symetryczny względem prostej}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.punkt_symetryczny_do_prostej()', licznik + i)
                  for i in range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\subsection{Odległość prostych skośnych}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(
        zadanie, [(f'generatory.odleglosc_prostych_skosnych(gotowiec={gotowiec})', licznik + i)
                  for i in range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])

    print(f'Zadań wyszło: {licznik - 1}')
    pool.close()
    pool.join()
    if not os.path.exists('wygenerowane'):
        os.makedirs('wygenerowane')
        print(" ! Tworzę katalog wygenerowane ", file=sys.stderr)
    plik = Path(
        'wygenerowane//' + nazwa_pliku + '.tex')
    plik.touch(exist_ok=True)
    plik = codecs.open(plik, "w", "utf8")
    plik.write(('% !TeX spellcheck = pl_PL-Polish\n'
                '\\documentclass[a4paper,10pt]{article}\n'  # można zmieniać rozmiar czcionki
                '\\linespread{1.3} %odstepy miedzy liniami\n'
                '\\usepackage[a4paper, lmargin=2cm, rmargin=2cm, tmargin=2cm, bmargin=2cm]{geometry}\n'
                '\\usepackage{amsfonts}\n'
                '\\usepackage{amsmath}\n'
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

    warstwa = 1  # od zera rozjeżdza się z numeracją obrazów
    for i in range(len(wyniki)):  # wynik to lista stringów i krotek
        try:
            # print(len(wyniki[i].get()))
            if len(wyniki[i].get()) == 1:
                plik.write(wyniki[i].get()[0])
            else:
                for k in wyniki[i].get():
                    dodaj_zadanie(plik, k, warstwa)
                    warstwa += 1
        except Exception:
            pass

    plik.write('\n\\end{document}')
    plik.close()

    puste = 0  # to do szacowania rozmiaru listy wyników
    for i in range(len(wyniki)):  # wynik to lista stringów i krotek
        try:
            wyniki[i].get()
        except Exception:
            puste += 1
    print('Puste miejsca w wynikach: ', puste)
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':  # średni czas generowania z dnia 30.01.2024:  241s, z gotowcami 140s.
    czas = list()
    ile_petli = 1  # to tylko do testowania średniego czasu generowania
    gotowce = True

    for i in range(1, ile_petli + 1):
        print('Rozpoczynam pętlę nr: ', i)
        start_time = time.time()
        generuj_algebra(nazwa_pliku='Algebra', ile_zadan=10, kolor_odpowiedzi='red', gotowiec = gotowce)
        czas.append(time.time() - start_time)
    print(czas)
    print('Średni czas generowania: ', sum(czas)/len(czas))
