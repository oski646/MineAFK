from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
from pynput import keyboard as KeyboardManager
import pygetwindow as gw
import time
import threading
import configparser
import requests
import json
config = configparser.ConfigParser()
config.read("config.ini")

# Global variables
version = config["Version"]["version"]
stones = int(config["Config"]["stones"])
pickaxe = int(config["Config"]["pickaxe"])
food = int(config["Config"]["food"])
dropSlots = config["Config"]["dropSlots"].split(",")
activityRoundsConfig = int(config["Config"]["activityRounds"])
activityCommands = config["Config"]["activityCommands"].split(",")
cobblexRoundsConfig = int(config["Config"]["cobblexRounds"])
cobblexCommands = config["Config"]["cobblexCommands"].split(",")
dropRoundsConfig = int(config["Config"]["dropRounds"])
eatRoundsConfig = int(config["Config"]["eatRounds"])
commandsDelayInSeconds = float(config["Config"]["commandsDelayInSeconds"])

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
print("Slot mięska - " + str(food) + " (jedzone co " + str(eatRoundsConfig) + " rund)")
print("Sloty do wyrzucenia - " + str(dropSlots) + " (wyrzucane co " + str(dropRoundsConfig) + " rund)")
print("Komendy aktywności - " + str(activityCommands) + " (wykonywane co " + str(activityRoundsConfig) + " rund)")
print("Cobblex - " + str(cobblexCommands) + " (tworzone co " + str(cobblexRoundsConfig) + " rund)")
print("Odstęp pomiędzy wysyłaniem komend - " + str(commandsDelayInSeconds) + " sek.")

print("")
print("")

# STOP - DON'T TOUCH
prefix = "MineAFK - "
mining = False
miningThread = None
miningThreadStop = False
activityThread = None
activityThreadStop = False
dropSlots = [ int(x) for x in dropSlots ]
# Round counters
activityRounds = 0
cobblexRounds = 0
dropRounds = 0
eatRounds = 0

def logger(message):
    print(prefix + message)

logger("Włączanie skryptu...")

logger("Sprawdzanie aktualizacji...")
response = requests.get("https://raw.githubusercontent.com/oski646/MineAFK/master/version.txt")
responseVersion = response.text
if responseVersion != version:
    logger("Twoja wersja jest nieaktualna, pobierz aktualną z: https://github.com/oski646/MineAFK")
    changesResponse = requests.get("https://api.github.com/repos/oski646/MineAFK/commits/master")
    changesResponse = requests.get("https://api.github.com/repos/oski646/MineAFK/commits/master")
    changesJson = json.loads(changesResponse.text)
    changes = changesJson["commit"]["message"]
    print("")
    print("Changelog")
    print(changes)
    print("")
else:
    logger("Posiadasz aktualną wersję skryptu.")

# Mouse controller
mouse = MouseController()
# Keyboard controller
keyboard = KeyboardController()

# Release all necessary keys
def releaseAll():
    mouse.release(Button.left)
    keyboard.release("a")
    keyboard.release("d")

# Function for player moving
def startMoving():
    global miningThreadStop
    global activityRounds, cobblexRounds, dropRounds, eatRounds
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
        activityRounds += 1
        cobblexRounds += 1
        dropRounds += 1
        eatRounds += 1
        startMoving()

def dropSlot(backX, backY):
    time.sleep(0.05)
    dropPosition = (int(config["Slots"]["dropX"]), int(config["Slots"]["dropY"]))
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
    firstRow = (int(config["Slots"]["firstRowX"]), int(config["Slots"]["firstRowY"]))
    mouse.position = firstRow
    firstStart = 1
    for i in range(1, 10):
        if i in dropSlots:
            dropSlot(int(config["Slots"]["firstRowX"]) + (firstStart * int(config["Slots"]["difference"])), int(config["Slots"]["firstRowY"]))
        time.sleep(0.1)
        mouse.position = (int(config["Slots"]["firstRowX"]) + (firstStart * int(config["Slots"]["difference"])), int(config["Slots"]["firstRowY"]))
        firstStart += 1

    # Second row
    secondRow = (int(config["Slots"]["secondRowX"]), int(config["Slots"]["secondRowY"]))
    mouse.position = secondRow
    secondStart = 1
    for i in range(10, 19):
        if i in dropSlots:
            dropSlot(int(config["Slots"]["secondRowX"]) + (secondStart * int(config["Slots"]["difference"])), int(config["Slots"]["secondRowY"]))
        time.sleep(0.1)
        mouse.position = (int(config["Slots"]["secondRowX"]) + (secondStart * int(config["Slots"]["difference"])), int(config["Slots"]["secondRowY"]))
        secondStart += 1

    # Third row
    thirdRow = (int(config["Slots"]["thirdRowX"]), int(config["Slots"]["thirdRowY"]))
    mouse.position = thirdRow
    thirdStart = 1
    for i in range(19, 28):
        if i in dropSlots:
            dropSlot(int(config["Slots"]["thirdRowX"]) + (thirdStart * int(config["Slots"]["difference"])), int(config["Slots"]["thirdRowY"]))
        time.sleep(0.1)
        mouse.position = (int(config["Slots"]["thirdRowX"]) + (thirdStart * int(config["Slots"]["difference"])), int(config["Slots"]["thirdRowY"]))
        thirdStart += 1

    # Fourth row
    fourthRow = (int(config["Slots"]["fourthRowX"]), int(config["Slots"]["fourthRowY"]))
    mouse.position = fourthRow
    fourthStart = 1
    for i in range(28, 37):
        if i in dropSlots:
            dropSlot(int(config["Slots"]["fourthRowX"]) + (fourthStart * int(config["Slots"]["difference"])), int(config["Slots"]["fourthRowY"]))
        time.sleep(0.1)
        mouse.position = (int(config["Slots"]["fourthRowX"]) + (fourthStart * int(config["Slots"]["difference"])), int(config["Slots"]["fourthRowY"]))
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
    time.sleep(commandsDelayInSeconds)

# Activity
def activity():
    global miningThread
    global miningThreadStop
    global food
    global activityThreadStop
    global activityRounds, cobblexRounds, dropRounds, eatRounds
    global activityRoundsConfig, cobblexRoundsConfig, dropRoundsConfig, eatRoundsConfig
    global activityCommands, cobblexCommands

    while True:
        if activityThreadStop == True:
            break
        if activityRounds == (activityRoundsConfig - 1) or cobblexRounds == (cobblexRoundsConfig - 1) or dropRounds == (dropRoundsConfig - 1) or eatRounds == (eatRoundsConfig - 1):
            if miningThread != None:
                miningThreadStop = True
                miningThread.join()
                miningThread = None

                # Activity
                if activityRounds == activityRoundsConfig:
                    for command in activityCommands:
                        sendCommand(command)
                    
                    activityRounds = 0
                # Cobblex commands
                if cobblexRounds == cobblexRoundsConfig:
                    for command in cobblexCommands:
                        sendCommand(command)
                    
                    cobblexRounds = 0
                # Drop slots
                if dropRounds == dropRoundsConfig:
                    drop()
                    dropRounds = 0
                # Eating
                if food >= 1 and food <= 9:
                    if eatRounds == eatRoundsConfig:
                        eat()
                        eatRounds = 0

                # Left click
                mouse.release(Button.left)
                time.sleep(0.1)

                # Start moving thread
                miningThreadStop = False
                miningThread = threading.Thread(target = startMoving)
                miningThread.start()

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