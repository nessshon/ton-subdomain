from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_tonconnect import ATCManager

from app.bot.handlers.windows import Window
from app.bot.manager import Manager

router = Router()
router.message.filter(F.chat.type == "private")


@router.message(Command("start"))
async def start_command(message: Message, manager: Manager, atc_manager: ATCManager) -> None:
    state_data = await manager.state.get_data()
    if atc_manager.user.account_wallet and state_data.get("wallet_address"):
        await Window.main_menu(manager)
    else:
        await Window.select_language(manager)

    await manager.delete_message(message)


@router.message(Command("language"))
async def language_command(message: Message, manager: Manager, atc_manager: ATCManager) -> None:
    if atc_manager.user.account_wallet and atc_manager.user.account_wallet.address:
        await Window.change_language(manager)
    else:
        await Window.select_language(manager)

    await manager.delete_message(message)


async def source_command(message: Message, manager: Manager, atc_manager: ATCManager) -> None:
    if atc_manager.user.account_wallet and atc_manager.user.account_wallet.address:
        await Window.source_code(manager)
    else:
        await Window.select_language(manager)

    await manager.delete_message(message)
