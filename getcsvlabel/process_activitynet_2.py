import json




with open("activity_net.v1-3.min.json") as f:
	contents = json.load(f)

label_list = []
f1 = open("Activity_train.jsonlist",'w')
f2 = open("Activity_val.jsonlist",'w')
f3 = open("Activity_test.jsonlist",'w')

for content in contents['database']:
	key = content
	dicts = contents['database'][key]
	print(dicts)



	ava_json = {
		"url":'oxy45khzj.bkt.clouddn.com/v_{0}.mp4'.format(key),
		"type":"video",
		"metadata":{
			"duration":dicts['duration'],
			"resolution": dicts['resolution'],
		},
		"clips":
			[
				{
					"name":"video_activitynet",
					"type": "video_detection",
					"version":"1",
					"data":dicts['annotations']

				}
			]
	}
#	print(ava_json)
	if dicts['subset'] == 'training':
		f1.write(json.dumps(ava_json) + '\n')
		this_label = dicts['annotations'][0]['label']
		if this_label not in label_list:
			label_list.append(this_label)
	if dicts['subset'] == 'validation':
		f2.write(json.dumps(ava_json) + '\n')
		this_label = dicts['annotations'][0]['label']
		if this_label not in label_list:
			label_list.append(this_label)
	if dicts['subset'] == 'testing':
		f3.write(json.dumps(ava_json) + '\n')

f1.close()

with open("Activity_label.txt",'w') as f:
	for idx,label in enumerate(label_list):
		f.write(str(idx+1) + '\t'+ label_list[idx] + '\n')

print(label_list)