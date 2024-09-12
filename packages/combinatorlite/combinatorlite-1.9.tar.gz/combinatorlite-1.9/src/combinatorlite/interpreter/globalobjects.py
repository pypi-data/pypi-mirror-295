import pickle

label =0
no_of_arguments=0 
world_version=0 
exec_status=0 
is_initial=0
runtime=0
#init_node_label = 1
graph_label = 1
world = None
C = 0.01
alpha = 0.5
PHASErunlimit = 0
L = 0.8

atype = {'iW':{'fun':{'i':['None'],'o':['any']}},
		'+':{'fun':{'i':['any','any'],'o':['any']}}, 
		'id':{'fun':{'i':['any'],'o':['any']}},
		'K':{'fun':{'i':['any'],'o':['any']}},
		'-':{'fun':{'i':['num','num'],'o':['num']}},
		'*':{'fun':{'i':['num','num'],'o':['num']}},
		'/':{'fun':{'i':['num','num'],'o':['num']}},
		'^':{'fun':{'i':['num','num'],'o':['num']}},
		'if':{'fun':{'i':['bool','any','any'],'o':['any']}},
		'=':{'fun':{'i':['any','any'],'o':['bool']}},
		'>':{'fun':{'i':['num','num'],'o':['bool']}}, 
		'&':{'fun':{'i':['bool','bool'],'o':['bool']}},
		'|':{'fun':{'i':['bool','bool'],'o':['bool']}},
		'!':{'fun':{'i':['bool'],'o':['bool']}},
		'hd':{'fun':{'i':['list'],'o':['any']}},
		'tl':{'fun':{'i':['list'],'o':['list']}},
		'cn': {'fun':{'i':['any','list'],'o':['list']}},
		'nl':{'fun':{'i':['any'],'o':['list']}},
		'ap': {'fun':{'i':['fun','any'],'o':['any']}},
		'fm':{'fun':{'i':['fun','list'],'o':['list']}}, 
		'zp':{'fun':{'i':['fun','list','list'],'o':['list']}}, 
		'ag':{'fun':{'i':['fun','list'],'o':['any']}},
		'rc':{'fun':{'i':['fun','fun','any'],'o':['any']}}, 
		'sn':{'fun':{'i':['world'],'o':['any']}},
		'ac':{'fun':{'i':['any'],'o':['world']}}, 
		'gc':{'fun':{'i':['any'],'o':['bool']}},
		'wm':{'fun':{'i':['any','any'],'o':['any']}},
		'lg':{'fun':{'i':['any'],'o':['fun']}},
		'lp':{'fun':{'i':['any','num'],'o':['any']}},
		'pop':{'fun':{'i':['any','any'],'o':['any']}},
		'pt':{'fun':{'i':['any'],'o':['any']}},
		'ak':{'fun':{'i':['dict','any','any'],'o':['dict']}}}

no_of_args = {'iW':0,'+':2,'id':1, 'K': 1,'-':2,'*':2,'/':2,'^':2,'if':3,'=':2,'>':2,'&':2,'|':2,'!':1,'hd':1,'tl':1,'cn':2,'nl':1,'ap':2,'fm':2,'zp':3,'ag':2,'rc':3,'sn':1,'ac':1,'gc':1,'wm':2,'lg':1,'gp':1, 'lp':2,'pop':2,'pt':1,'ak':3}


class current_node_label:
	def __init__(self):
		self.init_node_label = 1
	
	def set_node_label(self,node_label):
		self.init_node_label = node_label
	
	def inc_node_label(self):
		self.init_node_label += 1
current_node_label_obj = current_node_label()        

class nodeattributes:
    def __init__(self):
        self.attrib = {'wv': world_version, 'es': exec_status,'ii':is_initial,'rt':runtime,'w':world,'ty':None, 'dat':None}
    
    def updateattrib(self,attributes):
        self.attrib.update(attributes)

node_attributes_object = nodeattributes()
node_attributes = node_attributes_object.attrib
######## pint -> {'nodelabel':{'childnode_index':{'childnode_port':[probability]}}}
######### fp -> {'parentnodelabel'+'-'+'childnodelabel'+'-'+childnode_port: [probability]}}} 

graph_attributes = {'label':0,'name':'graph'}
#nodes = {init_node_label:node_attributes}
#graph = {'edges':{init_node_label:{1:init_node_label,2:init_node_label}}, 'terminalnodes':[terminal_init_node_labels], initialnodes:[initial_init_node_labels]}
#nodes = dict()

initgraph = {'attr':graph_attributes,'world':None,'edges':{},'nodes':{},'terminalnodes':{}, 'initialnodes':[], 'existingnodes':{} ,'atype': {'fun':{'i':['none'],'o':['none']}}}

