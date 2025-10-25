# دليل رفع موقع BTC-CloudX

## الملفات المطلوبة للموقع (Frontend)
```
index.html          - الصفحة الرئيسية
styles.css          - ملف التصميم
script.js           - الجافاسكريبت الرئيسي
languages.js        - ملف اللغات
.htaccess          - إعدادات Apache (للاستضافة المشتركة)
netlify.toml       - إعدادات Netlify (إذا كنت تستخدم Netlify)
```

## خطوات الرفع

### 1. للاستضافة المشتركة (Shared Hosting)
- ارفع جميع الملفات إلى مجلد `public_html` أو `www`
- تأكد من أن ملف `.htaccess` مرفوع
- تأكد من أن أسماء الملفات صحيحة (حساسة للأحرف)

### 2. لـ Netlify
- اسحب وأفلت المجلد كاملاً على موقع Netlify
- أو ارفع عبر Git
- ملف `netlify.toml` سيتم قراءته تلقائياً

### 3. لـ Vercel
- ارفع المجلد عبر Vercel CLI أو الموقع
- لا حاجة لإعدادات إضافية

## استكشاف الأخطاء

### إذا كانت الصفحة فارغة:
1. افتح Developer Tools (F12)
2. اذهب إلى Console
3. ابحث عن أخطاء تحميل الملفات

### إذا كان التصميم مفقود:
- تحقق من تحميل `styles.css`
- تحقق من رابط Tailwind CSS

### إذا كانت الوظائف لا تعمل:
- تحقق من تحميل `script.js` و `languages.js`
- تحقق من أخطاء JavaScript في Console

## إعداد البوت (Backend)

### متطلبات الخادم:
- Python 3.8+
- دعم HTTPS
- إمكانية تشغيل Python scripts

### ملفات البوت المطلوبة:
```
main.py
localization.py
data_store.py
command_processors.py
helpers.py
devices.py
plan.py
create_plan.py
requirements.txt (إنشاء هذا الملف)
```

### خطوات إعداد البوت:
1. ارفع ملفات Python إلى الخادم
2. قم بتثبيت المتطلبات: `pip install -r requirements.txt`
3. اضبط متغيرات البيئة (BOT_TOKEN, WEBHOOK_URL)
4. اضبط Webhook في تليجرام
5. حدث رابط Web App في البوت

## روابط مهمة:
- Netlify: https://netlify.com
- Vercel: https://vercel.com
- Railway: https://railway.app (للبوت Python)
- Heroku: https://heroku.com (للبوت Python)
