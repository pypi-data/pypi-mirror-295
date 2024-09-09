from urllib.parse import unquote
from colorama import Fore
from datetime import datetime, timedelta
from threading import Thread, Lock
from typing import Literal
from random import randint, shuffle, choice
from os import system as sys, getcwd, path
from platform import system as s_name
from time import sleep
from shutil import get_terminal_size as gts
from collections import Counter
from json import dump, dumps, load, loads
from requests import get, Session
from subprocess import run as terminal, Popen
from sys import exit, executable



VERSION = '3.0.1'




















HPV_TEAM = f'''
 _  _ _____   __   ___         _      ___ __  _ _  ___ 
| || | _ \ \ / /__| _ ) __ ___(_)_ _ |_  )  \| | |( _ )
| __ |  _/\ V /___| _ \/ _/ _ \ | ' \ / / () |_  _/ _ \\
|_||_|_|   \_/    |___/\__\___/_|_||_/___\__/  |_|\___/
+-----------------------------------------+
| Контент: t.me/HPV_TEAM /// t.me/HPV_PRO |
+-----------------------------------------+
| Сотрудничество: t.me/HPV_BASE |
+-------------------------------+
| Автор: t.me/A_KTO_Tbl |
+-----------------------+
| V{VERSION} |
+--------+
'''

def HPV_Banner():
    '''Вывод баннера'''

    for HPV in HPV_TEAM.split('\n'): # Вывод баннера
        print(Fore.MAGENTA + HPV.center(gts()[0], ' '))
        sleep(0.026)




















def HPV_Get_Accounts() -> dict:
    '''Получение списка аккаунтов'''

    print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Получение списка аккаунтов!')
    PATH = path.join(getcwd(), 'Core', 'Config', 'HPV_Account.json')

    try:
        with open(PATH, 'r') as HPV:
            return load(HPV)
    except:
        print(Fore.MAGENTA + '[HPV]' + Fore.RED + ' — Ошибка чтения `HPV_Account.json`, ссылки указаны некорректно!')
        exit()



def HPV_Get_Proxy() -> list:
    '''Получение списка proxy'''

    PATH = path.join(getcwd(), 'Core', 'Proxy', 'HPV_Proxy.txt')
    PROXY = []

    with open(PATH, 'r') as HPV:
        for Proxy in HPV.read().split('\n'):
            if Proxy:
                try:
                    Proxy = Proxy.split(':')
                    PROXY.append({'IP': Proxy[0], 'Port': Proxy[1], 'Login': Proxy[2], 'Password': Proxy[3]})
                except:
                    pass

        return PROXY



def HPV_Get_Config(_print: bool = True) -> list:
    '''Получение конфигурационных данных'''

    if _print:
        print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Получение конфигурационных данных!')

    PATH = path.join(getcwd(), 'Core', 'Config', 'HPV_Config.json')

    try:
        with open(PATH, 'r') as HPV:
            return load(HPV)
    except:
        return []



