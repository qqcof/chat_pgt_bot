import logging
import openai
import config
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)
chat_api= config.chat_api

bot = Bot(config.token)
dp = Dispatcher(bot)

@dp.message_handler()
async def chat_cmd(message: types.Message):
    openai.api_key = chat_api
    model_engine = 'text-davinci-003'
    prompt = message.text.split(maxsplit=1)
    if len(prompt) < 1:
        await message.reply("Жду Ваших вопросов :)")
        return
    prompt = prompt[1] if len(prompt) > 1 else message.text
    try:
        completation = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            temperature=0.5,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=None
        )
        if not completation.choices:
            await message.reply("API OpenAI вернул пустой ответ")
            return
        response = completation.choices[0].text
        # Разбиваем длинный текст ответа на несколько сообщений
        response_parts = [response[i:i+4096] for i in range(0, len(response), 4096)]
        for part in response_parts:
            await message.reply(part)
    except Exception as e:
        logging.error(f"Ошибка при вызове OpenAI API: {e}")
        await message.reply("Произошла ошибка при обработке вашего запроса, попробуйте еще раз позже.")
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)