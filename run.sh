#!/bin/bash

# Скрипт для запуска main.py под виртуальным окружением
# с дополнительными проверками и логированием

set -e  # Завершать скрипт при первой ошибке

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Функции для цветного вывода
error() { echo -e "${RED}[ERROR]${NC} $1"; }
success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
info() { echo -e "[INFO] $1"; }

# Пути
VENV_DIR=".venv"
PYTHON_SCRIPT="main.py"
REQUIREMENTS_FILE="requirements.txt"

# Проверка зависимостей
check_dependencies() {
    info "Проверка зависимостей..."
    
    if [ ! -d "$VENV_DIR" ]; then
        error "Виртуальное окружение $VENV_DIR не найдено!"
        info "Создайте его командой: python3 -m venv $VENV_DIR"
        exit 1
    fi
    
    if [ ! -f "$PYTHON_SCRIPT" ]; then
        error "Файл $PYTHON_SCRIPT не найден!"
        exit 1
    fi
    
    # Проверяем, установлен ли Python в виртуальном окружении
    if [ ! -f "$VENV_DIR/bin/python" ]; then
        error "Python не найден в виртуальном окружении!"
        exit 1
    fi
}

# Проверка и установка зависимостей из requirements.txt
install_requirements() {
    if [ -f "$REQUIREMENTS_FILE" ]; then
        info "Обнаружен $REQUIREMENTS_FILE, проверяем зависимости..."
        source "$VENV_DIR/bin/activate"
        
        # Проверяем, установлены ли все зависимости
        if ! pip install -r "$REQUIREMENTS_FILE" --quiet; then
            error "Ошибка при установке зависимостей из $REQUIREMENTS_FILE"
            exit 1
        fi
        
        deactivate
        success "Зависимости проверены и установлены"
    else
        warning "Файл $REQUIREMENTS_FILE не найден, пропускаем установку зависимостей"
    fi
}

# Основная функция запуска
run_script() {
    info "Запуск $PYTHON_SCRIPT под виртуальным окружением..."
    
    # Активируем виртуальное окружение
    source "$VENV_DIR/bin/activate"
    
    # Получаем версию Python для информации
    PYTHON_VERSION=$(python --version 2>&1)
    info "Используется: $PYTHON_VERSION"
    
    # Запускаем Python-скрипт
    info "Выполняется: python $PYTHON_SCРИPT $@"
    python "$PYTHON_SCRIPT" "$@"
    
    # Сохраняем код возврата
    EXIT_CODE=$?
    
    # Деактивация
    deactivate
    
    return $EXIT_CODE
}

# Главная функция
main() {
    info "=== Запуск Python-скрипта под виртуальным окружением ==="
    
    check_dependencies
    install_requirements
    
    # Запускаем скрипт, передавая все аргументы
    run_script "$@"
    
    EXIT_CODE=$?
    
    if [ $EXIT_CODE -eq 0 ]; then
        success "Скрипт $PYTHON_SCRIPT завершился успешно"
    else
        error "Скрипт $PYTHON_SCRIPT завершился с ошибкой (код: $EXIT_CODE)"
    fi
    
    exit $EXIT_CODE
}

# Запуск главной функции с передачей всех аргументов
main "$@"