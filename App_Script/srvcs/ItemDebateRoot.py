# ***********************************************************************************************************************************************
# ItemDebateRoot.py :        class for the root of a debate
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


class ItemDebateRoot ( Item ):
    '''
    ItemDebateRoot is a member of a debate-thread
    '''

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # constructor. 
    #
    #
    # 16.01.2013   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def __init__(self, page ):
        try:
            Item.__init__(self, page )                                      # wake up papa ; mother njbTools is included by inheritance!
            self.objTypIdx = self.getObjectTypeId( 'DEBATE_ROOT' )          # define what kind of object we have by setting the object_type_id as integer

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    #
    # data handling . mostly overloaded in the derived specialists
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # load :  by given objectID in item.base_collection a object will be loaded
    # 
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # def load( self, itemBaseID ):
    #
    # class uses function in the base-class 'Item'


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # loadDetails :  by given object_type index and object-detail-id the machine loads the detail-data of given item
    # 
    # this function should be overloaded by the specialized deriver classes
    #
    # parameter : objDetailId       :    the mongo-id of the item in the detail-data-colection
    # return    : html              :    formatet HTML 
    #
    # 16.01.2012   - bervie-      initial realese
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # def loadDetails( self, objDtlId ):
    #
    # class uses function in the base-class 'Item'

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # save()   save a JOB_ROOT - 
    # 
    # parameter   :  self
    # returns     :  _id of last inserted element
    #
    # 16.01.2012   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # def save( self ):
    #
    # class uses function in the base-class 'Item'


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # saveDetails : save the details of an debate-root-element to the detail-collection
    #              
    # function will be overwritten by the specialyzed child-classes
    #
    # returns   : newDetailObjId        :  the ID of the data-item in the detail-collection
    #
    # 17.01.2013   - bervie-      initial realese
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # def saveDetails( self ):
    #
    # using methode in superclass 'Item'



    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # chainCreateHeader()  :   creating a new header for a discussion-thread : DEBATE_HEADER
    #
    # parameter     :  rootElemID           : the root-elem we are looking for
    # return        :  createdHeaderId      : the new created ID of the Header
    #
    # HINT : the initiator is the creator of the root-element. In this case it means the guy who asked for some help in his neighbouhood
    #        the prospect is the guy who is interested in getting the job. for every initiator/prospect-pair there is chain 
    #
    #
    #
    #
    # 21.12.2012   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def chainCreateHeader( self  ):
        try:
            rootElemId      = self.Page.ViewState['MongoID']
            headerTypeId    = self.getObjectTypeId('ROOT_HEADER')
            self.log.w2lgDvlp("ItemDebateMsg.chainCreateHeader called for  " + rootElemId + " of TypeId : " + unicode(headerTypeId) )
            root = self.itemTbl.Rows.Find( rootElemId )

            # 1. write the detail-data-ID
            initiatorGUID       = root['_creatorGUID']              # the creator of the root-elem
            prospectGUID        = self.usrDt.getItem('GUID')        # current user
            headerCreated       = System.DateTime.UtcNow            # time of header-creation

            lastUpdateInitiator = System.DBNull.Value               # last insert from job-offerer
            lastUpdateprospect  = System.DateTime.UtcNow            # last insert from service-provider interested in the job
            lastVisitInitiator  = System.DBNull.Value               # last visit from job-offerer
            lastVisitProspect   = System.DBNull.Value               # last visit from service-provider interested in the job


            # 2. write the item.base-data
            self.objTypIdx       = headerTypeId
            self.objectDetailID  = newDebateHeaderDetailId

            headerId = self.storeGeneralBase()
            self.setMembrAttrb()

            # self.data is not changed for HEADER-elements
            return headerId


        except Exception,e:
            self.log.w2lgError(traceback.format_exc())

