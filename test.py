import subprocess
import shlex
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

def get_public_ip():
    """ Get public IP of this machine to enable increased security """
    command = 'dig +short myip.opendns.com @resolver1.opendns.com'
    proc = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    logging.debug("The command %s is being executed", command)
    out, err = proc.communicate()
    if err:
        logging.error("Error while executing command %s, Error: %s", command, err)
    else:
        logging.debug("The output of command %s is %s", command, out)
    return out.strip().decode('ascii')


logging.debug("The public IP is %s", get_public_ip())