from oslo_config import cfg
from oslo_log import log
from oslo_db import options
from pig_manage import paths
from jinja2 import Environment, FileSystemLoader

CONF = cfg.CONF

opts = [
    cfg.StrOpt('my_ip',
               default="127.0.0.1",
               help=('The admin ip address')),
    cfg.StrOpt('my_fqdn',
               default="localhost",
               help=('The fqdn of this node')),
    #cfg.StrOpt('template_dir',
    #           default="/etc/pig_manage/templates",
    #           help=('The virtual ip address')),
    cfg.StrOpt('mysql_password',
               default='zhangwei',
               help=('The password for root and wsrep user')),
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

CONF.register_opts(opts)
#options.set_defaults(CONF, 'sqlite:///' + paths.state_path_def('pig_manage.sqlite'),
#                    'pig_manage.sqlite')


database_group = cfg.OptGroup(name='pig',
                              title='Options for pig manage Database')

sql_opts = [
    cfg.StrOpt('mysql_engine',
               default='InnoDB',
               help='MySQL engine to use.')
]
CONF.register_group(database_group)
CONF.register_opts(sql_opts, group=database_group)

#env = Environment(loader=FileSystemLoader(CONF.template_dir))
#[database]
#connection=mysql://root:zhangwei@127.0.0.1:3306/pig?charset=utf8
