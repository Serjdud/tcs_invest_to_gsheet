import logging
import sys
import logging.handlers

def setup_logging():
    """Setup logging to syslog and terminal"""
    logger = logging.getLogger('tcs_invest_tracker')
    
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.INFO)
    
    # Formatter for logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Handler for terminal
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler for syslog
    try:
        syslog_handler = logging.handlers.SysLogHandler(address='/dev/log')
        syslog_handler.setFormatter(formatter)
        logger.addHandler(syslog_handler)
    except Exception as e:
        logger.warning(f"Failed to setup syslog: {e}")
    
    return logger

# Create and configure logger
logger = setup_logging()