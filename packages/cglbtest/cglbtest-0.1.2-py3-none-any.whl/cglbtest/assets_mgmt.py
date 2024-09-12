from.utils_file import dir_remove,dir_create,dir_copy,move
class AssetsMgmt:
	def __init__(A,foldername='',working_dir=''):
		B=working_dir;A.foldername=foldername
		if A.foldername:A.assets_path=(f"{B}/"if B else'')+A.foldername;dir_remove(A.assets_path);dir_create(A.assets_path)
	def test_results_move(A,test_name,target_name,source_path):
		B=test_name
		if not A.foldername:return
		dir_create(f"{A.assets_path}/{B}");dir_copy(source_path,f"{A.assets_path}/{B}/{target_name}")
	def test_results_move_multi(A,test_name,name_path_map):
		if not A.foldername:return
		for(B,C)in name_path_map.items():A.test_results_move(test_name,B,C)