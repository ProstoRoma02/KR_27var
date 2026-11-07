// JavaScript для приложения "Обслуживание серверов"

document.addEventListener('DOMContentLoaded', function() {
    // Инициализация всех функциональностей
    initOperationCards();
    initFilters();
    initStatusColors();
    initPrintButton();
    initDataRefresh();
});

// Функция для инициализации карточек операций
function initOperationCards() {
    const toggleButtons = document.querySelectorAll('.toggle-details');
    
    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const operationId = this.getAttribute('data-operation-id');
            const extraInfo = document.getElementById(`extra-${operationId}`);
            
            if (extraInfo) {
                if (extraInfo.style.display === 'none' || extraInfo.style.display === '') {
                    extraInfo.style.display = 'block';
                    this.innerHTML = '<i class="fas fa-times-circle"></i> Скрыть детали';
                } else {
                    extraInfo.style.display = 'none';
                    this.innerHTML = '<i class="fas fa-info-circle"></i> Детали';
                }
            }
        });
    });
    
    // Добавляем анимацию при наведении на карточки
    const operationCards = document.querySelectorAll('.operation-card');
    operationCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 8px 16px rgba(0,0,0,0.2)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
        });
    });
}

// Функция для инициализации фильтров
function initFilters() {
    const filterForm = document.querySelector('.filter-form');
    if (filterForm) {
        filterForm.addEventListener('submit', function(e) {
            // Показываем индикатор загрузки
            const submitButton = this.querySelector('button[type="submit"]');
            const originalText = submitButton.innerHTML;
            submitButton.innerHTML = '<span class="loading"></span> Загрузка...';
            submitButton.disabled = true;
            
            // Автоматическое скрытие через 5 секунд (на случай если что-то пойдет не так)
            setTimeout(() => {
                submitButton.innerHTML = originalText;
                submitButton.disabled = false;
            }, 5000);
        });
        
        // Валидация числовых полей
        const numberInputs = this.querySelectorAll('input[type="number"]');
        numberInputs.forEach(input => {
            input.addEventListener('input', function() {
                if (this.value < parseInt(this.min)) {
                    this.value = this.min;
                }
                if (this.value > parseInt(this.max)) {
                    this.value = this.max;
                }
            });
        });
    }
}

// Функция для окрашивания элементов по статусу
function initStatusColors() {
    const statusBadges = document.querySelectorAll('.status-badge');
    
    statusBadges.forEach(badge => {
        const status = badge.textContent.toLowerCase();
        
        // Добавляем классы для анимации
        badge.style.transition = 'all 0.3s ease';
        
        // Добавляем эффект пульсации для статуса "выполняется"
        if (status.includes('выполняется') || status.includes('идут работы')) {
            badge.style.animation = 'pulse 2s infinite';
        }
    });
    
    // Создаем анимацию пульсации
    const style = document.createElement('style');
    style.textContent = `
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.7; }
            100% { opacity: 1; }
        }
    `;
    document.head.appendChild(style);
}

// Функция для кнопки печати
function initPrintButton() {
    const printButton = document.querySelector('button[onclick="window.print()"]');
    if (printButton) {
        printButton.addEventListener('click', function() {
            // Показываем сообщение перед печатью
            showNotification('Подготовка страницы к печати...', 'info');
            
            // Добавляем специальные стили для печати
            const printStyle = document.createElement('style');
            printStyle.media = 'print';
            printStyle.textContent = `
                header, footer, .breadcrumb, .operation-actions, .sql-info, .action-card {
                    display: none !important;
                }
                .operation-detail {
                    margin: 0;
                    padding: 0;
                }
                body {
                    font-size: 12pt;
                    line-height: 1.5;
                }
                .info-card {
                    break-inside: avoid;
                    page-break-inside: avoid;
                }
            `;
            document.head.appendChild(printStyle);
            
            // Удаляем стиль после печати
            window.addEventListener('afterprint', function() {
                printStyle.remove();
                showNotification('Печать завершена', 'success');
            });
        });
    }
}

// Функция для обновления данных
function initDataRefresh() {
    const refreshButtons = document.querySelectorAll('[onclick="location.reload()"]');
    
    refreshButtons.forEach(button => {
        button.addEventListener('click', function() {
            showNotification('Обновление данных...', 'info');
            
            // Добавляем индикатор загрузки
            const originalText = this.innerHTML;
            this.innerHTML = '<span class="loading"></span> Обновление...';
            this.disabled = true;
            
            // Сохраняем контекст для восстановления кнопки
            const self = this;
            
            // Автоматическое восстановление через 3 секунды
            setTimeout(() => {
                self.innerHTML = originalText;
                self.disabled = false;
            }, 3000);
        });
    });
    
    // Добавляем обработчик для F5 и Ctrl+R
    document.addEventListener('keydown', function(e) {
        if ((e.key === 'F5') || (e.ctrlKey && e.key === 'r')) {
            e.preventDefault();
            showNotification('Обновление страницы...', 'info');
            setTimeout(() => {
                location.reload();
            }, 500);
        }
    });
}

