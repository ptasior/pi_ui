data = {}
threads = {}
objects = {}

def app(path):
    return data[path]

def addThread(name, handler):
    threads[name] = handler

def performMainLoop():
    for i in threads:
        threads[i]()

