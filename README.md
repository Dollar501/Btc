# 🚀 BTC-CloudX - نظام شامل لإدارة الاستثمار في التعدين السحابي

## 🌟 نظرة عامة

BTC-CloudX هي منصة متكاملة لإدارة الاستثمار في التعدين السحابي للبيتكوين، تتضمن:
- 🤖 **بوت Telegram** متطور مع نظام حسابات كامل
- 🌐 **تطبيق ويب** حديث مع واجهة تفاعلية
- 💼 **لوحة تحكم Admin** لإدارة المنصة
- 💰 **نظام إيداع وسحب** متكامل
- 🔐 **REST API** للتواصل الآمن
- 📊 **قاعدة بيانات** منظمة لتتبع كل العمليات

**الإصدار:** 2.0.0 (محدّث بالكامل)  
**اللغات المدعومة:** العربية، الإنجليزية، الصينية

## ✨ المميزات الجديدة في النسخة 2.0

### 👥 نظام إدارة الحسابات
- ✅ **تسجيل مستخدمين** عبر البوت مع بيانات كاملة
- ✅ **كود تحقق فريد** لكل مستخدم (BTC-X-77-XXXXX)
- ✅ **ملف شخصي** مع رصيد ومعلومات كاملة
- ✅ **سجل معاملات** شامل لكل مستخدم

### 💰 نظام الإيداع والسحب
- ✅ **5 محافظ رقمية**: USDT (TRC20/ERC20), BTC, ETH, BNB
- ✅ **طلبات إيداع** مع رفع صور الإثبات
- ✅ **طلبات سحب** إلى محافظ المستخدمين
- ✅ **تتبع حالة الطلبات**: معلقة/موافق/مرفوض

### 🔐 لوحة تحكم Admin
- ✅ **إدارة المستخدمين**: عرض وتعديل جميع المستخدمين
- ✅ **الموافقة على الإيداعات**: مراجعة ومعالجة الطلبات
- ✅ **معالجة السحوبات**: تأكيد وتحويل الأموال
- ✅ **إحصائيات شاملة**: الخزنة، الإيداعات، السحوبات
- ✅ **إدارة المحافظ**: تحديث عناوين محافظ الشركة

### 🌐 REST API
- ✅ **مصادقة آمنة** بـ JWT Tokens
- ✅ **Endpoints كاملة** لجميع العمليات
- ✅ **CORS Support** للتكامل مع الموقع
- ✅ **رفع ملفات** للصور والإثباتات

### 📊 قاعدة البيانات
- ✅ **SQLite محلية** سهلة النشر
- ✅ **8 جداول منظمة**: مستخدمين، محافظ، معاملات، إيداعات، سحوبات
- ✅ **Foreign Keys** لربط البيانات
- ✅ **Indexes** لتحسين الأداء

## 📁 هيكل المشروع المُحدث

```
BTC-CloudX-main/
├── 🤖 البوت والخادم
│   ├── main.py                 # البوت الرئيسي + Flask server
│   ├── database.py             # قاعدة البيانات الكاملة ⭐ جديد
│   ├── api.py                  # REST API ⭐ جديد
│   ├── auth_handlers.py        # نظام التسجيل والحسابات ⭐ جديد
│   ├── admin_panel.py          # لوحة تحكم Admin ⭐ جديد
│   ├── localization.py         # الترجمات
│   ├── data_store.py           # بيانات الخطط والأجهزة
│   ├── helpers.py              # دوال مساعدة (محدثة)
│   └── devices.py              # إدارة الأجهزة
│
├── 🌐 الموقع
│   ├── index.html              # الصفحة الرئيسية
│   ├── account.html            # صفحة الحساب ⭐ جديد
│   ├── account.js              # JavaScript للحساب ⭐ جديد
│   ├── script.js               # JavaScript الرئيسي
│   ├── languages.js            # ملف اللغات
│   └── styles.css              # التصميم
│
├── 📊 البيانات
│   ├── btc_cloudx.db           # قاعدة البيانات ⭐ (تُنشأ تلقائياً)
│   └── uploads/                # مجلد صور الإيداعات ⭐
│       └── proofs/
│
├── ⚙️ الإعدادات
│   ├── .env                    # المتغيرات البيئية
│   ├── .env.example            # قالب البيئة (محدث)
│   ├── requirements.txt        # المكتبات (محدث)
│   ├── runtime.txt             # إصدار Python
│   ├── Procfile                # للنشر
│   └── render.yaml             # إعدادات Render
│
└── 📖 التوثيق
    ├── README.md               # هذا الملف
    ├── SETUP_GUIDE.md          # دليل الإعداد الشامل ⭐ جديد
    └── QUICK_START.md          # البدء السريع ⭐ جديد
```

