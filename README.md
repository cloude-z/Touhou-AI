# Tohou-AI

> This project references some ideas and codes from: https://github.com/nkMengXin/ResNet_Touhou

The most original motivation for me to enter the field of AI is, sometimes it is more funny to watch others to play the
game. Just like when I get back to the old days and sat with my friends in front of a computer together, watching
him or me playing the game, and chatting, having fun. So when I first time saw it is possible to train one own AI to 
play some shit, it's like wow that's so awesome! So, why can't I do one by myself?

But in the end, this is only a sample project for myself for kind of training, learning and there ain't too hard theory 
or something behind it, so I just think there won't be too many guys visit. Here are therefore only some simple 
introductions about the build-up and functions. (As for the end effect with some gifs and pics, I'll upload in the 
future to let you, the visitors, can directly see what it finally seems to be like!)

## data_acquisition.py

To acquire the datasets by oneself, which include the screenshots of game and the movements of keyboard serving as 
labels. The function is achieved by the packages `win32gui`, `keyboard`, `cv2`, `pyautogui` etc. which I guess can be
minimalized (some of them really redundant).

## data_rename.py

If one names the files in the sequence like `1.jpg, 2.jpg, ..., 10.jpg`. Finally when the files are read into a list or 
tensor, the sequence will be changed to `1.jpg, 10.jpg, 11.jpg, ..., 2.jpg, ...`, which is caused by the naming rule 
within the system I guess. The order will end up to be messed up. So, this file is to reorder the messed sequence 
`1, 2, 3` to `0001, 0002, 0003`.

## data_load.py

hmmm, it is data_load

## model.py

hmmm, it's model

## train_eval.py

Some function for model training

## CNN.ipynb

The model is actually trained and evaluated here because of the better visualization and modification.

## TohoAI

The real shit of TohoAI!