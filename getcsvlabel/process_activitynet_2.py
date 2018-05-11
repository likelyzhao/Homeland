import json




with open("activity_net.v1-3.min.json") as f:
	contents = json.load(f)

id2name ={}

label_list = []
f1 = open("Activity_label_struct.txt",'w')


for content in contents['taxonomy']:
	key = content
	if key['parentId'] not in id2name:
		id2name[key['parentId']] = key['parentName']
	if key['nodeId'] not in id2name:
		id2name[key['nodeId']] = key['nodeName']
	#dicts = contents['database']['nodeId']
#print(sorted(id2name.items()))
struct = {}
for content in contents['taxonomy']:
	if content['parentId'] not in struct:
		struct[content['parentId']] = []
		struct[content['parentId']].append(content['nodeId'])
	else:
		struct[content['parentId']].append(content['nodeId'])

for id in sorted(struct.items()):
	if  (id[0]) is None:
		continue
	print(id)
	f1.write(id2name[id[0]] + '\n')
	for node in id[1]:
		f1.write(id2name[node] + '\n')

	f1.write('\n'*2)


