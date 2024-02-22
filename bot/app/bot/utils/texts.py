from abc import abstractmethod, ABCMeta

from aiogram.types import (
    InlineKeyboardButton,
    SwitchInlineQueryChosenChat,
    LoginUrl,
    WebAppInfo,
)
from aiogram.utils.markdown import hide_link, hlink


class Text(metaclass=ABCMeta):

    def __init__(self, language_code: str) -> None:
        self.language_code = language_code if language_code == "ru" else "en"

    @property
    @abstractmethod
    def data(self) -> dict:
        raise NotImplementedError

    def get(self, code: str) -> str:
        return self.data[self.language_code][code]


class TextMessage(Text):

    @property
    def data(self) -> dict:
        return {
            "ru": {
                "source_code": (
                    hlink("Исходный код", "https://github.com/nessshon/ton-subdomain/tree/main/bot")
                ),
                "select_language": (
                    "👋 <b>Привет</b>, {full_name}!\n\n"
                    "Выберите язык:"
                ),
                "change_language": (
                    "<b>Выберите язык:</b>\n\n"
                ),
                "main_menu": (
                    f"{hide_link('https://telegra.ph//file/4361dbc645b1b25796a01.jpg')}"
                    "🏠 <b>Главное меню</b>\n\n"
                    "<b>Рад приветствовать тебя в этом боте,</b> специально созданном "
                    "для управления поддоменами .ton в сети TON.\n\n"
                    "• <b>Выбери свой домен</b>, воспользовавшись кнопкой, "
                    "либо отправь мне адрес смарт-контракта NFT домена.\n\n"
                    "<blockquote>Если у тебя еще нет домена – ты можешь приобрести его, "
                    "воспользовавшись соответствующей кнопкой.</blockquote>"
                ),
                "settings_menu": (
                    f"{hide_link('https://telegra.ph//file/a6e8dd433075543b601d2.jpg')}"
                    "⚙️ <b>Меню настроек</b>\n\n"
                    "• <b>Подключен кошелек:</b>\n<code>{wallet}</code>"
                ),
                "switch_warning": (
                    "Внимание! Не забудьте переподключить кошелек!"
                ),

                "deploy_and_set": (
                    "<b>Разверните и установите смарт-контракта</b>\n\n"
                    "• Для управления DNS-записями и создания поддоменов "
                    "необходимо развернуть и установить запись смарт-контракта.\n\n"
                    "<blockquote>Для выполнения этого действия необходимо отправить транзакцию "
                    "с помощью вашего кошелька.</blockquote>"
                ),
                "send_subdomain": (
                    "<b>Отправьте поддомен</b>\n\n"
                    "• Придумайте и отправьте мне поддомен, который вы хотите добавить.\n\n"
                    "<blockquote>Важно, чтобы поддомен не превышал 128 символов, "
                    "включая латинские буквы, цифры и дефис.</blockquote>"
                ),
                "wrong_subdomain": (
                    "<b>Неправильный поддомен</b>\n\n"
                    "• Отправьте корректный поддомен, который вы хотите добавить.\n\n"
                    "<blockquote>Важно, чтобы поддомен не превышал 128 символов, "
                    "включая латинские буквы, цифры и дефис.</blockquote>"
                ),
                "select_options": (
                    "<b>Выберите опцию</b>\n\n"
                    "• <b>Установить Хранилище</b> - HEX\n"
                    "• <b>Установить Кошелек</b> - адрес кошелька\n"
                    "• <b>Установить Сайт</b> - ADNL адрес\n\n"
                    "<b>Выбран поддомен:</b> <code>{subdomain}</code>"
                ),
                "send_storage": (
                    "<b>Отправьте HEX хранилища:</b>"
                ),
                "wrong_storage": (
                    "<b>Неправильный HEX хранилища!</b>\n\n"
                ),
                "set_storage_done": (
                    "\n\n"
                    "<b>Поддомен:</b>\n"
                    "<code>{subdomain}</code>\n"
                    "<b>HEX хранилища:</b>\n"
                    "<code>{storage_hex}</code>\n\n"
                    "<b>Хранилище установлено!</b>"
                ),
                "send_wallet": (
                    "<b>Отправьте адрес кошелька:</b>"
                ),
                "wrong_wallet": (
                    "<b>Неправильный адрес кошелька!</b>\n\n"
                ),
                "set_wallet_done": (
                    "\n\n"
                    "<b>Поддомен:</b>\n"
                    "<code>{subdomain}</code>\n"
                    "<b>Адрес кошелька:</b>\n"
                    "<code>{wallet_address}</code>\n\n"
                    "<b>Кошелек установлен!</b>"
                ),
                "send_site": (
                    "<b>Отправьте ADNL адрес сайта:</b>"
                ),
                "wrong_site": (
                    "<b>Неправильный ADNL адрес сайта!</b>"
                ),
                "set_site_done": (
                    "\n\n"
                    "<b>Поддомен:</b>\n"
                    "<code>{subdomain}</code>\n"
                    "<b>ADNL адрес:</b>\n"
                    "<code>{adnl_address}</code>\n\n"
                    "<b>Сайт установлен!</b>"
                ),
                "transaction_accepted": (
                    "<b>Транзакция принята</b>\n\n"
                    "• Транзакция обработана кошельком."
                ),

                "wrong_address": (
                    "<b>Неправильный адрес NFT!</b>\n\n"
                    "• Отправьте корректный адрес NFT."
                ),
                "wrong_collection": (
                    "<b>Неправильная коллекция NFT!</b>\n\n"
                    "• Указанный адрес NFT не принадлежит коллекцией TON DNS Domains."
                ),
                "wrong_owner": (
                    "<b>Неправильный владелец NFT!</b>\n\n"
                    "• Вы не являетесь владельцем NFT.\n\n"
                    "<blockquote>Возможно, NFT выставлен на продажу, "
                    "снимите его с продажи и попробуйте снова.</blockquote>"
                ),

                "unknown_error": (
                    "<b>Произошла неизвестная ошибка!</b>\n\n"
                    "• Попробуйте ещё раз.\n\n"
                    "<blockquote>Отчет об ошибке отправлен разработчикам.</blockquote>"
                ),
            },
            "en": {
                "source_code": (
                    hlink("Source code", "https://github.com/nessshon/ton-subdomain/tree/main/bot")
                ),
                "select_language": (
                    "👋 <b>Hello</b>, {full_name}!\n\n"
                    "Select language:"
                ),
                "change_language": (
                    "<b>Select language:</b>\n\n"
                ),
                "main_menu": (
                    f"{hide_link('https://telegra.ph//file/4361dbc645b1b25796a01.jpg')}"
                    "🏠 <b>Main menu</b>\n\n"
                    "<b>I am glad to welcome you to this bot,</b> "
                    "specially created for managing .ton subdomains in the TON network.\n\n"
                    "• <b>Select your domain</b> using the button, "
                    "or send me the NFT domain smart-contract address.\n\n"
                    "<blockquote>If you don't have a domain yet, "
                    "you can purchase it by using the appropriate button.</blockquote>"
                ),
                "settings_menu": (
                    f"{hide_link('https://telegra.ph//file/a6e8dd433075543b601d2.jpg')}"
                    "⚙️ <b>Settings menu</b>\n\n"
                    "<b>• Connected wallet:</b>\n<code>{wallet}</code>"
                ),
                "switch_warning": (
                    "Attention! Remember to reconnect your wallet!"
                ),

                "deploy_and_set": (
                    "<b>Deploy and install the smart contract</b>\n\n"
                    "• To manage DNS records and create subdomains, "
                    "you need to deploy and install a smart contract record."
                    "<blockquote>To perform this action, you must send a transaction "
                    "using your wallet.</blockquote>"
                ),
                "send_subdomain": (
                    "<b>Send subdomain</b>\n\n"
                    "• Come up with and send me the subdomain you want to add.\n\n"
                    "<blockquote>It is important that the subdomain does not exceed 128 characters, "
                    "including Latin letters, numbers and hyphens.</blockquote>"
                ),
                "wrong_subdomain": (
                    "<b>Invalid subdomain</b>\n\n"
                    "• Submit a valid subdomain that you want to add.\n\n"
                    "<blockquote>It is important that the subdomain does not exceed 128 characters, "
                    "including Latin letters, numbers and hyphens.</blockquote>"
                ),
                "select_options": (
                    "<b>Select an option</b>\n\n"
                    "• <b>Set Storage</b> - HEX\n"
                    "• <b>Set Wallet</b> - wallet address\n"
                    "• <b>Set Site</b> - ADNL address\n\n"
                    "<b>Subdomain selected:</b> <code>{subdomain}</code>"
                ),
                "send_storage": (
                    "<b>Send storage HEX:</b>"
                ),
                "wrong_storage": (
                    "<b>Wrong Storage HEX!</b>\n\n"
                ),
                "set_storage_done": (
                    "\n\n"
                    "<b>Subdomain:</b>\n"
                    "<code>{subdomain}</code>\n"
                    "<b>HEX storage:</b>\n"
                    "<code>{storage_hex}</code>\n\n"
                    "<b>Storage installed!</b>"
                ),
                "send_wallet": (
                    "<b>Send wallet address:</b>"
                ),
                "wrong_wallet": (
                    "<b>Wrong wallet address!</b>"
                ),
                "set_wallet_done": (
                    "\n\n"
                    "<b>Subdomain:</b>\n"
                    "<code>{subdomain}</code>\n"
                    "<b>Wallet address:</b>\n"
                    "<code>{wallet_address}</code>\n\n"
                    "<b>Wallet installed!</b>"
                ),
                "send_site": (
                    "<b>Send ADNL address:</b>"
                ),
                "wrong_site": (
                    "<b>Wrong ADNL address!</b>\n\n"
                ),
                "set_site_done": (
                    "\n\n"
                    "<b>Subdomain:</b>\n"
                    "<code>{subdomain}</code>\n"
                    "<b>ADNL address:</b>\n"
                    "<code>{adnl_address}</code>\n\n"
                    "<b>The site is installed!</b>"
                ),
                "transaction_accepted": (
                    "<b>Transaction accepted</b>\n\n"
                    "• Transaction processed by wallet."
                ),

                "wrong_address": (
                    "<b>Invalid NFT address!</b>\n\n"
                    "• Submit the correct NFT address."
                ),
                "wrong_collection": (
                    "<b>Invalid NFT collection!</b>\n\n"
                    "• The specified NFT address does not belong to the TON DNS Domains collection."
                ),
                "wrong_owner": (
                    "<b>Wrong NFT owner!</b>\n\n"
                    "• You are not the owner of the NFT.\n\n"
                    "<blockquote>The NFT may be up for sale,"
                    "take it off sale and try again.</blockquote>"
                ),

                "unknown_error": (
                    "<b>An unknown error has occurred!</b>\n\n"
                    "• Try again.\n\n"
                    "<blockquote>A bug report has been sent to the developers.</blockquote>"
                ),
            }
        }


