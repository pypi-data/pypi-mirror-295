import requests
import sqlite3
# filename = 'pa_novel_test_active_01.py'
url_0 = 'https://62.kehou1.icu//api.php/index/getWzDetail?id=38105'
url = 'https://62.kehou1.icu//api.php/index/getWzDetail?id='


def create_sqlite_db():
    conn = sqlite3.connect('novel.db')
    cursor = conn.cursor()
    sql = 'create table if not exists novels (id integer primary key autoincrement, ok integer, novel text)'
    cursor.execute(sql)
    conn.commit()
    conn.close()
    print('创建数据库成功！')


def novel_to_sqlite(ok, novel):
    conn = sqlite3.connect('novel.db')
    cursor = conn.cursor()
    sql = 'insert into novels (ok, novel) values (?, ?)'
    cursor.execute(sql, (ok, novel))
    conn.commit()
    conn.close()


def main(start_num=0, end_num=38105):
    ok = 0
    novel = ' '
    create_sqlite_db()
    for i in range(start_num, end_num):
        try:
            response = requests.get(url + str(i), timeout=30)
        except Exception as e:
            novel = str(e)
            ok = 0
        else:
            novel = response.text
            ok = 1
        finally:
            novel_to_sqlite(ok, novel)
        print(f'({i + 1 - start_num}/{end_num - start_num})')
    pass


if __name__ == '__main__':
    response0 = requests.get(url_0)
    print(response0.text)
    main(3, 5)
