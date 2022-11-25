import logging
import os
import sys

import azure.functions as func
import fastapi

LOGGING_LVL = os.getenv('LOGGING_LEVEL', 'DEBUG')

logger = logging.getLogger('api-sample')
logger.setLevel(LOGGING_LVL)
logg_formatter = logging.Formatter(
    '%(asctime)s - (%(thread)d, %(threadName)s) - %(levelname)s - %(message)s',
    '%d.%m.%Y %H:%M:%S')

# Console handler
console_rec_auto = logging.StreamHandler()
console_rec_auto.setFormatter(logg_formatter)
logger.addHandler(console_rec_auto)

logger.debug('Logging versions ...')
logger.debug(f'Python: {sys.version}')
logger.debug(f'Azure functions: {func.__version__}')
logger.debug(f'FastAPI: {fastapi.__version__}')

app = fastapi.FastAPI()

# TODO: Add setup or configuration specifications for the application here
