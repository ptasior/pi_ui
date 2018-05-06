import traceback
try:
    import drivers.lcd
    isSupported = True
except:
    print('Cannot load LCD driver. Missing RPiGPIO or patform not supported')
    print(traceback.format_exc())
    isSupported = False

if isSupported:
    from PIL import Image
    from PIL import ImageDraw
    from PIL import ImageFont
    from PIL import ImageColor

import shared_data


class MenuLcd(object):
    def __init__(self):
        if not isSupported: return

        self.menu = shared_data.objects['menu']
        self.menuPos = []
        self.currentBranch = None
        self.cursor = 0
        self.prevItems = 0

        self.lcd = drivers.lcd.LCD()
        self.lcd.init()

        self.updateBranch()

        self.drawList()
        self.drawCursor()

        # self.lcd.clear()



    def drawCursor(self):
        image = Image.new("RGB", (128, 128), "BLACK")
        draw = ImageDraw.Draw(image)
        draw.rectangle([(2, self.cursor*14+4),(6,self.cursor*14+8)],fill = "WHITE")

        self.lcd.drawRect(image, 0,0,10,128)


    def updateBranch(self):
        self.currentBranch = self.menu.menu

        for p in self.menuPos:
            self.currentBranch = self.currentBranch[p]


    def drawList(self):
        itemsCount = len(self.currentBranch.keys())

        imgWidth = max(itemsCount, self.prevItems)*14
        image = Image.new("RGB", (128, imgWidth), "BLACK")
        draw = ImageDraw.Draw(image)

        cnt = 0
        for i in sorted(self.currentBranch.keys()):
            color = 'WHITE' if self.currentBranch[i] == 'script' else 'SILVER'
            draw.text((10, cnt*14), i, fill = color)
            cnt = cnt +1

        self.prevItems = itemsCount
        self.lcd.drawRect(image,0,0,128,imgWidth)


    def up(self):
        self.cursor = (self.cursor - 1) % len(self.currentBranch)
        self.drawCursor()


    def down(self):
        self.cursor = (self.cursor + 1) % len(self.currentBranch)
        self.drawCursor()


    def go(self):
        it = sorted(self.currentBranch.keys())[self.cursor]
        if self.currentBranch[it] == 'script':
            shared_data.objects['menu'].execute('/'.join(self.menuPos+[it]))
            return

        self.menuPos.append(it)

        self.updateBranch()
        self.drawList()

        self.cursor = 0
        self.drawCursor()


    def back(self):
        if not len(self.menuPos):
            return

        self.menuPos.pop()

        self.updateBranch()
        self.drawList()

        self.cursor = 0
        self.drawCursor()

