import socket

class Server:
    def __init__(self):
       
        self.host = ''       # Symbolic name meaning all available interfaces
        self.port = 12345    # Arbitrary non-privileged port

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(0.5)
        self.s.bind((self.host, self.port))

        self.conn = []
        self.addr = []

        self.s.listen(10)

    def connect_new(self):
        try:
            new_conn, new_addr = self.s.accept()
            self.conn.append(new_conn)
            self.addr.append(new_addr)

            data = self.conn[-1].recv(1024)
            team_name = data.decode('utf-8')

            if team_name != 'None':
                return (True, team_name)
            else:
                return (True, None)
        except socket.timeout:
            return (False, None)
        except:
            raise
        
    def send(self, conn_number, data):
        try:
            self.conn[conn_number].sendall(data)
        except socket.error:
            self.close(conn_number)
            raise ConnectionError("Connection was closed")

    def close(self, conn_number):
        self.conn[conn_number].close()
    
    def close_all(self):
        for c in self.conn:
            c.close()
