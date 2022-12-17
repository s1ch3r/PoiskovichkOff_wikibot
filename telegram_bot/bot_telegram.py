from aiogram.utils import executor
from create_bot import dp




async def on_startup(_):
    print('Бот успешно запущен. Скоро здесь будет служебная информация о боте. \nК примеру список его возможностей или источники из которых он берет информицию хз не придумал до конца ещё')

from handlers import client, admin, other
client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

#переименовать client в usual_commands(usual), other в non_command_messages(non_commands), admin в wiki_request_command(wikipedia_request)
#инлайн клавиатура в доп вопросе??? мб тогда доп вопрос вне машины состяний, главное запоминать последний запрос пользователя
