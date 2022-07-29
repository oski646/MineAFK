from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
from pynput import keyboard as KeyboardManager
import time
import threading

import modules.config as config
import modules.logger as logger
import modules.check_version as check_version
import modules.welcome_message as welcome_message

# ----- DO NOT TOUCH THIS SECTION -----
mining = False
miningThread = None
miningThreadStop = False
activityThread = None
activityThreadStop = False
dropSlots = [int(x) for x in config.dropSlots]
activityRounds = 0
cobblexRounds = 0
dropRounds = 0
eatRounds = 0
mouse = MouseController()
keyboard = KeyboardController()
# ----- DO NOT TOUCH THIS SECTION -----

welcome_message.send()
logger.info("Włączanie skryptu...")
check_version.run()

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

        mouse.press(Button.left)
        delay = (config.stones / 4) - 0.2
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
    dropPosition = (config.slots["dropX"], config.slots["dropY"])
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
    firstRow = (config.slots["firstRowX"], config.slots["firstRowY"])
    mouse.position = firstRow
    firstStart = 1
    for i in range(1, 10):
        if i in dropSlots:
            dropSlot(config.slots["firstRowX"] + (firstStart * config.slots["difference"]), config.slots["firstRowY"])
        time.sleep(0.1)
        mouse.position = (config.slots["firstRowX"] + (firstStart * config.slots["difference"]), config.slots["firstRowY"])
        firstStart += 1

    # Second row
    secondRow = (config.slots["secondRowX"], config.slots["secondRowY"])
    mouse.position = secondRow
    secondStart = 1
    for i in range(10, 19):
        if i in dropSlots:
            dropSlot(config.slots["secondRowX"] + (secondStart * config.slots["difference"]), config.slots["secondRowY"])
        time.sleep(0.1)
        mouse.position = (config.slots["secondRowX"] + (secondStart * config.slots["difference"]), config.slots["secondRowY"])
        secondStart += 1

    # Third row
    thirdRow = (config.slots["thirdRowX"], config.slots["thirdRowY"])
    mouse.position = thirdRow
    thirdStart = 1
    for i in range(19, 28):
        if i in dropSlots:
            dropSlot(config.slots["thirdRowX"] + (thirdStart * config.slots["difference"]), config.slots["thirdRowY"])
        time.sleep(0.1)
        mouse.position = (config.slots["thirdRowX"] + (thirdStart * config.slots["difference"]), config.slots["thirdRowY"])
        thirdStart += 1

    # Fourth row
    fourthRow = (config.slots["fourthRowX"], config.slots["fourthRowY"])
    mouse.position = fourthRow
    fourthStart = 1
    for i in range(28, 37):
        if i in dropSlots:
            dropSlot(config.slots["fourthRowX"] + (fourthStart * config.slots["difference"]), config.slots["fourthRowY"])
        time.sleep(0.1)
        mouse.position = (config.slots["fourthRowX"] + (fourthStart * config.slots["difference"]), config.slots["fourthRowY"])
        fourthStart += 1

    time.sleep(0.25)

    keyboard.press("e")
    keyboard.release("e")

    time.sleep(0.25)

def eat():
    time.sleep(0.1)
    keyboard.press(str(config.food))
    keyboard.release(str(config.food))
    time.sleep(0.1)
    mouse.press(Button.right)
    time.sleep(3)
    mouse.release(Button.right)
    time.sleep(0.1)
    keyboard.press(str(config.pickaxe))
    keyboard.release(str(config.pickaxe))

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
    time.sleep(config.commandsDelayInSeconds)

# Activity
def activity():
    global miningThread
    global miningThreadStop
    global activityThreadStop
    global activityRounds, cobblexRounds, dropRounds, eatRounds

    while True:
        if activityThreadStop == True:
            break
        if activityRounds == (config.activityRoundsConfig - 1) or cobblexRounds == (config.cobblexRoundsConfig - 1) or dropRounds == (config.dropRoundsConfig - 1) or eatRounds == (config.eatRoundsConfig - 1):
            if miningThread != None:
                miningThreadStop = True
                miningThread.join()
                miningThread = None

                # Activity
                if activityRounds == config.activityRoundsConfig:
                    for command in config.activityCommands:
                        sendCommand(command)
                    
                    activityRounds = 0
                # Cobblex commands
                if cobblexRounds == config.cobblexRoundsConfig:
                    for command in config.cobblexCommands:
                        sendCommand(command)
                    
                    cobblexRounds = 0
                # Drop slots
                if dropRounds == config.dropRoundsConfig:
                    drop()
                    dropRounds = 0
                # Eating
                if config.food >= 1 and config.food <= 9:
                    if eatRounds == config.eatRoundsConfig:
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
            logger.info("Zaczęto kopanie na AFK'u!")

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
        logger.info("Zatrzymywanie kopania...")
        logger.info("Zaczekaj na zakończenie wątków!")

        # Stop mining
        mining = False
        roundCount = 0
        activityThreadStop = True
        activityThread.join()
        activityThread = None
        miningThreadStop = True
        miningThread.join()
        miningThread = None

        logger.info("Kopanie zostało zatrzymane!")

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
