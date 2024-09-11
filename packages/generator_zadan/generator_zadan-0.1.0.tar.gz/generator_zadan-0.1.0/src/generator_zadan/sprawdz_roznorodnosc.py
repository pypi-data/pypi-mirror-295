# noinspection PyUnresolvedReferences
import generatory

from datetime import timedelta
import time
import os
from pathlib import Path  # do obsługi plików
import pickle
import random
import sys  # do wysyłania komunikatów w czerwonym kolorze
from tqdm import tqdm, trange

""" 
Zapisuj w formie: 
generuj = 'generatory.calka_nieoznaczona(typ=3)'
zapisz_gotowca = True
zapisz_gotowca_jako = 'calka_nieoznaczona_typ_3.pickle'
bo pod taką nazwą jest wczytywane w modułach. Jak będzie inna nazwa to moduł nie znajdzie pliku.
"""

generuj = 'generatory.plaszczyzna_styczna()'
zapisz_gotowca = False
zapisz_gotowca_jako = 'plaszczyzna_styczna.pickle'

print('Testujemy: ', generuj)
if zapisz_gotowca:
    print('Zapisujemy do pliku: ', zapisz_gotowca_jako)
# Testuje powtarzalność generatora
start_time = time.time()
liczba_losowan = 1000

zestaw = set()

tqdmbar = tqdm(range(1, liczba_losowan+1), smoothing=0)
for i in tqdmbar:
    zadanie = eval(generuj)
    if zadanie not in zestaw:
        zestaw.add(zadanie)
        tqdmbar.set_description(f'Różnych: {len(zestaw)}')

print('\nRóżnych zadań wyszło: ', len(zestaw))
print('procent powtórzeń', (liczba_losowan - len(zestaw)) / liczba_losowan * 100)
print("--- Średni czas losowania --- : ", (time.time() - start_time)/liczba_losowan)

if zapisz_gotowca:
    print("Zapisuję dane do pliku")
    if not os.path.exists('generatory/gotowe'):
        os.makedirs('generatory/gotowe')
        print(" ! Tworzę katalog generatory/gotowe ", file=sys.stderr)
    plik = Path(
        'generatory//gotowe//' + zapisz_gotowca_jako)
    zestaw = list(zestaw)
    # plik = 'test.pkl'
    with open(plik, "wb") as file:
        pickle.dump(zestaw, file)
