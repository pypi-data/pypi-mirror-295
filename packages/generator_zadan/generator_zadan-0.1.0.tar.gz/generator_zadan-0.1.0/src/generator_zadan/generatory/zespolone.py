import os  # do tworzenia katalogów
import random
import sys  # do wysyłania komunikatów w czerwonym kolorze
import time  # dla testów wydajności
from fractions import Fraction

import numpy as np
import sympy as sp
from sympy import I
import warnings  # wyłącz ostrzeżenia przy generowaniu obrazów
warnings.filterwarnings('ignore')
random.seed()

# Todo: Poprawić/uzupełnić docstringi

def rownanie_liniowe(nr_warstwy: int = 0):  # na 10000 losowań było 9602 różnych

    # random.seed()
    z = sp.symbols('z', complex=True)
    wspolczynniki = [-6, -5, -4, -3, -2, -1, 2, 3, 4, 5, 6, 7, 8, 9]
    while True:
        a = [random.choice([2, 3, 4, 5, 6, 7, 8, 9]), random.choice(wspolczynniki)]
        b = [random.choice([2, 3, 4, 5, 6, 7, 8, 9]), random.choice(wspolczynniki)]
        c = [random.choice(wspolczynniki), random.choice(wspolczynniki)]
        rozwiazanie = sp.solve((a[0] + a[1] * I) * z - (b[0] + b[1] * I) * z - (c[0] + c[1] * I))
        if len(rozwiazanie) == 0:
            rozwiazanie = [0.5 + 0.5 * I]
        if (a[1] != b[1] and sp.re(rozwiazanie[0]) != 0 and sp.im(rozwiazanie[0]) != 0
                and int(sp.re(rozwiazanie[0])) == sp.re(rozwiazanie[0])
                and int(sp.im(rozwiazanie[0])) == sp.im(rozwiazanie[0])):
            break
    #    print(rozwiazanie)
    lewa_prawa = random.choice([0, 1])
    if lewa_prawa == 0:
        rownanie = str('\\left(' + str(sp.expand((a[0] + a[1] * I))) + '\\right)z = '
                       + str(sp.expand((c[0] + c[1] * I))) + '+\\left('
                       + str(sp.expand((b[0] + b[1] * I))) + '\\right)z')
    else:
        rownanie = str(str(sp.expand((c[0] + c[1] * I))) + '+\\left('
                       + str(sp.expand((b[0] + b[1] * I))) + '\\right)z = ' + '\\left('
                       + str(sp.expand((a[0] + a[1] * I))) + '\\right)z')

    rownanie = rownanie.replace('I', 'i')
    rownanie = rownanie.replace('*', '')
    rozwiazanie = str(rozwiazanie[0])
    rozwiazanie = rozwiazanie.replace('I', 'i')
    rozwiazanie = rozwiazanie.replace('*', '')
    return ('Rozwiązać równanie w zbiorze liczb zespolonych.\\ Sprawdzić rozwiązanie.\n'
            f'\t\\[\n'
            f'\t\t{rownanie}\n'
            f'\t\\]',
            f'$z={rozwiazanie}.$')
    # return [rownanie, list(rozwiazanie)]


def rownanie_kwadratowe(nr_warstwy: int = 0):  # na 2000 losowań było 194 różnych
    # random.seed()
    z = sp.symbols('z', complex=True)
    wspolczynniki = [-6, -5, -4, -3, -2, -1, 2, 3, 4, 5, 6, 7, 8, 9]
    while True:
        z1 = [random.choice(wspolczynniki), random.choice(wspolczynniki)]
        z2 = [random.choice(wspolczynniki), random.choice(wspolczynniki)]
        a = [random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9]), random.choice(wspolczynniki)]
        delta = ((a[0] + a[1] * 1j) * (-(z1[0] + z1[1] * 1j)
                                       - (z2[0] + z2[1] * 1j))) ** 2 - 4 * (a[0] + a[1] * 1j) ** 2 * (
                        z1[0] + z1[1] * 1j) * (z2[0] + z2[1] * 1j)
        if (abs(delta) < 15
                and abs((a[0] + a[1] * 1j) * (-(z1[0] + z1[1] * 1j) - (z2[0] + z2[1] * 1j))) < 15
                and np.real(delta) != 0 and np.imag(delta) != 0
                and (a[0] * (z1[0] + z2[0]) - a[1] * (z1[1] + z2[1])) != 0
                and (a[1] * (z1[0] + z2[0]) + a[0] * (z1[1] + z2[1])) != 0):
            break
    sqrt_delta = sp.sqrt(int(sp.re(delta)) + int(sp.im(delta)) * I).expand(complex=True)
    przestawiony_trojmian = sp.collect(
        sp.expand((a[0] + a[1] * I) * (z - (z1[0] + z1[1] * I)) * (z - (z2[0] + z2[1] * I))), z)
    poprawiony_trojmian = str('\\left(' + str(przestawiony_trojmian.coeff(z, 2)) +
                              '\\right)z^2 + \\left(' + str(przestawiony_trojmian.coeff(z, 1)) +
                              '\\right) z + \\left(' + str(przestawiony_trojmian.coeff(z, 0)) + '\\right)')
    rozwiazanie = sp.solve(przestawiony_trojmian)
    poprawiony_trojmian = poprawiony_trojmian.replace('I', 'i')
    poprawiony_trojmian = poprawiony_trojmian.replace('*', ' ')
    rozwiazanie[0] = str(rozwiazanie[0])
    rozwiazanie[0] = rozwiazanie[0].replace('I', 'i')
    rozwiazanie[0] = rozwiazanie[0].replace('*', ' ')
    rozwiazanie[1] = str(rozwiazanie[1])
    rozwiazanie[1] = rozwiazanie[1].replace('I', 'i')
    rozwiazanie[1] = rozwiazanie[1].replace('*', ' ')
    delta = str(delta)
    delta = delta.replace('j', 'i')
    delta = delta.replace('(', '')
    delta = delta.replace(')', '')
    return (f'Rozwiązać równanie w zbiorze liczb zespolonych.\\ Sprawdzić jedno z rozwiązań.\n'
            f'\t\\[\n'
            f'\t\t{poprawiony_trojmian}=0\n'
            f'\t\\]',
            f'$\\Delta = {delta}, \\quad '
            f'\\sqrt{{\\Delta}}=\\pm( {sp.latex(sqrt_delta)}) \\quad '
            f'z_{{1}}={rozwiazanie[0]} \\quad '
            f'z_{{2}}={rozwiazanie[1]}$')


