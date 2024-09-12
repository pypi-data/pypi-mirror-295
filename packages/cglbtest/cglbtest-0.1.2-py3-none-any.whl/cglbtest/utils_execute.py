import os,subprocess
from.utils_file import dir_create,dir_remove
class UtilsExecute:
	def __init__(A,pre_folder_delete=None,pre_folder_creation=None,command_suffix=''):A.pre_folder_delete=pre_folder_delete;A.pre_folder_creation=pre_folder_creation;A.command_suffix=command_suffix
	def _pre_operations(A,working_directory):
		B=working_directory
		if A.pre_folder_delete:
			for dir in A.pre_folder_delete:dir_remove(os.path.join(B,dir))
		if A.pre_folder_creation:
			for dir in A.pre_folder_creation:dir_create(os.path.join(B,dir))
	def _post_operations(A,working_directory):0
	def _process(A,command,working_directory):B=working_directory;A._pre_operations(B);C=f"{command}{A.command_suffix}";subprocess.run(C,shell=True,check=True,cwd=B);A._post_operations(B)
	def process(A,command,working_directory):A._process(command,working_directory)