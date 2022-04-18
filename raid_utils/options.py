import requests
import os
import random

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0',
    'Connection': 'keep-alive'
}


def get_id(token, user_id):
    params = {
        'v': '5.92',
        'access_token': token,
        'screen_name': user_id
    }
    url = 'https://api.vk.com/method/utils.resolveScreenName'
    rq = requests.get(url=url, params=params, headers=headers).json()
    if str(rq['response']['type']) == 'user':
        return str(rq['response']['object_id'])
    else:
        return str(rq['response']['object_id']*-1)


def get_full_link(link, token):
    params = {
        'access_token': token,
        'v': '5.92',
        'url': link,
    }
    url = 'https://api.vk.com/method/utils.checkLink'
    rq = requests.get(url=url, params=params, headers=headers).json()
    print('Ссылка на беседу:\n'+rq['response']['link'])


def invite_bots(token, conf_id, bots):
    for bot in bots:
        params = {
            'v': '5.92',
            'access_token': token,
            'peer_id': conf_id,
            'bot_id': '-'+bot
        }
        url = 'https://api.vk.com/method/bot.addBotToChat'
        a = requests.get(url=url, params=params, headers=headers)
        try:
            res = a.json()['error']['error_msg']
            if res == 'Flood control':
                print('Флуд контроль. Добавлять нельзя')
                break
        except:
            pass
    else:
        print('Боты приглашены!')


def upload_avatars(tokens):
    avatars = os.listdir('avatars')
    x = 1
    for token in tokens:
        params = {
            'access_token': token,
            'v': '5.92'
        }
        url = 'https://api.vk.com/method/photos.getOwnerPhotoUploadServer'
        r = requests.get(url=url, params=params, headers=headers)
        img = {'photo': ('photo.jpg', open('avatars/'+random.choice(avatars), 'rb'))}
        response = requests.post(url=r.json()['response']['upload_url'], files=img, headers=headers).json()
        params = {
            'access_token': token,
            'v': '5.92',
            'server': response['server'],
            'hash': response['hash'],
            'photo': response['photo']
        }
        url = 'https://api.vk.com/method/photos.saveOwnerPhoto'
        try:
            requests.post(url=url, data=params, headers=headers).json()['response']
        except:
            pass
        x += 1
