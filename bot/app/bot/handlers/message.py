from aiogram import Router, F
from aiogram.types import Message
from aiogram_tonconnect import ATCManager
from aiogram_tonconnect.tonconnect.models import SendTransactionCallbacks
from pytonapi import AsyncTonapi
from pytonapi.exceptions import TONAPIError

from app.bot.handlers.windows import Window
from app.bot.manager import Manager
from app.bot.utils.states import State
from app.bot.utils.transactions import SetWalletTransaction, SetStorageTransaction, SetSiteTransaction
from app.bot.utils.misc import validate_domain, StorageBagId, AdnlAddress
from app.config import get_dns_collections

router = Router()
router.message.filter(F.chat.type == "private")

SUBDOMAIN_MANAGER_CODE = "b5ee9c7201020a0100011d000114ff00f4a413f4bcf2c80b0102016202030202ce040500d3a1c61843ae92415270058001e5c08c45ae160f80012a04f1ae4205bc05e007ae93e00203f205f085060fe81edf42604384011c4705e033e04883dcb11fb64ddc4964ad1ba06b879240dc23572f37cc5caaab143a2ffe67bca06742438001246203c005060fe81edf42610201200607020120080900bb0ccc741d35c87e900c3c007e1071c17cb87d4831c0244c3834c7c0608414de8d246ea38db50074083e40be10a0c1fd03dbe84c00b4fff4c000700066350c1004e0c1fd05e5cc1620c1fd16cc38807e40be10a0c1fd05fe18bc00a44c38a0001b3b51343e90007e187d010c3e18a000193e10b23e1073c5bd00327b5520001d0824f4c1c0643a0835d244b5c8c060"  # noqa


@router.message(State.main_menu, F.content_type == "text")
async def main_menu_message(message: Message, manager: Manager, atc_manager: ATCManager) -> None:
    if message.content_type == "text":
        address = message.text
        await manager.send_loading()
        await manager.delete_message(message)

        try:
            nft = await manager.tonapi.nft.get_item_by_address(address)
        except TONAPIError:
            text = manager.text_message.get("wrong_address")
            await Window.main_menu(manager, text=text)
            return

        collection_address = nft.collection.address.to_userfriendly(True)
        owner_address = nft.owner.address.to_raw()

        if collection_address not in get_dns_collections(manager.is_testnet):
            text = manager.text_message.get("wrong_collection")
        elif owner_address != atc_manager.user.account_wallet.address:
            text = manager.text_message.get("wrong_owner")
        else:
            async def get_next_resolver(tonapi: AsyncTonapi, domain_name: str) -> str | None:
                try:
                    dns_record = await tonapi.dns.resolve(domain_name)
                except TONAPIError:
                    return None
                return dns_record.next_resolver

            execute_result = await manager.tonapi.blockchain.execute_get_method(
                nft.address.to_raw(), "get_domain"
            )
            domain = execute_result.decoded.get("domain", None)
            next_resolver = await get_next_resolver(manager.tonapi, f"{domain}.ton")
            await manager.state.update_data(domain=domain, domain_address=nft.address.to_raw())

            if next_resolver:
                contract = await manager.tonapi.blockchain.get_account_info(next_resolver)
                if contract.code == SUBDOMAIN_MANAGER_CODE:
                    await manager.state.update_data(next_resolver_address=contract.address.to_raw())
                    await Window.send_subdomain(manager)
                    return

            await Window.deploy_and_set(manager)
            return

        await Window.main_menu(manager, text=text)


@router.message(State.send_subdomain, F.content_type == "text")
async def send_subdomain_message(message: Message, manager: Manager) -> None:
    subdomain = message.text.lower()
    await manager.send_loading()
    await manager.delete_message(message)

    if validate_domain(subdomain):
        await manager.state.update_data(subdomain=subdomain)
        await Window.select_options(manager)

    else:
        text = manager.text_message.get("wrong_subdomain")
        await Window.send_subdomain(manager, text=text)


@router.message(State.send_storage, F.content_type == "text")
async def send_storage_message(message: Message, manager: Manager, atc_manager: ATCManager) -> None:
    storage_hex = message.text
    await manager.delete_message(message)

    try:
        bag_id = StorageBagId(storage_hex)
        state_data = await manager.state.get_data()
        await manager.state.update_data(storage_hex=storage_hex)

        await atc_manager.open_send_transaction_window(
            callbacks=SendTransactionCallbacks(
                after_callback=Window.transaction_accepted,
                before_callback=Window.select_options,
            ),
            transaction=SetStorageTransaction(
                domain=state_data["subdomain"],
                bag_id=bag_id.bytes,
                subdomain_manager_address=state_data["next_resolver_address"],
            ),
        )
    except (Exception,):
        text = manager.text_message.get("wrong_storage")
        await Window.send_storage(manager, text=text)


@router.message(State.send_wallet)
async def send_wallet_message(message: Message, manager: Manager, atc_manager: ATCManager) -> None:
    wallet_address = message.text
    await manager.send_loading()
    await manager.delete_message(message)

    try:
        wallet = await manager.tonapi.accounts.parse_address(wallet_address)
        state_data = await manager.state.get_data()
        await manager.state.update_data(wallet_address=wallet_address)

        await atc_manager.open_send_transaction_window(
            callbacks=SendTransactionCallbacks(
                after_callback=Window.transaction_accepted,
                before_callback=Window.select_options,
            ),
            transaction=SetWalletTransaction(
                domain=state_data["subdomain"],
                wallet_address=wallet.raw_form,
                subdomain_manager_address=state_data["next_resolver_address"],
            ),
        )

    except TONAPIError:
        text = manager.text_message.get("wrong_wallet")
        await Window.send_wallet(manager, text=text)


@router.message(State.send_site)
async def send_site_message(message: Message, manager: Manager, atc_manager: ATCManager) -> None:
    adnl_address = message.text
    await manager.send_loading()
    await manager.delete_message(message)

    try:
        adnl = AdnlAddress(adnl_address)
        state_data = await manager.state.get_data()
        await manager.state.update_data(adnl_address=adnl_address)

        await atc_manager.open_send_transaction_window(
            callbacks=SendTransactionCallbacks(
                after_callback=Window.transaction_accepted,
                before_callback=Window.select_options,
            ),
            transaction=SetSiteTransaction(
                domain=state_data["subdomain"],
                adnl_address=adnl.bytes,
                subdomain_manager_address=state_data["next_resolver_address"],
            ),
        )

    except (TONAPIError,):
        text = manager.text_message.get("wrong_site")
        await Window.send_site(manager, text=text)


@router.message()
async def default_message(message: Message, manager: Manager) -> None:
    await manager.delete_message(message)
