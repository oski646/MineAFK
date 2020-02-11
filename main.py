from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
from pynput import keyboard as KeyboardManager
import pygetwindow as gw
import time
import threading
import configparser
config = configparser.ConfigParser()
config.read("config.ini")

# Global variables
stones = int(config["Config"]["stones"])
pickaxe = int(config["Config"]["pickaxe"])
food = int(config["Config"]["food"])
dropSlots = config["Config"]["dropSlots"].split(",")
rounds = int(config["Config"]["rounds"])
commands = config["Config"]["commands"].split(",")

# Welcome message
print("")
print("##################  MineAFK  ##################")
print("")
print("Autor: oski646")
print("WWW: https://github.com/oski646")
print("Jeśli chcesz tu coś zmieniać proszę bardzo, lecz pamiętaj o twórcy tego skryptu.")
print("")
print("##################  MineAFK  ##################")
print("")

print("## Konfiguracja ##")
print("Ilość stoniarek - " + str(stones))
print("Slot kilofa - " + str(pickaxe))
print("Slot mięska - " + str(food))
print("Sloty do wyrzucenia - " + str(dropSlots))
print("Ilość tur do powtórzenia aktywności - " + str(rounds))
print("Komendy do wykonania - " + str(commands))

print("")
print("")

# STOP - DON'T TOUCH
prefix = "MineAFK - "
mining = False
miningThread = None
miningThreadStop = False
activityThread = None
activityThreadStop = False
rounds -= 1
roundCount = 0
dropSlots = [ int(x) for x in dropSlots ]

def logger(message):
    print(prefix + message)

logger("Włączanie skryptu...")

# Mouse controller
mouse = MouseController()
# Keyboard controller
keyboard = KeyboardController()

# Check if minecraft is already launched
try:
    minecraft = gw.getWindowsWithTitle("Minecraft\u200b 1.8.8 (Blazing\u200bPack.pl)")[0]
except IndexError:
    logger("Wymagana wersja: Minecraft 1.8.8 (BlazingPack.pl)")
    logger("Niestety nie masz włączonego minecrafta - nie wspieramy innych wersji!")
    time.sleep(5)
    exit()

# Check minecraft resolution
width = minecraft.width
height = minecraft.height
if(width != 1296 and height != 759):
    logger("Minecraft jest zminimalizowany lub okno nie jest w rozmiarach 1280x720")
    time.sleep(5)
    exit()

# Release all necessary keys
def releaseAll():
    mouse.release(Button.left)
    keyboard.release("a")
    keyboard.release("d")

# Function for player moving
def startMoving():
    global miningThreadStop
    global roundCount
    while True:
        if miningThreadStop == True:
            break

        # Left click
        mouse.press(Button.left)
        delay = (stones / 4) - 0.2
        keyboard.press("d")
        time.sleep(delay)
        keyboard.release("d")
        keyboard.press("a")
        time.sleep(delay)
        keyboard.release("a")
        roundCount += 1
        startMoving()

def dropSlot(backX, backY):
    time.sleep(0.05)
    dropPosition = (1346, 565)
    time.sleep(0.05)
    mouse.click(Button.left)
    time.sleep(0.05)
    mouse.click(Button.right)
    time.sleep(0.05)
    mouse.position = dropPosition
    time.sleep(0.05)
    mouse.click(Button.left)
    time.sleep(0.05)
    mouse.position = (backX, backY)
    time.sleep(0.05)


def drop():
    global dropSlots
    time.sleep(0.25)

    keyboard.press("e")
    keyboard.release("e")

    time.sleep(0.25)

    # First row
    firstRow = (819, 580)
    mouse.position = firstRow
    firstStart = 1
    for i in range(1, 10):
        if i in dropSlots:
            dropSlot(819 + (firstStart * 36), 580)
        time.sleep(0.1)
        mouse.position = (819 + (firstStart * 36), 580)
        firstStart += 1

    # Second row
    secondRow = (819, 617)
    mouse.position = secondRow
    secondStart = 1
    for i in range(10, 19):
        if i in dropSlots:
            dropSlot(819 + (secondStart * 36), 617)
        time.sleep(0.1)
        mouse.position = (819 + (secondStart * 36), 617)
        secondStart += 1

    # Third row
    thirdRow = (819, 653)
    mouse.position = thirdRow
    thirdStart = 1
    for i in range(19, 28):
        if i in dropSlots:
            dropSlot(819 + (thirdStart * 36), 653)
        time.sleep(0.1)
        mouse.position = (819 + (thirdStart * 36), 653)
        thirdStart += 1

    # Fourth row
    fourthRow = (819, 698)
    mouse.position = fourthRow
    fourthStart = 1
    for i in range(28, 37):
        if i in dropSlots:
            dropSlot(819 + (fourthStart * 36), 698)
        time.sleep(0.1)
        mouse.position = (819 + (fourthStart * 36), 698)
        fourthStart += 1

    time.sleep(0.25)

    keyboard.press("e")
    keyboard.release("e")

    time.sleep(0.25)

def eat():
    global food
    global pickaxe
    time.sleep(0.1)
    keyboard.press(str(food))
    keyboard.release(str(food))
    time.sleep(0.1)
    mouse.press(Button.right)
    time.sleep(3)
    mouse.release(Button.right)
    time.sleep(0.1)
    keyboard.press(str(pickaxe))
    keyboard.release(str(pickaxe))

# Function for sending command to server
def sendCommand(command):
    keyboard.press("t")
    keyboard.release("t")
    time.sleep(0.2)
    keyboard.press("/")
    keyboard.release("/")
    time.sleep(0.2)
    keyboard.type(command)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

# Activity
def activity():
    global miningThread
    global miningThreadStop
    global interval
    global food
    global roundCount
    global activityThreadStop
    global rounds

    while True:
        if activityThreadStop == True:
            break
        if roundCount == rounds:
            if miningThread != None:
                miningThreadStop = True
                miningThread.join()
                miningThread = None

                # Send commands
                for command in commands:
                    sendCommand(command)

                # Drop
                drop()

                # Eat
                if food >= 1 and food <= 9:
                    eat()

                # Left click
                mouse.release(Button.left)
                time.sleep(2)

                # Start moving thread
                miningThreadStop = False
                miningThread = threading.Thread(target = startMoving)
                miningThread.start()
                roundCount = 0

# Function to listen pressed keys
def on_press(key):
    if key == KeyboardManager.Key.f8:
        global mining
        if mining == False:
            logger("Zaczęto kopanie na AFK'u!")

# Function to listen released keys
def on_release(key):
    if key == KeyboardManager.Key.f8:
        global mining
        global miningThread
        global miningThreadStop
        global activityThread
        global activityThreadStop
        global roundCount
        if mining == False:
            # Start moving thread
            miningThread = threading.Thread(target = startMoving)
            miningThread.start()

            roundCount = 0

            # Start command thread
            activityThread = threading.Thread(target = activity)
            activityThread.start()
            
            mining = True
    if key == KeyboardManager.Key.f9:
        logger("Zatrzymywanie kopania...")
        logger("Zaczekaj na zakończenie wątków!")

        # Stop mining
        mining = False
        roundCount = 0
        activityThreadStop = True
        activityThread.join()
        activityThread = None
        miningThreadStop = True
        miningThread.join()
        miningThread = None

        logger("Kopanie zostało zatrzymane!")

        # Release all necessary keys
        releaseAll()

        activityThreadStop = False
        miningThreadStop = False
    if key == KeyboardManager.Key.f10:
        # Release all necessary keys
        releaseAll()
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