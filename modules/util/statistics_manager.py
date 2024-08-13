import os

from modules.database.models import Messages, ChatMembers
from datetime import datetime, timedelta
from matplotlib import pyplot as plt


class StatsManager:
    def __init__(self, member: ChatMembers):
        self.member: ChatMembers = member
        self.now: datetime = datetime.now()

    def __get_stats(self, days_period, now: datetime | None = None) -> list[Messages]:
        """
        Статистика за последнее время
        :param days_period: период, за который будет выдана статистика
        :param now: текущее время
        """
        if now is None: now = self.now
        return Messages \
            .select() \
            .where(Messages.updated_at.between(now - timedelta(days=days_period), now) & Messages.sender == self.member)

    def __compress_int_list(self, lst: list[int], to: int, i: int = 0) -> list[int]:
        """
        Сжимает список с int/float
        :param lst: Список
        :param to: Необходимая длина
        :param i: Техническая переменная для рекурсии
        :return: Сжатый список
        """
        if len(lst) <= to: return lst
        if i + 2 > len(lst): i = 0

        lst[i] = (lst.pop(i + 1) + lst[i]) // 2

        self.__compress_int_list(lst=lst, to=to, i=i + 1)
        return lst

    @property
    def per_day(self) -> int:
        """
        :return: Кол-во сообщений за текущий день
        """
        return len(self.__get_stats(1))

    @property
    def per_week(self) -> int:
        """
        :return: кол-во сообщений за текущую неделю
        """
        return len(self.__get_stats(7))

    @property
    def per_month(self) -> int:
        """
        :return: кол-во сообщений за текущий месяц
        """
        return len(self.__get_stats(30))

    @property
    def per_all(self) -> int:
        """
        :return: Кол-во сообщений за все время
        """
        return len(Messages.select())

    @property
    def all_logs_grouped_by_days(self) -> list[int]:
        """
        :return: Все сообщения сгруппированные по дням
        """
        all_logs = Messages \
            .select() \
            .where(Messages.sender == self.member) \
            .order_by(Messages.updated_at)

        grouped = []
        cur_date = all_logs[0].updated_at
        for _ in range((all_logs[-1].updated_at - cur_date).days + 1):
            grouped.append(
                len(tuple(filter(lambda x: cur_date <= x.updated_at <= (cur_date + timedelta(days=1)), all_logs))))
            cur_date += timedelta(days=1)

        return grouped

    @property
    def all_today_hours(self) -> list[int]:
        """
        :return: Все сообщения за сегодня сгруппированные по часам
        """
        hrs = today_zero_hr_time = self.now - timedelta(
            hours=self.now.hour, minutes=self.now.minute, seconds=self.now.second, microseconds=self.now.microsecond
        )
        all_today_logs = Messages \
            .select() \
            .where((Messages.sender == self.member) & (Messages.updated_at.between(today_zero_hr_time, self.now))) \
            .order_by(Messages.updated_at)

        grouped = []
        for _ in range(1, 25):
            grouped.append(
                len(tuple(filter(lambda x: hrs <= x.updated_at <= (hrs + timedelta(hours=1)), all_today_logs)))
            )
            hrs += timedelta(hours=1)

        return grouped

    @property
    def de_send(self) -> dict:
        """
        :return: Словарь для pyrogram.Message.reply_photo(...)
        """
        file = open(str(self.make_plt_pic(self.member.ID)), "rb")
        os.remove(file.name)
        return {"photo": file, "caption": str(self)}

    def make_plt_pic(self, name: str) -> str:
        """
        Составляет график активности
        :param name: Имя файла
        """
        plt.figure(figsize=(23, 20))
        plt.style.use("grayscale")

        plt.subplot(211)  # rows / cols / position
        plt.title("СЕГОДНЯ")
        plt.ylabel("СООБЩЕНИЯ")
        plt.xlabel("ЧАС")
        plt.grid()
        plt.minorticks_on()
        plt.bar(
            [i for i in range(1, len(self.all_today_hours) + 1)],
            self.all_today_hours
        )

        plt.subplot(212)
        plt.title("ЗА ВСЕ ВРЕМЯ")
        plt.xlabel("ДЕНЬ")
        plt.ylabel("СООБЩЕНИЯ")
        plt.grid()
        plt.minorticks_on()

        plt.bar(
            [i for i in range(len(self.all_logs_grouped_by_days))],
            self.__compress_int_list(self.all_logs_grouped_by_days, to=100)
        )

        plt.suptitle('С Т А Т А   П О Л Ь З О В А Т Е Л Я')
        plt.savefig(str(name))
        return str(name) + ".png"

    def __str__(self):
        return "Сообщения пользователя {}\nДень | Неделя | Месяц | Все время\n{} | {} | {} | {}".format(
            self.member.config[0].custom_name,
            str(self.per_day).rjust(3, "0"),
            str(self.per_week).rjust(3, "0"),
            str(self.per_month).rjust(3, "0"),
            str(self.per_all).rjust(3, "0")
        )
