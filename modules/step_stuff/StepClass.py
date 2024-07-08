from pyrogram import types
from typing import Callable, Any, Final


class Step:
    __name__ = "StepFilter"
    REGISTERED: dict[int, tuple[Callable, dict[str, Any]]] = {}

    def register_by_chat_id(self, chat_id: int, func: Callable, **kwargs_for_func) -> None:
        self.REGISTERED[chat_id] = (func, kwargs_for_func)

    async def get_and_execute(self, msg: types.Message):
        chat_id = msg.chat.id

        if not self.exist(chat_id): return
        func_call_result = await self.REGISTERED[chat_id][0](message=msg, **self.REGISTERED[chat_id][1])
        del self.REGISTERED[chat_id]

        return func_call_result

    def exist(self, id_: int) -> bool:
        return self.REGISTERED.get(id_) is not None

    def __call__(self, _, msg: types.Message):
        return self.exist(msg.chat.id)


NEXT_STEP: Final[Step] = Step()  # Use ONLY this to register next sent messages:3!!!
