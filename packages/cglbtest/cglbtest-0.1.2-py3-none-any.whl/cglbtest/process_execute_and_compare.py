import os
from.utils_compare import UtilsCompare
from.utils_execute import UtilsExecute
class ProcessExecuteAndCompare:
	def __init__(A,utils_execute,utils_compare,test_exe_path,ref_exe_path=None,prefix_files_path='',error_rule_patterns=None,dir_to_compare=''):A.utils_execute=utils_execute;A.utils_compare=utils_compare;A.test_exe_path=test_exe_path;A.ref_exe_path=ref_exe_path;A.prefix_files_path=prefix_files_path;A.error_rule_patterns=error_rule_patterns;A.dir_to_compare=dir_to_compare
	def execute_and_compare(A,test_dir,ref_dir,run_ref=True,name='',report_dir=''):
		C=ref_dir;B=test_dir;B=A.prefix_files_path+B.rstrip('/');C=A.prefix_files_path+C.rstrip('/');A.utils_execute.process(A.test_exe_path,B)
		if run_ref:A.utils_execute.process(A.ref_exe_path,C)
		return A.utils_compare.compare_directory(f"{B}/{A.dir_to_compare}",f"{C}/{A.dir_to_compare}",report_dir=report_dir,name=name,error_rule_patterns=A.error_rule_patterns)