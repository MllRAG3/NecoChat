"""Run this file to start bot"""
from modules.bot import Il
from modules.util import create_tables
from modules.processes import handlers_to_add


def add_handlers() -> None:
    for handler in handlers_to_add:
        Il.add_handler(handler().pyrogram_handler)
        print(f"{handler().__name__.capitalize()} (handler) успешно добавлен!")


def run_bot() -> None:
    try:
        add_handlers()
        create_tables()
        Il.run()
    except Exception as e:
        print(f"Can't run bot!\nError found: {e}")


if __name__ == "__main__":
    run_bot()
