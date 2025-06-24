import asyncio
import pyshark
import base64


# Explicitly set an event loop
asyncio.set_event_loop(asyncio.new_event_loop())

# Path to your packet file
file_path = './myNetworkTraffic.pcap'

# Open the packet file using FileCapture
capture = pyshark.FileCapture(file_path)
capture = sorted(capture, key=lambda packet: float(packet.frame_info.time_relative))
flag = ""
flag_possible_charaters = set(b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_{}")

for i,packet in enumerate(capture):
    payload = packet.tcp.payload
    hex_strings = payload.split(':')
    ascii_payload = [chr(int(v, 16)) for v in hex_strings]
    s_base64 = ''.join(ascii_payload)
    bin_data = base64.b64decode(s_base64) 

    if all(c in flag_possible_charaters for c in bin_data):
        part_flag = bin_data.decode()
        print(f"{i}. {part_flag}")
        flag += part_flag
print(f"\n\n\n\nflag: {flag}")
