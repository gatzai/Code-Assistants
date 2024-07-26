import requests
import json
import time
import re

'''
根据 all_url 爬取 bannergress 中的任务meta数据，规范化文本形式，减少工作量
'''

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0",
    'Content-Type': 'text/html; charset=UTF-8',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ru;q=0.6,zh-TW;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Upgrade-Insecure-Requests': '1'
}

all_url = [
    "https://bannergress.com/banner/%E6%A9%98%E7%8C%AB%E7%8C%AB%E6%97%A5%E4%B9%9F%E6%83%B3%E5%96%9D%E8%8C%B6%E9%A2%9C-5bd6",
    "https://bannergress.com/banner/csx-%E5%B8%86%E8%88%B9%E8%BF%90%E5%8A%A8-62bc",
    "https://bannergress.com/banner/eva%E4%BD%BF%E5%BE%92%E7%B3%BB%E5%88%97-8665",
    "https://bannergress.com/banner/ingressss-csx-ed79",
    "https://bannergress.com/banner/csx-cutebunny-0753",
    "https://bannergress.com/banner/%E9%BA%93%E5%B1%B1%E9%87%91%E7%A7%8B-1609",
    "https://bannergress.com/banner/%E6%9D%9C%E7%94%AB-5e0c",
    "https://bannergress.com/banner/%E6%A9%98%E5%AD%90%E6%B4%B2%E5%A4%B4-fdfd",
    "https://bannergress.com/banner/%E6%B9%96%E5%A4%A7%E6%A0%A1%E5%BE%BD-e914",
    "https://bannergress.com/banner/%E9%95%BF%E6%B2%99%E7%90%86%E5%B7%A5%E5%A4%A7%E5%AD%A6%E6%A0%A1%E8%AE%AD-5bf7",
    "https://bannergress.com/banner/%E9%95%BF%E6%B2%99%E5%AD%A6%E9%99%A2-%E5%8E%9F%E9%95%BF%E6%B2%99%E5%A4%A7%E5%AD%A6-%E6%AF%95%E4%B8%9A%E7%BA%AA%E5%BF%B5-6342",
    "https://bannergress.com/banner/exploring-the-beauty-of-csust-1fc4",
    "https://bannergress.com/banner/%E6%B9%96%E5%8D%97%E5%95%86%E5%AD%A6%E9%99%A2%E5%A4%9C%E6%99%AF-4d2e",
    "https://bannergress.com/banner/%E9%B9%BF%E6%9E%97%E4%B9%8B%E6%A3%AE-0693",
    "https://bannergress.com/banner/%E6%98%9F%E5%9F%8E%E9%95%BF%E6%B2%99-efd9",
    "https://bannergress.com/banner/%E8%BF%99%E4%B8%80%E4%B8%96%E6%9C%89%E5%96%B5%E6%98%9F%E4%BA%BA%E5%92%8C%E7%8C%AB%E5%A5%B4-82d7",
    "https://bannergress.com/banner/%E6%B9%98%E6%B1%9F%E6%B1%9F%E6%99%AF-c03e",
    "https://bannergress.com/banner/%E6%A9%98%E6%B4%B2%E7%84%B0%E7%81%AB-a697",
    "https://bannergress.com/banner/%E7%AC%A8%E6%9F%B4%E5%85%84%E5%BC%9F-cd7f",
    "https://bannergress.com/banner/%E5%BF%8D%E5%88%AB%E7%A6%BB-525f",
    "https://bannergress.com/banner/my-rock-list-3292",
    "https://bannergress.com/banner/%E8%B4%BA%E9%BE%99%E4%BD%93%E8%82%B2%E5%9C%BA-f5aa",
    "https://bannergress.com/banner/%E5%B2%B3%E9%BA%93%E5%B1%B1-8912",
    "https://bannergress.com/banner/%E5%A4%A9%E5%BF%83%E9%98%81-0ac7",
    "https://bannergress.com/banner/%E6%B5%A3%E6%BA%AA%E6%B2%99-f545",
    "https://bannergress.com/banner/%E5%8D%B0%E8%B1%A1%E6%B5%8F%E9%98%B3-3a77",
    "https://bannergress.com/banner/%E6%98%9F%E5%9F%8E%E9%95%BF%E6%B2%99-e054",
    "https://bannergress.com/banner/%E9%95%BF%E6%B2%99%E5%A4%A9%E9%99%85%E7%BA%BF-68c3",
    "https://bannergress.com/banner/i-love-changsha-1c9b",
    "https://bannergress.com/banner/ingressfs-changsha-prime%E7%89%881-0-dc0f",
    "https://bannergress.com/banner/ingressfs-%E5%85%AD%E4%B8%80%E6%9D%A5%E9%95%BF%E6%B2%99-1c99",
    "https://bannergress.com/banner/%E9%95%BF%E6%B2%99%E7%BD%91%E7%BA%A2%E6%89%93%E5%8D%A1%E5%A2%99-95f5",
    "https://bannergress.com/banner/%E9%95%BF%E6%B2%99%E7%B2%BE%E7%A5%9E-%E4%B9%B1%E6%90%9E%E7%89%88-8e80",
    "https://bannergress.com/banner/%E9%95%BF%E6%B2%99%E7%BE%8E%E9%A3%9F-4376",
    "https://bannergress.com/banner/%E9%95%BF%E6%B2%99%E5%9C%B0%E9%93%81%E4%B8%80%E5%8F%B7%E7%BA%BF-686b",
    "https://bannergress.com/banner/%E9%95%BF%E6%B2%99%E5%9C%B0%E9%93%81%E4%BA%8C%E5%8F%B7%E7%BA%BF-5f62",
    "https://bannergress.com/banner/%E9%95%BF%E6%B2%99%E5%9C%B0%E9%93%81%E4%B8%89%E5%8F%B7%E7%BA%BF-82ec",
    "https://bannergress.com/banner/%E9%95%BF%E6%B2%99%E5%9C%B0%E9%93%81%E5%9B%9B%E5%8F%B7%E7%BA%BF-f604",
    "https://bannergress.com/banner/%E9%95%BF%E6%B2%99%E5%9C%B0%E9%93%81%E4%BA%94%E5%8F%B7%E7%BA%BF-194d",
    "https://bannergress.com/banner/%E9%95%BF%E6%B2%99%E5%9C%B0%E9%93%81%E5%85%AD%E5%8F%B7%E7%BA%BF-4bdd",
    "https://bannergress.com/banner/%E6%8E%92%E6%8E%92%E5%9D%90%E5%90%83%E6%9E%9C%E6%9E%9C-22f8",
    "https://bannergress.com/banner/%E8%B8%8F%E6%98%A5-a4eb",
    "https://bannergress.com/banner/csx-happy-mice-1b9e",
    "https://bannergress.com/banner/%E6%99%82%E9%9B%A8%E3%83%8E%E6%97%85%E8%B7%AFvol-1-82fc",
    "https://bannergress.com/banner/%E5%A4%8F%E7%9B%AE-b193",
    "https://bannergress.com/banner/%E6%B9%96%E5%8D%97%E5%86%9C%E5%A4%A7%E4%B9%8B%E6%98%A5-%E6%A8%B1-63a1",
    "https://bannergress.com/banner/%E4%B9%A1%E9%87%8C%E5%88%AB%E6%83%B3%E8%BF%9B%E5%9F%8E-2197",
    "https://bannergress.com/banner/%E7%8C%AB%E5%92%8C%E7%8C%AB-d242",
    "https://bannergress.com/banner/%E6%B1%89%E4%BB%A3%E7%93%A6%E5%BD%93-bdf2",
    "https://bannergress.com/banner/%E8%BF%99%E6%98%AF%E5%AE%A2%E6%A0%88%E5%91%80-0dd1",
    "https://bannergress.com/banner/%E5%B7%AE%E4%B8%8D%E5%A4%9A%E6%98%AF%E6%9D%A1%E5%BA%9F%E5%92%B8%E9%B1%BC%E4%BA%86-7493",
    "https://bannergress.com/banner/%E5%8D%83%E5%B9%B4%E5%AD%A6%E5%BA%9C-dffa",
    "https://bannergress.com/banner/%E6%82%A0%E5%93%89%E6%82%A0%E5%93%89%E5%85%AC%E5%9B%AD%E7%B3%BB%E5%88%97-239f",
    "https://bannergress.com/banner/%E5%86%B0%E4%B8%8E%E7%81%AB%E4%B9%8B%E6%AD%8C%E5%AE%B6%E6%97%8F%E5%8A%A8%E7%89%A9-94d1",
    "https://bannergress.com/banner/%E5%85%A8%E6%98%AF%E5%A4%B4%E5%A4%B4%E5%A4%B4-2297",
    "https://bannergress.com/banner/%E6%9D%A5%E5%88%B0%E4%B8%AD%E5%8D%97%E5%A4%A7%E5%AD%A6-%E5%AE%9E%E7%8E%B0%E4%BA%BA%E7%94%9F%E7%90%86%E6%83%B3-9b70",
    "https://bannergress.com/banner/inside-the-lanxiu-city-3b52",
    "https://bannergress.com/banner/%E6%B9%96%E5%8D%97%E5%86%9C%E4%B8%9A%E5%A4%A7%E5%AD%A6%E6%A0%A1%E5%BE%BD-2701",
    "https://bannergress.com/banner/%E8%8D%8F%E8%8B%92%E5%86%AC%E6%98%A5%E5%8E%BB-9b6b"

]

