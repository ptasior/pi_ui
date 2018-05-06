import shared_data

def execute():
    if shared_data.objects['menuLcd'].lcd.isTurnedOn():
        print("LCD off")
        shared_data.objects['menuLcd'].lcd.turnOff()
    else:
        print("LCD on")
        shared_data.objects['menuLcd'].lcd.turnOn()

