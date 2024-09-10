__version__ = "0.1.96"

try:
    from logzio import sender
    import logging


    def get_silent_logger():
        logger = logging.getLogger("silent_logger")
        logger.addHandler(logging.NullHandler())
        return logger


    def patched_get_stdout_logger(debug):
        return get_silent_logger()


    sender.get_stdout_logger = patched_get_stdout_logger
except Exception as e:
    pass