test_all_url = [
    "https://bannergress.com/banner/%E6%A9%98%E7%8C%AB%E7%8C%AB%E6%97%A5%E4%B9%9F%E6%83%B3%E5%96%9D%E8%8C%B6%E9%A2%9C-5bd6",
    "https://bannergress.com/banner/csx-%E5%B8%86%E8%88%B9%E8%BF%90%E5%8A%A8-62bc",
    "https://bannergress.com/banner/eva%E4%BD%BF%E5%BE%92%E7%B3%BB%E5%88%97-8665",
    "https://bannergress.com/banner/ingressss-csx-ed79"
]

def request_html_text(url):
    response = requests.get(url, headers = headers)
    response.encoding = 'utf-8-sig'
    #print(response.status_code)
    return response.text

def title_and_imgurl(html_text):
    title_patten = "(?<=\"og:title\" content=\")([^<]*)(?=\">)"
    title = re.search(title_patten, html_text)
    t_title = ''
    if title:
        #print(title.group())
        t_title = title.group()

    image_patten = "(?<=\"og:image\" content=\")([^<]*)(?=\">)"
    img_url = re.search(image_patten, html_text)
    t_img_url = ''
    if img_url:
        #print(img_url.group())
        t_img_url = img_url.group()
    return t_title, t_img_url

