import json
import os

import requests
from bserpy import Client

API_KEY = os.environ["ER_API_KEY"]
WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]
NICKNAME = os.environ["ER_NICKNAME"]
SEEN_FILE = "seen_games.json"


def load_seen():
    try:
        with open(SEEN_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except FileNotFoundError:
        return None


def save_seen(ids):
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(ids)[-100:], f)


def make_message(g):
    return "웨에에옹"


def send_discord(text):
    r = requests.post(
        WEBHOOK_URL,
        json={"content": text, "username": "우는 고양이 😿"},
    )
    print("디스코드 전송 결과:", r.status_code)
    return r.status_code in (200, 204)


def main():
    with Client(api_key=API_KEY) as client:
        user = client.users.get_uid(NICKNAME)
        games = client.users.get_games(user.user_id)
        ids = {g.game_id for g in games}
        seen = load_seen()

        if seen is None:
            save_seen(ids)
            print("처음 실행이라 기준만 저장했어요.")
            return

        new_games = [g for g in games if g.game_id not in seen]
        new_games.sort(key=lambda g: g.game_id)
        for g in new_games:
            if send_discord(make_message(g)):
                seen.add(g.game_id)
        save_seen(seen)
        print("확인 완료. 새 게임:", len(new_games), "개")


main()
