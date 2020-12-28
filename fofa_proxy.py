# -*- coding: utf-8 -*-
import fofa
import requests


def check(proxy_ip, proxy_port):
    url = 'https://www.baidu.com'
    proxies = {
        'https': fr'socks5://{proxy_ip}:{proxy_port}'
    }
    try:
        requests.get(url=url, proxies=proxies, timeout=3)
        print('success')
    except requests.exceptions.ConnectionError:
        print('error')
    except requests.exceptions.ReadTimeout:
        print('timeout')
    except KeyboardInterrupt:
        print('用户退出')
        exit()
    except requests.exceptions.InvalidSchema:
        print('未检测到pysocks')
        print('pip install -U requests[socks]')
        print('pip install pysocks')
        exit()


if __name__ == "__main__":
    email, key = ('test@qq.com', 'key')
    client = fofa.Client(email, key)
    query_str = 'protocol="socks5"&&"Authentication"'
    for page in range(1, 5):
        data = client.get_data(query_str, page=page, fields="ip,port")
        for ip, port in data["results"]:
            print("%s,%s" % (ip, port))
            check(ip, port)
