// 实时数据同步功能
class RealtimeSync {
    constructor(options = {}) {
        this.pollInterval = options.pollInterval || 30000; // 30秒轮询一次
        this.maxRetries = options.maxRetries || 3;
        this.currentRetry = 0;
        this.isPolling = false;
        this.lastUpdate = new Date();
        this.endpoints = options.endpoints || {};
        this.callbacks = options.callbacks || {};

        this.init();
    }

    init() {
        console.log('RealtimeSync initialized with', this.pollInterval, 'ms interval');
        this.startPolling();
        this.setupVisibilityHandling();
    }

    setupVisibilityHandling() {
        // 当页面不可见时停止轮询，可见时恢复
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.stopPolling();
                console.log('Polling stopped - page hidden');
            } else {
                this.startPolling();
                console.log('Polling resumed - page visible');
            }
        });
    }

    startPolling() {
        if (this.isPolling) return;

        this.isPolling = true;
        console.log('Starting realtime polling...');

        this.pollTimer = setInterval(() => {
            this.performSync();
        }, this.pollInterval);

        // 立即执行一次同步
        this.performSync();
    }

    stopPolling() {
        if (!this.isPolling) return;

        this.isPolling = false;
        if (this.pollTimer) {
            clearInterval(this.pollTimer);
            this.pollTimer = null;
        }
        console.log('Realtime polling stopped');
    }

    async performSync() {
        if (!this.isPolling) return;

        try {
            console.log('Performing sync check...');

            // 检查学生数据更新
            if (this.endpoints.studentData) {
                await this.checkStudentData();
            }

            // 检查用户列表更新
            if (this.endpoints.userList) {
                await this.checkUserList();
            }

            // 检查待处理学生档案
            if (this.endpoints.pendingProfiles) {
                await this.checkPendingProfiles();
            }

            this.currentRetry = 0;
            this.lastUpdate = new Date();

        } catch (error) {
            console.error('Sync failed:', error);
            this.handleSyncError(error);
        }
    }

    async checkStudentData() {
        try {
            const response = await fetch(this.endpoints.studentData, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'If-Modified-Since': this.lastUpdate.toUTCString()
                }
            });

            if (response.status === 200) {
                const data = await response.json();
                if (data.has_updates && this.callbacks.onStudentDataUpdate) {
                    this.callbacks.onStudentDataUpdate(data);
                }
            }
        } catch (error) {
            console.error('Failed to check student data:', error);
        }
    }

    async checkUserList() {
        try {
            const response = await fetch(this.endpoints.userList, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'If-Modified-Since': this.lastUpdate.toUTCString()
                }
            });

            if (response.status === 200) {
                const data = await response.json();
                if (data.has_updates && this.callbacks.onUserListUpdate) {
                    this.callbacks.onUserListUpdate(data);
                }
            }
        } catch (error) {
            console.error('Failed to check user list:', error);
        }
    }

    async checkPendingProfiles() {
        try {
            const response = await fetch(this.endpoints.pendingProfiles, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'If-Modified-Since': this.lastUpdate.toUTCString()
                }
            });

            if (response.status === 200) {
                const data = await response.json();
                if (data.has_updates && this.callbacks.onPendingProfilesUpdate) {
                    this.callbacks.onPendingProfilesUpdate(data);
                }
            }
        } catch (error) {
            console.error('Failed to check pending profiles:', error);
        }
    }

    handleSyncError(error) {
        this.currentRetry++;

        if (this.currentRetry >= this.maxRetries) {
            console.error('Max retries reached, stopping polling');
            this.stopPolling();

            if (this.callbacks.onSyncError) {
                this.callbacks.onSyncError(error);
            }
        }
    }

    // 手动触发同步
    forceSync() {
        console.log('Force sync triggered');
        this.performSync();
    }

    // 更新轮询间隔
    updatePollInterval(interval) {
        this.pollInterval = interval;
        if (this.isPolling) {
            this.stopPolling();
            this.startPolling();
        }
    }

    // 销毁实例
    destroy() {
        this.stopPolling();
        console.log('RealtimeSync destroyed');
    }
}

