import tkinter
import time
import threading
from tkinter import Tk

import modules.config as config
import modules.logger as logger
import modules.check_version as check_version
import modules.welcome_message as welcome_message
import modules.windows_management as windows_management

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
# ----- DO NOT TOUCH THIS SECTION -----

welcome_message.send()
logger.info("Włączanie skryptu...")
check_version.run()

# Release all necessary keys
def releaseAll():
    windows_management.mouse_left_click_release()
    windows_management.release_key("a")
    windows_management.release_key("d")

# Function for player moving
def startMoving():
    global miningThreadStop
    global activityRounds, cobblexRounds, dropRounds, eatRounds
    while True:
        if miningThreadStop == True:
            break

        windows_management.mouse_left_click_press()
        if config.fastPickaxe:
            # Delays
            horizontalDelay = (config.horizontalStones / 4) - 0.2
            verticalDelay = (config.verticalStones / 4) - 0.2

            # Move to the right
            windows_management.press_key("d")
            time.sleep(horizontalDelay)
            windows_management.release_key("d")

            # Move forward
            if config.verticalStones > 0:
                windows_management.press_key("w")
                time.sleep(verticalDelay)
                windows_management.release_key("w")

            # Move to the left
            windows_management.press_key("a")
            time.sleep(horizontalDelay)
            windows_management.release_key("a")

            # Move backward
            if config.verticalStones > 0:
                windows_management.press_key("s")
                time.sleep(verticalDelay)
                windows_management.release_key("s")
        else:
            time.sleep(5)
        activityRounds += 1
        cobblexRounds += 1
        dropRounds += 1
        eatRounds += 1
        startMoving()

def drop_slot(backX, backY):
    windows_management.mouse_move(backX, backY)
    time.sleep(0.05)
    windows_management.mouse_left_click()
    time.sleep(0.05)
    windows_management.mouse_right_click()
    time.sleep(0.05)
    windows_management.mouse_move(config.slots["dropX"], config.slots["dropY"])
    time.sleep(0.05)
    windows_management.mouse_left_click()
    time.sleep(0.05)
    windows_management.mouse_move(backX, backY)
    time.sleep(0.05)

def calculate_inventory_mouse_position(slot):
    # Rows
    firstRowIndexes = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    secondRowIndexes = [10, 11, 12, 13, 14, 15, 16, 17, 18]
    thirdRowIndexes = [19, 20, 21, 22, 23, 24, 25, 26, 27]
    fourthRowIndexes = [28, 29, 30, 31, 32, 33, 34, 35, 36]

    if config.backgroundMining["isBlazingPack"]:
        if slot in firstRowIndexes:
            return (config.slots["firstRowX"] + (firstRowIndexes.index(slot) * config.slots["difference"]), -config.slots["firstRowY"] + 50)
        elif slot in secondRowIndexes:
            return (config.slots["firstRowX"] + (secondRowIndexes.index(slot) * config.slots["difference"]), -config.slots["firstRowY"] + 50 + config.slots["difference"])
        elif slot in thirdRowIndexes:
            return (config.slots["firstRowX"] + (thirdRowIndexes.index(slot) * config.slots["difference"]), -config.slots["firstRowY"] + 50 + (2 * config.slots["difference"]))
        elif slot in fourthRowIndexes:
            return (config.slots["firstRowX"] + (fourthRowIndexes.index(slot) * config.slots["difference"]), -config.slots["firstRowY"] + 50 + (3 * config.slots["difference"]))
    else:
        if slot in firstRowIndexes:
            return (config.slots["firstRowX"] + (firstRowIndexes.index(slot) * config.slots["difference"]), config.slots["firstRowY"] - 20)
        elif slot in secondRowIndexes:
            return (config.slots["firstRowX"] + (secondRowIndexes.index(slot) * config.slots["difference"]), config.slots["firstRowY"] - 20 + config.slots["difference"])
        elif slot in thirdRowIndexes:
            return (config.slots["firstRowX"] + (thirdRowIndexes.index(slot) * config.slots["difference"]), config.slots["firstRowY"] - 20 + (2 * config.slots["difference"]))
        elif slot in fourthRowIndexes:
            return (config.slots["firstRowX"] + (fourthRowIndexes.index(slot) * config.slots["difference"]), config.slots["firstRowY"] - 20 + (3 * config.slots["difference"]))

def drop():
    global dropSlots

    # Open inventory
    time.sleep(0.25)
    windows_management.press_key("e")
    windows_management.release_key("e")
    time.sleep(0.25)

    for slot in dropSlots:
        drop_slot(calculate_inventory_mouse_position(slot))

    # Close inventory
    time.sleep(0.25)
    windows_management.press_key("e")
    windows_management.release_key("e")
    time.sleep(0.25)

def eat():
    time.sleep(0.1)
    windows_management.press_key(str(config.food))
    windows_management.release_key(str(config.food))
    time.sleep(0.1)
    windows_management.mouse_right_click_press()
    time.sleep(3)
    windows_management.mouse_right_click_release()
    time.sleep(0.1)
    windows_management.press_key(str(config.pickaxe))
    windows_management.release_key(str(config.pickaxe))

def sendCommand(command):
    windows_management.mouse_left_click_release()
    windows_management.press_key("t")
    windows_management.release_key("t")
    time.sleep(0.5)
    windows_management.type_string("/" + command)
    time.sleep(0.5)
    windows_management.click_enter()
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

                time.sleep(1)

                # Start moving thread
                miningThreadStop = False
                miningThread = threading.Thread(target = startMoving)
                miningThread.start()

def start_mining():
    global mining
    global miningThread
    global miningThreadStop
    global activityThread
    global activityThreadStop
    global roundCount
    if mining == False:
        if config.backgroundMining["isBlazingPack"]:
            logger.info("Sending blazingpack messages")
            windows_management.send_blazingpack_messages()
            time.sleep(1)
            logger.info("Minimizing blazingpack window")
            windows_management.minimize()
        time.sleep(2)

        # Start moving thread
        miningThread = threading.Thread(target = startMoving)
        miningThread.start()

        roundCount = 0

        # Start command thread
        activityThread = threading.Thread(target = activity)
        activityThread.start()
        
        mining = True
        logger.info("Zaczęto kopanie na AFK'u!")

def stop_mining():
    global mining
    global miningThread
    global miningThreadStop
    global activityThread
    global activityThreadStop
    global roundCount
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

# GUI initialization
root = Tk()
root.title("MineAFK (" + config.version + ")")
root.iconbitmap('./app/pickaxe.ico')
root.geometry("320x180")

start_mining_button = tkinter.Button(root, text="Start", width=8, pady=8, command=start_mining)
start_mining_button.pack(padx=10, pady=10)

stop_mining_button = tkinter.Button(root, text="Stop", width=8, pady=8, command=stop_mining)
stop_mining_button.pack(padx=10, pady=10)

root.mainloop()