def HPV_Get_Empty_Request() -> dict:
    '''Получение данных c пустыми запросами'''

    try:
        return {
            "Authentication_1": {
                "Method": "get",
                "Url": "https://bcoin2048.com",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "Upgrade-Insecure-Requests": "1", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Accept-Language": "HPV TEAM"}
            },
            "Authentication_2": {
                "Method": "get",
                "Url": "https://bcoin2048.com/static/css/main.beac74a7.css",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "text/css,*/*;q=0.1", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "style", "Referer": "https://bcoin2048.com/", "Accept-Language": "HPV TEAM"}
            },
            "Authentication_3": {
                "Method": "get",
                "Url": "https://bcoin2048.com/static/js/main.e1e021b5.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "script", "Referer": "https://bcoin2048.com/", "Accept-Language": "HPV TEAM"}
            },
            "Authentication_4": {
                "Method": "post",
                "Url": "https://bcoin2048.com/api/v2/squads/get-squad",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "Content-Type": "application/json", "Telegram-Init-Data": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "Origin": "https://bcoin2048.com", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://bcoin2048.com/", "Accept-Language": "HPV TEAM"}
            },
            "Authentication_5": {
                "Method": "post",
                "Url": "https://bcoin2048.com/api/v2",
                "Json": {"operationName": "getViewerLeaderboardsParticipant", "variables": {"leaderboardId": "SUM_EARNED_DAILY"}, "query": "query getViewerLeaderboardsParticipant($leaderboardId: LeaderboardId!, $date: Date) {\n  viewerLeaderboardResult(leaderboardId: $leaderboardId, date: $date) {\n    place\n    score\n    __typename\n  }\n}"},
                "Headers": {"User-Agent": "HPV TEAM", "Content-Type": "application/json", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "telegram-init-data": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "Origin": "https://bcoin2048.com", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://bcoin2048.com/", "Accept-Language": "HPV TEAM"}
            },
            "Authentication_6": {
                "Method": "post",
                "Url": "https://bcoin2048.com/api/v2",
                "Json": {"operationName": "logWebappStart", "variables": {}, "query": "mutation logWebappStart {\n  LogWebappStart\n}"},
                "Headers": {"User-Agent": "HPV TEAM", "Content-Type": "application/json", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "telegram-init-data": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "Origin": "https://bcoin2048.com", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://bcoin2048.com/", "Accept-Language": "HPV TEAM"}
            },
            "Authentication_7": {
                "Method": "post",
                "Url": "https://bcoin2048.com/api/v2",
                "Json": {"operationName": "SaveUserPlatform", "variables": {"platform": "android"}, "query": "mutation SaveUserPlatform($platform: String!) {\n  SaveUserPlatform(platform: $platform)\n}"},
                "Headers": {"User-Agent": "HPV TEAM", "Content-Type": "application/json", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "telegram-init-data": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "Origin": "https://bcoin2048.com", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://bcoin2048.com/", "Accept-Language": "HPV TEAM"}
            },
            "Authentication_8": {
                "Method": "post",
                "Url": "https://bcoin2048.com/api/v2",
                "Json": {"operationName": "getDailyTasks", "variables": {}, "query": "query getDailyTasks {\n  dailyTasks {\n    id\n    name\n    link\n    __typename\n  }\n}"},
                "Headers": {"User-Agent": "HPV TEAM", "Content-Type": "application/json", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "telegram-init-data": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "Origin": "https://bcoin2048.com", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://bcoin2048.com/", "Accept-Language": "HPV TEAM"}
            },
            "Authentication_9": {
                "Method": "post",
                "Url": "https://bcoin2048.com/api/v2",
                "Json": {"operationName": "getSumBicoinsMined", "variables": {}, "query": "query getSumBicoinsMined {\n  sumBicoinsMined\n}"},
                "Headers": {"User-Agent": "HPV TEAM", "Content-Type": "application/json", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "telegram-init-data": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "Origin": "https://bcoin2048.com", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://bcoin2048.com/", "Accept-Language": "HPV TEAM"}
            },
            "Authentication_10": {
                "Method": "post",
                "Url": "https://bcoin2048.com/api/v2",
                "Json": {"operationName": "GetViewer", "variables": {}, "query": "query GetViewer {\n  viewer {\n    id\n    energyUnits\n    nextEnergyUnitsAt\n    bicoinBalance\n    name\n    inviteesCount\n    inviteesInviteesCount\n    inviteesReward\n    inviteesInviteesReward\n    allTimeEarnedBicoins\n    photoURL\n    bestGameEver {\n      bicoinReward\n      score\n      __typename\n    }\n    bestGameDaily {\n      bicoinReward\n      score\n      __typename\n    }\n    features\n    inviterId\n    hadClaimedFirst2048Reward\n    isBot\n    deleteTileBoostersCount\n    moveBackBoostersCount\n    moveWithoutTileBoostersCount\n    adsWatchedToday\n    completedTasks\n    completedCheckpoints\n    dailyTasksStreak\n    dailyTasksLastCompletedAt\n    __typename\n  }\n}"},
                "Headers": {"User-Agent": "HPV TEAM", "Content-Type": "application/json", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "telegram-init-data": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "Origin": "https://bcoin2048.com", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://bcoin2048.com/", "Accept-Language": "HPV TEAM"}
            },
            "Authentication_11": {
                "Method": "get",
                "Url": "https://bcoin2048.com/favicon.ico",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "image", "Referer": "https://bcoin2048.com/", "Accept-Language": "HPV TEAM"}
            },
            "Authentication_12": {
                "Method": "post",
                "Url": "https://bcoin2048.com/api/v2/squadsget-squad",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "Content-Type": "application/json", "Telegram-Init-Data": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "Origin": "https://bcoin2048.com", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://bcoin2048.com/", "Accept-Language": "HPV TEAM"}
            },
            "Authentication_13": {
                "Method": "get",
                "Url": "https://bcoin2048.com/static/media/x-logo.f037ed9381ef692c3cfc83e19ecfd43b.svg",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "image", "Referer": "https://bcoin2048.com/", "Accept-Language": "HPV TEAM"}
            },
            "Authentication_14": {
                "Method": "get",
                "Url": "https://bcoin2048.com/static/media/tg-logo.589b881498401201f8597e163ccd747f.svg",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "image", "Referer": "https://bcoin2048.com/", "Accept-Language": "HPV TEAM"}
            },
            "Authentication_15": {
                "Method": "post",
                "Url": "https://bcoin2048.com/api/v2",
                "Json": {"operationName": "getSecondsTillNextDay", "variables": {}, "query": "query getSecondsTillNextDay {\n  secondsTillNextDay\n}"},
                "Headers": {"User-Agent": "HPV TEAM", "Content-Type": "application/json", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "telegram-init-data": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "Origin": "https://bcoin2048.com", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://bcoin2048.com/", "Accept-Language": "HPV TEAM"}
            },
            "Authentication_16": {
                "Method": "get",
                "Url": "https://bcoin2048.com/static/media/bicoin.3eeb27b9fe87c93bc2b1302c6adc8234.svg",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "image", "Referer": "https://bcoin2048.com/", "Accept-Language": "HPV TEAM"}
            },
            "Authentication_17": {
                "Method": "get",
                "Url": "https://bcoin2048.com/static/media/chevron-right.225fd8efe767db8fb9ea66fb37df06a3.svg",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "image", "Referer": "https://bcoin2048.com/", "Accept-Language": "HPV TEAM"}
            },
            "Authentication_18": {
                "Method": "get",
                "Url": "https://bcoin2048.com/static/media/exited.ee09c7323a3a7f7fbd5d.png",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "image", "Referer": "https://bcoin2048.com/", "Accept-Language": "HPV TEAM"}
            },
            "Authentication_19": {
                "Method": "get",
                "Url": "https://bcoin2048.com/static/media/settings.ba5443b536d9450389ff.png",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "image", "Referer": "https://bcoin2048.com/", "Accept-Language": "HPV TEAM"}
            },



            "Play_1": {
                "Method": "get",
                "Url": "https://bcoin2048.com/static/media/video.d0dc76693376013aea6eafaa28ac463f.svg",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "image", "Referer": "https://bcoin2048.com/game", "Accept-Language": "HPV TEAM"}
            },
            "Play_2": {
                "Method": "get",
                "Url": "https://bcoin2048.com/static/media/share.36a8933600df2a7877fd88a0896204f9.svg",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "image", "Referer": "https://bcoin2048.com/game", "Accept-Language": "HPV TEAM"}
            },
            "Play_3": {
                "Method": "get",
                "Url": "https://bcoin2048.com/static/media/delete-tile.c5764dc4f57809118737320cb1a31ab8.svg",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "image", "Referer": "https://bcoin2048.com/game", "Accept-Language": "HPV TEAM"}
            },
            "Play_4": {
                "Method": "get",
                "Url": "https://bcoin2048.com/favicon.ico",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "image", "Referer": "https://bcoin2048.com/game", "Accept-Language": "HPV TEAM"}
            },
            "Play_5": {
                "Method": "get",
                "Url": "https://bcoin2048.com/static/media/bicoin.3eeb27b9fe87c93bc2b1302c6adc8234.svg",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "image", "Referer": "https://bcoin2048.com/game", "Accept-Language": "HPV TEAM"}
            },
            "Play_6": {
                "Method": "get",
                "Url": "https://bcoin2048.com/static/media/x-logo.f037ed9381ef692c3cfc83e19ecfd43b.svg",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "image", "Referer": "https://bcoin2048.com/game", "Accept-Language": "HPV TEAM"}
            },
            "Play_7": {
                "Method": "get",
                "Url": "https://bcoin2048.com/static/media/move-back.7d3189149a4da96c5876d413f0243b01.svg",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "image", "Referer": "https://bcoin2048.com/game", "Accept-Language": "HPV TEAM"}
            },
            "Play_8": {
                "Method": "get",
                "Url": "https://bcoin2048.com/static/media/free-move.532a99194924ab25598de5a86db5474b.svg",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "image", "Referer": "https://bcoin2048.com/game", "Accept-Language": "HPV TEAM"}
            },
            "Play_9": {
                "Method": "get",
                "Url": "https://bcoin2048.com/static/media/tg-logo.589b881498401201f8597e163ccd747f.svg",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "image", "Referer": "https://bcoin2048.com/game", "Accept-Language": "HPV TEAM"}
            },
            "Play_10": {
                "Method": "get",
                "Url": "https://bcoin2048.com/static/media/done.5e9fc255161b7dc54b9047f256e8790f.svg",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "image", "Referer": "https://bcoin2048.com/", "Accept-Language": "HPV TEAM"}
            },
            "Play_11": {
                "Method": "get",
                "Url": "https://bcoin2048.com/static/media/refresh.c69b832012039b944442e4f44912121b.svg",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "image", "Referer": "https://bcoin2048.com/", "Accept-Language": "HPV TEAM"}
            },



            "Get_Boosts_1": {
                "Method": "get",
                "Url": "https://bcoin2048.com/favicon.ico",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "image", "Referer": "https://bcoin2048.com/boosters", "Accept-Language": "HPV TEAM"}
            },
            "Get_Boosts_2": {
                "Method": "get",
                "Url": "https://bcoin2048.com/static/media/move-back.7d3189149a4da96c5876d413f0243b01.svg",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "image", "Referer": "https://bcoin2048.com/boosters", "Accept-Language": "HPV TEAM"}
            },
            "Get_Boosts_3": {
                "Method": "get",
                "Url": "https://bcoin2048.com/static/media/free-move.532a99194924ab25598de5a86db5474b.svg",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "image", "Referer": "https://bcoin2048.com/boosters", "Accept-Language": "HPV TEAM"}
            },
            "Get_Boosts_4": {
                "Method": "get",
                "Url": "https://bcoin2048.com/static/media/delete-tile.c5764dc4f57809118737320cb1a31ab8.svg",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "image", "Referer": "https://bcoin2048.com/boosters", "Accept-Language": "HPV TEAM"}
            },
            "Get_Boosts_5": {
                "Method": "get",
                "Url": "https://bcoin2048.com/static/media/video.d0dc76693376013aea6eafaa28ac463f.svg",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "image", "Referer": "https://bcoin2048.com/boosters", "Accept-Language": "HPV TEAM"}
            },



            "Get_Halving_1": {
                "Method": "get",
                "Url": "https://bcoin2048.com/favicon.ico",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "image", "Referer": "https://bcoin2048.com/halving", "Accept-Language": "HPV TEAM"}
            },
            "Get_Halving_2": {
                "Method": "get",
                "Url": "https://bcoin2048.com/static/media/bicoin.3eeb27b9fe87c93bc2b1302c6adc8234.svg",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "image", "Referer": "https://bcoin2048.com/halving", "Accept-Language": "HPV TEAM"}
            },



            "AutoDailyTask_1": {
                "Method": "get",
                "Url": "https://bcoin2048.com/favicon.ico",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "image", "Referer": "https://bcoin2048.com/daily-tasks", "Accept-Language": "HPV TEAM"}
            },
            "AutoDailyTask_2": {
                "Method": "get",
                "Url": "https://bcoin2048.com/static/media/bicoin.3eeb27b9fe87c93bc2b1302c6adc8234.svg",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "image", "Referer": "https://bcoin2048.com/daily-tasks", "Accept-Language": "HPV TEAM"}
            },
            "AutoDailyTask_3": {
                "Method": "get",
                "Url": "https://bcoin2048.com/static/media/done.5e9fc255161b7dc54b9047f256e8790f.svg",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "X-Requested-With": "HPV TEAM", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "image", "Referer": "https://bcoin2048.com/daily-tasks", "Accept-Language": "HPV TEAM"}
            }
        }
    except:
        return {}



