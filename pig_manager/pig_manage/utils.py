import json
import requests
import subprocess
from subprocess import PIPE, STDOUT, Popen
from shlex import split
from oslo_log import log

LOG = log.getLogger(__name__)

# Execute shell commands
def execute(cmd, shell=False):
    p = Popen(split(cmd), stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=shell)
    output = p.communicate()[0]
    LOG.info("execute command: %s with returncode %s", cmd, p.returncode)
    LOG.debug(output)
    return p.returncode, output

def call(cmd):
    LOG.info("execute command: %s ", cmd)
    subprocess.call(split(cmd))

def exec_in_background(cmd):
    Popen(["nohup"] + split(cmd))

def exec_with_pipe(cmd1, cmd2):
    p1 = Popen(split(cmd1), stdout=PIPE)
    Popen(split(cmd2), stdin=p1.stdout)
    p1.stdout.close()
    LOG.info('execute command: %s | %s', cmd1, cmd2)

def exec_with_input(cmd, input):
    p = Popen(split(cmd), stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    stdout = p.communicate(input=input)[0]
    LOG.info('execute command: %s with result %s', cmd, stdout)


def post(url, headers, data):
    r = requests.post(url, headers=headers, data=json.dumps(data))
    if r.status_code == 200:
        return r.status_code, r.json()
    return r.status_code, None
