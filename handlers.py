from typing import List, TypeVar, Optional, Union

from telegram.ext import BaseHandler
from telegram._utils.types import DVInput
from telegram.ext._utils.types import CCT, HandlerCallback

RT = TypeVar("RT")
UT = TypeVar("UT")


class QueueHandler(BaseHandler):
    state: int = 0
    handlers: List[BaseHandler]

    def __init__(self, handlers: List[BaseHandler]):
        super().__init__(handlers[0].callback)

        self.handlers = handlers

    def check_update(self, update: object) -> Optional[Union[bool, object]]:
        if self.state < len(self.handlers):
            if self.handlers[self.state].check_update(update):
                return True
            else:
                return False
        else:
            self.state = 0

# про рекурсивные объекты:
#
# входной точкой в подобъекты всегда является handle_update(...) объекта,
# поэтому изменение state в объекте вызывает параллельное использование подобъектов
#
# функция может за одно своё выполнение набрать несколько апдейтов,
# при этом за одно выполнение можно обработать только одно,
# поэтому в конце остаются лишние
#
# нужно как-то заменить вызов handle_update(...) на его добавление в какую-то очередь на выполнение
#
# если state объекта не будет обновляться лишний раз, баг тоже будет исправлен

    async def handle_update(self, update, application, check_result, context):
        application.create_task(self.handlers[self.state].handle_update(
            update, application, check_result, context), update)

        await application.update_queue.put(update)
        self.state += 1
