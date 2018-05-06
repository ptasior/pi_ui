import RPi.GPIO as GPIO
import time

KEY_UP_PIN          = 6
KEY_DOWN_PIN        = 19
KEY_LEFT_PIN        = 5
KEY_RIGHT_PIN       = 26
KEY_PRESS_PIN       = 13
KEY1_PIN            = 21
KEY2_PIN            = 20
KEY3_PIN            = 16

REPEAT_EVERY = 0.3

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
    def __init__(self, onDown, onRepeat=None, onUp=None):
        self.onDown = onDown
        self.onRepeat = onRepeat
        self.onUp = onUp

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(KEY_UP_PIN, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(KEY_DOWN_PIN, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(KEY_LEFT_PIN, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(KEY_RIGHT_PIN, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(KEY_PRESS_PIN, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(KEY1_PIN, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(KEY2_PIN, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(KEY3_PIN, GPIO.IN, GPIO.PUD_UP)

        self.state = {}
        for k, v in KEYS.items():
            self.state[k] = [False, False, True, None]



    def start(self):
        while True:
            self.poll()



    def poll(self):
        for k, v in KEYS.items():
            if GPIO.input(k) == 0:
                self.state[k][0] = True
                self.down(k)
            else:
                self.state[k][0] = False
        self.up()



    def down(self, key):
        if not self.state[key][1]:
            self.onDown(KEYS[key])
            self.state[key] = [True, True, False, time.time()]



    def up(self):
        for k,v in KEYS.items():
            if not self.state[k][0] and not self.state[k][2]:
                if self.onUp: self.onUp(v)
                self.state[k] = [False, False, True, None]
            elif self.state[k][0] and self.state[k][3] < time.time()-REPEAT_EVERY:
                if self.onRepeat: self.onRepeat(v)
                self.state[k][3] = time.time()



if __name__ == '__main__':
    def down(key):
        print('Pressed: '+key)

    def repeated(key):
        print('Repeated: '+key)

    def up(key):
        print('Released: '+key)

    keys = Keys(down, repeated, up)
    keys.start()

