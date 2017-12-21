import os
import json

access_key = 'Access_Key'
access_key = 'Secret_Key'
bucket_name = 'Bucket_Name'

localfile = 'bbb.png'

def get_qiniu_Auth(access_key,secret_key):
	from qiniu import Auth

	# write ak sk
	q = Auth(access_key, secret_key)
	return q

def upload_with_token(Auth,bucket_name,key,localfile):
	from qiniu import put_file,etag

	token = Auth.upload_token(bucket_name, key, 3600)

	ret, info = put_file(token, key, localfile)
	print(ret)
	assert ret['key'] == key
	assert ret['hash'] == etag(localfile)

Auth = get_qiniu_Auth(access_key,access_key)
with open('sofifa_page_data.json') as f:
	line = f.readline()
	dict = json.loads(line)
	for item in dict:
		url = item['header_img']
		new_url = url.replace('/48','')
		print(url.replace('/48',''))
		import subprocess
		subprocess.call(['wget ' + new_url + ' -O ' + localfile],shell=True)
		key = item['name'] + '_'+item['term'];
		upload_with_token(Auth,bucket_name,key,localfile)


