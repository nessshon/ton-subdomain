from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram_tonconnect import ATCManager
from aiogram_tonconnect.tonconnect.models import ConnectWalletCallbacks, SendTransactionCallbacks

from app.bot.handlers.windows import Window
from app.bot.manager import Manager
from app.bot.utils.states import State
from app.bot.utils.texts import SUPPORTED_LANGUAGES
from app.bot.utils.transactions import DeploySubdomainManagerTransaction

router = Router()
router.callback_query.filter(F.message.chat.type == "private")


@router.callback_query(F.data == "main")
async def main_menu_callback_query(call: CallbackQuery, manager: Manager) -> None:
    await Window.main_menu(manager)
    await call.answer()


@router.callback_query(State.select_language)
async def select_language_callback_query(call: CallbackQuery, manager: Manager, atc_manager: ATCManager) -> None:
    if call.data in SUPPORTED_LANGUAGES.keys():
        await manager.state.update_data(language_code=call.data)
        await atc_manager.update_interfaces_language(call.data)
        await atc_manager.connect_wallet(
            callbacks=ConnectWalletCallbacks(
                before_callback=Window.select_language,
                after_callback=Window.main_menu,
            ),
        )

    await call.answer()


@router.callback_query(State.change_language)
async def change_language_callback_query(call: CallbackQuery, manager: Manager, atc_manager: ATCManager) -> None:
    if call.data == "back":
        await Window.settings_menu(manager, atc_manager)

    elif call.data in SUPPORTED_LANGUAGES.keys():
        manager.text_button.language_code = call.data
        manager.text_message.language_code = call.data
        await manager.state.update_data(language_code=call.data)
        await atc_manager.update_interfaces_language(call.data)
        await Window.settings_menu(manager, atc_manager)

    await call.answer()


@router.callback_query(State.main_menu)
async def main_menu_callback_query(call: CallbackQuery, manager: Manager, atc_manager: ATCManager) -> None:
    if call.data == "settings_menu":
        await Window.settings_menu(manager, atc_manager)

    await call.answer()


@router.callback_query(State.settings_menu)
async def settings_menu_callback_query(call: CallbackQuery, manager: Manager, atc_manager: ATCManager) -> None:
    if call.data == "back":
        await Window.main_menu(manager)

    elif call.data == "change_language":
        await Window.change_language(manager)

    elif call.data.startswith("switch"):
        is_testnet = False if call.data == "switch_to_mainnet" else True
        manager.is_testnet = is_testnet
        await manager.state.update_data(is_testnet=is_testnet)
        await call.answer(manager.text_message.get("switch_warning"), show_alert=True)
        await Window.settings_menu(manager, atc_manager)

    elif call.data == "disconnect_wallet":
        if atc_manager.tonconnect.connected:
            await atc_manager.disconnect_wallet()
            await manager.state.update_data(account_wallet=None)
        await Window.select_language(manager)

    await call.answer()


@router.callback_query(State.deploy_and_set)
async def deploy_and_set_callback_query(call: CallbackQuery, manager: Manager, atc_manager: ATCManager) -> None:
    if call.data == "back":
        await Window.main_menu(manager)

    elif call.data == "deploy_and_set":
        state_data = await manager.state.get_data()
        domain_address = state_data.get("domain_address")

        await atc_manager.send_transaction(
            callbacks=SendTransactionCallbacks(
                before_callback=Window.main_menu,
                after_callback=Window.send_subdomain,
            ),
            transaction=DeploySubdomainManagerTransaction(
                owner_address=atc_manager.user.account_wallet.address.to_raw(),
                domain_address=domain_address,
            ),
        )

    await call.answer()


@router.callback_query(State.send_subdomain)
async def send_subdomain_callback_query(call: CallbackQuery, manager: Manager) -> None:
    if call.data == "back":
        await Window.main_menu(manager)

    await call.answer()


@router.callback_query(State.select_options)
async def select_options_callback_query(call: CallbackQuery, manager: Manager) -> None:
    if call.data == "back":
        await Window.send_subdomain(manager)

    elif call.data == "set_storage":
        await manager.state.update_data(option=call.data)
        await Window.send_storage(manager)

    elif call.data == "set_wallet":
        await manager.state.update_data(option=call.data)
        await Window.send_wallet(manager)

    elif call.data == "set_site":
        await manager.state.update_data(option=call.data)
        await Window.send_site(manager)

    await call.answer()


@router.callback_query(State.send_storage)
@router.callback_query(State.send_wallet)
@router.callback_query(State.send_site)
async def selected_options_callback_query(call: CallbackQuery, manager: Manager) -> None:
    if call.data == "back":
        await Window.select_options(manager)

    await call.answer()


@router.callback_query(State.transaction_accepted)
async def transaction_accepted_callback_query(call: CallbackQuery, manager: Manager) -> None:
    if call.data == "back":
        await Window.select_options(manager)

    await call.answer()