# Todo: dołożyć wyrażenie w stylu ((1+i*sqrt(3))/2)^10 które wygeneruje 1 lub -1 lub
# Todo: 2 albo 3 do potęgi, która jest stopniem pierwiastka
def pierwiastek_zespolony(stopien=3, nr_warstwy=0):  # generuje 152 różne zadania z 3 i 4 stopniem
    if stopien == 3:
        liczba = random.choice([27 * I, -27 * I, 64 * I, -64 * I,
                                Fraction(64, 27) * I ** 4, -Fraction(64, 27) * I ** 4, Fraction(64, 27) * I,
                                -Fraction(64, 27) * I,
                                Fraction(27, 64) * I ** 4, -Fraction(27, 64) * I ** 4, Fraction(27, 64) * I,
                                -Fraction(27, 64) * I])
        # w powyższym bez I**4 pojawia się co jakiś czas błąd przy sp.latex(liczba) w odpowiedzi - nie wiem czemu.
        # liczba = (liczba**3).expand(complex=True).collect(I)
        while True:
            rozne_pierwiastki = random.choice([sp.sqrt(2), sp.sqrt(3), sp.sqrt(5)])
            a = random.choice((-1, 1))
            b = random.choice((-1, 1))
            iloraz = (liczba / (a + b * I * rozne_pierwiastki)).expand(complex=True).collect(I)
            if sp.im(iloraz) != 0 and sp.re(iloraz) != 0 and a != b and a != sp.im(iloraz):
                break
        z = sp.symbols('z', complex=True)
        rozwiazanie = sp.latex(sp.solve(z ** 3 - liczba, rational=True)).replace('[', '\{').replace(']', '\}')
        strona = random.choice((0, 1))  # do wymieszania nawiasów pod pierwiastkiem
        pierwiastek = (f'\t\\[\n'
                       f'\t\t\\sqrt[\\leftroot{{2}}\\uproot{{-4}} \\displaystyle ^{{3}}]{{\\left('
                       f'{sp.latex(iloraz) if strona == 0 else sp.latex(a + b * I * rozne_pierwiastki)} \\right)'
                       f' \\left({sp.latex(a + b * I * rozne_pierwiastki) if strona == 0 else sp.latex(iloraz)} \\right)}}\n'
                       f'\t\\]')
        return ('Wyznaczyć wszystkie zadane pierwiastki zespolone i zaznaczyć je na płaszczyźnie zespolonej\n'
                f'{pierwiastek}',
                f'$\\sqrt[\\leftroot{{2}}\\uproot{{-4}} \\displaystyle ^{{3}}]{{{sp.latex(liczba)}}} = {rozwiazanie}.$')
    if stopien == 4:
        liczba = random.choice(
            [1 + sp.sqrt(3) * I, 1 - sp.sqrt(3) * I, -1 + sp.sqrt(3) * I, -1 - sp.sqrt(3) * I,
             sp.sqrt(3) + I, sp.sqrt(3) - I, -sp.sqrt(3) + I, -sp.sqrt(3) - I,
             1 + I, 1 - I, -1 + I, -1 - I])  # te ostatnie generują łatwe liczby pod pierwiastkiem
        # print(liczba)
        liczba = (liczba ** 4).expand(complex=True).collect(I)
        while True:
            rozne_pierwiastki = random.choice([sp.sqrt(2), sp.sqrt(3), sp.sqrt(5)])
            a = random.choice((-2, -1, 1, 2))
            b = random.choice((-2, -1, 1, 2))
            iloraz = (liczba / (a + b * I * rozne_pierwiastki)).expand(complex=True).collect(I)
            if sp.im(iloraz) != 0 and sp.re(iloraz) != 0 and a != b and a != sp.im(iloraz):
                break
        # print(liczba)
        z = sp.symbols('z', complex=True)
        rozwiazanie = sp.latex(sp.solve(z ** 4 - liczba)).replace('[', '\{').replace(']', '\}')
        # print(sp.latex(rozwiazanie))
        strona = random.choice((0, 1))  # do wymieszania nawiasów pod pierwiastkiem
        pierwiastek = (f'\t\\[\n'
                       f'\t\t\\sqrt[\\leftroot{{2}}\\uproot{{-4}} \\displaystyle ^{{4}}]{{\\left('
                       f'{sp.latex(iloraz) if strona == 0 else sp.latex(a + b * I * rozne_pierwiastki)} \\right)'
                       f' \\left({sp.latex(a + b * I * rozne_pierwiastki) if strona == 0 else sp.latex(iloraz)} \\right)}}\n'
                       f'\t\\]')
        # pierwiastek = str('$$\\sqrt[\\leftroot{2}\\uproot{-4} \\displaystyle ^{4}]{\\left(' + sp.latex(
        #     iloraz) + '\\right) \\left(' + sp.latex(a + b * I * rozne_pierwiastki) + '\\right)}$$')
        return ('Wyznaczyć wszystkie zadane pierwiastki zespolone i zaznaczyć je na płaszczyźnie zespolonej\n'
                f'{pierwiastek}',
                f'$\\sqrt[\\leftroot{{2}}\\uproot{{-4}} \\displaystyle ^{{4}}]{{{sp.latex(liczba)}}} = {rozwiazanie}.$')
        # return str(
        #     r'        \item Wyznaczyć wszystkie zadane pierwiastki zespolone i zaznaczyć je na płaszczyźnie zespolonej.' + '\n' +
        #     '        ' + pierwiastek + '\n' +
        #     '        \\textcolor{\kolorodpowiedzi}{Rozwiązaniem jest $z = ' + sp.latex(rozwiazanie).replace('[',
        #                                                                                                      '\{').replace(
        #         ']', '\}') + '.$}\n\n'
        # )


