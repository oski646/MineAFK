# MineAFK
Skrypt stworzony dla społeczności ludzi kopiących AFK na serwerach minecraft

## Wymagania
- Python 
  - (wersja 64 bit) - [POBIERZ](https://www.python.org/ftp/python/3.8.1/python-3.8.1-amd64.exe)
  - (wersja 32 bit) - [POBIERZ](https://www.python.org/ftp/python/3.8.1/python-3.8.1.exe)
- Minecraft
  - rozdzielczość: 1280x720
  - umiejscowiony na środku ekranu (tak jak domyślnie otwiera się minecraft bez zmieniania pozycji)

## Instalacja manualna
1. Pobierz sobie repozytorium - [link](https://github.com/oski646/MineAFK.git)
2. Przejdź do folderu z repozytorium
3. Pobierz wszystkie potrzebne moduły
```
pip install -r requirements.txt
```
4. Wszystko gotowe! Teraz wystarczy odpalić sobie skrypt komendą
```
python main.py
```

## Instalacja automatyczna
1. Pobierz paczkę - [link](https://drive.google.com/drive/folders/19JwqDHnmwm5ND0hm19M4UIqAGOinjUC-?usp=sharing)
2. Wypakuj paczkę
3. W pliku `config` masz całą potrzebną konfigurację
4. Odpalamy skrypt klikając dwa razy w plik `.exe`

## Objaśnienie configu
```
[Config]
stones = 13 <-- Ilość stoniarek (liczone w szerokości)
pickaxe = 8 <-- Slot kilofa (liczba podana jako numer który klikasz na klawiaturze) - potrzebne tylko jeśli jedzenie jest włączone
food = 0 <-- Slot jedzenia (liczba podana jako numer który klikasz na klawiaturze) - ustaw 0 jeśli nie chcesz jeść jedzenia
dropSlots = 6,7 <-- Sloty, które mają zostać wyrzucone
rounds = 2 <-- Co ile tur ma wyrzucić itemy i wykonać komendy (jedna tura to przejście w lewo i prawo - powrót do miejsca startu)
commands = cx,cx,naprawkilof <-- Komendy, które mają zostać wykonane
```

## Ułożenie slotów w ekwipunku
        [1]  [2]  [3]  [4]  [5]  [6]  [7]  [8]  [9]
        [10] [11] [12] [13] [14] [15] [16] [17] [18]
        [19] [20] [21] [22] [23] [24] [25] [26] [27]
        [28] [29] [30] [31] [32] [33] [34] [35] [36]

## Lista keybindów
- **F8** - Wystartowanie kopania
- **F9** - Zatrzymanie kopania
- **F10** - Wyjście ze skryptu

## Problemy, pytania, nowości
Wszystkie takie sprawy proszę zgłaszać w tej [sekcji](https://github.com/oski646/MineAFK/issues)