def HPV_Get_Accept_Language() -> dict:
    '''Получение данных с языковыми заголовками'''

    try:
        return {
            "RU": "ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7",
            "US": "en-US,en;q=0.9",
            "GB": "en-GB,en;q=0.9",
            "DE": "de,de-DE;q=0.9,en-US;q=0.8,en;q=0.7",
            "FR": "fr,fr-FR;q=0.9,en-US;q=0.8,en;q=0.7",
            "ES": "es,es-ES;q=0.9,en-US;q=0.8,en;q=0.7",
            "IT": "it,it-IT;q=0.9,en-US;q=0.8,en;q=0.7",
            "CN": "zh,zh-CN;q=0.9,en-US;q=0.8,en;q=0.7",
            "JP": "ja,ja-JP;q=0.9,en-US;q=0.8,en;q=0.7",
            "KR": "ko,ko-KR;q=0.9,en-US;q=0.8,en;q=0.7",
            "BR": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "CA": "en-CA,en;q=0.9,fr-CA;q=0.7",
            "AU": "en-AU,en;q=0.9",
            "IN": "en-IN,en;q=0.9,hi;q=0.7",
            "MX": "es-MX,es;q=0.9,en-US;q=0.8,en;q=0.7",
            "NL": "nl,nl-NL;q=0.9,en-US;q=0.8,en;q=0.7",
            "TR": "tr,tr-TR;q=0.9,en-US;q=0.8,en;q=0.7",
            "SE": "sv,sv-SE;q=0.9,en-US;q=0.8,en;q=0.7",
            "NO": "no,no-NO;q=0.9,en;q=0.8",
            "FI": "fi,fi-FI;q=0.9,sv;q=0.8,en;q=0.7",
            "PL": "pl,pl-PL;q=0.9,en-US;q=0.8,en;q=0.7",
            "AR": "es-AR,es;q=0.9,en-US;q=0.8,en;q=0.7",
            "ZA": "en-ZA,en;q=0.9,af;q=0.8,zu;q=0.7",
            "IL": "he,he-IL;q=0.9,en-US;q=0.8,en;q=0.7",
            "EG": "ar,ar-EG;q=0.9,en-US;q=0.8,en;q=0.7",
            "IR": "fa,fa-IR;q=0.9,en-US;q=0.8,en;q=0.7",
            "AF": "fa-AF,ps;q=0.9,en;q=0.8",
            "AL": "sq,sq-AL;q=0.9,en;q=0.8",
            "DZ": "ar-DZ,ar;q=0.9,fr;q=0.8,en;q=0.7",
            "AO": "pt-AO,pt;q=0.9,en;q=0.8",
            "AM": "hy,hy-AM;q=0.9,en;q=0.8",
            "AZ": "az,az-AZ;q=0.9,ru;q=0.8,en;q=0.7",
            "BH": "ar-BH,ar;q=0.9,en;q=0.8",
            "BD": "bn,bn-BD;q=0.9,en;q=0.8",
            "BY": "be,be-BY;q=0.9,ru;q=0.8,en;q=0.7",
            "BE": "nl-BE,fr-BE;q=0.9,de-BE;q=0.8,en;q=0.7",
            "BJ": "fr-BJ,fr;q=0.9,en;q=0.8",
            "BT": "dz,dz-BT;q=0.9,en;q=0.8",
            "BO": "es-BO,es;q=0.9,qu;q=0.8,en;q=0.7",
            "BA": "bs,hr-BA;q=0.9,sr-BA;q=0.8,en;q=0.7",
            "BW": "en-BW,en;q=0.9,tn;q=0.8",
            "BN": "ms-BN,ms;q=0.9,en;q=0.8",
            "BG": "bg,bg-BG;q=0.9,en;q=0.8",
            "BF": "fr-BF,fr;q=0.9,en;q=0.8",
            "BI": "fr-BI,fr;q=0.9,rn;q=0.8,en;q=0.7",
            "KH": "km,km-KH;q=0.9,en;q=0.8",
            "CM": "fr-CM,fr;q=0.9,en-CM;q=0.8,en;q=0.7",
            "CV": "pt-CV,pt;q=0.9,en;q=0.8",
            "TD": "fr-TD,fr;q=0.9,ar-TD;q=0.8,en;q=0.7",
            "CL": "es-CL,es;q=0.9,en;q=0.8",
            "CO": "es-CO,es;q=0.9,en;q=0.8",
            "KM": "fr-KM,fr;q=0.9,ar;q=0.8,en;q=0.7",
            "CG": "fr-CG,fr;q=0.9,en;q=0.8",
            "CD": "fr-CD,fr;q=0.9,en;q=0.8",
            "CR": "es-CR,es;q=0.9,en;q=0.8",
            "CI": "fr-CI,fr;q=0.9,en;q=0.8",
            "HR": "hr,hr-HR;q=0.9,en;q=0.8",
            "CU": "es-CU,es;q=0.9,en;q=0.8",
            "CY": "el-CY,el;q=0.9,tr;q=0.8,en;q=0.7",
            "CZ": "cs,cs-CZ;q=0.9,en;q=0.8",
            "DK": "da,da-DK;q=0.9,en;q=0.8",
            "DJ": "fr-DJ,fr;q=0.9,ar-DJ;q=0.8,en;q=0.7",
            "DO": "es-DO,es;q=0.9,en;q=0.8",
            "EC": "es-EC,es;q=0.9,en;q=0.8",
            "SV": "es-SV,es;q=0.9,en;q=0.8",
            "GQ": "es-GQ,es;q=0.9,fr;q=0.8,pt;q=0.7",
            "ER": "ti,ti-ER;q=0.9,ar;q=0.8,en;q=0.7",
            "EE": "et,et-EE;q=0.9,ru;q=0.8,en;q=0.7",
            "SZ": "en-SZ,en;q=0.9,ss;q=0.8",
            "ET": "am,am-ET;q=0.9,en;q=0.8",
            "FJ": "en-FJ,en;q=0.9,fj;q=0.8",
            "GA": "fr-GA,fr;q=0.9,en;q=0.8",
            "GM": "en-GM,en;q=0.9",
            "GE": "ka,ka-GE;q=0.9,ru;q=0.8,en;q=0.7",
            "GH": "en-GH,en;q=0.9",
            "GR": "el,el-GR;q=0.9,en;q=0.8",
            "GT": "es-GT,es;q=0.9,en;q=0.8",
            "GN": "fr-GN,fr;q=0.9,en;q=0.8",
            "GW": "pt-GW,pt;q=0.9,en;q=0.8",
            "GY": "en-GY,en;q=0.9",
            "HT": "fr-HT,fr;q=0.9,ht;q=0.8,en;q=0.7",
            "HN": "es-HN,es;q=0.9,en;q=0.8",
            "HU": "hu,hu-HU;q=0.9,en;q=0.8",
            "IS": "is,is-IS;q=0.9,en;q=0.8",
            "ID": "id,id-ID;q=0.9,en;q=0.8",
            "IQ": "ar-IQ,ar;q=0.9,ku;q=0.8,en;q=0.7",
            "IE": "en-IE,en;q=0.9,ga;q=0.8",
            "JM": "en-JM,en;q=0.9",
            "JO": "ar-JO,ar;q=0.9,en;q=0.8",
            "KZ": "kk,kk-KZ;q=0.9,ru;q=0.8,en;q=0.7",
            "KE": "en-KE,en;q=0.9,sw;q=0.8",
            "KI": "en-KI,en;q=0.9",
            "KP": "ko-KP,ko;q=0.9,en;q=0.8",
            "KW": "ar-KW,ar;q=0.9,en;q=0.8",
            "KG": "ky,ky-KG;q=0.9,ru;q=0.8,en;q=0.7",
            "LA": "lo,lo-LA;q=0.9,en;q=0.8",
            "LV": "lv,lv-LV;q=0.9,ru;q=0.8,en;q=0.7",
            "LB": "ar-LB,ar;q=0.9,fr;q=0.8,en;q=0.7",
            "LS": "en-LS,en;q=0.9,st;q=0.8",
            "LR": "en-LR,en;q=0.9",
            "LY": "ar-LY,ar;q=0.9,en;q=0.8",
            "LI": "de-LI,de;q=0.9,en;q=0.8",
            "LT": "lt,lt-LT;q=0.9,ru;q=0.8,en;q=0.7",
            "LU": "fr-LU,fr;q=0.9,de;q=0.8,en;q=0.7",
            "MG": "mg,mg-MG;q=0.9,fr;q=0.8,en;q=0.7",
            "MW": "en-MW,en;q=0.9,ny;q=0.8",
            "MY": "ms,my-MY;q=0.9,en;q=0.8",
            "MV": "dv,dv-MV;q=0.9,en;q=0.8",
            "ML": "fr-ML,fr;q=0.9,en;q=0.8",
            "MT": "mt,mt-MT;q=0.9,en;q=0.8",
            "MR": "ar-MR,ar;q=0.9,fr;q=0.8,en;q=0.7",
            "MU": "en-MU,en;q=0.9,fr;q=0.8",
            "MN": "mn,mn-MN;q=0.9,ru;q=0.8,en;q=0.7",
            "ME": "sr-ME,sr;q=0.9,bs;q=0.8,en;q=0.7",
            "MA": "ar-MA,ar;q=0.9,fr;q=0.8,en;q=0.7",
            "MZ": "pt-MZ,pt;q=0.9,en;q=0.8",
            "MM": "my,my-MM;q=0.9,en;q=0.8",
            "NA": "en-NA,en;q=0.9,af;q=0.8,de;q=0.7",
            "NP": "ne,np;q=0.9,en;q=0.8",
            "NZ": "en-NZ,en;q=0.9,mi;q=0.8",
            "NI": "es-NI,es;q=0.9,en;q=0.8",
            "NE": "fr-NE,fr;q=0.9,en;q=0.8",
            "NG": "en-NG,en;q=0.9,yo;q=0.8,ha;q=0.7",
            "MK": "mk,mk-MK;q=0.9,sq;q=0.8,en;q=0.7",
            "OM": "ar-OM,ar;q=0.9,en;q=0.8",
            "PK": "ur,ur-PK;q=0.9,en;q=0.8",
            "PA": "es-PA,es;q=0.9,en;q=0.8",
            "PG": "en-PG,en;q=0.9,tpi;q=0.8",
            "PY": "es-PY,es;q=0.9,gn;q=0.8,en;q=0.7",
            "PE": "es-PE,es;q=0.9,qu;q=0.8,en;q=0.7",
            "PH": "en-PH,en;q=0.9,tl;q=0.8",
            "PT": "pt-PT,pt;q=0.9,en;q=0.8",
            "QA": "ar-QA,ar;q=0.9,en;q=0.8",
            "RO": "ro,ro-RO;q=0.9,en;q=0.8",
            "RW": "rw,rw-RW;q=0.9,fr;q=0.8,en;q=0.7",
            "KN": "en-KN,en;q=0.9",
            "LC": "en-LC,en;q=0.9",
            "VC": "en-VC,en;q=0.9",
            "WS": "sm,sm-WS;q=0.9,en;q=0.8",
            "ST": "pt-ST,pt;q=0.9,en;q=0.8",
            "SA": "ar-SA,ar;q=0.9,en;q=0.8",
            "SN": "fr-SN,fr;q=0.9,en;q=0.8",
            "SC": "fr-SC,fr;q=0.9,en;q=0.8",
            "SL": "en-SL,en;q=0.9",
            "SG": "en-SG,en;q=0.9,zh;q=0.8,ms;q=0.7",
            "SB": "en-SB,en;q=0.9",
            "SO": "so,so-SO;q=0.9,en;q=0.8",
            "SS": "en-SS,en;q=0.9,ar;q=0.8",
            "SD": "ar-SD,ar;q=0.9,en;q=0.8",
            "SR": "nl-SR,nl;q=0.9,en;q=0.8",
            "SY": "ar-SY,ar;q=0.9,en;q=0.8",
            "TJ": "tg,tg-TJ;q=0.9,ru;q=0.8,en;q=0.7",
            "TZ": "sw-TZ,sw;q=0.9,en;q=0.8",
            "TH": "th,th-TH;q=0.9,en;q=0.8",
            "TL": "pt-TL,pt;q=0.9,en;q=0.8",
            "TG": "fr-TG,fr;q=0.9,en;q=0.8",
            "TO": "to,to-TO;q=0.9,en;q=0.8",
            "TT": "en-TT,en;q=0.9,hns;q=0.8,fr;q=0.7",
            "TN": "ar-TN,ar;q=0.9,fr;q=0.8,en;q=0.7",
            "TM": "tk,tk-TM;q=0.9,ru;q=0.8,en;q=0.7",
            "TV": "en-TV,en;q=0.9",
            "UG": "en-UG,en;q=0.9,sw;q=0.8",
            "AE": "ar-AE,ar;q=0.9,en;q=0.8",
            "UY": "es-UY,es;q=0.9,en;q=0.8",
            "UZ": "uz,uz-UZ;q=0.9,ru;q=0.8,en;q=0.7",
            "VU": "bi,bi-VU;q=0.9,en;q=0.8,fr;q=0.7",
            "VA": "it-VA,it;q=0.9,en;q=0.8",
            "VE": "es-VE,es;q=0.9,en;q=0.8",
            "VN": "vi,vi-VN;q=0.9,en;q=0.8",
            "YE": "ar-YE,ar;q=0.9,en;q=0.8",
            "ZM": "en-ZM,en;q=0.9",
            "ZW": "en-ZW,en;q=0.9,sn;q=0.8"
        }
    except:
        return {}










