import socket
import threading
import pickle
from datetime import datetime
import time


def get_socket(addr):
    s = socket.socket()
    s.connect(addr)
    return s


def handle_message(mess):
    if mess['action'] == 'msg':
        print(f'{mess["from"]}: {mess["message"]} \n')


def prepare_message(message, address):
    mes = {'action': 'msg',
           'time': str(datetime.now()),
           'to': address,
           'from': name,
           'message': message
           }
    return pickle.dumps(mes)


def control():
    while True:
        command = input(
            'Введите команду: 1 - сообщение клиенту 2 - сообщение в группу 3 - присоединиться к группе 4 - для выхода \n')
        if command == '1':
            address = input('Введите адресата: \n')
            message = input('Введите сообщение: \n')
            mes = prepare_message(message, address)
            s.send(mes)
        elif command == '2':
            group = input('Введите номер группы: \n')
            message = input('Введите сообщение: \n')
            mes = prepare_message(message, f'#{group}')
            s.send(mes)
        elif command == '3':
            group = input('Введите номер группы, к которой хотите присоединиться \n')
            mes = {'action':'join',
                   'room':f'#{group}'}
            s.send(pickle.dumps(mes))
        elif command == '4':
            mes = {'action': 'quit'}
            s.send(pickle.dumps(mes))
            s.close()
            break
        time.sleep(1)


def main_loop():
    try:
        while True:
            data = s.recv(1024)
            mes = pickle.loads(data)
            handle_message(mes)
    except Exception as e:
        print(e)
    finally:
        print('Программа закончена')

def get_presence():
    mes = {'action':'presence',
           'time':str(datetime.now()),
           'user': name
           }
    return pickle.dumps(mes)


if __name__ == '__main__':
    addr = ('', 8887)
    s = get_socket(addr)
    name = 'Li'
    print(f'Тебя зовут {name}')
    s.send(get_presence())
    receive = threading.Thread(target=main_loop)
    receive.start()
    cont = threading.Thread(target=control)
    cont.start()
