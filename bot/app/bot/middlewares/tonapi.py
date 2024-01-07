from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject
from pytonapi import AsyncTonapi

from app.config import Config


class TONAPIMiddleware(BaseMiddleware):
    """
    Middleware for passing tonapi object.
    """

    def __init__(self, config: Config) -> None:
        self.config = config

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
        state: FSMContext = data.get("state")
        state_data = await state.get_data()
        is_testnet = state_data.get("is_testnet")
        is_testnet = is_testnet if is_testnet is not None else False

        # Initialize the tonapi instance
        tonapi = AsyncTonapi(
            self.config.tonapi.API_KEY,
            is_testnet=is_testnet,
            max_retries=self.config.tonapi.MAX_RETRIES,
        )

        data["tonapi"] = tonapi
        data["is_testnet"] = is_testnet

        return await handler(event, data)
