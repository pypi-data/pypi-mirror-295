import os
from jinja2 import Template
CURRENT_DIR=os.path.dirname(os.path.realpath(__file__))
def template_render(filename,data):
	with open(f"{CURRENT_DIR}/{filename}",'r')as A:B=A.read();C=Template(B);return C.render(data)