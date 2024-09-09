# 该模块是有关python爬虫相关的知识文档以及用法

# todo 导入所需的包

# 连接数据库的包
import sqlite3

# 爬虫相关的包
import requests
import bs4



# todo 函数实现：

# sqlite3创建数据库表
import sqlite3
conn = sqlite3.connect('test.db')  # 数据库文件是test.db，如果文件不存在，会自动在当前目录创建:
cursor = conn.cursor()  # 创建一个Cursor
# 执行一条SQL语句，创建user表:
cursor.execute('CREATE TABLE IF NOT EXISTS user (id VARCHAR(20) PRIMARY KEY, name TEXT, age INTEGER)')
print(cursor.rowcount)  # 通过rowcount获得插入的行数
cursor.close()  # 关闭Cursor
conn.commit()  # 提交事务
conn.close()  # 关闭Connection

'''
    也可以这样使用sql语句：
    novel_name, novel = '', ''
    sql = 'insert into novels (novel_name, novel) values (?, ?)'
    cursor.execute(sql, (novel_name, novel))    
'''
# sqlite3增删改查
# 插入数据
import sqlite3
conn = sqlite3.connect('example.db')  # 连接到SQLite数据库
cursor = conn.cursor()  # 创建一个Cursor对象
# 插入一行数据
cursor.execute("INSERT INTO stocks VALUES ('2023-04-01','BUY','RHAT',100,35.14)")
conn.commit()  # 提交事务
conn.close()  # 关闭Connection

# 查询数据
import sqlite3
conn = sqlite3.connect('example.db')  # 连接到SQLite数据库
cursor = conn.cursor()  # 创建一个Cursor对象
# 查询数据
cursor.execute("SELECT * FROM stocks WHERE symbol='RHAT'")
print(cursor.fetchall())  # 获取查询结果
conn.close()  # 关闭Connection

# 更新数据
import sqlite3
conn = sqlite3.connect('example.db')  # 连接到SQLite数据库
cursor = conn.cursor()  # 创建一个Cursor对象
# 更新数据
cursor.execute("UPDATE stocks SET price = 35.14 WHERE symbol = 'IBM'")
conn.commit()  # 提交事务
conn.close()  # 关闭Connection

# 删除数据
import sqlite3
conn = sqlite3.connect('example.db')  # 连接到SQLite数据库
cursor = conn.cursor()  # 创建一个Cursor对象
# 删除数据
cursor.execute("DELETE FROM stocks WHERE symbol = 'MSFT'")
conn.commit()  # 提交事务
conn.close()  # 关闭Connection