import socket
import select

class Client:
    def __init__(self, ip_address):
        if ip_address == True:
            self.host = socket.gethostname()  # This connects to itself
        else:
            self.host = ip_address
        self.port = 12345   # The same port as used by the server

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, team_name=None):
        self.s.connect((self.host, self.port))

        if team_name:
            data = bytes(team_name, 'utf-8')
            self.s.sendall(data)
        else:
            data = bytes('None', 'utf-8')
            self.s.sendall(data)

    def receive(self):
        r, _, _ = select.select([self.s], [self.s], [])
        if len(r):
            data = self.s.recv(1024)
            if not data:
                raise ConnectionError("Connection was closed")
            
            string = data.decode('utf-8')
            commands = string.rstrip('\n').split('\n')
            return (True, commands)
        else:
            return (False, None)

    def close(self):
        self.s.close()