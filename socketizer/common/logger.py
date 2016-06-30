from django.utils import timezone


def get_logger():
    import logging
    import logging.handlers

    log = logging.getLogger('socketizer')
    log.setLevel(logging.DEBUG)

    handler = logging.handlers.SysLogHandler(address='/var/log')

    log.addHandler(handler)
    return log
