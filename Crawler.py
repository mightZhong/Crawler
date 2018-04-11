import requests
import json
import time
import datetime

url_load = 'https://be02.bihu.com/bihube-pc/api/user/loginViaPassword'
headers_load = {
	'Accept': '*/*',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'zh-CN,zh;q=0.9',
	'Connection': 'keep-alive',
	'Content-Length': '91',
	'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
	'Host': 'be02.bihu.com',
	'Origin': 'https://bihu.com',
	'Referer': 'https://bihu.com/login',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
}

headers_follow = {
	'Accept': '*/*',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'zh-CN,zh;q=0.9',
	'Connection': 'keep-alive',
	'Content-Length': '57',
	'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
	'Host': 'be02.bihu.com',
	'Origin': 'https://bihu.com',
	'Referer': 'https://bihu.com/?category=follow',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
}

headers_vote = {
	'Accept': '*/*',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
	'Connection': 'keep-alive',
	'Content-Length': '70',
	'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
	'Host': 'be02.bihu.com',
	'Origin': 'https://bihu.com',
	'Referer': 'https://bihu.com/article/',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
}


class Crawler(object):
	def __init__(self, user, latest_time):
		self.user = user
		self.latest_time = latest_time

	def login(self):
		try:
			self.session = requests.session()
			content = self.session.post(url_load, headers = headers_load, data = self.user)
			print content
			if content.cookies.get_dict():
				self.session.cookies.update(content.cookies)

			res = json.loads(content.content)
			self.userId = res[ 'data' ][ 'userId' ]
			self.accessToken = res[ "data" ][ "accessToken" ]
			return True
		except Exception, e:
			print e

	def get_latest_article(self):
		follow_data = {
			'userId': self.userId,
			'accessToken': self.accessToken
		}

		content = self.session.post("https://be02.bihu.com/bihube-pc/api/content/show/getFollowArtList", headers = headers_follow, data = follow_data)
		if content.cookies.get_dict():
			self.session.cookies.update(content.cookies)

		data = json.loads(content.content)
		#print data
		artList = data['data']['artList']['list']
		for art in artList:
			#print art
			createTime = art['createTime']
			#print type(createTime)
			#print createTime
			#print '***************** %d' % createTime/1000

			createTime = createTime/1000
			#print createTime

			timestamp = time.time()
			#rint timestamp
			timestruct = time.localtime(timestamp)
			#print time.strftime('%Y-%m-%d %H:%M:%S', timestruct)
			now = datetime.datetime.fromtimestamp(timestamp)	

			timestruct = time.localtime(createTime)
			#print time.strftime('%Y-%m-%d %H:%M:%S', timestruct)
			artTime = datetime.datetime.fromtimestamp(createTime)
			#print (now - artTime).days
			sec = (now - artTime).seconds
			#print sec

			if sec < self.latest_time:
				print '--------->Find a new artcle!'
				self.artId = str(art['id'])
				print 'artcle id is ' + self.artId
				#download_artcle(id)
				return True

			return False



	def vote_article(self):
		headers_vote['Referer'] = headers_vote['Referer']+self.artId
		#print headers_vote
		#content = session.get(url)
		#print content.text
		vote_data = {
		'userId': self.userId,
		'accessToken': self.accessToken,
		'artId': self.artId
		}

		url = 'https://be02.bihu.com/bihube-pc/api/content/upVote'
		#print vote_data

		content = self.session.post(url, headers = headers_vote, data = vote_data)
		if content.cookies.get_dict():
			self.session.cookies.update(content.cookies)
		print 'vote result ' + content.content
		return True



