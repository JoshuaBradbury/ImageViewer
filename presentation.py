from tkinter import *
import os
from random import randint
from PIL import Image, ImageTk
import shutil
import time

if not os.path.exists("img"):
    print("Sorry, a folder called img needs to exists, that contains all the images")

t = Tk()
t.resizable(False, False)
t.attributes('-fullscreen', True)

width = t.winfo_screenwidth()
height = t.winfo_screenheight()
padding = 50

c = Canvas(t, bd=-2, width=width, height=height, bg="#434343")
c.pack()

counter = 0

if not os.path.exists("temp"):
    os.mkdir("temp")

for image in os.listdir("img"):
    im_temp = Image.open("img/" + image).convert("RGBA")
    im_temp = im_temp.resize((width - (padding * 2), height - (padding * 2)), Image.NEAREST)
    im_temp.save("temp/img" + str(counter) + ".ppm", "ppm")
    counter += 1

global tempImage
tempImage = None

images = []

global currentImage
currentImage = 0

for img in os.listdir("temp"):
    images.append(Image.open("temp/" + img))

def getCurrentImage():
    return images[currentImage]

def getNextImage():
    if currentImage == len(images) - 1:
        return images[0]
    else:
        return images[currentImage + 1]

def render():
    global tempImage
    c.delete("all")
    tempImage = ImageTk.PhotoImage(Image.blend(getCurrentImage(), getNextImage(), alpha=((updating + 50) / 50) if updating <= 0 else 0))
    c.create_image(width / 2, height / 2, image=tempImage)
    c.update()
    
running = True

def stop(event):
    running = False
    t.destroy()
    images = []
    tempImage = None

t.bind("<Escape>", stop)

global updating

def left(event):
    global currentImage, updating
    currentImage -= 1
    if currentImage < 0:
        currentImage = len(images) - 1
    updating = -50

def right(event):
    global currentImage, updating
    currentImage += 1
    if currentImage == len(images):
        currentImage = 0
    updating = -50

t.bind("<Left>", left)
t.bind("<Right>", right)

updating = -50
maxUpdating = 50
try:
    while running:
        render()
        if updating == 0:
            currentImage += 1
            if currentImage == len(images):
                currentImage = 0
        if updating == maxUpdating:
            updating = -50
        else:
            updating += 1
        t.update()
except:
    Exception
