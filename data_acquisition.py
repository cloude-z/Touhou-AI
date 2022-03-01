from pydoc import locate
import pyautogui
import numpy as np
import time
import win32gui
import cv2
import keyboard
import csv

def GetWindowList():
    """
    将当前桌面上窗口的标题名打印至屏幕。
    Print the title name of all the current windows on the desktop.
    """
    win32gui.EnumWindows(lambda x, L: print(win32gui.GetWindowText(x)), None)

def WindowInit(WinName=None):
    """
    查找目标窗口，返回该窗口的句柄与屏幕坐标值。
    Find the target window and return the handle of the window with the value of window's coordinate.
    """
    if WinName == None:
        # WinName = "Python_Zettelkasten - Obsidian v0.12.19"
        WinName = "東方妖々夢　～ Perfect Cherry Blossom. ver 1.00b"
    else:
        WinName = WinName
    win_handle = win32gui.FindWindow(None, WinName)
    
    try:
        locat = win32gui.GetWindowRect(win_handle)   # left, top, right, bottom: 左边框，上边框，右边框，下边框
        win32gui.SetForegroundWindow(win_handle)
    except Exception:   # 检查游戏是否运行。Check if the game is running.
        if win_handle == 0:
            print("未开启程序 -- 退出 --")
            exit()
    return locat, win_handle

i = 0
def ScreenShotCapture(locat):
    """
    保存游戏屏幕截图。
    Save a screenshot of the game.
    """
    global i
    Img = pyautogui.screenshot(region=(locat[0]+35, locat[1]+45, locat[2]-locat[0]-262, locat[3]-locat[1]-64))
    Img = cv2.cvtColor(np.asarray(Img), cv2.COLOR_RGB2BGR)
    Img = cv2.resize(Img, (150,200))
    cv2.imwrite('Dataset/Capture_10/'+ str(i) + '.jpg', Img)
    i = i + 1

def KeyboardListener():
    """
    监听键盘当前操作，并将操作写入 CSV 文件。
    Listen to the current operation of the keyboard and append that operation to a CSV file.
    """
    key_list = [0, 0, 0, 0, 0] # 顺序 - 上下左右Shift。Order - Up Down Left Right Shift.
    if 72 in keyboard._pressed_events:
        key_list[0] = 1
    if 80 in keyboard._pressed_events:
        key_list[1] = 1
    if 75 in keyboard._pressed_events:
        key_list[2] = 1
    if 77 in keyboard._pressed_events:
        key_list[3] = 1
    if 42 in keyboard._pressed_events:
        key_list[4] = 1

    with open("Dataset/KeyCapture_10.csv", "a", newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(key_list)
    print('\r' + str(key_list), end='')

# 初始化截屏区域的坐标，窗口句柄。Initialize the coordinates of screenshot area and window's handle
locat, win_handle = WindowInit()
# 等待15s用于打开游戏。Wait 15s for opening the game.
print('Waiting:', end='') 
for l in range(14):
    time.sleep(1)
    print('.', end='.', flush=True)

def DataAquisition(locat):
    """
    采集一次数据，即一张截图 + 对应键盘键位。
    Acquire the data once, i.e. one screenshot + the corresponding keyboard keys.
    """
    ScreenShotCapture(locat)
    KeyboardListener()

# 
keyboard.hook(lambda _: DataAquisition(locat))
keyboard.wait('esc')

# 获取桌面上的窗口列表 Get a list including all the names of current windows on the desktop.
# GetWindowList()