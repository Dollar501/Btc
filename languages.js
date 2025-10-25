// BTC-CloudX Web App - Corrected & Enhanced Script

// --- CORE CLASSES --- //

class Bitcoin3DAnimation {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        if (!this.container) return;
        this.bitcoins = [];
        this.animationId = null;
        this.init();
    }

    init() {
        this.container.style.position = 'absolute';
        this.container.style.width = '100%';
        this.container.style.height = '100%';
        this.container.style.overflow = 'hidden';
        this.container.style.pointerEvents = 'none';
        
        this.createBitcoins(15);
        this.animate();
        
        setInterval(() => {
            if (this.bitcoins.length < 20) this.createBitcoins(1);
        }, 2000);
    }

    createBitcoin() {
        const element = document.createElement('div');
        element.innerHTML = '₿';
        element.style.position = 'absolute';
        element.style.fontSize = '20px';
        element.style.color = '#f7931a';
        element.style.fontWeight = 'bold';
        element.style.textShadow = '0 0 10px rgba(247, 147, 26, 0.5)';
        element.style.userSelect = 'none';
        element.style.zIndex = '1';
        
        const startX = Math.random() * window.innerWidth;
        const startY = Math.random() * window.innerHeight;
        const startZ = Math.random() * -2000 - 1000;
        
        return {
            element,
            x: startX, y: startY, z: startZ,
            speedZ: Math.random() * 3 + 2,
            rotationX: Math.random() * 360, rotationY: Math.random() * 360, rotationZ: Math.random() * 360,
            rotationSpeedX: (Math.random() - 0.5) * 4, rotationSpeedY: (Math.random() - 0.5) * 4,
        };
    }

    createBitcoins(count) {
        for (let i = 0; i < count; i++) {
            const bitcoin = this.createBitcoin();
            this.bitcoins.push(bitcoin);
            this.container.appendChild(bitcoin.element);
        }
    }

    animate() {
        this.bitcoins.forEach((bitcoin, index) => {
            bitcoin.z += bitcoin.speedZ;
            bitcoin.rotationX += bitcoin.rotationSpeedX;
            bitcoin.rotationY += bitcoin.rotationSpeedY;
            
            const scale = Math.max(0.1, (bitcoin.z + 2000) / 2000);
            const opacity = Math.max(0, Math.min(1, (bitcoin.z + 1000) / 1000));
            
            bitcoin.element.style.transform = `translate3d(${bitcoin.x}px, ${bitcoin.y}px, 0) scale(${scale}) rotateX(${bitcoin.rotationX}deg) rotateY(${bitcoin.rotationY}deg)`;
            bitcoin.element.style.opacity = opacity;
            
            if (bitcoin.z > 500 || opacity <= 0) {
                bitcoin.element.remove();
                this.bitcoins.splice(index, 1);
            }
        });
        this.animationId = requestAnimationFrame(() => this.animate());
    }
}

class Navigation {
    constructor() {
        this.pages = document.querySelectorAll('.page');
        this.navButtons = document.querySelectorAll('.nav-btn-bottom');
        this.backButtons = document.querySelectorAll('.back-btn');
        this.init();
    }

    init() {
        const handleNavClick = (pageId) => this.showPage(pageId);

        this.navButtons.forEach(btn => {
            btn.addEventListener('click', () => handleNavClick(btn.dataset.page));
        });

        this.backButtons.forEach(btn => {
            btn.addEventListener('click', () => handleNavClick(btn.dataset.page));
        });

        this.showPage('home-page'); // Show the initial page
    }

    showPage(pageId) {
        if (!pageId) return;

        this.pages.forEach(page => {
            page.classList.toggle('active', page.id === pageId);
        });

        this.navButtons.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.page === pageId);
        });

        window.scrollTo(0, 0);
    }
}

