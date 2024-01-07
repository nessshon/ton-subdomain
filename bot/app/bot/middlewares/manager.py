from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject, User

from app.bot.manager import Manager


class ManagerMiddleware(BaseMiddleware):
    """
    Middleware for passing manager object.
    """

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        """
        Call the middleware.

        :param handler: The handler function.
        :param event: The Telegram event.
        :param data: Additional data.
        """
        user: User = data.get("event_from_user")
        state: FSMContext = data.get("state")
        state_data = await state.get_data()

        language_code = state_data.get("language_code", user.language_code)
        manager = Manager("💎", data, language_code)

        # Pass the manager object to the handler function
        data["manager"] = manager

        # Call the handler function with the event and data
        return await handler(event, data)
