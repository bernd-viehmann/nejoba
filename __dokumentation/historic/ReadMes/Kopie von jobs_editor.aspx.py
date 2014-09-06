#  
# editor.aspx.py 
#  
# the webform is used for creating new job offers for the community. user can define the location, the typ of the job and the time of action
#  
#
#  03.10.2012   bevie    initial realese
#  13.01.2013   bevie    redesign to new Item_class partition
#
#
#  
from System.Web.Configuration import *
import System.DateTime
import System.Drawing.Color
import System.Web.UI.WebControls
import System.Guid
import traceback                    # for better exception understanding
import re                           # for finding the taggs

# # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # #
# # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # #
# # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # #
# # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # #

import mongoDbMgr                       # father : the acces to the database


# ################################################################################################################################################################################################################################################################################ #
# ################################################################################################################################################################################################################################################################################ #
class ItemBase( mongoDbMgr.mongoMgr ):
    '''BaseItem Class is the controller for a base-itm. The base-item is part of any item that is administrated by the nejoba system
       Other classes derive from this class to have the basic-functionality for nejoba-objects
       
       important member-attributes:
            self.strngSeperator : the character used to seperate strings into array-elemnts

            self.objectTypes  : a array of strings with the available object-types in nejoba
                                the index of a string in this array is written to the mongo to show what kind of object we have
       '''

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # constructor. 
    #
    # prepares the class for her job. stores an array with the object-types and a reference to the item-cache-table
    #
    # parameter : 
    #               itemCache : reference to the data-table that stores all base-itmes
    #
    # 17.11.2012   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def __init__(self, page ):
        try:
            mongoDbMgr.mongoMgr.__init__(self, page )                     # wake up papa ; mother njbTools is included by inheritance!

            self.strngSeperator = WebConfigurationManager.AppSettings['stringSeperator']        # define the character used for string-seperation
            objTypConf = WebConfigurationManager.AppSettings['objectTypes']                     
            self.objectTypes = objTypConf.split(self.strngSeperator)                            # available item-types stored in an array

            self.baseData = {}
            self.itemTbl     = self.appCch.dtSt.Tables["items"]
            self.itemTagsTbl = self.appCch.dtSt.Tables["itemTags"]


        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # storeGeneralBase()   store the basis-administration-data of an object to the mongo-DB
    # 
    # parameter
    # 
    #   objectType	                -int-               type identifier
    #   _objectDetailID	            -mongo_id-          mongoID of the data-item represented by this item
    #   _rootElemGUID	            -string-            GUID of an root_elem must be created outside - OR - the GUID of an existing root-objct the current item belongs to
    #
    #   headline                    -string-            the headline of the object  HINT: Only added to cached data-table. in db we have an extra-object
    #   bodymsg                     -string-            the body-message
    #
    #   _parentID	                -mongo_id-          forerunner of this object
    #   _followerID	                -mongo-id-          follower of this object
    #
    #   _locationID	                -mongo_id-          location if the item 
    #   taggingLabels	            -string-array-      taggs for the job
    #   from	                    -DateTime-          when will action be started
    #   till	                    -Datetime-          when will action end
    #
    # created internal :
    #
    #   _hostGUID	                -string-            GIUD of server hosting this item
    #   _creatorGUID	            -string-            GUID of the creator of this object
    #   creationTime	            -DateTime-          time the item was created in UTC
    #
    #
    # 17.11.2012   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def storeGeneralBase( self, objectType, objectDetailID, rootElemGUID=System.DBNull.Value, headline=System.DBNull.Value, bodymsg=System.DBNull.Value, parentID=System.DBNull.Value, followerID=System.DBNull.Value, locationID=System.DBNull.Value, taggingLabels=System.DBNull.Value, timeFrom=System.DBNull.Value, timeTo=System.DBNull.Value ):
        try:
            # get the index of the given object_type
            objTypIdx = self.objectTypes.index(objectType)
            if objTypIdx < 0:
                self.log.w2lgError('BaseItem->storeGeneralBase  : called with unknown object-type [' + objectType + ']. Abborting' )
                return
            
            creationDate    = System.DateTime.UtcNow                                                            # UTC time used for timestamps
            creatorGUID     = self.usrDt.getItem('GUID')                                                        # get the ID of the working user
            hostGUID        = self.strngSeperator = WebConfigurationManager.AppSettings['serverHostName']       # a unique ID for the server

            # 1. write the data to the mongo-db
            # made db-internal self.baseData['_ID'] = ''
            self.baseData['objectType']         = objTypIdx                 
            self.baseData['_objectDetailID']    = objectDetailID            
            self.baseData['_hostGUID']          = hostGUID                  
            self.baseData['_rootElemGUID']      = rootElemGUID
            self.baseData['_parentID']          = parentID
            self.baseData['_followerID']        = followerID
            self.baseData['_creatorGUID']       = creatorGUID               
            self.baseData['creationTime']       = creationDate
            self.baseData['_locationID']        = locationID 
            self.baseData['taggingLabels']      = taggingLabels
            self.baseData['from']               = timeFrom
            self.baseData['till']               = timeTo
            storeDataDct = {'collection':'item.base','slctKey':None,'data': self.baseData}
            newObjId = self.insertDoc(storeDataDct)

            # 2. add the inserted data also to cached data-table (except TaggingLables, which are an special-case)
            newRow = self.itemTbl.NewRow();
            newRow['_ID']                   = newObjId
            newRow['objectType']            = objTypIdx
            newRow['_objectDetailID']       = self.emptyIfNull( objectDetailID )
            newRow['_hostGUID']             = hostGUID                  
            newRow['_rootElemGUID']         = rootElemGUID              
            newRow['_parentID']             = self.emptyIfNull( parentID )
            newRow['_followerID']           = self.emptyIfNull( followerID )
            newRow['_creatorGUID']          = creatorGUID
            newRow['creationTime']          = creationDate
            newRow['_locationID']           = self.emptyIfNull( locationID )
            newRow['from']                  = timeFrom
            newRow['till']                  = timeTo
            # add the headline and part of the body-text to the cached data-table also. will be displayed in list-view of location
            if headline !=System.DBNull.Value : 
                newRow['subject']  = self.appCch.RemoveHtml(headline.ToString()).strip()[:140]
            if bodymsg  !=System.DBNull.Value : 
                newRow['body']     = self.appCch.RemoveHtml(bodymsg.ToString()).strip()[:200]
            self.itemTbl.Rows.Add(newRow)

            # 3. write tagging-lables to the extra Tagging-DataTable in the cache
            if taggingLabels != System.DBNull.Value:
                for tag in taggingLabels:
                    newRow = self.itemTagsTbl.NewRow();
                    newRow['_ID'] = newObjId                # the mongo_id
                    newRow['tag'] = tag                     # the tag
                    self.itemTagsTbl.Rows.Add(newRow)

            # 4. return newly created id to the caller
            self.newObjId = newObjId

            self.log.w2lgDvlp("ctrl_ItemBase->storeGeneralBase : object id of inserted item " + str(newObjId) ) 

            return newObjId

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # getHashTags      : find all strings that beginns with a # : they will be used as tag for the annoncments
    #                            using regular-expressions from the python re module
    #
    # 18.11.2012  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def getHashTags(self, textToCheck):
        try:
            self.log.w2lgDvlp('!!  --  texttocheck --  !!' + textToCheck )
            lstOfTags = re.findall("[#]{1}[^ \t\n\r\f\v<]*", textToCheck, re.U)
        
            # print all tags found to the nejoba log
            self.tagList = []
            for tag in lstOfTags:
                item = tag[1:26].upper()
                self.log.w2lgDvlp('!!  --  found tag before adding --  !!' + item )
                if len( item ) > 0 :
                    if (item not in self.tagList):
                        self.tagList.Add(item)
            # debug
            #for item in self.tagList:
            #    self.log.w2lgDvlp('!!  --  found tag  --  !!' + item )

            # if no taggs were defined we do not have to add anything
            if len(self.tagList) == 0:
                self.tagList = None;

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # emptyIfNull      : if System.DBNull.Value has to be inserted for an ID this function converts it to an empty string 
    #
    # 22.13.2012  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def emptyIfNull(self, txtToChck):
        try:
            if txtToChck == System.DBNull.Value:
                return System.String.Empty
            else:
                return unicode(txtToChck)

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())