def hacks_and_time(html_text):
    return '', ''

def get_title_and_imgurl(url):
    html_text = request_html_text(url)
    return title_and_imgurl(html_text)

def blog_context(start):
    start -= 1
    index = start + 1
    blog = ""
    for url in all_url[start:]:
        title,img_url = get_title_and_imgurl(url)
        title,img_url = get_title_and_imgurl(url)
        block = ""
        block += f'### {index}.{title}\n'
        block += '---\n'
        block += f'![{title}]({img_url})\n'
        block += f'[🚪Bannergress传送门]({url})\n'
        blog += block
        index += 1
    print(blog)

def tg_context(start):
    start -= 1
    index = start + 1
    messages = ""
    for url in all_url[start:]:
        html_text = request_html_text(url)
        title,img_url = title_and_imgurl(html_text)
        hacks,mission_time = hacks_and_time(html_text)
        block = ""
        block += f'{index}.{title}\n\n'
        block += "【位置】\n\n"
        block += "【路线】\n\n"
        block += f'【Actions】{hacks}\n\n'
        block += f'【任务用时】{mission_time}\n\n'
        block += f'【[Bannergress]({url})】\n\n'
        block += "【标签】\n\n"
        block += "\n\n\n"
        messages += block
        index += 1
    print(messages)
    
if __name__ == "__main__":
    #tg_context(56)
    blog_context(56)