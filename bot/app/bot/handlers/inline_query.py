from aiogram import Router, F
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from aiogram_tonconnect import ATCManager
from aiogram_tonconnect.tonconnect.models import AccountWallet
from pytonapi.schema.nft import NftItem

from app.bot.manager import Manager
from app.bot.utils.states import State
from app.config import get_dns_collections

router = Router()
router.inline_query.filter(F.chat_type == "sender")


@router.inline_query(State.main_menu)
async def select_deposit_nft(inline_query: InlineQuery, manager: Manager) -> None:
    offset = int(inline_query.offset) if inline_query.offset else 0
    collections, items = get_dns_collections(manager.is_testnet), []

    state_data = await manager.state.get_data()
    account_wallet = AccountWallet(**state_data.get("account_wallet", {}))

    for collection_address in collections:
        response = await manager.tonapi.accounts.get_nfts(
            account_wallet.address.to_raw(),
            collection=collection_address,
            limit=25, offset=offset, indirect_ownership=False,
        )
        items += response.nft_items

    results = [
        create_nft_article(item) for item in
        sorted(items, key=lambda item: item.index)
    ]

    if results:
        next_offset = str(offset + len(items))
        await inline_query.answer(
            results=results, cache_time=10, is_personal=True, next_offset=next_offset
        )


def create_nft_article(nft: NftItem) -> InlineQueryResultArticle:
    title = (
        nft.dns if nft.dns else nft.metadata.get("name", nft.metadata.get("name", "Unknown"))
    )
    collection = (
        nft.collection.name if nft.collection else None
    )
    description = nft.metadata.get("description", "")
    description = f"• {collection}\n{nft.collection.description}" if collection else description

    return InlineQueryResultArticle(
        title=title,
        id=nft.address.to_userfriendly(),
        description=description,
        thumb_url=nft.previews[-1].url,
        input_message_content=InputTextMessageContent(
            message_text=nft.address.to_userfriendly(),
        )
    )
