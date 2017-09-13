import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool

#获取单页
def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

#解析网页
def parse_one_page(html):
    #通过re将正则表达式字符串转换成正则表达式对象，做到这里发现猫眼封了爬虫，改爬豆瓣
    pattern = re.compile('<li>.*?item.*?title">(.*?)</span>.*?inq">(.*?)</span>.*?</li>', re.S)
    items = re.findall(pattern, html)
    #格式化
    for item in items:
        yield{
            'name': item[0],
            'comments': item[1]
        }

#输出到txt
def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()

def main(start):
    url = 'https://movie.douban.com/top250?start=' + str(start) + '&filter='
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    #创建进程池，实现秒抓
    pool = Pool()
    pool.map(main, [i*25 for i in range(10)])