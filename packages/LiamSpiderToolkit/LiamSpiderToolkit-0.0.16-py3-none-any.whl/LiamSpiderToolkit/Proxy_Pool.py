# import requests
# import time
#
# proxy_url = 'http://v2.api.juliangip.com/dynamic/getips?auto_white=1&num=1&pt=1&result_type=text&split=1&trade_no=1311726158969977&sign=6cdb3de729d7d95fa5f5bf8ae9c5b879'
# proxy_pool = []  # 用于存储可用的代理IP
#
# def fetch_proxy():
#     """从给定的URL获取代理IP"""
#     response = requests.get(proxy_url)
#     if response.status_code == 200:
#         proxy_ip = response.text.strip()  # 假设返回的IP是文本格式且没有额外的空格或换行符
#         return proxy_ip
#     else:
#         return None
#
# def test_proxy(proxy_ip):
#     """测试代理IP的可用性"""
#     proxies = {
#         'http': f'http://{proxy_ip}',
#         'https': f'https://{proxy_ip}',
#     }
#     try:
#         response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=5)
#         response.raise_for_status()  # 如果请求成功，则不会抛出异常
#         # 如果需要更严格的验证（例如，检查响应内容中的特定IP地址），可以在这里添加
#         return True
#     except requests.RequestException:
#         return False
#
# def main():
#     i = 0
#     while i < 100:  # 你可以根据需要设置循环条件，比如只获取一定数量的代理
#         proxy_ip = fetch_proxy()
#         print(f"Fetched proxy: {proxy_ip}")
#         if proxy_ip and test_proxy(proxy_ip):
#             proxy_pool.append(proxy_ip)
#             print(f"Added valid proxy: {proxy_ip}")
#         # 可以在这里添加一些延时，以避免对目标API造成过大压力
#         time.sleep(5)  # 需要先导入time模块
#         print(f"Current pool size: {len(proxy_pool)}")
#         i += 1
#
# if __name__ == '__main__':
#     main()


# import requests
#
# def test_proxy(proxy_url):
#     """测试代理IP的可用性"""
#     proxies = {
#         'http': proxy_url,
#         'https': proxy_url,  # 如果代理同时支持HTTP和HTTPS，可以这样设置
#     }
#     try:
#         # 尝试通过代理发送请求到httpbin.org/ip
#         response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=5)
#         response.raise_for_status()  # 如果请求成功，则不会抛出异常
#         # 检查响应内容中是否包含了预期的代理IP地址（可选）
#         # 注意：由于httpbin.org返回的是你的公网IP，而不是代理的IP，
#         # 所以这里不能直接通过检查响应内容来验证代理的IP。
#         # 你可能需要检查其他指标，比如请求是否成功通过代理发送。
#         print("代理测试成功，请求成功发送。")
#         return True
#     except requests.RequestException as e:
#         print(f"代理测试失败：{e}")
#         return False
#
# # 测试代理IP
# proxy_url = 'http://v2.api.juliangip.com/dynamic/getips?auto_white=1&num=1&pt=1&result_type=text&split=1&trade_no=1311726158969977&sign=6cdb3de729d7d95fa5f5bf8ae9c5b879'
# proxy_url1 = requests.get(proxy_url).text
# # proxy_url = 'http://111.224.220.171:49015'
# if test_proxy(proxy_url1):
#     print(f"代理IP {proxy_url1} 是可用的。")
# else:
#     print(f"代理IP {proxy_url1} 不可用。")


