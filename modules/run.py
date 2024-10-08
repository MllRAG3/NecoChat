"""Run this file to start bot"""
from modules.bot import Il
from modules.util import create_tables
from modules.processes import handlers_to_add


def add_handlers() -> None:
    added = []
    for handler in handlers_to_add:
        Il.add_handler(handler().pyrogram_handler)
        added.append(handler().__name__.capitalize())

    print("Добавлены обработчики команд:", end="\n")
    for num, name in enumerate(added, start=1):
        print(f"{num}) {name}", end="\n")


def run_bot() -> None:
    try:
        add_handlers()
        create_tables()
        Il.run()
    except Exception as e:
        print(f"Can't run bot!\nError found: {e}")


if __name__ == "__main__":
    run_bot()
