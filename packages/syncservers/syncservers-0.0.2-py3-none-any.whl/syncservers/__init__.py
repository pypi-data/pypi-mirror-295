import logging
from logging.handlers import RotatingFileHandler


LOGGING_FORMAT = "%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s"
LOGGING_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class EasyScheduleFilter(logging.Filter):
    def filter(self, record):
        message= record.getMessage()
        # remove next_run_time messages
        if "next_run_time:" in message:
            return False

        # other rules

        return True


def config_logging(log_file_path, level=logging.INFO):
    logging.basicConfig(
        handlers=[
            RotatingFileHandler(
                filename=log_file_path,
                maxBytes=1024*1024*20,
                backupCount=10,
                encoding="utf-8",
            ),
            logging.StreamHandler(),
        ],
        level=level,
        format=LOGGING_FORMAT,
        datefmt=LOGGING_DATE_FORMAT,
    )

    easy_schedule_logger = logging.getLogger('EasyScheduler')
    easy_schedule_logger.addFilter(EasyScheduleFilter())

def config_test_logging():
    logging.basicConfig(
        level=logging.INFO,
        format=LOGGING_FORMAT,
        datefmt=LOGGING_DATE_FORMAT,
    )
