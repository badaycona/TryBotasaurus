import logging
import os

def get_logger(name):
    os.makedirs('logs', exist_ok=True)
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.FileHandler(f'logs/{name}.log', encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
