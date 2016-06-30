import configparser


def secret_variable(section, key, default=None,
                    config_file='secret_variables.secret_variables'):
    """Reads secret variables from secret_variables.secret_variables file

    The function does not check if the file exists
    """
    cfg = configparser.RawConfigParser()
    cfg.read(config_file)
    if cfg.has_option(section, key):
        return cfg.get(section, key)
    else:
        return default
