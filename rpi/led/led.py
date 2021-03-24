import platform
import sys

# for development purposes (I always use MacOS)
if platform.system() == "Darwin":
    import fake_rpi

    sys.modules["RPi"] = fake_rpi.RPi
    sys.modules["RPi.GPIO"] = fake_rpi.RPi.GPIO
import RPi.GPIO as GPIO


def on(channel):
    GPIO.setup(channel, GPIO.OUT)
    GPIO.output(channel, True)


def off(channel):
    GPIO.output(channel, False)
