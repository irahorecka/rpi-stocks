from . import lcd, led
from .base import BaseRPi


class RPi_3BP(BaseRPi):
    pi_model = "3B+"

    def __init__(self):
        super().__init__()
        self.gpio_name_pair = {
            4: "",
            5: "",
            6: "",
            12: "",
            13: "",
            16: "",
            17: "",
            18: "",
            19: "",
            20: "",
            21: "",
            22: "",
            23: "",
            24: "",
            25: "",
            26: "",
            27: "",
        }

    @staticmethod
    def lcd_display(*args, **kwargs):
        """ Display information on 16x2 LCD display. """
        lcd.display(*args, **kwargs)

    @staticmethod
    def lcd_display_datetime(*args, **kwargs):
        """ Display datetime on 16x2 LCD display. """
        lcd.display_datetime(*args, **kwargs)

    @staticmethod
    def led_on(*args, **kwargs):
        led.on(*args, **kwargs)

    @staticmethod
    def led_off(*args, **kwargs):
        led.off(*args, **kwargs)

    def cleanup(self):
        for channel in self.gpio_name_pair.keys():
            self.gpio_cleanup(channel)
