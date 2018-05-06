import traceback
try:
    import drivers.keys
    import drivers.ir
    isSupported = True
except:
    print('Cannot load Keys driver. Missing RPiGPIO or patform not supported')
    print(traceback.format_exc())
    isSupported = False

import shared_data

class Keys(object):
    def __init__(self):
        if not isSupported: return

        shared_data.addThread('keys', self.loop)
        self.keys = drivers.keys.Keys(self.onPress)
        self.ir = drivers.ir.IR()
        self.ir.initListen(self.onIR)

    def loop(self):
        self.keys.poll()
        self.ir.poll()

    def onPress(self, key):
        print("pressed: "+key)
        if key == 'UP':
            shared_data.objects['menuLcd'].up()
        elif key == 'DOWN':
            shared_data.objects['menuLcd'].down()
        elif key == 'RIGHT':
            shared_data.objects['menuLcd'].go()
        elif key == 'LEFT':
            shared_data.objects['menuLcd'].back()
        elif key == 'KEY1':
            shared_data.objects['menu'].execute('lcd/toggle')


    def onIR(self, key):
        print("IR pressed: "+key)

