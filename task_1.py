import re
import subprocess
import pprint
import ipaddress


def host_ping(hosts:list):
    for host in hosts:
        if isinstance(host, ipaddress.IPv4Address):
            address = ipaddress.ip_address(host).compressed
        else:
            address = host
        ping = subprocess.Popen(f'ping -W 2 -c 1 {address}',shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        er = ping.stderr.read()
        if er:
            print(f'Узел {host} не доступен,ошибка запроса')
        else:
            ms = ping.stdout.read()
            loss = float(re.findall(r'(\d{1,3}.\d{1,3})% packet loss', ms.decode())[0])
            if loss <= 50:
                print(f'Узел {host} доступен, ')
            else:
                print(f'Узел {host} не доступен')



if __name__ == '__main__':
    hosts = [
        'ya.ru',
        ipaddress.IPv4Address('192.168.0.1'),
        ipaddress.IPv4Address('192.168.0.20'),
        'ya.ruy'
    ]
    host_ping(hosts)