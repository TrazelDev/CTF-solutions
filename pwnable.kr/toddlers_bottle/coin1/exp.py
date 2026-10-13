#!/bin/python3
from pwn import *
import re
import math
context.log_level = 'critical'

# remote:
#s = ssh(user='coin1', host='pwnable.kr', password='guest', port=2222)
#io = s.remote('0', 9007)
# local: ( has to be ran locally cause the server is too slow)
io = remote('0', 9007)

io.recv()
sleep(3)

def solve_cycle():
    msg = io.recv().decode()
    coins = int(re.findall('[0-9]+', msg)[0])
    attempts = int(re.findall('[0-9]+', msg)[1])
    log.info(f"attempts: {attempts}")
    log.info(f"coins: {coins}")


    left = 0
    right = (coins // 2) + 1
    for i in range(attempts):
        app_input = str(list(range(left,right,1)))[1:-1].replace(',', '')
        expected_weight = len(range(left,right,1)) * 10
        io.sendline(app_input.encode())
        weight = io.recv().decode()

        log.info(f"app_input: {app_input}")
        log.info(f"expected_weight: {expected_weight}")
        log.info(f"weight: {weight}")

        if int(weight) == expected_weight:
            tmp = right
            right = right + math.ceil((right - left) / 2)
            left = tmp
        else:
            right = left + math.ceil((right - left) / 2)
        log.info(f"right: {right}")
        log.info(f"left: {left}")

    io.sendline(str(left).encode())
    print(io.recvline().decode())

for i in range(100):
    solve_cycle()
io.interactive()
