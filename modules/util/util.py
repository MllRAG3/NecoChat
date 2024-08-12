import matplotlib.pyplot as plt
from modules.database.models import models
from modules.database import db

from datetime import datetime
import re


def create_tables() -> None:
    """Database models to tables"""
    if not any(models):
        print("No database models created.")
        return
    with db:
        db.create_tables(models)
    print(f"created models: {', '.join(map(lambda x: x.__name__, models))}")


def extract_arguments(text: str) -> str or None:
    regexp = re.compile(r"/\w*(@\w*)*\s*([\s\S]*)", re.IGNORECASE)
    result = regexp.match(text)
    return result.group(2) if text.startswith('/') and text is not None else None


def safe_to_datetime(value: str, f: str = "%d/%m/%Y %H:%M") -> datetime | None:
    try:
        return datetime.strptime(value, f)
    except ValueError:
        return None


def make_plt_pic(
        cust_num: int,
        today: list[int],
        all_time: list[int],
        usernik: str = "Хз кто ето"
) -> None:
    plt.figure(figsize=(10, 5))
    plt.style.use("grayscale")

    plt.subplot(211)  # rows / cols / position
    plt.title("сегодня")
    plt.ylabel("Сообщения")
    plt.minorticks_on()
    plt.bar(
        [i for i in range(1, len(today) + 1)],
        today
    )

    plt.subplot(212)
    plt.title("за все время")
    plt.xlabel("День")
    plt.ylabel("Сообщения")
    plt.minorticks_on()

    plt.bar(
        [i for i in range(len(all_time))],
        all_time
    )

    plt.suptitle(f'С Т А Т А   П О Л Ь З О В А Т Е Л Я   {usernik}')
    plt.savefig(str(cust_num))
