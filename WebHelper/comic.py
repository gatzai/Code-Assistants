#爬取某色图网站的色图，每一卷按文件分开
from requests_html import HTMLSession
import re
import json
import time
import os
#time.sleep(1)

comic_path = "./comics/"
catalog = {}

#代理
proxies = {
	'http':'http://127.0.0.1:7890',
	'https':'http://127.0.0.1:7890'
}
target_url = "https://www.ho5ho.com/"

#模拟成浏览器
headers = {
	"User=Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
}


def xpath_comic_name():
	return '//div[@class="post-title font-title"]//a/text()'

def xpath_comic_cover():
	return '//div[@class="page-item-detail manga"]//img/@data-src'

def xpath_comic_link():
	return '//div[@class="page-item-detail manga"]/div/a/@href'

def xpath_chapter_link():
	return '//li[@class="wp-manga-chapter"]//a/@href'

def xpath_chapter_name():
	return '//li[@class="wp-manga-chapter"]//a/text()'

def get_outside_page_tail(page):
	return 'page/'+str(page)

#test for 403 image
def deal403(imgurl,pageurl):
	ref_headers = headers
	ref_headers["Referer"] = pageurl
	session.headers=headers
	img_res = session.get(imgurl, proxies=proxies)
	#print(res.status_code)
	return img_res

def check_path(path):
	if os.path.exists(path):
		return True
	else:
		os.makedirs(path)
		return False

def vertify_name(name):
	name = re.sub(r'[\\\/\<|\>|?|:|*|\||"]','',name)
	return name

def load_data():
	global catalog
	with open('./content.json','r',encoding='utf8')as fp:
	    catalog = json.load(fp)

def save_data():
	global catalog
	result_json = json.dumps(catalog)
	with open("content.json",'w',encoding="utf-8") as f:
		f.write(result_json)

def set_visited(key):
	global catalog
	if key in catalog:
		print("existed: ",key)
	else:
		print("add:",key)
		catalog[key] = {}
	save_data()

def is_visit(key):
	global catalog
	if key in catalog:
		print("existed: ",key)
		return True
	return False

def record_new_comic(comic_name,chapter_name):
	global catalog
	if comic_name not in catalog:
		catalog[comic_name] = {}
	catalog[comic_name][chapter_name] = {}
	catalog[comic_name][chapter_name]['finished'] = 0
	catalog[comic_name][chapter_name]['page'] = 0
	catalog[comic_name][chapter_name]['error'] = 0

def match_img_urls(text):
	reg = 'var chapter_preloaded_images =.*?;'
	pattern = re.compile(reg, re.S)
	reg_find = re.findall(pattern,text)
	if not reg_find:
		return []
	img_url_text = reg_find[0]
	img_url_text = img_url_text.replace('\\','')
	reg2 = '".*?"'
	pattern2 = re.compile(reg2, re.S)
	result = re.findall(pattern2,img_url_text)
	#print(len(result))
	img_urls = []
	for imgurl in result:
		url = imgurl.replace('"','')
		img_urls.append(url)
	return img_urls

def save_comic(path, chapter_name, comic_name, url):
	global catalog
	res = session.get(url, headers=headers, proxies=proxies)
	#res.html.render()
	img_urls = match_img_urls(res.text)
	if not img_urls:
		return
	comic_pages = len(img_urls)

	print("pages:",comic_pages)
	index = 0
	#print("test:",catalog)
	#查看是否已经记录了
	if chapter_name not in catalog[comic_name]:
		#如果没有记录，那么就构造一个记录
		#print("not ",comic_name + '-' + chapter_name)
		record_new_comic(comic_name, chapter_name)
		check_path(path)
		save_data()
	else:
		#若已经记录了，查看是否载入完毕
		current_page = catalog[comic_name][chapter_name]['page']
		if catalog[comic_name][chapter_name]['finished'] == 1 and current_page >= comic_pages:
			print('complete: ', comic_name)
			return
		else:
			#如果没有载入完毕，就从 current_page 开始
			index = current_page
			img_urls = img_urls[current_page:]

	for link in img_urls:
		time.sleep(1)
		load_data()
		#img_res = deal403(link, url)
		ref_headers = headers
		ref_headers["Referer"] = url.encode("utf-8").decode("latin1")
		session.headers=headers
		try:
			img_res = session.get(link, proxies=proxies)
			file_path = path + '/' + str(index) + '.jpg'
			with open(file_path,'wb') as f:
				f.write(img_res.content)
		except:
			print("[Except]no image:",index)
			#只要本章存在找不到的图片就立刻退出本章，finish为1，page为图片连接失效页面, [error]=1
			catalog[comic_name][chapter_name]['error'] = 1
			catalog[comic_name][chapter_name]['page'] = index
			save_data()
			break
		index = index + 1
		catalog[comic_name][chapter_name]['page'] = index
		save_data()
	catalog[comic_name][chapter_name]['finished'] = 1
	save_data()

def choose_chapter(url, comic_name):
	res = session.get(url, headers=headers, proxies=proxies)
	#print(url)
	chapters_url = res.html.xpath(xpath_chapter_link())
	chapters_name = res.html.xpath(xpath_chapter_name())
	index = -1
	for chapter_url in chapters_url:
		index = index + 1
		c_name = chapters_name[index].strip()
		path = comic_path + comic_name + '/' + c_name
		print("chapter:",c_name)
		save_comic(path, c_name, comic_name, chapter_url)

def travel_page(pageurl):
	res = session.get(pageurl, headers=headers, proxies=proxies)
	comic_name = res.html.xpath(xpath_comic_name())
	comic_cover = res.html.xpath(xpath_comic_cover())
	comic_link = res.html.xpath(xpath_comic_link())
	index = -1
	for name in comic_name:
		index = index + 1
		name = vertify_name(name)
		if not is_visit(name):
			#如果没有记录，就先创个文件夹，然后整个封面图
			path = comic_path + name + '/'
			if not os.path.exists(path):
				check_path(path)
			else:
				print(path, "[Warning][Data not match] already existed!") #有目录，但没记录
				#continue #todo先注释掉, 测过没问题，数据不匹配时会重新写数据的
			time.sleep(1)
			img_cover = session.get(comic_cover[index], headers=headers, proxies=proxies)
			cover_path = path + '0.jpg'
			with open(cover_path,'wb') as f:
				f.write(img_cover.content)
			set_visited(name)
		#接下来就是获取漫画了,经过一个中间页,选择章节
		choose_chapter(comic_link[index], name)

	print(index+1)

#scan all page
def scan_all(from_page=0,to_page=1):
	for i in range(from_page,to_page+1):
		pageurl = target_url + get_outside_page_tail(i+1)
		print("--------At page:",i)
		travel_page(pageurl)

#只扫描第一页，相当于更新了
def update_comic():
	pageurl = target_url + get_outside_page_tail(1)
	travel_page(pageurl)

def main():
	print('start')
	check_path(comic_path)
	global session
	load_data()

	session = HTMLSession()
	session.trust_env = False
	#res = session.get(target_url, headers=headers, proxies=proxies)
	#res.encoding = "utf-8"
	#print(res.status_code)
	scan_all(43,61)

if __name__=='__main__':
	main()


#图片一般都是动态加载的，静态爬取是无法获取的
#查看页面源码: view-source:http...
#参考：https://blog.csdn.net/weixin_39911056/article/details/110705901

#爬取图片还会遇到403问题, 修改一下header的referer就行