class LanguageManager {
    constructor() {
        this.currentLang = 'ar';
        this.config = {
            ar: { code: 'AR', dir: 'rtl' },
            en: { code: 'EN', dir: 'ltr' },
            zh: { code: 'CH', dir: 'ltr' }
        };
        this.init();
    }

    init() {
        const langToggle = document.getElementById('language-toggle');
        const langDropdown = document.getElementById('language-dropdown');
        const dropdownArrow = document.getElementById('dropdown-arrow');
        
        langToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            langDropdown.classList.toggle('hidden');
            dropdownArrow.style.transform = langDropdown.classList.contains('hidden') ? 'rotate(0deg)' : 'rotate(180deg)';
        });

        document.querySelectorAll('.lang-option').forEach(option => {
            option.addEventListener('click', (e) => {
                this.setLanguage(e.currentTarget.dataset.lang);
                langDropdown.classList.add('hidden');
            });
        });
        
        document.addEventListener('click', () => {
            langDropdown.classList.add('hidden');
            dropdownArrow.style.transform = 'rotate(0deg)';
        });
        
        const savedLang = localStorage.getItem('btc-cloudx-language') || 'ar';
        this.setLanguage(savedLang);
    }

    setLanguage(lang) {
        if (!LANG_PACK[lang]) return;
        this.currentLang = lang;
        const conf = this.config[lang];
        
        document.documentElement.lang = lang;
        document.documentElement.dir = conf.dir;
        document.getElementById('current-lang-text').textContent = conf.code;
        
        this.updateAllText();
        localStorage.setItem('btc-cloudx-language', lang);
    }

    updateAllText() {
        const t = LANG_PACK[this.currentLang];
        const elements = {
            'platform-tagline': t.platform_tagline,
            'article-title': t.article_title, 'article-content': t.article_content, 'article-note': t.article_note,
            'enter-platform-text': t.enter_platform_text, 'maintenance-subtitle': t.maintenance_subtitle,
            'coupon-title': t.coupon_title, 'reveal-coupon-text': t.reveal_coupon_text,
            'coupon-code-label': t.coupon_code_label, 'rewards-title': t.rewards_title,
            'reward-amount': t.reward_amount, 'reward-condition': t.reward_condition,
            'countdown-label': t.countdown_label, 'days-label': t.days_label, 'hours-label': t.hours_label, 'minutes-label': t.minutes_label,
            'nav-home-bottom': t.nav_home, 'nav-plans-bottom': t.nav_plans, 'nav-hardware-bottom': t.nav_hardware,
            'nav-custom-plan-bottom': t.nav_custom_plan, 'nav-faq-bottom': t.nav_faq,
            'plans-title': t.plans_title, 'hardware-title': t.hardware_title, 'custom-plan-title': t.custom_plan_title, 'faq-title': t.faq_title,
            'amount-label': t.amount_label, 'duration-label': t.duration_label,
            'year-1-label': t.year_one, 'year-2-label': t.year_two, 'year-3-label': t.year_three,
            'year-unit': t.year_unit, 'calculate-plan-btn': t.calculate_button,
            'results-title': t.results_title, 'investment-amount-label': t.investment_amount_label,
            'contract-duration-label': t.contract_duration_label, 'daily-profit-label': t.daily_profit,
            'monthly-profit-label': t.monthly_profit, 'total-profit-label': t.total_profit_label, 'roi-label': t.roi_label,
            'confirm-plan-btn': t.confirm_plan_btn, 'modify-plan-btn': t.modify_plan_btn
        };

        for (const id in elements) {
            const el = document.getElementById(id);
            if (el) el.innerHTML = elements[id];
        }
        document.getElementById('investment_amount').placeholder = t.amount_placeholder;
        document.querySelectorAll('.back-text').forEach(el => el.textContent = t.back_text);

        // Re-render dynamic content
        this.renderPlans();
        this.renderHardware();
        this.renderFAQ();
    }

    renderPlans() {
        const container = document.getElementById('plans-container');
        const t = LANG_PACK[this.currentLang];
        const plansData = [
            { price: 200, hash: 10, daily: 0.41, monthly: 12.30, annual: 149.65, bonus: t.bonus_pro, device: 'Antminer S21 XP', name: t.plan_pro_name, desc: t.plan_pro_desc, colors: 'from-green-500/20 to-emerald-500/20 border-green-500/30' },
            { price: 1000, hash: 55, daily: 2.26, monthly: 67.80, annual: 824.90, bonus: t.bonus_adv, device: 'Antminer S21 XP', name: t.plan_adv_name, desc: t.plan_adv_desc, colors: 'from-blue-500/20 to-indigo-500/20 border-blue-500/30' },
            { price: 5000, hash: 295, daily: 12.13, monthly: 363.90, annual: 4427.45, bonus: t.bonus_elite, device: 'S21 XP Hydro', name: t.plan_elite_name, desc: t.plan_elite_desc, colors: 'from-purple-500/20 to-pink-500/20 border-purple-500/30', popular: true },
        ];
        
        container.innerHTML = plansData.map(plan => `
            <div class="plan-card bg-gradient-to-r ${plan.colors} backdrop-blur-md rounded-xl p-6 border shadow-2xl relative">
                ${plan.popular ? `<div class="absolute top-0 right-0 bg-gradient-to-l from-pink-500 to-purple-600 text-white px-4 py-1 rounded-bl-lg text-sm font-bold">${t.most_profitable}</div>` : ''}
                <div class="flex items-center justify-between mb-4 ${plan.popular ? 'mt-6' : ''}">
                    <div><h3 class="text-xl font-bold text-white">${plan.name}</h3><p class="text-sm text-gray-300">${plan.desc}</p></div>
                    <div class="text-right"><p class="text-3xl font-bold text-green-400">$${plan.price}</p><p class="text-sm text-gray-400">${t.min_investment}</p></div>
                </div>
                <div class="grid grid-cols-2 gap-4 mb-6 text-center">
                    <div class="bg-black/30 p-3 rounded-lg"><p class="text-gray-400 text-sm">${t.mining_power}</p><p class="text-lg font-bold text-white">${plan.hash} TH/s</p></div>
                    <div class="bg-black/30 p-3 rounded-lg"><p class="text-gray-400 text-sm">${t.used_device}</p><p class="text-lg font-bold text-white">${plan.device}</p></div>
                    <div class="bg-black/30 p-3 rounded-lg"><p class="text-gray-400 text-sm">${t.daily_profit}</p><p class="text-lg font-bold text-yellow-400">$${plan.daily}</p></div>
                    <div class="bg-black/30 p-3 rounded-lg"><p class="text-gray-400 text-sm">${t.monthly_profit}</p><p class="text-lg font-bold text-orange-400">$${plan.monthly}</p></div>
                    <div class="bg-black/30 p-3 rounded-lg col-span-2"><p class="text-gray-400 text-sm">${t.annual_profit}</p><p class="text-2xl font-bold text-green-500">$${plan.annual}</p></div>
                </div>
                <div class="flex items-center space-x-2 mb-6"><span class="text-green-400">✓</span><span class="text-sm text-gray-300">${plan.bonus}</span></div>
                <button class="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-lg transition-colors">${t.subscribe_now}</button>
            </div>
        `).join('');
    }
    
    renderHardware() {
        const container = document.getElementById('hardware-container');
        const t = LANG_PACK[this.currentLang];
        const hardwareData = [
             { name: t.s21_name, desc: t.s21_desc, hash: '270 TH/s', consumption: '3510W', efficiency: '13 J/TH', daily: '$11.10', available: t.available, colors: 'from-blue-600/20 to-cyan-500/20 border-blue-500/30' },
             { name: t.s21_hydro_name, desc: t.s21_hydro_desc, hash: '295 TH/s', consumption: '5360W', efficiency: '18.1 J/TH', daily: '$12.13', available: t.available, latest: t.latest, colors: 'from-purple-600/20 to-pink-500/20 border-purple-500/30' },
        ];

        container.innerHTML = hardwareData.map(dev => `
            <div class="hardware-card bg-gradient-to-r ${dev.colors} backdrop-blur-md rounded-xl p-6 border shadow-2xl relative">
                ${dev.latest ? `<div class="absolute top-0 right-0 bg-gradient-to-l from-pink-500 to-purple-600 text-white px-4 py-1 rounded-bl-lg text-sm font-bold">${dev.latest}</div>` : ''}
                <div class="flex items-center justify-between mb-6 ${dev.latest ? 'mt-6' : ''}">
                    <div><h3 class="text-2xl font-bold text-white">${dev.name}</h3><p class="text-gray-300">${dev.desc}</p></div>
                    <div class="bg-green-500/20 px-4 py-2 rounded-lg border border-green-500/30"><span class="text-green-400 font-bold">${dev.available}</span></div>
                </div>
                <div class="grid grid-cols-2 gap-4 mb-6 text-center">
                    <div class="bg-black/30 p-4 rounded-lg"><p class="text-gray-400 text-sm">${t.mining_power}</p><p class="text-xl font-bold text-blue-400">${dev.hash}</p></div>
                    <div class="bg-black/30 p-4 rounded-lg"><p class="text-gray-400 text-sm">${t.power_consumption}</p><p class="text-xl font-bold text-yellow-400">${dev.consumption}</p></div>
                    <div class="bg-black/30 p-4 rounded-lg"><p class="text-gray-400 text-sm">${t.efficiency}</p><p class="text-xl font-bold text-green-400">${dev.efficiency}</p></div>
                    <div class="bg-black/30 p-4 rounded-lg"><p class="text-gray-400 text-sm">${t.daily_profit}</p><p class="text-xl font-bold text-orange-400">${dev.daily}</p></div>
                </div>
                 <button class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg transition-colors">${t.book_now}</button>
            </div>
        `).join('');
    }

    renderFAQ() {
        const container = document.getElementById('faq-container');
        const faqData = LANG_PACK[this.currentLang].faq_data;
        container.innerHTML = faqData.map(item => `
            <div class="faq-item bg-gradient-to-r from-gray-800/50 to-gray-700/50 backdrop-blur-md rounded-xl border border-gray-600/30 overflow-hidden">
                <button class="faq-question w-full p-4 text-right font-bold flex justify-between items-center text-white">
                    <span class="text-lg">${item.q}</span>
                    <span class="transform transition-transform duration-200">▼</span>
                </button>
                <div class="faq-answer hidden p-4 pt-0 text-gray-300 bg-black/20">
                    <p class="leading-relaxed">${item.a}</p>
                </div>
            </div>
        `).join('');
        
        document.querySelectorAll('.faq-question').forEach(button => {
            button.addEventListener('click', () => {
                const answer = button.nextElementSibling;
                const item = button.parentElement;
                item.classList.toggle('open');
                answer.classList.toggle('hidden');
                const arrow = button.querySelector('span:last-child');
                arrow.style.transform = item.classList.contains('open') ? 'rotate(180deg)' : 'rotate(0deg)';
            });
        });
    }
}

