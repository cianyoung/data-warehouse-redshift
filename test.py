import subprocess
import shlex
def get_public_ip():
    """ Get public IP of this machine to enable increased security """
    command = 'dig +short myip.opendns.com @resolver1.opendns.com'
    proc = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    print(shlex.split(command))
    out, err = proc.communicate()
    print(out)
    return out.strip().decode('ascii')

print(get_public_ip())