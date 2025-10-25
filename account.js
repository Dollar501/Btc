// account.js
// JavaScript للصفحة الشخصية والحساب

const API_BASE_URL = 'http://localhost:5000/api'; // غيّر هذا للإنتاج
let currentUser = null;
let authToken = null;

// ==================== Initialization ====================

document.addEventListener('DOMContentLoaded', function() {
    // التحقق من وجود token في localStorage
    authToken = localStorage.getItem('auth_token');
    
    if (authToken) {
        loadUserProfile();
    } else {
        // محاولة الحصول على telegram_id من Telegram WebApp
        if (window.Telegram && window.Telegram.WebApp) {
            const tg = window.Telegram.WebApp;
            tg.ready();
            
            if (tg.initDataUnsafe && tg.initDataUnsafe.user) {
                checkTelegramAccount(tg.initDataUnsafe.user.id);
            }
        }
    }
    
    // تحميل محافظ الشركة للإيداع
    loadCompanyWallets();
});

// ==================== Authentication ====================

async function checkTelegramAccount(telegramId) {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/check-telegram`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ telegram_id: telegramId })
        });
        
        const data = await response.json();
        
        if (data.success && data.has_account) {
            authToken = data.token;
            localStorage.setItem('auth_token', authToken);
            currentUser = data.user;
            showAccountDashboard();
            loadUserProfile();
        } else {
            showLoginScreen();
        }
    } catch (error) {
        console.error('Error checking account:', error);
        showLoginScreen();
    }
}

async function loginWithCode() {
    const code = document.getElementById('verificationCode').value.trim();
    
    if (!code) {
        alert('❌ الرجاء إدخال كود التحقق');
        return;
    }
    
    if (!code.startsWith('BTC-X-77-')) {
        alert('❌ كود التحقق غير صحيح');
        return;
    }
    
    try {
        // التحقق من الكود
        const response = await fetch(`${API_BASE_URL}/auth/verify-code`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ verification_code: code })
        });
        
        const data = await response.json();
        
        if (data.success && data.valid) {
            alert('✅ تم التحقق من الكود بنجاح!\n\nيرجى إكمال عملية التسجيل من البوت.');
            // يمكن هنا إعادة توجيه المستخدم أو فتح البوت
        } else {
            alert('❌ كود التحقق غير صحيح');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('❌ حدث خطأ في التحقق من الكود');
    }
}

function showLoginScreen() {
    document.getElementById('notLoggedIn').classList.remove('hidden');
    document.getElementById('accountDashboard').classList.add('hidden');
}

function showAccountDashboard() {
    document.getElementById('notLoggedIn').classList.add('hidden');
    document.getElementById('accountDashboard').classList.remove('hidden');
}

function logout() {
    if (confirm('هل تريد تسجيل الخروج؟')) {
        localStorage.removeItem('auth_token');
        authToken = null;
        currentUser = null;
        showLoginScreen();
    }
}

// ==================== Load User Profile ====================

async function loadUserProfile() {
    try {
        const response = await fetch(`${API_BASE_URL}/user/profile`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentUser = data.user;
            displayUserInfo(data.user);
            loadTransactions();
            loadDeposits();
            loadWithdrawals();
        } else {
            showLoginScreen();
        }
    } catch (error) {
        console.error('Error loading profile:', error);
        showLoginScreen();
    }
}

function displayUserInfo(user) {
    document.getElementById('welcomeMessage').textContent = `مرحباً ${user.first_name}!`;
    document.getElementById('accountBalance').textContent = `$${user.balance.toFixed(2)}`;
    document.getElementById('fullName').textContent = `${user.first_name} ${user.last_name}`;
    document.getElementById('email').textContent = user.email;
    document.getElementById('phone').textContent = user.phone;
    document.getElementById('verificationCodeDisplay').textContent = user.verification_code;
}

// ==================== Tabs ====================

function switchTab(tab) {
    // إزالة التنشيط من جميع الأزرار
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('border-purple-500', 'text-white');
        btn.classList.add('border-transparent', 'text-gray-400');
    });
    
    // إخفاء جميع المحتويات
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.add('hidden');
    });
    
    // تنشيط التاب المحدد
    document.getElementById(`tab-${tab}`).classList.remove('border-transparent', 'text-gray-400');
    document.getElementById(`tab-${tab}`).classList.add('border-purple-500', 'text-white');
    document.getElementById(`content-${tab}`).classList.remove('hidden');
}

// ==================== Transactions ====================

async function loadTransactions() {
    try {
        const response = await fetch(`${API_BASE_URL}/user/transactions?limit=20`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayTransactions(data.transactions);
        }
    } catch (error) {
        console.error('Error loading transactions:', error);
    }
}

function displayTransactions(transactions) {
    const container = document.getElementById('transactionsList');
    
    if (!transactions || transactions.length === 0) {
        container.innerHTML = '<p class="text-gray-400 text-center py-8">لا توجد معاملات بعد</p>';
        return;
    }
    
    container.innerHTML = transactions.map(trans => {
        const emoji = trans.type === 'deposit' ? '📥' : trans.type === 'withdrawal' ? '📤' : '💱';
        const color = trans.type === 'deposit' ? 'text-green-400' : 'text-orange-400';
        
        return `
            <div class="bg-white/5 p-4 rounded-lg">
                <div class="flex justify-between items-start">
                    <div>
                        <p class="text-white font-bold">${emoji} ${trans.type}</p>
                        <p class="text-sm text-gray-400">${trans.description || ''}</p>
                        <p class="text-xs text-gray-500">${new Date(trans.created_at).toLocaleString('ar-EG')}</p>
                    </div>
                    <p class="${color} font-bold">$${trans.amount.toFixed(2)}</p>
                </div>
            </div>
        `;
    }).join('');
}

// ==================== Deposits ====================

async function loadDeposits() {
    try {
        const response = await fetch(`${API_BASE_URL}/deposit/history`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayDeposits(data.deposits);
        }
    } catch (error) {
        console.error('Error loading deposits:', error);
    }
}

function displayDeposits(deposits) {
    const container = document.getElementById('depositsList');
    
    if (!deposits || deposits.length === 0) {
        container.innerHTML = '<p class="text-gray-400 text-center py-8">لا توجد طلبات إيداع</p>';
        return;
    }
    
    container.innerHTML = deposits.map(dep => {
        const statusColors = {
            'pending': 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
            'approved': 'bg-green-500/20 text-green-400 border-green-500/30',
            'rejected': 'bg-red-500/20 text-red-400 border-red-500/30'
        };
        
        const statusText = {
            'pending': '⏳ قيد المراجعة',
            'approved': '✅ تمت الموافقة',
            'rejected': '❌ مرفوض'
        };
        
        return `
            <div class="bg-white/5 p-4 rounded-lg border border-white/10">
                <div class="flex justify-between items-start mb-2">
                    <div>
                        <p class="text-white font-bold">طلب #${dep.request_number}</p>
                        <p class="text-sm text-gray-400">${dep.wallet_type}</p>
                    </div>
                    <p class="text-green-400 font-bold">$${dep.amount.toFixed(2)}</p>
                </div>
                <div class="flex justify-between items-center">
                    <span class="text-xs px-3 py-1 rounded-full border ${statusColors[dep.status] || statusColors.pending}">
                        ${statusText[dep.status] || statusText.pending}
                    </span>
                    <p class="text-xs text-gray-500">${new Date(dep.created_at).toLocaleDateString('ar-EG')}</p>
                </div>
            </div>
        `;
    }).join('');
}

// ==================== Withdrawals ====================

async function loadWithdrawals() {
    try {
        const response = await fetch(`${API_BASE_URL}/withdrawal/history`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayWithdrawals(data.withdrawals);
        }
    } catch (error) {
        console.error('Error loading withdrawals:', error);
    }
}

function displayWithdrawals(withdrawals) {
    const container = document.getElementById('withdrawalsList');
    
    if (!withdrawals || withdrawals.length === 0) {
        container.innerHTML = '<p class="text-gray-400 text-center py-8">لا توجد طلبات سحب</p>';
        return;
    }
    
    container.innerHTML = withdrawals.map(wth => {
        const statusColors = {
            'pending': 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
            'approved': 'bg-green-500/20 text-green-400 border-green-500/30',
            'rejected': 'bg-red-500/20 text-red-400 border-red-500/30'
        };
        
        const statusText = {
            'pending': '⏳ قيد المراجعة',
            'approved': '✅ تم التحويل',
            'rejected': '❌ مرفوض'
        };
        
        return `
            <div class="bg-white/5 p-4 rounded-lg border border-white/10">
                <div class="flex justify-between items-start mb-2">
                    <div>
                        <p class="text-white font-bold">طلب #${wth.request_number}</p>
                        <p class="text-sm text-gray-400">${wth.wallet_type}</p>
                        <p class="text-xs text-gray-500 font-mono">${wth.wallet_address.substring(0, 20)}...</p>
                    </div>
                    <p class="text-orange-400 font-bold">$${wth.amount.toFixed(2)}</p>
                </div>
                <div class="flex justify-between items-center">
                    <span class="text-xs px-3 py-1 rounded-full border ${statusColors[wth.status] || statusColors.pending}">
                        ${statusText[wth.status] || statusText.pending}
                    </span>
                    <p class="text-xs text-gray-500">${new Date(wth.created_at).toLocaleDateString('ar-EG')}</p>
                </div>
            </div>
        `;
    }).join('');
}

// ==================== Deposit Modal ====================

let companyWallets = [];

async function loadCompanyWallets() {
    try {
        const response = await fetch(`${API_BASE_URL}/wallets/company`);
        const data = await response.json();
        
        if (data.success) {
            companyWallets = data.wallets;
        }
    } catch (error) {
        console.error('Error loading wallets:', error);
    }
}

function showDepositModal() {
    if (!currentUser) {
        alert('❌ يجب تسجيل الدخول أولاً');
        return;
    }
    
    // ملء قائمة المحافظ
    const select = document.getElementById('depositWalletType');
    select.innerHTML = '<option value="">-- اختر المحفظة --</option>';
    
    companyWallets.forEach(wallet => {
        const option = document.createElement('option');
        option.value = wallet.id;
        option.textContent = wallet.wallet_name;
        option.dataset.address = wallet.wallet_address;
        select.appendChild(option);
    });
    
    // عرض عنوان المحفظة عند الاختيار
    select.addEventListener('change', function() {
        if (this.value) {
            const selectedOption = this.options[this.selectedIndex];
            document.getElementById('companyWalletAddress').textContent = selectedOption.dataset.address;
            document.getElementById('walletAddressDisplay').classList.remove('hidden');
        } else {
            document.getElementById('walletAddressDisplay').classList.add('hidden');
        }
    });
    
    document.getElementById('depositModal').classList.remove('hidden');
}

function closeDepositModal() {
    document.getElementById('depositModal').classList.add('hidden');
    document.getElementById('depositWalletType').value = '';
    document.getElementById('depositAmount').value = '';
    document.getElementById('depositProof').value = '';
    document.getElementById('walletAddressDisplay').classList.add('hidden');
}

function copyWalletAddress() {
    const address = document.getElementById('companyWalletAddress').textContent;
    navigator.clipboard.writeText(address);
    alert('✅ تم نسخ العنوان');
}

async function submitDeposit() {
    const walletId = document.getElementById('depositWalletType').value;
    const amount = document.getElementById('depositAmount').value;
    const proofFile = document.getElementById('depositProof').files[0];
    
    if (!walletId || !amount || !proofFile) {
        alert('❌ الرجاء ملء جميع الحقول ورفع صورة الإثبات');
        return;
    }
    
    if (parseFloat(amount) <= 0) {
        alert('❌ المبلغ يجب أن يكون أكبر من صفر');
        return;
    }
    
    try {
        const selectedWallet = companyWallets.find(w => w.id == walletId);
        
        const formData = new FormData();
        formData.append('amount', amount);
        formData.append('wallet_type', selectedWallet.wallet_type);
        formData.append('wallet_address', selectedWallet.wallet_address);
        formData.append('proof_image', proofFile);
        
        const response = await fetch(`${API_BASE_URL}/deposit/create`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${authToken}`
            },
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert(`✅ تم إرسال طلب الإيداع بنجاح!\n\nرقم الطلب: ${data.request_number}\n\nسيتم مراجعته خلال 24 ساعة.`);
            closeDepositModal();
            loadDeposits();
            loadUserProfile(); // لتحديث الرصيد
        } else {
            alert('❌ ' + data.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('❌ حدث خطأ في إرسال الطلب');
    }
}

