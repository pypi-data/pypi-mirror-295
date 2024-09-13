import os


def env_read(key, default, TYPE=None):
    if key in os.environ:
        if TYPE is None:
            return os.environ[key]
        else:
            return TYPE(os.environ[key])
    else:
        return default
