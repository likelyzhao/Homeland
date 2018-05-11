import json
import os

set = 'train'
def downlsvc(movie_name):
	import subprocess
#	cmd = u'curl http://xsio.qiniu.io/' + movie_name + ' -H \'Host:otd9g8ppk.bkt.clouddn.com\' -o movie_temp'
	cmd = u'wget ' + 'otd9g8ppk.bkt.clouddn.com/' +movie_name + ' -O movie_temp'
	print(cmd)
	subprocess.call([cmd], shell=True)

with open("mmdate.txt") as f:
	contents = f.readlines()

labels = []
with open("lsvc_class_index.txt") as f:
	for line in f:
		labels.append(line.split('\t')[-1].strip())
print(labels)


setlabel = {}
with open("lsvc_{}.txt".format(set)) as f:
	for line in f:
		setlabel[line.split(',')[0].strip()] = line.split(',')[-1].strip()
print(setlabel)

f = open("lsvc_{}.jsonlist".format(set),'w')

for content in contents:
	filename = content.split('	')[0]
	print(filename)

	filename_idx = os.path.basename(filename)
	filename_idx,_ = os.path.splitext(filename_idx)
	if filename_idx not in setlabel:
		continue
	downlsvc(filename)

	import cv2

	video = cv2.VideoCapture('movie_temp')
	length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
	width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
	height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
	fps = video.get(cv2.CAP_PROP_FPS)
	duration = length * 1.0 / fps


	ava_json = {
		"url":'otd9g8ppk.bkt.clouddn.com/'+ filename,
		"type":"video",
		"metadata":{
			"duration":duration,
			"resolution": str(width) + "x" + str(height),
		},
		"clips":
			[
				{
					"name":"video_lsvc",
					"type": "video_untrimmed_cls",
					"version":"1",
					"data":[
						{"label": labels[int(setlabel[filename_idx])]
					}]

				}
			]
	}
#	print(ava_json)

	f.write(json.dumps(ava_json) + '\n')

f.close()