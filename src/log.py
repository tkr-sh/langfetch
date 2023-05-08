import logging


class log(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[38;5;214m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: f"{grey} {format} {reset}",
        logging.INFO: f"{grey} {format} {reset}",
        logging.WARNING: f"{yellow} {format} {reset}",
        logging.ERROR: f"{red} {format} {reset}",
        logging.CRITICAL: f"{bold_red} {format} {reset}"
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# create logger with 'spam_application'
logger = logging.getLogger("lang_fetch")
logger.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(log())

logger.addHandler(ch)
