import os
import json

access_key = 'Access_Key'
secret_key = 'Secret_Key'
bucket_name = 'Bucket_Name'
bucket_based_url = "Based_url"
localfile = 'bbb.png'
json_file = 'test.json'
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


expand_range =3

def check_splits(frameidx_list):
	start_list =[]
	end_list =[]
	score_list =[]
	print(frameidx_list)
	max_idx = max(frameidx_list)
	score = range(0,max_idx)
	for i in range(0,len(score)):
		score[i]=0

#	print(score)
	for idx in frameidx_list:
		for x in range(idx-expand_range,idx + expand_range):
			if x <=0:
				continue
			if x >= max_idx:
				continue
			score[x]+=1
	str_s =''
	for scr in score:
		str_s +=str(scr)
#	print(str_s)
	parts = str_s.split('0')
	for part in parts:
		#print(len(part))
		if len(part) >=10:
			idx = str_s.find(part)
			start_list.append(idx)
			end_list.append(idx + len(part))
			sum =0
			for x in part:
				sum +=int(x)
			score_list.append(min(sum/len(part)/2.0,1))
#			print(part)


	return start_list,end_list,score_list

def write_json(starts ,ends,scores,orign_dic,fout):
	res_list =[]
	for idx , start in enumerate(starts):
		res ={}
		res['label'] = 'march'
		res['score'] = scores[idx]
		res['time'] = [start,ends[idx]]
		res_list.append(res)
	orign_dic['video'] = res_list
	fout.write(json.dumps(orign_dic) + '\n')
	pass


fp = []
# Auth = get_qiniu_Auth(access_key,secret_key)
pre_name = ""
issame = False
frameidx_list =[]
fout =  open("splits.json",'w')
with open(json_file) as f:
	for line in f.readlines():
		dict = json.loads(line)
		url = dict['url']
		filename = url.split('/')[-1]
		filename = filename.split('_')
		if pre_name != filename[0] :
			if issame :
				starts,ends,scores= check_splits(frameidx_list)
				write_json(starts,ends,scores,bk_dict,fout)
				frameidx_list=[]
			print(filename[0])
			pre_name = filename[0]
			bk_dict = dict
			issame = True
		frameidx_list.append(int(filename[-1].split('.')[0]))
		if len(filename) !=2:
			print(len(filename))
			print(filename)
		res = dict['label']['class']
#		print(res['terror'])

		if res['index'] == 0:
			continue
		if res['score'] < threshold:
			continue

starts,ends,scores= check_splits(frameidx_list)
write_json(starts, ends, scores, dict, fout)




