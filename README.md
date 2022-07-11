# Tohou-AI

> This project references some ideas and codes from: https://github.com/nkMengXin/ResNet_Touhou

The most original motivation for me to enter the field of AI is, sometimes it is more funny to watch others to play the
game. Just like when I get back to the old days and sat with my friends in front of a computer together, watching
him or me playing the game, and chatting, having fun. So when I first time saw it is possible to train one own AI to 
play some shit, it's like wow that's so awesome! So, why can't I do one by myself?

But eventually, this is only a sample project for myself for kind of training, learning and there ain't too hard theory 
or something behind it, so I just think there won't be too many guys visit. Here are therefore only some simple 
introductions about the build-up and functions. 

## Screenshot

One can check `video.mp4` file, I don't know why Github can't play video.

<video src="./video.mp4" controls="controls" width="480" height="640"></video>

## Usage

Download the code first and 'cuz the model was trained on Perfect Cherry Blossom (東方妖々夢, Tōhō Yōyōmu, lit. "Ghostly Dream"), the 7th game in the series of Touho Project. If you want to used the pre-trained `.pth` model in this repository, plz buy or download the game from somewhere you can :). Ofc, you can train your own model by oneself!

```
git clone https://github.com/bakalaugh/Toho-AI.git
```
#### Requirements
|Package|Version|
|:--|:--|
|pytorch|1.9.0|
|sklearn|-|
|cv2|-|
|pandas|-|
|matplotlib|-|
|pyautogui|-|
|pywin32|-|
|keyboard|-|

#### TohoAI.py

The real shit of TohoAI to play the game! Open the game first, then run `TohoAI.py` it will let you play the game automatically.

## Train own model

#### data_acquisition.py

To acquire the datasets by oneself, which include the screenshots of game and the movements of keyboard serving as 
labels. The function is achieved by the packages `win32gui`, `keyboard`, `cv2`, `pyautogui` etc. which I guess can be
minimalized (some of them really redundant).

#### data_rename.py

If one names the files in the sequence like `1.jpg, 2.jpg, ..., 10.jpg`. Finally when the files are read into a list or 
tensor, the sequence will be changed to `1.jpg, 10.jpg, 11.jpg, ..., 2.jpg, ...`, which is caused by the naming rule 
within the system. The order will end up to be messed up. So, this file is to reorder the messed sequence 
`1, 2, 3` to `0001, 0002, 0003` ('cuz I messed it up at the very first :( ).

#### data_load.py
#### model.py
#### train_eval.py

Some functions for model training and data feeding.

#### CNN.ipynb
#### CNN.py

The model is actually trained and evaluated in `.ipynb` file because of the better visualization and modification. If needed, one can use `CNN.py` as alternative.