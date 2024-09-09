import os
import requests
import sqlite3

def  get_novel_jiami(url):
    response = requests.get(url)
    return response.text

# 将小说内容保存到数据库
def save_to_db(novel, novel_name):
    conn = sqlite3.connect('novels.db')
    cursor = conn.cursor()
    sql = 'insert into novels (novel_name, novel) values (?, ?)'
    cursor.execute(sql, (novel_name, novel))
    conn.commit()
    print('Save to db success!')

# 创建数据库表
def create_table():
    conn = sqlite3.connect('novels.db')
    cursor = conn.cursor()
    sql = 'create table if not exists novels (id integer primary key autoincrement, novel_name text, novel text)'
    cursor.execute(sql)
    print('Create table success!')

def main(url, start=0, end=100):
    create_table()
    for i in range(1, 2):
        url_0 = os.path.join(url, str(i))
        html = get_novel_jiami(url_0)
        save_to_db(html, url_0)
    print(f'main({url}), end')
# 主程序
if __name__ == '__main__':
    create_table()
    url = 'https://www.xbiquge.la/2_2074/'
    for i in range(1, 2):
        url = f'https://www.xbiquge.la/2_2074/{i}/'
        html = get_novel_jiami(url)
        save_to_db(html, url)
























# import requests
# import os
#
# # 获取文件列表
# def get_file_list():
#     url = 'http://127.0.0.1:8000/api/files/'
#     response = requests.get(url)
#     return response.json()['data']
#
# # 下载文件
# def download_file(file):
#     url = f'http://127.0.0.1:8000/api/download/{file}'
#     response = requests.get(url, stream=True)
#     with open(f'./{file}', 'wb') as f:
#         for chunk in response.iter_content(chunk_size=512):
#             if chunk:
#                 f.write(chunk)
#
# # 删除文件
# def delete_file(file):
#     url = f'http://127.0.0.1:8000/api/delete/{file}'
#     requests.delete(url)
#
# # 主程序
# if __name__ == '__main__':
#     files = get_file_list()
#     print('Files:', files)
#     for file in files:
#
#         download_file(file)
#         delete_file(file)
#     print('Download and delete files successfully!')
#     os.system("pause")


# import sqlite3
# import requests
# from bs4 import BeautifulSoup
#
#
# def get_html(url):
#     response = requests.get(url)
#     return response.text
#
#
# def parse_html(html):
#     soup = BeautifulSoup(html, 'lxml')
#     a_list = soup.find('div', class_='main').find_all('a')
#     return a_list
#
#
# def save_to_db(url):
#     conn = sqlite3.connect('data.db')
#     cursor = conn.cursor()
#     cursor.execute('create table if not exists data (url text)')
#     cursor.execute('insert into data values (?)', (url,))
#     conn.commit()
#     conn.close()
#     return True
#
#
# def main():
#     url = 'https://www.cnblogs.com/'
#     html = get_html(url)
#     a_list = parse_html(html)
#     for a in a_list:
#         href = a['href']
#         save_to_db(href)
#     print('Save successfully!')
#
#
# if __name__ == '__main__':
#     main()
#     print('Done!')
#     pass
# pass
