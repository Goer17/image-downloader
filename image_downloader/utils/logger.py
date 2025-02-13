import os
import logging
from datetime import datetime
from pathlib import Path

def __logger():
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)

    if not os.path.exists("logs"):
        os.makedirs("logs")
    path = Path("logs") / f"{datetime.now().strftime("%Y-%m-%d")}.log"
    
    file_handler = logging.FileHandler(path)
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
	
    return logger

logger = __logger()