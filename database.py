# database.py
"""
نظام قاعدة البيانات لـ BTC-CloudX
يشمل: المستخدمين، المحافظ، المعاملات، الإيداعات، السحوبات
"""

import sqlite3
import hashlib
import secrets
import string
from datetime import datetime
from decimal import Decimal
from typing import Optional, Dict, List, Tuple
import os

# Try to import psycopg2 for PostgreSQL support
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    HAS_POSTGRES = True
except ImportError:
    HAS_POSTGRES = False


class Database:
    """مدير قاعدة البيانات الرئيسي - يدعم PostgreSQL و SQLite"""
    
    def __init__(self, db_path: str = "btc_cloudx.db"):
        # Check if DATABASE_URL is provided (for PostgreSQL)
        self.database_url = os.getenv('DATABASE_URL')
        
        if self.database_url:
            # Use PostgreSQL
            if self.database_url.startswith('postgres://'):
                # Render uses postgres:// but psycopg2 needs postgresql://
                self.database_url = self.database_url.replace('postgres://', 'postgresql://', 1)
            self.use_postgres = True
            print("📊 Using PostgreSQL database")
        else:
            # Use SQLite (for local development)
            self.db_path = db_path
            self.use_postgres = False
            print(f"📊 Using SQLite database: {db_path}")
        
        self.init_database()
    
    def get_connection(self):
        """إنشاء اتصال بقاعدة البيانات"""
        if self.use_postgres:
            conn = psycopg2.connect(self.database_url, cursor_factory=RealDictCursor)
            return conn
        else:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
    
    def init_database(self):
        """إنشاء جداول قاعدة البيانات"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # SQL syntax differs between SQLite and PostgreSQL
        if self.use_postgres:
            # PostgreSQL syntax
            users_table = '''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    telegram_id BIGINT UNIQUE NOT NULL,
                    verification_code TEXT UNIQUE NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT UNIQUE NOT NULL,
                    email_verified INTEGER DEFAULT 0,
                    phone_verified INTEGER DEFAULT 0,
                    account_status TEXT DEFAULT 'pending',
                    balance NUMERIC(10, 2) DEFAULT 0.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            '''
        else:
            # SQLite syntax
            users_table = '''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER UNIQUE NOT NULL,
                    verification_code TEXT UNIQUE NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT UNIQUE NOT NULL,
                    email_verified INTEGER DEFAULT 0,
                    phone_verified INTEGER DEFAULT 0,
                    account_status TEXT DEFAULT 'pending',
                    balance REAL DEFAULT 0.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            '''
        
        cursor.execute(users_table + ')')
        
        # جدول المحافظ الرقمية للمستخدمين
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_wallets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                wallet_type TEXT NOT NULL,
                wallet_address TEXT NOT NULL,
                is_primary INTEGER DEFAULT 0,
                verified INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # جدول طلبات الإيداع
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS deposit_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                request_number TEXT UNIQUE NOT NULL,
                amount REAL NOT NULL,
                wallet_type TEXT NOT NULL,
                wallet_address TEXT NOT NULL,
                transaction_hash TEXT,
                proof_image_path TEXT,
                status TEXT DEFAULT 'pending',
                admin_notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                processed_at TIMESTAMP,
                processed_by INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # جدول طلبات السحب
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS withdrawal_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                request_number TEXT UNIQUE NOT NULL,
                amount REAL NOT NULL,
                wallet_type TEXT NOT NULL,
                wallet_address TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                admin_notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                processed_at TIMESTAMP,
                processed_by INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # جدول الاستثمارات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS investments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                plan_name TEXT NOT NULL,
                amount REAL NOT NULL,
                hashrate REAL NOT NULL,
                daily_profit REAL NOT NULL,
                start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_date TIMESTAMP,
                status TEXT DEFAULT 'active',
                total_earned REAL DEFAULT 0.0,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # جدول المعاملات (سجل شامل)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'completed',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # جدول الأدمن
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE NOT NULL,
                username TEXT NOT NULL,
                role TEXT DEFAULT 'admin',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول إعدادات المحافظ الرسمية للشركة
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS company_wallets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                wallet_type TEXT UNIQUE NOT NULL,
                wallet_address TEXT NOT NULL,
                wallet_name TEXT NOT NULL,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # إضافة المحافظ الافتراضية
        self._add_default_wallets()
    
    def _add_default_wallets(self):
        """إضافة المحافظ الرقمية الافتراضية للشركة"""
        default_wallets = [
            ('USDT_TRC20', 'TXxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'USDT (TRC20)'),
            ('USDT_ERC20', '0xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'USDT (ERC20)'),
            ('Bitcoin', 'bc1qxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'Bitcoin (BTC)'),
            ('Ethereum', '0xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'Ethereum (ETH)'),
            ('BNB_BSC', '0xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'BNB (BSC)')
        ]
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        for wallet_type, address, name in default_wallets:
            cursor.execute(
                'INSERT OR IGNORE INTO company_wallets (wallet_type, wallet_address, wallet_name) VALUES (?, ?, ?)',
                (wallet_type, address, name)
            )
        
        conn.commit()
        conn.close()
    
    def generate_verification_code(self) -> str:
        """توليد كود تحقق فريد بصيغة BTC-X-77-XXXXX"""
        while True:
            # توليد 5 أحرف/أرقام عشوائية
            random_part = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(5))
            code = f"BTC-X-77-{random_part}"
            
            # التأكد من عدم وجود الكود في قاعدة البيانات
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM users WHERE verification_code = ?', (code,))
            exists = cursor.fetchone()
            conn.close()
            
            if not exists:
                return code
    
    def generate_request_number(self, prefix: str = 'REQ') -> str:
        """توليد رقم طلب فريد"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_part = ''.join(secrets.choice(string.digits) for _ in range(4))
        return f"{prefix}-{timestamp}-{random_part}"
    
    # ==================== User Management ====================
    
    def create_user(self, telegram_id: int, first_name: str, last_name: str, 
                   email: str, phone: str) -> Dict:
        """إنشاء مستخدم جديد"""
        verification_code = self.generate_verification_code()
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (telegram_id, verification_code, first_name, last_name, email, phone)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (telegram_id, verification_code, first_name, last_name, email, phone))
            
            user_id = cursor.lastrowid
            conn.commit()
            
            # تسجيل معاملة الإنشاء
            self.add_transaction(user_id, 'account_created', 0.0, 'تم إنشاء الحساب بنجاح')
            
            return {
                'success': True,
                'user_id': user_id,
                'verification_code': verification_code,
                'message': 'تم إنشاء الحساب بنجاح'
            }
        except sqlite3.IntegrityError as e:
            conn.rollback()
            return {
                'success': False,
                'message': f'خطأ: البريد الإلكتروني أو رقم الهاتف مسجل مسبقاً'
            }
        finally:
            conn.close()
    
    def get_user_by_telegram_id(self, telegram_id: int) -> Optional[Dict]:
        """الحصول على معلومات المستخدم باستخدام telegram_id"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
        user = cursor.fetchone()
        conn.close()
        
        return dict(user) if user else None
    
    def get_user_by_verification_code(self, code: str) -> Optional[Dict]:
        """الحصول على معلومات المستخدم باستخدام كود التحقق"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE verification_code = ?', (code,))
        user = cursor.fetchone()
        conn.close()
        
        return dict(user) if user else None
    
    def verify_email(self, user_id: int) -> bool:
        """تأكيد البريد الإلكتروني"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET email_verified = 1 WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        return True
    
    def update_user_balance(self, user_id: int, amount: float, operation: str = 'add'):
        """تحديث رصيد المستخدم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if operation == 'add':
            cursor.execute('UPDATE users SET balance = balance + ? WHERE id = ?', (amount, user_id))
        elif operation == 'subtract':
            cursor.execute('UPDATE users SET balance = balance - ? WHERE id = ?', (amount, user_id))
        
        conn.commit()
        conn.close()
    
    # ==================== Wallet Management ====================
    
    def add_user_wallet(self, user_id: int, wallet_type: str, wallet_address: str) -> Dict:
        """إضافة محفظة للمستخدم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO user_wallets (user_id, wallet_type, wallet_address)
                VALUES (?, ?, ?)
            ''', (user_id, wallet_type, wallet_address))
            
            conn.commit()
            return {'success': True, 'message': 'تم إضافة المحفظة بنجاح'}
        except sqlite3.IntegrityError:
            return {'success': False, 'message': 'المحفظة مسجلة مسبقاً'}
        finally:
            conn.close()
    
    def get_user_wallets(self, user_id: int) -> List[Dict]:
        """الحصول على محافظ المستخدم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user_wallets WHERE user_id = ?', (user_id,))
        wallets = cursor.fetchall()
        conn.close()
        
        return [dict(wallet) for wallet in wallets]
    
    def get_company_wallets(self) -> List[Dict]:
        """الحصول على محافظ الشركة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM company_wallets WHERE is_active = 1')
        wallets = cursor.fetchall()
        conn.close()
        
        return [dict(wallet) for wallet in wallets]
    
    # ==================== Deposit Management ====================
    
    def create_deposit_request(self, user_id: int, amount: float, wallet_type: str,
                              wallet_address: str, proof_image_path: str = None) -> Dict:
        """إنشاء طلب إيداع"""
        request_number = self.generate_request_number('DEP')
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO deposit_requests 
            (user_id, request_number, amount, wallet_type, wallet_address, proof_image_path)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, request_number, amount, wallet_type, wallet_address, proof_image_path))
        
        conn.commit()
        conn.close()
        
        return {
            'success': True,
            'request_number': request_number,
            'message': 'تم إنشاء طلب الإيداع بنجاح'
        }
    
    def get_pending_deposits(self) -> List[Dict]:
        """الحصول على طلبات الإيداع المعلقة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT d.*, u.first_name, u.last_name, u.verification_code
            FROM deposit_requests d
            JOIN users u ON d.user_id = u.id
            WHERE d.status = 'pending'
            ORDER BY d.created_at DESC
        ''')
        deposits = cursor.fetchall()
        conn.close()
        
        return [dict(deposit) for deposit in deposits]
    
    def approve_deposit(self, request_id: int, admin_id: int) -> bool:
        """الموافقة على طلب إيداع"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # الحصول على معلومات الطلب
        cursor.execute('SELECT user_id, amount FROM deposit_requests WHERE id = ?', (request_id,))
        request = cursor.fetchone()
        
        if not request:
            conn.close()
            return False
        
        user_id, amount = request
        
        # تحديث حالة الطلب
        cursor.execute('''
            UPDATE deposit_requests 
            SET status = 'approved', processed_at = CURRENT_TIMESTAMP, processed_by = ?
            WHERE id = ?
        ''', (admin_id, request_id))
        
        # إضافة المبلغ لرصيد المستخدم
        cursor.execute('UPDATE users SET balance = balance + ? WHERE id = ?', (amount, user_id))
        
        # تسجيل المعاملة
        cursor.execute('''
            INSERT INTO transactions (user_id, type, amount, description)
            VALUES (?, 'deposit', ?, 'إيداع تم الموافقة عليه')
        ''', (user_id, amount))
        
        conn.commit()
        conn.close()
        return True
    
    # ==================== Withdrawal Management ====================
    
    def create_withdrawal_request(self, user_id: int, amount: float, 
                                 wallet_type: str, wallet_address: str) -> Dict:
        """إنشاء طلب سحب"""
        # التحقق من الرصيد
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT balance FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        
        if not user or user['balance'] < amount:
            conn.close()
            return {'success': False, 'message': 'الرصيد غير كافٍ'}
        
        request_number = self.generate_request_number('WTH')
        
        cursor.execute('''
            INSERT INTO withdrawal_requests 
            (user_id, request_number, amount, wallet_type, wallet_address)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, request_number, amount, wallet_type, wallet_address))
        
        conn.commit()
        conn.close()
        
        return {
            'success': True,
            'request_number': request_number,
            'message': 'تم إنشاء طلب السحب بنجاح'
        }
    
    def get_pending_withdrawals(self) -> List[Dict]:
        """الحصول على طلبات السحب المعلقة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT w.*, u.first_name, u.last_name, u.verification_code
            FROM withdrawal_requests w
            JOIN users u ON w.user_id = u.id
            WHERE w.status = 'pending'
            ORDER BY w.created_at DESC
        ''')
        withdrawals = cursor.fetchall()
        conn.close()
        
        return [dict(withdrawal) for withdrawal in withdrawals]
    
    # ==================== Transaction Management ====================
    
    def add_transaction(self, user_id: int, trans_type: str, amount: float, 
                       description: str = '') -> int:
        """إضافة معاملة جديدة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO transactions (user_id, type, amount, description)
            VALUES (?, ?, ?, ?)
        ''', (user_id, trans_type, amount, description))
        
        trans_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return trans_id
    
    def get_user_transactions(self, user_id: int, limit: int = 50) -> List[Dict]:
        """الحصول على معاملات المستخدم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM transactions 
            WHERE user_id = ? 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (user_id, limit))
        transactions = cursor.fetchall()
        conn.close()
        
        return [dict(trans) for trans in transactions]
    
    # ==================== Admin Functions ====================
    
    def get_all_users(self, limit: int = 100) -> List[Dict]:
        """الحصول على جميع المستخدمين"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users ORDER BY created_at DESC LIMIT ?', (limit,))
        users = cursor.fetchall()
        conn.close()
        
        return [dict(user) for user in users]
    
    def get_platform_stats(self) -> Dict:
        """إحصائيات المنصة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # عدد المستخدمين
        cursor.execute('SELECT COUNT(*) as count FROM users')
        total_users = cursor.fetchone()['count']
        
        # إجمالي الإيداعات
        cursor.execute('SELECT SUM(amount) as total FROM deposit_requests WHERE status = "approved"')
        total_deposits = cursor.fetchone()['total'] or 0
        
        # إجمالي السحوبات
        cursor.execute('SELECT SUM(amount) as total FROM withdrawal_requests WHERE status = "approved"')
        total_withdrawals = cursor.fetchone()['total'] or 0
        
        # الخزنة
        treasury = total_deposits - total_withdrawals
        
        conn.close()
        
        return {
            'total_users': total_users,
            'total_deposits': total_deposits,
            'total_withdrawals': total_withdrawals,
            'treasury': treasury
        }


# إنشاء نسخة عامة من قاعدة البيانات
db = Database()
