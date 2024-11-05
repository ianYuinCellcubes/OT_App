#   ****************************************************************************
#           Optical Tweezer Multi Trap GUI
#               M. Jin  09/21/2024  Basic Trap and path mapping
#                       rev. 101024 trap and path delete/add functions
#                       rev. 101324 curved path defining pts (4) with OT selection
#                                   replaced array declaration splintX=[[0]*nTrap]*6; splintY=[[0]*nTrap]*6 
#                                       with splintY=[[0 for colx in range(6)] for rowy in range(nTrap)] # mButtons[4][5]
#                                       as former declaration results in repeated elements
#                            101624 multi spline path plotting function added with path clearing
#                            101824 searchBox XY shift with traps, target, and paths tracking
#                            102024 image capture of rootCanvas2 searchBox onto rootCanvas
#                            102824 pathX, pathY renamed to splintX, splintY
#                                   declare pathX, pathY as discrete movement coordinates of OT's
#                            110324 splineX, splineY inpolated path coords tabulation routine added
#
#   ****************************************************************************
from tkinter import *   # Button, Frame, Tk
import tkinter.messagebox as msgbox
from PIL import ImageTk, Image, ImageGrab # pip install pillow
import pathlib
from screeninfo import get_monitors     # pip install screeninfo in command line first
import sys #keyboard, pyautogui # for cursor tracking
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import os
from scipy.interpolate import CubicSpline
import numpy as np
import time
import miicam

os.chdir("C:\\CLUTS") # \\ for literal '\' in the string !!!!!!!!
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
screenHeight=sHeight[1]

root = Tk()
#logoImage = PhotoImage(file='C:\C3_logos\C3Logo1.png')
#root.iconphoto(False, logoImage)
#sOffset=int(sWidth[0]/2)-100 #-1400 # offset within monitor size
ysOffset=100
screenAspect=sWidth[0]/sHeight[0]
screenN=2   # menu screen size scaling factor (min 2, max 4 for full screen)
menuWidth=int(sWidth[0]*screenN/4)      # menu window width/height
menuHeight=int(sHeight[0]*screenN*3/8)
xsOffset=sWidth[0]-menuWidth-20      # sWidth[0]-menuWidth-20
ysOffset=+10    # offset within monitor size
root.geometry(str(menuWidth)+"x"+str(menuHeight)+"+"+str(xsOffset)+"+"+str(ysOffset))
root.title("Optical Tweezer Utility")

# ********************** rootCanvas = sub-canvas within root window *********************
subWidth=screenWidth/10; subHeight=screenHeight/10
canvasWidth=int(menuWidth*0.60); canvasHeight=int(menuWidth*0.60/screenAspect) # make this screenN*1/10 of target screen size for simple scaling
tBoxWidth=canvasWidth/10; tBoxHeight=canvasHeight/10
tBextend=6 # tBox extention for smaller screen capture box to avoid capturing boax outline
canvasX=menuWidth-canvasWidth-20; canvasY=150    # offset within subwindow
canOffsetX=int(canvasWidth/2); canOffsetY=int(canvasHeight/2)
trapXoffset=int(0.4*canvasWidth); trapYoffset=int(0.45*canvasHeight) # 2nd macro screen offset
trapWidth=int(canvasWidth/10); trapHeight=int(canvasHeight/10)
rootCanvas = Canvas(root, width=canvasWidth, height=canvasHeight, highlightbackground="black", bg="gray80")
rootCanvas.pack()
rootCanvas2 = Canvas(root, width=canvasWidth, height=canvasHeight, highlightbackground="black", bg="gray80")
rootCanvas2.pack()

# For spline interpolation
pathFig, bx = plt.subplots(figsize=(4,2.5), sharey=True)    # this determines the figure size !!!!!!!!!!!!!!!      
rtCanvas2 = FigureCanvasTkAgg(pathFig, master=rootCanvas2) 
#rtCanvas2.get_tk_widget().pack()

# *******************************************************************************
#  Writer :: IanYu
def onBtnOpen():
    if hcam:
        self.closeCamera()
    else:
        arr = miicam.Miicam.EnumV2()
        if 0 == len(arr):
            msgbox.showwarning("Test", "test444")
        elif 1 == len(arr):
            cur = arr[0]
            openCamera()


# *******************************************************************************

def load_Path():
    global cPath
    cPath=pathlib.Path(__file__).parent.resolve()   # current script directory
    file = str(cPath) + "\\MFC.png"           # 5040 x 3600 
    im=Image.open(file)     #.convert('RGB') # load and separate color
    im=im.resize((canvasWidth, canvasHeight))
    global my_image # !!!!!! must be decleared to show image !!@!!!!!
    my_image=ImageTk.PhotoImage(im) 
    rootCanvas2.create_image(0, 0, image = my_image, anchor = NW)
    #return my_image

