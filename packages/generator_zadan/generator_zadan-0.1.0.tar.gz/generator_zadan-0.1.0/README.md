# generator_zadan

Na użytek własny. 

Generuje losowo różnego typu zadania (z rozwiązaniami) dla pierwszego roku studiów na uczelni technicznej.
Zadania mają mieć ***przyjazne*** dane i wyniki.
Powoli pewnie będzie typów zadań przybywać. 
W pliku modułach generatorów jest więcej niż w plikach dokumentacji.
Prace trwają. 

Przy każdym generowaniu są inne zadania.

Generator był przygotowany do pliku TeX-owego i funkcje generujące nie są przystosowane do formatu Markdown.
Dlatego pliki ipynb w dokumentacji mają taką dziwną strukturę w sekcji prezentującej przykładowe zadania.
Na razie nie zamierzam tego zmieniać.  

Głównym celem jest format pdf tworzony z plików TeX.
Do tego są pliki: *generuj_analiza.py* i *generuj_algebra.py*.
Tam jest więcej zadań.

Funkcje na chwilę obecną nie są w żaden sposób udokumentowane. 
To było tworzone na użytek własny.
Jak ktoś chce korzystać to proszę bardzo.
Licencja poniżej. 

## Installation

```bash
$ pip install generator_zadan  - Jeszcze nie działa - Cierpliwośći :)
```

## Usage

-  Dokumentacja na stronie [readthedocs.](https://generator_zadan.readthedocs.io/en/latest/index.html)

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`generator_zadan` was created by Adam Bohonos. It is licensed under the terms of the MIT license.

## Credits

`generator_zadan` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
