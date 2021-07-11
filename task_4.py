import subprocess

if __name__ == '__main__':
    server = subprocess.Popen('python3 server/server.py', shell=True)
    n = int(input('Введите количество клиентов мессенджера'))
    for i in range(n):
        client = subprocess.Popen('python3 client/client.py', shell=True)
