#encoding=utf8
import os
import sys
import json
import requests
import urllib

DATA_SOURCE ={
	"网易云"  : "wy",
	"天天动听": "tt",
	"酷狗音乐": "kg",
	"酷我音乐": "kw",
	"QQ音乐"  : "qq",
	"虾米音乐": "xm",
	"百度音乐": "bd",
	"电信音乐": "dx",
}

global INDEX
INDEX = 1

def get_search_list(keyword, source="酷我音乐", max_page=1):
	sign = "a5cc0a8797539d3a1a4f7aeca5b695b9"
	source = DATA_SOURCE[source]
	keyword = urllib.quote(keyword)
	song_list = []
	for page in range(1, max_page+1):
		url = "http://api.itwusun.com/music/search/%s/%d?format=json&sign=%s&keyword=%s" %(source, page, sign, keyword)
		# print url
		data = requests.get(url).content
		if not data:
			break
		song_list += json.loads(data)
	# print song_list
	return song_list

def donwload_song(song_url, file_name, retry=3):
	try:
		urllib.urlretrieve(song_url, file_name)
	except KeyboardInterrupt:
		print "KeyboardInterrupt"
		sys.exit(1)
	except Exception as e:
		print e
		if retry > 0:
			return donwload_song(song_url, file_name, retry=retry-1)
		else:
			return False
		
def download_list(song_list):
	global INDEX
	for song in song_list:
		AlbumArtist = song["AlbumArtist"]
		Artist = song["Artist"]
		SongName = song["SongName"]
		SongName = SongName.split(u"-")[0]
		SongName = SongName.split(u"(")[0]
		SongName = SongName.split(u"（")[0]
		SongName = SongName.strip()
		
		qualitys = ["FlacUrl", "HqUrl", "SqUrl", "CopyUrl", "LqUrl", "ListenUrl"]
		"""
		ListenUrl=http://api.itwusun.com/music/songurl/kw_320_3565336.mp3?sign=44b6f88d120d99b8408aa4eb59ecf756
		LqUrl=http://api.itwusun.com/music/songurl/kw_128_3565336.mp3?sign=3934b789c9823fb4fff44b0c5250d8a4
		SqUrl=http://api.itwusun.com/music/songurl/kw_320_3565336.mp3?sign=44b6f88d120d99b8408aa4eb59ecf756
		CopyUrl=http://api.itwusun.com/music/songurl/kw_128_4342213.mp3?sign=898494237d87678f3bfec51d71ca8741
		HqUrl=http://api.itwusun.com/music/songurl/kw_192_3559894.mp3?sign=49160f6037178daae33197b17f3a1cb5
		"""
		song_url = ""
		for quality in qualitys:
			song_url = song.get(quality, "").encode("gbk", "ignore")
			if song_url:
				# print quality, song_url
				break
		
		file_name = "Songs/%s-%s.mp3" %(Artist, SongName)
		file_name = file_name.encode("gbk", "ignore")
		if os.path.exists(file_name):
			continue
		print "%d.%s %s" %(INDEX, file_name, song_url)
		donwload_song(song_url, file_name)
		INDEX += 1

if __name__ == "__main__":
	if len(sys.argv) == 3:
		keyword = sys.argv[1]
		max_page = int(sys.argv[2])
	elif len(sys.argv) == 2:
		keyword = sys.argv[1]
		max_page = 1
	else:
		keyword = "中国好声音"
		max_page = 1
	try:
		keyword = keyword.decode("gbk")
		keyword = keyword.encode("utf8")
	except:
		pass
		
	song_list = get_search_list(keyword, max_page=max_page)
	song_list = [song for song in song_list if (len(song["SongName"]) <= 10 and u"、" not in song["Artist"] and song["AlbumArtist"])]
	download_list(song_list)