import os
import socket

def get_network_ip():
    '''
    Get the local machine's network IP (not 127.0.0.1).
    ref: http://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib/25850698#25850698
    '''
    if os.name == 'posix':
        # we're on *nix
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.connect(('<broadcast>', 0))
        return s.getsockname()[0]
    else:
        # we're on Windows
        return socket.gethostbyname(socket.gethostname())
