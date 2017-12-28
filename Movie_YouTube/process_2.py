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


fp = []
# Auth = get_qiniu_Auth(access_key,secret_key)
pre_name = ""
issame = False
frameidx_list =[]
fout =  open("rename.txt",'w')
fout2 =  open("remove.txt",'w')
idx =0
with open(json_file) as f:
	for line in f.readlines():
		filename = line.split('	')[0]
		if 'mp4' in filename or 'webm' in filename:
			_,ext= os.path.splitext(filename)
#			print(filename)
#			print(ext)
			new_name = "MARCH_YOUTUBE_{0:03}{1}".format(idx,ext)
#			print(new_name)
			idx+=1
			fout.write('{0}	{1}\n'.format(filename,new_name))

#			print(filename)
			pass
		else:
#			print(filename)
			fout2.write(line)

fout.close()
fout2.close()







