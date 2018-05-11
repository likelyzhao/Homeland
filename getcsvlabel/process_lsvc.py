import json

with open("Activity.json") as f:
	contents = f.readlines()


f = open("Activity.jsonlist",'w')

for content in contents:
	dicts = json.loads(content)

	ava_json = {
		"url":dicts['url'],
		"type":"video",
		"metadata":{
			"duration":dicts['video_info']['duration'],
			"resolution": dicts['video_info']['resolution'],
		},
		"clips":
			[
				{
					"name":"video_activitynet",
					"type": "video_detection",
					"version":"1",
					"data":dicts['label']['action-detect']['actions']

				}
			]
	}
#	print(ava_json)

	f.write(json.dumps(ava_json) + '\n')

f.close()