// ==================== Withdrawal Modal ====================

function showWithdrawalModal() {
    if (!currentUser) {
        alert('❌ يجب تسجيل الدخول أولاً');
        return;
    }
    
    if (currentUser.balance < 10) {
        alert('❌ الحد الأدنى للسحب هو $10');
        return;
    }
    
    document.getElementById('withdrawalModal').classList.remove('hidden');
}

function closeWithdrawalModal() {
    document.getElementById('withdrawalModal').classList.add('hidden');
    document.getElementById('withdrawalWalletType').value = 'USDT_TRC20';
    document.getElementById('withdrawalWalletAddress').value = '';
    document.getElementById('withdrawalAmount').value = '';
}

async function submitWithdrawal() {
    const walletType = document.getElementById('withdrawalWalletType').value;
    const walletAddress = document.getElementById('withdrawalWalletAddress').value.trim();
    const amount = document.getElementById('withdrawalAmount').value;
    
    if (!walletType || !walletAddress || !amount) {
        alert('❌ الرجاء ملء جميع الحقول');
        return;
    }
    
    if (parseFloat(amount) < 10) {
        alert('❌ الحد الأدنى للسحب هو $10');
        return;
    }
    
    if (parseFloat(amount) > currentUser.balance) {
        alert('❌ الرصيد غير كافٍ');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/withdrawal/create`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                wallet_type: walletType,
                wallet_address: walletAddress,
                amount: parseFloat(amount)
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert(`✅ تم إرسال طلب السحب بنجاح!\n\nرقم الطلب: ${data.request_number}\n\nسيتم معالجته خلال 24 ساعة.`);
            closeWithdrawalModal();
            loadWithdrawals();
            loadUserProfile();
        } else {
            alert('❌ ' + data.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('❌ حدث خطأ في إرسال الطلب');
    }
}
