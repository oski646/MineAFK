from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
from pynput import keyboard as KeyboardManager
import time

# Mouse controller
mouse = MouseController()

# Welcome message
print("")
print("##################  MineAFK - Slot Reader  ##################")
print("")
print("Autor: oski646")
print("WWW: https://github.com/oski646")
print("Jeśli chcesz tu coś zmieniać proszę bardzo, lecz pamiętaj o twórcy tego skryptu.")
print("")
print("##################  MineAFK - Slot Reader  ##################")
print("")

def test():
    global firstRow, secondRow, thirdRow, fourthRow, difference
    mouse.position = firstRow
    firstStart = 1
    for i in range(1, 10):
        time.sleep(0.3)
        mouse.position = (firstRow[0] + (firstStart * difference), firstRow[1])
        firstStart += 1

    # Second row
    mouse.position = secondRow
    secondStart = 1
    for i in range(10, 19):
        time.sleep(0.3)
        mouse.position = (secondRow[0] + (secondStart * difference), secondRow[1])
        secondStart += 1

    # Third row
    mouse.position = thirdRow
    thirdStart = 1
    for i in range(19, 28):
        time.sleep(0.3)
        mouse.position = (thirdRow[0] + (thirdStart * difference), thirdRow[1])
        thirdStart += 1

    # Fourth row
    mouse.position = fourthRow
    fourthStart = 1
    for i in range(28, 37):
        time.sleep(0.3)
        mouse.position = (fourthRow[0] + (fourthStart * difference), fourthRow[1])
        fourthStart += 1

prefix = "MineAFK - "
firstRow = (0, 0)
secondRow = (0, 0)
thirdRow = (0, 0)
fourthRow = (0, 0)
drop = (0, 0)
difference = 0

# Steps
firstStep = True
secondStep = False
thirdStep = False
fourthStep = False
fifthStep = False
finish = False

def logger(message):
    print(prefix + message)

logger("Zeskanuj proszę pierwszy rząd twojego ekwipunku. \nKliknij F8 jeśli twój kursor będzie na odpowiednim slocie!\n")

# Function to listen pressed keys
def on_press(key):
    pass

# Function to listen released keys
def on_release(key):
    global firstRow, secondRow, thirdRow, fourthRow, difference
    global firstStep, secondStep, thirdStep, fourthStep, fifthStep, finish

    if key == KeyboardManager.Key.f8:
        if firstStep == True:
            firstRow = mouse.position
            logger("Zeskanuj proszę drugi przedmiot w pierwszym rzędzie twojego ekwipunku. \nKliknij F8 jeśli twój kursor będzie na odpowiednim slocie!\n")
            firstStep = False
            secondStep = True
            return
        if secondStep == True:
            before = firstRow[0]
            after = mouse.position[0]
            difference = after - before
            logger("Zeskanuj proszę drugi rząd twojego ekwipunku. \nKliknij F8 jeśli twój kursor będzie na odpowiednim slocie!\n")
            secondStep = False
            thirdStep = True
            return
        if thirdStep == True:
            secondRow = mouse.position
            logger("Zeskanuj proszę trzeci rząd twojego ekwipunku. \nKliknij F8 jeśli twój kursor będzie na odpowiednim slocie!\n")
            thirdStep = False
            fourthStep = True
            return
        if fourthStep == True:
            thirdRow = mouse.position
            logger("Zeskanuj proszę czwarty rząd twojego ekwipunku. \nKliknij F8 jeśli twój kursor będzie na odpowiednim slocie!\n")
            fourthStep = False
            fifthStep = True
            return
        if fifthStep == True:
            fourthRow = mouse.position
            logger("Zeskanuj miejsce poza ekwipunkiem aby można było wyrzucać przedmioty. \nKliknij F8 jeśli twój kursor będzie w odpowiednim miejscu!\n")
            fifthStep = False
            finish = True
            return
        if finish == True:
            drop = mouse.position
            logger("Wykonywanie testowania... Nie ruszaj myszką!\n")
            time.sleep(2)

            test()

            time.sleep(2)

            print("\n\nJeśli ten test przebiegł pomyślnie i każdy slot został odczytany to skopiuj poniższy kod i wklej go na sam dół do configu.")
            print("Jeśli coś poszło nie tak to wykonaj test jeszcze raz ale dokładniej.")
            print("")
            print("[Slots]")
            print("firstRowX = " + str(firstRow[0]))
            print("firstRowY = " + str(firstRow[1]))
            print("secondRowX = " + str(secondRow[0]))
            print("secondRowY = " + str(secondRow[1]))
            print("thirdRowX = " + str(thirdRow[0]))
            print("thirdRowY = " + str(thirdRow[1]))
            print("fourthRowX = " + str(fourthRow[0]))
            print("fourthRowY = " + str(fourthRow[1]))
            print("dropX = " + str(drop[0]))
            print("dropY = " + str(drop[1]))
            print("difference = " + str(difference))
            print("")
            input("Kliknij ENTER aby zakończyć program.")
            return False

# Keyboard listener
with KeyboardManager.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# Keyboard listener
listener = KeyboardManager.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()
