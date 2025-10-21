// 扩展功能模块 - 中国股市牛市顶部风险分析系统

// 全局变量
let currentProgress = 0;

// 初始化扩展功能
export function initializeExtensions() {
    // 确保DOM加载完成
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', setupExtensions);
    } else {
        setupExtensions();
    }
}

// 设置扩展功能
function setupExtensions() {
    console.log('市场分析器扩展功能初始化');
    
    // 重写refreshData函数
    const originalRefreshData = window.refreshData;
    if (originalRefreshData) {
        window.refreshData = enhancedRefreshData;
    }
    
    // 初始化日志面板
    if (!document.getElementById('errorContent')) {
        console.warn('错误面板未找到');
    }
    
    // 初始化时重置进度步骤
    if (window.resetProgressSteps) {
        window.resetProgressSteps();
    }
}

// 显示日志信息到错误面板
export function logMessage(message, type = 'info') {
    const errorContent = document.getElementById('errorContent');
    if (errorContent) {
        const timestamp = new Date().toLocaleTimeString();
        const logEntry = document.createElement('div');
        logEntry.className = `log-entry log-${type}`;
        logEntry.innerHTML = `<span class="log-time">${timestamp}</span>: ${message}`;
        errorContent.prepend(logEntry);
        
        // 限制日志数量
        if (errorContent.children.length > 50) {
            errorContent.removeChild(errorContent.lastChild);
        }
    } else {
        console.log(`[${type.toUpperCase()}] ${message}`);
    }
}

// 更新进度
export function updateProgress(percent, message) {
    currentProgress = percent;
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    
    if (progressBar && progressText) {
        progressBar.style.width = `${percent}%`;
        progressText.textContent = message || `${percent}%`;
    }
    
    // 记录进度到日志
    logMessage(message, 'info');
}

// 标识数据异常
export function markDataError(elementId, errorType = 'error') {
    const element = document.getElementById(elementId);
    if (element) {
        // 创建异常指示器
        let indicator = element.querySelector('.data-source-indicator');
        if (!indicator) {
            indicator = document.createElement('span');
            indicator.className = 'data-source-indicator';
            element.parentNode.insertBefore(indicator, element.nextSibling);
        }
        
        // 设置指示器样式和文本
        indicator.className = `data-source-indicator indicator-${errorType}`;
        
        if (errorType === 'error') {
            indicator.textContent = '✗ 数据异常';
        } else if (errorType === 'alternative') {
            indicator.textContent = '⚠ 使用备选数据';
        } else if (errorType === 'real') {
            if (indicator.parentNode) {
                indicator.parentNode.removeChild(indicator);
            }
        }
    }
}

// 获取连接模式
export function getConnectionMode() {
    const connectionModeElem = document.getElementById('connectionMode');
    return connectionModeElem ? connectionModeElem.value : 'direct';
}

