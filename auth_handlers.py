# auth_handlers.py
"""
معالجات التسجيل والمصادقة للبوت
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from database import db
from localization import get_text
import re

# حالات المحادثة
FIRST_NAME, LAST_NAME, EMAIL, PHONE, WALLET_TYPE, WALLET_ADDRESS = range(6)

# ==================== Registration Flow ====================

async def start_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """بدء عملية التسجيل"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    # التحقق من وجود حساب
    existing_user = db.get_user_by_telegram_id(user_id)
    if existing_user:
        await query.edit_message_text(
            text=f"✅ لديك حساب مسجل بالفعل!\n\n"
                 f"👤 الاسم: {existing_user['first_name']} {existing_user['last_name']}\n"
                 f"🔑 كود التحقق: `{existing_user['verification_code']}`\n"
                 f"💰 الرصيد: ${existing_user['balance']:.2f}",
            parse_mode='Markdown'
        )
        return ConversationHandler.END
    
    # توليد كود التحقق
    verification_code = db.generate_verification_code()
    context.user_data['verification_code'] = verification_code
    context.user_data['telegram_id'] = user_id
    
    await query.edit_message_text(
        text=f"🎉 مرحباً بك في BTC-CloudX!\n\n"
             f"📋 لإنشاء حسابك، سنحتاج بعض المعلومات.\n\n"
             f"🔑 كود التحقق الخاص بك:\n`{verification_code}`\n\n"
             f"⚠️ احفظ هذا الكود! ستحتاجه لإكمال التسجيل على الموقع.\n\n"
             f"📝 الخطوة 1/4: أدخل اسمك الأول:",
        parse_mode='Markdown'
    )
    
    return FIRST_NAME

async def receive_first_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """استقبال الاسم الأول"""
    first_name = update.message.text.strip()
    
    if len(first_name) < 2:
        await update.message.reply_text("❌ الاسم يجب أن يكون حرفين على الأقل. حاول مرة أخرى:")
        return FIRST_NAME
    
    context.user_data['first_name'] = first_name
    
    await update.message.reply_text(
        f"✅ تم حفظ: {first_name}\n\n"
        f"📝 الخطوة 2/4: أدخل اسم العائلة:"
    )
    
    return LAST_NAME

async def receive_last_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """استقبال اسم العائلة"""
    last_name = update.message.text.strip()
    
    if len(last_name) < 2:
        await update.message.reply_text("❌ اسم العائلة يجب أن يكون حرفين على الأقل. حاول مرة أخرى:")
        return LAST_NAME
    
    context.user_data['last_name'] = last_name
    
    await update.message.reply_text(
        f"✅ تم حفظ: {last_name}\n\n"
        f"📝 الخطوة 3/4: أدخل بريدك الإلكتروني:"
    )
    
    return EMAIL

async def receive_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """استقبال البريد الإلكتروني"""
    email = update.message.text.strip()
    
    # التحقق من صيغة البريد
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        await update.message.reply_text("❌ البريد الإلكتروني غير صحيح. حاول مرة أخرى:")
        return EMAIL
    
    context.user_data['email'] = email
    
    await update.message.reply_text(
        f"✅ تم حفظ: {email}\n\n"
        f"📝 الخطوة 4/4: أدخل رقم هاتفك (مع رمز الدولة):\n"
        f"مثال: +201234567890"
    )
    
    return PHONE

