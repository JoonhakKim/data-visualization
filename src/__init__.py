
#including config file inside of __init.py

#changing the placement of the config file 
#would cause a circulatory importing problems
#shit way of coding but for small program like this--I.E if I can manage
#its more convinient 

#################################################
####                                        #####
####    #####   ###  ####    ###  #   ## ##  #### 
###    #       #   # #  ##   #        # ##    ###
##     ##      #   # #   #  ####  #      #     ##
#       #####   ###  #   #   #    #   ###       #
#                                               #
from pathlib import Path


file_path = Path(__file__).resolve().parent
db_path = str(file_path.parents[0] / 'Database')
















#                                                #
##                                              ##
####                                          ####
##################################################


#importing module 
from . import stock_utils
from . import data_loader
from . import data_loader_helpers
from . import data_visualizer




