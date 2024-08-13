from typing import Final
from pymorphy3 import MorphAnalyzer

CREATOR_ID: Final[int] = 1044385209
BOT_ID: Final[int] = 7377494530

OP_USERS: Final[list[int]] = [
    CREATOR_ID,
    BOT_ID,
]

analyzer: Final[MorphAnalyzer] = MorphAnalyzer(lang='ru')
