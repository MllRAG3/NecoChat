from typing import Final

CREATOR_ID: Final[int] = 1044385209
BOT_ID: Final[int] = 7377494530

OP_USERS: Final[list[int]] = [
    CREATOR_ID,
    BOT_ID,
]

INTERACTIVE: Final[dict[str, str | list[str]]] = {
    "погладить": "{} погладил(а) {}",
}
