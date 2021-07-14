import ipaddress
import subprocess
import tabulate
import re


def host_ping(hosts):
    success_list = []
    loss_list = []
    error_list = []
    for host in hosts:
        if isinstance(host, ipaddress.IPv4Address):
            address = ipaddress.ip_address(host).compressed
        else:
            address = host
        ping = subprocess.Popen(f'ping -W 2 -c 1 {address}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        er = ping.stderr.read()
        if er:
            error_list.append(address)
        else:
            ms = ping.stdout.read()
            loss = float(re.findall(r'(\d{1,3}.\d{1,3})% packet loss', ms.decode())[0])
            if loss <= 50:
                success_list.append(address)
            else:
                loss_list.append(address)
    print(tabulate.tabulate({'success': success_list, 'loss': loss_list, 'errors': error_list}, headers='keys'))


if __name__ == '__main__':
    hosts = ipaddress.ip_network('192.168.0.0/29')
    host_ping(hosts)
