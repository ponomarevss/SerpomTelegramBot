import asyncio
import logging
from typing import Any, Dict

from aiogram import Bot, Dispatcher, F, Router, html, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from form import Form
from keyboards import like_bot_keyboard_builder

BOT_TOKEN = "6956131544:AAE2QYfsW6hae4ypg8mfvkvBkUdIJsgZVnM"

form_router = Router()
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
dp.include_router(form_router)


@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.name)
    await message.answer(
        "Hi there! What's your name?",
    )


@form_router.message(Form.name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(Form.like_bots)
    await message.answer(
        f"Nice to meet you, {html.quote(message.text)}!\nDo you like to write bots?",
        reply_markup=like_bot_keyboard_builder.as_markup()
    )


@form_router.callback_query(Form.like_bots, F.data == "yes")
async def process_like_write_bots(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.update_data(like_bots=callback.data)
    await state.set_state(Form.language)
    await callback.message.answer(
        "Cool! I'm too!\nWhat programming language did you use for it?"
    )


@form_router.callback_query(Form.like_bots, F.data == "no")
async def process_dont_like_write_bots(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.update_data(like_bots=callback.data)
    data = await state.get_data()
    await state.clear()
    await callback.message.answer(
        "Not bad not terrible.\nSee you soon."
    )
    await show_summary(message=callback.message, data=data, positive=False)


@form_router.message(Form.like_bots)
async def process_unknown_write_bots(message: Message) -> None:
    await message.reply("I don't understand you :(")


@form_router.message(Form.language)
async def process_language(message: Message, state: FSMContext) -> None:
    data = await state.update_data(language=message.text)
    await state.clear()

    if message.text.casefold() == "python":
        await message.reply(
            "Python, you say? That's the language that makes my circuits light up! 😉"
        )

    await show_summary(message=message, data=data)


async def show_summary(message: Message, data: Dict[str, Any], positive: bool = True) -> None:
    name = data["name"]
    like_bots = data.get("like_bots")
    language = data.get("language")
    text = f"I'll keep in mind that, {html.quote(name)}, "
    text += (
        f"you like to write bots with {html.quote(language)}."
        if positive
        else "you don't like to write bots, so sad..."
    )
    await message.answer(text=text)
    await message.answer(
        text=f"Summary data:\n"
             f"name: {name}\n"
             f"like_bots: {like_bots}\n"
             f"language: {language}"
    )


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
