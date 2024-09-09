# import sqlite3
# import Spader_nover_jiami_to_sqliit
# conn = sqlite3.connect('novels.db')
# cursor = conn.cursor()
# # sql = 'insert into novels (novel_name, novel) values (?, ?)'
# # cursor.execute(sql, ('novel_name', 'novel'))
#
# a = cursor.execute('select * from novels')
# for i in a:
#     print(i)
#
# conn.commit()
# print('Select from db success!')

# LiamSpiderToolkit.Proxy_Pool
# .check_proxy(proxies)
# .get_proxies()

import LiamSpiderToolkit
print(LiamSpiderToolkit.Proxy_Pool.get_proxies())
# pa_novel_test_active_01












if __name__ == '__main__':
    """
    包测试文件
    """