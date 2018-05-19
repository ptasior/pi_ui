import pigpio
import time

KEY_UP_PIN          = 6
KEY_DOWN_PIN        = 19
KEY_LEFT_PIN        = 5
KEY_RIGHT_PIN       = 26
KEY_PRESS_PIN       = 13
KEY1_PIN            = 21
KEY2_PIN            = 20
KEY3_PIN            = 16

KEYS = {
        KEY_UP_PIN: 'UP',
        KEY_DOWN_PIN: 'DOWN',
        KEY_LEFT_PIN: 'LEFT',
        KEY_RIGHT_PIN: 'RIGHT',
        KEY_PRESS_PIN: 'PRESS',
        KEY1_PIN: 'KEY1',
        KEY2_PIN: 'KEY2',
        KEY3_PIN: 'KEY3'
    }


class Keys:
    def __init__(self, onDown, onUp=None):
        self.onDown = onDown
        self.onUp = onUp

        self.cb = []

        self.pi = pigpio.pi()

        if not self.pi.connected:
           raise Exception("Can not connect to pigpio")

        for k in KEYS:
            self.cb.append(self.pi.callback(k, pigpio.EITHER_EDGE, self.callback))

        # c.cancel()
        # pi.stop()


    def callback(self, gpio, level, tick):
        if level: self.onDown(gpio)
        else:     self.onUp(gpio)


if __name__ == '__main__':
    def down(key):
        print('Pressed: '+KEYS[key])

    def up(key):
        print('Released: '+KEYS[key])

    keys = Keys(down, up)
    time.sleep(60)