def HPV_Request(proxy: dict) -> bool:
    try:
        get('https://ipecho.net/plain', proxies=proxy)
        return True
    except:
        return False



def HPV_Checker(proxy) -> dict:
    PROXY = f"{proxy['Login']}:{proxy['Password']}@{proxy['IP']}:{proxy['Port']}"
    PROXY_HTTPS = {'http': f'http://{PROXY}', 'https': f'https://{PROXY}'}
    PROXY_SOCKS5 = {'http': f'socks5://{PROXY}', 'https': f'socks5://{PROXY}'}

    if HPV_Request(PROXY_HTTPS):
        return PROXY_HTTPS
    elif HPV_Request(PROXY_SOCKS5):
        return PROXY_SOCKS5



def HPV_Proxy_Checker(_print: bool = True) -> list:
    '''Проверка HTTPS, SOCKS5 проксей на валидность'''

    print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Получение списка проксей!') if _print else None
    PROXY_LIST = HPV_Get_Proxy() # Список всех доступных проксей с файла
    VALID_PROXY = [] # Список валидных проксей
    THREADS = [] # Список потоков

    if PROXY_LIST:
        print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Проверка прокси на работоспособность... Подождите немного!') if _print else None

        def _HPV_Checker(proxy):
            HPV = HPV_Checker(proxy)
            if HPV:
                VALID_PROXY.append(HPV)

        for proxy in PROXY_LIST:
            THREAD = Thread(target=_HPV_Checker, args=(proxy,))
            THREAD.start()
            THREADS.append(THREAD)

        for THREAD in THREADS:
            THREAD.join()

        print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + f' — Проверка прокси окончена! Работоспособные: {len(VALID_PROXY)}') if _print else None
    
    else:
        print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Прокси не обнаружены!') if _print else None

    return VALID_PROXY









