# RtlSetProcessIsCritical

`RtlSetProcessIsCritical` is a Python script that interacts with Windows API to set a process as critical, ensuring it can't be terminated. This can be useful in scenarios where you want to safeguard critical processes from accidental or unauthorized termination.

## Features

- Set a process as critical to prevent it from being terminated. Can be useful for software/malware protection.
- ❗❗❗BSOD on termination.❗❗❗
- Uses Windows API calls to achieve the functionality.
- Simple and easy-to-use command-line interface.
- ❗ADMIN REQUIRED❗

## Usage 

python main.py [on|off] [pid|process_name]

## Editing

- You can edit the script numerous ways, like make the parent process critical for example
- 😥 At least give some credits if you are using my python version (BASED ON https://github.com/LocalAlloc/RtlSetProcessIsCritical)
