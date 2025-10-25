# admin_panel.py
"""
لوحة التحكم الخاصة بالأدمن لإدارة المستخدمين والطلبات
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import db
import os

# قائمة معرفات الأدمن (يمكن أخذها من .env)
ADMIN_IDS = [int(x) for x in os.getenv('ADMIN_TELEGRAM_IDS', '').split(',') if x.strip()]

def is_admin(telegram_id: int) -> bool:
    """التحقق من كون المستخدم أدمن"""
    return telegram_id in ADMIN_IDS

# ==================== Admin Main Menu ====================

async def show_admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض لوحة التحكم الرئيسية للأدمن"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await query.edit_message_text("❌ ليس لديك صلاحية الوصول لهذه اللوحة.")
        return
    
    # الحصول على الإحصائيات
    stats = db.get_platform_stats()
    
    text = "🔐 لوحة التحكم - Admin Panel\n"
    text += "━━━━━━━━━━━━━━━━━━━━━\n\n"
    text += "📊 إحصائيات المنصة:\n\n"
    text += f"👥 إجمالي المستخدمين: {stats['total_users']}\n"
    text += f"💰 إجمالي الإيداعات: ${stats['total_deposits']:.2f}\n"
    text += f"💸 إجمالي السحوبات: ${stats['total_withdrawals']:.2f}\n"
    text += f"🏦 الخزنة: ${stats['treasury']:.2f}\n\n"
    text += "اختر القسم المطلوب:"
    
    keyboard = [
        [InlineKeyboardButton("👥 إدارة المستخدمين", callback_data="admin_users")],
        [InlineKeyboardButton("💰 طلبات الإيداع", callback_data="admin_deposits"),
         InlineKeyboardButton("💸 طلبات السحب", callback_data="admin_withdrawals")],
        [InlineKeyboardButton("📊 إحصائيات تفصيلية", callback_data="admin_stats")],
        [InlineKeyboardButton("⚙️ الإعدادات", callback_data="admin_settings")],
        [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=text, reply_markup=reply_markup)

# ==================== User Management ====================

async def admin_show_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض قائمة المستخدمين"""
    query = update.callback_query
    await query.answer()
    
    if not is_admin(update.effective_user.id):
        await query.edit_message_text("❌ ليس لديك صلاحية الوصول.")
        return
    
    users = db.get_all_users(limit=20)
    
    text = "👥 قائمة المستخدمين\n━━━━━━━━━━━━━━━\n\n"
    
    if not users:
        text += "لا يوجد مستخدمين مسجلين بعد."
    else:
        for user in users:
            text += f"👤 {user['first_name']} {user['last_name']}\n"
            text += f"   📧 {user['email']}\n"
            text += f"   🔑 {user['verification_code']}\n"
            text += f"   💰 ${user['balance']:.2f}\n"
            text += f"   📅 {user['created_at'][:10]}\n\n"
    
    keyboard = [
        [InlineKeyboardButton("🔍 بحث عن مستخدم", callback_data="admin_search_user")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="admin_panel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # تقسيم النص إذا كان طويلاً جداً
    if len(text) > 4000:
        text = text[:3900] + "\n\n... (عرض جزئي)"
    
    await query.edit_message_text(text=text, reply_markup=reply_markup)

# ==================== Deposit Management ====================

async def admin_show_deposits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض طلبات الإيداع المعلقة"""
    query = update.callback_query
    await query.answer()
    
    if not is_admin(update.effective_user.id):
        await query.edit_message_text("❌ ليس لديك صلاحية الوصول.")
        return
    
    deposits = db.get_pending_deposits()
    
    text = "💰 طلبات الإيداع المعلقة\n━━━━━━━━━━━━━━━━━━━\n\n"
    
    if not deposits:
        text += "✅ لا توجد طلبات إيداع معلقة."
        keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="admin_panel")]]
    else:
        for dep in deposits[:10]:  # عرض أول 10 طلبات فقط
            text += f"📋 طلب #{dep['request_number']}\n"
            text += f"👤 {dep['first_name']} {dep['last_name']}\n"
            text += f"🔑 {dep['verification_code']}\n"
            text += f"💵 المبلغ: ${dep['amount']:.2f}\n"
            text += f"💳 المحفظة: {dep['wallet_type']}\n"
            text += f"📅 {dep['created_at'][:16]}\n"
            text += "━━━━━━━━━━━━━━━\n\n"
        
        keyboard = []
        # إضافة أزرار الموافقة/الرفض لأول 5 طلبات
        for dep in deposits[:5]:
            keyboard.append([
                InlineKeyboardButton(
                    f"✅ موافقة #{dep['request_number'][-4:]}", 
                    callback_data=f"approve_dep_{dep['id']}"
                ),
                InlineKeyboardButton(
                    f"❌ رفض #{dep['request_number'][-4:]}", 
                    callback_data=f"reject_dep_{dep['id']}"
                )
            ])
        
        keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="admin_panel")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if len(text) > 4000:
        text = text[:3900] + "\n\n... (عرض جزئي)"
    
    await query.edit_message_text(text=text, reply_markup=reply_markup)

async def admin_approve_deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """الموافقة على طلب إيداع"""
    query = update.callback_query
    await query.answer()
    
    if not is_admin(update.effective_user.id):
        await query.edit_message_text("❌ ليس لديك صلاحية الوصول.")
        return
    
    deposit_id = int(query.data.split('_')[2])
    admin_id = update.effective_user.id
    
    # الموافقة على الطلب
    result = db.approve_deposit(deposit_id, admin_id)
    
    if result:
        await query.answer("✅ تمت الموافقة على الطلب", show_alert=True)
        # إعادة عرض قائمة الإيداعات
        await admin_show_deposits(update, context)
    else:
        await query.answer("❌ فشلت العملية", show_alert=True)

async def admin_reject_deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """رفض طلب إيداع"""
    query = update.callback_query
    await query.answer()
    
    if not is_admin(update.effective_user.id):
        await query.edit_message_text("❌ ليس لديك صلاحية الوصول.")
        return
    
    deposit_id = int(query.data.split('_')[2])
    
    # تحديث حالة الطلب إلى مرفوض
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE deposit_requests 
        SET status = 'rejected', processed_at = CURRENT_TIMESTAMP, processed_by = ?
        WHERE id = ?
    ''', (update.effective_user.id, deposit_id))
    conn.commit()
    conn.close()
    
    await query.answer("❌ تم رفض الطلب", show_alert=True)
    await admin_show_deposits(update, context)

# ==================== Withdrawal Management ====================

async def admin_show_withdrawals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض طلبات السحب المعلقة"""
    query = update.callback_query
    await query.answer()
    
    if not is_admin(update.effective_user.id):
        await query.edit_message_text("❌ ليس لديك صلاحية الوصول.")
        return
    
    withdrawals = db.get_pending_withdrawals()
    
    text = "💸 طلبات السحب المعلقة\n━━━━━━━━━━━━━━━━━━━\n\n"
    
    if not withdrawals:
        text += "✅ لا توجد طلبات سحب معلقة."
        keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="admin_panel")]]
    else:
        for wth in withdrawals[:10]:
            text += f"📋 طلب #{wth['request_number']}\n"
            text += f"👤 {wth['first_name']} {wth['last_name']}\n"
            text += f"🔑 {wth['verification_code']}\n"
            text += f"💵 المبلغ: ${wth['amount']:.2f}\n"
            text += f"💳 المحفظة: {wth['wallet_type']}\n"
            text += f"📍 العنوان: `{wth['wallet_address']}`\n"
            text += f"📅 {wth['created_at'][:16]}\n"
            text += "━━━━━━━━━━━━━━━\n\n"
        
        keyboard = []
        for wth in withdrawals[:5]:
            keyboard.append([
                InlineKeyboardButton(
                    f"✅ تم التحويل #{wth['request_number'][-4:]}", 
                    callback_data=f"approve_wth_{wth['id']}"
                ),
                InlineKeyboardButton(
                    f"❌ رفض #{wth['request_number'][-4:]}", 
                    callback_data=f"reject_wth_{wth['id']}"
                )
            ])
        
        keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="admin_panel")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if len(text) > 4000:
        text = text[:3900] + "\n\n... (عرض جزئي)"
    
    await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='Markdown')

