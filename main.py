import os
import logging
from flask import Flask
from telegram import Update, InlineQueryResultVoice
from telegram.ext import Application, CommandHandler, InlineQueryHandler, ContextTypes
from threading import Thread

# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен бота (временно добавим сюда напрямую)
TOKEN = '7895485090:AAGSt9yakLpiUSPaD3w068sSba2uKZw_3zI'

# Данные о голосовых сообщениях (замените на реальные file_id)
voice_messages = [
    {"id": '1', "title": "Розыскадан келиб босишди", "file_id": 'AwACAgIAAxkBAAMCZxfKocwaWulmxjYV_blPPxp4l_UAArJfAAJK-ShI7_45_vWg5mQ2BA'}, 
    # ошна розыскадан келиб босишди икки кундан бери ашадедим
    {"id": '2', "title": "Силага кайп бўп қоптими а", "file_id": 'AwACAgIAAxkBAAMEZxfK0gKdFsE-S3o2X8KGwRTu-TAAAnNfAALfIwhI-IrEji-3j9Y2BA'},
    # силага кайп бўп қоптими а қанақадир таблоси узун мошинада ташкенни айланиб юраслар эканда а
    {"id": '3', "title": "Бўлди якшанба саунага чиқамиз", "file_id": 'AwACAgIAAxkBAAMGZxfK7ayTGiKqxYWUELy1re_Qi1MAAlY7AAI8rrhK515XDvGOZ2c2BA'},
    # бўлди якшанба саунага чиқамиз
    {"id": '4', "title": "Мени аям группалариндан чикип кеет деган", "file_id": 'AwACAgIAAxkBAAMIZxfLDoSOPzhCIuluM3hAixgpaSQAAnYdAAJxLVlKeOefFzqlMOw2BA'},
    # Блин дийиш мениям группалариндан чикип кееет деган яна қўшилволяпман э
    {"id": '5', "title": "Қадан бунақа гап келади калленга сени", "file_id": 'AwACAgIAAxkBAAMKZxfLOTW_k1pS3l4wA-sldkVZ9z0AApNKAAIfGhhJqXhldHggubw2BA'},
    # Қадан бунақа гап келади калленга сени
    {"id": '6', "title": "Мениям кўнглим бор", "file_id": 'AwACAgIAAxkBAAMMZxfLUUvH5hP-Nl6X5gE8ieRYHH0AAsAqAAIEN2FJyWaUV41fx5U2BA'},
    # Насиниэмсин мениям кўнглим бор, мениям кўнглим оғрийди
    {"id": '7', "title": "Хазиллашиб қўйдимда пидараз", "file_id": 'AwACAgIAAxkBAAMOZxfLrljte3rH6MkOOYYexjhXXkgAAsMqAAIEN2FJtyllxqLoQqI2BA'},
    # Хазиллашиб қўйдимда пидараз
    {"id": '8', "title": "Вариант қима менга", "file_id": 'AwACAgIAAxkBAAMQZxfL1piVEJBRcZXa5sNfD8PIEPEAAs4qAAIEN2FJtr4JHpd5Rlc2BA'},
    # Вариант қима менга
    {"id": '9', "title": "Тур йўқале нима деяпсан", "file_id": 'AwACAgIAAxkBAAMSZxfL50-12OUQHdXmh-kHj3XLyw4AAh4rAAIEN2FJsSNNAuS2TKs2BA'},
    # Тур йўқале нима деяпсан
    {"id": '10', "title": "Хее Андрюха нимўляпсан бле", "file_id": 'AwACAgIAAxkBAAMUZxfMBcMeqAllJei6CkMwbizZJWkAAisrAAIEN2FJNElY1NlD0e42BA'},
    # Хее Андрюха нима бўляпсан блее
    {"id": '11', "title": "Ха вошшем ёрворяпти", "file_id": 'AwACAgIAAxkBAAMWZxfMJoY8AVLvPw7jaFTb5VLFmHcAAjMrAAIEN2FJ-JV1EB_5nHY2BA'},
    # Ха вошшем ёрворяпти
    {"id": '12', "title": "Кўт бўсенам дўсм бўласан", "file_id": 'AwACAgIAAxkBAAMYZxfMSal0Rp47LcpLxs-e86YiEZ8AAo8yAALgBahIEYNLX97xo4s2BA'},
    # Кўт бўсенам дўсм бўласан
    {"id": '13', "title": "Вай жала.. тупойманда бле", "file_id": 'AwACAgIAAxkBAAMaZxfMfIIu_B53Swk-ibevOI_JcR0AAicvAALgBbBIwI0XEwLeWo82BA'},
    # Вай жала... Битта харпни ўннига қўйип қўяман деб.. Тупойманда бле
    {"id": '14', "title": "Ёзип туровир минде", "file_id": 'AwACAgIAAxkBAAMcZxfMnhxxVs89Y92dWXI57x5A32wAArQ6AAL1X2BJUETszbIVAAG4NgQ'},
    # Ха бу йўқ бўп кеттин ёзип туровир уяғ буяғ қилиб
    {"id": '15', "title": "Пашол нахуй дияппан", "file_id": 'AwACAgIAAxkBAAMeZxfMx1FhwLCqqqv2DbNe6E4FzQEAAh09AAKS6GlJkLpyjVrqypI2BA'},
    # Пашол нахуй дияппан
    {"id": '16', "title": "Хааа ха бўпти", "file_id": 'AwACAgIAAxkBAAMgZxfM4Ctd7nkIjcmcHlXoGq5kVrMAAiU0AAISQcBJGS4qUge6Ft42BA'},
    # Хааа ха бўпти
    {"id": '17', "title": "Хушёр қайна", "file_id": 'AwACAgIAAxkBAAMiZxfM-Z0v-LW7p11NkCFnAdeiKqEAArs1AAISQcBJ27xoEoE4JcA2BA'},
    # Ашинчун ўзинга эхтият бўлип юровир хушёр қайна
    {"id": '18', "title": "Хааааа", "file_id": 'AwACAgIAAxkBAAMkZxfNIfCSRVeWWaWFbq07K6CshioAArs3AAJiPhhKwMtKN9Ke8Ew2BA'},
    # Хааааа
    {"id": '19', "title": "Бўпти хўп чунган бўсен", "file_id": 'AwACAgIAAxkBAAMmZxfNO28qj1ajnRjdywqXuRltvm4AAv83AAK-tFBK1oDNw3FXrk42BA'},
    # Бўпти хўп чунган бўсен
    {"id": '20', "title": "Ха бўпти яхши", "file_id": 'AwACAgIAAxkBAAMoZxfNVrarWVqCD09RoDiayU2jwhcAAg8-AAKAOClKcCI1whqkG3c2BA'},
    # Ха бўпти, яхши
    {"id": '21', "title": "Миям ғалати бўпполди", "file_id": 'AwACAgIAAxkBAAMqZxfNdzkM0ctSFP8X-5TM_echr8UAAsVEAALLq6lL-Smqxu_Py4E2BA'},
    # Э хози нимўлди чунмадим миям ғалати бўпполди, кимдир бинаса дияпти
    {"id": '22', "title": "Бўпти ошна яхши дам олинг, иссиғроқ кийинволин", "file_id": 'AwACAgIAAxkBAAMsZxfNmL4jFmAXUGpHCpcuYLKic1EAAvlOAAIOkvFIMpsr8VA4wdk2BA'},
    # Бўпти ошна яхши дам олинг тинч бўлинга иссиғроқ кийинволин
    {"id": '23', "title": "Жигарим раҳмат катта боризга шукур", "file_id": 'AwACAgIAAxkBAAMuZxfNrCnPcDp_IBsuOytW_44RnC4AAkROAAK4lXlJJV6V3CDLrHA2BA'},
    # Жигарим раҳмат катта боризга шукур доим бор бўлинг
    {"id": '24', "title": "Орқада турган қизил футболкали қиз", "file_id": 'AwACAgIAAxkBAAMwZxfNw1mbbhSNnDieG6GoNFnFWroAAu5ZAAK4lYlJupxqbyap4yQ2BA'},
    # Орқадан турган қизил футболкали қиз чиройли қиз эдиканда бети кўринме қопти
    {"id": '25', "title": "Ваалайкум ассалом яхшимисизлар", "file_id": 'AwACAgIAAxkBAAMyZxfN3IWjj22wFtdrI9VPMYGMWQ0AAqM2AAKH0GFKjwE-dAOTvWU2BA'},
    # Ваалайкум ассалом яхшимисизлар
    {"id": '26', "title": "Ошна мия кечро ишледими?", "file_id": 'AwACAgIAAxkBAAM0ZxfN-ZDrO0Tdd0q-1MD5xXXE_moAAkczAAL3jWFKCP1LK_TwB7U2BA'},
    # Ошна мия кечро ишледими?
]

