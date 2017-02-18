from oslo_config import cfg
from oslo_log import log
from jinja2 import Environment, FileSystemLoader

CONF = cfg.CONF

opts = [
    cfg.StrOpt('my_ip',
               default="127.0.0.1",
               help=('The admin ip address')),
    cfg.StrOpt('my_fqdn',
               default="localhost",
               help=('The fqdn of this node')),
]

extra_opt = [
    cfg.DictOpt('extra_opts',
                default={},
                help=('The extra options for services')),
]

cli_opts = [
    cfg.BoolOpt('config',
                 default=False,
                 help=('config only')),
    cfg.BoolOpt('service',
                 default=False,
                 help=('service only')),
    cfg.BoolOpt('all',
                 default=False,
                 help=('execute all')),
]


env = Environment(loader=FileSystemLoader(CONF.template_dir))
