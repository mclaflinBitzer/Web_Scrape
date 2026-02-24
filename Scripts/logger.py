# %%
import logging
import os

# %%
def setup_logger(name:str, log_file: str = "logs/app.log"):
    os.makedirs("logs", exist_ok=True)
    
    logger = logging.getLogger("web_scraping_logger")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# %%



