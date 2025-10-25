# 🚀 خطوات النشر التفصيلية - BTC-CloudX

## 📋 المتطلبات الأساسية
- حساب GitHub
- حساب Hostinger
- حساب Render
- Telegram Bot Token

---

## 1️⃣ رفع المشروع على GitHub

### خطوات الرفع:
```bash
# في مجلد المشروع
git init
git add .
git commit -m "Initial commit - BTC-CloudX Platform"
git branch -M main
git remote add origin https://github.com/yourusername/btc-cloudx.git
git push -u origin main
```

### الملفات المطلوبة للـ GitHub:
- ✅ جميع ملفات المشروع
- ✅ `.gitignore` (تم إنشاؤه)
- ✅ `README_DEPLOYMENT.md` (تم إنشاؤه)
- ✅ `.env.example` (تم إنشاؤه)

---

## 2️⃣ نشر الواجهة الأمامية على Hostinger

### الملفات المطلوب رفعها:
```
public_html/
├── index.html
├── styles.css
├── script.js
├── languages.js
├── input.css
├── img/ (المجلد كاملاً)
└── .htaccess
```

### خطوات الرفع:
1. **تسجيل الدخول** إلى cPanel في Hostinger
2. **فتح File Manager**
3. **الانتقال** إلى مجلد `public_html`
4. **رفع الملفات** المذكورة أعلاه
5. **التأكد** من أن `index.html` في المجلد الرئيسي
6. **اختبار** الموقع من خلال الرابط

### إعدادات .htaccess (موجود بالفعل):
```apache
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ index.html [QSA,L]

# Enable compression
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/plain
    AddOutputFilterByType DEFLATE text/html
    AddOutputFilterByType DEFLATE text/xml
    AddOutputFilterByType DEFLATE text/css
    AddOutputFilterByType DEFLATE application/xml
    AddOutputFilterByType DEFLATE application/xhtml+xml
    AddOutputFilterByType DEFLATE application/rss+xml
    AddOutputFilterByType DEFLATE application/javascript
    AddOutputFilterByType DEFLATE application/x-javascript
</IfModule>
```

---

## 3️⃣ نشر البوت على Render

### خطوات النشر:
1. **تسجيل الدخول** إلى Render.com
2. **إنشاء Web Service جديد**
3. **ربط GitHub Repository**
4. **إعدادات الخدمة:**
   - **Name**: `btc-cloudx-bot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`

### متغيرات البيئة المطلوبة:
```
TELEGRAM_BOT_TOKEN=your_actual_bot_token
WEB_APP_URL=https://yourdomain.com
TELEGRAM_SUPPORT_URL=https://t.me/yourusername
PORT=10000
WEBHOOK_URL=https://your-render-app.onrender.com
```

### الملفات المطلوبة للـ Render:
- ✅ `requirements.txt` (محدث)
- ✅ `Procfile` (تم إنشاؤه)
- ✅ `render.yaml` (تم إنشاؤه)
- ✅ `runtime.txt` (تم إنشاؤه)

---

## 4️⃣ إعداد Telegram Bot

### خطوات الإعداد:
1. **إنشاء بوت** مع @BotFather
2. **الحصول على Token**
3. **إعداد Web App:**
   ```
   /setmenubutton
   @your_bot_name
   Web App
   https://yourdomain.com
   ```
4. **إعداد Commands:**
   ```
   start - بدء استخدام البوت
   ```

---

## 5️⃣ اختبار النشر

### قائمة الفحص:
- [ ] الموقع يعمل على Hostinger
- [ ] البوت يرد على Render
- [ ] Web App يفتح من البوت
- [ ] تبديل اللغات يعمل
- [ ] حاسبة الاستثمار تعمل
- [ ] نظام الكوبونات يعمل
- [ ] جميع الصفحات تعمل بشكل صحيح

---

## 🔧 استكشاف الأخطاء

### مشاكل شائعة وحلولها:

#### البوت لا يرد:
- تحقق من `BOT_TOKEN`
- تحقق من `WEBHOOK_URL`
- راجع logs في Render

#### الموقع لا يعمل:
- تحقق من رفع جميع الملفات
- تحقق من `.htaccess`
- تحقق من مسارات الملفات

#### Web App لا يفتح:
- تحقق من `WEB_APP_URL`
- تحقق من إعدادات البوت
- تحقق من HTTPS

---

## 📞 الدعم الفني

إذا واجهت أي مشاكل:
1. راجع logs في Render
2. تحقق من متغيرات البيئة
3. تأكد من صحة جميع الروابط
4. اختبر كل جزء منفصلاً

---

**🎉 مبروك! مشروع BTC-CloudX جاهز للعمل!**
