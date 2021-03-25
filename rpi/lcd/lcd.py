import datetime
import platform
import sys
import time
from pytz import timezone

# for development purposes (I always use MacOS)
if platform.system() == "Darwin":
    import fake_rpi

    sys.modules["smbus"] = fake_rpi.smbus
import smbus


class LCD:
    """
    A class to handle 16x2 I2C LCD display
    sequences upon instantiation.
    """

    # Define some device parameters
    I2C_ADDR = 0x27  # I2C device address
    LCD_WIDTH = 16  # Maximum characters per line
    # Define some device constants
    LCD_CHR = 1  # Mode - Sending data
    LCD_CMD = 0  # Mode - Sending command
    LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
    LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line
    LCD_LINE_3 = 0x94  # LCD RAM address for the 3rd line
    LCD_LINE_4 = 0xD4  # LCD RAM address for the 4th line
    LCD_BACKLIGHT = 0x08  # On
    # LCD_BACKLIGHT= 0x00  # Off
    ENABLE = 0b00000100  # Enable bit
    # Timing constants
    E_PULSE = 0.0005
    E_DELAY = 0.0005
    # Open I2C interface
    bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

    def __init__(self):
        """ Initialise display. """
        self._lcd_byte(0x33, self.LCD_CMD)  # 110011 Initialise
        self._lcd_byte(0x32, self.LCD_CMD)  # 110010 Initialise
        self._lcd_byte(0x06, self.LCD_CMD)  # 000110 Cursor move direction
        self._lcd_byte(0x0C, self.LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
        self._lcd_byte(0x28, self.LCD_CMD)  # 101000 Data length, number of lines, font size
        self._lcd_byte(0x01, self.LCD_CMD)  # 000001 Clear display
        time.sleep(self.E_DELAY)

    def _lcd_byte(self, bits, mode):
        """
        Send byte to data pins.
        bits = the data
        mode = 1 for data
               0 for command
        """
        bits_high = mode | (bits & 0xF0) | self.LCD_BACKLIGHT
        bits_low = mode | ((bits << 4) & 0xF0) | self.LCD_BACKLIGHT
        # High bits
        self.bus.write_byte(self.I2C_ADDR, bits_high)
        self._lcd_toggle_enable(bits_high)
        # Low bits
        self.bus.write_byte(self.I2C_ADDR, bits_low)
        self._lcd_toggle_enable(bits_low)

    def _lcd_toggle_enable(self, bits):
        """ Toggle enable display. """
        time.sleep(self.E_DELAY)
        self.bus.write_byte(self.I2C_ADDR, (bits | self.ENABLE))
        time.sleep(self.E_PULSE)
        self.bus.write_byte(self.I2C_ADDR, (bits & ~self.ENABLE))
        time.sleep(self.E_DELAY)

    def _lcd_blank(self):
        """ Blank LCD display. """
        self._lcd_byte(0x01, self.LCD_CMD)

    def _lcd_string(self, message, line):
        """ Send string to display. """
        message = message.center(self.LCD_WIDTH, " ")
        self._lcd_byte(line, self.LCD_CMD)
        for i in range(self.LCD_WIDTH):
            self._lcd_byte(ord(message[i]), self.LCD_CHR)

    def display(self, line1, line2, duration):
        """ Display input line 1 & 2 string onto LCD display. """
        try:
            for line in (line1, line2):
                if len(line) > 16:
                    raise ValueError(f'"{line}" has {len(line)} chars. Maximum char is 16.')
            self._lcd_string(line1, self.LCD_LINE_1)
            self._lcd_string(line2, self.LCD_LINE_2)
            time.sleep(duration)
        finally:
            self._lcd_blank()

    def display_datetime(self, tz):
        """ Display current time and date onto LCD display. """
        month = {
            "01": "Jan",
            "02": "Feb",
            "03": "Mar",
            "04": "Apr",
            "05": "May",
            "06": "Jun",
            "07": "Jul",
            "08": "Aug",
            "09": "Sept",
            "10": "Oct",
            "11": "Nov",
            "12": "Dec",
        }
        current_time = datetime.datetime.now(timezone("UTC")).astimezone(timezone(tz))
        current_month = month[current_time.strftime("%m")]
        self._lcd_string(current_time.strftime("%I:%M:%S %p"), self.LCD_LINE_1)
        self._lcd_string(current_time.strftime(f"{current_month} %d, %Y"), self.LCD_LINE_2)
