import time
import vk_api
import random
from raid_utils import jsonreader
from python3_anticaptcha import ImageToTextTask
from threading import Thread


class WallSpam(Thread):
    def __init__(self, token, wall, ms, med, captcha_key, n):
        Thread.__init__(self)
        self.token = token
        self.wall = wall
        self.ms = ms
        self.med = med
        self.captcha_key = captcha_key
        self.n = n

    def run(self):
        def captcha_handler(captcha):
            key = ImageToTextTask.ImageToTextTask(
                anticaptcha_key=self.captcha_key, save_format='const') \
                .captcha_handler(captcha_link=captcha.get_url())
            return captcha.try_again(key['solution']['text'])
        k = 1
        while True:
            try:
                vk_session = vk_api.VkApi(
                    token=self.token,
                    captcha_handler=captcha_handler)
                vk = vk_session.get_api()
                if self.ms == 1:
                    a = open('args.txt', encoding='utf8')
                    msg = a.read().split('\n')
                    a.close()
                    vk.wall.post(
                        owner_id=self.wall,
                        message=random.choice(msg),
                        attachments=self.med
                    )
                if self.ms == 2:
                    msg = jsonreader.get_json_param('msg').split('\n')[0]
                    vk.wall.post(
                        owner_id=self.wall,
                        message=msg,
                        attachments=self.med
                    )
                print(f'[WALL RAID] {k} ОТПРАВЛЕНО С {self.n} АККАУНТА!')
                k += 1
            except KeyError:
                print('Ошибка при отправке каптчи')
            except:
                pass
            time.sleep(random.randint(1, 3))


class SpamComment(Thread):
    def __init__(self, token, wall, post_id, ms, med, captcha_key, n):
        Thread.__init__(self)
        self.token = token
        self.wall = wall
        self.post_id = post_id
        self.ms = ms
        self.med = med
        self.captcha_key = captcha_key
        self.n = n

    def run(self):
        def captcha_handler(captcha):
            key = ImageToTextTask.ImageToTextTask(
                anticaptcha_key=self.captcha_key, save_format='const') \
                .captcha_handler(captcha_link=captcha.get_url())
            return captcha.try_again(key['solution']['text'])
        vk_session = vk_api.VkApi(
            token=self.token,
            captcha_handler=captcha_handler)
        vk = vk_session.get_api()
        k = 1
        while True:
            try:
                if self.ms == 1:
                    a = open('args.txt', encoding='utf8')
                    msg = a.read().split('\n')
                    a.close()
                    vk.wall.createComment(
                        owner_id=self.wall,
                        post_id=self.post_id,
                        message=random.choice(msg),
                        attachments=self.med
                    )
                if self.ms == 2:
                    msg = jsonreader.get_json_param('msg').split('\n')[0]
                    vk.wall.createComment(
                        owner_id=self.wall,
                        post_id=self.post_id,
                        message=msg,
                        attachments=self.med
                    )
                print(f'[WALL RAID] {k} ОТПРАВЛЕНО С {self.n} АККАУНТА!')
                k += 1
            except KeyError:
                print('Ошибка при отправке каптчи')
            except:
                pass
            time.sleep(random.randint(1, 3))


class SpamBoard(Thread):
    def __init__(self, token, media, brd, ms, captcha_key, n):
        Thread.__init__(self)
        self.token = token
        self.media = media
        self.brd = brd
        self.ms = ms
        self.captcha_key = captcha_key
        self.n = n

    def run(self):
        def captcha_handler(captcha):
            key = ImageToTextTask.ImageToTextTask(
                anticaptcha_key=self.captcha_key, save_format='const') \
                .captcha_handler(captcha_link=captcha.get_url())
            return captcha.try_again(key['solution']['text'])
        vk = vk_api.VkApi(token=self.token, captcha_handler=captcha_handler).get_api()
        brd = self.brd[6:].split('_')
        k = 1
        while True:
            try:
                if self.ms == 1:
                    a = open('args.txt', encoding='utf8')
                    msg = a.read().split('\n')
                    a.close()
                    vk.board.createComment(
                        group_id=brd[0],
                        topic_id=brd[1],
                        message=random.choice(msg),
                        attachments=self.media
                    )
                if self.ms == 2:
                    msg = jsonreader.get_json_param('msg').split('\n')[0]
                    vk.board.createComment(
                        group_id=brd[0],
                        topic_id=brd[1],
                        message=msg,
                        attachments=self.media
                    )
                print(f'[TOPIC RAID] {k} ОТПРАВЛЕНО С {self.n} АККАУНТА!')
                k += 1
            except KeyError:
                print('Ошибка при отправке каптчи')
            except:
                pass
            time.sleep(random.randint(1, 3))