def auto_vote(user):
	'''
	url_load = 'https://be02.bihu.com/bihube-pc/api/user/loginViaPassword'
	headers_base = {
		'Accept': '*/*',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'zh-CN,zh;q=0.9',
		'Connection': 'keep-alive',
		'Content-Length': '91',
		'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
		'Host': 'be02.bihu.com',
		'Origin': 'https://bihu.com',
		'Referer': 'https://bihu.com/login',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
	}

	headers_follow = {
		'Accept': '*/*',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'zh-CN,zh;q=0.9',
		'Connection': 'keep-alive',
		'Content-Length': '57',
		'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
		'Host': 'be02.bihu.com',
		'Origin': 'https://bihu.com',
		'Referer': 'https://bihu.com/?category=follow',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
	}

	headers_vote = {
	'Accept': '*/*',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
	'Connection': 'keep-alive',
	'Content-Length': '70',
	'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
	'Host': 'be02.bihu.com',
	'Origin': 'https://bihu.com',
	'Referer': 'https://bihu.com/article/',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
	}
	'''
	'''
	login_data = {
		'phone': '13735894914',
		'password': 'f2e2a792861b4ded509bee1953545a60191d6c8f13a20b416395997f9d9bc2bb'
	}
	'''
	
	session = requests.session()

	content = session.post(url_load, headers = headers_load, data = user)
	
	
	if content.cookies.get_dict():
		session.cookies.update(content.cookies)
	#print content
	#print content.content	
	'''
	f = open("/Users/might/Documents/bihu.html", 'w')
	f.write(content.content)
	f.close()
	'''
	#print content.content
	#print content.json()
	#print (content.text)['data']
	#print isinstance(content.text, dict)
	#print isinstance(content.text, str)
	#its = cons
	
	res = json.loads(content.content)
	userId = res[ 'data' ][ 'userId' ]
	accessToken = res[ "data" ][ "accessToken" ]
	
	#print "userId " + userId + " accessToken " + accessToken
	#print "**********1************"
	follow_data = {
		'userId': userId,
		'accessToken': accessToken
	}
	#s = session.post("https://be02.bihu.com/bihube-pc/api/content/show/getFollowArtList", headers = headers_follow, verify=True)
	#s = session.post("https://be02.bihu.com/bihube-pc/api/content/show/getFollowArtList", verify=True)
	content = session.post("https://be02.bihu.com/bihube-pc/api/content/show/getFollowArtList", headers = headers_follow, data = follow_data)
	if content.cookies.get_dict():
		session.cookies.update(content.cookies)
	#print s.text
	#print s.content
	#print s
	data = json.loads(content.content)
	#print data
	artList = data['data']['artList']['list']
	for art in artList:
		#print art
		createTime = art['createTime']
		#print type(createTime)
		#print createTime
		#print '***************** %d' % createTime/1000

		createTime = createTime/1000
		#print createTime

		timestamp = time.time()
		#rint timestamp
		timestruct = time.localtime(timestamp)
		#print time.strftime('%Y-%m-%d %H:%M:%S', timestruct)
		now = datetime.datetime.fromtimestamp(timestamp)	

		timestruct = time.localtime(createTime)
		#print time.strftime('%Y-%m-%d %H:%M:%S', timestruct)
		artTime = datetime.datetime.fromtimestamp(createTime)
		#print (now - artTime).days
		sec = (now - artTime).seconds
		#print sec

		if sec < 30*60:
			print '--------->Find a new artcle!'
			artId = str(art['id'])
			print 'artcle id is ' + artId
			#download_artcle(id)

			headers_vote['Referer'] = headers_vote['Referer']+artId
			#print headers_vote
			#content = session.get(url)
			#print content.text
			vote_data = {
			'userId': userId,
			'accessToken': accessToken,
			'artId': artId
			}

			#vote
			url = 'https://be02.bihu.com/bihube-pc/api/content/upVote'
			#print vote_data
			content = session.post(url, headers = headers_vote, data = vote_data)
			if content.cookies.get_dict():
				session.cookies.update(content.cookies)
			print 'vote result ' + content.content
			'''
			# give comment
			url = 'https://be02.bihu.com/bihube-pc/api/content/createCommen'
			headers_comment = headers_vote
			headers_comment['Content-Length'] = '108'
			print headers_comment
			comment_data = vote_data
			comment_data['content'] = 'thanks~'
			comment_data['commentId'] = ''
			comment_data['rootCmtId'] = ''
			print comment_data
			content = session.post(url, headers = headers_comment, data = comment_data)
			print content
			'''
		break

'''
	f = open("/Users/might/Documents/bihu.html", 'w')
	f.write(s.content)
	f.close()
'''
	#print content.text		



def main():
	#st = time.localtime(1522034538000)
	#print time.strftime('%Y-%m-%d %H:%M:%S', st)
	#print time.time()
	'''
	timestamp = time.time()
	print timestamp
	timestruct = time.localtime(timestamp)
	print time.strftime('%Y-%m-%d %H:%M:%S', timestruct)
	timea = datetime.datetime.fromtimestamp(timestamp)
	print '1522235518'
	timestamp = 1522235518
	timestruct = time.localtime(timestamp)
	print time.strftime('%Y-%m-%d %H:%M:%S', timestruct)
	timeb = datetime.datetime.fromtimestamp(timestamp)
	print (timea - timeb).days
	sec = (timea - timeb).seconds
	print sec/3600
	'''
	#timestamp = 1522034538000
	#datetime_struct = datetime.datetime.fromtimestamp(timestamp)
	#print datetime_struct.strftime('%Y-%m-%d %H:%M:%S')
	#datetime_struct = datetime.datetime.utcfromtimestamp(timestamp)
	#print datetime_struct.strftime('%Y-%m-%d %H:%M:%S')
	#return 0
	users =[
		{
			'phone': '13735894914',
			'password': 'f2e2a792861b4ded509bee1953545a60191d6c8f13a20b416395997f9d9bc2bb'
		},
		{
			'phone': '13675877696',
			'password': 'f2e2a792861b4ded509bee1953545a60191d6c8f13a20b416395997f9d9bc2bb'
		}
	]
	'''
	session = requests.session()
	content = session.post(url_load, headers = headers_load, data = users[0])
	if content.cookies.get_dict():
		print content.cookies
		session.cookies.update(content.cookies)
	print content
	res = json.loads(content.content)
	userId = res[ 'data' ][ 'userId' ]
	accessToken = res[ "data" ][ "accessToken" ]
	'''

	'''
	count = 0
	while True:
		#for user in users:
		count = count+1

		for user in users:
			time.sleep(10)
			print "user %s flush %d time" % (user['phone'], count)
			try:
				auto_vote(user)
			except Exception as e:
				print e
	'''

	crawlers = []
	latest_time = 70  #s
	for user in users:
		crawler = Crawler(user, latest_time)
		crawlers.append(crawler)
		if crawler.login():
			print "user %s login success" % user['phone']
		else:
			print "user %s login failed" % user['phone']


	while True:
		for crawler in crawlers:
			timestamp = time.time()
			timestruct = time.localtime(timestamp)
			print time.strftime('%Y-%m-%d %H:%M:%S', timestruct)+" user %s flush" % crawler.user['phone']
			try:
				if crawler.get_latest_article():
					if crawler.vote_article():
						print "user %s vote success" % crawler.user['phone']
			except Exception, e:
				print e
				if crawler.login():
					print "user %s relogin success" % user['phone']
				else:
					print "user %s relogin failed" % user['phone']
			time.sleep(30)

if __name__ == '__main__':
	main()