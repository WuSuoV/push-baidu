import json
import os.path
import re

import requests

def get_config():
    file = "config.json"
    if not os.path.exists(file):
        with open(file,'w',encoding='utf8') as f:
            txt = '{\n' \
                  '"api": "",\n' \
                  '"##": "mode：local or sitemap",\n' \
                  '"mode": "",\n' \
                  '"##": "如果是local就写本地路径，如果是sitemap就写链接",\n' \
                  '"path": ""\n' \
                  '}'
            f.write(txt)

    with open(file,'r',encoding='utf8') as f:
        return json.load(f)

myconfig = get_config()

def push_baidu(url):
    api = myconfig['api']

    headers = {
        "User-Agent": "curl/7.12.1",
        "Host": "data.zz.baidu.com",
        "Content-Type": "text/plain",
        "Content-Length": "83"
    }

    respons = requests.post(url=api, data=url, headers=headers)
    return respons.text

def get_urls_txt(file):
    with open(file=file, mode='r', encoding='utf8') as f:
        return f.read()

def get_urls_xml(url):
    res_text = requests.get(url).text
    urls = re.findall(r"<loc>(.+?)</loc>", res_text)
    urls_txt = ""
    for i in urls:
        urls_txt += f"{i}\n"
    return urls_txt


if __name__ == '__main__':
    print(">>> Github: https://github.com/Qiantigers/push-baidu\n\n"
          ">>> 勿埋我心博客: https://www.qian.blue\n\n")
    try:
        mode = myconfig['mode']
        if mode == 'local':
            urls = get_urls_txt(myconfig['path'])
            print(push_baidu(urls))
        elif mode == 'sitemap':
            urls = get_urls_xml(myconfig['path'])
            print(push_baidu(urls))
        else:
            print("config.json配置错误，请检查！")
        input('按任意键退出……')
    except Exception as e:
        print("config.json配置错误，请检查！")
        input('按任意键退出……')
