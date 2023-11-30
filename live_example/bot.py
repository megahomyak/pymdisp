from aiogram.types import Message
import m_tg_utils
import pymdisp
import asyncio
from getpass import getpass

bot = m_tg_utils.Bot(token=getpass("Enter the bot's token: "))
dispatcher = pymdisp.Dispatcher()

async def get_number(waiter: pymdisp.Waiter, error_message: str):
    while True:
        message = await waiter
        try:
            return (int(message.text), message)
        except ValueError:
            await message.reply(error_message)

async def get_text(waiter: pymdisp.Waiter, error_message: str):
    while True:
        message = await waiter
        if message.text:
            return (message.text, message)
        else:
            await message.reply(error_message)

async def handle_message(waiter: pymdisp.Waiter, message: Message):
    if message.text == "/start":
        await message.reply("Hello! Enter your name, please:")
        name, message = await get_text(waiter, "Your message did not contain any text. Please, enter your name:")
        await message.reply("Now, enter your surname:")
        surname, message = await get_text(waiter, "Your message did not contain any text. Please, enter your surname:")
        await message.reply("Now, enter your age:")
        age, message = await get_number(waiter, "No, age must be a number! Please, try again:")
        await message.reply(f"Thanks for testing the library! Your name is {name} {surname} and you're {age} years old!")

@bot.dp.message()
async def _handle_message(message: Message):
    asyncio.create_task(dispatcher.dispatch(
        key=message.chat.id,
        message=message,
        handler=handle_message,
    ))

bot.start()
