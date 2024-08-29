from enum import Enum
from RPi import GPIO


GPIO.setmode(GPIO.BCM)


class Key(Enum):
    NO_KEY = None
    UP = 17
    DOWN = 16
    LEFT = 12
    RIGHT = 21


for key in Key:
    if pin := key.value:
        GPIO.setup(pin, GPIO.IN, GPIO.PUD_UP)


def get_key() -> Key:
    for key in Key:
        if pin := key.value:
            if GPIO.input(pin) == GPIO.LOW:
                return key

    return Key.NO_KEY

