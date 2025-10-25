# plan.py
# Handles displaying the pre-defined investment plans.

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from localization import get_text
from data_store import INVESTMENT_PLANS

async def show_investment_plans(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays the investment plan category menu."""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton(get_text("monthly_plans", context), callback_data="show_plan_cat_monthly")],
        [InlineKeyboardButton(get_text("quarterly_plans", context), callback_data="show_plan_cat_quarterly")],
        [InlineKeyboardButton(get_text("annually_plans", context), callback_data="show_plan_cat_annually")],
        [InlineKeyboardButton(get_text("back_to_main_menu", context), callback_data="main_menu_from_child")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=f"{get_text('plans_title', context)}\n\n{get_text('plans_intro', context)}",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def display_plan_category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays the details of plans in a selected category."""
    query = update.callback_query
    await query.answer()
    
    category = query.data.split('show_plan_cat_')[1]
    plans = INVESTMENT_PLANS.get(category, [])
    
    response_text = ""
    for plan in plans:
        response_text += f"*{plan['name']}*\n"
        # ... and so on for other plan details
        response_text += "--------------------\n"

    keyboard = [[InlineKeyboardButton(get_text("back_to_main_menu", context), callback_data="investment_plans")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=response_text, reply_markup=reply_markup, parse_mode='Markdown')