async def receive_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """استقبال رقم الهاتف وإكمال التسجيل"""
    phone = update.message.text.strip()
    
    # التحقق من صيغة الهاتف
    if len(phone) < 10:
        await update.message.reply_text("❌ رقم الهاتف غير صحيح. حاول مرة أخرى:")
        return PHONE
    
    context.user_data['phone'] = phone
    
    # إنشاء الحساب في قاعدة البيانات
    result = db.create_user(
        telegram_id=context.user_data['telegram_id'],
        first_name=context.user_data['first_name'],
        last_name=context.user_data['last_name'],
        email=context.user_data['email'],
        phone=phone
    )
    
    if result['success']:
        verification_code = result['verification_code']
        
        keyboard = [
            [InlineKeyboardButton("🌐 افتح الموقع للإكمال", url=f"https://your-website.com?code={verification_code}")],
            [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            text=f"✅ تم إنشاء حسابك بنجاح!\n\n"
                 f"👤 الاسم: {context.user_data['first_name']} {context.user_data['last_name']}\n"
                 f"📧 البريد: {context.user_data['email']}\n"
                 f"📱 الهاتف: {phone}\n\n"
                 f"🔑 كود التحقق الخاص بك:\n`{verification_code}`\n\n"
                 f"⚠️ احفظ هذا الكود! ستحتاجه على الموقع.\n\n"
                 f"🎯 الخطوة التالية:\n"
                 f"افتح الموقع وأدخل كود التحقق لإكمال التسجيل وإضافة محفظتك الرقمية.",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            f"❌ {result['message']}\n\n"
            f"يرجى التواصل مع الدعم الفني."
        )
    
    # مسح البيانات
    context.user_data.clear()
    
    return ConversationHandler.END

async def cancel_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """إلغاء عملية التسجيل"""
    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text("❌ تم إلغاء عملية التسجيل.")
    else:
        await update.message.reply_text("❌ تم إلغاء عملية التسجيل.")
    
    context.user_data.clear()
    return ConversationHandler.END

# ==================== Account Management ====================

async def show_account_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض معلومات الحساب"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    user = db.get_user_by_telegram_id(user_id)
    
    if not user:
        keyboard = [[InlineKeyboardButton("📝 إنشاء حساب", callback_data="start_registration")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text="❌ ليس لديك حساب مسجل.\n\n"
                 "قم بإنشاء حساب للاستفادة من جميع ميزات المنصة!",
            reply_markup=reply_markup
        )
        return
    
    # الحصول على المعاملات الأخيرة
    transactions = db.get_user_transactions(user['id'], limit=5)
    
    trans_text = ""
    if transactions:
        trans_text = "\n\n📊 آخر المعاملات:\n"
        for trans in transactions[:5]:
            trans_text += f"• {trans['type']}: ${trans['amount']:.2f}\n"
    
    keyboard = [
        [InlineKeyboardButton("💰 الإيداع", callback_data="start_deposit"),
         InlineKeyboardButton("💸 السحب", callback_data="start_withdrawal")],
        [InlineKeyboardButton("📜 سجل المعاملات", callback_data="view_transactions")],
        [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=f"👤 معلومات الحساب\n"
             f"━━━━━━━━━━━━━━━\n"
             f"👤 الاسم: {user['first_name']} {user['last_name']}\n"
             f"📧 البريد: {user['email']}\n"
             f"📱 الهاتف: {user['phone']}\n"
             f"🔑 كود التحقق: `{user['verification_code']}`\n\n"
             f"💰 الرصيد الحالي: ${user['balance']:.2f}\n"
             f"📅 تاريخ التسجيل: {user['created_at'][:10]}"
             f"{trans_text}",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def show_transactions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض سجل المعاملات"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    user = db.get_user_by_telegram_id(user_id)
    
    if not user:
        await query.edit_message_text("❌ ليس لديك حساب مسجل.")
        return
    
    transactions = db.get_user_transactions(user['id'], limit=20)
    
    if not transactions:
        text = "📜 سجل المعاملات\n━━━━━━━━━━━━━━━\n\nلا توجد معاملات بعد."
    else:
        text = f"📜 سجل المعاملات\n━━━━━━━━━━━━━━━\n\n"
        for trans in transactions:
            emoji = "📥" if trans['type'] == 'deposit' else "📤" if trans['type'] == 'withdrawal' else "💱"
            text += f"{emoji} {trans['type']}: ${trans['amount']:.2f}\n"
            text += f"   📅 {trans['created_at'][:16]}\n"
            if trans['description']:
                text += f"   📝 {trans['description']}\n"
            text += "\n"
    
    keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="account_info")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=text, reply_markup=reply_markup)

# ==================== Deposit Flow ====================

async def start_deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """بدء عملية الإيداع"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    user = db.get_user_by_telegram_id(user_id)
    
    if not user:
        await query.edit_message_text("❌ يجب إنشاء حساب أولاً!")
        return
    
    # الحصول على محافظ الشركة
    company_wallets = db.get_company_wallets()
    
    text = "💰 الإيداع\n━━━━━━━━━━━━━━━\n\n"
    text += "اختر المحفظة التي تريد الإيداع بها:\n\n"
    
    keyboard = []
    for wallet in company_wallets:
        keyboard.append([InlineKeyboardButton(
            f"{wallet['wallet_name']}", 
            callback_data=f"deposit_wallet_{wallet['id']}"
        )])
    
    keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="account_info")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=text, reply_markup=reply_markup)

async def show_deposit_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض عنوان المحفظة للإيداع"""
    query = update.callback_query
    await query.answer()
    
    wallet_id = int(query.data.split('_')[2])
    
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM company_wallets WHERE id = ?', (wallet_id,))
    wallet = cursor.fetchone()
    conn.close()
    
    if not wallet:
        await query.edit_message_text("❌ خطأ في المحفظة")
        return
    
    wallet = dict(wallet)
    
    text = f"💰 الإيداع عبر {wallet['wallet_name']}\n"
    text += "━━━━━━━━━━━━━━━\n\n"
    text += f"📍 عنوان المحفظة:\n`{wallet['wallet_address']}`\n\n"
    text += "⚠️ تعليمات مهمة:\n"
    text += "1. احفظ عنوان المحفظة أعلاه\n"
    text += "2. قم بتحويل المبلغ المطلوب\n"
    text += "3. التقط صورة لإثبات التحويل\n"
    text += "4. افتح الموقع لإكمال طلب الإيداع\n\n"
    text += "🌐 لإكمال الطلب، افتح الموقع وأرفق صورة الإيداع."
    
    keyboard = [
        [InlineKeyboardButton("🌐 فتح الموقع", url="https://your-website.com/deposit")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="start_deposit")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='Markdown')

# ==================== Withdrawal Flow ====================

async def start_withdrawal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """بدء عملية السحب"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    user = db.get_user_by_telegram_id(user_id)
    
    if not user:
        await query.edit_message_text("❌ يجب إنشاء حساب أولاً!")
        return
    
    text = f"💸 طلب السحب\n━━━━━━━━━━━━━━━\n\n"
    text += f"💰 رصيدك الحالي: ${user['balance']:.2f}\n\n"
    text += "⚠️ ملاحظات:\n"
    text += "• الحد الأدنى للسحب: $10\n"
    text += "• معالجة الطلبات خلال 24 ساعة\n\n"
    text += "🌐 لإنشاء طلب سحب، افتح الموقع وأكمل البيانات المطلوبة."
    
    keyboard = [
        [InlineKeyboardButton("🌐 فتح الموقع", url="https://your-website.com/withdrawal")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="account_info")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=text, reply_markup=reply_markup)
