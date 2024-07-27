import asyncio

from aiogram.utils.markdown import hbold
from aiogram_tonconnect import ATCManager
from aiogram_tonconnect.tonconnect.models import AccountWallet
from pytonapi import AsyncTonapi
from pytonapi.exceptions import TONAPIError
from pytoniq_core import Builder

from app.bot.manager import Manager
from app.bot.utils import keyboards
from app.bot.utils.states import State


async def get_next_resolver_address(tonapi: AsyncTonapi, tx_hash: str) -> str | None:
    for _ in range(10):
        try:
            event = await tonapi.events.get_event(tx_hash)
            for action in event.actions:
                if action.ContractDeploy:
                    return action.ContractDeploy.address.to_raw()
        except TONAPIError:
            await asyncio.sleep(1)
        continue
    return None


class Window:

    @staticmethod
    async def source_code(manager: Manager) -> None:
        text = manager.text_message.get("source_code")
        reply_markup = keyboards.source_code(manager.text_button)

        await manager.send_message(text, reply_markup=reply_markup)
        await manager.state.set_state(State.source_code)

    @staticmethod
    async def select_language(manager: Manager, **_) -> None:
        text = manager.text_message.get("select_language")
        reply_markup = keyboards.select_language(manager.text_button)

        frmt_data = {"full_name": hbold(manager.user.full_name)}

        await manager.send_message(text.format_map(frmt_data), reply_markup=reply_markup)
        await manager.state.set_state(State.select_language)

    @staticmethod
    async def change_language(manager: Manager) -> None:
        text = manager.text_message.get("change_language")
        reply_markup = keyboards.select_language(manager.text_button, include_back=True)

        await manager.send_message(text, reply_markup=reply_markup)
        await manager.state.set_state(State.change_language)

    @staticmethod
    async def main_menu(manager: Manager, text: str = None, account_wallet: AccountWallet = None, **_) -> None:
        if account_wallet is not None:
            await manager.state.update_data(wallet_address=account_wallet.address.to_userfriendly())
        if not text:
            text = manager.text_message.get("main_menu").format(fullname=hbold(manager.user.full_name))
        reply_markup = keyboards.main_menu(manager.text_button, manager.is_testnet)

        await manager.send_message(text, reply_markup=reply_markup)
        await manager.state.set_state(State.main_menu)

    @staticmethod
    async def settings_menu(manager: Manager, atc_manager: ATCManager, **_) -> None:
        wallet = atc_manager.user.account_wallet.address.to_userfriendly()
        text = manager.text_message.get("settings_menu").format(wallet=wallet)
        reply_markup = keyboards.settings_menu(manager.text_button, manager.is_testnet)

        await manager.send_message(text, reply_markup=reply_markup)
        await manager.state.set_state(State.settings_menu)

    @staticmethod
    async def deploy_and_set(manager: Manager) -> None:
        text = manager.text_message.get("deploy_and_set")
        reply_markup = keyboards.deploy_and_set(manager.text_button)

        await manager.send_message(text, reply_markup=reply_markup)
        await manager.state.set_state(State.deploy_and_set)

    @staticmethod
    async def send_subdomain(manager: Manager, text: str = None, transaction_boc: str = None, **_) -> None:
        if transaction_boc:
            builder = Builder.from_boc(transaction_boc)
            tx_hash = [b.hash.hex() for b in builder][0]
            next_resolver_address = await get_next_resolver_address(manager.tonapi, tx_hash)
            await manager.state.update_data(next_resolver_address=next_resolver_address)

        if not text:
            text = manager.text_message.get("send_subdomain")
        reply_markup = keyboards.back(manager.text_button)

        await manager.send_message(text, reply_markup=reply_markup)
        await manager.state.set_state(State.send_subdomain)

    @staticmethod
    async def select_options(manager: Manager, **_) -> None:
        state_data = await manager.state.get_data()
        subdomain = state_data.get("subdomain")

        text = manager.text_message.get("select_options").format(subdomain=subdomain)
        reply_markup = keyboards.select_options(manager.text_button)

        await manager.send_message(text, reply_markup=reply_markup)
        await manager.state.set_state(State.select_options)

    @staticmethod
    async def send_storage(manager: Manager, text: str = None, **_) -> None:
        if not text:
            text = manager.text_message.get("send_storage")
        reply_markup = keyboards.back_main(manager.text_button)

        await manager.send_message(text, reply_markup=reply_markup)
        await manager.state.set_state(State.send_storage)

    @staticmethod
    async def send_wallet(manager: Manager, text: str = None, **_) -> None:
        if not text:
            text = manager.text_message.get("send_wallet")
        reply_markup = keyboards.back_main(manager.text_button)

        await manager.send_message(text, reply_markup=reply_markup)
        await manager.state.set_state(State.send_wallet)

    @staticmethod
    async def send_site(manager: Manager, text: str = None, **_) -> None:
        if not text:
            text = manager.text_message.get("send_site")
        reply_markup = keyboards.back_main(manager.text_button)

        await manager.send_message(text, reply_markup=reply_markup)
        await manager.state.set_state(State.send_site)

    @staticmethod
    async def transaction_accepted(manager: Manager, **_) -> None:
        state_data = await manager.state.get_data()
        subdomain = f"{state_data.get('subdomain', '')}.{state_data.get('domain', '')}"

        text = manager.text_message.get("transaction_accepted")
        reply_markup = keyboards.back_main(manager.text_button)

        options_texts = {
            "set_storage": manager.text_message.get("set_storage_done").format(
                subdomain=subdomain, storage_hex=state_data.get("storage_hex", "-"),
            ),
            "set_wallet": manager.text_message.get("set_wallet_done").format(
                subdomain=subdomain, wallet_address=state_data.get("wallet_address", "-"),
            ),
            "set_site": manager.text_message.get("set_site_done").format(
                subdomain=subdomain, adnl_address=state_data.get("adnl_address", "-"),
            ), None: ""
        }
        text += options_texts[state_data.get("option", None)]

        await manager.send_message(text, reply_markup=reply_markup)
        await manager.state.set_state(State.transaction_accepted)

    @staticmethod
    async def unknown_error(manager: Manager) -> None:
        text = manager.text_message.get("unknown_error")
        reply_markup = keyboards.main(manager.text_button)

        await manager.send_message(text, reply_markup=reply_markup)
        await manager.state.set_state(State.unknown_error)
