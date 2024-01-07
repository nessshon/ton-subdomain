from aiogram.fsm.state import StatesGroup

from aiogram.fsm.state import State as BaseState


class State(StatesGroup):
    select_language = BaseState()
    change_language = BaseState()

    main_menu = BaseState()
    settings_menu = BaseState()

    deploy_and_set = BaseState()
    send_subdomain = BaseState()
    select_options = BaseState()

    send_storage = BaseState()
    send_wallet = BaseState()
    send_site = BaseState()
    transaction_accepted = BaseState()

    unknown_error = BaseState()
