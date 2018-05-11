import os
FILE_NAME = 'log720.txt'
FILE_OUT = "720.json"
FILE_LIST = []
fout  = open(FILE_OUT,"w")
dict_list =[]

with open(FILE_NAME) as f:
	for line in f.readlines():
		import json
		dict =  json.loads(line)
		if dict['img'] not in FILE_LIST:
			FILE_LIST.append(dict['img'])
			dict_out = {}
			dict_out['url'] = dict["img"]
			dict_out['type'] = "image"
			dict_out['label'] = [{
				"name":"general_d",
				"type":"detection",
				"version":"1",
				"data":[
					{"class":"face","bbox":dict['pts'],'score':dict['score']},
				]
				}]
			dict_list.append(dict_out)
		else:
			pidx = 0
			for idx,line in enumerate(FILE_LIST):
				if line  == dict['img']:
					pidx = idx
					break

			out = {
				"class": "face", "bbox": dict['pts'],'score':dict['score']
			}

			import copy
			temp = copy.deepcopy(dict_list[pidx])
			temp['label'][0]['data'].append(out)
			dict_list[pidx] = temp

	for dict_out in dict_list:
		fout.write(json.dumps(dict_out) + '\n')