def load_Path2():
    #file = str(cPath) + "\\screenshot4.png"           # 5040 x 3600 
    #im2=Image.open(file)     #.convert('RGB') # load and separate color
    im2=take_screenshot()
    im2=im2.resize((canvasWidth, canvasHeight))
    global my_image2
    my_image2=ImageTk.PhotoImage(im2) 
    rootCanvas.create_image(0, 0, image = my_image2, anchor = NW)

grabOffsetX=xsOffset+canvasX+10
grabOffsetY=ysOffset+canvasY+canvasHeight+123
print ("GX ", grabOffsetX, grabOffsetY)

def take_screenshot():
    dx=2; dy=0
    xc=grabOffsetX+trapXoffset; yc=grabOffsetY+trapYoffset
    screenshot = ImageGrab.grab(bbox=(xc-dx, yc-dy, xc+tBoxWidth-dx, yc+tBoxHeight-dy)) # Coordinates of the snapshot
    #screenshot = ImageGrab.grab(bbox=())
    return screenshot

#imageCapture=take_screenshot()
#im2=imageCapture.resize((canvasWidth, canvasHeight))
#my_image2=ImageTk.PhotoImage(im2)
#rootCanvas.create_image(0, 0, image = my_image2, anchor = NW)
rootCanvas.place(x=canvasX, y=canvasY)
rootCanvas2.place(x=canvasX, y=canvasY+canvasHeight+70)
rootCanvas2.create_rectangle(trapXoffset-tBextend, trapYoffset-tBextend, trapXoffset+tBoxWidth+tBextend, trapYoffset+tBoxHeight+tBextend, outline='red')

line = rootCanvas.create_line(2, 2,canvasWidth, 2,fill='black')
line = rootCanvas.create_line(2, canvasHeight, canvasWidth, canvasHeight,fill='black')
line = rootCanvas.create_line(2, 2, 2, canvasHeight,fill='black')
line = rootCanvas.create_line(canvasWidth, 2, canvasWidth, canvasHeight,fill='black')

onWidth=4; offWidth=4; xPitch=onWidth+offWidth

win1 = Toplevel()
win1.geometry(f"{screenWidth}x{sHeight[1]}+{sWidth[0]}+000") # <- shift window right by sWidth[0] of main monitor
win1.overrideredirect(True)
win1Canvas= Canvas(win1, width=screenWidth, height=sHeight[1])
win1Canvas.pack()
root.focus_set()        # Ensures root window has focus to operate without mouse-click select

# ***************** Optical Trap Parameters ************************
counter = IntVar(value=127)
rowM= IntVar(value=12)      # trap search width
colN= IntVar(value=12)      # trap search height
nTrap=6 # max number of traps
nTarget=6
trapCount=0 # trap count
#trapText = [[None]*5]*7
trapX=[0]*nTrap; trapY=[0]*nTrap# x,y coords of nTraps
trapTextX=[None]*nTrap; trapTextY=[None]*nTrap
for i in range(nTrap):
    trapTextX[i]=IntVar(value=trapX[i])
    trapTextY[i]=IntVar(value=trapY[i])

targetCount=0 # target count
targetX=[0]*nTarget; targetY=[0]*nTarget# x,y coords of nTargets
selectedOT=10  # 10-none selected
splinePts=5
splintX=[[0 for colx in range(splinePts+2)] for rowy in range(nTrap)] # splintX[4][7]
splintY=[[0 for colx in range(splinePts+2)] for rowy in range(nTrap)] # splintY[4][7]
#splintX=[[0]*nTrap]*6; splintY=[[0]*nTrap]*6    # max total spline inflection pts including OT and Target points
nSpline=[0]*nTrap           # spline pts of each trap 2: OT and target, 3: OT, target and a point in between max 6 (not nTrap)
trapText=[[None for cols in range(7)] for rows in range(6)] # trapText[rows][cols]
trapButtons=[[None for cols in range(7)] for rows in range(6)] # trapButtons[rows][cols]
dT=2    # OT trap tangential movement increment toward the next spline point
fieldWidth=1000; fieldHeight=1000   # actual 
pathX=[[0 for colx in range(fieldWidth*fieldHeight)] for rowy in range(nTrap)] # max trap travel pts pathX[rowy][colx]
pathY=[[0 for colx in range(fieldHeight*fieldHeight)] for rowy in range(nTrap)] # max trap travel pts pathX[nTrap][fieldHeight]
pathN=[[0 for colx in range(splinePts+1)] for rowy in range(nTrap)] # path total increment number for each segment of nTraps
pathNtotal=[0]*nTrap
# -------------------- Optical Trap Parameters ----------------------

grayLevel=[0, 0 , 0, 0]
grayLevel[0]=0; grayLevel[1]=85; grayLevel[2]=170; grayLevel[3]=255 
deleteIndex=IntVar(value=0)  # index number to delete
gray1=IntVar(value=grayLevel[1])
gray2=IntVar(value=grayLevel[2]); gray3=IntVar(value=grayLevel[3])
grayStep=IntVar(value=4); grayWidth=IntVar(value=16)
#onColumn4=IntVar(value=16); offColumn4=IntVar(value=8)
colorSelect = 7  # initialize global variable 1(B) 2(G) 4(R) 7(W)
xmin=0; #xmax=canvasWidth
ymin=0; canvasQuad=int(canvasHeight/4)

