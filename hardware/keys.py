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
        self._key_clicked = Key.NO_KEY

        for key in Key:
            if key_gpio := key.value:
                GPIO.setup(key_gpio, GPIO.IN, GPIO.PUD_UP)
                GPIO.add_event_detect(key_gpio, GPIO.FALLING, callback=self._handle_key_pressed, bouncetime=20)
                GPIO.add_event_detect(key_gpio, GPIO.RISING, callback=self._handle_key_released, bouncetime=20)
    
    def _handle_key_pressed(self, channel):
        self._last_key_pressed = Key(channel)

    def _handle_key_released(self, channel):
        key = Key(channel)
        if key == self._last_key_pressed:
            self._key_clicked = Key(channel)
            self._last_key_pressed = Key.NO_KEY
            
    def get_key(self) -> Key:
        key = self._key_clicked
        self.flus()
        return key
    
    def flush(self):
        self._last_key_pressed = Key.NO_KEY
        self._key_clicked = Key.NO_KEY


_key_handler = _KeysHandler()


def KeyHandler() -> _KeysHandler:
    return _key_handler
