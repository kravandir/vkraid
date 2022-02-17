import requests
import random
import os
import vk_api
from time import sleep
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from python3_anticaptcha import ImageToTextTask
from threading import Thread

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0',
    'Connection': 'keep-alive'
}


class KickUsersByUser(Thread):
    def __init__(self, token, ids, chat):
        Thread.__init__(self)
        self.token = token
        self.ids = ids
        self.chat = chat

    def run(self):
        print('Главный акк - ваш аккаунт, с которого вам надо кикнуть всех участников в беседе\n'
              'Указывайте его логин и пароль в первой строке')
        owner = self.token

        print('Запуск')
        url = 'https://api.vk.com/method/messages.getChat'
        params = {
            'access_token': owner,
            'chat_id': self.chat,
            'v': 5.92
        }
        g = requests.get(url=url, params=params, headers=headers).json()['response']['members_count']
        for _ in range(int(g) // 24 + 1):
            cod = 'var b = API.messages.getChat({"chat_id":"' + self.chat + '"}).users;var x = 0;while (x < 24){if (b[x] != ' + str(self.ids[0]) + ') {API.messages.removeChatUser({"chat_id":"' + self.chat + '","member_id":b[x]});}x=x+1;}'
            url = 'https://api.vk.com/method/execute'
            params = {
                'access_token': owner,
                'code': cod,
                'v': 5.92
            }
            requests.get(url=url, params=params, headers=headers)


class KickUsersByGroup(Thread):
    def __init__(self, group_id, token_group, ids, cmd):
        Thread.__init__(self)
        self.group_id = group_id
        self.token_group = token_group
        self.ids = ids
        self.cmd = cmd

    def run(self):
        print('Пригласите бота в беседу и отправьте ему упоминание')
        longpoll = VkBotLongPoll(vk_api.VkApi(token=self.token_group), self.group_id)
        kf_id = 0
        count = 0
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.object.text == self.cmd:
                try:
                    print('Айди беседы - ', event.chat_id)
                    kf_id = event.chat_id
                    url = 'https://api.vk.com/method/messages.getConversationMembers'
                    params = {
                        'access_token': self.token_group,
                        'peer_id': 2000000000 + kf_id,
                        'v': 5.92
                    }
                    url_request = requests.get(url=url, params=params, headers=headers).json()
                    count = len(url_request['response']['items'])
                    print('Скоро начнется исключение...')
                    break
                except:
                    pass
        cod = 'var b = API.messages.getConversationMembers({"peer_id":"' + str(2000000000+kf_id) + '"}).items;var x = 0;while (x < 24){if (b[x].member_id != ' + str(self.ids[0]) + ') {if (b[x].member_id != -' + str(self.group_id) + ') {API.messages.removeChatUser({"chat_id":"' + str(kf_id) + '","member_id":b[x].member_id});}}x=x+1;}'
        for _ in range((count // 24)+1):
            try:
                url = 'https://api.vk.com/method/execute'
                params = {
                    'access_token': self.token_group,
                    'code': cod,
                    'v': 5.92
                }
                requests.get(url=url, params=params, headers=headers).json()
            except:
                pass


class DeleteSubs(Thread):
    def __init__(self, token, group_id):
        Thread.__init__(self)
        self.token = token
        self.group_id = group_id

    def run(self):
        print("Токен берётся с первого акка по списку")
        url = 'https://api.vk.com/method/utils.resolveScreenName'
        params = {
            'access_token': self.token,
            'screen_name': self.group_id,
            'v': 5.92
        }
        group_id = requests.get(url=url, params=params, headers=headers).json()['response']['object_id']
        url = 'https://api.vk.com/method/groups.getMembers'
        params = {
            'access_token': self.token,
            'group_id': group_id,
            'v': 5.92
        }
        g = requests.get(url=url, params=params, headers=headers).json()['response']['count']
        for _ in range(int(g) // 24 + 1):
            cod = 'var b = API.groups.getMembers({"group_id":"' + group_id + '","count":"24"}).items;var x = 0;while (x < 24){API.groups.removeUser({"group_id":"' + group_id + '","user_id":b[x]});x=x+1;}'
            url = 'https://api.vk.com/method/execute'
            params = {
                'access_token': self.token,
                'code': cod,
                'v': 5.92
            }
            requests.get(url=url, params=params, headers=headers)


class DeleteWall(Thread):
    def __init__(self, token, owner):
        Thread.__init__(self)
        self.token = token
        self.owner = owner

    def run(self):
        url = 'https://api.vk.com/method/utils.resolveScreenName'
        params = {
            'access_token': self.token,
            'screen_name': self.owner,
            'v': 5.92
        }
        rq = requests.get(url=url, params=params, headers=headers).json()
        if str(rq['response']['type']) == "user":
            owner = str(rq['response']['object_id'])
        else:
            owner = str(rq['response']['object_id'] * -1)
        url = 'https://api.vk.com/method/wall.get'
        params = {
            'access_token': self.token,
            'owner_id': owner,
            'count': 1,
            'v': 5.92
        }
        g = requests.get(url=url, params=params, headers=headers).json()['response']['count']
        cod = 'var g = 12;var x = 1;while (x < g){var b = API.wall.get({"owner_id":"' + owner + '","count":"1"}).items[0].id;API.wall.delete({"owner_id":"' + owner + '","post_id":b});x=x+1;}'
        for _ in range(int(g) // 12 + 1):
            url = 'https://api.vk.com/method/execute'
            params = {
                'access_token': self.token,
                'code': cod,
                'v': 5.92
            }
            requests.get(url=url, params=params, headers=headers)


class DeleteComment(Thread):
    def __init__(self, token, w):
        Thread.__init__(self)
        self.token = token
        self.w = w

    def run(self):
        owner = self.w[0]
        post_id = self.w[1]
        url = 'https://api.vk.com/method/wall.getComments'
        params = {
            'access_token': self.token,
            'owner_id': owner,
            'post_id': post_id,
            'count': 1,
            'v': 5.92
        }
        count = requests.get(url=url, params=params, headers=headers).json()['response']['count']
        for x in range(int(count)):
            url = 'https://api.vk.com/method/wall.getComments'
            params = {
                'access_token': self.token,
                'owner_id': owner,
                'post_id': post_id,
                'count': 1,
                'v': 5.92
            }
            a = requests.get(url=url, params=params, headers=headers).json()['response']['items'][0]['id']
            print(f"Удалён {x+1} комментарий")
            url = 'https://api.vk.com/method/wall.deleteComment'
            params = {
                'access_token': self.token,
                'owner_id': owner,
                'comment_id': a,
                'v': 5.92
            }
            requests.get(url=url, params=params, headers=headers)
        else:
            print("Комментарии удалены!")


class InviteAllFriends(Thread):
    def __init__(self, token, idi, x):
        Thread.__init__(self)
        self.token = token
        self.idi = idi
        self.x = x

    def run(self):
        longpoll = VkLongPoll(vk_api.VkApi(token=self.token))
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.text == "invite":
                url = 'https://api.vk.com/method/friends.get'
                params = {
                    'access_token': self.token,
                    'user_id': self.idi,
                    'v': 5.92
                }
                a = requests.get(url=url, params=params, headers=headers).json()['response']['items']
                print(f'Приглашение началось c {self.x+1} акка')
                for i in a:
                    url = 'https://api.vk.com/method/messages.addChatUser'
                    params = {
                        'access_token': self.token,
                        'chat_id': event.chat_id,
                        'user_id': i,
                        'v': 5.92
                    }
                    requests.get(url=url, params=params, headers=headers)
                else:
                    print(f'Все друзья приглашены с {self.x+1} акка!')


class InviteRaidbots(Thread):
    def __init__(self, acc_token, invite_token, group, friend_id, your_id, captcha_key):
        Thread.__init__(self)
        self.acc_token = acc_token
        self.invite_token = invite_token
        self.group = group
        self.friend_id = friend_id
        self.your_id = your_id
        self.captcha_key = captcha_key

    def run(self):
        def captcha_handler(captcha):
            key = ImageToTextTask.ImageToTextTask(
                anticaptcha_key=self.captcha_key, save_format='const') \
                .captcha_handler(captcha_link=captcha.get_url())
            return captcha.try_again(key['solution']['text'])
        vk11 = vk_api.VkApi(token=self.acc_token, captcha_handler=captcha_handler).get_api()
        kf_list = []
        for x in range(5):
            kf_id = vk11.messages.createChat(user_ids=self.friend_id, title=str(x + 1))
            kf_list.append(kf_id)
        for kf_id in kf_list:
            url = 'https://api.vk.com/method/bot.addBotToChat'
            params = {
                'access_token': self.invite_token,
                'peer_id': 2000000000 + int(kf_id),
                'bot_id': '-' + self.group,
                'v': 5.92
            }
            requests.get(url=url, params=params, headers=headers)
            url = 'https://api.vk.com/method/messages.removeChatUser'
            params = {
                'access_token': self.acc_token,
                'chat_id': kf_id,
                'user_id': self.your_id,
                'v': 5.92
            }
            requests.get(url=url, params=params, headers=headers)
        print('Всё работает. Пизда другу')


class DeleteSpam(Thread):
    def __init__(self, token, kf_id, g):
        Thread.__init__(self)
        self.token = token
        self.kf_id = kf_id
        self.g = g

    def run(self):
        offset = 0
        msgbase = []
        print('Получаем id сообщений!')
        for _ in range((int(self.g) // 24)+1):
            try:
                url = 'https://api.vk.com/method/messages.getHistory'
                params = {
                    'access_token': self.token,
                    'peer_id': 2000000000 + int(self.kf_id),
                    'count': 24,
                    'offset': offset,
                    'v': 5.92
                }
                msg_ids = requests.get(url=url, params=params, headers=headers).json()['response']['items']
                for x in range(len(msg_ids)):
                    msgbase.append(msg_ids[x]['id'])
                offset += 24
            except:
                pass
        print('id сообщений получены!')
        x = 0
        for _ in range((int(self.g) // 24)+1):
            msgs = []
            for _ in range(24):
                try:
                    msgs.append(msgbase[x])
                except:
                    pass
                x += 1
            try:
                cod = 'var b = ' + str(msgs) + ';var x = 0;while (x < 24)' + '{API.messages.delete({"message_ids":b[x],"delete_for_all":true});x=x+1;}'
                url = 'https://api.vk.com/method/execute'
                params = {
                    'access_token': self.token,
                    'code': cod,
                    'v': 5.92
                }
                requests.get(url=url, params=params, headers=headers).json()
            except:
                pass
        print('Всё удалено!')



class DeleteMessages(Thread):
    def __init__(self, token, id_list):
        Thread.__init__(self)
        self.token = token
        self.id_list = id_list

    def run(self):
        vk = vk_api.VkApi(token=self.token).get_api()
        id_list_2 = []
        for x in self.id_list:
            url = 'https://api.vk.com/method/utils.resolveScreenName'
            params = {
                'access_token': self.token,
                'screen_name': x,
                'v': 5.92
            }
            rq = requests.get(url=url, params=params, headers=headers).json()
            if str(rq['response']['type']) == "user":
                rq = str(rq['response']['object_id'])
            else:
                rq = str(rq['response']['object_id'] * -1)
            id_list_2.append(rq)
        while True:
            longpoll = VkLongPoll(vk_api.VkApi(token=self.token))
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and str(event.user_id) in id_list_2 and not event.from_me:
                    try:
                        vk.messages.delete(message_ids=event.message_id, delete_for_all='true')
                    except:
                        vk.messages.delete(message_ids=event.message_id)


class AutoSay(Thread):
    def __init__(self, token, captcha_key, id_list, ms, media, g):
        Thread.__init__(self)
        self.token = token
        self.captcha_key = captcha_key
        self.id_list = id_list
        self.ms = ms
        self.media = media
        self.g = g

    def run(self):
        def captcha_handler(captcha):
            key = ImageToTextTask.ImageToTextTask(
                anticaptcha_key=self.captcha_key, save_format='const') \
                .captcha_handler(captcha_link=captcha.get_url())
            return captcha.try_again(key['solution']['text'])

        id_list_2 = []
        for x in self.id_list:
            url = 'https://api.vk.com/method/utils.resolveScreenName'
            params = {
                'access_token': self.token,
                'screen_name': x,
                'v': 5.92
            }
            rq = requests.get(url=url, params=params, headers=headers).json()
            if str(rq['response']['type']) == "user":
                rq = str(rq['response']['object_id'])
            else:
                rq = str(rq['response']['object_id'] * -1)
            id_list_2.append(rq)
        vk = vk_api.VkApi(token=self.token, captcha_handler=captcha_handler).get_api()
        while True:
            longpoll = VkLongPoll(vk_api.VkApi(token=self.token))
            for event in longpoll.listen():
                try:
                    if event.type == VkEventType.MESSAGE_NEW and str(event.user_id) in id_list_2 and not event.from_me:
                        if self.g == "1":
                            vk.messages.send(
                                peer_id=event.peer_id,
                                message=random.choice(self.ms),
                                attachment=self.media,
                                random_id=random.randint(0, 999999)
                            )
                        if self.g == "2":
                            vk.messages.setActivity(peer_id=event.peer_id, type='typing')
                            sleep(random.randint(3, 7))
                            vk.messages.send(
                                peer_id=event.peer_id,
                                message=random.choice(self.ms),
                                attachment=self.media,
                                random_id=random.randint(0, 999999),
                                reply_to=event.message_id
                            )
                except KeyError:
                    print('Неуспешно решена каптча')
                except:
                    pass


class AlbumSpam(Thread):
    def __init__(self, token, group_id, album_id):
        Thread.__init__(self)
        self.token = token
        self.group_id = group_id
        self.album_id = album_id

    def run(self):
        folder = os.listdir("raidfiles")
        raidphoto = random.choice(folder)
        url = 'https://api.vk.com/method/photos.getUploadServer'
        params = {
            'access_token': self.token,
            'album_id': self.album_id,
            'group_id': self.group_id,
            'v': 5.92
        }
        a = requests.get(url=url, params=params, headers=headers).json()['response']['upload_url']
        img = {'photo': (raidphoto, open("raidfiles/"+raidphoto, 'rb'))}
        response = requests.post(a, files=img, headers=headers).json()

        vk = vk_api.VkApi(token=self.token).get_api()
        print(f"Фотка {raidphoto} успешно загружена. Начинается атака!")
        while True:
            try:
                vk.photos.save(
                    album_id=self.album_id,
                    group_id=self.group_id,
                    server=response['server'],
                    photos_list=response['photos_list'],
                    hash=response['hash']
                )
            except:
                pass


class GroupJoin(Thread):
    def __init__(self, tokens, gr_id):
        Thread.__init__(self)
        self.tokens = tokens
        self.gr_id = gr_id

    def run(self):
        url = 'https://api.vk.com/method/utils.resolveScreenName'
        params = {
            'access_token': self.tokens[0],
            'screen_name': self.gr_id,
            'v': 5.92
        }
        gr_id = str(abs(requests.get(url=url, params=params, headers=headers).json()['response']['object_id']))
        for token in self.tokens:
            url = 'https://api.vk.com/method/groups.join'
            params = {
                'access_token': token,
                'group_id': gr_id,
                'v': 5.92
            }
            requests.get(url=url, params=params, headers=headers)
        print("Все вошли в группу")


class LeaveGroup(Thread):
    def __init__(self, tokens, gr_id):
        Thread.__init__(self)
        self.tokens = tokens
        self.gr_id = gr_id

    def run(self):
        url = 'https://api.vk.com/method/utils.resolveScreenName'
        params = {
            'access_token': self.tokens[0],
            'screen_name': self.gr_id,
            'v': 5.92
        }
        gr_id = str(abs(requests.get(url=url, params=params, headers=headers).json()['response']['object_id']))
        for token in self.tokens:
            url = 'https://api.vk.com/method/groups.leave'
            params = {
                'access_token': token,
                'group_id': gr_id,
                'v': 5.92
            }
            requests.get(url=url, params=params, headers=headers)
        print("Все вышли из группы")


class Repost(Thread):
    def __init__(self, tokens, post, msg):
        Thread.__init__(self)
        self.tokens = tokens
        self.post = post
        self.msg = msg

    def run(self):
        k = 1
        for token in self.tokens:
            url = 'https://api.vk.com/method/wall.repost'
            params = {
                'access_token': token,
                'object': self.post,
                'message': self.msg,
                'v': 5.92
            }
            requests.get(url=url, params=params, headers=headers)
            print(k, 'аккаунт репостнул запись...')
            k += 1


class Voting(Thread):
    def __init__(self, tokens, captcha_key, poll, var, ch):
        Thread.__init__(self)
        self.tokens = tokens
        self.captcha_key = captcha_key
        self.poll = poll
        self.var = var
        self.ch = ch

    def run(self):
        def captcha_handler(captcha):
            key = ImageToTextTask.ImageToTextTask(
                anticaptcha_key=self.captcha_key, save_format='const') \
                .captcha_handler(captcha_link=captcha.get_url())
            return captcha.try_again(key['solution']['text'])
        owner = self.poll[19:].split("_")[0]
        id_poll = self.poll[19:].split("_")[1]
        for token in self.tokens:
            try:
                vk = vk_api.VkApi(token=token, captcha_handler=captcha_handler).get_api()
                answer_id = vk.polls.getById(owner_id=owner, poll_id=id_poll)["answers"][self.var]["id"]
                if self.ch == "1":
                    vk.polls.addVote(
                        owner_id=owner,
                        poll_id=id_poll,
                        answer_ids=answer_id
                    )
                if self.ch == "2":
                    vk.polls.deleteVote(
                        owner_id=owner,
                        poll_id=id_poll,
                        answer_ids=answer_id
                    )
            except KeyError:
                print('Неуспешно решена каптча')
            except:
                pass


class Likes(Thread):
    def __init__(self, tokens, captcha_key, tp, p, ch):
        Thread.__init__(self)
        self.tokens = tokens
        self.captcha_key = captcha_key
        self.tp = tp
        self.p = p
        self.ch = ch

    def run(self):
        def captcha_handler(captcha):
            key = ImageToTextTask.ImageToTextTask(
                anticaptcha_key=self.captcha_key, save_format='const') \
                .captcha_handler(captcha_link=captcha.get_url())
            return captcha.try_again(key['solution']['text'])
        owner = self.p[15 + len(self.tp):].split("_")[0]
        id_p = self.p[15 + len(self.tp):].split("_")[1]
        for token in self.tokens:
            try:
                vk = vk_api.VkApi(token=token, captcha_handler=captcha_handler).get_api()
                if self.ch == "1":
                    vk.likes.add(type=self.tp, owner_id=owner, item_id=id_p)
                if self.ch == "2":
                    vk.likes.delete(type=self.tp, owner_id=owner, item_id=id_p)
            except KeyError:
                print('Неуспешно решена каптча')
            except:
                pass


class Status(Thread):
    def __init__(self, tokens, captcha_key, stat):
        Thread.__init__(self)
        self.tokens = tokens
        self.captcha_key = captcha_key
        self.stat = stat

    def run(self):
        def captcha_handler(captcha):
            key = ImageToTextTask.ImageToTextTask(
                anticaptcha_key=self.captcha_key, save_format='const') \
                .captcha_handler(captcha_link=captcha.get_url())
            return captcha.try_again(key['solution']['text'])
        for token in self.tokens:
            vk_session = vk_api.VkApi(token=token, captcha_handler=captcha_handler)
            vk = vk_session.get_api()
            try:
                vk.status.set(text=self.stat)
            except KeyError:
                print('Неуспешно решена каптча')
            except:
                pass
