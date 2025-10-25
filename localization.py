# localization.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

# Add all bot text here for easy translation
LANGUAGES = {
    'ar': {
        # General
        "welcome": "أهلاً بك {user_mention} في *BTC-CloudX*!\n\nاستخدم الأزرار أدناه للبدء.",
        "open_app_button": "🚀 فتح التطبيق الكامل",
        "bot_menu_button": "⚙️ استخدام البوت مباشرة",
        "main_menu_title": "القائمة الرئيسية للبوت. اختر أحد الخيارات:",
        "back_to_main_menu": "🔙 العودة للقائمة الرئيسية",
        "price": "السعر",
        "hashrate": "القوة التعدينية",
        "annual_profit": "الربح السنوي الصافي",
        "device_source": "الجهاز المصدر",
        "daily_profit": "الربح اليومي الصافي",
        "semi_annual_bonus": "عائد نصف سنوي",

        # Main Menu Buttons
        "featured_plans": "📊 الخطط المميزة",
        "how_it_works": "⚙️ طبيعة عملنا",
        "faq": "❓ أسئلة شائعة",
        "privacy_policy": "📄 الخصوصية وسياسة العمل",
        "get_subscription_code": "💳 الحصول على كود اشتراك",
        "contact_us": "📞 تواصل معنا",
        "language": "🌐 اللغة",

        # Sections Content
        "featured_plans_title": "الخطط الاستثمارية المميزة",
        "faq_title": "اختر سؤالاً لعرض إجابته:",
        "back_to_faq_menu": "🔙 العودة لقائمة الأسئلة",

        # Subscription Code
        "subscription_code_text": "✅ تم إنشاء كود الاشتراك الخاص بك بنجاح!\n\nالكود الخاص بك هو:\n`{user_code}`\n\nاحتفظ بهذا الكود، فهو معرّفك الدائم معنا.",

        # Contact Us
        "contact_us_title": "📞 تواصل معنا",
        "contact_us_content": "فريقنا جاهز للإجابة على جميع استفساراتك. يمكنك التواصل معنا عبر:",
        "join_channel_button": "📢 قناتنا على تليجرام",
        "contact_support_button": "💬 التحدث إلى الدعم الفني",
        "contact_me_button": "💬 تواصل معي",

        # Language
        "select_language": "اختر لغتك المفضلة:",
        "language_updated": "✅ تم تحديث اللغة إلى العربية.",

        # Web App Data Handler
        "custom_plan_result_title": "✅ تم استلام تفاصيل خطتك المخصصة",
        "investment_amount": "مبلغ الاستثمار",
        "contract_duration": "مدة العقد",
        "calculated_hashrate": "القوة التعدينية المحسوبة",
        "total_profit_estimate": "إجمالي الربح الصافي التقديري",
        "plan_request_prompt": "لطلب هذه الخطة أو لمناقشة التفاصيل، يرجى التواصل مع الدعم الفني.",
        "close_message_button": "✖️ إغلاق",
        
        # Plan Categories
        "monthly_plans": "📅 الخطط الشهرية",
        "quarterly_plans": "📅 الخطط ربع السنوية",
        "annually_plans": "📅 الخطط السنوية",
        "plans_title": "📊 خطط الاستثمار",
        "plans_intro": "اختر نوع الخطة التي تناسبك:",
    },
    'en': {
        # General
        "welcome": "🎉 Welcome {user_mention} to *BTC-CloudX*!\n\n🚀 Your gateway to secure cloud mining investment. Use the buttons below to get started!",
        "open_app_button": "🚀 Open Full Application",
        "bot_menu_button": "⚙️ Use Bot Interface",
        "main_menu_title": "🏠 Main Menu - Choose your option:",
        "back_to_main_menu": "🔙 Back to Main Menu",
        "price": "💰 Price",
        "hashrate": "⚡ Hash Rate",
        "annual_profit": "📈 Net Annual Profit",
        "device_source": "🖥️ Mining Device",
        "daily_profit": "💵 Daily Net Profit",
        "semi_annual_bonus": "🎁 Semi-Annual Bonus",

        # Main Menu Buttons
        "featured_plans": "📊 Premium Investment Plans",
        "how_it_works": "⚙️ How Our Service Works",
        "faq": "❓ Frequently Asked Questions",
        "privacy_policy": "📄 Privacy Policy & Terms",
        "get_subscription_code": "💳 Generate Subscription Code",
        "contact_us": "📞 Contact Support Team",
        "language": "🌐 Change Language",

        # Sections Content
        "featured_plans_title": "🌟 Premium Investment Plans",
        "faq_title": "❓ Select a question to view the answer:",
        "back_to_faq_menu": "🔙 Return to FAQ List",

        # Subscription Code
        "subscription_code_text": "✅ Success! Your subscription code has been generated!\n\n🔑 Your unique code is:\n`{user_code}`\n\n💡 Please save this code - it's your permanent identifier with BTC-CloudX!",

        # Contact Us
        "contact_us_title": "📞 Contact Us",
        "contact_us_content": "💬 Our support team is available 24/7 to help you! Contact us through:",
        "join_channel_button": "📢 Join Our Telegram Channel",
        "contact_support_button": "💬 Chat with Support Agent",
        "contact_me_button": "💬 Contact Me",

        # Language
        "select_language": "🌐 Choose your preferred language:",
        "language_updated": "✅ Language successfully updated to English!",

        # Web App Data Handler
        "custom_plan_result_title": "✅ Custom Plan Details Received Successfully!",
        "investment_amount": "💰 Investment Amount",
        "contract_duration": "📅 Contract Duration",
        "calculated_hashrate": "⚡ Calculated Hash Rate",
        "total_profit_estimate": "📊 Estimated Total Net Profit",
        "plan_request_prompt": "🤝 To proceed with this plan or discuss details, please contact our technical support team.",
        "close_message_button": "✖️ Close Message",
        
        # Plan Categories
        "monthly_plans": "📅 Monthly Plans",
        "quarterly_plans": "📅 Quarterly Plans",
        "annually_plans": "📅 Annual Plans",
        "plans_title": "📊 Investment Plans",
        "plans_intro": "Choose the plan type that suits you:",
    },
    'zh': {
        # General
        "welcome": "🎉 欢迎 {user_mention} 来到 *BTC-CloudX*！\n\n🚀 您的安全云挖矿投资门户。请使用下面的按钮开始您的投资之旅！",
        "open_app_button": "🚀 打开完整应用程序",
        "bot_menu_button": "⚙️ 使用机器人界面",
        "main_menu_title": "🏠 主菜单 - 请选择您的选项：",
        "back_to_main_menu": "🔙 返回主菜单",
        "price": "💰 价格",
        "hashrate": "⚡ 算力",
        "annual_profit": "📈 年净利润",
        "device_source": "🖥️ 挖矿设备",
        "daily_profit": "💵 日净利润",
        "semi_annual_bonus": "🎁 半年奖金",

        # Main Menu Buttons
        "featured_plans": "📊 高级投资计划",
        "how_it_works": "⚙️ 我们的服务原理",
        "faq": "❓ 常见问题解答",
        "privacy_policy": "📄 隐私政策和条款",
        "get_subscription_code": "💳 生成订阅代码",
        "contact_us": "📞 联系支持团队",
        "language": "🌐 更改语言",

        # Sections Content
        "featured_plans_title": "🌟 高级投资计划",
        "faq_title": "❓ 选择一个问题查看答案：",
        "back_to_faq_menu": "🔙 返回常见问题列表",

        # Subscription Code
        "subscription_code_text": "✅ 成功！您的订阅代码已生成！\n\n🔑 您的唯一代码是：\n`{user_code}`\n\n💡 请保存此代码 - 这是您在BTC-CloudX的永久标识符！",

        # Contact Us
        "contact_us_title": "📞 联系我们",
        "contact_us_content": "💬 我们的支持团队24/7随时为您提供帮助！通过以下方式联系我们：",
        "join_channel_button": "📢 加入我们的Telegram频道",
        "contact_support_button": "💬 与支持代理聊天",
        "contact_me_button": "💬 联系我",

        # Language
        "select_language": "🌐 选择您的首选语言：",
        "language_updated": "✅ 语言已成功更新为中文！",

        # Web App Data Handler
        "custom_plan_result_title": "✅ 自定义计划详情接收成功！",
        "investment_amount": "💰 投资金额",
        "contract_duration": "📅 合同期限",
        "calculated_hashrate": "⚡ 计算算力",
        "total_profit_estimate": "📊 预计总净利润",
        "plan_request_prompt": "🤝 要继续此计划或讨论详情，请联系我们的技术支持团队。",
        "close_message_button": "✖️ 关闭消息",
        
        # Plan Categories
        "monthly_plans": "📅 月度计划",
        "quarterly_plans": "📅 季度计划",
        "annually_plans": "📅 年度计划",
        "plans_title": "📊 投资计划",
        "plans_intro": "选择适合您的计划类型：",
    }
}