def rownanie_ze_sprzezeniem(calkowite: bool = 1, kwadratowe: bool = 1):
    x, y = sp.symbols('x y', real=True)
    z = sp.symbols('z', complex=True)
    wspolczynniki = (-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7)
    while True:
        liczby = {}  # potencjalnie lepsze od tworzenia listy i dodawania elementów
        for i in range(4):  # losuje 3 liczb zespolonych i zapisuje w słowniku
            [u, v] = [random.choice(wspolczynniki) for _ in range(2)]
            liczby[i] = u + v * I
        r = x + I * y  # inne oznaczenie by osobno wyświetlać równanie z "z" oraz równanie z "x" i "y"
        rownanie = ((liczby[0] if kwadratowe is False else sp.re(liczby[0]))
                    + (liczby[1] if kwadratowe is False else sp.re(liczby[1])) * sp.conjugate(z)
                    + (1 - int(kwadratowe)) * liczby[2] * z + int(kwadratowe) * z ** 2)
        rownanie_latex = sp.latex(rownanie)
        # rownanie = ((liczby[0] if kwadratowe == 0 else sp.re(liczby[0]))
        #             + (liczby[1] if kwadratowe == 0 else sp.re(liczby[1])) * sp.conjugate(r)
        #             + (1 - kwadratowe) * liczby[2] * r + kwadratowe * r ** 2)
        rownanie = rownanie.subs(z, r)
        rozwiazanie = sp.solve(rownanie)
        try:
            if len(rozwiazanie) > 0 and (type(rozwiazanie) == list and all(
                    (all if calkowite else any)((int(i) == i and -10 < i < 10) for i in j.values()) for j in
                    rozwiazanie)
                                         or type(rozwiazanie) == dict and (all if calkowite else any)(
                        (int(i) == i and -10 < i < 10) for i in rozwiazanie.values())):
                break
        except Exception:
            print(Exception)
            break
    # print(print([rozwiazanie[i] for i in rozwiazanie.keys()]))
    # print(rownanie_latex)
    # print(sp.latex(rownanie))
    # print(sp.latex(sp.re(rownanie)))
    # print(sp.latex(sp.im(rownanie)))
    # print(rozwiazanie)
    return (
        f'Rozwiązać równanie w zbiorze liczb zespolonych\n'
        f'\t\\[\n'
        f'\t\t{rownanie_latex} = 0\n'
        f'\t\\]',
        f'${sp.latex(rownanie)} = 0,$ \\\\ \n'
        f'${sp.latex(rownanie.factor(x, y))} = 0,$\\\\\n'
        f'$\\left\\{{\n'
        f'\t\\begin{{array}}{{c}}\n'
        f'\t\t{sp.latex(sp.re(rownanie))} = 0\\\\\n'
        f'\t\t{sp.latex(sp.im(rownanie))} = 0\n'
        f'\t\\end{{array}}\n'
        f'\\right.$ \\\\\n'
        f'$z = {sp.latex(rozwiazanie)}.$')

    # print(sp.solve(z ** 5 - I, (x, y)))  # trudne
    # print(sp.solve(z ** 3 + sp.Abs(z) ** 2 * sp.conjugate(z), (x, y)))  # trudne
    # print(sp.solve(z + sp.conjugate(z) - sp.Abs(z), (x, y)))
    # print(sp.solve(z ** 2 + 2 * sp.conjugate(z), (x, y)))
    # print(sp.solve(2 * z + (4 - I) * sp.conjugate(z) - 15 - 4 * I, (x, y)))