// Вспомогательная функция для показа уведомлений
function showNotification(message, type = 'info') {
    // Удаляем существующие уведомления
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => notification.remove());
    
    // Создаем новое уведомление
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${getIconForType(type)}"></i>
            <span>${message}</span>
        </div>
        <button class="notification-close">&times;</button>
    `;
    
    // Добавляем стили
    const style = document.createElement('style');
    style.textContent = `
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            display: flex;
            align-items: center;
            gap: 12px;
            z-index: 9999;
            animation: slideIn 0.3s ease-out;
            max-width: 400px;
        }
        
        .notification-info {
            border-left: 4px solid #3498db;
        }
        
        .notification-success {
            border-left: 4px solid #27ae60;
        }
        
        .notification-warning {
            border-left: 4px solid #f39c12;
        }
        
        .notification-error {
            border-left: 4px solid #e74c3c;
        }
        
        .notification-content {
            display: flex;
            align-items: center;
            gap: 10px;
            flex: 1;
        }
        
        .notification-content i {
            font-size: 1.2rem;
        }
        
        .notification-close {
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: #6c757d;
            padding: 0;
            width: 24px;
            height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .notification-close:hover {
            color: #333;
        }
        
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
    
    // Добавляем на страницу
    document.body.appendChild(notification);
    
    // Добавляем обработчик закрытия
    const closeButton = notification.querySelector('.notification-close');
    closeButton.addEventListener('click', function() {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => {
            notification.remove();
            style.remove();
        }, 300);
    });
    
    // Автоматическое закрытие через 5 секунд
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => {
                notification.remove();
                style.remove();
            }, 300);
        }
    }, 5000);
}

// Функция для получения иконки по типу уведомления
function getIconForType(type) {
    switch(type) {
        case 'success': return 'check-circle';
        case 'warning': return 'exclamation-triangle';
        case 'error': return 'times-circle';
        default: return 'info-circle';
    }
}

// Функция для форматирования даты
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Функция для подсветки SQL-кода
function highlightSQL() {
    const sqlBlocks = document.querySelectorAll('pre code');
    
    sqlBlocks.forEach(block => {
        const sql = block.textContent;
        
        // Простая подсветка ключевых слов SQL
        const highlighted = sql.replace(
            /\b(SELECT|FROM|WHERE|JOIN|ON|LEFT|RIGHT|INNER|OUTER|GROUP BY|ORDER BY|HAVING|COUNT|AVG|SUM|MAX|MIN|LIMIT|OFFSET|AND|OR|AS|IN|BETWEEN|LIKE|IS NULL|IS NOT NULL)\b/gi,
            '<span class="sql-keyword">$1</span>'
        ).replace(
            /\b(INSERT|UPDATE|DELETE|CREATE|DROP|TABLE|DATABASE|INDEX|VIEW|TRIGGER|PROCEDURE|FUNCTION)\b/gi,
            '<span class="sql-ddl">$1</span>'
        ).replace(
            /('[^']*'|"[^"]*")/g,
            '<span class="sql-string">$1</span>'
        ).replace(
            /(\d+)/g,
            '<span class="sql-number">$1</span>'
        ).replace(
            /(--.*$)/gm,
            '<span class="sql-comment">$1</span>'
        );
        
        block.innerHTML = highlighted;
    });
    
    // Добавляем стили для подсветки
    const highlightStyle = document.createElement('style');
    highlightStyle.textContent = `
        .sql-keyword { color: #d73a49; font-weight: bold; }
        .sql-ddl { color: #6f42c1; font-weight: bold; }
        .sql-string { color: #032f62; }
        .sql-number { color: #005cc5; }
        .sql-comment { color: #6a737d; font-style: italic; }
    `;
    document.head.appendChild(highlightStyle);
}

// Вызываем подсветку SQL после загрузки DOM
setTimeout(highlightSQL, 100);

// Функция для отслеживания времени выполнения
function trackPerformance() {
    if (window.performance) {
        const timing = window.performance.timing;
        const loadTime = timing.loadEventEnd - timing.navigationStart;
        
        console.log(`Время загрузки страницы: ${loadTime} мс`);
        console.log(`Время до DOMContentLoaded: ${timing.domContentLoadedEventEnd - timing.navigationStart} мс`);
        
        // Логируем в скрытый элемент для отладки
        const perfInfo = document.createElement('div');
        perfInfo.className = 'performance-info hidden';
        perfInfo.innerHTML = `
            <div>Время загрузки: ${loadTime} мс</div>
            <div>Запросов к БД: ${document.querySelectorAll('.sql-snippet').length}</div>
            <div>Операций на странице: ${document.querySelectorAll('.operation-card').length}</div>
        `;
        document.body.appendChild(perfInfo);
    }
}

// Инициализация отслеживания производительности
setTimeout(trackPerformance, 1000);

// Добавляем обработчик для подтверждения сложных действий
function addConfirmations() {
    const resetButton = document.querySelector('a[href*="operation_list"]');
    if (resetButton && resetButton.textContent.includes('Сбросить')) {
        resetButton.addEventListener('click', function(e) {
            if (window.location.search) {
                e.preventDefault();
                if (confirm('Вы уверены, что хотите сбросить все фильтры?')) {
                    window.location.href = this.href;
                }
            }
        });
    }
}

// Инициализация подтверждений
addConfirmations();

// Функция для динамического обновления счетчиков
function updateCounters() {
    const counters = document.querySelectorAll('.stat-value, .results-count strong');
    
    counters.forEach(counter => {
        const originalValue = counter.textContent;
        if (!isNaN(originalValue) && originalValue.trim() !== '') {
            const target = parseInt(originalValue);
            let current = 0;
            const increment = target / 50; // Анимация за 50 шагов
            
            const updateCounter = () => {
                if (current < target) {
                    current += increment;
                    if (current > target) current = target;
                    counter.textContent = Math.floor(current);
                    requestAnimationFrame(updateCounter);
                }
            };
            
            updateCounter();
        }
    });
}

// Запускаем анимацию счетчиков после небольшой задержки
setTimeout(updateCounters, 500);