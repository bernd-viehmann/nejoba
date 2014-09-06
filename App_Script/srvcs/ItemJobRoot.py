# ***********************************************************************************************************************************************
# ItemJobRoot.py :        class for headers added 
# 
# parent :                  Item
#
#
#  16.01.2012  - bervie -     initial realese
#
#
# ***********************************************************************************************************************************************
import clr
clr.AddReference('MongoDB.Bson')
clr.AddReference('MongoDB.Driver')
from MongoDB.Bson import *
from MongoDB.Driver import *
from System.Web.Configuration import *

import System.Text
import traceback            # for better exception understanding
import System.Guid
import re

from Item import *       # base-class for data-objects


class ItemJobRoot( Item ):
    '''
    ItemJobRoot is a member of a debate-thread
    '''

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # constructor. 
    #
    #
    # 16.01.2013   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def __init__(self, page ):
        try:
            Item.__init__(self, page )                              # wake up papa ; mother njbTools is included by inheritance!
            self.objTypIdx = self.getObjectTypeId( 'JOB_ROOT' )     # define what kind of object we have by setting the object_type_id as integer

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # save(..)   an announce stored to the mongo-db and the item-cache
    # 
    #
    # class uses function in the base-class 'Item'
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # saveDetails : save the details of an debate-root-element to the detail-collection
    # 
    #
    # class uses function in the base-class 'Item'
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 



