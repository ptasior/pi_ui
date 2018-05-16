#!/usr/bin/python3

from menu import Menu
from lcd import MenuLcd
from keys import Keys
from player import Player
from web_server import WebServer
from youtube_linker import YoutubeLinker
import shared_data

shared_data.objects['menu'] = Menu()
# m.execute('lcd/on.py')
shared_data.objects['menuLcd'] = MenuLcd()
shared_data.objects['keys'] = Keys()
shared_data.objects['player'] = Player()
shared_data.objects['webServer'] = WebServer()
shared_data.objects['youtubeLinker'] = YoutubeLinker()

print('Initialised, starting main loop')
while True:
    shared_data.performMainLoop()

