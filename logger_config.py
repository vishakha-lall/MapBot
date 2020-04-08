from functools import wraps
import logging

FORMAT = "%(asctime)s - %(name)-s - %(levelname)-s - %(message)s"
LEVEL = logging.DEBUG
logging.basicConfig(format=FORMAT, level=LEVEL)
log = logging.getLogger(__name__)


def logger(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        log = logging.getLogger(fn.__name__)
        log.info("About to run %s" % fn.__name__)
        out = fn(*args, **kwargs)
        log.info("Done running %s" % fn.__name__)
        return out

    return wrapper
