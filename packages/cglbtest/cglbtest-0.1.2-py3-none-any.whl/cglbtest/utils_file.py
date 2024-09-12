import json,os,shutil
def file_remove(path):
	if os.path.exists(path):os.remove(path)
def dir_remove(path):
	if os.path.exists(path):shutil.rmtree(path)
def dir_create(path):
	if not os.path.exists(path):os.makedirs(path)
def dir_copy(source_dir,target_dir):shutil.copytree(source_dir,target_dir)
def text_write(path,data):
	with open(path,'w')as A:A.write(data)
def text_load(path):
	with open(path,'r')as A:return A.read()
def json_write(path,data):
	with open(path,'w')as A:json.dump(data,A,indent=4)
def json_load(path):
	with open(path)as A:return json.load(A)
def move(source,target):shutil.move(source,target)