# Flask приложение
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# Функция для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обрабатывает команду /start, отправляет приветственное сообщение пользователю.
    """
    await update.message.reply_text(
        'Используйте инлайн-режим для выбора голосового сообщения. '
        'Введите @menioshnambot любой символ или слово.'
    )

# Функция для обработки инлайн-запросов
async def inline_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обрабатывает инлайн-запросы и возвращает список голосовых сообщений по запросу.
    """
    query = update.inline_query.query.strip().lower()

    # Если запрос пустой, возвращаем все голосовые сообщения
    results = []

    # Если запрос не пустой, фильтруем сообщения по названию
    if query:
        logger.info(f"Поисковый запрос: {query}")
        filtered_voices = [voice for voice in voice_messages if query in voice["title"].lower()]
    else:
        # Показываем все голосовые сообщения при любом символе
        filtered_voices = voice_messages

    # Формируем результаты для инлайн-ответа
    for voice in filtered_voices:
        results.append(InlineQueryResultVoice(
            id=voice["id"],
            voice_url=voice["file_id"],
            title=voice["title"]
        ))

    # Отправляем результаты инлайн-запроса
    try:
        await update.inline_query.answer(results)
        logger.info("Инлайн-запрос успешно обработан")
    except Exception as e:
        logger.error(f"Ошибка при обработке инлайн-запроса: {e}")

# Основная функция для запуска бота
def main():
    """
    Запуск бота с обработчиками команд и инлайн-запросов.
    """
    # Создание приложения с токеном
    application = Application.builder().token(TOKEN).build()

    # Обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Обработчик инлайн-запросов
    application.add_handler(InlineQueryHandler(inline_query_handler))

    # Запуск polling в отдельном потоке
    try:
        application.run_polling()
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")

# Функция для запуска Flask-сервера и бота параллельно
def run():
    # Запускаем Flask сервер в отдельном потоке
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Запуск Telegram бота
    main()

if __name__ == '__main__':
    run()