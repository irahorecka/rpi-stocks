import platform
import sys

# for development purposes (I always use MacOS)
if platform.system() == "Darwin":
    import fake_rpi

    sys.modules["RPi"] = fake_rpi.RPi
    sys.modules["RPi.GPIO"] = fake_rpi.RPi.GPIO
import RPi.GPIO as GPIO


class BaseRPi:
    """ Base class to be inherited by children RPi models. """

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        # To be inherited and modified by children class
        self.gpio_name_pair = {}

    @staticmethod
    def gpio_setup(channel, mode):
        """ Provide class interface for GPIO.setup """
        if mode == "in":
            GPIO.setup(channel, GPIO.IN)
        elif mode == "out":
            GPIO.setup(channel, GPIO.OUT)
        else:
            raise ValueError(f"{mode} is not an acceptable keyword argument.")

    @staticmethod
    def gpio_cleanup(channel):
        """ Provide class interface for GPIO.cleanup """
        GPIO.cleanup(channel)
