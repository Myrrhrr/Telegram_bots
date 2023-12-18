from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

import openai
import logging

# Token BotFather
TELEGRAM_TOKEN = ""
#  API OpenAI
OPENAI_API_KEY = ""

openai.api_key = OPENAI_API_KEY

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


NAME, AGE, MARITAL_STATUS, DREAMS, OCCUPATION = range(5)

def start(update: Update, context: CallbackContext) -> int:
    user = update.effective_user
    chat_id = update.effective_chat.id
    context.user_data[chat_id] = {}  # Create an empty dictionary for the user
    update.message.reply_text(f"Привет, {user.first_name}! Давай познакомимся. Напиши свое имя:")
    return NAME

def save_user_data(update: Update, context: CallbackContext) -> int:
    chat_id = update.effective_chat.id
    user_info = context.user_data[chat_id]
    user_info['name'] = update.message.text
    update.message.reply_text(f"Отлично, {user_info['name']}! Теперь укажи свой возраст:")
    return AGE

def save_age(update: Update, context: CallbackContext) -> int:
    chat_id = update.effective_chat.id
    user_info = context.user_data[chat_id]
    user_info['age'] = update.message.text
    update.message.reply_text("Хорошо, а какое у тебя семейное положение?")
    return MARITAL_STATUS

def save_marital_status(update: Update, context: CallbackContext) -> int:
    chat_id = update.effective_chat.id
    user_info = context.user_data[chat_id]
    user_info['marital_status'] = update.message.text
    update.message.reply_text("Отлично! Расскажи, о чем ты мечтаешь?")
    return DREAMS

def save_dreams(update: Update, context: CallbackContext) -> int:
    chat_id = update.effective_chat.id
    user_info = context.user_data[chat_id]
    user_info['dreams'] = update.message.text
    update.message.reply_text("Интересно! А чем ты занимаешься?")
    return OCCUPATION

def save_occupation(update: Update, context: CallbackContext) -> int:
    chat_id = update.effective_chat.id
    user_info = context.user_data[chat_id]
    user_info['occupation'] = update.message.text
    update.message.reply_text("Спасибо за информацию! Теперь я подготовлю для тебя что-то особенное.")

    
    prompt = f"Напиши мотивационный текст из двух предложений учитывая информацию о пользователе: Имя: {user_info['name']}\nВозраст: {user_info['age']}\nСемейное положение: {user_info['marital_status']}\nЧто мечтаешь: {user_info['dreams']}\nЧем занимаешься: {user_info['occupation']}\n"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500
    )

    
    update.message.reply_text(response.choices[0].text)

    # Сброс данных пользователя после завершения диалога
    del context.user_data[chat_id]
    return ConversationHandler.END

def main() -> None:
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, save_user_data)],
            AGE: [MessageHandler(Filters.text & ~Filters.command, save_age)],
            MARITAL_STATUS: [MessageHandler(Filters.text & ~Filters.command, save_marital_status)],
            DREAMS: [MessageHandler(Filters.text & ~Filters.command, save_dreams)],
            OCCUPATION: [MessageHandler(Filters.text & ~Filters.command, save_occupation)],
        },
        fallbacks=[],
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
