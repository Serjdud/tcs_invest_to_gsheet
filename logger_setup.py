import logging
import sys
import os
import platform
from pathlib import Path

def setup_logging():
    """Setup logging to terminal and system logs for Linux, macOS, and Windows"""
    logger = logging.getLogger('tcs_invest_tracker')
    
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.INFO)
    
    # Formatter for logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 1. Handler for terminal (works on all platforms)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 2. System-specific logging
    system = platform.system()
    if system in ['Linux', 'Darwin']:  # Linux or macOS
        setup_unix_logging(logger, formatter)
    elif system == 'Windows':
        setup_windows_logging(logger, formatter)
    
    logger.info(f"Logging initialized on {system}")
    return logger

def setup_unix_logging(logger, formatter):
    """Setup syslog for Linux and macOS"""
    try:
        import logging.handlers
        
        # Try different syslog addresses for different systems
        syslog_addresses = [
            '/dev/log',           # Most Linux systems
            '/var/run/syslog',    # macOS and some Linux
        ]
        
        for address in syslog_addresses:
            try:
                if os.path.exists(address):
                    syslog_handler = logging.handlers.SysLogHandler(address=address)
                    syslog_handler.setFormatter(formatter)
                    logger.addHandler(syslog_handler)
                    logger.info(f"Syslog configured with address: {address}")
                    break
            except Exception:
                continue
        else:
            logger.warning("Could not connect to any syslog address")
            
    except ImportError:
        logger.warning("SysLogHandler not available")

def setup_windows_logging(logger, formatter):
    """Setup Windows Event Log"""
    try:
        import logging.handlers
        
        # Windows Event Log
        event_log_handler = logging.handlers.NTEventLogHandler('TCSInvestTracker')
        event_log_handler.setFormatter(formatter)
        logger.addHandler(event_log_handler)
        logger.info("Windows Event Log configured")
            
    except ImportError:
        logger.warning("Windows Event Log handler not available")
    except Exception as e:
        logger.warning(f"Windows Event Log setup failed: {e}")

# Create and configure logger
logger = setup_logging()