class TextButton(Text):

    @property
    def data(self) -> dict:
        return {
            "ru": {
                "back": "‹ Назад",
                "main": "⌂ Главная",
                "source_code": "</> Исходный код",

                "disconnect_wallet": "× Отключить кошелек",
                "select_domain": "≡ Выбрать домен",
                "buy_ton_domains": "• Купить .TON домены",
                "buy_on_getgems": "• Купить на Getgems",
                "settings_menu": "⎔ Настройки",

                "change_language": "⇋ Изменить язык бота",
                "switch_to_mainnet": "◈ Переключить на основную сеть",
                "switch_to_testnet": "◇ Переключить на тестовую сеть",

                "deploy_and_set": "⌬ Развернуть и установить",

                "set_storage": "• Установить хранилище",
                "set_wallet": "• Установить кошелек",
                "set_site": "• Установить сайт",
            },
            "en": {
                "back": "‹ Back",
                "main": "⌂ Main",
                "source_code": "</> Source code",

                "disconnect_wallet": "× Disconnect wallet",
                "select_domain": "≡ Select domain",
                "buy_ton_domains": "• Buy .TON domains",
                "buy_on_getgems": "• Buy on Getgems",
                "settings_menu": "⎔ Settings",

                "change_language": "⇋ Change bot language",
                "switch_to_mainnet": "◈ Switch to Mainnet",
                "switch_to_testnet": "◇ Switch to Testnet",

                "deploy_and_set": "⌬ Deploy and Set",

                "set_storage": "• Set storage",
                "set_wallet": "• Set wallet",
                "set_site": "• Set site",
            }
        }

    def get_button(
            self,
            code: str,
            url: str | None = None,
            web_app: WebAppInfo | None = None,
            login_url: LoginUrl | None = None,
            switch_inline_query: str | None = None,
            switch_inline_query_current_chat: str | None = None,
            switch_inline_query_chosen_chat: SwitchInlineQueryChosenChat | None = None,
    ) -> InlineKeyboardButton:
        text = self.get(code)
        if url:
            return InlineKeyboardButton(text=text, url=url)
        elif web_app:
            return InlineKeyboardButton(text=text, web_app=web_app)
        elif login_url:
            return InlineKeyboardButton(text=text, login_url=login_url)
        elif switch_inline_query:
            return InlineKeyboardButton(text=text, switch_inline_query=switch_inline_query)
        elif switch_inline_query_current_chat:
            return InlineKeyboardButton(text=text, switch_inline_query_current_chat=switch_inline_query_current_chat)
        elif switch_inline_query_chosen_chat:
            return InlineKeyboardButton(text=text, switch_inline_query_chosen_chat=switch_inline_query_chosen_chat)
        return InlineKeyboardButton(text=text, callback_data=code)
