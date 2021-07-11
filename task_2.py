from task_1 import host_ping
import ipaddress

if __name__ == '__main__':
    network = list(ipaddress.IPv4Network('192.168.0.0/24').hosts())
    host_ping(network)
