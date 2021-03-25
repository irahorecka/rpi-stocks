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
    def lcd_display(msg1, msg2, duration=1):
        """ Display information on 16x2 LCD display. """
        lcd.display(msg1, msg2, duration)

    @staticmethod
    def lcd_display_datetime(timezone):
        """ Display datetime on 16x2 LCD display. """
        lcd.display_datetime(timezone)

    @staticmethod
    def led_on(channel):
        """ Turn LED at GPIO channel ON. """
        led.on(channel)

    @staticmethod
    def led_off(channel):
        """ Turn LED at GPIO channel OFF. """
        led.off(channel)

    def setup(self, channel, mode="out"):
        """ Setup GPIO channel for input or output. """
        self.gpio_setup(channel, mode)

    def cleanup(self):
        """ Cleanup all GPIO channels. """
        for channel in self.gpio_name_pair.keys():
            self.gpio_cleanup(channel)
