import ctypes
import time

import psutil
import sys
from ctypes.wintypes import HANDLE, DWORD

# Define constants from the Windows API
# RtlSetProcessIsCritical is not documented btw
#based on https://github.com/dennisbabkin/MakeProcCrit/tree/main
PROCESS_SET_INFORMATION = 0x0200
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
kernel32 = ctypes.windll.kernel32
ntdll = ctypes.windll.ntdll
OpenProcess = kernel32.OpenProcess
NtSetInformationProcess = ntdll.NtSetInformationProcess
CloseHandle = kernel32.CloseHandle


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    pass
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1) # u can remove this and make this script stop if admin rights are not given
    #sys.exit()


class PROCESS_INFORMATION_CLASS(ctypes.c_uint):
    ProcessBreakOnTermination = 0x1D

def make_proc_critical_by_pid(pid, critical=True):
    hProcess = OpenProcess(PROCESS_SET_INFORMATION | PROCESS_QUERY_INFORMATION, False, pid)
    if not hProcess:
        error_code = kernel32.GetLastError()
        print(f"Failed to open process with PID: {pid}. Error code: {error_code}")
        return False

    break_on_termination = ctypes.c_uint32(1 if critical else 0)
    status = NtSetInformationProcess(hProcess, PROCESS_INFORMATION_CLASS.ProcessBreakOnTermination, ctypes.byref(break_on_termination), ctypes.sizeof(break_on_termination))

    if status != 0:
        print(f"Failed to change critical status. Status code: {status}")
        CloseHandle(hProcess)
        return False

    CloseHandle(hProcess)
    return True

def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py [on|off] [pid|process_name]")
        return

    action = sys.argv[1].lower()
    identifier = sys.argv[2]

    if action not in ["on", "off", "1", "0"]:
        print("Invalid action. Use 'on' or 'off'.")
        return

    critical = action in ["on", "1"]

    if identifier.isdigit():
        pid = int(identifier)
        if make_proc_critical_by_pid(pid, critical):
            print(f"Successfully {'made critical' if critical else 'removed critical status from'} process PID: {pid}")
        else:
            print(f"Failed to {'make critical' if critical else 'remove critical status from'} process PID: {pid}")
    else:
        process_name = identifier if identifier.endswith('.exe') else f"{identifier}.exe"
        found = False
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'].lower() == process_name.lower():
                pid = proc.info['pid']
                if make_proc_critical_by_pid(pid, critical):
                    print(f"Successfully {'made critical' if critical else 'removed critical status from'} process PID: {pid}")
                else:
                    print(f"Failed to {'make critical' if critical else 'remove critical status from'} process PID: {pid}")
                found = True
                break
        if not found:
            print(f"Process '{process_name}' not found.")

if __name__ == "__main__":
    main()
    time.sleep(3)
