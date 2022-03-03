import requests
import random
import os
import vk_api
from python3_anticaptcha import ImageToTextTask
from threading import Thread


class Profile(Thread):
    def __init__(self, token, profile_menu, x):
        Thread.__init__(self)
        self.token = token
        self.profile_menu = profile_menu
        self.x = x

    def run(self):
        if self.profile_menu in [1, 2]:
            if self.profile_menu == 1:
                print(f"https://vk.com/id{self.x} аккаунт закрыл профиль")
                value = 'true'
            else:
                value = 'false'
                print(f"https://vk.com/id{self.x} аккаунт открыл профиль")
            url = 'https://api.vk.com/method/account.setPrivacy'
            params = {
                'access_token': self.token,
                'key': 'closed_profile',
                'value': value,
                'v': 5.92
            }
            requests.get(url=url, params=params)
        else:
            def getlist(filename):
                f = open(filename, encoding='utf-8', errors='ignore')
                return random.choice(f.read().split('\n'))

            name = getlist("name.txt")
            surname = getlist("surname.txt")
            dr = f"{random.randint(1, 28)}.{random.randint(1, 12)}.{random.randint(1950, 2003)}"
            print(f"https://vk.com/{self.x}.{name} {surname} {dr}\n===========")
            params = {
                "lang": "0",
                "v": "5.127",
                "access_token": self.token,
                "sex": "2",
                "bdate": dr,
                "first_name": name,
                "last_name": surname,
                "vkui": "1"
            }
            url = "https://api.vk.com/method/account.saveProfileInfo"
            r = requests.get(url=url, params=params)
            print(r.json())


class AddFriend(Thread):
    def __init__(self, token, addfriend_menu, user_id, captcha_key):
        Thread.__init__(self)
        self.token = token
        self.addfriend_menu = addfriend_menu
        self.user_id = user_id
        self.captcha_key = captcha_key

    def run(self):
        def captcha_handler(captcha):
            key = ImageToTextTask.ImageToTextTask(
                anticaptcha_key=self.captcha_key, save_format='const') \
                .captcha_handler(captcha_link=captcha.get_url())
            return captcha.try_again(key['solution']['text'])
        vk = vk_api.VkApi(token=self.token, captcha_handler=captcha_handler).get_api()
        if self.addfriend_menu == 1:
            vk.friends.add(user_id=self.user_id)
        else:
            vk.friends.delete(user_id=self.user_id)
        params = {
            'v': '5.92',
            'access_token': self.token
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Connection': 'keep-alive'
        }
        url = 'https://api.vk.com/method/users.get'
        a = requests.get(url=url, params=params, headers=headers).json()
        name = a['response'][0]['first_name']
        surname = a['response'][0]['last_name']
        print(f'{name} {surname} добавил в друзья!')
