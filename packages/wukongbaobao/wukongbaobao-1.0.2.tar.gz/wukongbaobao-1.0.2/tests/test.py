import argparse
import os, sys, subprocess
import shlex
import json
## CVE-2022-30525

## subprocess.getstatusoutput os.system os.open

parser = argparse.ArgumentParser(
    prog='top',
    description='Show top lines from each file')
parser.add_argument('filenames')
# parser.add_argument('-j', action='version')
parser.version = '1.0'

args = parser.parse_args()
for i in range(3):
    # subprocess.check_call(['ping', '223.6.6.6'])
    try:
        # res = subprocess.run(['curl', 'cip.cc'], timeout=2, env = {'aaa': '111'}, capture_output=True, encoding='utf8')
        res = subprocess.check_output(['ping',  '-c 4', '223.6.6.6'])
    except Exception as e:
        print(e)
    else:
        print(i, res)
