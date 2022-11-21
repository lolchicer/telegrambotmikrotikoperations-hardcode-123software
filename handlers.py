from typing import List, TypeVar, Optional, Union

from telegram.ext import BaseHandler
from telegram._utils.types import DVInput
from telegram.ext._utils.types import CCT, HandlerCallback

RT = TypeVar("RT")
UT = TypeVar("UT")


class QueueHandler(BaseHandler):
    state: int = 0
    handlers: List[BaseHandler]

    def __init__(self, handlers: List[BaseHandler], block: DVInput[bool] = ...):
        super().__init__(handlers[0].callback, block)

        self.handlers = handlers

    def check_update(self, update: object) -> Optional[Union[bool, object]]:
        if self.handlers[self.state].check_update(update):
            return True
        else:
            return False

    async def handle_update(self, update, application, check_result, context):
        if self.state < len(self.handlers) - 1:
            await application.update_queue.put(update)
            self.state += 1
        else:
            self.state = 0
        await self.handlers[self.state - 1].handle_update(update, application, check_result, context)
