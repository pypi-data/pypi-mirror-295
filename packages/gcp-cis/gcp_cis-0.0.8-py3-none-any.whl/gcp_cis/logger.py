import logging
from logging.handlers import RotatingFileHandler


class Logger:
    def __init__(self):
        self.logger = None

    def create_log_handler(self, log_file_path, job_name="GCP_CIS", level=logging.DEBUG):
        handler = RotatingFileHandler(
            log_file_path, maxBytes=5000000, backupCount=7, encoding="utf-8"
        )

        formatter = logging.Formatter(
            "%(asctime)s %(name)s %(levelname)s: %(message)s")
        handler.setFormatter(formatter)

        self.logger = logging.getLogger(job_name)
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        self.logger.addHandler(handler)
        self.logger.setLevel(level)
