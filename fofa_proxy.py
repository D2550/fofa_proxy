import fofa
import requests
import os
import threading
from queue import Queue

# 设置线程数
THREAD_NUM = 10

# 定义任务队列
task_queue = Queue()

# 初始化 FOFA 客户端
email, key = ('email', 'key')
client = fofa.Client(email, key)


def check_proxy():
    while not task_queue.empty():
        proxy_ip, proxy_port = task_queue.get()
        url = 'https://www.baidu.com'
        proxies = {
            'https': fr'socks5://{proxy_ip}:{proxy_port}'
        }
        try:
            requests.get(url=url, proxies=proxies, timeout=3)
            print(fr'[*] success: socks5://{proxy_ip}:{proxy_port}')
            # r = requests.get('https://www.taobao.com/help/getip.php', proxies=proxies, timeout=3)
            # public_ip = r.text.replace('ipCallback({ip:"', '').replace('"})', '')
            # print('[*] 出口IP:', end='')
            # os.system('nali ' + public_ip)
            with open('success.txt', 'a') as file:
                file.write(fr'[*] success: socks5://{proxy_ip}:{proxy_port}' + '\n')
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.ReadTimeout:
            pass
        except KeyboardInterrupt:
            print('用户退出')
            exit()
        except requests.exceptions.InvalidSchema:
            print('未检测到pysocks')
            print('pip install -U requests[socks]')
            print('pip install pysocks')
            exit()


def worker():
    while True:
        check_proxy()


def main():
    query_str = 'protocol="socks5"&&"Authentication"'
    for page in range(1, 5):
        data = client.get_data(query_str, page=page, fields="ip,port")
        for ip, port in data["results"]:
            task_queue.put((ip, port))

    threads = []
    for i in range(THREAD_NUM):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
