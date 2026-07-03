#!/bin/bash

# Script to run main.py under virtual environment
# with system log recording

set -e

# Name for log (will appear in syslog)
SCRIPT_NAME="tcs_invest_runner"

# Functions for system log recording
log_info() { 
    logger -t "$SCRIPT_NAME" -p user.info "[INFO] $1"
    echo "[INFO] $1"  # Duplicate to console for convenience
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

# Paths
VENV_DIR=".venv"
PYTHON_SCRIPT="main.py"
REQUIREMENTS_FILE="requirements.txt"

# Check dependencies
check_dependencies() {
    log_info "Checking dependencies..."
    
    if [ ! -d "$VENV_DIR" ]; then
        log_error "Virtual environment $VENV_DIR not found"
        exit 1
    fi
    
    if [ ! -f "$PYTHON_SCRIPT" ]; then
        log_error "File $PYTHON_SCRIPT not found"
        exit 1
    fi
    
    if [ ! -f "$VENV_DIR/bin/python" ]; then
        log_error "Python not found in virtual environment"
        exit 1
    fi
}

# Install dependencies
install_requirements() {
    if [ -f "$REQUIREMENTS_FILE" ]; then
        log_info "Found $REQUIREMENTS_FILE, checking dependencies..."
        source "$VENV_DIR/bin/activate"

        if pip install -r "$REQUIREMENTS_FILE" --quiet; then
            log_success "Dependencies installed"
        else
            log_error "Error installing dependencies"
            exit 1
        fi
        
        deactivate
    else
        log_warning "File $REQUIREMENTS_FILE not found"
    fi
}

# Run Python script
run_script() {
    log_info "Running $PYTHON_SCRIPT under virtual environment"
    
    source "$VENV_DIR/bin/activate"

    # Use MinCifri certificate
    export SSL_TBANK_VERIFY=True
    
    PYTHON_VERSION=$(python --version 2>&1)
    log_info "Using: $PYTHON_VERSION"
    
    log_info "Executing: python $PYTHON_SCRIPT $@"
    
    # Run Python script and log the result
    if python "$PYTHON_SCRIPT" "$@"; then
        log_success "Python script executed successfully"
        EXIT_CODE=0
    else
        EXIT_CODE=$?
        log_error "Python script failed with error (code: $EXIT_CODE)"
    fi
    
    deactivate
    return $EXIT_CODE
}

# Main function
main() {
    log_info "=== Starting Python script under virtual environment ==="
    
    check_dependencies
    install_requirements
    run_script "$@"
    
    EXIT_CODE=$?
    log_info "Script finished with exit code: $EXIT_CODE"
    
    exit $EXIT_CODE
}

# Start
main "$@"