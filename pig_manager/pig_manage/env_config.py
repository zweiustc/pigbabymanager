import ConfigParser
from oslo_config import cfg

config_file = "/etc/pig/installer-env.conf"
configParser = ConfigParser.ConfigParser()
configParser.read(config_file)

def get(section='DEFAULT', key=''):
    if has_option(section, key):
        return configParser.get(section, key)
    return None

def set(section='DEFAULT', key='', value=''):
    return configParser.set(section, key, value)

def add_section(section):
    configParser.add_section(section)

def remove_section(section):
    configParser.remove_section(section)

def write():
    with open(config_file, 'w+') as fout:
        configParser.write(fout)

def has_option(section='DEFAULT', key=''):
    return configParser.has_option(section, key)

def _build_nodes(nodes):
    results = []
    if nodes != "":
        for n in nodes.split(','):
            results.append(n.strip())
    return results
