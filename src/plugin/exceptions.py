import logging
from functools import wraps

LOGGER = logging.getLogger('plugin-peak-shape')


def get_initial_exception(error: Exception) -> Exception:

    parent = error.__cause__ or error.__context__
    if parent is None:
        return error

    return get_initial_exception(parent)


def exception_wrapper(func):

    @wraps(func)
    def wrapped(*args, **kwargs):

        try:
            result = func(*args, **kwargs)

        except Exception as error:
            LOGGER.warning('Restoring shapes ware not completed successfully!')
            raise get_initial_exception(error)

        else:
            LOGGER.info('Restoring shapes are completed!')
            return result

    return wrapped


class PluginError(Exception):
    pass
