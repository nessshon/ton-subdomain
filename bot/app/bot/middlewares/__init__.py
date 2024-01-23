from aiogram import Dispatcher
from aiogram_tonconnect.middleware import AiogramTonConnectMiddleware

from .manager import ManagerMiddleware
from .throttling import ThrottlingMiddleware
from .tonapi import TONAPIMiddleware


def register_middlewares(dp: Dispatcher, **kwargs) -> None:
    """
    Register bot middlewares.
    """
    dp.update.outer_middleware.register(
        AiogramTonConnectMiddleware(
            redis=kwargs["redis"],
            manifest_url=kwargs["config"].tonconnect.MANIFEST_URL,
            exclude_wallets=[],
            qrcode_type="url",
        )
    )
    dp.update.outer_middleware.register(TONAPIMiddleware(kwargs["config"]))
    dp.update.outer_middleware.register(ThrottlingMiddleware())
    dp.update.outer_middleware.register(ManagerMiddleware())


__all__ = [
    "register_middlewares",
]
