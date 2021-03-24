from .lcd import LCD

lcd = LCD()


def display(*args, **kwargs):
    lcd.display(*args, **kwargs)


def display_datetime(*args, **kwargs):
    lcd.display_datetime(*args, **kwargs)
