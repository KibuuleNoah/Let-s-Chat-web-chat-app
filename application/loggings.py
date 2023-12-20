import logging

logging.basicConfig(
    level=logging.INFO,
    # filename="app.log", filemode="a"
    format="[%(name)s]:->[%(levelname)s]",
)


def logger(name):
    logger_ = logging.getLogger(name)
    return logger_