async def admin_approve_withdrawal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """الموافقة على طلب سحب (تأكيد التحويل)"""
    query = update.callback_query
    await query.answer()
    
    if not is_admin(update.effective_user.id):
        await query.edit_message_text("❌ ليس لديك صلاحية الوصول.")
        return
    
    withdrawal_id = int(query.data.split('_')[2])
    admin_id = update.effective_user.id
    
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # الحصول على معلومات الطلب
    cursor.execute('SELECT user_id, amount FROM withdrawal_requests WHERE id = ?', (withdrawal_id,))
    request = cursor.fetchone()
    
    if request:
        user_id, amount = request
        
        # خصم المبلغ من رصيد المستخدم
        cursor.execute('UPDATE users SET balance = balance - ? WHERE id = ?', (amount, user_id))
        
        # تحديث حالة الطلب
        cursor.execute('''
            UPDATE withdrawal_requests 
            SET status = 'approved', processed_at = CURRENT_TIMESTAMP, processed_by = ?
            WHERE id = ?
        ''', (admin_id, withdrawal_id))
        
        # تسجيل المعاملة
        cursor.execute('''
            INSERT INTO transactions (user_id, type, amount, description)
            VALUES (?, 'withdrawal', ?, 'سحب تمت الموافقة عليه')
        ''', (user_id, amount))
        
        conn.commit()
        await query.answer("✅ تم تأكيد التحويل", show_alert=True)
    else:
        await query.answer("❌ الطلب غير موجود", show_alert=True)
    
    conn.close()
    await admin_show_withdrawals(update, context)

