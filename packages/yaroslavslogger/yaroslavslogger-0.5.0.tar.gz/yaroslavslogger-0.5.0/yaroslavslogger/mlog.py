import logging
import logging.handlers


def init_log(file_name, level=3, console=True):
    if level > 4: level = 4
    loglev = [logging.CRITICAL, logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_file = file_name
    fh = logging.handlers.WatchedFileHandler(log_file)
    fh.setLevel(loglev[level])
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    rh = logging.handlers.RotatingFileHandler(file_name, maxBytes=100000000, backupCount=16)
    logger.addHandler(rh)
    if console:
        ch = logging.StreamHandler()
        ch.setLevel(loglev[level])
        ch.setFormatter(formatter)
        logger.addHandler(ch)