def HPV_Headers() -> dict:
    '''Генератор уникальных параметров для Headers'''

    HPV_CHROME_VERSION = [

        '126.0.6478.111', # 25/06/2024
        '126.0.6478.110', # 19/06/2024
        '126.0.6478.72',  # 19/06/2024
        '126.0.6478.71',  # 14/06/2024
        '125.0.6422.186', # 14/06/2024
        '126.0.6478.50',  # 12/06/2024
        '125.0.6422.167', # 12/06/2024
        '125.0.6422.165', # 05/06/2024
        '125.0.6422.164', # 05/06/2024
        '125.0.6422.113', # 24/05/2025
        '125.0.6422.112', # 24/05/2025
        '125.0.6422.72',  # 22/05/2024
        '125.0.6422.71',  # 22/05/2024
        '125.0.6422.53',  # 16/05/2024
        '125.0.6422.52',  # 16/05/2024
        '124.0.6367.82',  # 24/04/2024
        '123.0.6312.121', # 24/04/2024
        '124.0.6367.54',  # 16/04/2024
        '123.0.6312.120', # 16/04/2024
        '123.0.6312.119', # 16/04/2024
        '123.0.6312.99',  # 03/04/2024
        '123.0.6312.81',  # 03/04/2024
        '123.0.6312.80',  # 27/03/2024
        '123.0.6312.41',  # 27/03/2024
        '123.0.6312.40',  # 20/03/2024
        '122.0.6261.120', # 20/03/2024
        '122.0.6261.119', # 13/03/2024
        '122.0.6261.106', # 13/03/2024

    ]
    HPV_PHONE_MODEL = [

        'Xiaomi Redmi K60 Pro',
        'Realme C33',
        'Realme Pad 2',
        'Realme Note 50',
        'Realme GT Neo 3T',
        'Xiaomi Redmi Pad Pro',
        'Realme Q5 Pro',
        'Realme 10 Pro',
        'Xiaomi Pad 6 Max 14',
        'Infinix Hot 11s',
        'Xiaomi Redmi A3',
        'Xiaomi Redmi Turbo 3',
        'Xiaomi Redmi Pad SE',
        'Infinix Hot 40 Pro',
        'Realme C65',
        'Xiaomi Redmi Note 11T Pro',
        'Xiaomi 12T',
        'Realme 12 Pro+',
        'Infinix Hot 12',
        'Realme Q5i',
        'Realme V25',
        'Xiaomi Redmi K70 Ultra',
        'Xiaomi 14 Pro',
        'Xiaomi Redmi 12',
        'Xiaomi Redmi Note 12 Turbo',
        'Infinix Smart 7',
        'Infinix Smart 8 Plus',
        'Xiaomi Mix Fold 4',
        'Xiaomi Civi 4 Pro',
        'Xiaomi Redmi Note 11 Pro',
        'Xiaomi Redmi Note 12S',
        'Realme C53',
        'Xiaomi Redmi Note 13 Pro',
        'Realme GT 6T',
        'Realme C67',
        'Xiaomi Poco F6 Pro',
        'Xiaomi Mix Flip',
        'Xiaomi Redmi K70 Pro',
        'Xiaomi 11i HyperCharge',
        'Infinix Hot 30i',
        'Realme 12 Lite',
        'Realme 9i',
        'Infinix Smart 8',
        'Realme 10',
        'Xiaomi Civi 1S',
        'Infinix Note 30',
        'Realme 13 Pro+',
        'Xiaomi Redmi 10A',
        'Xiaomi Poco M5s',
        'Realme GT5 Pro',
        'Infinix Zero',
        'Xiaomi 12S Pro',
        'Xiaomi Redmi Note 12',
        'Realme Narzo 50A Prime',
        'Xiaomi Redmi 12C',
        'Infinix Note 12i',
        'Xiaomi 13 Lite',
        'Xiaomi Poco M6 Plus',
        'Samsung Galaxy S22 Ultra',
        'Xiaomi 14 Civi',
        'Xiaomi Redmi A2',
        'Xiaomi Poco M4',
        'Xiaomi Poco M4 Pro',
        'Xiaomi Redmi 11 Prime',
        'Infinix Note 40',
        'Xiaomi Redmi 10 Power',
        'Xiaomi Poco C55',
        'Infinix Zero 30',
        'Xiaomi Redmi K40S',
        'Xiaomi Poco C65',
        'Xiaomi Redmi Note 11E',
        'Xiaomi Poco M6 Pro',
        'Xiaomi Pad 6S Pro 12.4',
        'Xiaomi Poco X4 GT',
        'Realme GT Neo 3',
        'Realme 11 Pro',
        'Realme 10s',
        'Infinix Note 40 Pro',
        'Realme C63',
        'Xiaomi Redmi Note 12 Pro',
        'Infinix Hot 30 Play',
        'Realme Narzo 50i Prime',
        'Xiaomi 12S Ultra',
        'Infinix Hot 40i',
        'Realme C30s',
        'Realme Pad Mini',
        'Infinix Smart 8 Pro',
        'Xiaomi Redmi 10 2022',
        'Xiaomi Redmi K60E',
        'Xiaomi 13T Pro',
        'Xiaomi Mix Fold 2',
        'Realme C35',
        'Infinix Note 12 Pro',
        'Xiaomi 12 Lite',
        'Infinix Hot 12 Play',
        'Xiaomi Poco C50',
        'Xiaomi 11i',
        'Realme Narzo 50',
        'Xiaomi 13T',
        'Xiaomi Redmi K50 Pro',
        'Realme 9 Pro',
        'Xiaomi 13 Ultra',
        'Xiaomi Poco M5',
        'Xiaomi Poco F4 GT',
        'Xiaomi Poco F5',
        'Xiaomi Poco F5 Pro',
        'Xiaomi Redmi Note 12T Pro',
        'Xiaomi Redmi Note 11E Pro',
        'Realme V23',
        'Xiaomi Pad 6',
        'Xiaomi Redmi Note 12 Pro Speed',
        'Realme C51s',
        'Realme GT5 240W',
        'Xiaomi Poco F6',
        'Xiaomi Redmi K70E',
        'Realme C30',
        'Xiaomi Redmi A3x',
        'Realme C61',
        'Xiaomi Mix Fold 3',
        'Realme C51',
        'Xiaomi Redmi K60 Ultra',
        'Xiaomi Redmi 10C',
        'Xiaomi Redmi A1',
        'Realme C31',
        'Infinix Note 12',
        'Realme V30',
        'Realme C55',
        'Xiaomi 14 Ultra',
        'Realme GT 6',
        'Xiaomi Poco C61',
        'Xiaomi Redmi K50i',
        'Infinix Hot 12 Pro',
        'Xiaomi Redmi Note 11',
        'Realme Narzo N53',
        'Infinix Smart 7 HD',
        'Xiaomi Redmi Note 11S',
        'Xiaomi Poco X4',
        'Xiaomi Poco X4 Pro',
        'Realme Pad X',
        'Xiaomi Redmi Note 13R',
        'Infinix Smart 8 HD',
        'Xiaomi Poco C51',
        'Infinix Hot 20',
        'Xiaomi Civi 3',
        'Xiaomi Poco F4',
        'Realme V23i',
        'Xiaomi 12T Pro',
        'Xiaomi Redmi 13C',
        'Honor X8B',
        'Honor Magic6 Pro',
        'Honor Magic6 Ultimate',
        'Honor X9b',
        'Honor 200 Lite',
        'Huawei Pura 70 Ultra',
        'Huawei Pura 70 Pro',
        'Huawei Pura 70',
        'Huawei nova 12s',
        'Huawei nova Y72',
        'Xiaomi Redmi Note 10T',
        'Xiaomi POCO X6',
        'Xiaomi POCO X6 Pro',
        'Xiaomi POCO M6 Pro',
        'Xiaomi POCO X5',
        'Xiaomi POCO X5 Pro',
        'Xiaomi POCO C40',
        'Xiaomi POCO M5s',
        'Xiaomi POCO M5',
        'Samsung Galaxy A05',
        'Samsung Galaxy A35',
        'Samsung Galaxy S24',
        'Samsung Galaxy S24+',
        'Samsung Galaxy S24 Ultra',
        'Samsung Galaxy A15',
        'Samsung Galaxy A25',
        'Samsung Z Flip5',
        'Samsung Galaxy A05s',
        'Samsung Galaxy A24',
        'Samsung Galaxy A14',
        'Samsung Galaxy S23 FE',
        'Samsung Galaxy Z Fold5',
        'Samsung Galaxy A34',
        'Samsung Galaxy M54',
        'Samsung Galaxy A54',
        'Samsung Galaxy S23+',
        'Samsung Galaxy S23',
        'Samsung Galaxy S23 Ultra',
        'Samsung Galaxy A03',
        'Samsung Galaxy A04',
        'Samsung Galaxy XCover6 Pro',
        'Samsung Galaxy A13',
        'Samsung Galaxy A23',
        'Samsung Galaxy M23',
        'Samsung Galaxy A33',
        'Samsung Galaxy A73',
        'Samsung Galaxy A53',
        'Samsung Galaxy Z Fold4',
        'Samsung Galaxy S22',
        'Samsung Galaxy S22+',
        'Samsung S21 FE',
        'vivo X100 Ultra',
        'vivo V30e',
        'vivo V30 lite',
        'vivo X100',
        'vivo Y27s',
        'vivo X100 Pro',
        'vivo V29e',
        'vivo V29',
        'vivo Y36',
        'vivo V27',
        'vivo V27e',
        'vivo X Note',
        'vivo X80 Pro',
        'vivo T1',
        'vivo X90 Pro',
        'vivo X90 Pro+',
        'vivo V25 Pro',
        'vivo Y35',
        'vivo V25',
        'vivo v23e',
        'vivo v23',
        'OPPO Reno11',
        'OPPO Find X7 Ultra',
        'OPPO Find X7',
        'OPPO Find N2'

    ]
    HPV_TELEGRAM_CLIENT = [

        'org.telegram.messenger', # Telegram
        'org.telegram.plus',      # Plus
        'ir.ilmili.telegraph',    # Telegraph

    ]

    HPV_Chrome_Version = choice(HPV_CHROME_VERSION) # Версия Google Chrome
    HPV_Android_Version = randint(11, 14) # Версия Android
    HPV_Phone_Model = choice(HPV_PHONE_MODEL) # Модель телефона
    HPV_Telegram_Client = choice(HPV_TELEGRAM_CLIENT) # Клиент Telegram

    USER_AGENT = f'Mozilla/5.0 (Linux; Android {HPV_Android_Version}; {HPV_Phone_Model}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{HPV_Chrome_Version} Mobile Safari/537.36'
    SEC_CH_UA = f'"Chromium";v="{HPV_Chrome_Version.split(".")[0]}", "Not(A:Brand";v="99", "Google Chrome";v="{HPV_Chrome_Version.split(".")[0]}"'
    SEC_CH_UA_MOBILE = '?1'
    SEC_CH_UA_PLATFORM = '"Android"'
    X_REQUESTED_WITH = HPV_Telegram_Client

    return {'USER_AGENT': USER_AGENT, 'SEC_CH_UA': SEC_CH_UA, 'SEC_CH_UA_MOBILE': SEC_CH_UA_MOBILE, 'SEC_CH_UA_PLATFORM': SEC_CH_UA_PLATFORM, 'X_REQUESTED_WITH': X_REQUESTED_WITH}




















def HPV_Config_Setup() -> None:
    '''Настройка конфига'''

    print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Настройка конфига... Подождите немного!')
    Accounts = HPV_Get_Accounts() # Словарь аккаунтов

    if Accounts:
        Proxys = HPV_Proxy_Checker() # Список проксей
        User_Agents = [] # Список уникальных параметров для Headers
        Uniq = [] # Список с уникальными параметрами для каждого аккаунта


        # Генератор уникальных параметров для Headers в количестве, соответствующем числу аккаунтов
        print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Генерация уникальных параметров Headers для каждого аккаунта!')
        while len(User_Agents) < len(Accounts):
            Headers = HPV_Headers() # Новые сгенерированные параметры для Headers
            if Headers not in User_Agents: # Проверка на отсутствие таких же параметров для Headers
                User_Agents.append(Headers)


        # Создание уникальных личностей для каждого аккаунта
        print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Создание уникальных личностей для каждого аккаунта!')
        for Number, Key in enumerate(Accounts):
            Uniq.append({'Name': Key, 'URL': Accounts[Key], 'Proxy': Proxys[Number % len(Proxys)] if len(Proxys) > 0 else None, 'Headers': User_Agents[Number]})


        # Сохранение данных
        print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Сохранение конфигурационных данных!')
        PATH = path.join(getcwd(), 'Core', 'Config', 'HPV_Config.json')
        with open(PATH, 'w', encoding='utf-8') as HPV:
            dump(Uniq, HPV, ensure_ascii=False, indent=4)

    else:
        print(Fore.MAGENTA + '[HPV]' + Fore.YELLOW + ' — Аккаунты не найдены!')
        exit()











def HPV_Upgrade_Alert(AUTO_UPDATE) -> bool:
    '''Проверка наличия обновления'''

    try:
        if AUTO_UPDATE:
            HPV = get('https://pypi.org/pypi/HPV-TEAM-Bcoin2048/json').json()['info']['version']
            return True if VERSION < HPV else False
    except:
        return False



def HPV_Upgrade(AUTO_UPDATE) -> None:
    '''Автоматическая проверка и установка обновления'''

    print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Проверка наличия обновления... Подождите немного!')
    PIP = 'pip' if s_name() == 'Windows' else 'pip3' # Определение ОС, для установки зависимостей

    try:
        if HPV_Upgrade_Alert(AUTO_UPDATE):
            print(Fore.MAGENTA + '[HPV]' + Fore.YELLOW + ' — Обнаружено обновление!')

            if AUTO_UPDATE:
                print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Идёт процесс обновления... Подождите немного!')
                terminal([PIP, 'install', '--upgrade', 'HPV_TEAM_Bcoin2048'], check=True) # Установка зависимостей

                print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Перезапуск программы...')
                Popen([executable, path.join(getcwd(), 'HPV_Bcoin2048.py')]); exit() # Перезапуск программы

            else:
                print(Fore.MAGENTA + '[HPV]' + Fore.YELLOW + ' — Автообновления отключены! Обновление не установлено!')

        else:
            print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Обновлений не обнаружено!')

    except Exception as ERROR:
        print(Fore.MAGENTA + '[HPV]' + Fore.RED + f' — Что-то пошло не так!\n\tОшибка: {ERROR}')








def HPV_Checking(File: str, Content: str) -> bool:
    '''Создание конфигурационных файлов'''

    try:
        with open(File, 'w') as HPV:
            if File.endswith('.json'):
                dump(Content, HPV, indent=4)
            else:
                HPV.write(Content)
    except:
        pass



