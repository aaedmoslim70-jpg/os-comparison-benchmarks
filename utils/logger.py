import logging
import os
from datetime import datetime

def setup_logger():
    """إعداد نظام السجلات"""
    os.makedirs('logs', exist_ok=True)
    
    logger = logging.getLogger('OSComparison')
    logger.setLevel(logging.DEBUG)
    
    # تجنب إضافة handlers متعددة
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # File handler
    handler = logging.FileHandler(f'logs/benchmark_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger
