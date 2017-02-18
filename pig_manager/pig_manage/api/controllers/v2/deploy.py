import os
import pecan
from pecan import rest
import threading
from wsme import types as wtypes

from kingcloudos.api import expose
from kingcloudos.common import exception
from kingcloudos import utils
from kingcloudos import env_config as env_conf

SUPPORT_ACTIONS = {
                   'deploy':
                      {
                        'command': '/usr/bin/startDeploy',
                        'log': 'startDeploy.log',
                      },
                   'deploy_pxe':
                      {
                        'command': '/usr/bin/startPxe',
                        'log': 'startPxe.log',
                      },
                   'add_controller':
                      {
                        'command': '/usr/bin/startDeploy --add-controller',
                        'log': 'startDeploy.log',
                      },
                   'add_compute':
                      {
                        'command': '/usr/bin/startDeploy --add-compute',
                        'log': 'startDeploy.log',
                      },
                   'add_network':
                      {
                        'command': '/usr/bin/startDeploy --add-network',
                        'log': 'startDeploy.log',
                      }
                   }

ACTION_LINES = {}

class DeployController(rest.RestController):
    """REST controller for deployment"""

    def __init__(self):
        super(DeployController, self).__init__()


    @expose.expose(wtypes.text, wtypes.text)
    def get_one(self, action):
        if not SUPPORT_ACTIONS.has_key(action):
            raise exception.ActionNotSupport(action=action)

        log_name = SUPPORT_ACTIONS[action]['log']
        log_file = "{}/{}".format(env_conf.get(key='log_dir'),
                                  log_name)
        if not os.path.isfile(log_file):
            return ""
        returncode, output = utils.execute("wc -l {}".format(log_file))

        total_line = output.split(' ')[0]
        if not ACTION_LINES.has_key(action):
            ACTION_LINES[action] = total_line

        cur_line = ACTION_LINES[action]
        returncode, output = utils.execute("sed -n '{},{}'p {}"
                                  .format(cur_line, total_line, log_file))
        ACTION_LINES[action] = int(total_line) + 1
        return str.replace(output, '\n', '<br>')


    @expose.expose(body=wtypes.DictType(str, str))
    def post(self, actions):
        if not actions.has_key("action"):
            raise exception.BadRequest(field='action')

        action = actions['action']
        if not SUPPORT_ACTIONS.has_key(action):
            raise exception.ActionNotSupport(action=action)

        command = SUPPORT_ACTIONS[action]['command']
        # execute deployment
        thread = threading.Thread(target=utils.execute,
                                  args=(command,))
        thread.daemon = True
        thread.start()
