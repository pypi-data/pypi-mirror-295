from combinatorlite.environment.apienv import *
from combinatorlite.interpreter.globalobjects import *
import time
import os
import psutil
import traceback

class world_exception(Exception):
    def __init__(self, message={}):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        self.error = message

class world_pending_exception(Exception):
    def __init__(self, message={}):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        self.error = message

class worldclass:
    
    def __init__(self,extfunctions={}, out_data_type='any', extenv = None):
        self.envtime_sec = 0
        self.total_runtime = 0
        self.world_failed = 0
        self.runtime = 0
        self.obs = None 
        self.extfunctions = extfunctions
        self.updateextfunctiontype()
        self.version = 0
        self.extenv = extenv
    

    def updateextfunctiontype(self):
        for k,v in self.extfunctions.items(): 
            if "type" in v:
                atype.update({k:v["type"]})
            else:
                atype.update({k: None})
            
            no_of_args.update({k:v["args"]})
    
    def reset(self):
        self.version = 0
        self.world_failed = 0
        self.runtime = 0
        self.obs = None  

        
    def upgrade(self):
        self.version +=1
        
    def put_ext_action(self,actionname,params):
        tick = time.time()
        try:
            self.obs = self.extfunctions[actionname]["function"](self.extenv,*params) 
            self.runtime += 1
            #self.total_runtime += 1
            tock = time.time()
            self.envtime_sec += tock - tick
        except Exception as e:
            traceback.print_exc()
            #print("action except",e)
            self.world_failed = 1
            tock = time.time()
            self.envtime_sec += tock - tick
            raise world_exception({'message':repr(e),'error':repr(e),'nodeid':0})
        
            
    def get_ext_data(self):
        return self.obs     
                   
    
######### initialize world
init_world = worldclass()