// 页面加载完成后自动初始化
document.addEventListener('DOMContentLoaded', function() {
    // 检测当前页面类型并设置相应的端点
    const path = window.location.pathname;
    let syncConfig = {
        pollInterval: 30000,
        maxRetries: 3,
        endpoints: {},
        callbacks: {}
    };

    if (path.includes('/admin_dashboard')) {
        // 管理员仪表板页面
        syncConfig.endpoints = {
            pendingProfiles: '/accounts/api/pending-profiles-count/',
            userList: '/accounts/api/recent-users/'
        };

        syncConfig.callbacks = {
            onPendingProfilesUpdate: function(data) {
                // 更新待处理学生档案数量
                const badge = document.getElementById('pending-profiles-badge');
                if (badge && data.count !== undefined) {
                    badge.textContent = data.count;
                    badge.style.display = data.count > 0 ? 'inline-block' : 'none';
                }

                // 显示通知
                if (data.new_students && data.new_students > 0) {
                    showNotification(`有 ${data.new_students} 名新学生注册需要创建档案`, 'info');
                }
            },

            onUserListUpdate: function(data) {
                // 更新用户统计数据
                const totalUsersEl = document.getElementById('total-users');
                const totalStudentsEl = document.getElementById('total-students');

                if (totalUsersEl && data.total_users !== undefined) {
                    totalUsersEl.textContent = data.total_users;
                }
                if (totalStudentsEl && data.total_students !== undefined) {
                    totalStudentsEl.textContent = data.total_students;
                }
            }
        };
    } else if (path.includes('/student_profiles')) {
        // 学生档案列表页面
        syncConfig.endpoints = {
            studentData: '/accounts/api/student-profiles-updates/'
        };

        syncConfig.callbacks = {
            onStudentDataUpdate: function(data) {
                if (data.updated_profiles && data.updated_profiles.length > 0) {
                    showNotification(`${data.updated_profiles.length} 个学生档案已更新`, 'success');
                    // 可以选择自动刷新页面或部分更新
                    setTimeout(() => {
                        window.location.reload();
                    }, 2000);
                }
            }
        };
    } else if (path.includes('/student_dashboard')) {
        // 学生仪表板页面
        syncConfig.pollInterval = 15000; // 更频繁的检查
        syncConfig.endpoints = {
            studentData: '/students/api/student-status/'
        };

        syncConfig.callbacks = {
            onStudentDataUpdate: function(data) {
                // 更新学生个人状态信息
                if (data.profile_status) {
                    const statusEl = document.getElementById('profile-status');
                    if (statusEl) {
                        statusEl.textContent = data.profile_status;
                    }
                }

                if (data.new_enrollments && data.new_enrollments.length > 0) {
                    showNotification(`您有 ${data.new_enrollments.length} 个新的选课记录`, 'success');
                }
            }
        };
    }

    // 初始化实时同步
    if (Object.keys(syncConfig.endpoints).length > 0) {
        window.realtimeSync = new RealtimeSync(syncConfig);

        // 添加手动刷新按钮功能
        const refreshBtn = document.getElementById('manual-refresh');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', function() {
                this.disabled = true;
                this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 同步中...';

                window.realtimeSync.forceSync();

                setTimeout(() => {
                    this.disabled = false;
                    this.innerHTML = '<i class="fas fa-sync"></i> 手动刷新';
                }, 2000);
            });
        }
    }
});

// 显示通知的辅助函数
function showNotification(message, type = 'info') {
    // 创建通知元素
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        max-width: 500px;
    `;

    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    document.body.appendChild(notification);

    // 自动移除通知
    setTimeout(() => {
        if (notification && notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 5000);
}

// 导出RealtimeSync类供其他脚本使用
window.RealtimeSync = RealtimeSync;