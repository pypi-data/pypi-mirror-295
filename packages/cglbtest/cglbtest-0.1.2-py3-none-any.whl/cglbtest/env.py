import yaml
class Env:
	def __init__(A,yaml_file=''):
		F=False;E='execute_and_compare';B=yaml_file;A.conf={}
		if B:
			with open(B,'r')as G:A.conf=yaml.safe_load(G)
		if A.conf.get(E,F):
			C=A.conf[E]
			for D in['meta','assets_mgmt','execute','file_check','compare']:
				if not C.get(D,F):C[D]={}