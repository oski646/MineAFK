# MineAFK
Skrypt stworzony dla społeczności ludzi kopiących AFK na serwerach minecraft

## Pobierz to jeśli nie działa ci plik `.exe`
- Python - [link](https://www.python.org/downloads/)

## Instalacja manualna
1. Pobierz sobie repozytorium - [link](https://github.com/oski646/MineAFK/archive/master.zip)
2. Przejdź do folderu z repozytorium
3. Zainstaluj poetry - [link](https://python-poetry.org/docs/#installation)
4. Zainstaluj wszystkie zależności
```
poetry install
```
4. Włączenie:
- skryptu: ```poetry run python main.py```
- slot readera: ```poetry run python mouse-position.py```

## Instalacja automatyczna
1. Pobierz najnowszą wersję paczki - [link](https://github.com/oski646/MineAFK/releases)
2. Wypakuj paczkę
3. W pliku `config` masz całą potrzebną konfigurację
4. Włączenie:
- skryptu: kliknij dwa razy na ```Skrypt.exe```
- slot readera: kliknij dwa razy na ```Slot reader.exe```

## Objaśnienie configu
```
# (!) PROSZĘ TEGO NIE RUSZAĆ (!) #
[Version]
version = 0.5 BETA

[Config]
horizontal_stones = 7 <-- ile jest stoniarek w szerokości
vertical_stones = 2 <-- ile jest stoniarek przód/tył
pickaxe = 8 <-- slot kilofa
eat_rounds = 3 <-- co ile rund ma jeść
food = 0 <-- slot mięska (ustaw 0 jeśli nie chcesz jeść)
drop_rounds = 4 <-- co ile rund ma wyrzucać itemy
drop_slots = 6,7 <-- sloty do wyrzucenia
activity_rounds = 1 <-- co ile rund ma się wykonać "aktywność"
activity_commands = naprawkilof <-- komendy do wykonania "aktywności"
cobblex_rounds = 2 <-- co ile rund ma się tworzyć cobblex
cobblex_commands = cx,cx <-- komendy do wytworzenia cobblex
commands_delay_in_seconds = 0.5 <-- odstęp w sekundach między wykonywaniem dwóch komend
fast_pickaxe = true <-- czy kopanie jest na kilofie 6/3/3

# (!) TA CAŁA SEKCJA WAS NIE INTERESUJE (!) #
# Jeśli chcecie coś tutaj zmieniać macie od tego "Slot reader" #
[Slots]
first_row_x = 815
first_row_y = 545
drop_x = 371
drop_y = 291
# Optymalna wartość tej zmiennej to 36, jeśli screen reader ci źle czyta sloty spróbuj zmienić tylko tą zmienną po otrzymaniu configu #
difference = 36 
```

## Ułożenie slotów w ekwipunku
        Pierwszy rząd     (EQ)         [1]  [2]  [3]  [4]  [5]  [6]  [7]  [8]  [9]
        Drugi rząd        (EQ)         [10] [11] [12] [13] [14] [15] [16] [17] [18]
        Trzeci rząd       (EQ)         [19] [20] [21] [22] [23] [24] [25] [26] [27]
        Czwarty rząd      (PODSTWA)    [28] [29] [30] [31] [32] [33] [34] [35] [36]
        
 *Zawsze na slocie, który ma być wyrzucony zostanie wyrzucone **stack - 1** czyli jeśli mamy na slocie 64 złota to wyrzucimy tylko 63 aby zostawić 1 na tym slocie*
 
## Slot reader
W celu poprawnego skonfigurowania slotów odpalamy `Slot reader.exe`. Skrypt odpala nam się i prosi o zeskanowanie sześciu pozycji. **(skanujemy sam środek slota)**

![Zdjęcie](https://i.imgur.com/nyRreuU.png)

1. Pierwszy krok
2. Drugi krok
3. Nie ma na zdjęciu ale chodzi o zeskanowanie miejsca poza ekwipunkiem.

## Lista keybindów
- **F8** - Wystartowanie kopania
- **F9** - Zatrzymanie kopania
- **F10** - Wyjście ze skryptu

## FAQ
### Program został wykryty jako wirus. Co zrobić w takiej sytuacji?
Program, który dostarczany jest jako plik `.exe` jest tworzony przy użyciu `pyinstaller`. Dzięki temu jestem w stanie dostarczyć pojedynczy plik, który odpala skrypt. Natomiast czasami zdarza się, że ten plik jest traktowany jako wirus (na co niestety nie mam wpływu) i zostaje on natychmiastowo usunięty z komputera. W takiej sytuacji polecam dodać program do wyjątków antywirusa lub manualne uruchomić program. Więcej można przeczytać [tutaj](https://medium.com/@markhank/how-to-stop-your-python-programs-being-seen-as-malware-bfd7eb407a7).

## Problemy, pytania, nowości
Wszystkie takie sprawy proszę zgłaszać w tej [sekcji](https://github.com/oski646/MineAFK/issues)
