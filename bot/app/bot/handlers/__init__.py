from aiogram import Dispatcher
from aiogram_tonconnect.handlers import AiogramTonConnectHandlers

from . import callback_query
from . import command
from . import errors
from . import inline_query
from . import message


def include_routers(dp: Dispatcher) -> None:
    """
    Include bot routers.
    """

    AiogramTonConnectHandlers().register(dp)

    dp.include_routers(
        *[
            errors.router,
            command.router,
            message.router,
            inline_query.router,
            callback_query.router,
        ]
    )


__all__ = [
    "include_routers",
]
