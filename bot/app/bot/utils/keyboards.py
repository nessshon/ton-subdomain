from aiogram.types import InlineKeyboardButton as Button
from aiogram.types import InlineKeyboardMarkup as Markup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.utils.texts import TextButton, SUPPORTED_LANGUAGES


def back(text_button: TextButton) -> Markup:
    return Markup(
        inline_keyboard=[
            [text_button.get_button("back")]
        ]
    )


def main(text_button: TextButton) -> Markup:
    return Markup(
        inline_keyboard=[[text_button.get_button("main")]]
    )


def source_code(text_button: TextButton) -> Markup:
    url = "https://github.com/nessshon/ton-subdomain/tree/main/bot"

    return Markup(
        inline_keyboard=[
            [text_button.get_button("source_code", url=url)],
            [text_button.get_button("main")]
        ]
    )


def main_menu(text_button: TextButton, is_testnet: bool) -> Markup:
    tondns_url = "https://dns.ton.org/?testnet=true" if is_testnet else "https://dns.ton.org/"
    getgems_url = (
        "https://testnet.getgems.io/collection/EQDjPtM6QusgMgWfl9kMcG-EALslbTITnKcH8VZK1pnH3UZA"
        if is_testnet else
        "https://getgems.io/collection/EQC3dNlesgVD8YbAazcauIrXBPfiVhMMr5YYk2in0Mtsz0Bz"
    )

    return Markup(
        inline_keyboard=[
            [text_button.get_button("select_domain", switch_inline_query_current_chat=" ")],
            [text_button.get_button("buy_ton_domains", web_app=WebAppInfo(url=tondns_url))],
            [text_button.get_button("buy_on_getgems", web_app=WebAppInfo(url=getgems_url))],
            [text_button.get_button("settings_menu")]
        ]
    )


def settings_menu(text_button: TextButton, is_testnet: bool) -> Markup:
    return Markup(
        inline_keyboard=[
            [text_button.get_button("switch_to_mainnet")
             if is_testnet else
             text_button.get_button("switch_to_testnet")],
            [text_button.get_button("change_language")],
            [text_button.get_button("disconnect_wallet")],
            [text_button.get_button("back")],
        ]
    )


def deploy_and_set(text_button: TextButton) -> Markup:
    return Markup(
        inline_keyboard=[
            [text_button.get_button("deploy_and_set")],
            [text_button.get_button("back")],
        ]
    )


def select_options(text_button: TextButton) -> Markup:
    return Markup(
        inline_keyboard=[
            [text_button.get_button("set_storage")],
            [text_button.get_button("set_wallet")],
            [text_button.get_button("set_site")],
            [text_button.get_button("back"), text_button.get_button("main")],
        ]
    )


def select_language(text_button: TextButton, include_back: bool = False) -> Markup:
    builder = InlineKeyboardBuilder().row(
        *[
            Button(text=text, callback_data=callback_data)
            for callback_data, text in SUPPORTED_LANGUAGES.items()
        ], width=2
    )
    if include_back:
        builder.row(text_button.get_button("back"))

    return builder.as_markup()