class CouponSystem {
    constructor() {
        this.revealBtn = document.getElementById('reveal-coupon-btn');
        this.couponContent = document.getElementById('coupon-content');
        this.init();
    }

    init() {
        if (!this.revealBtn) return;
        
        this.revealBtn.addEventListener('click', () => this.revealCoupon());

        if (localStorage.getItem('coupon-revealed') === 'true') {
            this.revealCoupon();
        }
    }

    revealCoupon() {
        this.couponContent.classList.remove('hidden');
        this.revealBtn.style.display = 'none';
        
        // Generate a random-ish code for display
        const userCode = `BTC-X-77-${Math.random().toString(36).substring(2, 9).toUpperCase()}`;
        document.getElementById('user-coupon-code').textContent = userCode;

        this.startCountdown();
        localStorage.setItem('coupon-revealed', 'true');
    }

    startCountdown() {
        let countdownEnd = localStorage.getItem('countdown-end');
        if (!countdownEnd || parseInt(countdownEnd) < Date.now()) {
            countdownEnd = Date.now() + (30 * 24 * 60 * 60 * 1000); // 30 days
            localStorage.setItem('countdown-end', countdownEnd);
        }
        
        const update = () => {
            const timeLeft = parseInt(countdownEnd) - Date.now();
            if (timeLeft <= 0) {
                document.getElementById('days-count').textContent = '00';
                return; // Stop countdown
            }
            const days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
            const hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));