# ################################################################################################################################################################################################################################################################################ #
# ################################################################################################################################################################################################################################################################################ #
class ItemMngr( ItemBase ):
    '''
    ItemManager is the generic class for working with nejoba.items
    in the constructor must be set what kind of object-type we have
    you can load , save or delete all kind of items
    
    loadItem            : loads the HTML of an single item 
    loadThread          : loads the HTML of a message-thread
    saveItem            : save a single item 
    saveThread          : append a new item at the end of a thread (or starts a new thread if it does not exists)
    deleteItem          : deletes a single item 
    deleteThread        : deletes a thread without the root_object
    deleteRootWithAll   : deletes a root-element and all objects that are related to it

    - internal functions -
    getChain            : returns an array with all item.base-_ids of a "what-ever-kind-of"-thread
    '''

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # constructor. save;load and display items that depend on root-objects like comments, offers or tour-data
    #
    #
    # parameter : Page :        reference to current webpage
    #             objType :     Type of object that will be handeled
    #
    #
    # 21.12.2012   - bervie-      initial realese
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def __init__(self, page ):
        try:
            ItemBase.__init__(self, page)
            self.html       = System.Text.StringBuilder()                                       # the html to write to the stream
            self.data       = {}                                                                # data loaded from db will be stored in dictionary


            self.objTypeSwitch = {  'JOB_ROOT'            : self.hndl_JOB_ROOT ,
                                    'JOB_HEADER'          : self.hndl_JOB_HEADER ,
                                    'JOB_MSG'             : self.hndl_JOB_MSG ,
                                    'JOB_SUBSCRIBER'      : self.hndl_JOB_SUBSCRIBER ,

                                    'DEBATE_ROOT'         : self.hndl_DEBATE_ROOT ,
                                    'DEBATE_HEADER'       : self.hndl_DEBATE_HEADER ,
                                    'DEBATE_MSG'          : self.hndl_DEBATE_MSG ,
                                    'DEBATE_SUBSCRIBER'   : self.hndl_DEBATE_SUBSCRIBER ,

                                    'REPORT_ROOT'         : self.hndl_REPORT_ROOT ,
                                    'REPORT_HEADER'       : self.hndl_REPORT_HEADER ,
                                    'REPORT_MSG'          : self.hndl_REPORT_MSG ,
                                    'REPORT_SUBSCRIBER'   : self.hndl_REPORT_SUBSCRIBER ,

                                    'EVENT_ROOT'          : self.hndl_EVENT_ROOT ,
                                    'EVENT_HEADER'        : self.hndl_EVENT_HEADER ,
                                    'EVENT_MSG'           : self.hndl_EVENT_MSG ,
                                    'EVENT_SUBSCRIBER'    : self.hndl_EVENT_SUBSCRIBER ,

                                    'PLACE_ROOT'          : self.hndl_PLACE_ROOT ,
                                    'PLACE_HEADER'        : self.hndl_PLACE_HEADER ,
                                    'PLACE_MSG'           : self.hndl_PLACE_MSG ,
                                    'PLACE_SUBSCRIBER'    : self.hndl_PLACE_SUBSCRIBER        }


            # the object-type defines what collection is used for the detail-data of the item
            self.typeToColl = {    0  : 'item.JOB_ROOT' , 
                                   1  : 'item.DEBATE_ROOT' , 
                                   2  : 'item.EVENT_ROOT' , 
                                   3  : 'item.PLACE_ROOT' , 
                                   4  : 'item.REPORT_ROOT' , 
                                   5  : 'item.JOB_HEADER' , 
                                   6  : 'item.DEBATE_HEADER' , 
                                   7  : 'item.EVENT_HEADER' , 
                                   8  : 'item.PLACE_HEADER' , 
                                   9  : 'item.REPORT_HEADER' , 
                                  10  : 'item.JOB_MSG' , 
                                  11  : 'item.DEBATE_MSG' , 
                                  12  : 'item.EVENT_MSG' , 
                                  13  : 'item.PLACE_MSG' , 
                                  14  : 'item.REPORT_MSG' , 
                                  15  : 'item.JOB_SUBSCRIBER' , 
                                  16  : 'item.DEBATE_SUBSCRIBER' , 
                                  17  : 'item.EVENT_SUBSCRIBER' , 
                                  18  : 'item.PLACE_SUBSCRIBER' , 
                                  19  : 'item.REPORT_SUBSCRIBE' }


        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # handler to set the detal-data-handler-class
    #
    # parameter : Page :        reference to current webpage
    #             objType :     Type of object that will be handeled
    #
    #
    # 21.12.2012   - bervie -      initial realese
    # 13.01.2013   - bervie -      renewed design
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def hndl_JOB_ROOT(self)          : return Item_JOB_ROOT(self.Page)
    def hndl_JOB_HEADER(self)        : return Item_JOB_HEADER(self.Page)
    def hndl_JOB_MSG(self)           : return Item_JOB_MSG(self.Page)
    def hndl_JOB_SUBSCRIBER(self)    : return Item_JOB_SUBSCRIBER(self.Page)

    def hndl_DEBATE_ROOT(self)       : return Item_DEBATE_ROOT(self.Page)
    def hndl_DEBATE_HEADER(self)     : return Item_DEBATE_HEADER(self.Page)
    def hndl_DEBATE_MSG(self)        : 
        self.log.w2lgDvlp( "hndl_DEBATE_MSG(self) called" )
        return Item_DEBATE_MSG(self.Page)
    def hndl_DEBATE_SUBSCRIBER(self) : return Item_DEBATE_SUBSCRIBER(self.Page)

    def hndl_REPORT_ROOT(self)       : return None
    def hndl_REPORT_HEADER(self)     : return None
    def hndl_REPORT_MSG(self)        : return None
    def hndl_REPORT_SUBSCRIBER(self) : return None

    def hndl_EVENT_ROOT(self)        : return None
    def hndl_EVENT_HEADER(self)      : return None
    def hndl_EVENT_MSG(self)         : return None
    def hndl_EVENT_SUBSCRIBER(self)  : return None

    def hndl_PLACE_ROOT(self)        : return None
    def hndl_PLACE_HEADER(self)      : return None
    def hndl_PLACE_MSG(self)         : return None
    def hndl_PLACE_SUBSCRIBER(self)  : return None


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # loadItem by given objectID in item.base_collection:
    # the function also loads the data from the associated data-details object
    # this is a generic function that loads the associatetd loder for this data_typ
    #
    #
    # parameter : itemBaseID  :    _id in item.base (mongo_id is also stored in session-cache)
    #
    #
    # 21.12.2012   - bervie-      initial realese
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def loadItem( self, itemBaseID ):
        try:
            row = self.itemTbl.Rows.Find( itemBaseID.ToString() )

            objTyp = row['objectType']                                              # object_type_ID == index in the string-array self.objectTypes
            objDtlId = row['_objectDetailID']                                       # the _id in the detail-collection ( main-data of the item )

            self.log.w2lgDvlp("ItmMngr -> loadItem called with  " + itemBaseID.ToString() + " of type : " + objTyp.ToString() + ' ;  Detail_ID = ' + objDtlId.ToString() )

            self.detailHndlr = self.objTypeSwitch[ self.objectTypes[objTyp] ]()     # select the needed type-class
            self.detailHndlr.loadItem(objDtlId)                                     # load the details in the special-item-class
            self.data.update( self.detailHndlr.data )                       
            
            for col in self.itemTbl.Columns:                                        # add maintenance-data from cached collection item.base
                self.data.Add(col, row[col])

            return self.data

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # saveItem stores a given item into the data-base AND the cache
    #
    # HINT : By object-Type we define what kind of data should be saved. the rest comes from the UI over self.Page
    #
    # parameter : objectType        = string defines what type of data will be saved ('comment' or 'announce' for example)
    #
    #             rootElemID        = if the item that should be saved is a "satelite"-element, that depends on a root-elemet here the 
    #                                 mongo-ID of the root-element is saved. will be stored as reference for every chain-item
    #
    #             parentID          = If we have a "follower" in a chain to save the mongo_id of the fore-runner is given as parameter 
    #                                 the parent-item will be updated with a new "_followerID" 
    #                                 and this id will be storeed as _parentID in thsi new item itself
    #
    # 21.12.2012   - bervie-      initial realese
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def saveItem( self, objectType, rootElemID = None, parentID = None ):
        try:
            self.detailHndlr = self.objTypeSwitch[ objectType.ToString() ]()     # select the needed type-class
            return self.detailHndlr.saveItem( objectType, rootElemID, parentID )
            
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # deleteItem : deletes a single satelite-object or a root-element with all dependencies
    #
    # parameter : objectID :     item.base-_id of the item to delete
    #
    # 21.12.2012   - bervie-      initial realese
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def deleteItem(self, itemBaseID ):
        try:
            self.detailHndlr = self.objTypeSwitch[ self.objectTypes[objTyp] ]()     # select the needed type-class
            return self.detailHndlr.deleteItem(objDtlId)

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # func. setNewFollowerId :  set the follower-ID in the currently last chain-item 
    #
    # parameter : parentId       :       id of parent that will be updated 
    #             newChainItmId  :       id of the added item that just before was created
    #
    # 02.12.2012   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def setNewFollowerId(self, parentId, newFollowerId):
        try:
            # add the new follower to the database
            updt = {}
            updt.update({'collection':'item.base'  })
            updt.update({'slctVal': parentId       })
            updt.update({'updatKey':'_followerID'  })
            updt.update({'updatVal': newFollowerId })
            updtDocId = self.updateDoc(updt)

            # add the new follower to the cached data-table
            row = self.itemTbl.Rows.Find( parentId )
            row['_followerID'] = newFollowerId.ToString()

            self.log.w2lgDvlp("UpdateParentFollower : baseItem " + parentId.ToString() + " has a new follower : " + newFollowerId.ToString() )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # func. getLastInChain :  get the last element in a thread
    #
    # parameter : headerId       :       id of parent that will be updated 
    #
    # 28.12.2012   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def getLastInChain(self, headerId ):
        try:
            # if no chain-element in the sequence we have to update the header_follower itself
            row = self.itemTbl.Rows.Find( headerId )
            if row['_followerID'] == System.String.Empty :
                return row

            # get the last item in the sequence 
            while( row['_followerID'] != System.String.Empty ):
                row = self.itemTbl.Rows.Find( row['_followerID'] )
                self.log.w2lgDvlp('class ItemMngr( ItemBase )->getLastInChain   NEXT ITEM :' + row['_id'] )

            return row

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # getChain :  get the ids of a given thread
    #
    # parameter : headerId       :       id of parent that will be updated 
    #
    # returns   : array          : all item.base._id's that are in the thread
    #
    # 28.12.2012   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def getChain(self, headerId ):
        try:
            chainList = [] 
            chainList.Add(headerId)

            # if no chain-element in the sequence we have to update the header_follower itself
            row = self.itemTbl.Rows.Find( headerId )
            if row['_followerID'] == System.String.Empty :
                return chainList

            # get the last item in the sequence 
            while( row['_followerID'] != System.String.Empty ):
                row = self.itemTbl.Rows.Find( row['_followerID'] )
                chainList.Add(row['_id'])

            return chainList

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # getHtmlOfThread( ... )  :   render the HTML of a thread  for writing it to the HTML-outstream
    #
    # parameter : headerId       : ID of header of chain-thread
    #
    # returns   : HTML           : The header-element for the comments. this will be the root for the comments
    #
    # 21.12.2012   - bervie-      initial realese
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def getHtmlOfThread( self, headerId ):
        try:
            chain = self.getChain(headerId)
            buffer = System.Text.StringBuilder()
            idx = 0
            for itm in chain:
                if idx == 0:
                    # special-case : 0 is Header : must get HTML of root-element-detail-data
                    header = self.itemTbl.Rows.Find( itm.ToString() )
                    headerType = self.objectTypes[ header['objectType'] ]
                    rootType = self.HeaderOfRoot[headerType]
                   
                    search = self.appCch.dtVwRootElem.FindRows( header['_rootElemGUID'] )               # all rows that depend on the given ROOT_ELEM

                    root = None                                                                         # search the  comment-header
                    for row in search:
                        searchType = self.objectTypes[ row['objectType'] ]
                        if  rootType == searchType:
                            root = row

                    if root is None:
                        self.log.w2lgDvlp("ItmMngr.getHtmlOfThread : no root_item found !" )
                        return

                    objDtlId = root['_objectDetailID']                                                  # _id in the detail-data-column
                    collection = self.typeToColl[ root['objectType'] ]        # what detail-data-col should be accessed

                    ctrlDict = {'collection':collection,'slctVal': objDtlId }
                    self.readDoc(ctrlDict)

                    data = ctrlDict['data']
                    buffer.Append( '<div class="well"><div class="row"><div class="span10">' )
                    if 'heading'in data:
                        buffer.Append( "<h3>" +  data['heading'].ToString() + "</h3>")
                    buffer.Append( data['body'].ToString() )
                    buffer.Append( '</div></div></div>' )
                else:
                    # get html-detail-data for a chain-link-element
                    chainlink = self.itemTbl.Rows.Find( itm.ToString() )

                    objDtlId = chainlink['_objectDetailID']                                             # _id in the detail-data-column
                    collection = self.typeToColl[ chainlink['objectType'] ]     # what detail-data-col should be accessed

                    ctrlDict = {'collection':collection,'slctVal': objDtlId }
                    self.readDoc(ctrlDict)
                    data = ctrlDict['data']
                    buffer.Append( '<div class="well"><div class="row"><div class="span10">' )
                    if 'heading'in data:
                        buffer.Append( "<h3>" +  data['heading'].ToString() + "</h3>")
                    buffer.Append( data['body'].ToString() )
                    buffer.Append( '</div></div></div>' )
                idx += 1

            return buffer.ToString()

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # displayItem :  display the details-data by a given element_id
    #
    # parameter : rootElementId       :       id of parent that will be updated 
    #
    # 31.12.2012   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def displayItem( self, rootElementId ):
        try:
            buffer = System.Text.StringBuilder()

            root = self.itemTbl.Rows.Find( rootElementId )

            rootType   = root['objectType']
            detailId   = root['_objectDetailID']
            detailColl = self.typeToColl[rootType]
            ctrlDict   = {'collection':detailColl,'slctVal': detailId }
            self.readDoc(ctrlDict)

            data = ctrlDict['data']
            buffer.Append( '<div class="well"><div class="row"><div class="span10">' )
            if 'heading'in data:
                buffer.Append( "<h3>" +  data['heading'].ToString() + "</h3>")
            buffer.Append( data['body'].ToString() )
            buffer.Append( '</div></div></div>' )

            return buffer.ToString()
                   

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())





# # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # #
# # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # #
# # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # #
# # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # #


# from srvcs.ctrl_ItemClasses import *

class Item_JOB_ROOT( ItemBase ) : 
    ''' 
    Class for managing a job_offer ( a request for some help from the neighbours )


    '''

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # constructor. save;load and display offers
    #
    #
    # parameter : Page :        reference to current webpage
    #             objType :     Type of object that will be handeled
    #
    #
    # 21.12.2012   - bervie-      initial realese
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def __init__(self, page):
        try:
            self.objType = 'JOB_ROOT'
            ItemBase.__init__(self, page )
            self.log.w2lgDvlp("Item_JOB_ROOT.__init__  called " )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # load job by given objectID 
    #
    # parameter : objectDetailID :   ID of dataobject in the detail-collection
    #
    # returns string with the data to be rendered (HTML-code)
    #
    #
    # 21.12.2012   - bervie-      initial realese
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def loadItem( self, objectDetailID ):
        try:
            ctrlDict = {'collection':'item.JOB_ROOT','slctVal':objectDetailID }
            self.readDoc(ctrlDict)
            self.data = ctrlDict['data']

            # generate HTML output for rendering to the webform
            html = System.Text.StringBuilder()
            html.Append( '<h2>' )
            html.Append( self.data['heading'].ToString() )
            html.Append( '</h2>' )
            html.Append( self.data['body'].ToString() )
            html.Append( '<hr/><br/>' )
            
            self.data['html'] = html.ToString()

            return self.data

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # saveItem()   an announce stored to the mongo-db and the item-cache
    # 
    # parameter:
    #  
    # objectType : what kind of data should be saved
    #
    # rootElemID : root_element is None for saving a root_element
    #
    # parentID   : no forerunner available for an root-element means we have a None here
    #
    #
    # 17.11.2012   - bervie-      initial realese
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def saveItem( self, objectType, rootElemID = None, parentID = None ):
        try:
            # get input from webform
            heading = self.ui.getCtrl('txbHeader').Text[:200]
            body = self.ui.getCtrl('txtMain').Text 

            slctLocation = self.ui.getCtrl('sel_lctn').SelectedValue.ToString()
            if slctLocation == -1: slctLocation = None

            slctType = self.ui.getCtrl('sel_type').SelectedItem.Text
            if slctType == -1: slctType = None

            input = heading + ' ' + body
            # add the selected announce-type from the selection to the string as normal tag 
            if slctType != None:
                input += ' #' + slctType
            
            #self.log.w2lgDvlp('!!  self.getHashTags(input) !!' + input )
            self.getHashTags(input)     # write stuff into self.tagList
            
            # write the data to the mongo-db detail table 
            itemData = {}
            itemData['heading'] = heading
            itemData['body'] = body

            storeDataDct = {'collection':'item.JOB_ROOT','slctKey':None,'data': itemData}
            self.newObjId = self.insertDoc(storeDataDct)

            guid = System.Guid.NewGuid().ToString('N')                  # we have a new announce which needs a GUID
            parentId = System.DBNull.Value                              # root elemnts never have parents !
            followerId = System.DBNull.Value                            # will be updated with first item_id in the chain
    
            # save data to the cache and the item.base collection
            self.lstInsertedId = self.storeGeneralBase( self.objType, self.newObjId, guid, heading, body, parentId, followerId, slctLocation, self.tagList )
            return self.lstInsertedId

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())













