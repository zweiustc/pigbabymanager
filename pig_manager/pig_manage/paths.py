import os

from oslo_config import cfg

path_opts = [
    cfg.StrOpt('pybasedir',
               default=os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                    '../')),
               help='Directory where the kingcloudos python module is installed.'),
    cfg.StrOpt('bindir',
               default='$pybasedir/bin',
               help='Directory where kingcloudos binaries are installed.'),
    cfg.StrOpt('state_path',
               default='$pybasedir',
               help="Top-level directory for maintaining kingcloudos 's state."),
]


def basedir_def(*args):
    """Return an uninterpolated path relative to $pybasedir."""
    return os.path.join('$pybasedir', *args)


def bindir_def(*args):
    """Return an uninterpolated path relative to $bindir."""
    return os.path.join('$bindir', *args)


def state_path_def(*args):
    """Return an uninterpolated path relative to $state_path."""
    return os.path.join('$state_path', *args)


def register_opts(conf):
    conf.register_opts(path_opts)


def list_opts():
    return {
        "DEFAULT": path_opts
    }