# ************** Functions & Classes ******************
def store_position(event):  # mouse cursor poistion
    xi, yi = event.x, event.y
    global trapCount #, splintX, splintY
    tempX=int(xi/10)+trapXoffset; tempY=int(yi/10)+trapYoffset
    #print (trapCount)
    if trapCount<nTrap:
        trapX[trapCount]=xi
        trapY[trapCount]=yi
        #print('{}, {}, {}'.format(trapCount, trapX[trapCount], trapY[trapCount])+" set")
        trapTextX[trapCount].set(trapX[trapCount])
        trapTextY[trapCount].set(trapY[trapCount])
        splintX[trapCount][0]=tempX; splintY[trapCount][0]=tempY
        #splintX[0][trapCount]=trapX[trapCount]; splintY[0][trapCount]=trapY[trapCount]
        print ("new ", splintX[0][0])
        if trapCount>0:
            print ("new ", splintX[1][0])
        trapCount+=1
    showTrapList()
    canvas2Update()
    
def erase_Path(sOT):
    eraserColor="gray80"
    #eraserColor="red"
    for i in range(nSpline[sOT]+1):
        rootCanvas2.create_line(splintX[sOT][i], splintY[sOT][i], splintX[sOT][i+1], splintY[sOT][i+1], width=2, fill=eraserColor)
        print("i ",i, " x ", splintX[sOT][i], " ", splintX[sOT][i+1])
    rootCanvas2.create_image(0, 0, image = my_image, anchor = NW)
    print("erased ",nSpline[sOT])

def draw_Path(sOT):
    tColor="black"
    for i in range(nSpline[sOT]+1):
        rootCanvas2.create_line(splintX[sOT][i], splintY[sOT][i], splintX[sOT][i+1], splintY[sOT][i+1], fill=tColor)
    
def addSplinePt(sx, sy):
    index=selectedOT
    if (nSpline[index]<splinePts):
        erase_Path(index)
        nSpline[index] +=1
        # shift target to insert spline point
        splintX[index][nSpline[index]+1]=splintX[index][nSpline[index]]
        splintY[index][nSpline[index]+1]=splintY[index][nSpline[index]]
        #  insert spline coordinate
        splintX[index][nSpline[index]]=sx; splintY[index][nSpline[index]]=sy
        draw_Path(index)
        #time.sleep(1)
    print("sel OT ", index, " nspline ", nSpline[index], " ", splintX[index][selectedOT])
    print("splitX", splintX)
    print("splitY", splintY)
    #canvas2Update()

def store_destination(event):  # mouse cursor poistion
    xi, yi = event.x, event.y
    global targetCount, trapCount
    #print (targetCount)
    if selectedOT==10:   # Execute only if no OT is selected for path modification
        if targetCount<nTarget and targetCount<trapCount:
            targetX[targetCount]=xi
            targetY[targetCount]=yi
            print('{}, {}, {}'.format(targetCount, targetX[targetCount], targetY[targetCount])+" target")
            splintX[targetCount][nSpline[targetCount]+1]=targetX[targetCount]; splintY[targetCount][nSpline[targetCount]+1]=targetY[targetCount]
            splintX[targetCount][nSpline[targetCount]+1]=targetX[targetCount]; splintY[targetCount][nSpline[targetCount]+1]=targetY[targetCount]
            targetCount+=1
        canvas2Update()
    else:   # if an OT is selected, add spline pts
        addSplinePt(xi, yi)
    #canvas2Update()

def delete_position(event):  # mouse cursor position
    xi, yi = event.x, event.y
    global trapCount, targetCount
    if trapCount>0:
        trapCount-=1
        targetCount-=1 # or if targetCount>0: ??
    canvas2Update()
    
def showTrapList():
    #global trapCount, targetCount
    for i in range(7):
        for k in range(6):
            bw=0; bh=0
            trapButtons[k][i].place(width=bw, height=bh)
        
    for i in range(7):
        if (i>0 and i<5):
            bw=30
        else:
            bw=40
        bh=40
        
        for k in range(trapCount):
            trapButtons[k][i].place(width=bw, height=bh)
        print (" Trap ", trapCount)
        
def exitProgram():
        sys.exit(0)
        
def rgb2hex(r,g,b):
    return f'#{r:02x}{g:02x}{b:02x}'

def displayUpdate():
    grayN = counter.get()
    r=int(colorSelect/4)
    g=int(colorSelect/2)-2*r
    b=colorSelect-4*r-2*g
    global hexColor
    hexColor=rgb2hex(r*grayN, g*grayN, b*grayN)
    if grayN<200 or colorSelect==1:
        textColor="white"
    else:
        textColor="black"
    canvas2Update()

