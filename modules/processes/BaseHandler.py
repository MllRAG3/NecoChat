from pyrogram.filters import Filter
from pyrogram.handlers.handler import Handler


class BaseHandler:
    __name__ = "Unknown"
    HANDLER: Handler = Handler
    FILTER: Filter | None = None

    async def func(self, *args, **kwargs):
        raise NotImplementedError

    @property
    def pyrogram_handler(self):
        return self.HANDLER(self.func, self.FILTER)