tool = Item_JOB_ROOT( Page )

# ------------------------------------------------------------------------------------------------------------------------------------------------##__aspn.net ------------------------------------------------
# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 18.03.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    try:
        if( not Page.IsPostBack ):
            # user must be logged in
            tool.usrDt.checkUserRigths( Page, 'free' )

            # fill locations-dropdown
            locations = tool.usrDt.getItem('cities')
            # tool.log.w2lgDvlp( ' Location for dropdown : ' + unicode(locations) )
            selLocations = tool.ui.getCtrl('sel_lctn')
            tool.fillUserLocations( selLocations, locations )

            # fill the job-type-dropdown
            selTypeOfJob = tool.ui.getCtrl('sel_type')
            tool.fillJobTypes(selTypeOfJob, 'DE')

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ------------------------------------------------------------------------------------------------------------------------------------------------##__handler ------------------------------------------------
# ***********************************************************************************************************************************************
# usrLoggedIn      : called after user succesfully logged in
#
# 18.11.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def HndlrButtonClick(sender, e):
    try:
        urlNext = None

        if sender.ID == 'btnSave':
            newId = tool.saveItem('JOB_ROOT')
            urlNext = Page.ResolveUrl(WebConfigurationManager.AppSettings['ViewDetailForm']) + '?item=' + unicode( newId )

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())

    if urlNext != None :
        Response.Redirect(urlNext)