def canvas2Update():
    global trapCount    # import global variable trapCount for use
    #print (trapCount,'dd')
    for k in range(trapCount):
        print ("Trap ", k, " X ", splintX[k][0], splintY[k][0])
            
    grayN = counter.get()
    r=int(colorSelect/4)
    g=int(colorSelect/2)-2*r
    b=colorSelect-4*r-2*g
    global hexColor
    hexColor=rgb2hex(r*grayN, g*grayN, b*grayN)
    dx=colN.get(); dy=rowM.get()
    tColor="black"
    eraserColor="gray80"
    #frameColor = rootCanvas["background"]
    
    for i in range(0,trapCount):
        localX=int(trapX[i]); localY=int(trapY[i])
        localXs=int(localX/10); localYs=int(localY/10)
        rootCanvas.create_rectangle(localX-dx, localY-dy, localX+dx, localY+dy, outline=eraserColor, fill=tColor)
        rootCanvas.create_text(localX, localY, text=(i+1), fill='white', font=('arial 12'))
        rootCanvas2.create_rectangle(localXs+trapXoffset, localYs+trapYoffset, localXs+trapXoffset+3, localYs+trapYoffset+3, fill=tColor)
                # ************  replace with splintX[i][0]
        print ("t: ", targetX[i])
        #if targetCount>0:
        if targetX[i]!=0:
            destinX=int(targetX[i]); destinY=int(targetY[i])
            rootCanvas2.create_rectangle(destinX-2, destinY-2, destinX+2, destinY+2, fill=tColor)
            rootCanvas2.create_text(destinX+4, destinY+4, text=(i+1), fill=tColor, font=('arial 12'))
            draw_Path(i)
            #rootCanvas2.create_line(localXs+trapXoffset, localYs+trapYoffset, destinX, destinY, fill=tColor)
    
def updateTarget(): # delete pts/lines from delelteIndex.get() to 6, reduce trapCount and then update by calling canvas2Update
    global trapCount, targetCount
    dx=colN.get(); dy=rowM.get()
    eraser="gray80" #rootCanvas["background"]
    for i in range(deleteIndex.get(), 6): # iterates 1 to 5
        localX=int(trapX[i]); localY=int(trapY[i])
        localXs=int(localX/10); localYs=int(localY/10)
        if (localX!=0 and localY!=0):
            rootCanvas.create_rectangle(localX-dx, localY-dy, localX+dx, localY+dy, outline=eraser,
                                        fill=eraser)
            rootCanvas2.create_rectangle(localXs+trapXoffset, localYs+trapYoffset, localXs+trapXoffset+3, localYs+trapYoffset+3, 
                                         outline= eraser, fill=eraser) # erase OT pt
            destinX=int(targetX[i]); destinY=int(targetY[i])  
            rootCanvas2.create_rectangle(destinX-2, destinY-2, destinX+2, destinY+2, outline=eraser, fill=eraser) # erase OT target
            rootCanvas2.create_text(destinX+4, destinY+4, text=(i+1),fill=eraser, font=('arial 12'))    # erase target label
            rootCanvas2.create_line(localXs+trapXoffset, localYs+trapYoffset, destinX, destinY, fill=eraser)              # erase path
        if i<5:
            trapX[i]=trapX[i+1]; trapY[i]=trapY[i+1] 
            targetX[i]=targetX[i+1]; targetY[i]=targetY[i+1]
            splintX[i][0]=splintX[i+1][0]; splintY[i][0]=splintY[i+1][0]
            splintX[i][nSpline[targetCount]+1]=splintX[i+1][nSpline[targetCount]+1]
            splintY[i][nSpline[targetCount]+1]=splintY[i+1][nSpline[targetCount]+1]
            print (deleteIndex.get(),' x')
            #print(i, str(sWidth[i]) + 'x' + str(sHeight[i]))
        else:
            trapX[5]=0; trapY[5]=0
            splintX[5][0]=0; splintY[5][0]=0
            splintX[5][nSpline[targetCount]+1]=0
            splintY[5][nSpline[targetCount]+1]=0

    trapCount-=1; targetCount-=1
    for i in range(nTrap):
        trapTextX[i].set(trapX[i])
        trapTextY[i].set(trapY[i])
    canvas2Update()

def onClickHeightInc(event=None):
    rowM.set(rowM.get()+1)
    if rowM.get()>64:
        rowM.set(64)
    displayUpdate()
def onClickHeightDec(event=None):
    rowM.set(rowM.get()-1)
    if rowM.get()<1:
        rowM.set(1)
    displayUpdate()
def onClickWidthInc(event=None):
    colN.set(colN.get()+1)
    if colN.get()>128:
        colN.set(128)
    displayUpdate()
def onClickWidthDec(event=None):
    colN.set(colN.get()-1)
    if colN.get()<1:
        colN.set(1)
    displayUpdate()
        
def onClickUp(event=None):
    if counter.get()==0 and rowM.get()>1:
        counter.set(counter.get()+(rowM.get()-1))
    else:
        counter.set(counter.get()+rowM.get())
    if counter.get()>255:
        counter.set(0)
    displayUpdate()
    
