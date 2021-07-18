import select
import socket
import pickle


class ServerVerifier(type):
    def __init__(self, data):
        self._data = data


class ChatServer():
    def __init__(self, addr):
        self.socket = socket.socket()
        self.socket.bind(addr)
        self.socket.listen(5)
        self.socket.settimeout(1)
        self.clients = []
        self.groups = {}
        self.logins = {}

    def handle_data(self, data, client):
        print(data)
        if data['action'] == 'msg':
            if data['to'][0] == '#':
                for cl in self.groups[data['to']]:
                    data['flag'] = 'сообщение из группы'
                    cl.send(pickle.dumps(data))
            else:
                self.logins[data['to']].send(pickle.dumps(data)) #todo - client can be absent in clients
        elif data['action'] == 'presence':
            self.logins[data['user']] = client
            print(self.logins.keys())
        elif data['action'] == 'quit':
            client.close()
            print(f'Клиент {client.fileno()}  отключился')
            self.clients.remove(client)
            return None
        elif data['action'] == 'join':
            if not self.groups.get(data['room']):
                self.groups[data['room']] = []
            self.groups[data['room']].append(client)
            print('Клиент присоединился к группе')

    def read(self, r):
        responses = {}
        for client in r:
            try:
                data = client.recv(1024)
                if not data:
                    raise Exception
            except:
                print(f'Клиент {client.fileno()} {client.getpeername()} отключился')
                self.clients.remove(client)
            else:
                responses[client] = self.handle_data(pickle.loads(data), client)
        return responses

    def send(self, requests, w):
        for sock in requests:
            for client in w:
                try:
                    client.send(requests[sock])
                except Exception as e:
                    print(e)

    def main_loop(self):
        while True:
            try:
                client, addr = self.socket.accept()
            except OSError as e:
                pass
            else:
                print(f'Получен запрос от клиента {str(addr)}')
                self.clients.append(client)
            finally:
                wait = 1
                r = []
                w = []
                try:
                    r, w, e = select.select(self.clients, self.clients, [], wait)
                except Exception as e:
                    print(f'Исключение {e}')
                requests = self.read(r)
                # if requests:
                #     send(requests, w, clients)


if __name__ == '__main__':
    addr = ('', 8887)
    serv = ChatServer(addr)
    serv.main_loop()
