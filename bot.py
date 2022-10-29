from config import API_TOKEN, USER_ID
import logging
import asyncio
from aiogram import Bot, Dispatcher, executor
from headhunter import HeadHunter

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
hh = HeadHunter('lastkey.txt')


async def scheduled():
    while True:
        new_vacancies = hh.new_vacancies()
        if new_vacancies:
            new_vacancies.reverse()
            for new_vacancy in new_vacancies:
                await bot.send_message(USER_ID, text=new_vacancy)
            hh.update_lastkey(new_vacancy)
        await asyncio.sleep(3600)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled())
    executor.start_polling(dp, skip_updates=True)