def get_text(key: str, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Fetches a text string in the user's selected language."""
    lang = context.user_data.get('lang', 'ar')
    # Fallback to English if key not in selected language, then to the key name itself as a last resort.
    return LANGUAGES.get(lang, {}).get(key, LANGUAGES.get('en', {}).get(key, f"_{key}_"))

def build_language_menu(context: ContextTypes.DEFAULT_TYPE) -> InlineKeyboardMarkup:
    """Builds the language selection menu."""
    keyboard = [
        [
            InlineKeyboardButton("🇸🇦 العربية", callback_data="set_lang_ar"),
            InlineKeyboardButton("🇬🇧 English", callback_data="set_lang_en"),
            InlineKeyboardButton("🇨🇳 中文", callback_data="set_lang_zh"),
        ],
        [InlineKeyboardButton(get_text("back_to_main_menu", context), callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def set_language_and_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sets the user's language and shows a confirmation."""
    query = update.callback_query
    await query.answer() # Acknowledge the button press first
    
    lang_code = query.data.split('set_lang_')[1]
    context.user_data['lang'] = lang_code
    
    # Use a direct lookup to ensure the confirmation is in the newly selected language
    confirmation_text = LANGUAGES.get(lang_code, {}).get("language_updated", "Language updated.")
    await query.answer(text=confirmation_text, show_alert=True)
    
    # Redisplay the main menu with the new language
    from helpers import build_main_menu # Avoid circular import
    await query.edit_message_text(
        text=get_text('main_menu_title', context),
        reply_markup=build_main_menu(context),
        parse_mode='Markdown'
    )
