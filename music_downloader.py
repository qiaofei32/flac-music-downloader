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

def get_search_list(keyword, source="酷狗音乐", max_page=1):
	sign = "a5cc0a8797539d3a1a4f7aeca5b695b9"
	source = DATA_SOURCE[source]
	keyword = urllib.quote(keyword)
	song_list = []
	for page in range(1, max_page+1):
		url = "http://api.itwusun.com/music/search/%s/%d?format=json&sign=%s&keyword=%s" %(source, page, sign, keyword)
		data = requests.get(url).content
		if not data:
			break
		song_list += json.loads(data)
	return song_list

def donwload_song(song_url, file_name, retry=3):
	try:
		urllib.urlretrieve(song_url, file_name)
	except:
		if retry > 0:
			return donwload_song(song_url, file_name, retry=retry-1)
		else:
			return False
		
def download_list(song_list):
	for song in song_list:
		AlbumArtist = song["AlbumArtist"]
		Artist = song["Artist"]
		SongName = song["SongName"]
		SongName = SongName.split(u"-")[0]
		SongName = SongName.split(u"(")[0]
		SongName = SongName.split(u"（")[0]
		SongName = SongName.strip()
		FlacUrl = song["FlacUrl"]
		file_name = "Songs/%s-%s.flac" %(Artist, SongName)
		file_name = file_name.encode("gbk")
		if os.path.exists(file_name):
			continue
		print file_name
		donwload_song(FlacUrl, file_name)

if __name__ == "__main__":
	if len(sys.argv) == 2:
		keyword = sys.argv[1]
		try:
			keyword = keyword.decode("gbk")
			keyword = keyword.encode("utf8")
		except:
			pass
	else:
		keyword = "中国好声音"
	song_list = get_search_list(keyword)
	download_list(song_list)