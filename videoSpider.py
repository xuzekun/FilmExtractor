# -*- coding:utf-8 -*-
import requests
from lxml import html  
import json
import logging

class VideoSpider():
	#@staticmethod
	def initParamsFromFile(self, fileName):
		with open(fileName) as json_file:
			self.params = json.load(json_file)

	def initParansFromJsonData(self, json_data):
		logging.info("video json data:" + json_data)
		self.params = json.loads(json_data)

	def getPage(self, url):
		headers = {
			'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.4.4; Nexus 5 Build/KTU84P) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Encoding':'gzip, deflate, sdch',
			'Accept-Language':'zh-CN,zh;q=0.8,ja;q=0.6,en;q=0.4'	
		}

		response = requests.get(url, headers=headers)
		#非200返回空
		if response.status_code != 200:
			return ""
		if "encoding" in self.params.keys() and self.params["encoding"] != "":
			#print self.params["encoding"]
			response.encoding = self.params["encoding"]
			
			return response.text 
		else:
			return response.content

	def getMainPageInfo(self, data):
		logging.info("entering getMainPagInfo")
		tree = html.fromstring(data)
		try:
			titles = tree.xpath(self.params['getInfo']['title'])
		except:
			return "Invalid expression title"

		try:
			hrefs = tree.xpath(self.params['getInfo']['href'])
		except:
			return "Invalid expression href"

		try:
			coverUrls = tree.xpath(self.params['getInfo']['coverUrl'])
		except:
			return "Invalid expression coverUrl"

		if len(titles) == 0:
			logging.info("title xpath error")
			return "title xpath err"
		if len(hrefs) == 0:
			logging.info("href xpath error")
			return "hrefs xpath err"
		if len(coverUrls) == 0:
			logging.info("coverUrl xpath error")
			return "coverUrl xpath err"

		output = []
		for i in range(0, len(titles)):
			item = {}
			item['title'] = titles[i]
			item['cover_url'] = coverUrls[i]
			if self.params['getInfo']['showType'] != "":
				item['show_type'] = self.params['getInfo']['showType']

			if self.params['getInfo']['prefix_url'] != "":
				item['url'] = self.params['getInfo']['prefix_url'] + hrefs[i]
			else:
				item['url'] = hrefs[i]

			output.append(item)

		output_json = json.dumps(output, ensure_ascii=False, indent=4)
		
		return output_json


	def getDetailPageInfo(self, urls):
		logging.info("entering getDetailPageInfo")
		output = []
		for url in urls:
			data = self.getPage(url)
			if data == "":
					return u'子页面访问失败，请检查url:' + url

			tree = html.fromstring(data)
			try:
				title = tree.xpath(self.params['getLink']['title'])
			except:
				return "Invalid expression title"

			try:
				coverUrl = tree.xpath(self.params['getLink']['coverUrl'])
			except:
				return "Invalid expression coverUrl"

			if len(title) == 0:
				logging.info("title xpath err")
				return "title xpath err"
			if len(coverUrl) == 0:
				logging.info("coverUrl xpath err")
				return "coverUrl xpath err"

			item = {}
			item['title'] = title[0]
			item['cover_url'] = coverUrl[0]
			item['url'] = url
			if self.params['getLink']['showType'] != "":
				item['show_type'] = self.params['getLink']['showType']

			output.append(item)
			print item
		output_json = json.dumps(output, ensure_ascii=False, indent=4)
		return output_json			
				
	# 获取二级链接
	def getLinks(self, data):
		tree = html.fromstring(data)
		try:
			hrefs = tree.xpath(self.params['getLink']['href'])
		except: 
			return  "Invalid expression href"

		if len(hrefs) == 0:
			logging.info("href xpath err")
			return "href xpath err"

		urls = []
		for i in range(0, len(hrefs)):
			if self.params['getLink']['prefix_url'] != "":
				url = self.params['getLink']['prefix_url'] + hrefs[i]
			else:
				url = hrefs[i]
			urls.append(url)

		return urls

	# 有图页面
	def getPicInfo(self, json_data):
		self.initParansFromJsonData(json_data)
		mainPage = self.getPage(self.params['url'])
		if mainPage == "":
			return u'主页访问失败，请检查url:' + self.params['url']
		outputData = self.getMainPageInfo(mainPage)
		return outputData

	# 无图页面
	def getNoPicInfo(self, json_data):
		self.initParansFromJsonData(json_data)
		mainPage = self.getPage(self.params['url'])
		if mainPage == "":
			return u'主页访问失败，请检查url:' + self.params['url']
		urls = self.getLinks(mainPage)
		if type(urls) is not type(list()):
			return urls
		outputData = self.getDetailPageInfo(urls)
		return outputData


if __name__ == '__main__':
	spider = VideoSpider()
	spider.initParamsFromFile('wobuka.json')
	data = spider.getPage(spider.params["url"])
	spider.getMainPagInfo(data)
	#spider.getLinks(data)