/**
 * 🚀 高级UI框架 - 学生管理系统
 * 现代化交互和动画系统
 */

class AdvancedUISystem {
    constructor() {
        this.version = '2.0.0';
        this.init();
        this.setupEventListeners();
        this.initializeComponents();
        console.log(`🎮 高级UI框架 v${this.version} 已启动`);
    }

    /**
     * 初始化系统
     */
    init() {
        // 检测用户偏好
        this.detectUserPreferences();

        // 初始化主题
        this.initializeTheme();

        // 初始化粒子背景
        this.initializeParticles();

        // 初始化页面加载动画
        this.initializePageLoader();

        // 初始化工具提示
        this.initializeTooltips();

        // 初始化通知系统
        this.initializeNotificationSystem();

        // 初始化性能监控
        this.initializePerformanceMonitoring();
    }

    /**
     * 检测用户偏好
     */
    detectUserPreferences() {
        // 检测系统主题偏好
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            this.setTheme('dark');
        }

        // 检测动画偏好
        if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            document.documentElement.setAttribute('data-reduced-motion', 'true');
        }

        // 检测高对比度
        if (window.matchMedia && window.matchMedia('(prefers-contrast: high)').matches) {
            document.documentElement.setAttribute('data-high-contrast', 'true');
        }
    }

    /**
     * 初始化主题系统
     */
    initializeTheme() {
        const savedTheme = localStorage.getItem('advanced-theme') || 'dark';
        const themeToggle = document.getElementById('themeToggle');

        this.setTheme(savedTheme);

        if (themeToggle) {
            themeToggle.addEventListener('click', () => this.toggleTheme());
        }

        // 监听系统主题变化
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!localStorage.getItem('advanced-theme')) {
                this.setTheme(e.matches ? 'dark' : 'light');
            }
        });
    }

    /**
     * 设置主题
     */
    setTheme(theme) {
        const html = document.documentElement;
        const themeIcon = document.getElementById('themeIcon');

        html.setAttribute('data-theme', theme);
        localStorage.setItem('advanced-theme', theme);

        if (themeIcon) {
            themeIcon.className = theme === 'dark' ? 'fas fa-moon' : 'fas fa-sun';
            themeIcon.title = `切换到${theme === 'dark' ? '亮色' : '暗色'}主题`;
        }

        // 更新meta标签
        const metaTheme = document.querySelector('meta[name="theme-color"]');
        if (metaTheme) {
            metaTheme.content = theme === 'dark' ? '#1a1a2e' : '#ffffff';
        }
    }

    /**
     * 切换主题
     */
    toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

        // 添加切换动画
        const themeToggle = document.getElementById('themeToggle');
        if (themeToggle) {
            themeToggle.style.transform = 'scale(1.2) rotate(720deg)';
            setTimeout(() => {
                themeToggle.style.transform = 'scale(1) rotate(0deg)';
            }, 600);
        }

        this.setTheme(newTheme);

        // 触发主题切换事件
        this.emitEvent('themeChanged', { theme: newTheme, previousTheme: currentTheme });
    }

    /**
     * 初始化粒子背景系统
     */
    initializeParticles() {
        const canvas = document.getElementById('particlesCanvas');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        const particles = [];
        const particleCount = Math.min(50, window.innerWidth / 30);

        class Particle {
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.size = Math.random() * 3 + 1;
                this.speedX = (Math.random() - 0.5) * 0.5;
                this.speedY = (Math.random() - 0.5) * 0.5;
                this.opacity = Math.random() * 0.5 + 0.2;
            }

            update() {
                this.x += this.speedX;
                this.y += this.speedY;

                // 边界检测
                if (this.x > canvas.width) this.x = 0;
                if (this.x < 0) this.x = canvas.width;
                if (this.y > canvas.height) this.y = 0;
                if (this.y < 0) this.y = canvas.height;
            }

            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(102, 126, 234, ${this.opacity})`;
                ctx.fill();
            }
        }

        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }

        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            particles.forEach(particle => particle.update());
            particles.forEach(particle => particle.draw());

            // 连接临近粒子
            for (let i = 0; i < particles.length; i++) {
                for (let j = i + 1; j < particles.length; j++) {
                    const dx = particles[i].x - particles[j].x;
                    const dy = particles[i].y - particles[j].y;
                    const distance = Math.sqrt(dx * dx + dy * dy);

                    if (distance < 150) {
                        ctx.beginPath();
                        ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                        ctx.strokeStyle = `rgba(102, 126, 234, ${0.1 * (1 - distance / 150)})`;
                        ctx.lineWidth = 0.5;
                        ctx.stroke();
                    }
                }
            }

            requestAnimationFrame(animate);
        }

        // 初始化粒子
        for (let i = 0; i < particleCount; i++) {
            particles.push(new Particle());
        }

        resizeCanvas();
        animate();

        window.addEventListener('resize', resizeCanvas);
    }

    /**
     * 初始化页面加载器
     */
    initializePageLoader() {
        const pageLoader = document.getElementById('pageLoader');
        if (!pageLoader) return;

        // 页面加载完成后的处理
        window.addEventListener('load', () => {
            setTimeout(() => {
                pageLoader.classList.add('fade-out');
                setTimeout(() => {
                    pageLoader.style.display = 'none';
                }, 500);
            }, 1000);
        });

        // 页面卸载时显示加载器
        window.addEventListener('beforeunload', () => {
            pageLoader.classList.remove('fade-out');
            pageLoader.style.display = 'flex';
        });
    }

    /**
     * 初始化工具提示
     */
    initializeTooltips() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));

        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl, {
                template: `
                    <div class="tooltip tooltip-advanced" role="tooltip">
                        <div class="tooltip-arrow"></div>
                        <div class="tooltip-inner bg-gradient-primary text-white"></div>
                    </div>
                `,
                delay: { show: 300, hide: 100 },
                animation: true,
                customClass: 'tooltip-advanced'
            });
        });
    }

    /**
     * 初始化通知系统
     */
    initializeNotificationSystem() {
        this.notificationContainer = document.createElement('div');
        this.notificationContainer.className = 'notification-container';
        this.notificationContainer.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            max-width: 400px;
        `;
        document.body.appendChild(this.notificationContainer);

        // 监听全局通知事件
        window.addEventListener('showNotification', (e) => {
            this.showNotification(e.detail);
        });
    }

    /**
     * 显示通知
     */
    showNotification(options) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${options.type || 'info'} fade-in-right`;

        notification.innerHTML = `
            <div class="notification-content">
                <div class="notification-icon">
                    <i class="fas fa-${options.icon || 'info-circle'}"></i>
                </div>
                <div class="notification-body">
                    <h6 class="notification-title">${options.title || '通知'}</h6>
                    <p class="notification-message">${options.message}</p>
                </div>
                <button class="notification-close" onclick="this.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;

        // 添加样式
        notification.style.cssText = `
            background: var(--glass-bg);
            backdrop-filter: var(--glass-blur);
            border: 1px solid var(--glass-border-light);
            border-radius: var(--radius-xl);
            box-shadow: var(--glass-shadow);
            margin-bottom: 10px;
            padding: 15px;
            position: relative;
            overflow: hidden;
        `;

        // 自动移除
        const duration = options.duration || 5000;
        setTimeout(() => {
            notification.classList.add('fade-out-right');
            setTimeout(() => notification.remove(), 300);
        }, duration);

        this.notificationContainer.appendChild(notification);
    }

    /**
     * 初始化性能监控
     */
    initializePerformanceMonitoring() {
        if ('performance' in window && 'PerformanceObserver' in window) {
            // 监控页面加载性能
            const perfObserver = new PerformanceObserver((list) => {
                for (const entry of list.getEntries()) {
                    if (entry.duration > 100) { // 超过100ms的操作
                        console.warn(`⚠️ 慢操作检测: ${entry.name} - ${entry.duration.toFixed(2)}ms`);
                    }
                }
            });

            try {
                perfObserver.observe({ entryTypes: ['measure', 'navigation', 'paint'] });
            } catch (e) {
                console.warn('性能监控初始化失败:', e);
            }
        }

        // 页面可见性变化监控
        document.addEventListener('visibilitychange', () => {
            if (document.visibilityState === 'visible') {
                this.emitEvent('pageVisible');
            } else {
                this.emitEvent('pageHidden');
            }
        });
    }

    /**
     * 设置事件监听器
     */
    setupEventListeners() {
        // 键盘快捷键
        document.addEventListener('keydown', (e) => this.handleKeyboardShortcuts(e));

        // 平滑滚动
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));
                if (target) {
                    this.smoothScrollTo(target);
                }
            });
        });

        // 表单增强
        this.enhanceForms();

        // 按钮增强
        this.enhanceButtons();

        // 卡片悬停增强
        this.enhanceCards();

        // 导航栏滚动效果
        this.setupNavbarScroll();

        // 搜索增强
        this.enhanceSearch();
    }

    /**
     * 处理键盘快捷键
     */
    handleKeyboardShortcuts(e) {
        // Ctrl/Cmd + K 搜索
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('input[type="search"], input[placeholder*="搜索"]');
            if (searchInput) {
                this.highlightElement(searchInput);
                searchInput.focus();
                searchInput.select();
            }
        }

        // Ctrl/Cmd + / 搜索
        if ((e.ctrlKey || e.metaKey) && e.key === '/') {
            e.preventDefault();
            const searchInput = document.querySelector('input[type="search"], input[placeholder*="搜索"]');
            if (searchInput) {
                this.highlightElement(searchInput);
                searchInput.focus();
                searchInput.select();
            }
        }

        // Ctrl/Cmd + Enter 提交表单
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const activeElement = document.activeElement;
            if (activeElement && activeElement.form) {
                e.preventDefault();
                this.submitFormEnhanced(activeElement.form);
            }
        }

        // ESC 关闭模态框
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('.modal.show');
            modals.forEach(modal => {
                const modalInstance = bootstrap.Modal.getInstance(modal);
                if (modalInstance) {
                    modalInstance.hide();
                }
            });

            // 清除搜索框
            const searchInputs = document.querySelectorAll('input[type="search"], input[placeholder*="搜索"]');
            searchInputs.forEach(input => {
                if (input.value) {
                    input.value = '';
                    this.triggerSearch(input);
                }
            });
        }

        // Ctrl/Cmd + L 聚焦用户名
        if ((e.ctrlKey || e.metaKey) && e.key === 'l') {
            e.preventDefault();
            const usernameInput = document.getElementById('id_username');
            if (usernameInput) {
                this.highlightElement(usernameInput);
                usernameInput.focus();
                usernameInput.select();
            }
        }

        // Ctrl/Cmd + P 聚焦密码
        if ((e.ctrlKey || e.metaKey) && e.key === 'p') {
            e.preventDefault();
            const passwordInput = document.getElementById('id_password');
            if (passwordInput) {
                this.highlightElement(passwordInput);
                passwordInput.focus();
            }
        }
    }

    /**
     * 平滑滚动
     */
    smoothScrollTo(target, offset = 80) {
        const targetPosition = target.offsetTop - offset;

        window.scrollTo({
            top: targetPosition,
            behavior: 'smooth',
            block: 'start'
        });
    }

    /**
     * 高亮元素
     */
    highlightElement(element) {
        element.classList.add('highlight-animation');
        setTimeout(() => {
            element.classList.remove('highlight-animation');
        }, 2000);
    }

    /**
     * 增强表单
     */
    enhanceForms() {
        const forms = document.querySelectorAll('form');

        forms.forEach(form => {
            // 添加表单验证增强
            form.addEventListener('submit', (e) => this.handleFormSubmit(e, form));

            // 为输入框添加增强效果
            const inputs = form.querySelectorAll('input, textarea, select');
            inputs.forEach(input => {
                // 聚焦效果
                input.addEventListener('focus', () => {
                    input.parentElement.classList.add('input-focused');
                });

                input.addEventListener('blur', () => {
                    input.parentElement.classList.remove('input-focused');
                });

                // 实时验证
                input.addEventListener('input', () => {
                    this.validateInput(input);
                });
            });
        });
    }

    /**
     * 增强按钮
     */
    enhanceButtons() {
        const buttons = document.querySelectorAll('.btn');

        buttons.forEach(button => {
            // 添加涟漪效果
            button.addEventListener('click', (e) => {
                this.createRippleEffect(e, button);
            });

            // 添加加载状态
            if (button.type === 'submit') {
                const form = button.form;
                if (form) {
                    form.addEventListener('submit', () => {
                        this.setButtonLoading(button);
                    });
                }
            }
        });
    }

    /**
     * 增强卡片
     */
    enhanceCards() {
        const cards = document.querySelectorAll('.card, .glass-card');

        cards.forEach((card, index) => {
            // 添加入场动画
            card.style.animationDelay = `${index * 0.1}s`;
            card.classList.add('fade-in-up');

            // 3D悬停效果（仅桌面端）
            if (window.innerWidth > 768) {
                card.addEventListener('mousemove', (e) => {
                    const rect = card.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;
                    const centerX = rect.width / 2;
                    const centerY = rect.height / 2;

                    const rotateX = (y - centerY) / 10;
                    const rotateY = (centerX - x) / 10;

                    card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(10px)`;
                });

                card.addEventListener('mouseleave', () => {
                    card.style.transform = '';
                });
            }
        });
    }

    /**
     * 设置导航栏滚动效果
     */
    setupNavbarScroll() {
        const navbar = document.querySelector('.navbar-advanced, .navbar');
        if (!navbar) return;

        let lastScroll = 0;

        window.addEventListener('scroll', () => {
            const currentScroll = window.pageYOffset;

            if (currentScroll > 100) {
                navbar.classList.add('scrolled');
                navbar.style.background = 'rgba(26, 26, 46, 0.95)';
                navbar.style.backdropFilter = 'blur(20px)';
            } else {
                navbar.classList.remove('scrolled');
                navbar.style.background = '';
                navbar.style.backdropFilter = '';
            }

            lastScroll = currentScroll;
        });
    }

    /**
     * 增强搜索
     */
    enhanceSearch() {
        const searchInputs = document.querySelectorAll('input[type="search"], input[placeholder*="搜索"]');

        searchInputs.forEach(input => {
            let searchTimer;

            input.addEventListener('input', (e) => {
                clearTimeout(searchTimer);
                searchTimer = setTimeout(() => {
                    this.triggerSearch(input);
                }, 300);
            });

            // 添加搜索历史
            this.setupSearchHistory(input);
        });
    }

    /**
     * 触发搜索
     */
    triggerSearch(input) {
        if (input.value.length >= 2 || input.value.length === 0) {
            const form = input.form;
            if (form) {
                // 显示加载状态
                input.classList.add('searching');

                // 模拟搜索延迟
                setTimeout(() => {
                    input.classList.remove('searching');
                    form.submit();
                }, 500);
            }
        }
    }

    /**
     * 设置搜索历史
     */
    setupSearchHistory(input) {
        const historyKey = 'searchHistory';
        let history = JSON.parse(localStorage.getItem(historyKey) || '[]');

        // 创建搜索建议下拉框
        const suggestionList = document.createElement('div');
        suggestionList.className = 'search-suggestions';

        input.addEventListener('focus', () => {
            if (history.length > 0) {
                this.showSearchSuggestions(history, suggestionList, input);
            }
        });

        input.addEventListener('blur', () => {
            setTimeout(() => suggestionList.remove(), 200);
        });

        // 添加当前搜索到历史
        input.form?.addEventListener('submit', () => {
            if (input.value.trim()) {
                history = history.filter(item => item !== input.value);
                history.unshift(input.value);
                history = history.slice(0, 10); // 保留最近10条
                localStorage.setItem(historyKey, JSON.stringify(history));
            }
        });
    }

    /**
     * 显示搜索建议
     */
    showSearchSuggestions(history, suggestionList, input) {
        suggestionList.innerHTML = `
            <div class="suggestion-header">搜索历史</div>
            ${history.map(item => `
                <div class="suggestion-item" onclick="this.closest('.search-suggestions').previousElementSibling.value='${item}'">
                    <i class="fas fa-history me-2"></i>
                    ${item}
                </div>
            `).join('')}
        `;

        // 定位和显示
        const rect = input.getBoundingClientRect();
        suggestionList.style.cssText = `
            position: absolute;
            top: ${rect.bottom + window.scrollY}px;
            left: ${rect.left + window.scrollX}px;
            width: ${rect.width}px;
            background: var(--glass-bg);
            backdrop-filter: var(--glass-blur);
            border: 1px solid var(--glass-border-light);
            border-radius: var(--radius-lg);
            box-shadow: var(--glass-shadow);
            z-index: 1000;
            max-height: 200px;
            overflow-y: auto;
        `;

        document.body.appendChild(suggestionList);
    }

    /**
     * 创建涟漪效果
     */
    createRippleEffect(e, button) {
        const ripple = document.createElement('span');
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;

        ripple.style.cssText = `
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.5);
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            animation: ripple-animation 0.6s ease-out;
            pointer-events: none;
        `;

        button.appendChild(ripple);

        setTimeout(() => ripple.remove(), 600);
    }

    /**
     * 处理表单提交
     */
    handleFormSubmit(e, form) {
        if (!form.checkValidity()) {
            e.preventDefault();
            e.stopPropagation();

            // 显示验证错误
            this.showFormValidationErrors(form);
        } else {
            this.setFormLoading(form);
        }
    }

    /**
     * 设置按钮加载状态
     */
    setButtonLoading(button) {
        if (!button) return;

        const originalText = button.innerHTML;
        button.disabled = true;
        button.innerHTML = `
            <span class="loading-spinner me-2"></span>
            处理中...
        `;

        // 10秒后恢复
        setTimeout(() => {
            button.disabled = false;
            button.innerHTML = originalText;
        }, 10000);
    }

    /**
     * 设置表单加载状态
     */
    setFormLoading(form) {
        const submitButton = form.querySelector('button[type="submit"]');
        if (submitButton) {
            this.setButtonLoading(submitButton);
        }
    }

    /**
     * 增强提交表单
     */
    submitFormEnhanced(form) {
        const submitButton = form.querySelector('button[type="submit"]');
        if (submitButton && !submitButton.disabled) {
            submitButton.disabled = true;

            // 添加提交动画
            const loadingText = document.createElement('span');
            loadingText.className = 'submit-loading';
            loadingText.innerHTML = '<span class="loading-spinner me-2"></span>提交中...';

            const originalText = submitButton.innerHTML;
            submitButton.innerHTML = '';
            submitButton.appendChild(loadingText);

            // 延迟提交以显示动画
            setTimeout(() => {
                form.submit();
            }, 800);
        }
    }

    /**
     * 验证输入
     */
    validateInput(input) {
        if (input.hasAttribute('required') && !input.value.trim()) {
            input.classList.add('is-invalid');
            input.classList.remove('is-valid');
        } else if (input.value.trim()) {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
        } else {
            input.classList.remove('is-invalid', 'is-valid');
        }
    }

    /**
     * 显示表单验证错误
     */
    showFormValidationErrors(form) {
        const inputs = form.querySelectorAll('input:invalid, textarea:invalid, select:invalid');

        inputs.forEach(input => {
            input.classList.add('shake-animation');

            // 显示错误提示
            const errorTooltip = new bootstrap.Tooltip(input, {
                title: input.validationMessage || '请填写此项',
                placement: 'top',
                trigger: 'manual',
                customClass: 'error-tooltip'
            });

            errorTooltip.show();

            setTimeout(() => {
                input.classList.remove('shake-animation');
                errorTooltip.hide();
            }, 3000);
        });
    }

    /**
     * 初始化组件
     */
    initializeComponents() {
        // 初始化懒加载图片
        this.initializeLazyLoading();

        // 初始化无限滚动
        this.initializeInfiniteScroll();

        // 初始化侧边栏
        this.initializeSidebar();

        // 初始化标签页
        this.initializeTabs();

        // 初始化模态框增强
        this.initializeModals();
    }

    /**
     * 初始化懒加载
     */
    initializeLazyLoading() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src || img.src;
                        img.classList.add('fade-in');
                        imageObserver.unobserve(img);
                    }
                });
            });

            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
    }

    /**
     * 初始化无限滚动
     */
    initializeInfiniteScroll() {
        const contentContainers = document.querySelectorAll('[data-infinite-scroll]');

        contentContainers.forEach(container => {
            let loading = false;
            const page = parseInt(container.dataset.page || '1');

            const loadMore = () => {
                if (loading) return;

                loading = true;
                const nextPage = page + 1;

                // 这里应该实现实际的AJAX加载逻辑
                console.log(`加载第 ${nextPage} 页...`);

                // 模拟加载
                setTimeout(() => {
                    loading = false;
                    container.dataset.page = nextPage;
                }, 2000);
            };

            // 监听滚动
            window.addEventListener('scroll', () => {
                if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 1000) {
                    loadMore();
                }
            });
        });
    }

    /**
     * 初始化侧边栏
     */
    initializeSidebar() {
        const sidebarToggle = document.querySelector('[data-sidebar-toggle]');
        const sidebar = document.querySelector('[data-sidebar]');

        if (sidebarToggle && sidebar) {
            sidebarToggle.addEventListener('click', () => {
                sidebar.classList.toggle('show');
            });
        }
    }

    /**
     * 初始化标签页
     */
    initializeTabs() {
        const tabContainers = document.querySelectorAll('[data-tabs]');

        tabContainers.forEach(container => {
            const tabs = container.querySelectorAll('[data-tab]');
            const panels = container.querySelectorAll('[data-panel]');

            tabs.forEach(tab => {
                tab.addEventListener('click', () => {
                    const targetId = tab.dataset.tab;

                    // 切换标签状态
                    tabs.forEach(t => t.classList.remove('active'));
                    tab.classList.add('active');

                    // 切换面板显示
                    panels.forEach(panel => {
                        if (panel.dataset.panel === targetId) {
                            panel.classList.add('show', 'fade-in');
                        } else {
                            panel.classList.remove('show');
                        }
                    });
                });
            });
        });
    }

    /**
     * 初始化模态框增强
     */
    initializeModals() {
        const modals = document.querySelectorAll('.modal');

        modals.forEach(modal => {
            modal.addEventListener('show.bs.modal', () => {
                modal.classList.add('modal-advanced');
            });

            modal.addEventListener('hidden.bs.modal', () => {
                modal.classList.remove('modal-advanced');
            });
        });
    }

    /**
     * 触发自定义事件
     */
    emitEvent(eventName, data = {}) {
        const event = new CustomEvent(eventName, { detail: data });
        window.dispatchEvent(event);
    }

    /**
     * 全局工具函数
     */
    static utils = {
        // 防抖函数
        debounce(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        },

        // 节流函数
        throttle(func, limit) {
            let inThrottle;
            return function() {
                const args = arguments;
                const context = this;
                if (!inThrottle) {
                    func.apply(context, args);
                    inThrottle = true;
                    setTimeout(() => inThrottle = false, limit);
                }
            };
        },

        // 格式化数字
        formatNumber(num) {
            return new Intl.NumberFormat().format(num);
        },

        // 格式化日期
        formatDate(date, options = {}) {
            const defaults = {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            };

            return new Intl.DateTimeFormat('zh-CN', { ...defaults, ...options }).format(new Date(date));
        },

        // 生成随机颜色
        randomColor() {
            const colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe'];
            return colors[Math.floor(Math.random() * colors.length)];
        },

        // 复制到剪贴板
        async copyToClipboard(text) {
            try {
                await navigator.clipboard.writeText(text);
                window.dispatchEvent(new CustomEvent('showNotification', {
                    detail: {
                        type: 'success',
                        icon: 'check-circle',
                        message: '已复制到剪贴板'
                    }
                }));
            } catch (err) {
                console.error('复制失败:', err);
            }
        },

        // 获取设备信息
        getDeviceInfo() {
            return {
                isMobile: window.innerWidth <= 768,
                isTablet: window.innerWidth > 768 && window.innerWidth <= 1024,
                isDesktop: window.innerWidth > 1024,
                userAgent: navigator.userAgent,
                language: navigator.language,
                platform: navigator.platform
            };
        }
    };
}

// 添加CSS动画样式
const advancedUIStyles = `
    .highlight-animation {
        animation: highlightPulse 2s ease-in-out;
    }

    @keyframes highlightPulse {
        0%, 100% { box-shadow: 0 0 0 rgba(102, 126, 234, 0.4); }
        50% { box-shadow: 0 0 20px rgba(102, 126, 234, 0.8); }
    }

    .shake-animation {
        animation: shake 0.5s ease-in-out;
    }

    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }

    .searching {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Ccircle cx='12' cy='12' r='10' stroke='rgba(102,126,234,0.3)' fill='none' stroke-width='2'/%3E%3Cpath d='M12 6v6l4 2' stroke='rgba(102,126,234,0.8)' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E");
        background-repeat: no-repeat;
        background-position: right 10px center;
        background-size: 16px 16px;
    }

    .submit-loading {
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }

    .loading-spinner {
        width: 16px;
        height: 16px;
        border: 2px solid rgba(255,255,255,0.3);
        border-top: 2px solid #ffffff;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .error-tooltip .tooltip-inner {
        background: var(--danger-gradient) !important;
    }

    .modal-advanced {
        backdrop-filter: blur(10px);
    }

    .search-suggestions {
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-xl);
    }

    .suggestion-header {
        padding: 8px 12px;
        font-weight: 600;
        color: var(--text-secondary);
        border-bottom: 1px solid var(--border-color);
    }

    .suggestion-item {
        padding: 10px 12px;
        cursor: pointer;
        transition: all 0.2s ease;
        color: var(--text-primary);
    }

    .suggestion-item:hover {
        background: rgba(102, 126, 234, 0.1);
        padding-left: 16px;
    }

    .ripple-animation {
        animation: rippleExpand 0.6s ease-out;
        pointer-events: none;
    }

    @keyframes rippleExpand {
        0% {
            transform: scale(0);
            opacity: 1;
        }
        100% {
            transform: scale(4);
            opacity: 0;
        }
    }

    .notification-container .notification {
        animation: slideInRight 0.3s ease-out;
    }

    @keyframes slideInRight {
        0% {
            transform: translateX(100%);
            opacity: 0;
        }
        100% {
            transform: translateX(0);
            opacity: 1;
        }
    }

    .notification-container .notification.fade-out-right {
        animation: slideOutRight 0.3s ease-out;
    }

    @keyframes slideOutRight {
        0% {
            transform: translateX(0);
            opacity: 1;
        }
        100% {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;

// 注入样式
const styleSheet = document.createElement('style');
styleSheet.textContent = advancedUIStyles;
document.head.appendChild(styleSheet);

// 初始化高级UI系统
document.addEventListener('DOMContentLoaded', () => {
    window.advancedUI = new AdvancedUISystem();

    // 导出全局函数
    window.showNotification = (options) => {
        window.dispatchEvent(new CustomEvent('showNotification', { detail: options }));
    };

    window.advancedUtils = AdvancedUISystem.utils;

    console.log('🚀 高级UI系统初始化完成');
    console.log('📋 可用功能:', {
        showNotification: '显示通知',
        advancedUtils: '工具函数集合',
        theme: '主题切换',
        search: '增强搜索',
        forms: '表单增强',
        animations: '动画系统'
    });
});