            document.getElementById('days-count').textContent = days.toString().padStart(2, '0');
            document.getElementById('hours-count').textContent = hours.toString().padStart(2, '0');
            document.getElementById('minutes-count').textContent = minutes.toString().padStart(2, '0');
        };

        update();
        setInterval(update, 60000);
    }
}

class CustomPlanCalculator {
    constructor() {
        this.amountInput = document.getElementById('investment_amount');
        this.durationInput = document.getElementById('investment_duration');
        this.durationDisplay = document.getElementById('duration_display');
        this.calculateBtn = document.getElementById('calculate-plan-btn');
        this.resultsDiv = document.getElementById('plan-results');
        this.modifyBtn = document.getElementById('modify-plan-btn');
        this.init();
    }

    init() {
        this.durationInput.addEventListener('input', () => {
            this.durationDisplay.textContent = this.durationInput.value;
        });

        this.calculateBtn.addEventListener('click', () => this.calculate());
        this.modifyBtn.addEventListener('click', () => this.resultsDiv.classList.add('hidden'));
    }

    calculate() {
        const amount = parseFloat(this.amountInput.value) || 0;
        const duration = parseInt(this.durationInput.value);

        if (amount < 200) {
            alert(LANG_PACK[languageManager.currentLang].amount_placeholder);
            return;
        }

        // Simple calculation logic (based on Pro plan ratio: $0.41 daily for $200)
        const baseProfitRatio = 0.41 / 200;
        // Add bonus for longer duration
        const durationBonus = [1, 1.1, 1.25][duration - 1]; 

        const dailyProfit = amount * baseProfitRatio * durationBonus;
        const monthlyProfit = dailyProfit * 30;
        const totalProfit = dailyProfit * 365 * duration;
        const roi = (totalProfit / amount) * 100;

        document.getElementById('display-amount').textContent = `$${amount.toFixed(2)}`;
        document.getElementById('display-duration').textContent = `${duration} ${LANG_PACK[languageManager.currentLang].year_unit}`;
        document.getElementById('display-daily').textContent = `$${dailyProfit.toFixed(2)}`;
        document.getElementById('display-monthly').textContent = `$${monthlyProfit.toFixed(2)}`;
        document.getElementById('display-total').textContent = `$${totalProfit.toFixed(2)}`;
        document.getElementById('display-roi').textContent = `${roi.toFixed(2)}%`;

        this.resultsDiv.classList.remove('hidden');
    }
}

// --- INITIALIZATION --- //

let languageManager; // Make it globally accessible within the script

document.addEventListener('DOMContentLoaded', () => {
    // Initialize components
    new Bitcoin3DAnimation('bitcoin-animation');
    new Navigation();
    languageManager = new LanguageManager(); // Assign to global variable
    new CouponSystem();
    new CustomPlanCalculator();
    
    // Maintenance button alert
    document.getElementById('enter-platform-btn').addEventListener('click', () => {
        const t = LANG_PACK[languageManager.currentLang];
        alert(`${t.article_title}\n\n${t.article_content}\n\n${t.article_note}`);
    });
    
    console.log("✅ BTC-CloudX App Initialized Successfully!");
});