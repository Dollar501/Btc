# api.py
"""
Flask API للتواصل بين البوت والموقع
يوفر endpoints للتسجيل، المحافظ، الإيداع، السحب، وإدارة الحسابات
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import jwt
import hashlib
from datetime import datetime, timedelta
from functools import wraps
from database import db
import secrets

# إعدادات Flask
app = Flask(__name__)
CORS(app)  # للسماح بالطلبات من الموقع

# إعدادات أمنية
SECRET_KEY = os.getenv('JWT_SECRET_KEY', secrets.token_hex(32))
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = 'uploads/proofs'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size

# إنشاء مجلد الرفع إذا لم يكن موجوداً
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ==================== Helper Functions ====================

def generate_token(user_id: int, telegram_id: int) -> str:
    """توليد JWT token للمستخدم"""
    payload = {
        'user_id': user_id,
        'telegram_id': telegram_id,
        'exp': datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token: str):
    """التحقق من صحة JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def require_auth(f):
    """Decorator للتحقق من تسجيل الدخول"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'success': False, 'message': 'مطلوب تسجيل الدخول'}), 401
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        payload = verify_token(token)
        if not payload:
            return jsonify({'success': False, 'message': 'جلسة غير صالحة'}), 401
        
        request.user_id = payload['user_id']
        request.telegram_id = payload['telegram_id']
        
        return f(*args, **kwargs)
    
    return decorated_function

def allowed_file(filename):
    """التحقق من امتداد الملف"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ==================== Authentication Endpoints ====================

@app.route('/api/auth/check-telegram', methods=['POST'])
def check_telegram():
    """التحقق من وجود حساب لمستخدم telegram"""
    data = request.get_json()
    telegram_id = data.get('telegram_id')
    
    if not telegram_id:
        return jsonify({'success': False, 'message': 'telegram_id مطلوب'}), 400
    
    user = db.get_user_by_telegram_id(telegram_id)
    
    if user:
        token = generate_token(user['id'], telegram_id)
        return jsonify({
            'success': True,
            'has_account': True,
            'user': {
                'id': user['id'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'email': user['email'],
                'verification_code': user['verification_code'],
                'balance': user['balance']
            },
            'token': token
        })
    else:
        return jsonify({
            'success': True,
            'has_account': False,
            'message': 'لا يوجد حساب مسجل'
        })

@app.route('/api/auth/register', methods=['POST'])
def register():
    """تسجيل مستخدم جديد"""
    data = request.get_json()
    
    # التحقق من البيانات المطلوبة
    required_fields = ['telegram_id', 'first_name', 'last_name', 'email', 'phone', 'verification_code']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'success': False, 'message': f'{field} مطلوب'}), 400
    
    # التحقق من كود التحقق (يجب أن يكون مرسل من البوت)
    verification_code = data.get('verification_code')
    if not verification_code.startswith('BTC-X-77-'):
        return jsonify({'success': False, 'message': 'كود التحقق غير صالح'}), 400
    
    # إنشاء المستخدم
    result = db.create_user(
        telegram_id=data['telegram_id'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data['phone']
    )
    
    if result['success']:
        user = db.get_user_by_telegram_id(data['telegram_id'])
        token = generate_token(user['id'], data['telegram_id'])
        
        return jsonify({
            'success': True,
            'message': 'تم التسجيل بنجاح',
            'user': {
                'id': user['id'],
                'verification_code': user['verification_code']
            },
            'token': token
        }), 201
    else:
        return jsonify(result), 400

@app.route('/api/auth/verify-code', methods=['POST'])
def verify_code():
    """التحقق من كود المستخدم"""
    data = request.get_json()
    code = data.get('verification_code')
    
    if not code:
        return jsonify({'success': False, 'message': 'كود التحقق مطلوب'}), 400
    
    user = db.get_user_by_verification_code(code)
    
    if user:
        return jsonify({
            'success': True,
            'valid': True,
            'user': {
                'first_name': user['first_name'],
                'last_name': user['last_name']
            }
        })
    else:
        return jsonify({
            'success': True,
            'valid': False,
            'message': 'كود غير صحيح'
        })

# ==================== User Profile Endpoints ====================

@app.route('/api/user/profile', methods=['GET'])
@require_auth
def get_profile():
    """الحصول على معلومات المستخدم"""
    user = db.get_user_by_telegram_id(request.telegram_id)
    
    if not user:
        return jsonify({'success': False, 'message': 'المستخدم غير موجود'}), 404
    
    # إزالة البيانات الحساسة
    safe_user = {
        'id': user['id'],
        'first_name': user['first_name'],
        'last_name': user['last_name'],
        'email': user['email'],
        'phone': user['phone'],
        'verification_code': user['verification_code'],
        'balance': user['balance'],
        'email_verified': user['email_verified'],
        'account_status': user['account_status'],
        'created_at': user['created_at']
    }
    
    return jsonify({'success': True, 'user': safe_user})

@app.route('/api/user/transactions', methods=['GET'])
@require_auth
def get_transactions():
    """الحصول على معاملات المستخدم"""
    limit = request.args.get('limit', 50, type=int)
    transactions = db.get_user_transactions(request.user_id, limit)
    
    return jsonify({
        'success': True,
        'transactions': transactions
    })

# ==================== Wallet Endpoints ====================

@app.route('/api/wallets/company', methods=['GET'])
def get_company_wallets():
    """الحصول على محافظ الشركة للإيداع"""
    wallets = db.get_company_wallets()
    return jsonify({
        'success': True,
        'wallets': wallets
    })

@app.route('/api/wallets/user', methods=['GET'])
@require_auth
def get_user_wallets():
    """الحصول على محافظ المستخدم"""
    wallets = db.get_user_wallets(request.user_id)
    return jsonify({
        'success': True,
        'wallets': wallets
    })

@app.route('/api/wallets/add', methods=['POST'])
@require_auth
def add_wallet():
    """إضافة محفظة جديدة للمستخدم"""
    data = request.get_json()
    
    wallet_type = data.get('wallet_type')
    wallet_address = data.get('wallet_address')
    
    if not wallet_type or not wallet_address:
        return jsonify({'success': False, 'message': 'بيانات المحفظة غير كاملة'}), 400
    
    result = db.add_user_wallet(request.user_id, wallet_type, wallet_address)
    return jsonify(result)

# ==================== Deposit Endpoints ====================

@app.route('/api/deposit/create', methods=['POST'])
@require_auth
def create_deposit():
    """إنشاء طلب إيداع جديد"""
    
    # التحقق من وجود ملف الصورة
    if 'proof_image' not in request.files:
        return jsonify({'success': False, 'message': 'صورة الإيداع مطلوبة'}), 400
    
    file = request.files['proof_image']
    
    if file.filename == '':
        return jsonify({'success': False, 'message': 'لم يتم اختيار ملف'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'نوع الملف غير مسموح'}), 400
    
    # حفظ الصورة
    filename = secure_filename(f"{request.user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}")
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # البيانات من الـ form
    amount = float(request.form.get('amount'))
    wallet_type = request.form.get('wallet_type')
    wallet_address = request.form.get('wallet_address')
    
    # إنشاء الطلب
    result = db.create_deposit_request(
        user_id=request.user_id,
        amount=amount,
        wallet_type=wallet_type,
        wallet_address=wallet_address,
        proof_image_path=filepath
    )
    
    return jsonify(result)

@app.route('/api/deposit/history', methods=['GET'])
@require_auth
def deposit_history():
    """سجل إيداعات المستخدم"""
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM deposit_requests 
        WHERE user_id = ? 
        ORDER BY created_at DESC
    ''', (request.user_id,))
    deposits = cursor.fetchall()
    conn.close()
    
    return jsonify({
        'success': True,
        'deposits': [dict(d) for d in deposits]
    })

# ==================== Withdrawal Endpoints ====================

@app.route('/api/withdrawal/create', methods=['POST'])
@require_auth
def create_withdrawal():
    """إنشاء طلب سحب جديد"""
    data = request.get_json()
    
    amount = data.get('amount')
    wallet_type = data.get('wallet_type')
    wallet_address = data.get('wallet_address')
    
    if not all([amount, wallet_type, wallet_address]):
        return jsonify({'success': False, 'message': 'بيانات غير كاملة'}), 400
    
    result = db.create_withdrawal_request(
        user_id=request.user_id,
        amount=float(amount),
        wallet_type=wallet_type,
        wallet_address=wallet_address
    )
    
    return jsonify(result)

@app.route('/api/withdrawal/history', methods=['GET'])
@require_auth
def withdrawal_history():
    """سجل سحوبات المستخدم"""
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM withdrawal_requests 
        WHERE user_id = ? 
        ORDER BY created_at DESC
    ''', (request.user_id,))
    withdrawals = cursor.fetchall()
    conn.close()
    
    return jsonify({
        'success': True,
        'withdrawals': [dict(w) for w in withdrawals]
    })

