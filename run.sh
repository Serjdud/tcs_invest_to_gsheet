#!/bin/bash

# Скрипт для запуска main.py под виртуальным окружением
# с записью в системный лог

set -e

# Имя для лога (будет отображаться в syslog)
SCRIPT_NAME="tcs_invest_runner"

# Функции для записи в системный лог
log_info() { 
    logger -t "$SCRIPT_NAME" -p user.info "[INFO] $1"
    echo "[INFO] $1"  # Дублируем в консоль для удобства
}

log_success() { 
    logger -t "$SCRIPT_NAME" -p user.info "[SUCCESS] $1"
    echo "[SUCCESS] $1"
}

log_warning() { 
    logger -t "$SCRIPT_NAME" -p user.warn "[WARNING] $1"
    echo "[WARNING] $1"
}

log_error() { 
    logger -t "$SCRIPT_NAME" -p user.err "[ERROR] $1"
    echo "[ERROR] $1" >&2
}

# Пути
VENV_DIR=".venv"
PYTHON_SCRIPT="main.py"
REQUIREMENTS_FILE="requirements.txt"

# Проверка зависимостей
check_dependencies() {
    log_info "Проверка зависимостей..."
    
    if [ ! -d "$VENV_DIR" ]; then
        log_error "Виртуальное окружение $VENV_DIR не найдено"
        exit 1
    fi
    
    if [ ! -f "$PYTHON_SCRIPT" ]; then
        log_error "Файл $PYTHON_SCRIPT не найден"
        exit 1
    fi
    
    if [ ! -f "$VENV_DIR/bin/python" ]; then
        log_error "Python не найден в виртуальном окружении"
        exit 1
    fi
}

# Установка зависимостей
install_requirements() {
    if [ -f "$REQUIREMENTS_FILE" ]; then
        log_info "Обнаружен $REQUIREMENTS_FILE, проверяем зависимости..."
        source "$VENV_DIR/bin/activate"
        
        if pip install -r "$REQUIREMENTS_FILE" --quiet; then
            log_success "Зависимости установлены"
        else
            log_error "Ошибка при установке зависимостей"
            exit 1
        fi
        
        deactivate
    else
        log_warning "Файл $REQUIREMENTS_FILE не найден"
    fi
}

# Запуск Python-скрипта
run_script() {
    log_info "Запуск $PYTHON_SCRIPT под виртуальным окружением"
    
    source "$VENV_DIR/bin/activate"
    
    PYTHON_VERSION=$(python --version 2>&1)
    log_info "Используется: $PYTHON_VERSION"
    
    log_info "Выполняется: python $PYTHON_SCRIPT $@"
    
    # Запускаем Python-скрипт и логируем результат
    if python "$PYTHON_SCRIPT" "$@"; then
        log_success "Python-скрипт выполнен успешно"
        EXIT_CODE=0
    else
        EXIT_CODE=$?
        log_error "Python-скрипт завершился с ошибкой (код: $EXIT_CODE)"
    fi
    
    deactivate
    return $EXIT_CODE
}

# Главная функция
main() {
    log_info "=== Запуск Python-скрипта под виртуальным окружением ==="
    
    check_dependencies
    install_requirements
    run_script "$@"
    
    EXIT_CODE=$?
    log_info "Скрипт завершил работу с кодом: $EXIT_CODE"
    
    exit $EXIT_CODE
}

# Запуск
main "$@"