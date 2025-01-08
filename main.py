import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CommandHandler, ContextTypes, ApplicationBuilder
import json
from dotenv import load_dotenv
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levellevel)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
token = os.getenv('TELEGRAM_TOKEN')

signs_translation = {
    'aries': 'Овен',
    'taurus': 'Телец',
    'gemini': 'Близнецы',
    'cancer': 'Рак',
    'leo': 'Лев',
    'virgo': 'Дева',
    'libra': 'Весы',
    'scorpio': 'Скорпион',
    'sagittarius': 'Стрелец',
    'capricorn': 'Козерог',
    'aquarius': 'Водолей',
    'pisces': 'Рыбы'
}

def get_horoscope(sign: str) -> str:
    url = f"https://horo.mail.ru/prediction/{sign}/today/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    script_tag = soup.find('script', id='horo-script')
    if not script_tag:
        return "Не удалось найти гороскоп. Попробуйте позже."
    
    script_content = script_tag.string
    json_data = json.loads(script_content.split('window.__PRELOADED_STATE__ = ')[1].rstrip(';'))
    
    horoscope_data = json_data.get('page_data', {}).get('prediction', {}).get('text', [])
    horoscope_text = "\n\n".join([item['html'] for item in horoscope_data if item['type'] == 'html'])
    
    if horoscope_text:
        return BeautifulSoup(horoscope_text, 'html.parser').get_text(strip=True)
    else:
        return "Не удалось получить гороскоп. Попробуйте позже."

def format_horoscope(sign: str, horoscope: str) -> str:
    sign_russian = signs_translation.get(sign, sign)
    return f'**Гороскоп для знака "{sign_russian}"**\n\n{horoscope}'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton("/horoscope_aries"), KeyboardButton("/horoscope_taurus")],
        [KeyboardButton("/horoscope_gemini"), KeyboardButton("/horoscope_cancer")],
        [KeyboardButton("/horoscope_leo"), KeyboardButton("/horoscope_virgo")],
        [KeyboardButton("/horoscope_libra"), KeyboardButton("/horoscope_scorpio")],
        [KeyboardButton("/horoscope_sagittarius"), KeyboardButton("/horoscope_capricorn")],
        [KeyboardButton("/horoscope_aquarius"), KeyboardButton("/horoscope_pisces")],
        [KeyboardButton("/help")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Привет! Я бот, который присылает гороскоп. Напиши /help, чтобы посмотреть все команды. Используйте команды /horoscope_<sign> для получения гороскопа.', reply_markup=reply_markup)

async def horoscope(update: Update, context: ContextTypes.DEFAULT_TYPE, sign: str) -> None:
    horoscope_text = get_horoscope(sign)
    formatted_horoscope = format_horoscope(sign, horoscope_text)
    await update.message.reply_text(formatted_horoscope, parse_mode='Markdown')

async def horoscope_aries(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await horoscope(update, context, 'aries')

async def horoscope_taurus(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await horoscope(update, context, 'taurus')

async def horoscope_gemini(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await horoscope(update, context, 'gemini')

async def horoscope_cancer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await horoscope(update, context, 'cancer')

async def horoscope_leo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await horoscope(update, context, 'leo')

async def horoscope_virgo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await horoscope(update, context, 'virgo')

async def horoscope_libra(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await horoscope(update, context, 'libra')

async def horoscope_scorpio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await horoscope(update, context, 'scorpio')

async def horoscope_sagittarius(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await horoscope(update, context, 'sagittarius')

async def horoscope_capricorn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await horoscope(update, context, 'capricorn')

async def horoscope_aquarius(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await horoscope(update, context, 'aquarius')

async def horoscope_pisces(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await horoscope(update, context, 'pisces')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "Доступные команды:\n"
        "/horoscope_aries - Гороскоп для Овна\n"
        "/horoscope_taurus - Гороскоп для Тельца\n"
        "/horoscope_gemini - Гороскоп для Близнецов\n"
        "/horoscope_cancer - Гороскоп для Рака\n"
        "/horoscope_leo - Гороскоп для Льва\n"
        "/horoscope_virgo - Гороскоп для Девы\n"
        "/horoscope_libra - Гороскоп для Весов\n"
        "/horoscope_scorpio - Гороскоп для Скорпиона\n"
        "/horoscope_sagittarius - Гороскоп для Стрельца\n"
        "/horoscope_capricorn - Гороскоп для Козерога\n"
        "/horoscope_aquarius - Гороскоп для Водолея\n"
        "/horoscope_pisces - Гороскоп для Рыб\n"
    )
    await update.message.reply_text(help_text)

def main():
    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("horoscope_aries", horoscope_aries))
    application.add_handler(CommandHandler("horoscope_taurus", horoscope_taurus))
    application.add_handler(CommandHandler("horoscope_gemini", horoscope_gemini))
    application.add_handler(CommandHandler("horoscope_cancer", horoscope_cancer))
    application.add_handler(CommandHandler("horoscope_leo", horoscope_leo))
    application.add_handler(CommandHandler("horoscope_virgo", horoscope_virgo))
    application.add_handler(CommandHandler("horoscope_libra", horoscope_libra))
    application.add_handler(CommandHandler("horoscope_scorpio", horoscope_scorpio))
    application.add_handler(CommandHandler("horoscope_sagittarius", horoscope_sagittarius))
    application.add_handler(CommandHandler("horoscope_capricorn", horoscope_capricorn))
    application.add_handler(CommandHandler("horoscope_aquarius", horoscope_aquarius))
    application.add_handler(CommandHandler("horoscope_pisces", horoscope_pisces))

    # chat_id = '2392612432'

    application.run_polling()

if __name__ == '__main__':
    main()
