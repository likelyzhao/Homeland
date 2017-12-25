import os
import json

access_key = 'Access_Key'
secret_key = 'Secret_Key'
bucket_name = 'Bucket_Name'
bucket_based_url = "Based_url"
localfile = 'bbb.png'
json_file = 'test.json'
threshold = 0.5

labels = {'1' : 'bloodiness','2':'bomb','3':'march','4':'beheaded','5':'fight'}


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

fp = []
for i in range(1,6):
	key =str(i)
	print(key)
	fp.append(open(labels[key] + '.jsonlist','w'))
# Auth = get_qiniu_Auth(access_key,secret_key)
with open(json_file) as f:
	for line in f.readlines():
		dict = json.loads(line)
		url = dict['url']
		res = dict['label']['class']
		print(res['terror'])
		if res['index'] == 0:
			continue
		if res['score'] < threshold:
			continue
		fp[res['index']-1].write(json.dumps(dict) + '\n')





