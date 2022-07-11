import torch
import torchvision.transforms as T

import pyautogui
import win32api
import win32con
import ctypes
import time

import model
from data_acquisition import WindowInit


def GameScreenShot(locat):
    Img = pyautogui.screenshot(region=(locat[0]+35, locat[1]+45, locat[2]-locat[0]-262, locat[3]-locat[1]-64))
    transforms = T.Compose([T.ToTensor(), T.Resize((200, 150))])
    Img = transforms(Img)
    Img = torch.unsqueeze(Img, 0)
    return Img.to(device)


MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA


def PressAndRelease(key, MapVirtualKey=MapVirtualKey):
    # 0x25 left; 0x26 up; 0x27 right; 0x28 down; 0xA0 left shift; 0x0D enter; 0x5A z
    win32api.keybd_event(key, MapVirtualKey(key, 0), 0, 0)
    time.sleep(0.02)
    win32api.keybd_event(key, MapVirtualKey(key, 0), win32con.KEYEVENTF_KEYUP, 0)


device = torch.device("cuda" if torch.cuda.is_available() else 'cpu')
print("Using device: {}".format(device))

# Load the pre-trained model
CNN_model = model.toho_CNN()
CNN_model.load_state_dict(torch.load("CNN_param.pth"))
CNN_model = CNN_model.to(device)

# Capture the screenshot of game [left, top, right, bottom] and predict the output
locate, win_handle = WindowInit()
keys = [0x26, 0x28, 0x25, 0x27, 0xA0]   # up, down, left, right ,shift

# Initialize the game
time.sleep(5)
win32api.keybd_event(0x5A, MapVirtualKey(0x5A, 0), 0, 0)
time.sleep(0.02)
win32api.keybd_event(0x5A, MapVirtualKey(0x5A, 0), win32con.KEYEVENTF_KEYUP, 0)

for _ in range(4):
    time.sleep(1)

    win32api.keybd_event(0x5A, MapVirtualKey(0x5A, 0), 0, 0)
    time.sleep(0.02)
    win32api.keybd_event(0x5A, MapVirtualKey(0x5A, 0), win32con.KEYEVENTF_KEYUP, 0)

while True:
    # Movement of the character
    Img = GameScreenShot(locate)
    with torch.no_grad():
        keyMove = CNN_model(Img).squeeze()
        keyInx = torch.nonzero(keyMove >= 0.5)

    if keyInx.shape[0] != 0:
        for e in keyInx:
            PressAndRelease(keys[e])
    else:
        time.sleep(0.02)

    # Open the fire
    win32api.keybd_event(0x5A, MapVirtualKey(0x5A, 0), 0, 0)
    time.sleep(0.01)
    win32api.keybd_event(0x5A, MapVirtualKey(0x5A, 0), win32con.KEYEVENTF_KEYUP, 0)

