/**
 * 会话超时管理脚本
 * 10分钟无操作自动退出登录
 */
(function() {
    'use strict';

    // 配置参数
    const config = {
        sessionTimeout: 10 * 60 * 1000, // 10分钟（毫秒）
        warningTime: 2 * 60 * 1000,    // 提前2分钟警告
        checkInterval: 30 * 1000,     // 每30秒检查一次
        warningShown: false,
        userActivityThreshold: 1000    // 1秒内的活动算作用户活跃
    };

    // 会话管理器对象
    const sessionManager = {
        lastActivity: Date.now(),
        warningTimeout: null,
        logoutTimeout: null,
        isActive: true,

        // 初始化
        init: function() {
            this.bindEvents();
            this.startMonitoring();
            console.log('会话超时管理已启动，超时时间：10分钟');
        },

        // 绑定事件监听器
        bindEvents: function() {
            // 用户活动事件
            const activityEvents = [
                'mousedown', 'mousemove', 'keypress', 'scroll',
                'touchstart', 'click', 'focus', 'blur'
            ];

            activityEvents.forEach(event => {
                document.addEventListener(event, this.handleUserActivity.bind(this), {
                    passive: true,
                    capture: true
                });
            });

            // 页面可见性变化
            document.addEventListener('visibilitychange', this.handleVisibilityChange.bind(this));

            // 窗口大小变化
            window.addEventListener('resize', this.handleUserActivity.bind(this));

            // AJAX请求监听
            this.interceptAjaxRequests();
        },

        // 拦截AJAX请求
        interceptAjaxRequests: function() {
            // 保存原始的XMLHttpRequest和fetch
            const originalXHR = window.XMLHttpRequest;
            const originalFetch = window.fetch;

            // 重写XMLHttpRequest
            window.XMLHttpRequest = function() {
                const xhr = new originalXHR();
                const originalOpen = xhr.open;
                const originalSend = xhr.send;

                xhr.open = function(method, url) {
                    // 更新最后活动时间
                    sessionManager.lastActivity = Date.now();
                    return originalOpen.apply(this, arguments);
                };

                xhr.send = function() {
                    // 更新最后活动时间
                    sessionManager.lastActivity = Date.now();
                    return originalSend.apply(this, arguments);
                };

                return xhr;
            };

            // 重写fetch API
            window.fetch = function() {
                // 更新最后活动时间
                sessionManager.lastActivity = Date.now();
                return originalFetch.apply(this, arguments);
            };
        },

        // 处理用户活动
        handleUserActivity: function(event) {
            const now = Date.now();

            // 检查距离上次活动的时间差
            if (now - this.lastActivity > config.userActivityThreshold) {
                this.lastActivity = now;
                this.resetTimers();
            }
        },

        // 处理页面可见性变化
        handleVisibilityChange: function() {
            if (!document.hidden) {
                // 页面变为可见时，重置计时器
                this.lastActivity = Date.now();
                this.resetTimers();
            }
        },

        // 开始监控
        startMonitoring: function() {
            this.resetTimers();

            // 定期检查会话状态
            setInterval(() => {
                this.checkSessionStatus();
            }, config.checkInterval);
        },

        // 重置计时器
        resetTimers: function() {
            // 清除之前的计时器
            this.clearTimers();

            // 如果已经显示了警告，先清除警告
            if (this.warningShown) {
                this.hideWarning();
            }

            // 设置新的超时计时器
            this.logoutTimeout = setTimeout(() => {
                this.forceLogout();
            }, config.sessionTimeout);

            // 设置警告计时器（提前2分钟）
            this.warningTimeout = setTimeout(() => {
                this.showWarning();
            }, config.sessionTimeout - config.warningTime);
        },

        // 清除计时器
        clearTimers: function() {
            if (this.logoutTimeout) {
                clearTimeout(this.logoutTimeout);
                this.logoutTimeout = null;
            }
            if (this.warningTimeout) {
                clearTimeout(this.warningTimeout);
                this.warningTimeout = null;
            }
        },

        // 检查会话状态
        checkSessionStatus: function() {
            const now = Date.now();
            const timeUntilLogout = config.sessionTimeout - (now - this.lastActivity);

            // 如果距离自动登出少于30秒，显示紧急警告
            if (timeUntilLogout > 0 && timeUntilLogout < 30000 && !this.warningShown) {
                this.showUrgentWarning(timeUntilLogout);
            }

            // 如果已经超时
            if (timeUntilLogout <= 0 && this.isActive) {
                this.forceLogout();
            }
        },

        // 显示警告
        showWarning: function() {
            this.warningShown = true;
            this.createWarningModal(false);
        },

        // 显示紧急警告
        showUrgentWarning: function(timeLeft) {
            this.createWarningModal(true, timeLeft);
        },

        // 隐藏警告
        hideWarning: function() {
            this.warningShown = false;
            const modal = document.getElementById('sessionWarningModal');
            if (modal) {
                modal.remove();
            }
        },

        // 创建警告模态框
        createWarningModal: function(urgent, timeLeft) {
            // 移除现有模态框
            const existingModal = document.getElementById('sessionWarningModal');
            if (existingModal) {
                existingModal.remove();
            }

            const modal = document.createElement('div');
            modal.id = 'sessionWarningModal';
            modal.className = 'modal fade show';
            modal.style.display = 'block';
            modal.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
            modal.innerHTML = `
                <div class="modal-dialog modal-dialog-centered" style="margin-top: 10vh;">
                    <div class="modal-content ${urgent ? 'border-danger' : 'border-warning'}" style="border-radius: 15px; overflow: hidden;">
                        <div class="modal-header ${urgent ? 'bg-danger' : 'bg-warning'} text-white py-3">
                            <h5 class="modal-title mb-0">
                                <i class="fas ${urgent ? 'fa-exclamation-triangle' : 'fa-clock'}"></i>
                                ${urgent ? '会话即将过期！' : '会话即将超时'}
                            </h5>
                        </div>
                        <div class="modal-body p-4">
                            <div class="text-center">
                                <div class="mb-3">
                                    <i class="fas fa-user-clock fa-3x text-${urgent ? 'danger' : 'warning'}"></i>
                                </div>
                                <p class="h5 mb-3">
                                    ${urgent ? '您的会话即将过期！' : '您已长时间未操作'}
                                </p>
                                <p class="mb-4 text-muted">
                                    ${urgent ? `将在 <span class="badge badge-danger">${Math.ceil(timeLeft / 1000)}</span> 秒后自动退出登录` : '为保护您的账户安全，系统将在2分钟后自动退出登录'}
                                </p>
                                <div class="progress mb-3" style="height: 8px;">
                                    <div class="progress-bar ${urgent ? 'bg-danger' : 'bg-warning'} progress-bar-striped progress-bar-animated"
                                         role="progressbar"
                                         style="width: ${urgent ? (timeLeft / config.sessionTimeout) * 100 : 80}%;">
                                    </div>
                                </div>
                                ${urgent ?
                                    '<p class="small text-muted">请立即操作以保持登录状态</p>' :
                                    '<p class="small text-muted">继续操作可重置会话时间</p>'
                                }
                            </div>
                        </div>
                        <div class="modal-footer border-top p-3">
                            <div class="container-fluid">
                                <div class="row align-items-center">
                                    <div class="col text-start">
                                        <small class="text-muted">
                                            <i class="fas fa-info-circle"></i>
                                            ${urgent ? '点击"继续操作"或页面任意位置以保持登录' : '会话超时时间：10分钟'}
                                        </small>
                                    </div>
                                    <div class="col text-end">
                                        <button type="button" class="btn btn-${urgent ? 'danger' : 'warning'} btn-sm me-2" onclick="sessionManager.extendSession()">
                                            <i class="fas fa-redo"></i> 继续操作
                                        </button>
                                        <button type="button" class="btn btn-secondary btn-sm" onclick="sessionManager.logout()">
                                            <i class="fas fa-sign-out-alt"></i> 立即退出
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            document.body.appendChild(modal);

            // 添加Bootstrap样式
            const bootstrapCSS = document.createElement('link');
            bootstrapCSS.href = 'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css';
            bootstrapCSS.rel = 'stylesheet';
            document.head.appendChild(bootstrapCSS);

            // 紧急警告时自动播放声音提示（如果可能）
            if (urgent) {
                this.playNotificationSound();
            }
        },

        // 播放提示音
        playNotificationSound: function() {
            try {
                // 创建音频上下文
                const audioContext = new (window.AudioContext || window.webkitAudioContext)();

                // 创建简单的提示音
                const oscillator = audioContext.createOscillator();
                const gainNode = audioContext.createGain();

                oscillator.connect(gainNode);
                gainNode.connect(audioContext.destination);

                oscillator.frequency.value = 800;
                oscillator.type = 'sine';

                gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
                gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);

                oscillator.start(audioContext.currentTime);
                oscillator.stop(audioContext.currentTime + 0.1);
            } catch (e) {
                // 静默处理音频播放错误
                console.log('无法播放提示音:', e);
            }
        },

        // 延长会话
        extendSession: function() {
            this.lastActivity = Date.now();
            this.hideWarning();
            this.resetTimers();

            // 显示成功消息
            this.showMessage('会话时间已延长', 'success');
        },

        // 显示消息
        showMessage: function(message, type) {
            // 移除现有消息
            const existingMessage = document.getElementById('sessionMessage');
            if (existingMessage) {
                existingMessage.remove();
            }

            const messageDiv = document.createElement('div');
            messageDiv.id = 'sessionMessage';
            messageDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
            messageDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 250px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);';
            messageDiv.innerHTML = `
                <div class="d-flex align-items-center">
                    <i class="fas fa-check-circle me-2"></i>
                    ${message}
                    <button type="button" class="btn-close ms-auto" data-bs-dismiss="alert"></button>
                </div>
            `;

            document.body.appendChild(messageDiv);

            // 3秒后自动消失
            setTimeout(() => {
                if (document.getElementById('sessionMessage')) {
                    document.getElementById('sessionMessage').remove();
                }
            }, 3000);
        },

        // 强制退出
        forceLogout: function() {
            this.isActive = false;
            this.clearTimers();

            // 显示退出提示
            this.showLogoutModal();

            // 延迟2秒后执行退出
            setTimeout(() => {
                window.location.href = '/accounts/logout/';
            }, 2000);
        },

        // 显示退出模态框
        showLogoutModal: function() {
            const modal = document.createElement('div');
            modal.className = 'modal fade show';
            modal.style.display = 'block';
            modal.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
            modal.innerHTML = `
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content border-danger">
                        <div class="modal-header bg-danger text-white">
                            <h5 class="modal-title">
                                <i class="fas fa-sign-out-alt"></i>
                                会话已过期
                            </h5>
                        </div>
                        <div class="modal-body text-center p-4">
                            <i class="fas fa-exclamation-triangle fa-3x text-danger mb-3"></i>
                            <h5 class="mb-3">会话已超时</h5>
                            <p class="text-muted mb-4">由于长时间未操作，您的登录会话已过期，将自动跳转到登录页面。</p>
                            <div class="spinner-border text-primary" role="status">
                                <span class="visually-hidden">正在退出...</span>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            document.body.appendChild(modal);
        },

        // 手动退出
        logout: function() {
            this.isActive = false;
            this.clearTimers();
            window.location.href = '/accounts/logout/';
        }
    };

    // 等待DOM加载完成后初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            sessionManager.init();
        });
    } else {
        sessionManager.init();
    }

    // 将会话管理器暴露到全局，以便其他脚本可以调用
    window.sessionManager = sessionManager;
})();