def onClickDown(event=None):
    if counter.get()>0 and counter.get()<rowM.get():
        counter.set(counter.get()-(rowM.get()-1))
    else:
        counter.set(counter.get()-rowM.get())
    if counter.get()<0:
        counter.set(255)
    displayUpdate()
    
def enterUpdate(event=None):        # event handle for when gray level is manually entered with <Carriage Return>
    grayLevel[0]=deleteIndex.get()
    grayLevel[1]=gray1.get()
    grayLevel[2]=gray2.get()
    grayLevel[3]=gray3.get()
    displayUpdate()

def deleteTarget(n):
    global trapCount, targetCount
    deleteIndex.set(n)
    print("here", n)
    updateTarget()
    showTrapList()
          
def onColumnInc2(event=None):
    gray2.set(gray2.get()+1)
    if gray2.get()>255:
        gray2.set(255)
    grayLevel[2]=gray2.get()
    displayUpdate()
    
def gray3Inc(event=None):
    gray3.set(gray3.get()+1)
    if gray3.get()>255:
        gray3.set(255)
    grayLevel[3]=gray3.get()
    displayUpdate()

def grayStepInc(event=None):
    grayStep.set(int((grayStep.get())*2))
    if grayStep.get()>64:
        grayStep.set(1)
    displayUpdate()
    
def grayWidthInc(event=None):
    grayWidth.set(int((grayWidth.get())*2))
    if grayWidth.get()>64:
        grayWidth.set(1)
    displayUpdate()
    
def grayWidthDec(event=None):
    grayWidth.set(int((grayWidth.get())/2))
    if grayWidth.get()<1:
        grayWidth.set(64)
    displayUpdate()
    
# ******************* Menu Buttons ******************
#trapText = [[None]*5]*7         # 5 rows, 7 columns
#trapButtons = [[None]*5]*7      # 5 traps (rows) 7 trap vars (columns)
#splintX=[[0 for colx in range(6)] for rowy in range(nTrap)] # mButtons[rows][cols]
#trapText=[[None for cols in range(7)] for rows in range(6)] # mButtons[rows][cols]
#trapButtons=[[None for cols in range(7)] for rows in range(6)] # mButtons[rows][cols]
def deselect_all():
    bColor="gray80"
    for k in range (trapCount):
        trapButtons[k][0].config(bg=bColor)
        
def real_action(k, m):
    global selectedOT
    deselect_all()
    print ("action ", k, m, " OT ", selectedOT)
    if selectedOT==m:
        selectedOT=10    # 10 = none selected
    else:
        selectedOT=m
    if k==6:
        if nSpline[selectedOT]>0:
            erase_Path(selectedOT)
            splintX[selectedOT][1]=splintX[selectedOT][nSpline[selectedOT]+1]
            splintY[selectedOT][1]=splintY[selectedOT][nSpline[selectedOT]+1]
            nSpline[selectedOT]=0

#selectColor="palegreen1"
def action(i,k):
    global selectedOT
    selectColor="palegreen1"
    real_action(i,k)
    if selectedOT==k:
        trapButtons[k][0].config(bg=selectColor)
        print ("new selectedOT: ", selectedOT)
        
textL = [[None for cols in range(4)] for rows in range(3)] 

    
class MenuButtons:
    hexColor="white"
    global trapText, trapButtons
    x1=75; y1=canvasY+canvasHeight+120; dx=60; dy=60; 
    for i in range(7):
        for k in range(6):
            trapText[k][i]=StringVar()
            if i==0:
                tText='T'+str(k+1)
                trapText[k][i].set(tText)
            else:
                xx=1
                trapText[k][i].set('%d' % (i))
            if i==5:
                xx=1
                trapText[k][i].set('D1')
            if i==6:
                xx=1
                trapText[k][i].set('Clr')
            trapButtons[k][i] = Button(root,textvariable = trapText[k][i], activebackground='gray64', bg='gray80', fg='black', 
                                       command = lambda i=i, k=k: action(i, k))
            if i==0:
                trapButtons[k][i].place(x=x1+dx*i-30, y=50+y1+dy*k,  width=0, height=0)
            else:
                trapButtons[k][i].place(x=x1+dx*i, y=50+y1+dy*k,  width=0, height=0)
    def __init__(self, master):        # __init__(className, variable)      
        self.keyIndex0 = Label(root, text="Press: ▲ Up/▼ Down (Height), ◄ L / R ►(Width), Esc (Quit)", justify="left",font=('Arial', 10))
        self.selectNum = Label(root, text="Select", justify="center", font=('Arial', 10))
        self.trapNumSelect = Label(root, text="Trap", justify="center", font=('Arial', 10))
        self.pathPt1 = Label(root, text="P1", justify="center", font=('Arial', 10))
        self.pathPt2 = Label(root, text="P2", justify="center", font=('Arial', 10))
        self.pathPt3 = Label(root, text="P3", justify="center", font=('Arial', 10))
        self.pathPt4 = Label(root, text="P4", justify="center", font=('Arial', 10))
        self.target = Label(root, text="Clear", justify="center", font=('Arial', 10))
            
        #******************** Trap Path Info *********************
        dx=50; dy=60; x1=75; y1=canvasY+canvasHeight+120

        print(trapText)
        # ******************* Placement ************************
        dy1=60; dy2=60
        x0=380; y0=270
        x2=canvasX+int(canvasWidth/2); y2=canvasY+int(canvasHeight/2)
        self.keyIndex0.place(x=x1-40, y=50)
        self.selectNum.place(x=x1-40, y=y1-30)
        self.trapNumSelect.place(x=x1-30, y=y1)
        self.pathPt1.place(x=x1+dx, y=y1)
        self.pathPt2.place(x=x1+dx*2, y=y1)
        self.pathPt3.place(x=x1+dx*3, y=y1)
        self.pathPt4.place(x=x1+dx*4, y=y1)
        self.target.place(x=x1+dx*5, y=y1)
                  
        master.bind('<Right>', lambda event: onClickWidthInc())
        master.bind('<Left>', lambda event: onClickWidthDec())
        master.bind('<Up>', lambda event: onClickHeightInc())
        master.bind('<Down>', lambda event: onClickHeightDec())
        master.bind('<Escape>', lambda event: exitProgram())
        master.bind('<Return>', lambda event: enterUpdate())
        
        displayUpdate()    
