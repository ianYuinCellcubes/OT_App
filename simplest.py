import miicam
from tkinter import *   # Button, Frame, Tk
from PIL import ImageTk, Image # pip install pillow
from screeninfo import get_monitors
from threading import *
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


def threading():
    t1 = Thread(target=App)
    t1.start()

class App:
    def __init__(self):
        self.hcam = None
        self.buf = None
        self.total = 0
        root = Tk()
        x = sWidth[0] - 1400
        y = 400
        imgWidth = 0
        imgHeight = 0
        canvasWidth = 400;
        canvasHeight = 250
        self.canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
        canvas.pack()

        pData = None

# the vast majority of callbacks come from miicam.dll/so/dylib internal threads
    @staticmethod
    def cameraCallback(nEvent, ctx):
        if nEvent == miicam.MIICAM_EVENT_IMAGE:
            ctx.CameraCallback(nEvent)

    def CameraCallback(self, nEvent):
        if nEvent == miicam.MIICAM_EVENT_IMAGE:
            try:
                self.hcam.PullImageV3(self.buf, 0, 24, 0, None)
                self.total += 1
                print('pull image ok, total = {}'.format(self.total))
                width, height = self.hcam.get_Size()
                pData = bytes(miicam.TDIBWIDTHBYTES(width * 24) * height)
                if pData is not None:
                    img = Image.frombytes("RGB", (width, height), pData, "raw")
                    self.canvas.create_image(10,10, anchor=NW, image = img)
            except miicam.HRESULTException as ex:
                print('pull image failed, hr=0x{:x}'.format(ex.hr & 0xffffffff))
        else:
            print('event callback: {}'.format(nEvent))

    def run(self):
        a = miicam.Miicam.EnumV2()
        if len(a) > 0:
            print('{}: flag = {:#x}, preview = {}, still = {}'.format(a[0].displayname, a[0].model.flag, a[0].model.preview, a[0].model.still))
            for r in a[0].model.res:
                print('\t = [{} x {}]'.format(r.width, r.height))
            self.hcam = miicam.Miicam.Open(a[0].id)
            if self.hcam:
                try:
                    width, height = self.hcam.get_Size()
                    bufsize = miicam.TDIBWIDTHBYTES(width * 24) * height
                    print('image size: {} x {}, bufsize = {}'.format(width, height, bufsize))
                    self.buf = bytes(bufsize)
                    if self.buf:
                        try:
                            self.hcam.StartPullModeWithCallback(self.cameraCallback, self)
                        except miicam.HRESULTException as ex:
                            print('failed to start camera, hr=0x{:x}'.format(ex.hr & 0xffffffff))

                    input('press ENTER to exit')
                finally:
                    self.hcam.Close()
                    self.hcam = None
                    self.buf = None
            else:
                print('failed to open camera')
        else:
            print('no camera found')

if __name__ == '__main__':
    app = App()
    app.run()
