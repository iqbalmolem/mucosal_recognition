import asyncio
import telegram



async def send_image(photo_raw, photo_predicted):
    bot = telegram.Bot("6518711807:AAHi8mP56h61AwKhdOweZy_cS07jM-XPoGY")
    async with bot:
        await bot.send_photo(photo=photo_raw, caption='raw',chat_id=686024024)
        await bot.send_photo(photo=photo_predicted, caption='predicted',chat_id=686024024)


def start(photo_raw, photo_predicted):
    asyncio.run(send_image(photo_raw, photo_predicted))
