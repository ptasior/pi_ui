import shared_data

def execute():
    print("LCD on")
    shared_data.objects['menuLcd'].lcd.turnOn();


