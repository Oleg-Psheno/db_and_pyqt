import select
import socket
import pickle


def create_socket(addr) -> socket.socket:
    s = socket.socket()
    s.bind(addr)
    s.listen(5)
    s.settimeout(1)
    return s


def handle_data(data, client, clients):
    print(data)
    if data['action'] == 'msg':
        if data['to'][0] == '#':
            for cl in groups[data['to']]:
                data['flag']='сообщение из группы'
                cl.send(pickle.dumps(data))
        else:
            logins[data['to']].send(pickle.dumps(data))
    elif data['action'] == 'presence':
        logins[data['user']] = client
        print(logins.keys())
    elif data['action'] == 'quit':
        client.close()
        print(f'Клиент {client.fileno()}  отключился')
        clients.remove(client)
        return None
    elif data['action'] == 'join':
        if not groups.get(data['room']):
            groups[data['room']] = []
        groups[data['room']].append(client)
        print('Клиент присоединился к группе')


    return pickle.dumps(data)


def read(r, clients):
    responses = {}
    for client in r:
        try:
            data = client.recv(1024)
            if not data:
                raise Exception
        except:
            print(f'Клиент {client.fileno()} {client.getpeername()} отключился')
            clients.remove(client)
        else:
            responses[client] = handle_data(pickle.loads(data), client, clients)
    return responses


def send(requests, w, clients):
    for sock in requests:
        for client in w:
            try:
                client.send(requests[sock])
            except Exception as e:
                print(e)




def main_loop(addr):
    s = create_socket(addr)

    clients = []
    while True:
        try:
            client, addr = s.accept()
        except OSError as e:
            pass
        else:
            print(f'Получен запрос от клиента {str(addr)}')
            clients.append(client)
        finally:
            wait = 1
            r = []
            w = []
            try:
                r, w, e = select.select(clients, clients, [], wait)
            except Exception as e:
                print(f'Исключение {e}')
            requests = read(r, clients)
            # if requests:
            #     send(requests, w, clients)


if __name__ == '__main__':
    logins = {}
    groups = {}
    addr = ('', 8888)
    main_loop(addr)
