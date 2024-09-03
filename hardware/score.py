from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import sevensegment


SEGMENT_LENGTH = 8


_serial = spi(port=0, device=0, gpio=noop())
_device = max7219(_serial, cascaded=2)
_seg = sevensegment(_device)


def print_score(score: int, best_score: int):
    score, best_score = str(score), str(best_score)
    text = ['0' * (SEGMENT_LENGTH - len(s)) + s for s in (score, best_score)]

    _seg.text = text[0] + text[1]
