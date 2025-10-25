# 🚀 دليل الإعداد الشامل - BTC-CloudX Platform

## 📋 نظرة عامة على التحديثات

تم تطوير المنصة بشكل كامل لتصبح نظام متكامل لإدارة الاستثمارات في التعدين السحابي مع:

### ✅ الميزات الجديدة:

1. **نظام التسجيل وإدارة الحسابات**
   - تسجيل المستخدمين عبر البوت
   - كود تحقق فريد لكل مستخدم (BTC-X-77-XXXXX)
   - معلومات كاملة: الاسم، البريد، رقم الهاتف

2. **نظام المحافظ الرقمية**
   - 5 محافظ رئيسية: USDT (TRC20/ERC20), BTC, ETH, BNB
   - إضافة محافظ للمستخدمين
   - محافظ الشركة للإيداعات

3. **نظام الإيداع والسحب**
   - طلبات إيداع مع إثبات الدفع (صور)
   - طلبات سحب للمستخدمين
   - تتبع حالة الطلبات

4. **لوحة تحكم Admin**
   - إدارة المستخدمين
   - الموافقة/رفض طلبات الإيداع
   - الموافقة/رفض طلبات السحب
   - إحصائيات شاملة للمنصة

5. **REST API**
   - للتواصل بين البوت والموقع
   - مصادقة بـ JWT
   - endpoints لكل العمليات

6. **قاعدة بيانات SQLite**
   - جداول منظمة للمستخدمين والمعاملات
   - تتبع كامل للعمليات

---

## 📁 الملفات الجديدة المُضافة

```
BTC-CloudX-main/
├── database.py          # قاعدة البيانات الكاملة
├── api.py               # REST API مع Flask
├── auth_handlers.py     # معالجات التسجيل والحسابات
├── admin_panel.py       # لوحة تحكم الأدمن
├── btc_cloudx.db        # قاعدة البيانات (ستُنشأ تلقائياً)
└── uploads/             # مجلد صور الإيداعات
    └── proofs/
```

---

## ⚙️ خطوات الإعداد

### 1️⃣ تحديث ملف `.env`

أضف المتغيرات التالية:

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
WEB_APP_URL=https://your-website.com
TELEGRAM_SUPPORT_URL=https://t.me/your_support
TELEGRAM_CHANNEL_URL=https://t.me/your_channel

# Admin Configuration
ADMIN_TELEGRAM_IDS=123456789,987654321

# API Security
JWT_SECRET_KEY=your_random_secret_key_here

# Server Configuration
PORT=5000
```

**مهم جداً:**
- `ADMIN_TELEGRAM_IDS`: ضع معرفات Telegram للأدمن مفصولة بفواصل
- لمعرفة telegram_id الخاص بك، تحدث مع البوت @userinfobot

### 2️⃣ تثبيت المكتبات المُحدثة

```bash
pip install -r requirements.txt
```

المكتبات الجديدة المُضافة:
- `Flask-CORS`: للسماح بطلبات الـ API
- `PyJWT`: للمصادقة والأمان
- `Pillow`: لمعالجة الصور

### 3️⃣ تشغيل البوت

```bash
python main.py
```

سيبدأ البوت وسيُنشئ:
- قاعدة البيانات `btc_cloudx.db` تلقائياً
- المحافظ الافتراضية للشركة
- مجلدات الرفع

### 4️⃣ تشغيل الـ API (اختياري للتطوير المحلي)

إذا كنت تريد تشغيل API منفصلة:

```bash
python api.py
```

ستعمل على: `http://localhost:5000`

---

## 🎯 كيفية استخدام النظام

### للمستخدم العادي:

1. **بدء البوت**: `/start`
2. **إنشاء حساب**: 
   - اضغط "📝 إنشاء حساب"
   - ستحصل على كود التحقق (BTC-X-77-XXXXX)
   - أدخل بياناتك: الاسم، البريد، الهاتف
3. **عرض الحساب**: "👤 حسابي"
4. **الإيداع**:
   - "💰 الإيداع" → اختر المحفظة
   - حوّل المبلغ للعنوان المعروض
   - ارفع صورة الإيداع على الموقع
5. **السحب**:
   - "💸 السحب" → أدخل بيانات محفظتك
   - انتظر موافقة الأدمن

### للأدمن:

1. **الوصول**: أرسل أي رسالة للبوت
2. **لوحة التحكم**:
   - سيظهر زر "🔐 لوحة التحكم" (للأدمن فقط)
3. **إدارة الطلبات**:
   - "💰 طلبات الإيداع" → الموافقة/الرفض
   - "💸 طلبات السحب" → تأكيد التحويل/الرفض
4. **المستخدمين**: عرض وإدارة جميع المستخدمين
5. **الإحصائيات**: إحصائيات شاملة للمنصة

---

## 🔧 تخصيص المحافظ الرقمية

لتحديث عناوين محافظ الشركة:

### الطريقة 1: من قاعدة البيانات

```python
from database import db

conn = db.get_connection()
cursor = conn.cursor()

# تحديث محفظة USDT TRC20 مثلاً
cursor.execute('''
    UPDATE company_wallets 
    SET wallet_address = 'عنوان_المحفظة_الجديد'
    WHERE wallet_type = 'USDT_TRC20'
''')

conn.commit()
conn.close()
```

