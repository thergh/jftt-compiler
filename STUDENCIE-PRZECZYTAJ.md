Hej, ten kompilator został napisany na kurs Języki Formalne i Techniki Translacji 2024-2025. Program został napisany z myślą o poprawności, ze znikomą optymalizacją.

Krótki opis plików:
- lexer.py - Analizator leksykalny. Dzieli lity tekst na tokeny.
- parser.py - Analizator gramatyki. Układa tokeny zgodnie z gramatyką i generuje AST.
- table.py - Tablica symboli. Wskazuje na miejsce w pamięci, gdzie zapisana jest wartość zmiennej lub wskaźnik na zmienną albo procedurę. 
- generator.py - Generator kodu wyjściowego. Najważniejsza część kompilacji.
- kompilator.py - Łączy kod w program do wykonania.

Mój kompilator jest oparty na AST - Abstract Syntax Tree. Jest to struktura danych tworzona przez parser podczas analizy gramatyki. Ja wybrałem reprezentację za pomocą krotek (tuples). Są one w formacie {identyfikator, atrybut1, atrybut2...}. Każda reguła gramatyki zwraca krotkę z unikatowym identyfikatorem i atrybutami tej reguły. Np reguła ('PID "[" NUM "]"') zwróci krotkę ('id_ARRAY_NUM', p.PID, p.NUM, p.lineno). 'id_ARRAY_NUM' to identyfikator, p.PID to nazwa tablicy, p.NUM to indeks tablicy, p.lineno to linia w której znajduje się ta tablica. Potem, w fasie generowania kodu, będę przechodził po tym drzewie i na podstawie identyfikatora napotkanej krotki wykorzystam jej atrybuty do generowania kodu wyjściowego.
Nie jest to jedyne możliwe podejście, lecz chyba najwygodniejsze na potrzeby tego zadania. Możnaby też generować kod od razu w parserze. Nie polecam tej drogi, nie jest wcale prostsza do zaimplementowania a bardzo łatwo zaplątać się w spaghetti code. Można też zastosować więcej faz kompilacji, np kod trójadresowy itp., jednak nie zagłębiałem się w ten temat więc zostawiam go dla ambitniejszych studentów.

Polecam zacząć generowanie kodu od najprostszych możliwych komend. Coś w stylu READ, WRITE. Gdy to się uda, łatwo będzie zrozumiec jak przejść do bardziej skomplikowanych struktur.

Co bym zmienił następnym razem?
- Lepsza obsługa tablic i ich indeksów.
- Schldniejsza struktura danych dla tablicy symboli. Po pewnym czasie stworzył się zbyt wielki chaos w atrybutach zmiennych w słowniku tablicy symboli.
- Lepsza obsługa unarnego minusa w parserze
- Większa uważność przy korzystaniu z drogich komend, jak SET, LOAD itp.
- Mnożenie i dzielenie jako procedury. To pozwoliłoby nie wklejać ich gargantuicznego kodu za każdym razem gdy wykonywana jest operacja.
- Prawdopodobnie zamiast krotek stringów lepiej byłoby stosować klasy jako node-y w AST


Powodzenia!


Pseudokod mnożenia:
```
if multiplicand < multiplier:
    temp = multiplicand
    multiplicand = multiplier
    multiplier = temp

result = 0
while multiplier > 0:
    if multiplier % 2 == 1:
        result = result + multiplicand
    multiplicand = multiplicand * 2
    multiplier = multiplier / 2
return result
```


Pseudokod dzielenia:
```
quotient = 0
remainder = dividend

while divisor <= remainder:
    temp_divisor = divisor
    multiple = 1
    
    # find the largest double of divisor <= remainder
    while temp_divisor * 2 <= remainder:
        temp_divisor = temp_divisor * 2
        multiple = multiple * 2

    # subtract the scaled divisor and update quotient
    remainder = remainder - temp_divisor
    quotient = quotient + multiple

return quotient  # Quotient
```

