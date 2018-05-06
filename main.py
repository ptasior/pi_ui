#!/usr/bin/python3

from menu import Menu
from lcd import MenuLcd
from keys import Keys
import shared_data

shared_data.objects['menu'] = Menu()
# m.execute('lcd/on.py')
shared_data.objects['menuLcd'] = MenuLcd()
shared_data.objects['keys'] = Keys()

print('Initialised, starting main loop')
while True:
    shared_data.performMainLoop()