### الطريقة 2: من الكود

عدّل ملف `database.py` السطر 140:

```python
default_wallets = [
    ('USDT_TRC20', 'عنوان_محفظتك_الحقيقي', 'USDT (TRC20)'),
    ('USDT_ERC20', 'عنوان_محفظتك_الحقيقي', 'USDT (ERC20)'),
    ('Bitcoin', 'عنوان_محفظتك_الحقيقي', 'Bitcoin (BTC)'),
    ('Ethereum', 'عنوان_محفظتك_الحقيقي', 'Ethereum (ETH)'),
    ('BNB_BSC', 'عنوان_محفظتك_الحقيقي', 'BNB (BSC)')
]
```

---

## 📡 API Endpoints

### Auth
- `POST /api/auth/check-telegram` - التحقق من حساب المستخدم
- `POST /api/auth/register` - تسجيل مستخدم جديد
- `POST /api/auth/verify-code` - التحقق من كود

### User
- `GET /api/user/profile` - معلومات المستخدم (يتطلب token)
- `GET /api/user/transactions` - معاملات المستخدم

### Wallets
- `GET /api/wallets/company` - محافظ الشركة
- `GET /api/wallets/user` - محافظ المستخدم
- `POST /api/wallets/add` - إضافة محفظة

### Deposit
- `POST /api/deposit/create` - إنشاء طلب إيداع (مع صورة)
- `GET /api/deposit/history` - سجل الإيداعات

### Withdrawal
- `POST /api/withdrawal/create` - إنشاء طلب سحب
- `GET /api/withdrawal/history` - سجل السحوبات

### Admin
- `GET /api/admin/users` - جميع المستخدمين
- `GET /api/admin/deposits/pending` - طلبات إيداع معلقة
- `GET /api/admin/withdrawals/pending` - طلبات سحب معلقة
- `POST /api/admin/deposit/approve/<id>` - موافقة على إيداع
- `GET /api/admin/stats` - إحصائيات

---

## 🗄️ هيكل قاعدة البيانات

### جدول `users`
- معلومات المستخدم الأساسية
- كود التحقق الفريد
- الرصيد الحالي
- حالة الحساب

### جدول `user_wallets`
- محافظ المستخدمين الرقمية
- ربطها بالمستخدم

### جدول `deposit_requests`
- طلبات الإيداع
- رقم الطلب الفريد
- صورة الإثبات
- الحالة (pending/approved/rejected)

### جدول `withdrawal_requests`
- طلبات السحب
- عنوان المحفظة المستهدفة
- الحالة

### جدول `transactions`
- سجل شامل لكل المعاملات
- ربطها بالمستخدمين

### جدول `company_wallets`
- محافظ الشركة الرسمية
- للإيداعات

---

## 🔐 الأمان

1. **JWT Tokens**: جميع طلبات API محمية
2. **File Upload Validation**: التحقق من امتدادات الملفات
3. **SQL Injection Protection**: استخدام parameterized queries
4. **Admin Verification**: تحقق من صلاحيات الأدمن
5. **HTTPS**: يُنصح بشدة للإنتاج

---

## 🚀 النشر (Deployment)

### على Render.com

1. **رفع الملفات** على GitHub
2. **إنشاء Web Service جديد**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
3. **إضافة Environment Variables** من `.env`
4. **Deploy**

### على Heroku

```bash
git init
git add .
git commit -m "Initial commit"
heroku create your-app-name
git push heroku master
```

---

## 📝 ملاحظات مهمة

### ⚠️ قبل الإطلاق الفعلي:

1. ✅ تحديث عناوين المحافظ الحقيقية
2. ✅ إضافة معرفات الأدمن في `.env`
3. ✅ تعيين JWT_SECRET_KEY عشوائي وقوي
4. ✅ اختبار جميع الوظائف
5. ✅ تفعيل HTTPS على الموقع

### 🔍 للتطوير والاختبار:

- استخدم محافظ Testnet
- اختبر جميع السيناريوهات
- راجع logs للأخطاء

---

## 📞 الدعم الفني

في حالة وجود مشاكل:

1. تحقق من logs البوت
2. تحقق من قاعدة البيانات
3. راجع متغيرات البيئة
4. تأكد من تثبيت جميع المكتبات

---

## 🎉 التحديثات القادمة المقترحة

- [ ] إرسال إشعارات للمستخدم عند الموافقة/الرفض
- [ ] نظام الإحالة (Referral)
- [ ] حساب الأرباح التلقائي للاستثمارات
- [ ] لوحة تحكم ويب كاملة للأدمن
- [ ] تقارير PDF للمستخدمين
- [ ] نظام دعم فني داخل البوت
- [ ] إحصائيات بيانية للأدمن

---

**تم التطوير بواسطة:** Cascade AI Assistant
**التاريخ:** أكتوبر 2025
**الإصدار:** 2.0.0

🚀 **BTC-CloudX** - منصتك الموثوقة للتعدين السحابي!
