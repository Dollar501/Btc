# command_processors.py
# Handles basic commands and general information sections.

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from helpers import build_main_menu
from localization import get_text

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command and displays the main menu."""
    user = update.effective_user
    context.user_data.setdefault('lang', 'ar')
    context.user_data['menu_expanded'] = True
    
    welcome_message = get_text('welcome', context).format(user_mention=user.mention_html())
    
    # Edit the message if it's a callback query, otherwise reply
    if update.callback_query:
        await update.callback_query.edit_message_text(
            text=welcome_message,
            reply_markup=build_main_menu(context),
            parse_mode='HTML'
        )
    else:
        await update.message.reply_html(
            welcome_message,
            reply_markup=build_main_menu(context)
        )

async def toggle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Toggles the main menu visibility."""
    query = update.callback_query
    await query.answer()
    context.user_data['menu_expanded'] = not context.user_data.get('menu_expanded', False)
    await query.edit_message_reply_markup(reply_markup=build_main_menu(context))

async def show_contact_us(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays contact information."""
    query = update.callback_query
    await query.answer()

    title = get_text("contact_us_title", context)
    content = get_text("contact_us_content", context)
    text_to_send = f"{title}\n\n{content}"

    keyboard = [
        [InlineKeyboardButton(get_text("join_channel_button", context), url="https://t.me/YOUR_CHANNEL_LINK")],
        [InlineKeyboardButton(get_text("contact_me_button", context), url="https://t.me/YOUR_USERNAME")],
        [InlineKeyboardButton(get_text("back_to_main_menu", context), callback_data="main_menu_from_child")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=text_to_send, reply_markup=reply_markup, parse_mode='Markdown')

async def select_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shows language selection options."""
    query = update.callback_query
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton("🇸🇦 العربية", callback_data="set_lang_ar"),
            InlineKeyboardButton("🇬🇧 English", callback_data="set_lang_en"),
        ],
        [InlineKeyboardButton(get_text("back_to_main_menu", context), callback_data="main_menu_from_child")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=get_text("select_language", context), reply_markup=reply_markup)

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sets the user's language preference."""
    query = update.callback_query
    await query.answer()
    
    lang_code = query.data.split('set_lang_')[1]
    context.user_data['lang'] = lang_code
    
    await query.answer(text=get_text("language_updated", context), show_alert=True)
    
    # Re-display the main menu with the new language
    await start(update, context)
