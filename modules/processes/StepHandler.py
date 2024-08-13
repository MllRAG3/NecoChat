from . import BaseHandler as B
from pyrogram import handlers, types
from modules.step_stuff import Step


class NextStepHandler(B.BaseHandler):
    __name__ = "NextStepHandler"
    HANDLER = handlers.MessageHandler
    FILTER = Step()

    async def func(self, _, message: types.Message):
        await Step(message=message).get_and_execute(message)
