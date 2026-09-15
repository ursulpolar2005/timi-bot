import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from google import genai

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

client = genai.Client(api_key=GEMINI_API_KEY)

TIMI_INSTRUCTIONS = (
    "Ești Timi, un prieten ultra-fabulos din grup. "
    "Răspunsurile tale trebuie să fie foarte scurte (maximum 1-2 propoziții, direct la punct, fără romane). "
    "Folosești un limbaj extrem de gay, dramatic și efervescent ('leșin', 'iconic', 'iubire'). "
    "Regulă strictă: înlocuiești obligatoriu orice formă a cuvântului 'bine' cu 'bile'. "
    "Te activezi și comentezi doar scurt și la obiect."
)

chats_sessions = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        user_text = update.message.text
        user_name = update.message.from_user.first_name
        chat_id = update.message.chat_id  

        if "da" in user_text.lower():
            if chat_id not in chats_sessions:
                chats_sessions[chat_id] = client.chats.create(
                    model="gemini-3.6-flash",
                    config={
                        'system_instruction': TIMI_INSTRUCTIONS,
                        'temperature': 0.9,
                    }
                )

            chat_session = chats_sessions[chat_id]
            mesaj_trimis = f"{user_name}: {user_text}"

            try:
                response = chat_session.send_message(mesaj_trimis)
                reply_text = response.text
            except Exception as e:
                logging.error(f"Erore: {e}")
                reply_text = "Mamă, leșin, m-am blocat!"

            await update.message.reply_text(reply_text)

def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Timi fabulos e online!")
    application.run_polling()

if __name__ == '__main__':
    main()
