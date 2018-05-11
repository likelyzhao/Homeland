import os
import json

test = '{"type":"video","metadata":{"duration":41.656589,"resolution":"1280x720"},"category":[{"label":"others"}],"clips":{"name":"","type":"","version":"","data":[]},"url":"../Playing_squash/LiHImkhSl8Q.mp4"}'
json.loads(test)


DIR_PATH= '/Users/zhaozhijian/Dev/video/vott/output/jsonlist'
OUT_FILE = "jsonlist.txt"
OUT_FILE2 = 'baobaolist.txt'
f_out = open(OUT_FILE,"w")
f_out2 = open(OUT_FILE2,"w")
for line in os.listdir(DIR_PATH):
	if line !=  '.DS_Store':
		print(line)
		with open(os.path.join(DIR_PATH,line)) as f:
			line_json = f.readline()
			f_out.write(line_json + '\n')
			import json
			print(line_json)
			dict = json.loads(line_json)
			if len(dict['category']) == 0:
				continue
			if dict['category'][0]['label'] == 'playing squash':
				f_out2.write('Playing_squash/'+os.path.basename(dict['url']) + '\n')



