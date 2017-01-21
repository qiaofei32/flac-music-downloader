#encoding=utf8
import os
import re
import sys
import web
import music_downloader

urls = (
	'/(.*)', 'Index',
	'/(.*)/(css|img|js)/(.*)', 'Static',
	'/(css|img|js)/(.*)', 'Static',
)

def notfound():
	return web.notfound("Sorry, the page you were looking for was not found.")

class Static:
	def GET(self, *args):
		dir, name = args[-2:]
		dir_path = 'templates/%s/' %dir
		ext = name.split(".")[-1]
		cType = {
			"css": "text/css",
			"png": "images/png",
			"jpg": "images/jpeg",
			"gif": "images/gif",
			"ico": "images/x-icon",
			"js" : "text/javascrip",
		}
		if name in os.listdir(dir_path):
			web.header("Content-Type", cType[ext])
			file_path = '%s/%s' %(dir_path, name)
			return open(file_path, "rb").read()
		else:
			raise web.notfound()

class Index:
	def GET(self, _):
		params = web.input()
		# web.debug(params)
		try:
			source = params.source.encode("utf8")
			keyword = params.keyword.encode("utf8")
			song_list = music_downloader.get_search_list(keyword=keyword, source=source, max_page=2)
			song_list = [song for song in song_list if (len(song["SongName"]) <= 10 and u"、" not in song["Artist"])]
			return render.index(song_list)
		except:
			return render.index([])

app = web.application(urls, globals())
render = web.template.render('templates/')
app.notfound = notfound

if __name__ == '__main__':
	app.run()