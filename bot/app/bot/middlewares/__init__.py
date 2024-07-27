from aiogram import Dispatcher
from aiogram_tonconnect.middleware import AiogramTonConnectMiddleware
from aiogram_tonconnect.tonconnect.storage.base import ATCRedisStorage
from aiogram_tonconnect.utils.qrcode import QRUrlProvider

from .manager import ManagerMiddleware
from .throttling import ThrottlingMiddleware
from .tonapi import TONAPIMiddleware
from ..utils.texts import ATCInlineKeyboard, ATCTextMessage


def register_middlewares(dp: Dispatcher, **kwargs) -> None:
    """
    Register bot middlewares.
    """
    dp.update.outer_middleware.register(
        AiogramTonConnectMiddleware(
            storage=ATCRedisStorage(kwargs["redis"]),
            manifest_url=kwargs["config"].tonconnect.MANIFEST_URL,
            redirect_url="https://t.me/TONSubdomainBot",
            qrcode_provider=QRUrlProvider(),
            text_message=ATCTextMessage,
            inline_keyboard=ATCInlineKeyboard,
            tonapi_token=kwargs["config"].tonconnect.KEY,
        )
    )
    dp.update.outer_middleware.register(TONAPIMiddleware(kwargs["config"]))
    dp.update.outer_middleware.register(ThrottlingMiddleware())
    dp.update.outer_middleware.register(ManagerMiddleware())


__all__ = [
    "register_middlewares",
]
