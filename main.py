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
mining_thread = None
mining_thread_stop = False
activity_thread = None
activity_thread_stop = False
drop_slots = [int(x) for x in config.drop_slots]
activity_rounds = 0
cobblex_rounds = 0
drop_rounds = 0
eat_rounds = 0
# ----- DO NOT TOUCH THIS SECTION -----

# Mouse controller
mouse = MouseController()
# Keyboard controller
keyboard = KeyboardController()

welcome_message.send()
logger.info("Włączanie skryptu...")
check_version.run()

# Release all necessary keys
def release_all():
    mouse.release(Button.left)
    keyboard.release("a")
    keyboard.release("d")

# Function for player moving
def start_moving():
    global mining_thread_stop
    global activity_rounds, cobblex_rounds, drop_rounds, eat_rounds
    while True:
        if mining_thread_stop == True:
            break

        mouse.press(Button.left)
        if config.fast_pickaxe:
            # Delays
            horizontal_delay = (config.horizontal_stones / 4) - 0.2
            vertical_delay = (config.vertical_stones / 4) - 0.2

            # Move to the right
            keyboard.press("d")
            time.sleep(horizontal_delay)
            keyboard.release("d")

            # Move forward
            if config.vertical_stones > 0:
                keyboard.press("w")
                time.sleep(vertical_delay)
                keyboard.release("w")

            # Move to the left
            keyboard.press("a")
            time.sleep(horizontal_delay)
            keyboard.release("a")

            # Move backward
            if config.vertical_stones > 0:
                keyboard.press("s")
                time.sleep(vertical_delay)
                keyboard.release("s")
        else:
            time.sleep(5)
        activity_rounds += 1
        cobblex_rounds += 1
        drop_rounds += 1
        eat_rounds += 1
        start_moving()

def drop_slot(x, y):
    mouse.position = (x, y)
    time.sleep(0.05)
    mouse.click(Button.left)
    time.sleep(0.05)
    mouse.click(Button.right)
    time.sleep(0.05)
    mouse.position = (config.slots["drop_x"], config.slots["drop_y"])
    time.sleep(0.05)
    mouse.click(Button.left)
    time.sleep(0.05)
    mouse.position = (x, y)
    time.sleep(0.05)

def calculate_inventory_mouse_position(slot):
    # Rows
    first_row_indexes = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    second_row_indexes = [10, 11, 12, 13, 14, 15, 16, 17, 18]
    third_row_indexes = [19, 20, 21, 22, 23, 24, 25, 26, 27]
    fourth_row_indexes = [28, 29, 30, 31, 32, 33, 34, 35, 36]

    if slot in first_row_indexes:
        return (config.slots["first_row_x"] + (first_row_indexes.index(slot) * config.slots["difference"]), config.slots["first_row_y"])
    elif slot in second_row_indexes:
        return (config.slots["first_row_x"] + (second_row_indexes.index(slot) * config.slots["difference"]), config.slots["first_row_y"] + config.slots["difference"])
    elif slot in third_row_indexes:
        return (config.slots["first_row_x"] + (third_row_indexes.index(slot) * config.slots["difference"]), config.slots["first_row_y"] + (2 * config.slots["difference"]))
    elif slot in fourth_row_indexes:
        return (config.slots["first_row_x"] + (fourth_row_indexes.index(slot) * config.slots["difference"]), config.slots["first_row_y"] + (3 * config.slots["difference"]))

def drop():
    global drop_slots

    # Open inventory
    time.sleep(0.25)
    keyboard.press("e")
    keyboard.release("e")
    time.sleep(0.25)

    for slot in drop_slots:
        drop_slot(calculate_inventory_mouse_position(slot)[0], calculate_inventory_mouse_position(slot)[1])

    # Close inventory
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

def send_command(command):
    mouse.release(Button.right)
    keyboard.press("t")
    keyboard.release("t")
    time.sleep(0.2)
    keyboard.press("/")
    keyboard.release("/")
    time.sleep(0.2)
    keyboard.type(command)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    time.sleep(config.commands_delay_in_seconds)

# Activity
def activity():
    global mining_thread
    global mining_thread_stop
    global activity_thread_stop
    global activity_rounds, cobblex_rounds, drop_rounds, eat_rounds

    while True:
        if activity_thread_stop == True:
            break
        if activity_rounds == (config.activity_rounds_config - 1) or cobblex_rounds == (config.cobblex_rounds_config - 1) or drop_rounds == (config.drop_rounds_config - 1) or eat_rounds == (config.eat_rounds_config - 1):
            if mining_thread != None:
                mining_thread_stop = True
                mining_thread.join()
                mining_thread = None

                # Activity
                if activity_rounds == config.activity_rounds_config:
                    for command in config.activity_commands:
                        send_command(command)
                    activity_rounds = 0
                # Cobblex commands
                if cobblex_rounds == config.cobblex_rounds_config:
                    for command in config.cobblex_commands:
                        send_command(command)
                    cobblex_rounds = 0
                # Drop slots
                if drop_rounds == config.drop_rounds_config:
                    drop()
                    drop_rounds = 0
                # Eating
                if config.food >= 1 and config.food <= 9:
                    if eat_rounds == config.eat_rounds_config:
                        eat()
                        eat_rounds = 0

                time.sleep(1)

                # Start moving thread
                mining_thread_stop = False
                mining_thread = threading.Thread(target = start_moving)
                mining_thread.start()

def start_mining():
    global mining
    global mining_thread
    global mining_thread_stop
    global activity_thread
    global activity_thread_stop
    global round_count
    if mining == False:
        # Start moving thread
        mining_thread = threading.Thread(target = start_moving)
        mining_thread.start()

        round_count = 0

        # Start command thread
        activity_thread = threading.Thread(target = activity)
        activity_thread.start()
        
        mining = True
        logger.info("Zaczęto kopanie na AFK'u!")

def stop_mining():
    global mining
    global mining_thread
    global mining_thread_stop
    global activity_thread
    global activity_thread_stop
    global round_count
    logger.info("Zatrzymywanie kopania...")
    logger.info("Zaczekaj na zakończenie wątków!")

    # Stop mining
    mining = False
    round_count = 0
    activity_thread_stop = True
    activity_thread.join()
    activity_thread = None
    mining_thread_stop = True
    mining_thread.join()
    mining_thread = None

    logger.info("Kopanie zostało zatrzymane!")

    # Release all necessary keys
    release_all()

    activity_thread_stop = False
    mining_thread_stop = False

# ----------------------------------------------------------------------------------------------------------------------

def on_press(key):
    pass

def on_release(key):
    if key == KeyboardManager.Key.f8:
        start_mining()
    if key == KeyboardManager.Key.f9:
        stop_mining()
    if key == KeyboardManager.Key.f10:
        release_all()
        return False

with KeyboardManager.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
listener = KeyboardManager.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()
