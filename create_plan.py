# create_plan.py
# Handles the Web App integration for creating a custom plan.

import json
from decimal import Decimal
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from localization import get_text
from data_store import MINING_HARDWARE

async def show_plan_creator_webapp(update: Update, context: ContextTypes.DEFAULT_TYPE, web_app_url: str) -> None:
    """Sends a message with a button to open the plan creator Web App."""
    query = update.callback_query
    await query.answer()
    
    keyboard = [[
        InlineKeyboardButton(
            get_text("open_web_app_button", context),
            web_app=WebAppInfo(url=web_app_url)
        )
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=get_text("open_plan_creator", context),
        reply_markup=reply_markup
    )

async def web_app_data_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Receives data from the Web App, calculates, and displays the results."""
    data = json.loads(update.effective_message.web_app_data.data)
    
    device_type = data['deviceType']
    device_id = data['deviceId']
    device = next((d for d in MINING_HARDWARE[device_type] if d['id'] == device_id), None)
    
    if not device:
        await update.message.reply_text("Error: Device not found.")
        return

    quantity = int(data['quantity'])
    device_price = Decimal(device['price'])
    device_profit = Decimal(device['profit'])

    # Calculations
    total_price = device_price * quantity
    monthly_profit_usd = device_profit * quantity
    annual_profit_usd = monthly_profit_usd * 12
    
    quarterly_profit_percent = ((monthly_profit_usd * 3) / total_price) * 100 if total_price > 0 else 0
    annual_profit_percent = (annual_profit_usd / total_price) * 100 if total_price > 0 else 0

    # Build response message
    response = f"{get_text('custom_plan_result_title', context)}\n"
    response += "-----------------------------------\n"
    response += f"*{get_text('result_price', context)}:* ${total_price:,.2f}\n"
    response += f"*{get_text('result_devices_count', context)}:* {quantity}\n"
    response += f"*{get_text('result_devices_used', context)}:*\n- {device['name']}\n"
    response += "________________________________\n"
    response += f"*{get_text('result_monthly_profit_usd', context)}:* ~${monthly_profit_usd:,.2f}\n"
    response += f"*{get_text('result_quarterly_profit_percent', context)}:* ~{quarterly_profit_percent:.2f}%\n"
    response += f"*{get_text('result_annual_profit_percent', context)}:* ~{annual_profit_percent:.2f}%\n"
    response += f"*{get_text('result_annual_profit_usd', context)}:* ~${annual_profit_usd:,.2f}\n"

    keyboard = [[InlineKeyboardButton(get_text("back_to_main_menu", context), callback_data="main_menu_from_child")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(text=response, reply_markup=reply_markup, parse_mode='Markdown')
