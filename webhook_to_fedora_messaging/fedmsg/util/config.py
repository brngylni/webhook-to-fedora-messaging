import os
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))) # This is now the current directory (util)
TEMPLATE = os.path.join(__location__, "template_conf.toml")
CONF_PATH = os.path.join(__location__, "conf.toml") 