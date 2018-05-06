import os
import traceback
import importlib.util


class Menu(object):
    def __init__(self):
        self.read_dir()

    def read_dir(self):
        self.menu = self.read_recursive('menu_data')
        print(str(self.menu))

    def read_recursive(self, path):
        ret = {}
        for f in os.listdir(path):
            f_path = os.path.join(path, f)
            if f.startswith('__'): continue

            if(os.path.isdir(f_path)):
                ret[f] = self.read_recursive(f_path)
            else:
                if f.endswith('.py'):
                    ret[f[:-3]] = 'script'

        return ret

    def execute(self, path):
        spec = importlib.util.spec_from_file_location("script", "menu_data/"+path+'.py')
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
            mod.execute()
        except Exception as e:
            # traceback.print_tb(e.__traceback__)
            print(traceback.format_exc())


