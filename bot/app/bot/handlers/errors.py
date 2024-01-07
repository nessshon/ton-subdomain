import asyncio
import logging
import traceback

from aiogram import Router, F
from aiogram.types import ErrorEvent, BufferedInputFile
from aiogram.utils.markdown import hcode, hbold
from aiogram.exceptions import TelegramBadRequest

from app.bot.handlers.windows import Window
from app.bot.manager import Manager

router = Router()


@router.errors(F.exception.message.contains("query is too old"))
async def query_too_old(_: ErrorEvent) -> bool:
    ...


@router.errors()
async def telegram_api_error(event: ErrorEvent, manager: Manager) -> bool:
    logging.exception(f'Update: {event.update}\nException: {event.exception}')
    await Window.unknown_error(manager)

    try:
        document_message = await manager.bot.send_document(
            chat_id=manager.config.bot.DEV_ID,
            document=BufferedInputFile(
                traceback.format_exc().encode(),
                filename=f'error_{event.update.update_id}.txt',
            ),
            caption=f'{hbold(type(event.exception).__name__)}: {str(event.exception)[:1021]}...',
        )
        update_json = event.update.model_dump_json(indent=2, exclude_none=True)
        update_json_chunks = [update_json[i:i + 4096] for i in range(0, len(update_json), 4096)]
        for update in update_json_chunks:
            await asyncio.sleep(.2)
            await document_message.reply(text=hcode(update))

    except TelegramBadRequest:
        pass

    return True
