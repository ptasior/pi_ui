import bottle
import os
from threading import Thread
import shared_data
 
def methodroute(route, method='GET'):
    def decorator(f):
        f.route = route
        f.method = method
        return f
    return decorator


class WebServer(object):
    def __init__(self):
        base_path = os.path.abspath(os.path.dirname(__file__))
        templates_path = os.path.join(base_path, 'templates')
        bottle.TEMPLATE_PATH.insert(0, templates_path)

        self.runThread()


    def runThread(self):
        self.thread = Thread(target = self.run)
        self.thread.setDaemon(True)
        self.thread.start()


    def _routeClass(self):
        for kw in dir(self):
            attr = getattr(self, kw)
            if hasattr(attr, 'route'):
                if hasattr(attr, 'method'):
                    bottle.route(attr.route, method=attr.method)(attr)
                else:
                    bottle.route(attr.route)(attr)


    def run(self):
        self._routeClass()
        bottle.run(host='0.0.0.0', port=8080, debug=True)


    @methodroute('/')
    def index(self):
        bottle.redirect('/menu')


    @methodroute('/menu')
    def menu(self):
        return bottle.template('menu',
                    items=shared_data.objects['menu'].menu
                )

    @methodroute('/execute/<path>')
    def execute(self, path):
        print(path)
        shared_data.objects['menu'].execute(path.replace('.','/'))
        bottle.redirect('/menu')


    @methodroute('/playlist')
    def playlist(self):
        return bottle.template('playlist',
                    items=shared_data.data['playlist']
                )

    @methodroute('/setup')
    def setup(self):
        return bottle.template('setup',
                    data=shared_data.data
                )

    @methodroute('/setupSave', 'POST')
    def setupSave(self):
        artist = bottle.request.forms.get('artist')
        if 'lastFm' not in shared_data.data:
            shared_data.data['lastFm'] = {}

        try: print(shared_data.data['lastFm']['artist'])
        except: pass
        shared_data.data['lastFm']['artist'] = artist

        bottle.redirect('/setup')

