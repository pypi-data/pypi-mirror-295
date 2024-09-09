import requests
def download_file(url, local_path, chunk_size=1024):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    print("文件下载成功,保存在:", local_path)
                else:
                    print("文件下载失败,状态码:", response.status_code)

if __name__ == '__main__':
    url = 'https://cdn.mysql.com/archives/mysql-8.4/mysql-8.4.0-linux-glibc2.28-x86_64.tar'
    local_path = 'MySQL/mysql-8.4.0-linux-glibc2.28-x86_64.tar'
    download_file(url, local_path)