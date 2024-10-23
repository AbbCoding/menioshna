from telegram import Update
from telegram.ext import Application, MessageHandler, filters

async def get_file_id(update: Update, context):
    file_id = update.message.voice.file_id
    await update.message.reply_text(f"file_id: {file_id}")

def main():
    # Замени на токен твоего бота
    application = Application.builder().token("7895485090:AAGSt9yakLpiUSPaD3w068sSba2uKZw_3zI").build()

    # Обработчик для голосовых сообщений
    application.add_handler(MessageHandler(filters.VOICE, get_file_id))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
