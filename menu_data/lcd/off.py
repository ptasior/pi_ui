import shared_data

def execute():
    print("LCD off")
    shared_data.objects['menuLcd'].lcd.turnOff();