def obszar_zespolony(typ: int = 1, nr_zadania: int = 1):
    # https://stackoverflow.com/questions/40747474/how-to-customize-and-add-extra-elements-to-sympy-plots
    if not os.path.exists('pics'):
        os.makedirs('pics')
        print(" ! Tworzę katalog pics ", file=sys.stderr)
    x, y = sp.symbols('x y', real=True)
    z = x + I * y
    from spb import plot_implicit
    # from sympy import plot_implicit, symbols, Eq, And, Or
    if typ == 1:  # przesunięty okrąg
        wspolczynniki = (-3, -2, -1, 1, 2, 3)
        liczby = {}  # potencjalnie lepsze od tworzenia listy i dodawania elementów
        [u, v] = [random.choice(wspolczynniki) for _ in range(2)]
        liczby[0] = u + v * I
        promien = random.choice([sp.Rational(1 / 2), 1, sp.sqrt(2), sp.Rational(3 / 2), 2, sp.Rational(5 / 2), 3])
        warunek = sp.Abs(z - liczby[0]) - promien
        warunki = ('\\left|z'
                   + ('+' if sp.re(liczby[0]) < 0 else '')
                   + (f'{sp.latex(-liczby[0])}\\right|  =  {sp.latex(promien)}'))
        p1 = plot_implicit(
            warunek,
            (x, -7, 7),
            (y, -7, 7),
            show_in_legend=False,
            show=False,
            # points=1000,
            aspect='equal',
            size=(4, 4),
            markers=[{'args': [sp.re(liczby[0]), sp.im(liczby[0])], 'color': "black", 'marker': "o", 'ms': 3}
                     # , {'args': [[sp.re(liczby[0]), sp.re(liczby[0])+promien], [sp.im(liczby[0]), sp.im(liczby[0])]],
                     #    'color': "blue", 'ls': '-', 'lw': 2}
                     ],
            # annotations=[{'xy': (sp.re(liczby[0]), sp.im(liczby[0])), 'text': "  S", 'ha': 'left', 'va': 'top', 'color': 'blue'},
            #              {'xy': (2, 2), 'text': "x=y ", 'ha': 'right', 'va': 'bottom', 'color': 'blue'}]
        )
        #
        # warunek = sp.latex(sp.Abs(z - liczby[0])) + ' = ' + f'{sp.latex(promien)}'
        warunek = sp.latex(
            (x - sp.re(liczby[0])) ** 2 + (y - sp.im(liczby[0])) ** 2) + ' = ' + f'{sp.latex(promien ** 2)}'
    if typ == 2:  # przesunięte koło - wnętrze lub zewnętrze
        wspolczynniki = (-3, -2, -1, 1, 2, 3)
        liczby = {}  # potencjalnie lepsze od tworzenia listy i dodawania elementów
        [u, v] = [random.choice(wspolczynniki) for _ in range(2)]
        liczby[0] = u + v * I
        wieksze_mniejsze = random.choice(('>', r'\geq', '<', r'\leq'))
        promien = random.choice([sp.Rational(1 / 2), 1, sp.sqrt(2), sp.Rational(3 / 2), 2, sp.Rational(5 / 2), 3])
        warunek = sp.Abs(
            z - (liczby[0])) > promien if wieksze_mniejsze == '>' or wieksze_mniejsze == r'\geq' else sp.Abs(
            z - (liczby[0])) < promien
        warunki = ('\\left|z' + (
            '+' if sp.re(liczby[0]) < 0 else '') + f'{sp.latex(-liczby[0])}\\right|  ' +
                   wieksze_mniejsze +
                   f' {sp.latex(promien)}')
        p1 = plot_implicit(
            warunek,
            (x, -7, 7),
            (y, -7, 7),
            show_in_legend=False,
            show=False,
            # points=1000,
            aspect='equal',
            size=(4, 4),
            markers=[{'args': [sp.re(liczby[0]), sp.im(liczby[0])], 'color': "black", 'marker': "o", 'ms': 3}
                     # , {'args': [[sp.re(liczby[0]), sp.re(liczby[0])+promien], [sp.im(liczby[0]), sp.im(liczby[0])]],
                     #    'color': "blue", 'ls': '-', 'lw': 2}
                     ],
            # annotations=[{'xy': (sp.re(liczby[0]), sp.im(liczby[0])), 'text': "  S", 'ha': 'left', 'va': 'top', 'color': 'blue'},
            #              {'xy': (2, 2), 'text': "x=y ", 'ha': 'right', 'va': 'bottom', 'color': 'blue'}]
        )
        # tu były cyrki spowodowane chyba brakiem wymiarów przy drugim wykresie.
        warunek = sp.Abs(z - liczby[0]) - promien
        p2 = plot_implicit(
            warunek,
            (x, -7, 7),
            (y, -7, 7),
            show_in_legend=False,
            color="red",
            show=False,
            # points=1000,
            aspect='equal',
            size=(4, 4),
            rendering_kw={"linestyles": ":" if wieksze_mniejsze == '>' or wieksze_mniejsze == '<' else "-",
                          "linewidths": 2}
        )

        p1.append(p2[0])
        # warunek = sp.latex(warunek)
        warunek = (f'{sp.latex((x - sp.re(liczby[0])) ** 2 + (y - sp.im(liczby[0])) ** 2)}' +
                   wieksze_mniejsze +
                   f'{sp.latex(promien ** 2)}')

    if typ == 3:  # pierścień
        wspolczynniki = (-3, -2, -1, 1, 2, 3)
        liczby = {}  # potencjalnie lepsze od tworzenia listy i dodawania elementów
        [u, v] = [random.choice(wspolczynniki) for _ in range(2)]
        liczby[0] = u + v * I
        while True:
            promien1 = random.choice([sp.Rational(1 / 2), 1, sp.sqrt(2), sp.Rational(3 / 2), 2, sp.Rational(5 / 2), 3])
            promien2 = random.choice([sp.Rational(1 / 2), 1, sp.sqrt(2), sp.Rational(3 / 2), 2, sp.Rational(5 / 2), 3])
            if promien1 < promien2 - 0.2:  # przy promieniach sqrt(2) i 3/2 nie widać pierścienia
                break
        nierownosc_mniejsza = random.choice(['>', r'\geq'])
        nierownosc_wieksza = random.choice(['<', r'\leq'])
        warunek1 = sp.Abs(z - liczby[0]) > promien1
        warunek2 = sp.Abs(z - liczby[0]) < promien2
        warunki = (f'{sp.latex(promien1)}' +
                   ('<' if nierownosc_mniejsza == '>' else r'\leq') +
                   f' \\left|z' + ('+' if sp.re(liczby[0]) < 0 else '') +
                   f'{sp.latex(-liczby[0])}\\right| {nierownosc_wieksza} {sp.latex(promien2)}')

        p1 = plot_implicit(sp.And(
            warunek1,
            warunek2
        ),
            (x, -7, 7),
            (y, -7, 7),
            show_in_legend=False,
            show=False,
            adaptive=False,
            depth=2,  # dokladność rysowania obszarów - od 0 do 4 - 4 bardzo czasochłonne
            # i generuje duże pliki - problem z kompilacją i potrzebny lualatex, który z kolei zgłasza dodatkowe problemy.
            aspect='equal',
            size=(4, 4),
            markers=[
                {'args': [sp.re(liczby[0]), sp.im(liczby[0])], 'color': "black", 'marker': "o", 'ms': 3}
                # , {'args': [[sp.re(liczby[0]), sp.re(liczby[0])+promien], [sp.im(liczby[0]), sp.im(liczby[0])]],
                #    'color': "blue", 'ls': '-', 'lw': 2}
            ],
            # annotations=[{'xy': (sp.re(liczby[0]), sp.im(liczby[0])), 'text': "  S", 'ha': 'left', 'va': 'top', 'color': 'blue'},
            #              {'xy': (2, 2), 'text': "x=y ", 'ha': 'right', 'va': 'bottom', 'color': 'blue'}]
        )

        p2 = plot_implicit(
            # sp.geometry.Circle(sp.geometry.Point(sp.re(liczby[0]), sp.im(liczby[0])), promien1).equation(),
            sp.Abs(z - liczby[0]) - promien1,
            (x, -7, 7),
            (y, -7, 7),
            show_in_legend=False,
            color="red",
            show=False,
            # points=1000,
            aspect='equal',
            size=(4, 4),
            rendering_kw={"linestyles": ":" if nierownosc_mniejsza == '>' else "-",
                          "linewidths": 1}
        )
        p1.append(p2[0])
        p3 = plot_implicit(
            sp.Abs(z - liczby[0]) - promien2,
            (x, -7, 7),
            (y, -7, 7),
            show_in_legend=False,
            color="red",
            show=False,
            aspect='equal',
            size=(4, 4),
            rendering_kw={"linestyles": ":" if nierownosc_wieksza == '<' else "-",
                          "linewidths": 1}
        )
        p1.append(p3[0])

        warunek1 = (f'{sp.latex((x - sp.re(liczby[0])) ** 2 + (y - sp.im(liczby[0])) ** 2)}' +
                    nierownosc_mniejsza +
                    f'{sp.latex(promien1 ** 2)}')
        warunek2 = (f'{sp.latex((x - sp.re(liczby[0])) ** 2 + (y - sp.im(liczby[0])) ** 2)}' +
                    nierownosc_wieksza +
                    f'{sp.latex(promien2 ** 2)}')
        warunek = warunek1 + '\\\\\n\t\t' + warunek2
    if typ == 4:  # przesunięte koła o różnych środkach (wnętrza lub zewnętrzna)
        wspolczynniki = (-3, -2, -1, 1, 2, 3)
        liczby = {}  # potencjalnie lepsze od tworzenia listy i dodawania elementów
        przeciecie = random.choice((True, False))
        while True:
            [u, v] = [random.choice(wspolczynniki) for _ in range(2)]
            liczby[0] = u + v * I
            [u, v] = [random.choice(wspolczynniki) for _ in range(2)]
            liczby[1] = u + v * I
            promien1 = random.choice([sp.Rational(1 / 2), 1, sp.sqrt(2), sp.Rational(3 / 2), 2, sp.Rational(5 / 2), 3])
            promien2 = random.choice([sp.Rational(1 / 2), 1, sp.sqrt(2), sp.Rational(3 / 2), 2, sp.Rational(5 / 2), 3])
            if (przeciecie is True
                    and liczby[0] != liczby[1]
                    and sp.Abs(promien1 - promien2) < sp.Abs(liczby[0] - liczby[1]) < promien1 + promien2):
                break
            if przeciecie is False:
                break
        nierownosc_pierwsza = random.choice(['>', r'\geq', '<', r'\leq'])
        nierownosc_druga = random.choice(['>', r'\geq', '<', r'\leq'])
        warunek1 = sp.Abs(z - liczby[0]) < promien1 if nierownosc_pierwsza in ('<', r'\leq') else sp.Abs(
            z - liczby[0]) > promien1
        warunek2 = sp.Abs(z - liczby[1]) < promien2 if nierownosc_druga in ('<', r'\leq') else sp.Abs(
            z - liczby[1]) > promien2
        warunki = ('\\left|z' + (
            '+' if sp.re(
                liczby[0]) < 0 else '') + f'{sp.latex(-liczby[0])}\\right| {nierownosc_pierwsza} {sp.latex(promien1)}\n'
                                          f' \t\t\\quad \\textnormal{{oraz}} \\quad\n\t\t'
                                          '\\left|z' + (
                       '+' if sp.re(liczby[
                                        1]) < 0 else '') + f'{sp.latex(-liczby[1])}\\right| {nierownosc_druga} {sp.latex(promien2)}')
        p1 = plot_implicit(sp.And(
            warunek1
        ),
            (x, -7, 7),
            (y, -7, 7),
            show_in_legend=False,
            show=False,
            adaptive=False,
            depth=2,  # dokladność rysowania obszarów - od 0 do 4 - 4 bardzo czasochłonne
            # i generuje duże pliki - problem z kompilacją i potrzebny lualatex, który z kolei zgłasza dodatkowe problemy.
            aspect='equal',
            size=(4, 4),
            markers=[
                {'args': [sp.re(liczby[0]), sp.im(liczby[0]), sp.re(liczby[1]), sp.im(liczby[1])], 'color': "black",
                 'marker': "o", 'ms': 3}
                # , {'args': [[sp.re(liczby[0]), sp.re(liczby[0])+promien], [sp.im(liczby[0]), sp.im(liczby[0])]],
                #    'color': "blue", 'ls': '-', 'lw': 2}
            ],
            rendering_kw={"alpha": 0.1}
            # annotations=[{'xy': (sp.re(liczby[0]), sp.im(liczby[0])), 'text': "  S", 'ha': 'left', 'va': 'top', 'color': 'blue'},
            #              {'xy': (2, 2), 'text': "x=y ", 'ha': 'right', 'va': 'bottom', 'color': 'blue'}]
        )
        p2 = plot_implicit(sp.And(
            warunek2
        ),
            (x, -7, 7),
            (y, -7, 7),
            show_in_legend=False,
            show=False,
            adaptive=False,
            depth=2,  # dokladność rysowania obszarów - od 0 do 4 - 4 bardzo czasochłonne
            # i generuje duże pliki - problem z kompilacją i potrzebny lualatex, który z kolei zgłasza dodatkowe problemy.
            aspect='equal',
            size=(4, 4),
            markers=[
                {'args': [sp.re(liczby[0]), sp.im(liczby[0]), sp.re(liczby[1]), sp.im(liczby[1])], 'color': "black",
                 'marker': "o", 'ms': 3}
                # , {'args': [[sp.re(liczby[0]), sp.re(liczby[0])+promien], [sp.im(liczby[0]), sp.im(liczby[0])]],
                #    'color': "blue", 'ls': '-', 'lw': 2}
            ],
            rendering_kw={"alpha": 0.1}
            # annotations=[{'xy': (sp.re(liczby[0]), sp.im(liczby[0])), 'text': "  S", 'ha': 'left', 'va': 'top', 'color': 'blue'},
            #              {'xy': (2, 2), 'text': "x=y ", 'ha': 'right', 'va': 'bottom', 'color': 'blue'}]
        )
        p1.append(p2[0])
        p3 = plot_implicit(sp.And(warunek1,
                                  warunek2
                                  ),
                           (x, -7, 7),
                           (y, -7, 7),
                           show_in_legend=False,
                           show=False,
                           adaptive=False,
                           depth=3,  # dokladność rysowania obszarów - od 0 do 4 - 4 bardzo czasochłonne
                           # i generuje duże pliki - problem z kompilacją i potrzebny lualatex, który z kolei zgłasza dodatkowe problemy.
                           aspect='equal',
                           size=(4, 4),
                           rendering_kw={"alpha": 0.9}
                           )
        p1.append(p3[0])

        p4 = plot_implicit(
            # sp.geometry.Circle(sp.geometry.Point(sp.re(liczby[0]), sp.im(liczby[0])), promien1).equation(),
            sp.Abs(z - liczby[0]) - promien1,
            (x, -7, 7),
            (y, -7, 7),
            show_in_legend=False,
            color="red",
            show=False,
            depth=2,
            aspect='equal',
            size=(4, 4),
            rendering_kw={"alpha": 0.2, "linestyles": ":" if nierownosc_pierwsza in ('<', '>') else "-",
                          "linewidths": 1}
        )
        p1.append(p4[0])
        p5 = plot_implicit(
            sp.Abs(z - liczby[1]) - promien2,
            (x, -7, 7),
            (y, -7, 7),
            show_in_legend=False,
            color="red",
            show=False,
            depth=2,
            aspect='equal',
            size=(4, 4),
            rendering_kw={"alpha": 0.2, "linestyles": ":" if nierownosc_druga in ('<', '>') else "-",
                          "linewidths": 1}
        )
        p1.append(p5[0])

        warunek1 = (f'{sp.latex((x - sp.re(liczby[0])) ** 2 + (y - sp.im(liczby[0])) ** 2)} ' +
                    nierownosc_pierwsza +
                    f' {sp.latex(promien1 ** 2)}')
        warunek2 = (f'{sp.latex((x - sp.re(liczby[1])) ** 2 + (y - sp.im(liczby[1])) ** 2)} ' +
                    nierownosc_druga +
                    f' {sp.latex(promien2 ** 2)}')
        warunek = warunek1 + '\\\\\n\t\t' + warunek2

    # strasznie mi się poniższe nie podoba (koszmar) - ale nie będzie mi się chciało tego poprawiać.
    if typ == 5:  # pierścień w środku układu plus argument.
        argument1_nierownosc = random.choice(('>', r'\geq'))
        argument2_nierownosc = random.choice(('<', r'\leq'))
        katy = ('-5 / 6', '-3 / 4', '-2 / 3', '1 / 2', '-1 / 3', '-1 / 4', '-1 / 6',
                '1', '5 / 6', '3 / 4', '2 / 3', '1 / 2', '1 / 3', '1 / 4', '1 / 6')
        while True:
            phi1 = sp.Rational(random.choice(katy)) * sp.pi
            phi2 = sp.Rational(random.choice(katy)) * sp.pi
            if phi1 < phi2:
                break
        liczby = {}  # potencjalnie lepsze od tworzenia listy i dodawania elementów
        liczby[0] = 0
        while True:
            promien1 = random.choice([1, sp.sqrt(2), sp.Rational(3 / 2), 2, sp.Rational(5 / 2), 3, 4, 5])
            promien2 = random.choice([1, sp.sqrt(2), sp.Rational(3 / 2), 2, sp.Rational(5 / 2), 3, 4, 5])
            if promien1 < promien2 - 0.2:  # przy promieniach sqrt(2) i 3/2 nie widać pierścienia
                break
        nierownosc_mniejsza = random.choice(['>', r'\geq'])
        nierownosc_wieksza = random.choice(['<', r'\leq'])
        warunek1 = sp.Abs(z - liczby[0]) > promien1
        warunek2 = sp.Abs(z - liczby[0]) < promien2

        warunki = (f'{sp.latex(promien1)}' +
                   ('<' if nierownosc_mniejsza == '>' else r'\leq') +
                   f' \\left|z \\right| {nierownosc_wieksza} {sp.latex(promien2)}\n'
                   f' \t\t\\quad \\textnormal{{oraz}} \\quad\n\t\t'
                   f'{sp.latex(phi1)} ' +
                   ('<' if argument1_nierownosc == '>' else r'\leq') +
                   f' \\arg(z) ' +
                   ('<' if argument2_nierownosc == '<' else r'\leq') +
                   f' {sp.latex(phi2)} ')

        p1 = plot_implicit((x) ** 2 + y ** 2,
                           (x, -7, 7),
                           (y, -7, 7),
                           show_in_legend=False,
                           show=False,
                           aspect='equal',
                           size=(4, 4),
                           markers=[
                               {'args': [[0, 10 * sp.cos(phi1)], [0, 10 * sp.sin(phi1)]],
                                # 'color': "blue",
                                'ls': (':' if argument1_nierownosc in ('>') else "-"),
                                'lw': 1}],
                           rendering_kw={"alpha": 0.2},
                           )
        p2 = plot_implicit((x) ** 2 + y ** 2,
                           (x, -7, 7),
                           (y, -7, 7),
                           show_in_legend=False,
                           show=False,
                           aspect='equal',
                           size=(4, 4),
                           markers=[
                               {'args': [[0, 10 * sp.cos(phi2)], [0, 10 * sp.sin(phi2)]],
                                # 'color': "blue",
                                'ls': (':' if argument2_nierownosc in ('<') else "-"),
                                'lw': 1}],
                           rendering_kw={"alpha": 0.2},
                           )
        p1.append(p2[1])  # dlaczego p2[1]?

        p3 = plot_implicit(sp.And((sp.And if phi2 - phi1 < sp.pi else sp.Or)(y * sp.cos(phi1) > sp.sin(phi1) * x,
                                                                             y * sp.cos(phi2) < sp.sin(phi2) * x),
                                  warunek1, warunek2),
                           (x, -7, 7),
                           (y, -7, 7),
                           depth=2,
                           show_in_legend=False,
                           show=False,
                           rendering_kw={"alpha": 0.9},
                           aspect='equal',
                           size=(4, 4),
                           )
        p1.append(p3[0])

        p4 = plot_implicit(
            # sp.geometry.Circle(sp.geometry.Point(sp.re(liczby[0]), sp.im(liczby[0])), promien1).equation(),
            sp.Abs(z - liczby[0]) - promien1,
            (x, -7, 7),
            (y, -7, 7),
            show_in_legend=False,
            color="red",
            show=False,
            # points=1000,
            aspect='equal',
            size=(4, 4),
            rendering_kw={"alpha": 0.2, "linestyles": ":" if nierownosc_mniejsza == '>' else "-",
                          "linewidths": 1}
        )
        p1.append(p4[0])
        p5 = plot_implicit(
            sp.Abs(z - liczby[0]) - promien2,
            (x, -7, 7),
            (y, -7, 7),
            show_in_legend=False,
            color="red",
            show=False,
            aspect='equal',
            size=(4, 4),
            rendering_kw={"alpha": 0.2, "linestyles": ":" if nierownosc_wieksza == '<' else "-",
                          "linewidths": 1}
        )
        p1.append(p5[0])

        warunek1 = (f'{sp.latex(promien1 ** 2)}' +
                    (' < ' if nierownosc_mniejsza == '>' else r'\leq ') +
                    f'{sp.latex((x - sp.re(liczby[0])) ** 2 + (y - sp.im(liczby[0])) ** 2)}' +
                    nierownosc_wieksza +
                    f'{sp.latex(promien2 ** 2)}')
        warunek3 = (f'{sp.latex(phi1)} ' +
                    ('<' if argument1_nierownosc == '>' else r'\leq') +
                    f' \\varphi ' +
                    ('<' if argument2_nierownosc == '<' else r'\leq') +
                    f' {sp.latex(phi2)} ')
        warunek = warunek1 + '\\\\\n\t\t' + warunek3

    p1.xlabel = None
    p1.ylabel = None
    p1.save(f'./pics/obszar{nr_zadania}.pdf')
    # p1.save(f'./pics/obszar{nr_zadania}.pgf')  # importujemy pdf-y bo pgf są jakieś ogromne przy obszarach zespolonych
    # print(sp.latex(warunek1), sp.latex(warunek2))
    p1.close()
    if typ < 3:  # do wyrównania warunków przy odpowiedziach
        przesuniecie = -2.8
    elif typ < 5:
        przesuniecie = -3.1
    else:
        przesuniecie = -3.3
    return ('Zaznaczyć na płaszczyźnie zespolonej obszar spełniający ' + (
        'warunek' if typ < 4 else 'warunki') + '\n' +
            f'\t\[\n'
            f'\t\t{warunki}\n'
            f'\t\]',
            f'\t\\begin{{tabular}}{{p{{0.4\\textwidth}}p{{0.3\\textwidth}}}}\n'
            f'\t\\begin{{gather*}}\n'
            f'\t\t{warunek}\n'
            f'\t\\end{{gather*}}'
            f'\t\t\n'
            f'\t&\n'
            # f'\t\t\\raisebox{{{przesuniecie}cm}}{{\\resizebox{{4cm}}{{!}}{{\\input{{../pics/obszar{nr_zadania}.pgf}}}}}}\n'
            f'\t\t\\raisebox{{{przesuniecie}cm}}{{\\resizebox{{4cm}}{{!}}{{\\includegraphics{{../pics/obszar{nr_zadania}}}}}}}\n'
            f'\t\\end{{tabular}}\n')


if __name__ == "__main__":  # to się uruchamia tylko, gdy plik jest uruchamiany jako program, a nie ładowany jako moduł
    start_time = time.time()
    # print('!!! zespolone.py były planowane jako moduł a uruchomiłeś je jako skrypt !!!')
    # polecenie, rozwiazanie = rownanie_liniowe()
    # print(polecenie,'\n', rozwiazanie)
    # polecenie, rozwiazanie = rownanie_kwadratowe()
    # polecenie, rozwiazanie = pierwiastek_zespolony(stopien=random.choice([3, 4]))
    # polecenie, rozwiazanie = rownanie_ze_sprzezeniem(calkowite=random.choice([0, 1]), kwadratowe=random.choice([0, 1]))
    for i in range(1):
        polecenie, rozwiazanie = obszar_zespolony(typ=5, nr_zadania=i)
        print(polecenie, '\n', rozwiazanie)
    print("Czas generowania --- %s seconds ---" % (time.time() - start_time))
