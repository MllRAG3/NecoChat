import re
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

from modules.database.models import models, Messages, ChatMembers
from modules.database import db


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


def compress_list(lst: list, to: int, i=0):
    if len(lst) <= to: return lst
    if i + 2 > len(lst): i = 0
    if isinstance(lst[i], int):
        lst[i] = (lst.pop(i + 1) + lst[i]) // 2
    else:
        del lst[i + 1]

    compress_list(lst=lst, to=to, i=i + 1)
    return lst


def make_plt_pic(
        cust_num: int,
        today: list[int],
        all_time: list[int],
) -> str:
    plt.figure(figsize=(23, 20))
    plt.style.use("grayscale")

    plt.subplot(211)  # rows / cols / position
    plt.title("СЕГОДНЯ")
    plt.ylabel("СООБЩЕНИЯ")
    plt.xlabel("ЧАС")
    plt.grid()
    plt.minorticks_on()
    print(today)
    plt.bar(
        [i for i in range(1, len(today) + 1)],
        today
    )

    plt.subplot(212)
    plt.title("ЗА ВСЕ ВРЕМЯ")
    plt.xlabel("ДЕНЬ")
    plt.ylabel("СООБЩЕНИЯ")
    plt.grid()
    plt.minorticks_on()

    all_time = compress_list(all_time, to=100)
    print(all_time)
    plt.bar(
        [i for i in range(len(all_time))],
        all_time
    )

    plt.suptitle('С Т А Т А   П О Л Ь З О В А Т Е Л Я')
    plt.savefig(str(cust_num))
    return str(cust_num) + ".png"


def get_all_logs_grouped_by_days(member: ChatMembers) -> list[int]:
    all_logs = Messages \
        .select() \
        .where(Messages.sender == member) \
        .order_by(Messages.updated_at)

    grouped = []
    cur_date = all_logs[0].updated_at  # here we start
    for _ in range((all_logs[-1].updated_at - cur_date).days + 1):
        grouped.append(
            len(tuple(filter(lambda x: cur_date <= x.updated_at <= (cur_date + timedelta(days=1)), all_logs))))
        cur_date += timedelta(days=1)

    return grouped


def get_all_today_hours(member: ChatMembers) -> list[int]:
    now = datetime.now()
    all_today_logs = Messages \
        .select() \
        .where(
            (Messages.sender == member) & (Messages.updated_at.between(now - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond), now))
        ) \
        .order_by(Messages.updated_at)

    grouped = []
    c = datetime(year=now.year, month=now.month, day=now.day, hour=0, minute=0, second=0, microsecond=0)
    for _ in range(1, 25):
        grouped.append(len(tuple(filter(lambda x: c <= x.updated_at <= (c + timedelta(hours=1)), all_today_logs))))
        c += timedelta(hours=1)

    return grouped
