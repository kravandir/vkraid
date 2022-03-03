from raid_modules import msgraid, oldfunc, raidgr
from raid_utils import jsonreader, options, reg
from raid_modules import new_func
print('\n\tRaidBotVk\t\n')


def get_message():
    global msg_tp
    print(
        '1.Спамить фразами из args.txt\n'
        '2.Спамить повторными фразами из message.txt')
    msg_tp = int(input())
    return msg_tp


while True:
    try:
        tokens = jsonreader.get_json_param('tokens')
        captcha = jsonreader.get_json_param('captcha')
        call = jsonreader.get_json_param('call')
        ids = jsonreader.get_json_param('ids')
        title = jsonreader.get_json_param('title')
        msg = jsonreader.get_json_param('msg')
        print(
            'Выход из программы [ENTER]\n'
            '0.Редактировать конфиг\n'
            '1.Рейд в вк\n2.Рейд группы\n'
            '3.Другие опции')
        raid = int(input())
        if raid == 0:
            regist = reg.Reg(True)
            print('1.Проверка логинов и паролей в acc.txt\n'
                  '2.Проверка данных из token.txt')
            ch = int(input())
            if ch == 1:
                regist = reg.Reg(False)
            regist.register()
        elif raid == 1:
            print(
                '0.Ввести боевой клич\n'
                '1.Рейд в лс\n2.Рейд в беседу\n'
                '3.Зайти по ссылке\n'
                '4.Пригласить с главного акка\n'
                '5.Добавить друг друга в др'
            )
            sp = int(input())
            if sp == 0:
                chat = input('Введите айди беседы: ')
                msgraid.MsgRaid(tokens[0], captcha, chat, call).start()
                print('Зов отправлен!')
            if sp == 1:
                n = 1
                user_id = input('Домен того, кому надо засрать лс: ')
                user_id = options.get_id(tokens[0], user_id)
                delmsg = int(input(
                        '1.Обычные сообщения\n'
                        '2.Исчезающие сообщения\n'
                    )
                )
                stick = int(input('1.Обычный рейд\n2.Рейд стикерами\n'))
                theme = int(input(
                        '1.Не менять тему чата\n'
                        '2.Менять тему чата при атаке\n'
                    )
                )
                if stick == 1:
                    ms = get_message()
                    print(
                        'Введите ссылку на медиафайл, например '
                        '"photo459509306_457244578". Если вам не '
                        'нужно прикреплять медиафайл, то '
                        'пропустите, нажав enter: '
                    )
                    media = input()
                    for name in tokens:
                        msgraid.SpamLs(name, user_id, media, ms, captcha, n, delmsg, theme).start()
                        n += 1
                elif stick == 2:
                    for name in tokens:
                        msgraid.StickerSpamLs(name, user_id, captcha, n, delmsg, theme).start()
                        n += 1
            elif sp == 2:
                print(
                    '1.Обычный рейд\n'
                    '2.Рейд стикерами\n'
                    '3.Рейд скриншотами\n'
                    '4.Рейд сменой темы чата\n'
                )
                raid_variant = int(input())
                n = 1
                edit_cf = int(input(
                        '1.Редактировать название конфы\n'
                        '2.Не редактировать название конфы\n'
                    )
                )
                if raid_variant == 1:
                    theme = int(input(
                            '1.Не менять тему чата\n'
                            '2.Менять тему чата при атаке\n'
                        )
                    )
                    edit = int(input(
                            '1.Редактировать сообщения\n'
                            '2.Не редактировать сообщения\n'
                        )
                    )
                    attach = input(
                        'Введите ссылку на медиафайл, например'
                        ' "photo459509306_457244578". Если вам '
                        'не нужно прикреплять медиафайл, то '
                        'пропустите, нажав enter: '
                    )
                    ms = get_message()
                    delmsg = int(input(
                            '1.Обычные сообщения\n'
                            '2.Исчезающие сообщения\n'
                        )
                    )
                    for name in tokens:
                        msgraid.SpamChat(name, ms, captcha, n, call, title, edit, attach, edit_cf, delmsg, theme).start()
                        n += 1
                elif raid_variant == 2:
                    theme = int(input(
                            '1.Не менять тему чата\n'
                            '2.Менять тему чата при атаке\n'
                        )
                    )
                    delmsg = int(input(
                            '1.Обычные сообщения\n'
                            '2.Исчезающие сообщения\n'
                        )
                    )
                    for name in tokens:
                        msgraid.StickerSpamChat(name, captcha, n, call, title, edit_cf, delmsg, theme).start()
                        n += 1
                elif raid_variant == 3:
                    for name in tokens:
                        msgraid.ScreenshotSpamChat(name, captcha, n, call, title, edit_cf).start()
                        n += 1
                elif raid_variant == 4:
                    for name in tokens:
                        msgraid.ThemeSpamChat(name, n, call, title, edit_cf).start()
                        n += 1

            elif sp == 3:
                link = input('Ссылка на беседу: ')
                msgraid.ConfJoin(tokens, link).start()
            elif sp == 4:
                msgraid.AddConf(tokens[0], ids, call).go()
            elif sp == 5:
                for name in tokens:
                    msgraid.AddFriend(name, captcha, ids).start()
        elif raid == 2:
            spam_group = int(input(
                    '1.Рейд стены\n'
                    '2.Рейд комментариев/стрима\n'
                    '3.Рейд обсуждения\n'
                )
            )
            med = input(
                'Введите ссылку на медиафайл, например '
                '"photo459509306_457244578". Если вам не '
                'нужно прикреплять медиафайл, '
                'то пропустите, нажав enter: '
            )
            ms = get_message()
            if spam_group == 1:
                wall = input(
                    'Домен страницы или группы, '
                    'чтобы заспамить: \n')
                wall = options.get_id(tokens[0], wall)
                n = 1
                for name in tokens:
                    raidgr.WallSpam(name, wall, ms, med, captcha, n).start()
                    n += 1
                else:
                    print('Спам запущен!')
            elif spam_group == 2:
                tp = int(input(
                    '1.Рейд комментов\n'
                    '2.Рейд стрима\n'))
                if tp == 1:
                    w = input(
                        'Введите ссылку на пост как в '
                        'примере "wall-118751940_8415": \n'
                    )[4:].split('_')
                else:
                    w = input(
                        'Введите ссылку на пост как в '
                        'примере "video-118751940_8415": \n'
                    )[5:].split('_')
                wall = w[0]
                post_id = w[1]
                n = 1
                for name in tokens:
                    raidgr.SpamComment(name, wall, post_id, ms, med, captcha, n).start()
                else:
                    print('Спам запущен!')
            elif spam_group == 3:
                topic = input(
                    'Введите ссылку на обсуждение, '
                    'например "topic-118751940_8415":\n'
                )
                n = 1
                for name in tokens:
                    raidgr.SpamBoard(name, med, topic, ms, captcha, n).start()
                    n += 1
        elif raid == 3:
            print(
                '1.Получить айди страницы\n'
                '2.Получить полную ссылку на беседу\n'
                '3.Пригласить список групп в беседу\n'
                '4.Загрузить аватарки\n'
                '5.Отдельные ништяки\n'
                '6.Настройка профиля\n'
                '7.Добавиться в друзья\n'
            )
            tools = int(input())
            if tools == 1:
                print(options.get_id(tokens[0], input('Введите домен:\n')))
            elif tools == 2:
                link = input("Введите ссылку на беседу:\n")
                options.get_full_link(link, tokens[0])
            elif tools == 3:
                print(
                    'Токен для инвайта по ссылке:\n'
                    'https://oauth.vk.com/authorize?client_id=6441755&redirect_uri=https://api.vk.com/blank.html&display=page&response_type=token&revoke=1\nИ подтвердить. А потом вставить новый токен, который сгенерировался в браузере'
                )
                token = input(
                    'Вставь токен из новой ссылки, он начинается от '
                    '"access_token=" и заканчивается до "&expires_in": '
                )
                d = 'Введите айди беседы для приглашения ботов: '
                conf_id = str(2000000000 + int(input(d)))
                bots = input('Айди групп через запятую:\n').split(',')
                print('Приглашение ботов в беседу')
                options.invite_bots(token, conf_id, bots)
            elif tools == 4:
                print('Происходит рандомная загрузка аватарок...')
                options.upload_avatars(tokens)
            elif tools == 5:
                ch = int(
                    input(
                        '1.Исключить всех участников беседы\n'
                        '2.Очистить группу вк от подпищиков\n'
                        '3.Почистить стену вк\n'
                        '4.Удаление всех комментариев\n'
                        '5.Пригласить друзей со всех акков\n'
                        '6.Удалить спам в своей беседе\n'
                        '7.Удалять сообщения собеседника\n'
                        '8.Ответ на сообщения говнотроллей\n'
                        '9.Засрать фотоальбом группы\n'
                        '10.Подписаться/отписаться на группу\n'
                        '11.Массовый репост записи\n'
                        '12.Проголосовать в опросе\n'
                        '13.Массовый лайк\n'
                        '14.Поставить статусы аккаунтам\n'
                        '15.Пригласить друга в конфы с рейд ботами\n'
                    )
                )
                if ch == 1:
                    b = int(input(
                            '1.Удалить пользователем конфу\n'
                            '2.Удалить конфу группой\n'
                        )
                    )
                    if b == 1:
                        chat = input('Введите айди беседы: ')
                        oldfunc.KickUsersByUser(tokens[0], ids, chat).start()
                    elif b == 2:
                        id_group = int(input('Введите айди группы:\n'))
                        print(
                            'Перейдите по этой ссылке:\n'
                            f'https://oauth.vk.com/authorize?client_id=3116505&scope=messages,manage,photos,docs,wall,stories&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token&group_ids={id_group}\n'
                            f'И нажмите "разрешить" и вставьте текст после "&access_token_{id_group}=":'
                        )
                        token_group = input()
                        cmd = input('Отправьте команду для активации: ')
                        oldfunc.KickUsersByGroup(id_group, token_group, ids, cmd).start()
                elif ch == 2:
                    group_id = input('Домен группы введите: ')
                    oldfunc.DeleteSubs(tokens[0], group_id).start()
                elif ch == 3:
                    print("Домен страницы или группы введи, чтобы всё удалить: ")
                    owner = input()
                    oldfunc.DeleteWall(tokens[0], owner).start()
                elif ch == 4:
                    print("Введите ссылку на пост как в примере (wall-118751940_8415): ")
                    w = input()[4:].split("_")
                    oldfunc.DeleteComment(tokens[0], w).start()
                elif ch == 5:
                    print('Чтобы всё активировать, напишите в беседе команду "invite"')
                    for x in range(len(tokens)):
                        oldfunc.InviteAllFriends(tokens[x], ids[x], x)
                elif ch == 6:
                    print('Действие выполняется с главного (первого акка)')
                    kf_id = input('Введите айди беседы:\n')
                    g = input('Сколько нужно удалить сообщений: ')
                    oldfunc.DeleteSpam(tokens[0], kf_id, g).start()
                elif ch == 7:
                    print('Действие выполняется с главного (первого акка)')
                    print(
                        'Чтобы поставить на автоудаление, введите домен страницы вк пользователей.'
                        'Если много пользователей, то введите их домены через запятую:')
                    id_list = input().split(",")
                    oldfunc.DeleteMessages(tokens[0], id_list).start()
                elif ch == 8:
                    print('Действие выполняется с главного акка (первая строка в acc или token txt)')
                    g = input("1.Просто ответ\n2.Ответ с пересыланием\n")
                    print(
                        'Чтобы поставить автоответчик на троля тупого,'
                        'введите его или их домены через запятую:')
                    id_list = input().split(",")
                    msg_tp = get_message()
                    ms = ''
                    if msg_tp == 1:
                        a = open("args.txt", encoding='utf8')
                        ms = a.read().split("\n")
                        a.close()
                    elif msg_tp == 2:
                        ms = msg.split('\n')
                    media = input(
                        'Введите ссылку на медиафайл, например "photo459509306_457244578". ' +
                        'Если вам не нужно прикреплять медиафайл, то пропустите, нажав enter: ')
                    oldfunc.AutoSay(tokens[0], captcha, id_list, ms, media, g).start()
                    print("Срач работает!")
                elif ch == 9:
                    print('Ссылка на альбом, например https://vk.com/album-118751940_272480573: ')
                    lnk = input()[21:].split("_")
                    group_id = lnk[0]
                    album_id = lnk[1]
                    print('Будут рандомно выбираться фотки в raidfiles!')
                    print('Скоро начнётся засерание, проверяйте альбом вк')
                    for token in tokens:
                        oldfunc.AlbumSpam(token, group_id, album_id).start()
                elif ch == 10:
                    gr_id = input("Введите домен группы:\n")
                    b = int(input("1.Вступить в группу\n2.Выйти из группы:\n"))
                    if b == 1:
                        oldfunc.GroupJoin(tokens, gr_id).start()
                    elif b == 2:
                        oldfunc.LeaveGroup(tokens, gr_id).start()
                elif ch == 11:
                    print('Ссылка на пост, например https://vk.com/wall-165757874_10528: ')
                    post = input()[15:]
                    msg = input('Введите подпись к репосту:')
                    oldfunc.Repost(tokens, post, msg).start()
                    print('Посты разосланы!')
                elif ch == 12:
                    print('Введите ссылку на опрос. Например, "https://vk.com/poll599246827_381566325":')
                    poll = input()
                    var = int(input('Напишите, какой по счёту вариант выберите: ')) - 1
                    ch = input('1.Добавить голоса\n2.Удалить голоса\n')
                    oldfunc.Voting(tokens, captcha, poll, var, ch).start()
                elif ch == 13:
                    print(
                        'post — запись на стене пользователя или группы\n'
                        'story — история\n'
                        'photo — фотография\n'
                        'video — видеозапись\n'
                        'market — товар')
                    tp = input()
                    print('Введите ссылку на то, что надо лайкнуть. Например, "https://vk.com/photo599246827_457239326":')
                    p = input()
                    ch = input('1.Поставить лайки\n2.Убрать лайки\n')
                    oldfunc.Likes(tokens, captcha, tp, p, ch).start()
                elif ch == 14:
                    stat = input("Статус: ")
                    oldfunc.Status(tokens, captcha, stat).start()
                elif ch == 15:
                    print(
                        'Введите токен своей страницы\n'
                        'https://oauth.vk.com/authorize?client_id=2685278&scope=notify%2Cphotos%2Cfriends%2Caudio%2Cvideo%2Cnotes%2Cpages%2Cdocs%2Cstatus%2Cquestions%2Coffers%2Cwall%2Cgroups%2Cmessages%2Cnotifications%2Cstats%2Cads%2Coffline&redirect_uri=https://api.vk.com/blank.html&display=page&response_type=token&revoke=1'
                    )
                    acc_token = input()
                    print(
                        'Введите токен для приглашения ботов\n'
                        'https://oauth.vk.com/authorize?client_id=6441755&redirect_uri=https://api.vk.com/blank.html&display=page&response_type=token&revoke=1'
                    )
                    invite_token = input()
                    friend_id = input("Введите id друга\n")
                    group = input("Введите id группы\n")
                    your_id = input("Введите свой id\n")
                    oldfunc.InviteRaidbots(acc_token, invite_token, group, friend_id, your_id, captcha).start()
            elif tools == 6:
                profile_menu = int(input(
                        "1.Закрыть профиль\n"
                        "2.Открыть профиль\n"
                        "3.Сменить имя, фамилию, дату рождения\n"
                    )
                )
                x = 0
                if profile_menu in [1, 2]:
                    for token in tokens:
                        if profile_menu == 1:
                            print(f"{x} аккаунт закрыл профиль")
                        else:
                            print(f"{x} аккаунт открыл профиль")
                        new_func.Profile(token, profile_menu, ids[x]).start()
                        x += 1
                else:
                    for token in tokens:
                        new_func.Profile(token, profile_menu, ids[x]).start()                    
            elif tools == 7:
                addfriend_menu = int(input("1.Добавиться\n2.Удалиться\n"))
                lnk = input("Домен профиля, куда добавляться\n")
                user_id = options.get_id(tokens[0], lnk)
                for token in tokens:
                    new_func.AddFriend(token, addfriend_menu, user_id, captcha).start()
    except KeyboardInterrupt:
        print('Выход')
        break
    except ValueError:
        print('Выход')
        break
