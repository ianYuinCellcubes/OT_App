import io
from tkinter import *   # Button, Frame, Tk
from screeninfo import get_monitors     # pip install screeninfo in command line first
import sys, miicam
from PIL import ImageTk, Image # pip install pillow
from screeninfo import get_monitors 
import pathlib

i=0
sWidth=[0,0]
sHeight=[0,0]
for monitor in get_monitors():
    sWidth[i] = monitor.width
    sHeight[i] = monitor.height
    print(i, str(sWidth[i]) + 'x' + str(sHeight[i]))
    i+=1
screenQuad=int(sHeight[1]/4)
screenWidth=sWidth[1]
root = Tk()
x=sWidth[0]-1400
y=400
imgWidth = 0
imgHeight = 0
pData = None
res = 0
temp = miicam.MIICAM_TEMP_DEF
tint = miicam.MIICAM_TINT_DEF
count = 0

root.title("test_Tkinter")
root.geometry("1200x720+"+str(x)+"+"+str(y))
canvasWidth=400; canvasHeight=250
rootCanvas = Canvas(root, width=canvasWidth, height=canvasHeight)
rootCanvas.pack()
arr = miicam.Miicam.EnumV2()
cur = arr[0]
hcam = miicam.Miicam.Open(cur.id)

if hcam:
    res = hcam.get_eSize()
    imgWidth = cur.model.res[res].width
    imgHeight = cur.model.res[res].height
    hcam.put_Option(miicam.MIICAM_OPTION_BYTEORDER, 0)  # Qimage use RGB byte order
    hcam.put_AutoExpoEnable(1)
else:
    print("error")
pData = bytes(miicam.TDIBWIDTHBYTES(imgWidth * 24) * imgHeight)
im = Image.frombytes('RGB', (imgWidth, imgHeight), pData, 'raw')
img = Image.open(io.BytesIO(pData))
im.show()
image = Image.frombytes(pData, imgWidth, imgHeight)
testImg = ImageTk.PhotoImage(data= pData)
root.mainloop()