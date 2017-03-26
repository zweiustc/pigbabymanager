import logging
import os
import sys
from wsgiref import simple_server

from oslo_config import cfg
from oslo_log import log
from six.moves import socketserver

from pig_manage.api import app

CONF = cfg.CONF


class ThreadedSimpleServer(socketserver.ThreadingMixIn,
                           simple_server.WSGIServer):
    """A Mixin class to make the API service greenthread-able."""
    pass


def main():
    log.register_options(CONF)
    CONF(default_config_files=['/etc/pig_manage/pig_manage.conf'])
    log.setup(CONF, 'pig_manage')

    # Build and start the WSGI app
    host = '0.0.0.0'
    port = 8888
    wsgi = simple_server.make_server(
            host, port,
            app.VersionSelectorApplication(),
            server_class=ThreadedSimpleServer)

    LOG = log.getLogger(__name__)
    LOG.info("Serving on http://%(host)s:%(port)s",
             {'host': host, 'port': port})
    LOG.info("Configuration:")
    CONF.log_opt_values(LOG, logging.DEBUG)

    try:
        wsgi.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    
    #path = os.path.abspath(
    #    os.path.dirname(os.path.dirname(__file__)))
    #python_path = os.environ.get("PYTHONPATH")
    #if not python_path:
    #    python_path = path
    #else:
    #    python_path += ';' + path
    #os.environ['PYTHONPATH'] = python_path

    main()
