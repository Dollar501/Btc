# helpers.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from localization import get_text
import os

# قائمة معرفات الأدمن
ADMIN_IDS = [int(x) for x in os.getenv('ADMIN_TELEGRAM_IDS', '').split(',') if x.strip()]

def is_admin(telegram_id: int) -> bool:
    """التحقق من كون المستخدم أدمن"""
    return telegram_id in ADMIN_IDS

def build_main_menu(context: ContextTypes.DEFAULT_TYPE) -> InlineKeyboardMarkup:
    """Builds the main menu for the bot chat."""
    keyboard = [
        [
            InlineKeyboardButton("👤 حسابي", callback_data="account_info"),
            InlineKeyboardButton("📝 إنشاء حساب", callback_data="start_registration"),
        ],
        [
            InlineKeyboardButton(get_text("featured_plans", context), callback_data="featured_plans"),
            InlineKeyboardButton(get_text("how_it_works", context), callback_data="how_it_works"),
        ],
        [
            InlineKeyboardButton(get_text("faq", context), callback_data="faq"),
            InlineKeyboardButton(get_text("privacy_policy", context), callback_data="privacy_policy"),
        ],
        [
            InlineKeyboardButton(get_text("get_subscription_code", context), callback_data="get_subscription_code"),
            InlineKeyboardButton(get_text("contact_us", context), callback_data="contact_us"),
        ],
        [
            InlineKeyboardButton(get_text("language", context), callback_data="language"),
        ],
        # A button to reopen the initial message with the Web App link
        [
             InlineKeyboardButton(get_text("open_app_button", context), callback_data="open_webapp")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
