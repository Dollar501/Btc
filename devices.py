# devices.py
# Handles the "Our Hardware" section of the bot.

import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from localization import get_text
from data_store import MINING_HARDWARE

async def show_hardware_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays the hardware category selection menu."""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton(get_text("show_asic", context), callback_data="browse_devices_asic_0")],
        [InlineKeyboardButton(get_text("show_gpu", context), callback_data="browse_devices_gpu_0")],
        [InlineKeyboardButton(get_text("back_to_main_menu", context), callback_data="main_menu_from_child")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=f"{get_text('hardware_title', context)}\n\n{get_text('hardware_intro', context)}",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def browse_devices(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Browses through devices and sends their picture and specs."""
    query = update.callback_query
    await query.answer()
    
    _, _, dev_type, index_str = query.data.split('_')
    index = int(index_str)
    
    device_list = MINING_HARDWARE[dev_type]
    device = device_list[index]
    
    # Build the caption text
    specs_text = (
        f"*{device['name']}*\n\n"
        f"- {get_text('profit_per_month', context)}: ~${device['profit']}\n"
        f"- {get_text('price_approx', context)}: ~${device['price']}"
    )
    
    # Build navigation buttons
    nav_row = []
    if index > 0:
        nav_row.append(InlineKeyboardButton(get_text("prev_device", context), callback_data=f"browse_devices_{dev_type}_{index - 1}"))
    if index < len(device_list) - 1:
        nav_row.append(InlineKeyboardButton(get_text("next_device", context), callback_data=f"browse_devices_{dev_type}_{index + 1}"))
    
    keyboard = [
        nav_row,
        [InlineKeyboardButton(get_text("back_to_hardware_menu", context), callback_data="our_hardware")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Get the local image path
    image_path = os.path.join('img', device['image'])

    # Delete the old message and send a new one with the photo
    await query.delete_message()
    
    try:
        with open(image_path, 'rb') as photo_file:
            await context.bot.send_photo(
                chat_id=query.effective_chat.id,
                photo=photo_file,
                caption=specs_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
    except FileNotFoundError:
        await context.bot.send_message(
            chat_id=query.effective_chat.id,
            text=f"⚠️ Error: Image not found for {device['name']}.\nPlease check the 'img' folder.",
            reply_markup=reply_markup
        )
