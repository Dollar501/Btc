# 🚀 دليل البدء السريع - BTC-CloudX

## ⚡ التشغيل السريع (5 دقائق)

### 1️⃣ الإعداد الأولي

```bash
# انسخ ملف البيئة
cp .env.example .env

# ثبّت المكتبات
pip install -r requirements.txt
```

### 2️⃣ تعديل ملف `.env`

افتح `.env` وعدّل القيم التالية:

```env
# توكن البوت من @BotFather
TELEGRAM_BOT_TOKEN=7123456789:AAHxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# معرف telegram الخاص بك (اعرفه من @userinfobot)
ADMIN_TELEGRAM_IDS=123456789

# JWT Secret (أي نص عشوائي طويل)
JWT_SECRET_KEY=my_super_secret_key_12345678901234567890

# رابط الموقع (لو عندك)
WEB_APP_URL=https://your-website.com
```

### 3️⃣ تشغيل البوت

```bash
python main.py
```

✅ **تم! البوت شغال الآن**

---

## 📱 اختبار البوت

1. **افتح البوت** على Telegram
2. **أرسل** `/start`
3. **اضغط** "📝 إنشاء حساب"
4. **املأ البيانات**:
   - الاسم الأول
   - اسم العائلة
   - البريد الإلكتروني
   - رقم الهاتف
5. **احصل على كود التحقق** (BTC-X-77-XXXXX)

---

## 🔐 الوصول للوحة Admin

1. تأكد أن `telegram_id` الخاص بك في `ADMIN_TELEGRAM_IDS`
2. افتح البوت
3. سترى زر "🔐 لوحة التحكم"

---

## 💰 اختبار الإيداع

1. اضغط "👤 حسابي"
2. اضغط "💰 الإيداع"
3. اختر المحفظة
4. انسخ العنوان
5. حوّل المبلغ (للاختبار: استخدم محفظة testnet)
6. التقط صورة
7. ارفع الصورة على صفحة الحساب

---

## 🎯 تخصيص المحافظ

### تحديث عناوين المحافظ الحقيقية:

افتح `database.py` السطر **140** وعدّل:

```python
default_wallets = [
    ('USDT_TRC20', 'TRxxxxYourRealWalletAddressxxxx', 'USDT (TRC20)'),
    ('USDT_ERC20', '0xxxxxYourRealWalletAddressxxxx', 'USDT (ERC20)'),
    ('Bitcoin', 'bc1qxxxYourBTCAddressxxxxxx', 'Bitcoin (BTC)'),
    ('Ethereum', '0xxxxxYourETHAddressxxxxxxx', 'Ethereum (ETH)'),
    ('BNB_BSC', '0xxxxxYourBNBAddressxxxxxxx', 'BNB (BSC)')
]
```

بعدها احذف ملف `btc_cloudx.db` وشغّل البوت من جديد.

---

## 📂 بنية المشروع

```
BTC-CloudX-main/
├── main.py              # البوت الرئيسي ✅
├── database.py          # قاعدة البيانات ✅
├── api.py               # REST API ✅
├── auth_handlers.py     # التسجيل والحسابات ✅
├── admin_panel.py       # لوحة Admin ✅
├── account.html         # صفحة الحساب ✅
├── account.js           # JavaScript ✅
├── btc_cloudx.db        # قاعدة البيانات (تُنشأ تلقائياً)
└── uploads/             # صور الإيداعات
```

---

## 🔧 المميزات المتاحة

### ✅ للمستخدم:
- [x] إنشاء حساب مع كود تحقق فريد
- [x] عرض الرصيد والمعلومات
- [x] طلبات إيداع مع صور
- [x] طلبات سحب
- [x] سجل المعاملات

### ✅ للأدمن:
- [x] عرض جميع المستخدمين
- [x] الموافقة/رفض الإيداعات
- [x] معالجة السحوبات
- [x] إحصائيات شاملة
- [x] إدارة المحافظ

---

## 🌐 فتح صفحة الحساب

افتح في المتصفح:
```
file:///c:/xampp/htdocs/BTC-CloudX-main/account.html
```

أو شغّل API محلياً:
```bash
python api.py
```

ثم افتح: `http://localhost:5000`

---

## ❓ المشاكل الشائعة

### البوت لا يشتغل؟
- تأكد من `TELEGRAM_BOT_TOKEN` صحيح
- تأكد من تثبيت جميع المكتبات

### لا أرى زر Admin؟
- تأكد من `telegram_id` في `ADMIN_TELEGRAM_IDS`
- اعرف `telegram_id` من @userinfobot

### API لا يعمل؟
- تأكد من تشغيل `python api.py`
- غيّر `API_BASE_URL` في `account.js`

---

## 📞 الدعم

اقرأ الدليل الشامل: `SETUP_GUIDE.md`

---

**تم! الآن لديك نظام كامل للتعدين السحابي 🚀**
