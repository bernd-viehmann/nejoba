# ***********************************************************************************************************************************************
# ItemDebateHeader.py :        class for headers added 
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


class ItemDebateHeader ( Item ):
    '''
    ItemDebateHeader is heading of a debate_thread
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
            self.objTypIdx = self.getObjectTypeId( 'DEBATE_HEADER' )          # define what kind of object we have by setting the object_type_id as integer

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
    #        self.log.w2lgDvlp("ItemDebateheader.save called " )

    #        # 1. save detail-data in the detail-collection
    #        newDetailId = self.saveDetails()

    #        # 2. define the values that will be inserted into item.base collection
    #        self.objectDetailID  = newDetailId      # the monog-id of the data in the detail-collection
    #        self.rootElemGUID    = System.Guid.NewGuid().ToString('N')      # we have a new announce which needs a GUID

    #        # 3. write data to the item.base-collection
    #        baseItemId = self.storeGeneralBase()

    #        return baseItemId

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
    #        self.log.w2lgDvlp("ItemDebateHeader.saveDetails called " )
    #        self.ui.getCtrlTree( self.Page.Master )

    #        # store who was the creator of the debate
    #        itemData = {}
    #        itemData['debateCreatorGUID'] = self.usrDt.getItem('GUID')
            
    #        # write the data to the mongo-db detail table 
    #        dstntn = self.typeToColl[ self.objTypIdx ]
    #        storeDataDct = {'collection':dstntn , 'slctKey':None , 'data': itemData}
    #        newObjId = self.insertDoc(storeDataDct)

    #        return newObjId

    #    except Exception,e:
    #        self.log.w2lgError(traceback.format_exc())