trapNum=[None]*6; trapText=[None]*6
oTrapX=[None]*6; oTrapY=[None]*6
oTarget=[None]*6; deleteButton=[None]*6

def arrayClick(num):    # needed to pass correct num to deleteTarget(i)
    return lambda: deleteTarget(num)

def clear_Trap():
    tColor='gray80'
    rootCanvas2.create_rectangle(trapXoffset-tBextend, trapYoffset-tBextend, trapXoffset+tBoxWidth+tBextend, trapYoffset+tBoxHeight+tBextend, outline=tColor)
    for i in range(0,trapCount):
        localX=int(trapX[i]); localY=int(trapY[i])
        localXs=int(localX/10); localYs=int(localY/10)
        rootCanvas2.create_rectangle(localXs+trapXoffset, localYs+trapYoffset, localXs+trapXoffset+3,
                                     localYs+trapYoffset+3, outline=tColor, fill=tColor)
        if targetX[i]!=0:
            erase_Path(i)
    #time.sleep(0.1)
        
def update_Box(deltaX, deltaY):
    global trapXoffset, trapYoffset
    trapXoffset+=deltaX
    trapYoffset+=deltaY
    for i in range(trapCount):
        splintX[i][0]=splintX[i][0]+deltaX
        splintY[i][0]=splintY[i][0]+deltaY
        pX=splintX[i][0]; pY=splintY[i][0]
        rootCanvas2.create_rectangle(pX, pY, pX+3, pY+3, fill='black')
        if splintX[i][1]!=0:
            draw_Path(i)
    rootCanvas2.create_rectangle(trapXoffset-tBextend, trapYoffset-tBextend, trapXoffset+tBoxWidth+tBextend, trapYoffset+tBoxHeight+tBextend, outline='red')
    #rootCanvas.create_image(0, 0, image = my_image2, anchor = NW)
    #rootCanvas2.create_image(0, 0, image = my_image, anchor = NW)
    
#my_image2=load_Path()
#rootCanvas.create_image(0, 0, image = my_image2, anchor = NW)
def update_Canvas2():
    my_image2=load_Path()
    rootCanvas.create_image(0, 0, image = my_image2, anchor = NW)
    
def begin_Search():
   # global pathN # 0 to pathN pts to be generated for search
    dy=rowM.get(); dx=colN.get()
    for k in range(targetCount):
        x0=trapX[k]-dx; y0=trapY[k]-dy
        #print ("x0", x0, y0)
        for j in range(2*dy+1):
            for i in range(2*dx+3):
                pathX[k][j*dy*2+i]=x0+i # define coordinates of search rectangle for each target 
                pathY[k][j*dy*2+i]=y0+j
                #print("path", j, pathX[k][j*dx+i], pathY[k][j*dx+i])
        pathNtotal[k]=4*dy*dx # total number of paths to be tabulated
        for i in range(pathNtotal[k]):
            for p in range(targetCount):
                rootCanvas.create_rectangle(pathX[p][i], pathY[p][i], pathX[p][i]+1, pathY[p][i]+1, outline='red', fill='red')
                pathXs=pathX[p][i]/10; pathYs=pathY[p][i]/10
                rootCanvas2.create_rectangle(pathXs+trapXoffset, pathYs+trapYoffset, pathXs+trapXoffset+3, pathYs+trapYoffset+3, outline='red', fill='red')
        splintX[k][0]=pathXs; splintY[k][0]=pathYs  # reassign target location to last search coords


