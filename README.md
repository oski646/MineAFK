# MineAFK
Skrypt stworzony dla społeczności ludzi kopiących AFK na serwerach minecraft

## Pobierz to jeśli nie działa ci plik `.exe`
- Python 
  - (wersja 64 bit) - [POBIERZ](https://www.python.org/ftp/python/3.8.1/python-3.8.1-amd64.exe)
  - (wersja 32 bit) - [POBIERZ](https://www.python.org/ftp/python/3.8.1/python-3.8.1.exe)

## Instalacja manualna
1. Pobierz sobie repozytorium - [link](https://github.com/oski646/MineAFK.git)
2. Przejdź do folderu z repozytorium
3. Pobierz wszystkie potrzebne moduły
```
pip install -r requirements.txt
```
4. Włączenie:
- skryptu: ```python main.py```
- slot readera: ```python mouse-position.py```

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
version = 0.4 BETA

[Config]
stones = 13 <-- ile jest stoniarek w szerokości
pickaxe = 8 <-- slot kilofa
eatRounds = 3 <-- co ile rund ma jeść
food = 0 <-- slot mięska (ustaw 0 jeśli nie chcesz jeść)
dropRounds = 4 <-- co ile rund ma wyrzucać itemy
dropSlots = 6,7 <-- sloty do wyrzucenia
activityRounds = 1 <-- co ile rund ma się wykonać "aktywność"
activityCommands = naprawkilof <-- komendy do wykonania "aktywności"
cobblexRounds = 2 <-- co ile rund ma się tworzyć cobblex
cobblexCommands = cx,cx <-- komendy do wytworzenia cobblex

# (!) TA CAŁA SEKCJA WAS NIE INTERESUJE (!) #
# Jeśli chcecie coś tutaj zmieniać macie od tego "Slot reader" #
[Slots]
firstRowX = 819
firstRowY = 580
secondRowX = 819
secondRowY = 617
thirdRowX = 819
thirdRowY = 653
fourthRowX = 819
fourthRowY = 698
dropX = 1346
dropY = 565
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
W celu poprawnego skonfigurowania slotów odpalamy `Slot reader.exe`. Skrypt odpala nam się i prosi o zeskanowanie sześciu pozycji.

![Zdjęcie](https://i.imgur.com/wGwoENB.png)

1. Pierwszy krok
2. Drugi krok
3. Trzeci krok
4. Czwarty krok
5. Piąty krok
6. Nie ma na zdjęciu ale chodzi o zeskanowanie miejsca poza ekwipunkiem.

## Lista keybindów
- **F8** - Wystartowanie kopania
- **F9** - Zatrzymanie kopania
- **F10** - Wyjście ze skryptu

## Problemy, pytania, nowości
Wszystkie takie sprawy proszę zgłaszać w tej [sekcji](https://github.com/oski646/MineAFK/issues)
