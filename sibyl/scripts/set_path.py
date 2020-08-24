# -*- coding: utf-8 -*-

import sys
import os
from os.path import dirname

env_var_name = 'RESPYTHONPATH'
default_sibyl_path = '~stockrsm/r209'
stockrsm_twisted_path = "/usr/home/enstb2/projets/stockrsm/.local/lib/python3.4/site-packages"

def set_path():
    sibyl_path = os.getenv(env_var_name, default_sibyl_path)
    local_path = dirname(dirname(dirname(os.path.abspath(__file__))))
    stock_rsm_path = os.path.expanduser(sibyl_path)

    sys.path.insert(0, stock_rsm_path)
    sys.path.insert(0, local_path)
    
    if (os.path.isdir(stockrsm_twisted_path)):
        sys.path.insert(0, stockrsm_twisted_path)
    
    import twisted
    print ("Twisted version in use: " + twisted.version.short())
    
    #print (sys.path)
    return stock_rsm_path
