# -*- coding:utf-8 -*-
import os
import json

access_key = 'Access_Key'
secret_key = 'Secret_Key'
bucket_name = 'Bucket_Name'
bucket_based_url = "Based_url"
localfile = 'bbb.png'
json_file = 'splits.json'
threshold = 0.5
movie_header = 'http://ozqw10x19.bkt.clouddn.com/IMDB评选TOP250/'

def _mkdir(path):
	if not os.path.exists(path):
		os.mkdir(path)

expand_range =3

def convertframe2time(frame_idx):
	hour = frame_idx/3600
	minutes = (frame_idx - 3600 * hour)/60
	seconds = (frame_idx - 3600 * hour)%60

	return '{0:02}:{1:02}:{2:02}'.format(hour,minutes,seconds)


def make_clips(movie_name,annotation_video):
	import subprocess
	if len(annotation_video) == 0:
		return
	cmd = 'curl http://xsio.qiniu.io/' + movie_name + ' -H \'Host:ozqw10x19.bkt.clouddn.com\' -o movie_temp'
	print(cmd)
	retcode = subprocess.call([cmd])
	for idx,anno in enumerate(annotation_video):
		ffmpeg_cmd = 'ffmpeg'
		start = anno['time'][0]
		end = anno['time'][1]

		ffmpeg_cmd += ' -ss ' + convertframe2time(start)
		ffmpeg_cmd += ' -t ' + convertframe2time(end)
		ffmpeg_cmd += ' -i movie_temp '
		ffmpeg_cmd +=  movie_name + '_' + str(idx) + '.mp4'
		print(ffmpeg_cmd)
		subprocess.call([ffmpeg_cmd])

with open(json_file) as f:
	for line in f.readlines():
		dict = json.loads(line)
		url = dict['url']
		movie_name = url.split('/')[-1].split('_')[0]
		make_clips(movie_name,dict['video'])