# import requests
# from requests.auth import HTTPProxyAuth
#
# def test_proxy(proxy_url, proxy_user, proxy_pass):
#     """测试代理IP的可用性，包括认证信息"""
#     proxies = {
#         'http': proxy_url,
#         'https': proxy_url,
#     }
#     # 如果代理需要认证，则添加HTTPProxyAuth
#     auth = HTTPProxyAuth(proxy_user, proxy_pass)
#     try:
#         # 注意：由于requests库在代理认证方面的实现，你可能需要将auth参数直接传递给requests函数
#         # 但是，对于简单的代理认证，通常不需要显式传递auth到requests.get()，
#         # 因为requests会自动处理proxies字典中的http(s)://user:pass@host:port格式的URL。
#         # 如果上述方法不起作用，你可能需要自定义一个适配器或使用其他库来处理代理认证。
#
#         # 尝试方法1：直接在proxies URL中包含用户名和密码（如果代理服务器支持这种格式）
#         # proxies_with_auth = f'http://{proxy_user}:{proxy_pass}@{proxy_url.split("//")[1]}'
#         # 但请注意，这种方法可能不适用于所有代理服务器，特别是当代理URL已经包含端口号时。
#
#         # 因此，我们尝试另一种方法，使用requests的Session和自定义的TransportAdapter（如果需要的话）
#         # 但为了简化，我们首先尝试在URL中直接包含认证信息（如果它有效的话）
#         # 注意：这里我们假设proxy_url不包含端口号之后的路径部分
#         proxy_host = proxy_url.split("//")[1].split(":")[0]
#         proxy_port = proxy_url.split("//")[1].split(":")[1] if ":" in proxy_url.split("//")[1] else "80"  # 默认HTTP端口为80，但这里可能是HTTPS的443或其他
#         proxies_with_auth = f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}'
#
#         # 现在我们可以尝试使用这个带有认证的代理URL
#         response = requests.get('https://www.baidu.com', proxies=proxies_with_auth, timeout=5)
#         response.raise_for_status()  # 如果请求成功，则不会抛出异常
#         print("代理测试成功，请求成功发送。")
#         return True
#     except requests.RequestException as e:
#         print(f"代理测试失败：{e}")
#         return False
#
# # 测试代理IP，包括用户名和密码
# proxy_url = 'http://v2.api.juliangip.com/dynamic/getips?auto_white=1&num=1&pt=1&result_type=text&split=1&trade_no=1311726158969977&sign=6cdb3de729d7d95fa5f5bf8ae9c5b879'
# proxy_url = requests.get(proxy_url).text
# # proxy_url = 'http://111.224.220.171:49015'
# proxy_user = '13526527597'  # 替换为你的代理用户名
# proxy_pass = 'YvpW8AMm'  # 替换为你的代理密码
#
# if test_proxy(proxy_url, proxy_user, proxy_pass):
#     print(f"代理IP {proxy_url}（带认证）是可用的。")
# else:
#     print(f"代理IP {proxy_url}（带认证）不可用。")


if __name__ == '__main__':
    """
    使用requests请求代理服务器
    请求http和https网页均适用
    """
    import requests

    # 提取代理API接口，获取1个代理IP
    api_url = 'http://v2.api.juliangip.com/dynamic/getips?auto_white=1&num=1&pt=1&result_type=text&split=1&trade_no' \
              '=1311726158969977&sign=6cdb3de729d7d95fa5f5bf8ae9c5b879 '

    # 获取API接口返回的代理IP
    proxy_ip = requests.get(api_url).text

    # 用户名密码认证(动态代理/独享代理)
    username = "13526527597"
    password = "YvpW8AMm"
    proxies = {
        "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip},
        "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip},
    }

    # 白名单方式（需提前设置白名单）
    # proxies = {
    #     "http": "http://%(proxy)s/" % {"proxy": proxy_ip},
    #     "https": "http://%(proxy)s/" % {"proxy": proxy_ip},
    # }

    # 要访问的目标网页
    target_url = "https://www.juliangip.com/api/general/Test"

    # 使用代理IP发送请求
    response = requests.get(target_url, proxies=proxies)

    # 获取页面内容
    if response.status_code == 200:
        print(response.text)

import requests


def get_proxies():
    """获取代理IP"""
    api_url = "http://v2.api.juliangip.com/dynamic/getips?auto_white=1&num=1&pt=1&result_type=text&split=1&trade_no=1311726158969977&sign=6cdb3de729d7d95fa5f5bf8ae9c5b879"
    proxy_ip = requests.get(api_url).text
    username = "13526527597"
    password = "YvpW8AMm"
    proxies = {
        "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip},
        "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip},
    }
    print('注意：代理IP: {} 的有效期仅有30秒'.format(proxy_ip))
    return proxies


def get_proxy():
    """获取代理IP"""
    api_url = "http://v2.api.juliangip.com/dynamic/getips?auto_white=1&num=1&pt=1&result_type=text&split=1&trade_no=1311726158969977&sign=6cdb3de729d7d95fa5f5bf8ae9c5b879"
    proxy_ip = requests.get(api_url).text
    return proxy_ip


def check_proxy(proxies):
    """测试代理IP是否可用"""
    try:
        response = requests.get("https://www.juliangip.com/api/general/Test", proxies=proxies, timeout=10)
        if response.status_code == 200:
            return True
        else:
            return False
        pass
    except Exception as e:
        return False


def get_yourself_proxies(api_url=None, username=None, password=None):
    """获取代理IP"""
    if api_url is None:
        api_url = "http://v2.api.juliangip.com/dynamic/getips?auto_white=1&num=1&pt=1&result_type=text&split=1&trade_no=1311726158969977&sign=6cdb3de729d7d95fa5f5bf8ae9c5b879"
    if username is None:
        username = "13526527597"
    if password is None:
        password = "YvpW8AMm"
    proxy_ip = requests.get(api_url).text
    proxies = {
        "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip},
        "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip},
    }
    print('代理IP: {} 的有效期仅有30秒到60秒'.format(proxy_ip))
    return proxies
