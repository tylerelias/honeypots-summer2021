import subprocess
import time

import read_json_log
import ip_addr
from datetime import datetime


IP_ADDR = 'FILL_OUT'
PORT = 8125


def send_data(data):
    for item in data:
        command = f'echo -n "{item["query"]}:{item["lat"]}:{item["lon"]}|c " | nc -w 1 -u {IP_ADDR} {PORT}'
        ps = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
        )
        print(f'Sending for: {item["query"]}')


if __name__ == '__main__':
    ip_addr_dict = ip_addr.load_ip_addr()
    send_data(ip_addr_dict)
