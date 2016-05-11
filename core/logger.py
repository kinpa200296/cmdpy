import logging
import os
from datetime import datetime


def setup_logger(logger):
    logger.setLevel(logging.DEBUG)
    path = os.path.join('logs', '{date}-log.log'.format(date=datetime.now().ctime()))
    path = path.replace(':', ' ')
    if not os.path.isdir('logs'):
        os.mkdir('logs')
    file_handler = logging.FileHandler(path, 'w')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s [%(levelname)s] %(message)s')
    file_handler.setFormatter(file_formatter)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_formatter = logging.Formatter('%(name)s [%(levelname)s] %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


setup_logger(logging.getLogger('cmdpy'))
