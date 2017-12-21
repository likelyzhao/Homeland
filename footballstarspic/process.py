import os
import json

access_key = 'Access_Key'
secret_key = 'Secret_Key'
bucket_name = 'Bucket_Name'
bucket_based_url = "Based_url"
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
	print(info)
	assert ret['key'] == key
	assert ret['hash'] == etag(localfile)
	return bucket_based_url + key

def _mkdir(path):
	if not os.path.exists(path):
		os.mkdir(path)

rootpath = 'football'
_mkdir(rootpath)
Auth = get_qiniu_Auth(access_key,secret_key)
with open('sofifa_page_data.json') as f:
	line = f.readline()
	dict = json.loads(line)
	for idx,item in enumerate(dict):
		url = item['header_img']

		uid = url.split('/')[-1].split('.')[0]
		print(uid)
		_mkdir(os.path.join(rootpath,uid))
		print(url)

		new_url = url.replace('/48','')
		print(url.replace('/48',''))
		for year in range(12,19):
			import requests
			new_url_with_year = new_url.replace('18',str(year))
			r = requests.get(new_url_with_year)
			if r.status_code is 200:
				save_path = os.path.join(rootpath,uid,str(year) + '.png')
				print("saving to " + save_path)
				ftest = open(save_path,'wb')
				ftest.write(r.content)
				ftest.close()

#		key = str(idx)+ '.png';
#		qiniu_url = upload_with_token(Auth,bucket_name,key,localfile)
		fout = open(os.path.join(rootpath,uid,'info.json'), 'w')
#		item['header_img'] = qiniu_url
		item['team'] = item['term']
		item.pop('term',None)
		fout.write(json.dumps(item) + '\n')
		fout.close()