def HPV_Check_Configs():
    '''Проверка наличия конфигурационных файлов'''

    HPV_Account_json = path.join(getcwd(), 'Core', 'Config', 'HPV_Account.json')
    HPV_Config_json = path.join(getcwd(), 'Core', 'Config', 'HPV_Config.json')
    HPV_Config_py = path.join(getcwd(), 'Core', 'Config', 'HPV_Config.py')
    HPV_Proxy_txt = path.join(getcwd(), 'Core', 'Proxy', 'HPV_Proxy.txt')

    FILES = {
        HPV_Account_json: {'ACCOUNT_1': 'https://bcoin2048.com/#tgWebAppData=query_id....', 'ACCOUNT_2': 'https://bcoin2048.com/#tgWebAppData=query_id....'},
        HPV_Config_json: '',
        HPV_Config_py: '\n\n# Автоматическое обновление программы\nAUTO_UPDATE = True # Для включения установите значение True, для отключения — False.\n# По умолчанию автообновление включено, и рекомендуется не изменять этот параметр. Однако, вы можете его отключить по соображениям безопасности!\n\n',
        HPV_Proxy_txt: ''
    }

    for File, Content in FILES.items():
        if not path.exists(File):
            HPV_Checking(File, Content)



def HPV_Config_Check(AUTO_UPDATE) -> None:
    '''Проверка конфига на валидность'''

    print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Проверка конфига... Подождите немного!')
    HPV_Check_Configs() # Проверка наличия конфигурационных файлов
    HPV_Upgrade(AUTO_UPDATE) # Автоматическая проверка и установка обновления
    Config = HPV_Get_Config() # Получение конфигурационных данных

    if Config:
        Accounts = HPV_Get_Accounts() # Получение списка аккаунтов
        ALL_PROXY = HPV_Proxy_Checker(_print=False) # Список всех доступных проксей
        USE_PROXY = [Proxy['Proxy'] for Proxy in Config] # Список используемых проксей
        INVALID_PROXY = [] # Список невалидных проксей

        USE_HEADERS = [Headers['Headers'] for Headers in Config] # Список используемых параметров для Headers

        THREADS = [] # Список потоков
        NEW_CONFIG = [] # Данные нового конфига, в случае изменений
        CHANGES = False # Были / небыли изменения


        # Проверка проксей каждой личности
        def HPV_Proxy_Check(Proxy) -> None:
            if not HPV_Request(Proxy):
                INVALID_PROXY.append(Proxy)


        # Получение свободного или малоиспользуемого прокси
        def HPV_New_Proxy():
            if FREE_PROXY: # Если есть свободные прокси из всего списка
                return FREE_PROXY.pop(0) # Берётся первый свободный прокси
            else: # Если свободных проксей нет
                USE_PROXY_COUNTER = Counter([dumps(_PROXY, sort_keys=True) for _PROXY in USE_PROXY])
                LEAST_USED_PROXY = loads(min(USE_PROXY_COUNTER, key=USE_PROXY_COUNTER.get))
                USE_PROXY.append(LEAST_USED_PROXY)
                return LEAST_USED_PROXY


        # Генерация новых параметров для Headers
        def HPV_New_Headers():
            while True:
                Headers = HPV_Headers() # Новые сгенерированные параметры для Headers
                if Headers not in USE_HEADERS:
                    return Headers


        # Проверка всех прокси, привязанных к аккаунтам
        print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Проверка проксей каждой личности... Подождите немного!')
        for Account in Config:
            if Account['Proxy']:
                THREAD = Thread(target=HPV_Proxy_Check, args=(Account['Proxy'],))
                THREAD.start()
                THREADS.append(THREAD)


        for THREAD in THREADS:
            THREAD.join()


        # Определение свободных прокси
        FREE_PROXY = [PROXY for PROXY in ALL_PROXY if PROXY not in USE_PROXY]


        # Замена невалидных прокси
        for Account in Config:
            if Account['Proxy'] in INVALID_PROXY: # Если прокси уникальной личности невалиден
                print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + f' — Найден невалидный прокси у `{Account["Name"]}`!')
                Account['Proxy'] = HPV_New_Proxy() # Новый прокси, взамен старого - нерабочего
                print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + f' — Прокси у `{Account["Name"]}` успешно заменён!')
                CHANGES = True


        # Сравнение аккаунтов в `HPV_Account.json` и `HPV_Config.json`
        print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Проверка наличия изменений в конфиге с аккаунтами... Подождите немного!')
        HPV_Account_Json, HPV_Config_Json = {(Name, URL) for Name, URL in Accounts.items()}, {(account['Name'], account['URL']) for account in Config}
        ACCOUNTS_TO_REMOVE = HPV_Config_Json - HPV_Account_Json # Неактуальные аккаунты
        NEW_ACCOUNTS = HPV_Account_Json - HPV_Config_Json # Новые аккаунты

        # Удаление неактуальных аккаунтов
        if ACCOUNTS_TO_REMOVE:
            print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Обнаружены неактуальные аккаунты. Производится их удаление...')
            NEW_CONFIG = [Account for Account in Config if (Account['Name'], Account['URL']) not in ACCOUNTS_TO_REMOVE] # Удаление неактуальных аккаунтов
            CHANGES = True

        # Добавление новых аккаунтов
        if NEW_ACCOUNTS:
            if not ACCOUNTS_TO_REMOVE:
                NEW_CONFIG = [Account for Account in Config] # Добавление текущих актуальных аккаунтов
            print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Обнаружены новые аккаунты. Выполняется их добавление...')
            for Name, URL in NEW_ACCOUNTS:
                Headers = HPV_New_Headers() # Генерация новых уникальных параметров для Headers
                NEW_CONFIG.append({'Name': Name, 'URL': URL, 'Proxy': HPV_New_Proxy(), 'Headers': Headers})
                USE_HEADERS.append(Headers)
                CHANGES = True


        # Сохранение данных при наличии изменений
        if CHANGES:
            print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Сохранение конфигурационных данных!')
            PATH = path.join(getcwd(), 'Core', 'Config', 'HPV_Config.json')
            with open(PATH, 'w', encoding='utf-8') as HPV:
                dump(NEW_CONFIG, HPV, ensure_ascii=False, indent=4)

    else:
        print(Fore.MAGENTA + '[HPV]' + Fore.YELLOW + ' — Конфигурационный файл не настроен или поврежден!')
        HPV_Config_Setup() # Настройка конфига




















