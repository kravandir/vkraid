import requests
from raid_utils import jsonreader
from python3_anticaptcha import ImageToTextTask


class Reg:
    def __init__(self, token):
        self.token = token
        self.captcha = jsonreader.get_json_param('captcha')

    def register(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Connection': 'keep-alive'
        }
        accfile = ''
        f = ''
        phone = ''
        passwd = ''
        if not self.token:
            accfile = 'acc.txt'
        elif self.token:
            accfile = 'token.txt'
        print('Генерация конфига...')
        accs = open(accfile, 'r', encoding='utf8')
        accs = accs.read().split('\n')
        print('Получение данных')
        x = 1
        tokenlist = []
        ids = []
        for acc in accs:
            acc = acc.strip(" ")
            try:
                if not self.token:
                    num_and_passwd = acc.split(':')
                    phone = num_and_passwd[0]
                    passwd = num_and_passwd[1]
                    params = {
                        'grant_type': 'password',
                        'client_id': '2274003',
                        'client_secret': 'hHbZxrka2uZ6jB1inYsH',
                        'username': phone,
                        'password': passwd
                    }
                    f = requests.get(url='https://oauth.vk.com/token', params=params, headers=headers)
                    tkn = f.json()['access_token']
                    tokenlist.append(tkn)
                    ids.append(str(f.json()['user_id']))
                    print(f'Cтрока {x} в файле "{accfile}" валид')
                else:
                    try:
                        params = {
                            'v': '5.92',
                            'access_token': acc
                        }
                        url = 'https://api.vk.com/method/users.get'
                        f = requests.get(url=url, params=params, headers=headers).json()
                        f['response'][0]['is_closed']
                        ids.append(str(f['response'][0]['id']))
                        tokenlist.append(acc)
                        print(f'Cтрока {x} в файле "{accfile}" валид')
                    except:
                        print(f'Cтрока {x} в файле "{accfile}" невалид')
            except:
                try:
                    if f.json()['error'] == 'need_captcha':
                        captch = f.json()['captcha_img']
                        captcha_key = ImageToTextTask.ImageToTextTask(
                            anticaptcha_key=self.captcha).captcha_handler(
                            captcha_link=captch)['solution']['text']
                        print(captch)
                        print(captcha_key)
                        try:
                            captchaparams = {
                                'grant_type': 'password',
                                'client_id': '2274003',
                                'client_secret': 'hHbZxrka2uZ6jB1inYsH',
                                'username': phone,
                                'password': passwd,
                                'captcha_sid': f.json()['captcha_sid'],
                                'captcha_key': captcha_key
                            }
                            f = requests.get(url='https://oauth.vk.com/token', params=captchaparams, headers=headers)
                            tkn = f.json()['access_token']
                            tokenlist.append(tkn)
                            ids.append(str(f.json()['user_id']))
                            print(f'Cтрока {x} в файле "{accfile}" валид')
                        except:
                            print(f'Cтрока {x} в файле "{accfile}" невалид')
                    else:
                        print(f'Cтрока {x} в файле "{accfile}" невалид')
                except:
                    pass
            x += 1
        print('установка сообщения')
        text = open('message.txt', 'r', encoding='utf8')
        text = text.read().split('\n')[0][:1882]
        f1 = 'Сообщение для спама у вас теперь '
        print(f1 + 'обновлено в файле "message.txt".')
        print('Введите название беседы, какое будет при рейде: ')
        title = input()
        print('Ключ от https://anti-captcha.com/: ')
        anti_captcha = input()
        print('Введите боевой клич, на который рейд боты начнут спамить: ')
        call = input()
        k = open('data.json', 'wt', encoding='utf8')
        k.write(
            '{\n\t"tokens":' + str(tokenlist).replace("'", '"') +
            ',\n\t"ids":' + str(ids).replace("'", '"') +
            ',\n\t"msg":"' + text +
            '",\n\t"title":"' + title +
            '",\n\t"captcha":"' + anti_captcha +
            '",\n\t"call":"' + call + '"\n}')
        k.close()
        print('Готово! Данные обновлены!')
