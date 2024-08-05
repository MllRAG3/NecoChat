from typing import Final
from pymorphy3 import MorphAnalyzer

CREATOR_ID: Final[int] = 1044385209
BOT_ID: Final[int] = 7377494530

OP_USERS: Final[list[int]] = [
    CREATOR_ID,
    BOT_ID,
]


MUTE_TIME_FOR_F_WORD: Final[int] = 300  # in secs


analyzer: Final[MorphAnalyzer] = MorphAnalyzer(lang='ru')