async def admin_reject_withdrawal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """رفض طلب سحب"""
    query = update.callback_query
    await query.answer()
    
    if not is_admin(update.effective_user.id):
        await query.edit_message_text("❌ ليس لديك صلاحية الوصول.")
        return
    
    withdrawal_id = int(query.data.split('_')[2])
    
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE withdrawal_requests 
        SET status = 'rejected', processed_at = CURRENT_TIMESTAMP, processed_by = ?
        WHERE id = ?
    ''', (update.effective_user.id, withdrawal_id))
    conn.commit()
    conn.close()
    
    await query.answer("❌ تم رفض الطلب", show_alert=True)
    await admin_show_withdrawals(update, context)

# ==================== Statistics ====================

async def admin_show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض إحصائيات تفصيلية"""
    query = update.callback_query
    await query.answer()
    
    if not is_admin(update.effective_user.id):
        await query.edit_message_text("❌ ليس لديك صلاحية الوصول.")
        return
    
    stats = db.get_platform_stats()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # إحصائيات إضافية
    cursor.execute('SELECT COUNT(*) FROM deposit_requests WHERE status = "pending"')
    pending_deposits = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM withdrawal_requests WHERE status = "pending"')
    pending_withdrawals = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM users WHERE created_at >= date("now", "-7 days")')
    new_users_week = cursor.fetchone()[0]
    
    conn.close()
    
    text = "📊 إحصائيات تفصيلية\n"
    text += "━━━━━━━━━━━━━━━━━━━━━\n\n"
    text += f"👥 إجمالي المستخدمين: {stats['total_users']}\n"
    text += f"👤 مستخدمين جدد (7 أيام): {new_users_week}\n\n"
    text += f"💰 إجمالي الإيداعات: ${stats['total_deposits']:.2f}\n"
    text += f"⏳ طلبات إيداع معلقة: {pending_deposits}\n\n"
    text += f"💸 إجمالي السحوبات: ${stats['total_withdrawals']:.2f}\n"
    text += f"⏳ طلبات سحب معلقة: {pending_withdrawals}\n\n"
    text += f"🏦 الخزنة الحالية: ${stats['treasury']:.2f}\n"
    
    keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="admin_panel")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=text, reply_markup=reply_markup)

# ==================== Settings ====================

async def admin_show_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض إعدادات المنصة"""
    query = update.callback_query
    await query.answer()
    
    if not is_admin(update.effective_user.id):
        await query.edit_message_text("❌ ليس لديك صلاحية الوصول.")
        return
    
    # الحصول على محافظ الشركة
    wallets = db.get_company_wallets()
    
    text = "⚙️ إعدادات المنصة\n"
    text += "━━━━━━━━━━━━━━━━━━━━━\n\n"
    text += "💳 المحافظ الرقمية:\n\n"
    
    for wallet in wallets:
        status = "✅" if wallet['is_active'] else "❌"
        text += f"{status} {wallet['wallet_name']}\n"
        text += f"   `{wallet['wallet_address']}`\n\n"
    
    keyboard = [
        [InlineKeyboardButton("💳 إدارة المحافظ", callback_data="admin_manage_wallets")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="admin_panel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='Markdown')