def move_to_Path():
    dx=colN.get(); dy=rowM.get()
    for k in range(targetCount):
        x0=trapX[k]-dx; y0=trapY[k]-dy
        print ("x0", x0, y0)
        for j in range(2*dy+1):
            for i in range(2*dx+3):
                pathX[k][j*dy*2+i]=x0+i # define coordinates of search rectangle for each target 
                pathY[k][j*dy*2+i]=y0+j
                print("path", j, pathX[k][j*dx+i], pathY[k][j*dx+i])
        pathNtotal[k]=4*dy*dx # total number of paths to be tabulated
        for i in range(pathNtotal[k]):
            for p in range(targetCount):
                rootCanvas.create_rectangle(pathX[p][i], pathY[p][i], pathX[p][i]+1, pathY[p][i]+1, outline='red', fill='red')
    dx=colN.get(); dy=rowM.get()
    tColor="black"
    eraserColor="gray80"
    #frameColor = rootCanvas["background"]
    # ************************************************************************
    dx=colN.get(); dy=rowM.get()
    eraser="gray80" #rootCanvas["background"]
    for i in range(0,trapCount):
        localX=int(trapX[i]); localY=int(trapY[i])
        localXs=int(localX/10); localYs=int(localY/10)
        rootCanvas.create_rectangle(localX-dx, localY-dy, localX+dx, localY+dy, outline=eraserColor, fill=tColor)
        rootCanvas.create_text(localX, localY, text=(i+1), fill='white', font=('arial 12'))
        rootCanvas2.create_rectangle(localXs+trapXoffset, localYs+trapYoffset, localXs+trapXoffset+3, localYs+trapYoffset+3, fill=tColor)
                # ************  replace with splintX[i][0]
        print ("t: ", targetX[i])
        #if targetCount>0:
        if targetX[i]!=0:
            destinX=int(targetX[i]); destinY=int(targetY[i])
            rootCanvas2.create_rectangle(destinX-2, destinY-2, destinX+2, destinY+2, fill=tColor)
            rootCanvas2.create_text(destinX+4, destinY+4, text=(i+1), fill=tColor, font=('arial 12'))
            draw_Path(i)
            
def generate_CGH():
    n=0
    # generate CGH for path coords of all targets
            
    
def shift_Left():
    if trapXoffset>0:
        dx=-10
        clear_Trap()
        load_Path2()
        update_Box(dx, 0)
    update_Canvas2()

def shift_Right():
    if trapXoffset<int(canvasWidth*0.9):
        dx=10
        clear_Trap()
        load_Path2()
        update_Box(dx, 0)
    update_Canvas2()

def shift_Up():
    if trapYoffset>0:
        dy=-10
        clear_Trap()
        load_Path2()
        update_Box(0, dy)
    update_Canvas2()
        
def shift_Down():
    if trapYoffset<int(canvasHeight*0.9):
        dy=10
        clear_Trap()
        load_Path2()
        update_Box(0, dy)
    update_Canvas2()

