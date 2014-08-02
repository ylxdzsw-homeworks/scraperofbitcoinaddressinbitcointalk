import scrapy
import json
import re
import time
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

bitcoinpattern = re.compile(r'(1[1-9A-HJ-NP-Za-km-z]{26,33})')

class scraperofbitcoinaddressinbitcointalk(CrawlSpider):
	name = 'scraperofbitcoinaddressinbitcointalk'
	allowed_domains = ['bitcointalk.org']
	start_urls = [
		'https://bitcointalk.org/index.php?topic=655359.0',
		'https://bitcointalk.org/index.php?topic=20333.0',
		'https://bitcointalk.org/index.php?topic=720871.0'
	]

	rules = (
		Rule(LinkExtractor(allow=('board', ))),
		Rule(LinkExtractor(allow=('topic', )),callback='zparse')
	)

	items = {}

	def zparse(self,response):
		a = response.css('.signature')
		for i in a:
			try:
				istr = reduce(lambda a,b : a+' '+b ,i.xpath('text()|./*/text()').extract())
				mat = bitcoinpattern.search(istr)
				if mat:
					username = i.xpath('../../../tr[1]/td[1]/b/a/text()').extract()[0]
					for j in mat.groups():
						if j not in self.items.get(username,[]):
							self.items[username] = self.items.get(username,[]) + [j]
			except Exception, e:
				print e
			time.sleep(0.01)

	def closed(self,reason):
		with open('output.json','wb') as f:
			f.write(json.dumps(self.items))





