from . import BaseHandler as B
from pyrogram import handlers, types
from modules.step_stuff import NEXT_STEP


class NextStepHandler(B.BaseHandler):
    __name__ = "NextStepHandler"
    HANDLER = handlers.MessageHandler
    FILTER = NEXT_STEP

    async def func(self, _, message: types.Message):
        await NEXT_STEP.get_and_execute(message)
