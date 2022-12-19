from aiogram.utils import executor
from create_bot import dp


async def on_startup(_):
    """
    Функция оповещающая о начале работы телеграм бота
    :param _:
    :return: Возвращает в консоль сообщение об успешном запуске бота
    """
    print(
        'Бот успешно запущен. Скоро здесь будет служебная информация о боте. \nК примеру список его возможностей или источники из которых он берет информицию хз не придумал до конца ещё')


from handlers import usual, wikipedia_request, random, non_commands

usual.register_handlers_usual(dp)
wikipedia_request.register_handlers_wikipedia_request(dp)
random.register_handlers_random(dp)
non_commands.register_handlers_non_commands(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
