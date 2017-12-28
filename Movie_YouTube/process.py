import os
import json

access_key = 'Access_Key'
secret_key = 'Secret_Key'
bucket_name = 'Bucket_Name'
bucket_based_url = "Based_url"
localfile = 'bbb.png'
json_file = 'list.txt'
threshold = 0.5

def get_qiniu_Auth(access_key,secret_key):
	from qiniu import Auth

	# write ak sk
	q = Auth(access_key, secret_key)
	return q

def upload_with_token(Auth,bucket_name,key,localfile):
	from qiniu import put_file,etag

	token = Auth.upload_token(bucket_name, key, 3600)

	ret, info = put_file(token, key, localfile)
	print(info)
	assert ret['key'] == key
	assert ret['hash'] == etag(localfile)
	return bucket_based_url + key

def _mkdir(path):
	if not os.path.exists(path):
		os.mkdir(path)


import subprocess32 as sp
import json


def probe(vid_file_path):
	''' Give a json from ffprobe command line

	@vid_file_path : The absolute (full) path of the video file, string.
	'''
	if type(vid_file_path) != str:
		raise Exception('Gvie ffprobe a full file path of the video')
		return

	command = ["ffprobe",
			"-loglevel",  "quiet",
			"-print_format", "json",
			 "-show_format",
			 "-show_streams",
			 vid_file_path
			 ]

	pipe = sp.Popen(command, stdout=sp.PIPE, stderr=sp.STDOUT)
	out, err = pipe.communicate()
	return json.loads(out)


def duration(vid_file_path):
	''' Video's duration in seconds, return a float number
	'''
	_json = probe(vid_file_path)

	if 'format' in _json:
		if 'duration' in _json['format']:
			return float(_json['format']['duration'])

	if 'streams' in _json:
		# commonly stream 0 is the video
		for s in _json['streams']:
			if 'duration' in s:
				return float(s['duration'])

	# if everything didn't happen,
	# we got here because no single 'return' in the above happen.
	raise Exception('I found no duration')
	#return None

def convertframe2time(time):
	hour = time / 3600
	minutes = (time - 3600 * hour) / 60
	seconds = (time - 3600 * hour) % 60

	return '{0:02}:{1:02}:{2:02}'.format(hour,minutes,seconds)


def split(vid_file_path):
	if type(vid_file_path) != str:
		raise Exception('Gvie ffprobe a full file path of the video')
		return
	last = duration(vid_file_path)
	start =0
	step = 5
	idx = 0
	while start < last:
		outputpath = '{0}_{1:03}.mp4'.format(vid_file_path,idx)
		command = ["ffmpeg",
			"-ss",  convertframe2time(start),
			"-t", str(step),
			 "-i",vid_file_path,
			outputpath
			 ]
		pipe = sp.Popen(command, stdout=sp.PIPE, stderr=sp.STDOUT)
		out, err = pipe.communicate()
		idx+=1
		start+=step


fp = []
pre_name = ""
issame = False
frameidx_list =[]
fout =  open("rename.txt",'w')
fout2 =  open("remove.txt",'w')
idx =0
split('MARCH_YOUTUBE_0.webm')

with open(json_file) as f:
	for line in f.readlines():
		filename = line.split('	')[0]


fout.close()
fout2.close()







