from enum import Enum
from RPi import GPIO


GPIO.setmode(GPIO.BCM)


class Key(Enum):
    NO_KEY = None
    UP = 26
    DOWN = 23
    LEFT = 25
    RIGHT = 22


class _KeysHandler:
    def __init__(self):
        self._last_key_pressed = Key.NO_KEY

        for key in Key:
            if key_gpio := key.value:
                GPIO.setup(key_gpio, GPIO.IN, GPIO.PUD_UP)
                GPIO.add_event_detect(key_gpio, GPIO.RISING, callback=self._handle_key_pressed, bouncetime=20)
    
    def _handle_key_pressed(self, channel):
        if self._last_key_pressed == Key.NO_KEY:
            self._last_key_pressed = Key(channel)
            
    def get_key(self) -> Key:
        return self._last_key_pressed
    
    def flush(self):
        self._last_key_pressed = Key.NO_KEY


KeyHandler = _KeysHandler()
