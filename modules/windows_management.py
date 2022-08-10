import win32gui, win32con, win32api
import time
import modules.config as config

hwnd = win32gui.FindWindow(None, config.backgroundMining["windowName"])

isMouseLeftButtonPressed = False
isMouseRightButtonPressed = False

# Mouse
def mouse_left_click_press():
    global isMouseLeftButtonPressed
    if isMouseLeftButtonPressed:
        return
    win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, 0, 0)
    isMouseLeftButtonPressed = True

def mouse_right_click_press():
    global isMouseRightButtonPressed
    if isMouseRightButtonPressed:
        return
    win32api.PostMessage(hwnd, win32con.WM_RBUTTONDOWN, 0, 0)
    isMouseRightButtonPressed = True

def mouse_left_click():
    mouse_left_click_press()
    time.sleep(0.02)
    mouse_left_click_release()

def mouse_left_click_release():
    global isMouseLeftButtonPressed
    if not isMouseLeftButtonPressed:
        return
    win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, 0)
    isMouseLeftButtonPressed = False

def mouse_right_click_release():
    global isMouseRightButtonPressed
    if not isMouseRightButtonPressed:
        return
    win32api.PostMessage(hwnd, win32con.WM_RBUTTONUP, 0, 0)
    isMouseRightButtonPressed = False

def mouse_right_click():
    mouse_right_click_press()
    time.sleep(0.02)
    mouse_right_click_release()

def mouse_move(x, y):
    win32api.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x, y))

# Keyboard
def get_key_data(key):
    return {
        'q': {
            'bits': '00010000',
            'vcode': 0x51,
        },
        'w': {
            'bits': '00010001',
            'vcode': 0x57,
        },
        'e': {
            'bits': '00010010',
            'vcode': 0x45,
        },
        'r': {
            'bits': '00010011',
            'vcode': 0x52,
        },
        't': {
            'bits': '00010100',
            'vcode': 0x54,
        },
        'y': {
            'bits': '00010101',
            'vcode': 0x59,
        },
        'u': {
            'bits': '00010110',
            'vcode': 0x55,
        },
        'i': {
            'bits': '00010111',
            'vcode': 0x49,
        },
        'o': {
            'bits': '00011000',
            'vcode': 0x4F,
        },
        'p': {
            'bits': '00011001',
            'vcode': 0x50,
        },
        'a': {
            'bits': '00011110',
            'vcode': 0x41,
        },
        's': {
            'bits': '00011111',
            'vcode': 0x53,
        },
        'd': {
            'bits': '00100000',
            'vcode': 0x44
        },
        'f': {
            'bits': '00100001',
            'vcode': 0x46,
        },
        'g': {
            'bits': '00100010',
            'vcode': 0x47,
        },
        'h': {
            'bits': '00100011',
            'vcode': 0x48,
        },
        'j': {
            'bits': '00100100',
            'vcode': 0x4A,
        },
        'k': {
            'bits': '00100101',
            'vcode': 0x4B,
        },
        'l': {
            'bits': '00100110',
            'vcode': 0x4C,
        },
        'z': {
            'bits': '01010110',
            'vcode': 0x5A,
        },
        'x': {
            'bits': '00101101',
            'vcode': 0x58,
        },
        'c': {
            'bits': '00101110',
            'vcode': 0x43,
        },
        'v': {
            'bits': '00101111',
            'vcode': 0x56,
        },
        'b': {
            'bits': '00110000',
            'vcode': 0x42,
        },
        'n': {
            'bits': '00110001',
            'vcode': 0x4E,
        },
        'm': {
            'bits': '00110010',
            'vcode': 0x4D,
        },
        'ENTER': {
            'bits': '00011100',
            'vcode': 0x0D,
        },
        ' ': {
            'bits': '00111001',
            'vcode': 0x20,
        },
        '/': {
            'bits': '00110101',
            'vcode': 0xBF,
        },
        '-': {
            'bits': '00001100',
            'vcode': 0xBD,
        },
        '0': {
            'bits': '00001011',
            'vcode': 0x30,
        },
        '1': {
            'bits': '00000010',
            'vcode': 0x31,
        },
        '2': {
            'bits': '00000011',
            'vcode': 0x32,
        },
        '3': {
            'bits': '00000100',
            'vcode': 0x33,
        },
        '4': {
            'bits': '00000101',
            'vcode': 0x34,
        },
        '5': {
            'bits': '00000110',
            'vcode': 0x35,
        },
        '6': {
            'bits': '00000111',
            'vcode': 0x36,
        },
        '7': {
            'bits': '00001000',
            'vcode': 0x37,
        },
        '8': {
            'bits': '00001001',
            'vcode': 0x38,
        },
        '9': {
            'bits': '00001010',
            'vcode': 0x39,
        },
        'ESCAPE': {
            'bits': '00000001',
            'vcode': 0x1B,
        }
    }[key]

def press_key(key):
    key_data = get_key_data(key)
    bits = int("0" + "0" + "0" + "0000" + "0" + key_data['bits'] + "0000000000000001", 2)
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, key_data['vcode'], bits)


def release_key(key):
    key_data = get_key_data(key)
    bits = int("1" + "1" + "0" + "0000" + "0" + key_data['bits'] + "0000000000000001", 2)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, key_data['vcode'], bits)

def click_enter():
    press_key('ENTER')
    time.sleep(0.02)
    release_key('ENTER')

def click_escape():
    press_key('ESCAPE')
    time.sleep(0.02)
    release_key('ESCAPE')

def type_string(string):
    for char in string:
        press_key(char)
        time.sleep(0.1)
        release_key(char)

def minimize():
    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

def maximize():
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

# Blazingpack specific
def send_blazingpack_messages():
    win32api.PostMessage(hwnd, win32con.WM_ACTIVATEAPP, 1, 0)
    win32api.PostMessage(hwnd, win32con.WM_NCACTIVATE, 0, 0)
    win32api.PostMessage(hwnd, win32con.WM_ACTIVATE, 0, 0)
    win32api.PostMessage(hwnd, win32con.WM_IME_NOTIFY, win32con.IMN_OPENSTATUSWINDOW, 0)
    win32api.PostMessage(hwnd, win32con.WM_SETFOCUS, 0, 0)
