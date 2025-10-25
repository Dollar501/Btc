# main.py
import logging
import os
import json
import hashlib
import threading
from decimal import Decimal

from dotenv import load_dotenv
from flask import Flask, jsonify
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, ContextTypes,
    CallbackQueryHandler
)

# Import bot modules
from localization import get_text, set_language_and_reply, build_language_menu
from data_store import MINING_HARDWARE, INVESTMENT_PLANS, FAQ_DATA, STATIC_MESSAGES
from helpers import build_main_menu

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get Web App URL from environment variables
WEB_APP_URL = os.getenv("WEB_APP_URL", "https://darkcyan-manatee-795600.hostingersite.com/")

# Initialize Flask app for web server
app = Flask(__name__)

@app.route('/')
def home():
    """Health check endpoint for hosting platforms."""
    return jsonify({
        "status": "running",
        "service": "BTC-CloudX Bot",
        "message": "Bot is active and running!"
    })

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({"status": "OK", "service": "healthy"})

@app.route('/status')
def status():
    """Status endpoint."""
    return jsonify({
        "bot_status": "active",
        "web_app_url": WEB_APP_URL,
        "service": "BTC-CloudX Mining Platform"
    })


# --- Command Handlers ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command and displays the main menu."""
    user = update.effective_user
    context.user_data.setdefault('lang', 'ar')
    
    welcome_message = get_text('welcome', context).format(user_mention=user.mention_html())
    
    # The button to open the Web App
    keyboard = [
        [InlineKeyboardButton(
            get_text("open_app_button", context),
            web_app=WebAppInfo(url=WEB_APP_URL)
        )],
        [InlineKeyboardButton(
            get_text("bot_menu_button", context),
            callback_data="main_menu"
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.message.reply_html(welcome_message, reply_markup=reply_markup)
        await update.callback_query.answer()
    else:
        await update.message.reply_html(welcome_message, reply_markup=reply_markup)


async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays the main menu of the bot."""
    query = update.callback_query
    await query.answer()
    
    text = get_text('main_menu_title', context)
    await query.edit_message_text(
        text=text,
        reply_markup=build_main_menu(context),
        parse_mode='Markdown'
    )

# --- Callback Query Handlers for Bot Menu ---


async def show_static_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays a static message like 'How it Works' or 'Privacy'."""
    query = update.callback_query
    await query.answer()
    
    key = query.data
    lang = context.user_data.get('lang', 'ar')
    text = STATIC_MESSAGES.get(lang, {}).get(key, "عذراً، المحتوى المطلوب غير موجود.")
    
    keyboard = [[InlineKeyboardButton(get_text("back_to_main_menu", context), callback_data="main_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='Markdown')

async def show_featured_plans(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays the featured investment plans in the chat with corrected Arabic labels."""
    query = update.callback_query
    await query.answer()
    
    # Use get_text only for the main title, assuming it's defined in localization
    response = f"*{get_text('featured_plans_title', context)}*\n\n"
    
    for plan in INVESTMENT_PLANS:
        # Get the plan name in the user's language
        lang = context.user_data.get('lang', 'ar')
        plan_name = plan['name'].get(lang, plan['name']['ar'])
        response += f"*{plan_name}*\n"
        # Use localized text for plan details
        response += f"💰 {get_text('price', context)}: ${plan['price']}\n"
        response += f"⚙️ {get_text('hashrate', context)}: {plan['hashrate']} TH/s\n"
        response += f"🔌 {get_text('device_source', context)}: {plan['device_source']}\n"
        response += f"📈 {get_text('daily_profit', context)}: ~${plan['daily_profit']:.2f}\n"
        response += f"📅 {get_text('annual_profit', context)}: ~${plan['annual_profit']:.2f}\n"
        
        # Check for the semi-annual bonus and add it if it exists
        if 'semi_annual_bonus' in plan and plan['semi_annual_bonus'] > 0:
            response += f"🎁 {get_text('semi_annual_bonus', context)}: ${plan['semi_annual_bonus']:.2f}\n"
        
        response += "--------------------\n"
    
    keyboard = [[InlineKeyboardButton(get_text("back_to_main_menu", context), callback_data="main_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=response, reply_markup=reply_markup, parse_mode='Markdown')


async def show_faq_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays the FAQ menu with questions."""
    query = update.callback_query
    await query.answer()
    
    # Get current language
    current_lang = context.user_data.get('language', 'ar')
    
    text = get_text('faq_title', context)
    keyboard = []
    
    # Get FAQ data for current language
    faq_data = FAQ_DATA.get(current_lang, FAQ_DATA['ar'])
    
    for i, (q, a) in enumerate(faq_data):
        keyboard.append([InlineKeyboardButton(q, callback_data=f"faq_{i}")])
    
    keyboard.append([InlineKeyboardButton(get_text("back_to_main_menu", context), callback_data="main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=text, reply_markup=reply_markup)


async def show_faq_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays the answer to a selected FAQ."""
    query = update.callback_query
    await query.answer()
    
    # Get current language
    current_lang = context.user_data.get('language', 'ar')
    
    faq_index = int(query.data.split('_')[1])
    
    # Get FAQ data for current language
    faq_data = FAQ_DATA.get(current_lang, FAQ_DATA['ar'])
    question, answer = faq_data[faq_index]
    
    text = f"❓ *{question}*\n\n{answer}"
    
    keyboard = [[InlineKeyboardButton(get_text("back_to_faq_menu", context), callback_data="faq")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='Markdown')

async def get_subscription_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generates and shows a unique, persistent user subscription code."""
    query = update.callback_query
    await query.answer()
    user_id = str(update.effective_user.id)
    
    hasher = hashlib.sha256(user_id.encode('utf-8'))
    unique_part = hasher.hexdigest()[:7].upper()
    
    user_code = f"BTC-77-{unique_part}"
    
    text = get_text('subscription_code_text', context).format(user_code=user_code)
    
    keyboard = [[InlineKeyboardButton(get_text("back_to_main_menu", context), callback_data="main_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='Markdown')

async def show_contact_us(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays contact information and links."""
    query = update.callback_query
    await query.answer()
    
    text = get_text("contact_us_content", context)
    
    keyboard = [
        [InlineKeyboardButton(get_text("join_channel_button", context), url=os.getenv("TELEGRAM_CHANNEL_URL"))],
        [InlineKeyboardButton(get_text("contact_support_button", context), url=os.getenv("TELEGRAM_SUPPORT_URL"))],
        [InlineKeyboardButton(get_text("back_to_main_menu", context), callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='Markdown')

async def language_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays the language selection menu."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=get_text("select_language", context),
        reply_markup=build_language_menu(context)
    )

# --- Web App Data Handler ---

async def web_app_data_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Receives data from the Web App and processes it."""
    try:
        data = json.loads(update.effective_message.web_app_data.data)
        logger.info(f"Received web app data: {data}")
        
        if data.get('action') == 'create_custom_plan':
            payload = data['payload']

            response = (
                f"*{get_text('custom_plan_result_title', context)}*\n"
                "-----------------------------------\n"
                f"*{get_text('investment_amount', context)}:* ${payload['investment']}\n"
                f"*{get_text('contract_duration', context)}:* {payload['duration']} سنوات\n"
                f"*{get_text('calculated_hashrate', context)}:* {payload['hashrate']} TH/s\n"
                f"*{get_text('total_profit_estimate', context)}:* ~${payload['totalProfit']}\n"
                "-----------------------------------\n"
                f"{get_text('plan_request_prompt', context)}"
            )
            
            keyboard = [
                [InlineKeyboardButton(get_text('contact_support_button', context), url=os.getenv("TELEGRAM_SUPPORT_URL"))],
                [InlineKeyboardButton(get_text('close_message_button', context), callback_data='delete_message')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(text=response, reply_markup=reply_markup, parse_mode='Markdown')
            
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"Error processing web app data: {e}")
        await update.message.reply_text("حدث خطأ أثناء معالجة طلبك من التطبيق.")

async def delete_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Deletes the message when the 'Close' button is pressed."""
    query = update.callback_query
    await query.answer()
    await query.delete_message()

def run_web_server():
    """Runs the Flask web server."""
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting web server on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)

def main() -> None:
    """Starts the bot and web server."""
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not BOT_TOKEN:
        logger.error("FATAL: TELEGRAM_BOT_TOKEN not found in .env file.")
        return
    if "your-app-url.com" in WEB_APP_URL:
        logger.warning("Warning: WEB_APP_URL is not set in .env file. The Web App will not work.")

    # Start web server in a separate thread
    web_thread = threading.Thread(target=run_web_server)
    web_thread.daemon = True
    web_thread.start()
    logger.info("Web server started in background thread")

    application = Application.builder().token(BOT_TOKEN).build()

    # --- Register Handlers ---
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data_handler))
    application.add_handler(CallbackQueryHandler(main_menu_handler, pattern=r"^main_menu$"))
    application.add_handler(CallbackQueryHandler(show_featured_plans, pattern=r"^featured_plans$"))
    application.add_handler(CallbackQueryHandler(show_static_message, pattern=r"^(how_it_works|privacy_policy)$"))
    application.add_handler(CallbackQueryHandler(show_faq_menu, pattern=r"^faq$"))
    application.add_handler(CallbackQueryHandler(show_faq_answer, pattern=r"^faq_\d+$"))
    application.add_handler(CallbackQueryHandler(get_subscription_code, pattern=r"^get_subscription_code$"))
    application.add_handler(CallbackQueryHandler(show_contact_us, pattern=r"^contact_us$"))
    application.add_handler(CallbackQueryHandler(language_menu_handler, pattern=r"^language$"))
    application.add_handler(CallbackQueryHandler(set_language_and_reply, pattern=r"^set_lang_"))
    application.add_handler(CallbackQueryHandler(delete_message_handler, pattern=r"^delete_message$"))
    application.add_handler(CallbackQueryHandler(start_command, pattern=r"^open_webapp$"))

    logger.info("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
