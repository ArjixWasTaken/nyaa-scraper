def save(file, conf):
    with open(file, 'w') as configfile:
        conf.write(configfile)


def getOpts():
    import configparser
    import copy
    import os

    config = configparser.ConfigParser()
    file = os.path.abspath(os.path.join('.', 'config.ini'))
    DEFAULT_OPTIONS = {
        'DEFAULT': {
            'limit': 5,
            'domain_name': 'https://nyaa.si',
            'out_dir': os.path.abspath(os.path.join('.', 'output'))
        }
    }
    if os.path.isfile(file):
        config.read(file)
        for i in DEFAULT_OPTIONS:
            if i not in config:
                config[i] = copy.deepcopy(DEFAULT_OPTIONS[i])
            for x in DEFAULT_OPTIONS[i]:
                if x not in config[i]:
                    config[i][x] = str(copy.deepcopy(DEFAULT_OPTIONS[i][x]))
        save(file, config)

    else:
        for i in DEFAULT_OPTIONS:
            config[i] = DEFAULT_OPTIONS[i]
        save(file, config)
    options = copy.deepcopy(dict(config['DEFAULT']))
    return options