# ==================== Admin Endpoints ====================

@app.route('/api/admin/users', methods=['GET'])
def admin_get_users():
    """الحصول على جميع المستخدمين (للأدمن فقط)"""
    # TODO: إضافة تحقق من صلاحيات الأدمن
    users = db.get_all_users()
    return jsonify({
        'success': True,
        'users': users
    })

@app.route('/api/admin/deposits/pending', methods=['GET'])
def admin_pending_deposits():
    """الحصول على طلبات الإيداع المعلقة"""
    deposits = db.get_pending_deposits()
    return jsonify({
        'success': True,
        'deposits': deposits
    })

@app.route('/api/admin/withdrawals/pending', methods=['GET'])
def admin_pending_withdrawals():
    """الحصول على طلبات السحب المعلقة"""
    withdrawals = db.get_pending_withdrawals()
    return jsonify({
        'success': True,
        'withdrawals': withdrawals
    })

@app.route('/api/admin/deposit/approve/<int:request_id>', methods=['POST'])
def admin_approve_deposit(request_id):
    """الموافقة على طلب إيداع"""
    # TODO: الحصول على admin_id من الـ token
    admin_id = 1  # مؤقت
    
    result = db.approve_deposit(request_id, admin_id)
    
    if result:
        return jsonify({'success': True, 'message': 'تم الموافقة على الطلب'})
    else:
        return jsonify({'success': False, 'message': 'فشل الموافقة على الطلب'}), 400

@app.route('/api/admin/stats', methods=['GET'])
def admin_stats():
    """إحصائيات المنصة"""
    stats = db.get_platform_stats()
    return jsonify({
        'success': True,
        'stats': stats
    })

# ==================== Health Check ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """فحص صحة API"""
    return jsonify({
        'status': 'OK',
        'service': 'BTC-CloudX API',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/')
def index():
    """الصفحة الرئيسية للـ API"""
    return jsonify({
        'message': 'BTC-CloudX API',
        'version': '1.0.0',
        'endpoints': {
            'auth': '/api/auth/*',
            'user': '/api/user/*',
            'wallets': '/api/wallets/*',
            'deposit': '/api/deposit/*',
            'withdrawal': '/api/withdrawal/*',
            'admin': '/api/admin/*'
        }
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
