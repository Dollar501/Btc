# 🐍 Python Bot - BTC-CloudX

## 📋 نظرة عامة

بوت Telegram احترافي مع REST API لمنصة BTC-CloudX.

---

## 📁 محتويات المجلد:

```
python-bot/
├── main.py               # البوت الرئيسي
├── api.py                # REST API (Flask)
├── database.py           # قاعدة بيانات PostgreSQL
├── auth_handlers.py      # معالجات المصادقة والتسجيل
├── admin_panel.py        # لوحة الأدمن
├── localization.py       # نظام اللغات (3 لغات)
├── data_store.py         # تخزين البيانات
├── command_processors.py # معالجات الأوامر
├── helpers.py            # دوال مساعدة
├── devices.py            # إدارة الأجهزة
├── plan.py               # الخطط الاستثمارية
├── create_plan.py        # إنشاء خطط
├── requirements.txt      # المكتبات المطلوبة
├── runtime.txt           # إصدار Python
├── Procfile              # أمر التشغيل
├── render.yaml           # إعدادات Render
├── .env.example          # مثال للمتغيرات
└── .env                  # المتغيرات الفعلية (لا ترفعه!)
```

---

## ✨ الميزات:

```
✅ بوت Telegram متكامل
✅ REST API (25+ endpoint)
✅ PostgreSQL (7 جداول)
✅ كود تحقق فريد (BTC-X-77-XXXXX)
✅ 5 محافظ رقمية:
   - USDT (TRC20)
   - Bitcoin (BTC)
   - Ethereum (ETH)
   - Binance Coin (BNB)
   - USD Coin (USDC)
✅ نظام إيداع (رفع صور)
✅ نظام سحب (حساب رسوم)
✅ JWT Authentication
✅ لوحة أدمن شاملة
✅ 3 لغات (عربي، إنجليزي، صيني)
```

---

## 🚀 التشغيل المحلي:

### 1️⃣ تثبيت المتطلبات:
```bash
pip install -r requirements.txt
```

### 2️⃣ إعداد .env:
```bash
cp .env.example .env

# عدّل .env:
BOT_TOKEN=your_bot_token
DATABASE_URL=postgresql://user:pass@localhost/dbname
ADMIN_TELEGRAM_IDS=your_telegram_id
JWT_SECRET_KEY=your_secret_key
```

### 3️⃣ تشغيل البوت:
```bash
python main.py
```

### 4️⃣ اختبار:
```
افتح Telegram → ابحث عن البوت
أرسل /start
```

---

## 🌐 النشر على Render:

### الطريقة السريعة:

```bash
# 1. ارفع على GitHub:
git init
git add .
git commit -m "Initial commit"
git push origin main

# 2. من Render Dashboard:
- New Web Service
- اربط GitHub
- اختر هذا المجلد
- Deploy!

# 3. أنشئ PostgreSQL:
- New PostgreSQL
- انسخ DATABASE_URL

# 4. أضف Environment Variables:
BOT_TOKEN
DATABASE_URL
ADMIN_TELEGRAM_IDS
JWT_SECRET_KEY
WEB_APP_URL
```

📖 **الدليل الكامل:** `../docs/DEPLOYMENT.md`

---

## 🗄️ قاعدة البيانات:

### الجداول (7):

1. **users** - المستخدمين
   ```sql
   - id, telegram_id, verification_code
   - first_name, last_name, email
   - main_balance, reward_balance
   ```

2. **user_wallets** - محافظ المستخدمين
   ```sql
   - user_id, wallet_type, wallet_address
   ```

3. **company_wallets** - محافظ الشركة
   ```sql
   - wallet_type, wallet_address, network
   - min_deposit
   ```

4. **deposit_requests** - طلبات الإيداع
   ```sql
   - user_id, amount, proof_image
   - status, created_at
   ```

5. **withdrawal_requests** - طلبات السحب
   ```sql
   - user_id, amount, wallet_address
   - status, transaction_hash
   ```

6. **transactions** - سجل المعاملات
   ```sql
   - user_id, type, amount
   - balance_before, balance_after
   ```

7. **admins** - المدراء
   ```sql
   - telegram_id, username
   - permissions
   ```

---

## 🔌 API Endpoints:

### المصادقة:
```
POST /api/auth/register
POST /api/auth/login
POST /api/auth/verify-code
```

### المستخدمين:
```
GET  /api/user/profile
PUT  /api/user/profile
GET  /api/user/balance
POST /api/user/wallet
```

### الإيداع/السحب:
```
POST /api/deposit/request
GET  /api/deposit/history
POST /api/withdrawal/request
GET  /api/withdrawal/history
```

### الأدمن:
```
GET  /api/admin/users
PUT  /api/admin/user/{id}
POST /api/admin/deposit/approve
POST /api/admin/withdrawal/approve
```

📖 **توثيق API الكامل:** `../docs/FEATURES_OVERVIEW.md`

---

## 💬 أوامر البوت:

### للمستخدمين:
```
/start        - بدء البوت
/register     - تسجيل حساب جديد
/login        - تسجيل الدخول
/mycode       - عرض كود التحقق
/balance      - عرض الرصيد
/deposit      - طلب إيداع
/withdraw     - طلب سحب
/wallet       - إدارة المحافظ
/help         - المساعدة
/language     - تغيير اللغة
```

### للمدراء:
```
/admin        - لوحة الأدمن
/users        - إدارة المستخدمين
/deposits     - طلبات الإيداع
/withdrawals  - طلبات السحب
/stats        - الإحصائيات
```

---

## 🔐 الأمان:

```
✅ JWT للمصادقة
✅ تشفير كلمات المرور
✅ التحقق من الصلاحيات
✅ حماية من SQL Injection
✅ معالجة الأخطاء
✅ تسجيل الإجراءات
```

---

## 🌍 اللغات المدعومة:

```
✅ العربية (ar)
✅ الإنجليزية (en)
✅ الصينية المبسطة (zh)
```

---

## 🔧 المتطلبات:

```
Python >= 3.11
PostgreSQL >= 13
python-telegram-bot
Flask
Flask-CORS
psycopg2-binary
PyJWT
```

---

## 📞 للمساعدة:

```
📖 ../docs/DEPLOYMENT.md - دليل النشر
📖 ../docs/TROUBLESHOOTING.md - حل المشاكل
📖 ../docs/FEATURES_OVERVIEW.md - شرح الميزات
```

---

## 💰 التكلفة:

```
Render Free Tier:    $0/شهر
PostgreSQL Free:     $0/شهر (1GB)

إجمالي:             $0/شهر 🎉
```

---

## 🎯 ملاحظات مهمة:

```
⚠️ لا ترفع .env على GitHub
⚠️ غيّر JWT_SECRET_KEY
⚠️ أضف ADMIN_TELEGRAM_IDS الصحيح
⚠️ استخدم HTTPS في الإنتاج
```

---

**🚀 جاهز للنشر! ابدأ الآن من ../docs/DEPLOYMENT.md**
