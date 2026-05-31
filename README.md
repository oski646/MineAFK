# MineAFK
Skrypt stworzony dla społeczności ludzi kopiących AFK na serwerach minecraft

## Pobierz to jeśli nie działa ci plik `.exe`
- Python - [link](https://www.python.org/downloads/)

## Instalacja manualna
1. Pobierz sobie repozytorium - [link](https://github.com/oski646/MineAFK/archive/master.zip)
2. Przejdź do folderu z repozytorium
3. Zainstaluj uv - [link](https://docs.astral.sh/uv/getting-started/installation/)
4. Zainstaluj wszystkie zależności
```
uv sync
```
4. Włączenie:
- aplikacji: ```uv run python main.py```

## Budowanie plików `.exe` na Windows
1. Zainstaluj zależności
```
uv sync --group build
```
2. Zbuduj aplikację
```
powershell -ExecutionPolicy Bypass -File .\app\build.ps1
```
3. Gotowy plik `MineAFK.exe` znajdziesz w folderze `dist`.

Jeśli masz włączone lokalne skrypty PowerShell, możesz też uruchomić krócej:
```
.\app\build.ps1
```

## Instalacja automatyczna
1. Pobierz najnowszą wersję paczki - [link](https://github.com/oski646/MineAFK/releases)
2. Wypakuj paczkę
3. Konfigurację możesz edytować w aplikacji przyciskiem `Edytuj konfigurację`
4. Włączenie:
- aplikacji: kliknij dwa razy na ```MineAFK.exe```

## Objaśnienie configu
Aplikacja zapisuje konfigurację w lokalnym katalogu użytkownika. Na Windows jest to `%LOCALAPPDATA%\MineAFK\config.ini`. Jeśli plik jeszcze nie istnieje, aplikacja utworzy tam nową domyślną konfigurację.

```
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
enable_eating = true <-- czy program ma jeść
enable_dropping_items = true <-- czy program ma wyrzucać itemy
enable_activity_commands = true <-- czy program ma wykonywać komendy aktywności
enable_cobblex = true <-- czy program ma tworzyć cobblex

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
W celu poprawnego skonfigurowania slotów odpalamy `MineAFK.exe` i klikamy `Start czytnika`. Aplikacja prosi o zeskanowanie slotu 1, slotu 2 i miejsca wyrzucania itemów klawiszem **F8**. **(skanujemy sam środek slota)**

![Zdjęcie](https://i.imgur.com/nyRreuU.png)

1. Pierwszy krok
2. Drugi krok
3. Nie ma na zdjęciu ale chodzi o zeskanowanie miejsca poza ekwipunkiem.

## Lista keybindów
- **F8** - Wystartowanie kopania
- **F9** - Zatrzymanie kopania
- **F10** - Zwolnienie przytrzymanych klawiszy i myszy

## FAQ
### Program został wykryty jako wirus. Co zrobić w takiej sytuacji?
Program, który dostarczany jest jako plik `.exe` jest tworzony przy użyciu `pyinstaller`. Dzięki temu jestem w stanie dostarczyć pojedynczy plik, który odpala skrypt. Natomiast czasami zdarza się, że ten plik jest traktowany jako wirus (na co niestety nie mam wpływu) i zostaje on natychmiastowo usunięty z komputera. W takiej sytuacji polecam dodać program do wyjątków antywirusa lub manualne uruchomić program. Więcej można przeczytać [tutaj](https://medium.com/@markhank/how-to-stop-your-python-programs-being-seen-as-malware-bfd7eb407a7).

## Problemy, pytania, nowości
Wszystkie takie sprawy proszę zgłaszać w tej [sekcji](https://github.com/oski646/MineAFK/issues)