## 🚀 Features

### 💻 Web Application
- **Interactive Dashboard**: Modern, responsive interface
- **3D Animations**: Eye-catching Bitcoin animations
- **Investment Calculator**: Custom plan creation tool
- **Hardware Showcase**: Mining equipment information
- **FAQ Section**: Comprehensive help system
- **Multi-Language**: Arabic, English, Chinese support

### 🤖 Telegram Bot
- **Enhanced Messages**: Improved text with emojis and better formatting
- **Multi-Language**: Complete translation support
- **Investment Plans**: Detailed plan information
- **Subscription System**: Unique user codes
- **Support Integration**: Direct contact with support team

## 🛠️ التثبيت والإعداد

### المتطلبات الأساسية
- ✅ Python 3.11+
- ✅ توكن بوت Telegram من @BotFather
- ✅ معرف Telegram للأدمن

### 🚀 البدء السريع (5 دقائق)

**اقرأ دليل البدء السريع الكامل:** [`QUICK_START.md`](QUICK_START.md)

```bash
# 1. انسخ ملف البيئة
cp .env.example .env

# 2. ثبّت المكتبات
pip install -r requirements.txt

# 3. عدّل .env (أضف التوكن ومعرف Admin)

# 4. شغّل البوت
python main.py
```

✅ **تم! البوت شغال الآن**

### 📖 الإعداد الشامل

**اقرأ الدليل الكامل:** [`SETUP_GUIDE.md`](SETUP_GUIDE.md)

يشمل:
- تخصيص المحافظ الرقمية
- إعداد API
- النشر على Render/Heroku
- حل المشاكل الشائعة

## 🌐 Language Support

The platform supports three languages with complete translations:

- **🇸🇦 Arabic (العربية)**: Primary language with RTL support
- **🇺🇸 English**: International users
- **🇨🇳 Chinese (中文)**: Asian market support

### Adding New Languages

1. Add language data to `languages.js`
2. Update `localization.py` with bot translations
3. Add language option to the dropdown menu
4. Update `LANGUAGE_CONFIG` in `script.js`

## 🎯 Investment Plans

### Available Plans
1. **Professional Contract (Pro)** - $200
   - 10 TH/s mining power
   - $0.41 daily profit
   - $148.73 annual profit

2. **Advanced Contract** - $500
   - 26 TH/s mining power
   - $1.06 daily profit
   - $386.71 annual profit

3. **Elite Hydro Contract** - $1000
   - 55 TH/s mining power
   - $2.41 daily profit
   - $878.19 annual profit

### Custom Plans
Users can create custom investment plans with:
- Flexible investment amounts (minimum $1000)
- Contract duration (1-3 years)
- Calculated returns and bonuses

## 🔧 Technical Details

### Frontend Technologies
- **HTML5**: Semantic markup
- **CSS3**: Advanced styling with animations
- **JavaScript ES6+**: Modern JavaScript features
- **Tailwind CSS**: Utility-first CSS framework

### Backend Technologies
- **Python 3.8+**: Core application
- **python-telegram-bot**: Telegram integration
- **Decimal**: Precise financial calculations
- **Environment Variables**: Secure configuration

### Key Features
- **3D Animations**: CSS3 transforms and JavaScript
- **Responsive Design**: Mobile-first approach
- **Multi-Language**: Dynamic content switching
- **Performance Optimized**: Efficient resource loading

## 🔐 Security Features

- **Data Encryption**: Secure user data handling
- **Input Validation**: Protection against malicious input
- **Environment Variables**: Secure configuration management
- **Rate Limiting**: Protection against abuse

## 📱 Mobile Optimization

- **Responsive Layout**: Adapts to all screen sizes
- **Touch-Friendly**: Optimized for mobile interaction
- **Fast Loading**: Optimized for mobile networks
- **Progressive Enhancement**: Works on all devices

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For technical support or questions:
- **Telegram**: Contact through the bot
- **Email**: support@btc-cloudx.com
- **Documentation**: Check this README

## 📄 License

This project is proprietary software. All rights reserved.

## 🔄 Recent Updates

### Version 2.0 (Latest)
- ✅ 3D Bitcoin animation background
- ✅ Enhanced language selector with dropdown
- ✅ Improved text quality (removed underscores, added emojis)
- ✅ Complete translation coverage
- ✅ Modern UI/UX improvements
- ✅ Better mobile responsiveness
- ✅ Performance optimizations

### Upcoming Features
- 🔄 Real-time profit tracking
- 🔄 Advanced analytics dashboard
- 🔄 Payment gateway integration
- 🔄 Push notifications
- 🔄 Advanced security features

---

**BTC-CloudX** - Your gateway to secure cloud mining investment 🚀
