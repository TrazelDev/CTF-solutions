#!/bin/python
import requests
import re

URL = "https://jupiter.challenges.picoctf.org/problem/29835/"
HTML = requests.get(URL).text

def inverse_permuation(p):
    inverse = [0] * len(p)
    for i, v in enumerate(p):
        inverse[v] = i
    return inverse

def get_flag_sections():
    flag_sections = re.findall("'.*'", HTML)
    flag_sections = [s.strip("'") for s in flag_sections]

    return flag_sections

def get_flag_construction_permution():
    reversed_permutation = re.findall("split\*[0-9]\)", HTML)
    reversed_permutation = [0] + [(int(re.findall("[0-9]", o)[0]) - 1) for o in reversed_permutation]

    return inverse_permuation(reversed_permutation)


flag_sections = get_flag_sections()
construction_permutation = get_flag_construction_permution()
flag = ""
for i in construction_permutation:
    flag += flag_sections[i]

print(flag)
# flag = picoCTF{no_clients_plz_7723ce}