// 增强的刷新数据函数
function enhancedRefreshData() {
    const refreshBtn = document.getElementById('refreshBtn');
    const refreshText = document.getElementById('refreshText');
    const refreshSpinner = document.getElementById('refreshSpinner');
    const dataStatus = document.getElementById('dataStatus');
    
    // 更新按钮状态
    if (refreshBtn) {
        refreshBtn.classList.add('loading');
    }
    if (refreshText) {
        refreshText.textContent = '获取数据中...';
    }
    if (refreshSpinner) {
        refreshSpinner.style.display = 'inline-block';
    }
    
    // 重置进度步骤
    if (window.resetProgressSteps) {
        window.resetProgressSteps();
    }
    
    // 重置进度条
    updateProgress(0, '准备获取数据...');
    
    // 记录连接模式
    const connectionMode = getConnectionMode();
    logMessage(`使用${connectionMode === 'direct' ? '直接连接(无VPN)' : 'VPN连接'}模式`, 'info');
    
    // 步骤1: 生成初始备选数据
    if (window.updateStepStatus) {
        window.updateStepStatus(0, 'active');
    }
    updateProgress(5, '生成初始备选数据...');
    
    // 尝试执行原始函数的主要逻辑
    try {
        // 立即使用备选数据显示UI
        if (window.generateFallbackData) {
            window.generateFallbackData();
        }
        
        // 步骤2: 更新UI显示
        if (window.updateStepStatus) {
            window.updateStepStatus(1, 'active');
        }
        updateProgress(10, '更新UI显示...');
        // 更新各个UI组件
        if (window.updateDashboard) window.updateDashboard();
        if (window.updateReport) window.updateReport();
        if (window.updateHistorical) window.updateHistorical();
        if (window.updateRawData) window.updateRawData();
        if (window.updateCharts) window.updateCharts();
        if (window.updateHistoricalChart) window.updateHistoricalChart();
        
        // 步骤3: 获取真实市场数据
        if (window.updateStepStatus) {
            window.updateStepStatus(2, 'active');
        }
        updateProgress(15, '开始获取真实市场数据...');
        // 获取真实数据
        if (window.fetchRealMarketData) {
            window.fetchRealMarketData()
                .then(() => {
                    // 步骤4: 更新图表
                    if (window.updateStepStatus) {
                        window.updateStepStatus(3, 'active');
                    }
                    updateProgress(80, '数据获取成功，更新UI显示...');
                    // 成功获取真实数据后更新显示
                    if (window.updateDashboard) window.updateDashboard();
                    if (window.updateReport) window.updateReport();
                    if (window.updateHistorical) window.updateHistorical();
                    if (window.updateRawData) window.updateRawData();
                    if (window.updateCharts) window.updateCharts();
                    if (window.updateHistoricalChart) window.updateHistoricalChart();
                    
                    // 更新状态信息
                    window.lastUpdateTime = new Date();
                    if (dataStatus && window.formatDateTime) {
                        dataStatus.textContent = `数据最后更新: ${window.formatDateTime(window.lastUpdateTime)}`;
                    }
                    
                    // 清除错误标记
                    markDataError('currentIndex', 'real');
                    markDataError('peRatio', 'real');
                    markDataError('pbRatio', 'real');
                    
                    // 步骤5: 完成
                    if (window.updateStepStatus) {
                        window.updateStepStatus(4, 'completed');
                    }
                    updateProgress(100, '数据刷新完成');
                    logMessage('数据获取成功，使用实时数据', 'success');
                })
                .catch(error => {
                    const errorMessage = `获取数据失败: ${error.message || error}`;
                    console.error(errorMessage);
                    logMessage(errorMessage, 'error');
                    
                    // 添加错误标记
                    markDataError('currentIndex', 'error');
                    markDataError('peRatio', 'alternative');
                    markDataError('pbRatio', 'alternative');
                    
                    window.lastUpdateTime = new Date();
                    if (dataStatus && window.formatDateTime) {
                        dataStatus.textContent = `数据最后更新: ${window.formatDateTime(window.lastUpdateTime)} (使用备选数据)`;
                    }
                    
                    // 即使出错也标记为完成
                    if (window.updateStepStatus) {
                        window.updateStepStatus(4, 'completed');
                    }
                    updateProgress(100, '使用备选数据完成');
                    logMessage('已使用备选数据，某些数据源不可用', 'warning');
                })
                .finally(() => {
                    // 恢复按钮状态
                    if (refreshBtn) {
                        refreshBtn.classList.remove('loading');
                    }
                    if (refreshText) {
                        refreshText.textContent = '刷新数据';
                    }
                    if (refreshSpinner) {
                        refreshSpinner.style.display = 'none';
                    }
                });
        } else {
            throw new Error('fetchRealMarketData函数未找到');
        }
    } catch (e) {
        logMessage(`执行刷新数据时出错: ${e.message}`, 'error');
        // 恢复按钮状态
        if (refreshBtn) {
            refreshBtn.classList.remove('loading');
        }
        if (refreshText) {
            refreshText.textContent = '刷新数据';
        }
        if (refreshSpinner) {
            refreshSpinner.style.display = 'none';
        }
        
        // 错误情况下也标记为完成
        if (window.updateStepStatus) {
            window.updateStepStatus(4, 'completed');
        }
    }
}

// 暴露主要函数到全局
if (typeof window !== 'undefined') {
    window.initializeMarketAnalyzerExtensions = initializeExtensions;
    window.logMessage = logMessage;
    window.updateProgress = updateProgress;
    window.markDataError = markDataError;
    window.getConnectionMode = getConnectionMode;
}