class ZoneButtons:
    hexColor="white"
    def __init__(self, master):        # __init__(className, variable)  
        self.trapNum = Label(root, text="Trap", justify="center", font=('Arial', 10))
        self.trapX = Label(root, text="X", justify="center", font=('Arial', 10))
        self.trapY = Label(root, text="Y", justify="center", font=('Arial', 10))
        self.target = Label(root, text="Target Pos.", justify="center", font=('Arial', 10))
        self.deleteTrap = Label(root, text="Delete", justify="center", font=('Arial', 10))
        
        # ************** Top trap list ********************
        dx=210; dx0=280; dx2=60; dx3=90; dx4=85; dy=50; dy2=screenQuad
        x0=300; dx5=70; y0=20; y1=canvasY-50
        for i in range(6):
            trapText[i]=str(i+1)
            trapNum[i]=Label(root, text=trapText[i], justify="center", font=('Arial', 10))
            trapNum[i].place(x=x0-dx0, y=y1+70+dy*i, width=50, height=30)
            oTrapX[i]=Label(root, textvariable=trapTextX[i], justify="center", font=('Arial', 9))
            oTrapY[i]=Label(root, textvariable=trapTextY[i], justify="center", font=('Arial', 9))
            #oTarget[i]=Label(root, textvariable="D1", justify="center", font=('Arial', 9))
            oTarget[i]=Label(root, text="D1", justify="center", font=('Arial', 9))
            deleteButton[i]=Button(root,text="x",activebackground='gray64', bg='gray80', 
                                   fg='black', command=arrayClick(i), font=('Arial', 12))
            deleteButton[i].pack()
            oTrapX[i].place(x=x0-dx, y=y1+70+dy*i, width=50, height=30)
            oTrapY[i].place(x=x0-dx+dx2, y=y1+70+dy*i, width=50, height=30)
            oTarget[i].place(x=x0-dx3, y=y1+70+dy*i, width=50, height=30)
            deleteButton[i].place(x=x0+dx5, y=y1+70+dy*i, width=30, height=30)
        
        self.keyUpHeight = Label(root, text="▲", height=1, justify="center")
        self.keyDownHeight = Label(root, text="▼", height=1, justify="center")
        self.searchX = Label(root, text="Search Width:", justify="center", font=('Arial', 10))
        self.searchY = Label(root, text="Search Height:", justify="center", font=('Arial', 10))
        self.keyUpWidth = Label(root, text="►", height=1, justify="right", font=('Arial', 9))
        self.keyDownWidth = Label(root, text="◄", height=1, justify="right", font=('Arial', 9)) 
        self.searchWidth = Label(root, textvariable=colN, justify="center", font=('Arial', 10))
        self.searchHeight = Label(root, textvariable=rowM, justify="center", font=('Arial', 10))
        
        self.searchParticle = Label(root, text="Initiate Trapping", justify="center", font=('Arial', 10))
        self.beginSearch = Button(root,text="Begin",activebackground='gray64', bg='gray80', 
                                   fg='black', command=begin_Search, font=('Arial', 10))
        self.moveParticle = Label(root, text="Move to Target Location", justify="center", font=('Arial', 10))
        self.moveToTarget = Button(root,text="Move",activebackground='gray64', bg='gray80', 
                                   fg='black', command=move_to_Path, font=('Arial', 10))
        
        self.trapPosition = Label(root, text="Trap Aperture Position:", justify="center", font=('Arial', 10))
        self.trapLeft = Button(root,text="◄",activebackground='gray64', bg='gray80', 
                                   fg='black', command=shift_Left, font=('Arial', 9))
        self.trapRight = Button(root,text="►",activebackground='gray64', bg='gray80', 
                                   fg='black', command=shift_Right, font=('Arial', 9))
        self.trapUp = Button(root,text="▲",activebackground='gray64', bg='gray80', 
                                   fg='black', command=shift_Up, font=('Arial', 9))
        self.trapDown = Button(root,text="▼",activebackground='gray64', bg='gray80', 
                                   fg='black', command=shift_Down, font=('Arial', 9))
        #self.searchWidth = Label(root, textvariable=colN, justify="center", font=('Arial', 10))
        #self.searchHeight = Label(root, textvariable=rowM, justify="center", font=('Arial', 10))
        
        # ***************************** Display **************************
        self.trapNum.place(x=x0-dx0, y=y1+30, width=60, height=30)
        self.trapX.place(x=x0-dx, y=y1+30, width=50, height=30)
        self.trapY.place(x=x0-dx+dx2, y=y1+30, width=50, height=30)
        self.target.place(x=x0-dx3-25, y=y1+30, width=160, height=30)
        self.deleteTrap.place(x=x0+dx5-35, y=y1+30, width=100, height=30)
        self.searchX.place(x=x0-dx-dx4+30, y=y1+10+dy*7, height=30)
        self.searchY.place(x=x0-dx-dx4+30, y=y1+10+dy*8, height=30)
        self.searchWidth.place(x=x0-dx4+40, y=y1+10+dy*7, height=30)
        self.searchHeight.place(x=x0-dx4+40, y=y1+10+dy*8, height=30)
        
        self.keyDownHeight.place(x=x0-dx4, y=y1+10+dy*8, height=30)
        self.keyUpHeight.place(x=x0-dx4+80, y=y1+10+dy*8, height=30)
        self.keyDownWidth.place(x=x0-dx4, y=y1+10+dy*7, height=30)
        self.keyUpWidth.place(x=x0-dx4+80, y=y1+10+dy*7, height=30)
        
        self.searchParticle.place(x=canvasX+50, y=canvasY-50, height=30)
        self.beginSearch.place(x=canvasX+225, y=canvasY-50, height=30)
        self.moveParticle.place(x=canvasX+350, y=canvasY-50, height=30)
        self.moveToTarget.place(x=canvasX+625, y=canvasY-50, height=30)
        
        self.trapPosition.place(x=canvasX+50, y=canvasY+canvasHeight+25, height=30)
        self.trapLeft.place(x=canvasX+300, y=canvasY+canvasHeight+25, height=30)
        self.trapRight.place(x=canvasX+400, y=canvasY+canvasHeight+25, height=30)
        self.trapUp.place(x=canvasX+350, y=canvasY+canvasHeight+10, height=25)
        self.trapDown.place(x=canvasX+350, y=canvasY+canvasHeight+40, height=25)
        
        
    def rStart(iself):  #alternate: def rStart(iself, _event=None):   # _event=None to prevent warnings
        global colorSelect
        colorSelect=4
        displayUpdate()
    
# ************** Functions End ******************
        
displayUpdate()
rootButtons = MenuButtons(root)
rootZoneButtons = ZoneButtons(root)
rootCanvas.bind('<Button-1>', store_position)    # store current cursor position within the rootCanvas
rootCanvas2.bind('<Button-1>', store_destination)    # store current cursor position within the rootCanvas
#rootCanvas.bind('<Button-2>', delete_position)   # delete the last cursor position within the rootCanvas
#rootCanvas.bind('<Button-3>', delete_position)   # delete the last cursor position within the rootCanvas in case scroll click is available
load_Path()
root.mainloop()