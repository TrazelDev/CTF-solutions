from pwn import *
val = 0x6C5CEC8

if args.LOCAL:
    p = process(['./col', 4*p32(val) + p32(val + 4)])
    p.interactive()
else:
    s = ssh(host='pwnable.kr', port=2222, user='col', password='guest')
    p = s.process(['./col', 4*p32(val) + p32(val + 4)])
    p.interactive()

