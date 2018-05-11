import os
import json

data_path = '/Users/zhaozhijian/Dev/BK_Video_Cls_train_v0.3/'
val_ratio = 0.2
extends = '.avi,.mp4'


def _mkdir(path):
	if not os.path.exists(path):
		os.mkdir(path)

fout_train = open('train.txt','w')
fout_val = open('val.txt','w')
for name in (os.listdir(data_path)):

	if os.path.isdir(os.path.join(data_path,name)):
		subpath = os.path.join(data_path,name)
		name_list =[]
		for tempname in os.listdir(subpath):
			for extend in extends.split(','):
				if extend in  os.path.join(subpath,tempname):
					name_list.append(tempname)

		val_num = int(val_ratio * len(name_list))
		train_num = len(name_list)- val_num
		print('label = {0} training : {1} val : {2}'.format(name,train_num,val_num))

		for filename in name_list[0:train_num]:
			fout_train.write('{0},{1}\n'.format(os.path.join(name,filename),name))

		for filename in name_list[-val_num:]:
			fout_val.write('{0},{1}\n'.format(os.path.join(name,filename),name))











