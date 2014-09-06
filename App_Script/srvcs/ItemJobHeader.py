# ***********************************************************************************************************************************************
# ItemJobHeader.py :        class for headers added for JOBS
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


class ItemJobHeader ( Item ):
    '''
    ItemJobHeader is the maintenance-starter for a job-trial-discussion
    '''

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # constructor. 
    #
    #
    # 16.01.2013   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def __init__(self, page ):
        try:
            Item.__init__(self, page )           # wake up papa ; mother njbTools is included by inheritance!
            self.objTypIdx = self.getObjectTypeId( 'JOB_HEADER' )     # define what kind of object we have by setting the object_type_id as integer

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # save       : calls detail-item-save and store the admin-data to the item.base-collection and to the app-cache
    # 
    # parameter  : self
    #
    # returns    : _id of last inserted element
    #
    #
    # 16.01.2013   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    #def save( self ):
    #    try:
    #        pass

    #    except Exception,e:
    #        self.log.w2lgError(traceback.format_exc())



    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # saveDetails : save details of item
    #              
    # function will be overwritten by the specialyzed child-classes
    #
    # returns   : newDetailObjId        :  the ID of the data-item in the detail-collection
    #
    # 17.01.2013   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    #def saveDetails( self ):
    #    try:
    #        pass

    #    except Exception,e:
    #        self.log.w2lgError(traceback.format_exc())