class HPV_Bcoin2048:
    '''
    AutoBot Ferma /// HPV
    ---------------------
    [1] - `Получение кол-ва доступных игр и запуск их прохождения`
    
    [2] - `Выполнение ежедневного задания`
    
    [3] - `Ожидание от 6 до 9 часов`
    
    [4] - `Повторение действий через 6-9 часов`
    '''



    def __init__(self, Name: str, URL: str, Proxy: dict, Headers: dict, AUTO_UPDATE: bool, Lock: Lock) -> None:
        self.HPV_PRO = Session()           # Создание `requests` сессии
        self.Name = Name                   # Ник аккаунта
        self.Token = self.URL_Clean(URL)   # Уникальная ссылка для авторизации в mini app
        self.Proxy = Proxy                 # Прокси (при наличии)
        self.Domain = 'https://bcoin2048.com/api/v2' # Домен игры

        # Уникальные параметров для Headers
        self.USER_AGENT = Headers['USER_AGENT']
        self.SEC_CH_UA = Headers['SEC_CH_UA']
        self.SEC_CH_UA_MOBILE = Headers['SEC_CH_UA_MOBILE']
        self.SEC_CH_UA_PLATFORM = Headers['SEC_CH_UA_PLATFORM']
        self.X_REQUESTED_WITH = Headers['X_REQUESTED_WITH']
        self.ACCEPT_LANGUAGE = self.Get_Accept_Language()

        # Конфиг
        self.AUTO_UPDATE = AUTO_UPDATE # Автоматическое обновление программы

        self.Console_Lock = Lock



    def URL_Clean(self, URL: str) -> str:
        '''Очистка уникальной ссылки от лишних элементов'''

        try:
            return unquote(URL.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
        except:
            return ''



    def Current_Time(self) -> str:
        '''Текущее время'''

        return Fore.BLUE + f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'



    def Logging(self, Type: Literal['Success', 'Warning', 'Error'], Smile: str, Text: str) -> None:
        '''Логирование'''

        with self.Console_Lock:
            COLOR = Fore.GREEN if Type == 'Success' else Fore.YELLOW if Type == 'Warning' else Fore.RED # Цвет текста
            DIVIDER = Fore.BLACK + ' | '   # Разделитель

            Time = self.Current_Time()        # Текущее время
            Name = Fore.MAGENTA + self.Name   # Ник аккаунта
            Smile = COLOR + str(Smile)        # Смайлик
            Text = COLOR + Text               # Текст лога

            print(Time + DIVIDER + Smile + DIVIDER + Text + DIVIDER + Name)



    def Get_Accept_Language(self) -> str:
        '''Получение языкового параметра, подходящего под IP'''

        Accept_Language = HPV_Get_Accept_Language() # Получение данных с языковыми заголовками

        # Определение кода страны по IP
        try:
            COUNTRY = self.HPV_PRO.get('https://ipwho.is/', proxies=self.Proxy).json()['country_code'].upper()
        except:
            COUNTRY = ''

        return Accept_Language.get(COUNTRY, 'en-US,en;q=0.9')



    def Empty_Request(self, Empty: str) -> None:
        '''Отправка пустых запросов с подгрузкой дополнений сайта, чтобы казаться человеком'''

        Request: dict = HPV_Get_Empty_Request()[Empty]

        for header_key in list(Request['Headers'].keys()):
            header_key_lower = header_key.lower()

            if header_key_lower == 'user-agent':
                Request['Headers'][header_key] = self.USER_AGENT
            elif header_key_lower == 'sec-ch-ua':
                Request['Headers'][header_key] = self.SEC_CH_UA
            elif header_key_lower == 'sec-ch-ua-mobile':
                Request['Headers'][header_key] = self.SEC_CH_UA_MOBILE
            elif header_key_lower == 'telegram-init-data':
                Request['Headers'][header_key] = self.Token
            elif header_key_lower == 'sec-ch-ua-platform':
                Request['Headers'][header_key] = self.SEC_CH_UA_PLATFORM
            elif header_key_lower == 'x-requested-with':
                Request['Headers'][header_key] = self.X_REQUESTED_WITH
            elif header_key_lower == 'accept-language':
                Request['Headers'][header_key] = self.ACCEPT_LANGUAGE

        try:
            self.HPV_PRO.request(method=Request['Method'], url=Request['Url'], params=Request.get('Params'), data=Request.get('Data'), json=Request.get('Json'), headers=Request.get('Headers'), proxies=self.Proxy)
        except:
            pass



    def Random_List(self) -> list:
        '''Рандомизация листа'''

        NEW_List = ['UP', 'DOWN', 'LEFT', 'UP', 'RIGHT', 'DOWN', 'LEFT', 'UP', 'RIGHT', 'DOWN', 'LEFT', 'UP', 'RIGHT', 'DOWN', 'LEFT', 'UP']
        shuffle(NEW_List)

        return NEW_List



    def Get_Info(self) -> dict:
        '''Получение информации о балансе и достынх играх'''

        HEADERS = {'User-Agent': self.USER_AGENT, 'Content-Type': 'application/json', 'sec-ch-ua': self.SEC_CH_UA, 'sec-ch-ua-mobile': self.SEC_CH_UA_MOBILE, 'telegram-init-data': self.Token, 'sec-ch-ua-platform': self.SEC_CH_UA_PLATFORM, 'Origin': 'https://bcoin2048.com', 'X-Requested-With': self.X_REQUESTED_WITH, 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty', 'Referer': 'https://bcoin2048.com/', 'Accept-Language': self.ACCEPT_LANGUAGE}
        JSON = {'operationName': 'GetViewer', 'variables': {}, 'query': 'query GetViewer {\n  viewer {\n    id\n    energyUnits\n    nextEnergyUnitsAt\n    bicoinBalance\n    name\n    inviteesCount\n    inviteesInviteesCount\n    inviteesReward\n    inviteesInviteesReward\n    allTimeEarnedBicoins\n    photoURL\n    bestGameEver {\n      bicoinReward\n      score\n      __typename\n    }\n    bestGameDaily {\n      bicoinReward\n      score\n      __typename\n    }\n    features\n    inviterId\n    hadClaimedFirst2048Reward\n    isBot\n    deleteTileBoostersCount\n    moveBackBoostersCount\n    moveWithoutTileBoostersCount\n    adsWatchedToday\n    completedTasks\n    completedCheckpoints\n    dailyTasksStreak\n    dailyTasksLastCompletedAt\n    __typename\n  }\n}'}

        try:
            HPV = self.HPV_PRO.post(self.Domain, headers=HEADERS, json=JSON, proxies=self.Proxy).json()['data']['viewer']

            Games = HPV['energyUnits'] # Кол-во доступных игр
            Balance = HPV['bicoinBalance'] # Текущий баланс
            Daily_Tasks = HPV['dailyTasksStreak'] # Кол-во выполненных заданий подряд
            if Daily_Tasks < 8:
                Daily_Tasks += 1

            return {'Status': True, 'Games': Games, 'Balance_Server': f'{Balance:,.0f}', 'Balance_Bot': f'{Balance * 1000:,.0f}', 'Daily_Tasks': Daily_Tasks}
        except:
            return {'Status': False}



    def Play(self) -> None:
        '''Запуск игры'''

        Headers_StartGame = {'User-Agent': self.USER_AGENT, 'Content-Type': 'application/json', 'sec-ch-ua': self.SEC_CH_UA, 'sec-ch-ua-mobile': self.SEC_CH_UA_MOBILE, 'telegram-init-data': self.Token, 'sec-ch-ua-platform': self.SEC_CH_UA_PLATFORM, 'Origin': 'https://bcoin2048.com', 'X-Requested-With': self.X_REQUESTED_WITH, 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty', 'Referer': 'https://bcoin2048.com/', 'Accept-Language': self.ACCEPT_LANGUAGE}
        Headers_CancelGame = {'User-Agent': self.USER_AGENT, 'Content-Type': 'application/json', 'sec-ch-ua': self.SEC_CH_UA, 'sec-ch-ua-mobile': self.SEC_CH_UA_MOBILE, 'telegram-init-data': self.Token, 'sec-ch-ua-platform': self.SEC_CH_UA_PLATFORM, 'Origin': 'https://bcoin2048.com', 'X-Requested-With': self.X_REQUESTED_WITH, 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty', 'Referer': 'https://bcoin2048.com/game', 'Accept-Language': self.ACCEPT_LANGUAGE}
        Json_StartGame = {'operationName': 'startGame', 'variables': {}, 'query': 'mutation startGame {\n  StartGame {\n    id\n    status\n    field\n    nextIndexes\n    nextTiles\n    deletedTiles\n    __typename\n  }\n}'}
        Json_MyLastGame = {'operationName': 'myLastGame', 'variables': {}, 'query': 'query myLastGame {\n  MyLastGame {\n    id\n    status\n    field\n    nextTiles\n    nextIndexes\n    deletedTiles\n    __typename\n  }\n}'}

        try:
            self.Logging('Success', '🟢', 'Игра началась, ожидание 2-12 минут...')

            # Получение ID игры
            try:
                GID = self.HPV_PRO.post(self.Domain, headers=Headers_StartGame, json=Json_StartGame, proxies=self.Proxy).json()['data']['StartGame']['id']
            except:
                GID = self.HPV_PRO.post(self.Domain, headers=Headers_StartGame, json=Json_MyLastGame, proxies=self.Proxy).json()['data']['MyLastGame']['id']

            self.Empty_Request('Play_1') # Пустой запрос
            self.Empty_Request('Play_2') # Пустой запрос
            self.Empty_Request('Play_3') # Пустой запрос
            self.Empty_Request('Play_4') # Пустой запрос
            self.Empty_Request('Play_5') # Пустой запрос
            self.Empty_Request('Play_6') # Пустой запрос
            self.Empty_Request('Play_7') # Пустой запрос
            self.Empty_Request('Play_8') # Пустой запрос
            self.Empty_Request('Play_9') # Пустой запрос

            # Совершение ходов
            for _ in range(randint(11, 32)):
                try:
                    for _ in range(randint(7, 11)):
                        self.Empty_Request('Play_5') # Пустой запрос
                        sleep(randint(2, 3)) # Промежуточное ожидание

                    Json_sendMovesButch = {'operationName': 'sendMovesButch', 'variables': {'data': {'gameId': GID, 'moves': self.Random_List(), 'addedTiles': []}}, 'query': 'mutation sendMovesButch($data: GameMovesInput!) {\n  SendMovesButch(data: $data) {\n    id\n    field\n    status\n    nextIndexes\n    nextTiles\n    deletedTiles\n    __typename\n  }\n}'}
                    self.HPV_PRO.post(self.Domain, headers=Headers_CancelGame, json=Json_sendMovesButch, proxies=self.Proxy)
                    sleep(randint(9, 20)) # Промежуточное ожидание
                except:
                    pass

            # Завершение игры
            sleep(randint(3, 5)) # Промежуточное ожидание
            Json_CancelGame = {'operationName': 'CancelGame', 'variables': {'gameID': GID}, 'query': 'mutation CancelGame($gameID: ID!) {\n  CancelGame(gameID: $gameID)\n}'}
            self.HPV_PRO.post(self.Domain, headers=Headers_CancelGame, json=Json_CancelGame, proxies=self.Proxy).json()['data']
            self.Logging('Success', '🎮', 'Игра сыграна!')
        except:
            self.Logging('Error', '🔴', 'Игра не сыграна!')



    def AutoPlay(self, Games: int) -> None:
        '''Автоматическое получение кол-ва доступных игр и запуск их прохождения'''

        try:
            if Games > 0:
                self.Logging('Success', '🎮', f'Игр доступно: {Games}!')

                for _ in range(Games):
                    self.Play()

                    self.Get_Info() # Пустой запрос
                    self.Empty_Request('Authentication_13') # Пустой запрос
                    self.Empty_Request('Authentication_14') # Пустой запрос
                    self.Empty_Request('Authentication_16') # Пустой запрос
                    self.Empty_Request('Authentication_17') # Пустой запрос
                    self.Empty_Request('Play_10') # Пустой запрос
                    self.Empty_Request('Authentication_19') # Пустой запрос
                    self.Empty_Request('Play_11') # Пустой запрос
                    self.Empty_Request('Authentication_11') # Пустой запрос
                    self.Empty_Request('Authentication_18') # Пустой запрос

                    sleep(randint(3, 5)) # Промежуточное ожидание
        except:
            pass



    def Daily_Task(self, ID: int) -> bool:
        '''Выполнение ежедневного задания'''

        HEADERS = {'User-Agent': self.USER_AGENT, 'Content-Type': 'application/json', 'sec-ch-ua': self.SEC_CH_UA, 'sec-ch-ua-mobile': self.SEC_CH_UA_MOBILE, 'telegram-init-data': self.Token, 'sec-ch-ua-platform': self.SEC_CH_UA_PLATFORM, 'Origin': 'https://bcoin2048.com', 'X-Requested-With': self.X_REQUESTED_WITH, 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty', 'Referer': 'https://bcoin2048.com/daily-tasks', 'Accept-Language': self.ACCEPT_LANGUAGE}
        JSON = {'operationName': 'CheckIfDailyTaskCompleted', 'variables': {'taskID': ID}, 'query': 'mutation CheckIfDailyTaskCompleted($taskID: Int!) {\n  CheckIfDailyTaskCompleted(taskID: $taskID)\n}'}

        try:
            return self.HPV_PRO.post(self.Domain, headers=HEADERS, json=JSON, proxies=self.Proxy).json()['data']['CheckIfDailyTaskCompleted']
        except:
            return False



    def AutoDailyTask(self, ID: int) -> None:
        '''Выполнение ежедневного задания'''

        try:
            self.Empty_Request('AutoDailyTask_1') # Пустой запрос
            self.Empty_Request('AutoDailyTask_2') # Пустой запрос

            if self.Daily_Task(ID):
                self.Logging('Success', '🟢', 'Ежедневное задание выполнено!')

                self.Get_Info() # Пустой запрос
                self.Empty_Request('AutoDailyTask_3') # Пустой запрос
        except:
            pass



    def Get_Tasks(self) -> None:
        '''Пустой запрос просмотра заданий'''

        HEADERS = {'User-Agent': self.USER_AGENT, 'Content-Type': 'application/json', 'sec-ch-ua': self.SEC_CH_UA, 'sec-ch-ua-mobile': self.SEC_CH_UA_MOBILE, 'telegram-init-data': self.Token, 'sec-ch-ua-platform': self.SEC_CH_UA_PLATFORM, 'Origin': 'https://bcoin2048.com', 'X-Requested-With': self.X_REQUESTED_WITH, 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty', 'Referer': 'https://bcoin2048.com/earn', 'Accept-Language': self.ACCEPT_LANGUAGE}
        JSON = {'operationName': 'getAllTasks', 'variables': {}, 'query': 'query getAllTasks {\n  tasks {\n    id\n    name\n    rewards {\n      bicoins\n      boosters\n      __typename\n    }\n    usersCompletedTask\n    maxUsersCompletedTask\n    description\n    logo\n    checkpoints {\n      id\n      name\n      link\n      taskId\n      isDummy\n      __typename\n    }\n    __typename\n  }\n}'}

        try:
            self.HPV_PRO.post(self.Domain,  headers=HEADERS, json=JSON, proxies=self.Proxy).json()['data']['tasks']
        except:
            pass



    def Get_Boosts(self) -> None:
        '''Пустой запрос просмотра бустов'''

        self.Empty_Request('Get_Boosts_1') # Пустой запрос
        self.Empty_Request('Get_Boosts_2') # Пустой запрос
        self.Empty_Request('Get_Boosts_3') # Пустой запрос
        self.Empty_Request('Get_Boosts_4') # Пустой запрос
        self.Empty_Request('Get_Boosts_5') # Пустой запрос



    def Get_Halving(self) -> None:
        '''Пустой запрос просмотра халвинга'''

        self.Empty_Request('Get_Halving_1') # Пустой запрос
        self.Empty_Request('Get_Halving_2') # Пустой запрос



    def Run(self) -> None:
        '''Активация бота'''

        while True:
            try:

                # Имитация захода в игру
                self.Empty_Request('Authentication_1') # Пустой запрос
                self.Empty_Request('Authentication_2') # Пустой запрос
                self.Empty_Request('Authentication_3') # Пустой запрос
                self.Empty_Request('Authentication_4') # Пустой запрос
                self.Empty_Request('Authentication_5') # Пустой запрос
                self.Empty_Request('Authentication_6') # Пустой запрос
                self.Empty_Request('Authentication_7') # Пустой запрос
                self.Empty_Request('Authentication_8') # Пустой запрос
                self.Empty_Request('Authentication_9') # Пустой запрос
                self.Empty_Request('Authentication_10') # Пустой запрос
                self.Empty_Request('Authentication_11') # Пустой запрос
                self.Empty_Request('Authentication_12') # Пустой запрос
                self.Empty_Request('Authentication_13') # Пустой запрос
                self.Empty_Request('Authentication_14') # Пустой запрос
                self.Empty_Request('Authentication_15') # Пустой запрос
                self.Empty_Request('Authentication_16') # Пустой запрос
                self.Empty_Request('Authentication_17') # Пустой запрос
                self.Empty_Request('Authentication_18') # Пустой запрос
                self.Empty_Request('Authentication_19') # Пустой запрос

                # Get_Info > 20 запрос при аутентификации
                INFO = self.Get_Info() # Получение информации о балансе и достынх играх

                if INFO['Status']: # Если аутентификация успешна
                    self.Logging('Success', '🟢', 'Инициализация успешна!')


                    Balance_Server = INFO["Balance_Server"] # Баланс который на сервере
                    Balance_Bot = INFO["Balance_Bot"] # Баланс который в игре
                    self.Logging('Success', '💰', f'Текущий баланс: {Balance_Bot} (бот) /// {Balance_Server} (сервер)')
                    sleep(randint(4, 9)) # Промежуточное ожидание


                    # Проверка на недавний фарм
                    if not INFO['Games']:
                        _Waiting = randint(6*60*60, 9*60*60) # Значение времени в секундах для ожидания
                        Waiting_STR = (datetime.now() + timedelta(seconds=_Waiting)).strftime('%Y-%m-%d %H:%M:%S') # Значение времени в читаемом виде

                        self.Logging('Warning', '⏳', f'Сбор уже производился! Следующий сбор: {Waiting_STR}!')

                        # Ожидание конца майнинга
                        _Waiting_For_Upgrade = int(_Waiting / (60*30))
                        for _ in range(_Waiting_For_Upgrade):
                            if HPV_Upgrade_Alert(self.AUTO_UPDATE): # Проверка наличия обновления
                                return
                            sleep(60*30)
                        sleep(_Waiting - (_Waiting_For_Upgrade * 60 * 30))
                        continue


                    # Рандомное выполнение действий
                    Autos = [lambda: self.AutoPlay(INFO['Games']), lambda: self.AutoDailyTask(INFO['Daily_Tasks']), self.Get_Boosts, self.Get_Halving]
                    shuffle(Autos) # Перемешивание списока функций
                    for Auto in Autos:
                        Auto() # Запуск случайных действий: запуск игр, выполнение заданий, выполнение ежедневного задания, пустой запрос просмотра бустов и халвинга
                        sleep(randint(3, 5)) # Промежуточное ожидание


                    Waiting = randint(6*60*60, 9*60*60) # Значение времени в секундах для ожидания
                    Waiting_STR = (datetime.now() + timedelta(seconds=Waiting)).strftime('%Y-%m-%d %H:%M:%S') # Значение времени в читаемом виде


                    _INFO = self.Get_Info()
                    Balance_Server = _INFO["Balance_Server"] # Баланс который на сервере
                    Balance_Bot = _INFO["Balance_Bot"] # Баланс который в игре
                    self.Logging('Success', '💰', f'Текущий баланс: {Balance_Bot} (бот) /// {Balance_Server} (сервер)')
                    self.Logging('Warning', '⏳', f'Следующий сбор: {Waiting_STR}!')


                    # Ожидание от 6 до 9 часов
                    Waiting_For_Upgrade = int(Waiting / (60*30))
                    for _ in range(Waiting_For_Upgrade):
                        if HPV_Upgrade_Alert(self.AUTO_UPDATE): # Проверка наличия обновления
                            return
                        sleep(60*30)
                    sleep(Waiting - (Waiting_For_Upgrade * 60 * 30))

                else: # Если аутентификация не успешна
                    self.Logging('Error', '🔴', 'Ошибка инициализации!')
                    if HPV_Upgrade_Alert(self.AUTO_UPDATE): # Проверка наличия обновления
                        return
                    sleep(randint(33, 66)) # Ожидание от 33 до 66 секунд

            except:
                if HPV_Upgrade_Alert(self.AUTO_UPDATE): # Проверка наличия обновления
                    return




















def HPV_Main(AUTO_UPDATE: bool) -> None:
    '''Запуск Bcoin2048'''

    if s_name() == 'Windows':
        sys(f'cls && title HPV Bcoin2048 - V{VERSION}')
    else:
        sys('clear')

    while True:
        HPV_Banner() # Вывод баннера
        HPV_Config_Check(AUTO_UPDATE) # Проверка конфига на валидность
        print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Проверка конфига окончена... Скрипт запустится через 5 секунд...\n'); sleep(5)

        Console_Lock = Lock()
        Threads = [] # Список потоков

        def Start_Thread(Name: str, URL: str, Proxy: dict, Headers: dict) -> None:
            Bcoin2048 = HPV_Bcoin2048(Name, URL, Proxy, Headers, AUTO_UPDATE, Console_Lock)
            Bcoin2048.Run()

        # Получение конфигурационных данных и запуск потоков
        for Account in HPV_Get_Config(_print=False):
            HPV = Thread(target=Start_Thread, args=(Account['Name'], Account['URL'], Account['Proxy'], Account['Headers'],))
            HPV.start()
            Threads.append(HPV)

        for thread in Threads:
            thread.join()






