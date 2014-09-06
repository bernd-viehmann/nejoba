# *********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
# Item.py :    base-class for all data-objects. 
#              the class stores maintenance-stuff of an object in item.base and the AppCache
#              the db-operating functions are overwritten in the inheritance-classes
# 
# ***********************************************************************************************************************************************
#  24.11.2012  - bervie -     initial realese
# *********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
import clr
clr.AddReference('MongoDB.Bson')
clr.AddReference('MongoDB.Driver')
from MongoDB.Bson import *
from MongoDB.Driver import *
from System.Web.Configuration import *
from System.Web import HttpUtility
import System.Text
import traceback            # for better exception understanding
import System.Guid
import re

import mongoDbMgr                       # father : the acces to the database


class Item ( mongoDbMgr.mongoMgr ):
    '''
    Item is the base-class for working with all data-entities in nejoba. 
    For every data-type there is a child that derives the always needed basefunctions :-)
    '''

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # constructor. 
    #
    #
    # 16.01.2013   - bervie -       initial realese
    # 30.01.2013   - bervie -       added self.OfferorGuid 
    #                               the member will store the GUID of the offeror. this hack is needed to find the correct header if the 
    #                               client adds a message in job_trial_editor. 
    #                               the function chainGetHeader will search the header of the offeror instead of creating a new header for the 
    #                               client
    #
    #
    #
    #
    #
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def __init__(self, page ):
        try:
            mongoDbMgr.mongoMgr.__init__(self, page )                   # wake up papa ; mother njbTools is included by inheritance!

            self.itemTbl     = self.appCch.dtSt.Tables["items"]         # cached item-base table
            self.itemTagsTbl = self.appCch.dtSt.Tables["itemTags"]      # cached tag-table

            self.objTypIdx      = None                                  # index of the object-type

            self.typeToColl = {    0  : 'item.JOB_ROOT' ,               # depending on the objectTypeId this dict defines what mongo-collection is used for the detail-data
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

            self.setMembrAttrb()                                        # set members that are used to write to item.base collection

            self.locName = None                                         # added 24.02.2013 if no location is available a None will switch to user-location

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # set members. outside of constructor function is called for a reset of the instance
    #
    #
    # 16.01.2013   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def setMembrAttrb( self ):
        try:
            # data used for storing data to the item.base-collection
            self.objectDetailID  = None                         # the monog-id of the data in the detail-collection
            self.rootElemGUID    = None                         # if needed the GUID of the fathe-element ths this element dependce of
            self.headline        = None                         # subject-text
            self.bodymsg         = None                         # main-description-text
            self.parentID        = None                         # the parent [ if needed ]
            self.followerID      = None                         # the aftercomer
            self.locationID      = None                         # what place this item belongs to?
            self.taggingLabels   = None                         # array of the hashtags
            self.timeFrom        = System.DateTime.MinValue     # starting-date or the point-in-time the item is valid   : DateTime-Item
            self.timeTo          = System.DateTime.MinValue     # end-time :                                               DateTime-Item
            #self.timeFrom        = System.DBNull.Value  # starting-date or the point-in-time the item is valid   : DateTime-Item
            #self.timeTo          = System.DBNull.Value  # end-time :                                               DateTime-Item

            # added 21.06.2013 bervie attributes used for the map
            self.tagZero         = None                 # the first Tag is stored in the cache to define which makcer-icon will be used
            self.lat             = None                 # geo-coordinate latitude
            self.lon             = None                 # geo-coordinate longitude

            self.data       = {}                        # will contain the detail-data and the maintenance-things from item.base-collection

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    #
    # base-methods. not overloaded
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # storeBase()   write the base-data of a new object into base-itme-collection and cached table in the webserver
    # 
    #   parameter   are set as class-member-attributes
    # 
    #       objectType	                -int-               type identifier
    #       _objectDetailID	            -mongo_id-          mongoID of the data-item represented by this item
    #       _rootElemGUID	            -string-            GUID of an root_elem must be created outside - OR - the GUID of an existing root-objct the current item belongs to
    # 
    #        headline                    -string-            the headline of the object  HINT: Only added to cached data-table. in db we have an extra-object
    #        bodymsg                     -string-            the body-message
    # 
    #        _parentID	                -mongo_id-          forerunner of this object
    #        _followerID	            -mongo-id-          follower of this object
    # 
    #        _locationID	            -mongo_id-          location if the item 
    #        taggingLabels	            -string-array-      taggs for the job
    #        from	                    -DateTime-          when will action be started
    #        till	                    -Datetime-          when will action end
    #
    #   created internal :
    #
    #        _hostGUID	                -string-            GIUD of server hosting this item
    #        _creatorGUID	            -string-            GUID of the creator of this object
    #        creationTime	            -DateTime-          time the item was created in UTC
    #
    #
    # 17.11.2012   - bervie-      initial realese
    # 23.03.2013   - bervie-      replaced the "just-in-time" save to the DataTabe by a save to the TaggContainer-class
    # 21.06.2013   - bervie-      added attributes used for the map. coordinates and firsat tag to select the marker needed for this item
    # 13.08.2013   - bervie-      changed insertion from add to insertAt(row,0). the new added rows should be shown as last item in the map or list
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def storeGeneralBase( self ):
        try:
            creationDate    = System.DateTime.UtcNow                            # UTC time used for timestamps
            creatorGUID     = self.usrDt.getItem('GUID')                        # get the ID of the working user
            creatorNick     = self.usrDt.getItem('nickname')                    # the nickname the user has choosen
            locationName    = self.getLocationName()                            # for root-objects the selected location in the 
            hostGUID        = self.strngSeperator = WebConfigurationManager.AppSettings['serverHostName']       # a unique ID for the server

            # 1. write the data to the mongo-db
            # made db-internal baseData['_ID'] = ''
            baseData = {}
            baseData['objectType']         = self.objTypIdx                 
            baseData['_objectDetailID']    = self.objectDetailID
            baseData['_hostGUID']          = hostGUID                  
            baseData['_rootElemGUID']      = self.rootElemGUID
            baseData['_parentID']          = self.parentID
            baseData['_followerID']        = self.followerID
            baseData['_creatorGUID']       = creatorGUID               
            baseData['creationTime']       = creationDate
            baseData['_locationID']        = self.locationID
            baseData['taggingLabels']      = self.taggingLabels
            baseData['from']               = self.timeFrom
            baseData['till']               = self.timeTo
            # 14.02.2013 -bervie- added additional infos to the table
            baseData['nickname']           = creatorNick
            baseData['locationname']       = locationName
            # 21.06.2013 -bervie- added attributes used for the map
            baseData['tagZero']            = self.tagZero
            baseData['lat']                = self.lat
            baseData['lon']                = self.lon

            storeDataDct = {'collection':'item.base','slctKey':None,'data': baseData}
            newObjId = self.insertDoc(storeDataDct)

            # 2. add the inserted data also to cached data-table (except TaggingLables, which are an special-case)
            newRow = self.itemTbl.NewRow();


            unitimeTill = self.timeTo.ToUniversalTime()
            newRow['_ID']                   = newObjId
            newRow['objectType']            = self.objTypIdx
            newRow['_objectDetailID']       = self.emptyIfNull( self.objectDetailID )
            newRow['_hostGUID']             = hostGUID                  
            newRow['_rootElemGUID']         = self.rootElemGUID
            newRow['_parentID']             = self.emptyIfNull( self.parentID   )
            newRow['_followerID']           = self.emptyIfNull( self.followerID )
            newRow['_creatorGUID']          = creatorGUID
            newRow['creationTime']          = creationDate
            newRow['_locationID']           = self.emptyIfNull( self.locationID )

            # 09.09.2013 bervie --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  
            #newRow['from']                  = self.timeFrom
            #newRow['till']                  = self.timeTo
            # insert universal time in the cache
            if self.timeFrom != System.DateTime.MinValue:
                unitimeFrom = self.timeFrom.ToUniversalTime()
            else:
                unitimeFrom = System.DateTime.MinValue

            if self.timeTo != System.DateTime.MinValue:
                unitimeTill = self.timeTo.ToUniversalTime()
            else:
                unitimeTill = System.DateTime.MinValue
            newRow['from']                  = unitimeFrom
            newRow['till']                  = unitimeTill
            # 09.09.2013 bervie --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  

            # 14.02.2013 -bervie- added additional infos to the table
            newRow['nickname']              = creatorNick
            newRow['locationname']          = locationName
            # 21.06.2013 -bervie- added attributes used for the map
            newRow['tagZero']               = self.tagZero
            newRow['lat']                   = self.lat
            newRow['lon']                   = self.lon

            # add the headline and part of the body-text to the cached data-table also. will be displayed in list-view of location
            if self.headline : newRow['subject']  = self.appCch.RemoveHtml(self.headline.ToString()).strip()[:140]
            if self.bodymsg  : newRow['body']     = self.appCch.RemoveHtml(self.bodymsg.ToString()).strip()[:300]

            # 20.08.2013 bervie 
            # to have a valid JSON-object when retriving objects from the items-cache we have to remove "
            if newRow['subject'] != System.DBNull.Value: newRow['subject']   = newRow['subject'].replace( '"' , "'" )
            if newRow['body'] != System.DBNull.Value:    newRow['body']      = newRow['body'].replace( '"' , "'" )
            
            #
            # insert rows at the beginning to be shown as first items in the list.
            # 13.08.2013  bervie
            #
            #self.itemTbl.Rows.InsertAt(newRow,0)

            self.itemTbl.Rows.Add(newRow)

            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
            #
            # 3. write tagging-lables to the extra Tagging-DataTable in the cache
            #
            # decapitated : we are using the TaggContainer-class instead of the data-table
            #
            #self.log.w2lgDvlp("ctrl_ItemBase->storeGeneralBase : type of tagging-lables  " + str( type( self.taggingLabels ) ) ) 
            #if self.taggingLabels  :
            #    for tag in self.taggingLabels :
            #        newRow = self.itemTagsTbl.NewRow();
            #        newRow['_ID']          = newObjId               # the mongo_id of the item this tag belongs to
            #        newRow['_locationID']  = self.locationID        # the _id of the location
            #        newRow['tag']          = tag                    # the tag
            #        self.itemTagsTbl.Rows.Add(newRow)
            #
            #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

            # 23.03.2013   - bervie-      replaced the "just-in-time" save to the DataTabe by a save to the TaggContainer-class ---------------------------------
            # 3. add the taggs to the tagging-container-class
            #
            #
            self.log.w2lgDvlp("ctrl_ItemBase->storeGeneralBase : type of tagging-lables  " + str( type( self.taggingLabels ) ) ) 
            if self.taggingLabels  :
                for tag in self.taggingLabels :
                    self.taggs.storeTagg( tag, self.locationID, newObjId )
                    # newObjId         = the mongo_id of the item this tag belongs to
                    # self.locationID  = the _id of the location
                    # tag              = the tag
            # ---------------------------------------------------------------------------------------------------------------------------------------------------

            # 4. return newly created id to the caller
            self.log.w2lgDvlp("Item->storeGeneralBase : object id of item inserted into item.base : " + str(newObjId) ) 
            return newObjId

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # getLocationName : if a root-object is saved we use the text from the drop-down-box as location-name
    #                   if it is only a message then the location-name of the user willo be used
    #
    # param         : the object-type as string
    # returns       : the index-id of  the object-type as integer
    #
    # 16.01.2013   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def getLocationName( self ):
        try:
            if self.locName :
                self.log.w2lgDvlp("Item->storeGeneralBase : drop-down-text used for location-name        : " + self.locName) 
                return self.locName
            else:
                self.log.w2lgDvlp("Item->storeGeneralBase : using user-home-location for location-name   : " + self.usrDt.getItem('locationname').ToString() ) 
                return self.usrDt.getItem('locationname').ToString()

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # getObjectTypeId : convert the object-type-name  from sting to integer. int is used in the db
    #
    # param         : the object-type as string
    # returns       : the index-id of  the object-type as integer
    #
    # 16.01.2013   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def getObjectTypeId(self, objTypeString ):
        try:
            strngSeperator      = WebConfigurationManager.AppSettings['stringSeperator']            # define the seperator
            objTypConf          = WebConfigurationManager.AppSettings['objectTypes']                # definition of the object-types as string
            objectTypes         = objTypConf.split(strngSeperator)                                  # available item-types stored in an array

            return objectTypes.index( objTypeString )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # getObjctTypeString : convert the object-type-id from integer to string. makes source-code readable
    #
    # param         : the object-type as integer used in DB and Item-Cache 
    # returns       : the name of  the object-type as string
    #
    # 16.01.2013   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def getObjectTypeString(self, objTypeId ):
        try:
            strngSeperator      = WebConfigurationManager.AppSettings['stringSeperator']            # define the seperator
            objTypConf          = WebConfigurationManager.AppSettings['objectTypes']                # definition of the object-types as string
            objectTypes         = objTypConf.split(strngSeperator)                                  # available item-types stored in an array

            return objectTypes[objTypeId]

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())










    # ***********************************************************************************************************************************************
    # getHashTags      : find all strings that beginns with a # : they will be used as tag for the annoncments
    #                    using regular-expressions from the python re module
    #
    #                    returns array with the hashtags from input
    #
    # 18.11.2012  - bervie -     initial realese
    # 14.04.2013  - bervie -     remove '&nbsp;' from hashtaggs
    #
    # ***********************************************************************************************************************************************
    def getHashTags(self, textLoad):
        try:
            textToCheck = HttpUtility.HtmlDecode(textLoad)

            self.log.w2lgDvlp('Item.getHashTags() called')
            pncttnMrk = [',','.','!','?',';',':','"',"'"]                           # define punctuation marks that will be removed
            lstOfTags = re.findall("[#]{1}[^ \t\n\r\f\v<]*", textToCheck, re.U)     # get given hashtags by a regular expression query
            preFltrTags = list()                                                    # get the given hashtags not seperated by a whitespace from each other
            for rawTag in lstOfTags:
                self.log.w2lgDvlp('Item.getHashTags()  raw-tag found by regular expression : ' + unicode(rawTag) )
                if rawTag.count('#') > 1:                                           # split more than one hashtags written without sepperation
                    preFltrTags = preFltrTags + rawTag.split('#')
                    addngHshTg = list()                                             # add the '#' again after calling split('#')
                    for checkerChan in preFltrTags:
                        if len(checkerChan.strip()) > 0:
                            addngHshTg.Add( '#' + checkerChan )
                    preFltrTags = list(addngHshTg)
                else:
                    preFltrTags.Add(rawTag)
            lstOfTags = list(preFltrTags)
            # remove comma and filter '<' or '>' (migth be a HTML-tag)
            preFltrTags = list()
            for rawTag in lstOfTags:
                tag = unicode(rawTag[1:20].lower())                                 # commas are used to sepperate tags
                for marker in pncttnMrk:
                    if marker in tag:
                        tag = tag[:tag.find(marker)]                                # cut string at punctuation-marks 
                tag = tag.replace('&nbsp;','')                                      # 14.04.2013 - remove non-braking-space <http://www.sightspecific.com/~mosh/www_faq/nbsp.html> - - - - 
                #tag = HttpUtility.HtmlDecode( tag )                                 # 19.04.2013  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                if( tag.count('<') == 0 ) and ( tag.count('>') == 0 ) and ( tag.count('&') == 0 ):
                    if tag.count('#') > 0:
                        preFltrTags = preFltrTags + tag.split('#')
                    else:
                        preFltrTags.Add(tag)
            tagList = list()
            for tag in preFltrTags:
                if len( tag ) > 0 :
                    if (tag not in tagList):
                        tagList.Add(tag.strip())
                        self.log.w2lgDvlp('Item.getHashTags()  tag found and will be added : ' + unicode(tag) )
            # if no taggs were defined we do not have to add anything
            if len(tagList) == 0:
                tagList = None;
                return []

            return tagList[:5]

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())
    #def getHashTags(self, textToCheck):
    #    try:
    #        self.log.w2lgDvlp('!!  --  texttocheck --  !!' + textToCheck )
    #        lstOfTags = re.findall("[#]{1}[^ \t\n\r\f\v<]*", textToCheck, re.U)
    #        # print all tags found to the nejoba log
    #        tagList = []
    #        for tag in lstOfTags:
    #            item = tag[1:26].lower()
    #            item = item.replace('&nbsp;','')            # 14.04.2013 - remove non-braking-space <http://www.sightspecific.com/~mosh/www_faq/nbsp.html> - - - - 
    #            item = HttpUtility.HtmlDecode( item )       # 19.04.2013  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #            self.log.w2lgDvlp('!!  --  found tag before adding --  !!' + item )
    #            if len( item ) > 0 :
    #                if (item not in tagList):
    #                    tagList.Add(item)
    #        # debug
    #        #for item in self.tagList:
    #        #    self.log.w2lgDvlp('!!  --  found tag  --  !!' + item )
    #        # if no taggs were defined we do not have to add anything
    #        if len(tagList) == 0:
    #            tagList = None;
    #        return tagList
    #    except Exception,e:
    #        self.log.w2lgError(traceback.format_exc())








    # ***********************************************************************************************************************************************
    # emptyIfNull      : if System.DBNull.Value has to be inserted for an ID this function converts it to an empty string 
    #
    # 22.13.2012  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def emptyIfNull(self, txtToChck):
        try:
            if not txtToChck:
                return System.String.Empty
            elif txtToChck == System.DBNull.Value:
                return System.String.Empty
            
            return unicode(txtToChck)

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    #
    # deleting-functions  . normally there is  no need to overload this guys
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # delete     : function initialy starts the delete of a job-offer with all depending objects or a offer-thread offered from a service provider
    #              the function is always called with the root-item row. if a thread created from a different user has to be deleted the 
    #              headerCreatorGuid
    #
    #
    #
    # parameter : baseRow        : row from item-table with the JOB_ROOT Element
    #             headerTypeName : what kind of header should be delted   
    #             creatorGuid    : who created the header ( used for differnt logged-in user 
    #                              like job-offer-creator deltes an offer comig from a different user
    #
    # 09.02.2013   - bervie-      initial realese
    # 10.02.2013   - bervie-      changed parameter signature
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def delete( self, baseRow, headerTypeName = None, headCreatorGuid = None ):
        try:
            mongoId             = baseRow['_ID']                    # mongo_id of current baseItem

            rootCreatorGuid     = baseRow['_creatorGUID']           # human that was the creator of the object
            userGuid            = self.usrDt.getItem('GUID')        # get USER GUID 

            objTypeId   = baseRow['objectType']             # get objectType 
            objectType  = self.typeToColl[objTypeId]        # the object-type as string

            self.log.w2lgDvlp( 'Item.delete called for ItemBaseElement  ' + mongoId.ToString() + ' ! It is a ' + objectType )

            if not headCreatorGuid:
                self.rootDelete( baseRow )        # delete a complete job-offer with all dependencies
            else :
                # get the header
                self.chainDelete( baseRow, headerTypeName, headCreatorGuid )            # delete a offer-thread for 

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # deleteChain : deletes a chain with header by given header_id. root_elem will survive. used to delete an offer from a service-provider
    #
    # parameter : itemBaseRow :     item.base-row with the root-element of the header-item
    #             threadType :      what object-type has the header. given as string 
    #             creatorGUID :     GUID of the creator of the header 
    #
    #
    #
    #
    # 19.01.2013   - bervie-      initial realese
    # 10.02.2013   - bervie-      reworked with type and chain-element
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def chainDelete(self, itemBaseRow , threadType, creatorGUID):
        try:
            # 1. create a list with all rows that should be deleted
            rowsToDelete = []           
            
            headerRow   = self.chainGetHeader( itemBaseRow['_ID'].ToString(), threadType, creatorGUID )
            # self.log.w2lgDvlp( 'Item.deleteChain header_ID     : ' + headerRow['_ID'].ToString() )
            # self.log.w2lgDvlp( 'Item.deleteChain header_Type   : ' + self.getObjectTypeString( headerRow['objectType'] ) )
            rowsToDelete.Add( headerRow )

            rowsInChain = self.chainGetIDs( itemBaseRow['_ID'].ToString(), threadType, creatorGUID )
            rowsToDelete.extend(rowsInChain[1:])

            for item in rowsToDelete:
                objTypeName = self.getObjectTypeString( System.Convert.ToInt32(item['objectType'] ) )
                # self.log.w2lgDvlp( 'Item.deleteChain item_ID     : ' + item['_ID'].ToString() + ' objectType  : ' + objTypeName )

            # 2. delete the detail-data in the data-specific collections
            self.chainDeleteDetails( rowsToDelete )

            # 3. delte the data in item.base 
            self.chainDeleteBase( rowsToDelete )

            # 4. remove the items in the cache
            self.chainDeleteCache( rowsToDelete )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # chainDeleteDetails : delete the rows in the mongo-collections for the detail-data
    #
    # parameter : rowsToDelete :     list with all rows that should  be deleted
    #
    # 10.02.2013   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def chainDeleteDetails( self, rowsToDelete ):
        try:
            for row in rowsToDelete:
                mongoID     = row['_objectDetailID'].ToString()
                objType     = row['objectType']
                objTypName  = self.getObjectTypeString( objType ) 

                collection = 'item.' + objTypName

                delet = {}
                delet.update({'collection':collection})
                delet.update({'slctVal':mongoID.ToString()})
                deletedId = self.delDoc(delet)
                self.log.w2lgDvlp( 'Item.chainDeleteDetails header_ID of item just deleted in ' + collection + '  __objectDetailID : ' + deletedId )


        except Exception,e:
            self.log.w2lgError(traceback.format_exc())

 

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # chainDeleteBase : delete the rows in the base.item-collection
    #
    # parameter : rowsToDelete :     list with all rows that should  be deleted
    #
    # 10.02.2013   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def chainDeleteBase( self, rowsToDelete ):
        try:
            for row in rowsToDelete:
                mongoID     = row['_ID'].ToString()
                collection = 'item.base'

                delet = {}
                delet.update({'collection':collection})
                delet.update({'slctVal':mongoID.ToString()})
                deletedId = self.delDoc(delet)
                self.log.w2lgDvlp( 'Item.chainDeleteBase header_ID of item just deleted in item.base   _ID : ' + deletedId )


        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # chainDeleteCache : delete the rows in the cache-table 
    #
    # parameter : rowsToDelete :     list with all rows that should  be deleted
    #
    # 10.02.2013   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def chainDeleteCache( self, rowsToDelete ):
        try:
            # delete items in tag-rows
            builder = System.Text.StringBuilder()
            builder.Append("_ID in ('")

            for rw in rowsToDelete:
                builder.Append( rw['_ID'].ToString() )
                builder.Append( "','" )


            # hint : 
            # the deletition of tags makes no scense for message-threads, because the taggs are set only for 
            # the root-element which is not deleted here.
            # so remember to implement it when deleteing root-elems !!
            query = builder.ToString()[:-2] + ")"
            self.log.w2lgDvlp( 'Item.chainDeleteCache query for ItemTags-delete: ' + query )
            tagsToDelete = self.itemTagsTbl.Select(query)
            
            for tag in tagsToDelete: 
                self.log.w2lgDvlp( 'Item.chainDeleteCache query tag will be delteted : ' + tag['_ID'].ToString() )
                tag.Delete()

            for item in rowsToDelete: 
                self.log.w2lgDvlp( 'Item.chainDeleteCache query item will be delteted : ' + item['_ID'].ToString() )
                item.Delete()

            # apply changes in the cache with  AcceptChanges()
            self.itemTbl.AcceptChanges()
            self.itemTagsTbl.AcceptChanges()

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())






    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # rootDelete : deletes a JOB_ROOT Item and all depending HEADERS and MESSAGES
    #
    # parameter : itemBaseRow :     item.base-_id of the item to delete
    #
    # 19.01.2013   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def rootDelete(self, itemBaseRow ):
        try:
            # delte in base-class Item :
            self.log.w2lgDvlp( 'Item.rootDelete called with ItemBaseId  : ' + itemBaseRow['_ID'].ToString() )

            # 1. get all depending objects
            #    currently we only delete JOB_ROOT elements. so we search here only for JOB_HEADERS
            headerParent    = itemBaseRow['_ID']
            objectType      = str(self.getObjectTypeId('JOB_HEADER'))

            query = "_parentID = '" + headerParent + "' AND objectType = " + objectType
            self.log.w2lgDvlp( 'Item.rootDelete query to get headers    : ' + query )

            headerRows =  self.itemTbl.Select(query)

            # 2. delete offer-threads found for JOB_ROOT element
            for row in headerRows:
                self.log.w2lgDvlp( 'Item.rootDelete _ID of header to be deleted                 : ' + row['_ID'].ToString() )
                self.log.w2lgDvlp( 'Item.rootDelete ojectType of header to be deleted           : ' + self.getObjectTypeString(row['objectType']) )
                self.log.w2lgDvlp( 'Item.rootDelete query to get headers                        : ' + row['_creatorGUID'].ToString() )

                self.chainDelete( itemBaseRow, 'JOB_HEADER', row['_creatorGUID'].ToString() )            

            # 3. delete the root-object and the tags in cache and mongodb 
            dummyList = [itemBaseRow]
            self.chainDeleteDetails( dummyList )
            self.chainDeleteBase( dummyList )
            self.chainDeleteCache( dummyList )

            # 2. delete all objects depending on the ncurrent root-element
            #    they are identified by "parentID == mongoID of root" and "object-type == JOB_HEADER
            #    we get the creator-GUIDS from them and deletet the chains



            # 3. delete the JOB_ROOT objects 
            #    ( remeber: do not forgwet to delete the tag-items in the cache also !!)




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
    #         this implmnt in base-class can be used for root-objects. if not : OVERLOAD
    #
    #         the loader-functions copy the loaded data into the member-attribute data{}
    #         the dict contains the item-base data and the HTML-stuff loaded in the detail-loader 
    #
    # parameter : itemBaseID  :    _id in item.base 
    # return    : html        :    formatet HTML with header as <h2> and body-data
    #
    # loaded data is also saved in the data{}-member
    #
    # 16.01.2012   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def load( self, itemBaseRow ):
        try:
            self.log.w2lgDvlp("Item.load called for ItemBaseId  " + itemBaseRow['_ID'].ToString() )

            for col in self.itemTbl.Columns:                                                            # add maintenance-data from cached collection item.base to the dict 
                self.data.Add(col, itemBaseRow[col])

            self.loadDetails( itemBaseRow )                                                             # get the detail-data for the requested item
            return 

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # loadDetails :  by given object_type index and object-detail-id the machine loads the detail-data of given item
    # 
    # this function should be overloaded by the specialized deriver classes
    #
    # parameter : objTypIdx         :    the id of the object-type
    #             objDetailId       :    the mongo-id of the item in the detail-data-colection
    #
    # return    : html              :    formatet HTML 
    #
    # 16.01.2012   - bervie-      initial realese
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def loadDetails( self, baseItmRow ):
        try:
            objTypeIdx      = baseItmRow['objectType']
            detailId        = baseItmRow['_objectDetailID']
            sourceCllctn    = self.typeToColl[ int(objTypeIdx)]
            self.log.w2lgDvlp("Item.loadDetails objType = " + str(objTypeIdx) + ' in collection ' + sourceCllctn + ' => detail-data-item-id : ' + detailId )

            ctrlDict = {'collection':sourceCllctn,'slctVal': detailId }
            self.readDoc(ctrlDict)
            self.data = ctrlDict['data']                                            # copy the selected data to the member-attribute data

            # generate HTML output for rendering to the webform
            html = System.Text.StringBuilder()


            #if self.data.has_key('heading'):
            #    html.Append( '<h4>' )
            #    html.Append( self.data['heading'].ToString() )
            #    html.Append( '</h4>' )

            if self.data.has_key('body'):
                html.Append( self.data['body'].ToString() )
                html.Append( '<br/>' )

            # # # # # # # # # 
            #
            # return html
            #
            # CR bervie 08.02.2012
            # before the function returns the StringBuilder. 
            #
            # no it adds detail-data as htnl to the data -dict of the item
            #
            #
            self.data['html'] = html.ToString()
            self.data['nickname'] = baseItmRow['nickname'].ToString()
            self.data['creationTime'] = baseItmRow['creationTime']

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # save()   the function calls the detail-saver, after that it stores the maintenance-data to base.item-collection 
    #          and the session-cached data-table.
    #          having base-functions for root-objects here. for messages, where a header must be created, function should be overwritten
    # 
    # parameter  :  dependsOfID : This is the Mongo_ID of the element that this has a closer relation with
    # returns    :  _id of last inserted into item.base-collection
    #
    # 16.01.2012   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def save( self, dependsOfID = None ):
        try:
            self.setMembrAttrb()        # flush data 

            # 1. save detail-data in the detail-collection
            newDetailId = self.saveDetails()

            # 2. define the values that will be inserted into item.base collection
            self.objectDetailID  = newDetailId      # the monog-id of the data in the detail-collection
            self.rootElemGUID    = System.Guid.NewGuid().ToString('N')      # we have a new announce which needs a GUID

            # 3. write data to the item.base-collection
            baseItemId = self.storeGeneralBase()

            return baseItemId

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # saveDetails : save the details data of a item. we have a default saver here which should be useable with root elements
    #               function will be overwritten by the specialyzed child-classes
    #
    # returns     : newDetailObjId - the ID of the data-item in the detail-collection
    #
    # 17.01.2013   - bervie -   initial realese
    # 23.03.2013   - bervie -   added rubric as first elem in the hashtag-array. it comes from the Page.ViewState['RUBRIC']
    # 21.06.2013   - bervie -   added timestamp for date-search (they will be stored as DateTime !)
    # 16.08.2013   - bervie -   the leading '§' is missing because the string is used for transmitting data to the AJAX-query. changed 
    # 13.09.2013   - bervie -   get the location-data from the textboxes if they exists
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def saveDetails( self ):
        try:
            self.log.w2lgDvlp("ItemDebateRoot.saveDetails called " )
            self.ui.ctrlDict = {}                                       # delete the ctrl-dict            
            self.ui.getCtrlTree( self.Page.Master )                     # reload ctrl-list

            itemData = {}
            if self.ui.ctrlDict.has_key('txbHeader') : itemData['heading']  = self.ui.getCtrl('txbHeader').Text[:200]
            if self.ui.ctrlDict.has_key('txtMain')   : itemData['body']     = self.ui.getCtrl('txtMain').Text

            # 13.09.2013 
            #
            # read the hashtags
            input = System.Text.StringBuilder()
            if itemData.has_key('heading')          : input.Append( self.ui.getCtrl('txbHeader').Text )
            if itemData.has_key('body')             : input.Append( self.ui.getCtrl('txtMain').Text )
            if self.ui.ctrlDict.has_key('txbx_jobType') : input.Append( ' #' + self.ui.getCtrl('txbx_jobType').Text.ToString())

            self.taggingLabels = self.getHashTags( input.ToString() )                        # get tags from the input and create the hashtag-list
            # the textbox for a rubric has NO leading '§'. that would not work with the AJAX-call
            # we add the missing char here for storing it in the database
            if self.ui.ctrlDict.has_key('txbx_tagforitem'):
                rbrcTag = self.ui.getCtrl('txbx_tagforitem').Text.strip('§')
                if( len( rbrcTag ) > 0 ) :
                    self.tagZero = '§' + rbrcTag.strip().upper()
                    if self.taggingLabels is not None:
                        self.taggingLabels.insert(0, self.tagZero)
                    else:
                        self.taggingLabels = [ self.tagZero ]

            # 21.06.2013 add the stuff needed for the map
            if self.ui.ctrlDict.has_key('txbx_lat'):
                geoLat = self.ui.shorterCoordinate(self.ui.getCtrl('txbx_lat').Text.strip())
                geoLon = self.ui.shorterCoordinate(self.ui.getCtrl('txbx_lon').Text.strip())
                self.log.w2lgDvlp("Item.saveDetails : geoLat to store  " + geoLat )
                self.log.w2lgDvlp("Item.saveDetails : geoLon to store  " + geoLon )
                self.lat = geoLat
                self.lon = geoLon

            # -----------------------------------------------------------------------------------------------------------------------------
            # -----------------------------------------------------------------------------------------------------------------------------

            # write the data to the mongo-db detail table 
            dstntn = self.typeToColl[ self.objTypIdx ]
            storeDataDct = {'collection':dstntn , 'slctKey':None , 'data': itemData}
            newObjId = self.insertDoc(storeDataDct)

            # add the detail-data as member-vars. used in Item.store-base-to-mongo 
            self.objectDetailID  = newObjId                                                                     # the monog-id of the data in the detail-collection
            if self.ui.ctrlDict.has_key('txbHeader') : self.headline   = self.ui.getCtrl('txbHeader').Text      # subject-text
            if self.ui.ctrlDict.has_key('txtMain')   : self.bodymsg    = self.ui.getCtrl('txtMain').Text        # main-description-text

            # CR 25.11.2013 bervie end
            if self.ui.ctrlDict.has_key('txbx_location_id') :   self.locationID = self.ui.getCtrl('txbx_location_id').Text       # location-id is now taken from the hidden textbox txbx_location_id : it is sometimes defined via javascript
            if self.ui.ctrlDict.has_key('txbx_location_name') : self.locName    = self.ui.getCtrl('txbx_location_name').Text   # location-name is now taken from the hidden textbox txbx_name : it is sometimes defined via javascript

            # 21.06.2013 bervie added timestamp for date-search (they will be stored as DateTime !)
            # bootstrap timepicker will be added later : <http://jdewit.github.io/bootstrap-timepicker/>
            format = 'dd.MM.yyyy-HH:mm:ss'
            provider = System.Globalization.CultureInfo('de-DE');
            if self.ui.ctrlDict.has_key('txbx_timeFrom'): 
                fromInpt = self.ui.getCtrl('txbx_timeFrom').Text.strip()
                if( len(fromInpt) > 0 ):
                    fromInpt += '-00:00:00'
                    fromDate = System.DateTime.ParseExact( fromInpt, format, provider )
                    self.timeFrom = fromDate

                    if self.ui.ctrlDict.has_key('txbx_timeTo'  ): 
                        toInpt = self.ui.getCtrl('txbx_timeTo').Text.strip()
                        if( len(toInpt) > 0 ):
                            toInpt += '-00:00:00'
                            toDate = System.DateTime.ParseExact( toInpt, format, provider )
                            self.timeTo = toDate
            # -------------------------------------------------------------------------------------
            return newObjId

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    #
    # chain-managment. may be overloaded in the specialyzed functions
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # chainAdd()  :   function adds an item to a chain. the completet handling of header and chain-pointers 
    #
    #
    # parameter  : rootElemRow                   : the root-element this item belongs to
    #              itemToAddRow                  : the row should been added to the chain-order
    #              ItemTypeName                  : name of the header-type as string 'JOB_HEADER';'DEBATE_HEADER'
    #              user_Guid                     : if not none an item from the thread of a different user has to be added
    #
    # return     : Nothing
    #
    # 21.12.2012   - bervie -      initial realese
    # 30.01.2013   - bervie -      something changed.
    # 10.02.2013   - bervie -      added parameter userGuid=None for use trial-editor for the job-announcment-creator
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def chainAdd( self, rootElemRow, itemToAddRow, ItemTypeName, creatorGuid=None  ):
        try:
            self.log.w2lgDvlp("Item.chainAdd started - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")

            # check for header. the creator of a job can add to thread of different user: then the 
            # creator_guid will be set to the user wo hs started the offer
            header = self.chainGetHeader( rootElemRow['_ID'].ToString(), ItemTypeName, creatorGuid )
            if not header:
                # no header present yet. create a new header for a brand-new thread
                self.log.w2lgDvlp("Item.chainAdd no header found")
                header  = self.chainCreateHeader( rootElemRow, ItemTypeName )

            # count number of MSGs we have already for the given header
            headerRootGuid = header['_rootElemGUID'].ToString()
            objName = ItemTypeName.replace('HEADER','MSG')
            objTpId = self.getObjectTypeId(objName)

            query = "_rootElemGUID = '" + headerRootGuid + "' AND objectType = " + str(objTpId)
            msgs = self.itemTbl.Select( query )                                     # all messages in array msgs !! use the force, luke
            numerOfMsgs = msgs.Length
            if numerOfMsgs == 0:
                # we have to add FIRST element in a new thread : append item to the header-element
                self.log.w2lgDvlp("Item.chainAdd started -   No messages found. will append item to header ")

                # update value in the cached item.base-table
                itemToAddRow['_parentID']       = None
                itemToAddRow['_followerID']     = None
                itemToAddRow['_rootElemGUID']   = header['_rootElemGUID'].ToString()

                # update attributes for cuttent item, that wilkl be inserted
                # update the item in the mongo
                updt = {}
                updt.update({'collection': 'item.base' })
                updt.update({'slctVal': itemToAddRow['_ID'].ToString() })
                updt.update({'updatKey':'_rootElemGUID'})
                updt.update({'updatVal':itemToAddRow['_rootElemGUID'].ToString() })
                ctrlID = self.updateDoc(updt)

                # destColl = self.typeToColl[objTpId]  wrong !!
                # updt.update({'collection': destColl })
                #updt.update({'slctKey':'_id'})

                # update the "_followerID-value" in the header of the thread
                header['_followerID'] = itemToAddRow['_ID'].ToString()
                updt = {}
                updt.update({'collection': 'item.base' })
                updt.update({'slctVal': header['_ID'].ToString() })
                updt.update({'updatKey':'_followerID'})
                updt.update({'updatVal':header['_followerID'].ToString() })
                ctrlID = self.updateDoc(updt)

                

            else:
                # append the new item to the end of the existing thread
                self.log.w2lgDvlp("Item.chainAdd started -   Item will be appended to existing thread ")
                
                # get last item in thread. the last is always without follower. only one last item should exist
                last = None
                ctrlCount = 0
                for itm in msgs:
                    if not itm['_followerID']:
                        last = itm
                        ctrlCount += 1

                if ctrlCount > 1:
                    raise Exception('Item.chainGetHeader  More than messages with follower = None found for header : ' + header['_ID'].ToString() )
                    return
                
                # update the data-cache with the new element to insert
                itemToAddRow['_parentID']       = last['_ID']
                itemToAddRow['_followerID']     = None
                itemToAddRow['_rootElemGUID']   = header['_rootElemGUID'].ToString()
                
                # update attributes for cuttent item, that wilkl be inserted
                # update the item in the mongo
                updt = {}
                updt.update({'collection': 'item.base' })
                updt.update({'slctVal': itemToAddRow['_ID'].ToString() })
                updt.update({'updatKey':'_parentID'})
                updt.update({'updatVal':itemToAddRow['_parentID'].ToString() })
                ctrlID = self.updateDoc(updt)
                updt['updatKey'] = '_rootElemGUID'
                updt['updatVal'] = itemToAddRow['_rootElemGUID'].ToString()
                ctrlID = self.updateDoc(updt)

                # update the currently 'last-but-one' in session-cache and databse
                last['_followerID'] = itemToAddRow['_ID']
                updt.update({'slctVal': last['_ID'].ToString() })
                updt.update({'updatKey':'_followerID'})
                updt.update({'updatVal':last['_followerID'].ToString() })
                ctrlID = self.updateDoc(updt)

            self.appCch.dtSt.AcceptChanges()

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # chainCreateHeader()  :   if no header is present this function creates a new one. overloaded in the derived specialist
    #
    # parameter     :  rootElemID           : the root-elem we are looking for
    # return        :  createdHeaderId      : the new created ID of the Header
    #
    # 21.12.2012   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def chainCreateHeader( self, rootElemRow, ItemTypeName, userGuid=None):
        try:
            self.log.w2lgDvlp("Item.chainCreateHeader started with root_elem_id " + rootElemRow['_ID'].ToString() + " , objType = " + ItemTypeName )
            pass

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())
    
    

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # chainGetHeader()  :   function searches the header-id for a given root-element. returns None if nothing found.
    #
    # parameter  : rootElemID     : The ID of the root-element
    #              ItemTypeName   : the needed header-type 
    #
    #
    #
    # return     : row of the found header if succesfull
    #              none if nothing was found
    #
    # 21.12.2012   - bervie -      initial realese
    # 30.01.2013   - bervie -      changed soething
    # 10.02.2013   - bervie -      added param creatorGuid to find the header of different user than logged-in
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def chainGetHeader( self, rootElemID, ItemTypeName, creatorGuid = None ):
        try:
            # build query-string in dependance of the given object-type
            self.log.w2lgDvlp("Item.chainGetHeader started with root_elem_id " + rootElemID + " , objType = " + ItemTypeName + ' creatorGUID = ' + unicode( creatorGuid ) )
            
            query = None
            HdrTypeId = self.getObjectTypeId( ItemTypeName )

            if ItemTypeName == 'JOB_HEADER':
                # change bervie 10.02.2013- - - - - - - - - - - - - - - - - - - - - - - - 
                if not creatorGuid:
                    creatorGuid = self.usrDt.getItem('GUID')
                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
                    
                # JOB_HEADER means one chain per root_elem/user
                # query = "_parentID = '" + rootElemID + "' AND objectType = " + str( HdrTypeId ) + " AND _creatorGUID = '" + self.usrDt.getItem('GUID') + "'"
                query = "_parentID = '" + rootElemID + "' AND objectType = " + str( HdrTypeId ) + " AND _creatorGUID = '" + creatorGuid + "'"

                self.log.w2lgDvlp("Item.chainGetHeader called for JOB_HEADER ; GUID of creator : " + creatorGuid )

            elif ItemTypeName == 'DEBATE_HEADER':
                # DEBATE_HEADER menas one chain per root_elem
                self.log.w2lgDvlp("Item.chainGetHeader called for DEBATE_HEADER " )
                query = "_parentID = '" + rootElemID + "' AND objectType = " + str( HdrTypeId )

            else:
                # unknown object-type
                raise Exception('Item.chainGetHeader  called with an unknown object-type !!') 
                return None

            # get header
            self.log.w2lgDvlp("Item.chainGetHeader QUERY                                   : " + query )
            rows = self.itemTbl.Select( query )
            self.log.w2lgDvlp("Item.chainGetHeader QUERY : number of found rows            : " +  str(rows.Length) )

            if rows.Length == 0:
                self.log.w2lgDvlp("Item.chainGetHeader can not find a header. returninh None, create a new !!" + query )
                return None
            elif rows.Length == 1:
                header = rows[0]
            elif rows.Length > 1:
                self.log.w2lgDvlp("Item.chainGetHeader has found a couple of headers. check database-collection !!" + query )
                header = rows[0]

            self.log.w2lgDvlp("Item.chainGetHeader loaded header with   HEADER_ID " + header['_ID'].ToString() + " of type : " + self.getObjectTypeString( header['objectType'] ) + " and crearorGUID :" + header['_creatorGUID'].ToString() )

            return header

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # chainGetIDs :  get the ids of a given thread
    #
    # parameter :   baseItemID      : id of root
    #               ItemTypeName    : name of the header-type
    #               creatorGuid     : the creator of the headeris only defined if it is not the currently logged-in user 
    #
    # returns   : array          : all item.base._id's that are in the thread
    #
    # 28.12.2012   - bervie-      initial realese
    # 30.01.2013   - bervie-      creatorGuid-parameter added for using the job-trial-editor as creator of a job
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def chainGetIDs(self, baseItemID, ItemTypeName, creatorGUID=None ):
        try:
            self.log.w2lgDvlp("Item.chainGetIDs started " )
            chainList = []
            root = self.itemTbl.Rows.Find( baseItemID )
            chainList.Add( root )

            # 1. get header element
            HdrTypeId = self.getObjectTypeId(ItemTypeName)

            # if no different user is defined as header-creator the function will use the currently logged in  guy
            if not creatorGUID:
                creatorGUID = self.usrDt.getItem('GUID')

            if ItemTypeName == 'DEBATE_HEADER':
                query = "_parentID = '" + baseItemID + "' AND objectType = " + unicode( HdrTypeId )
            elif ItemTypeName == 'JOB_HEADER':
                query = "_parentID = '" + baseItemID + "' AND objectType = " + unicode( HdrTypeId ) + " AND _creatorGUID = '" + creatorGUID + "'"
            
            headers = self.itemTbl.Select( query )
            self.log.w2lgDvlp("-----------Item.chainGetIDs : Query to load the header  : " + query )    
            self.log.w2lgDvlp("-----------Item.chainGetIDs : Number of headers found   : " + str(len(headers)) )    

            if headers.Length == 0 : 
                self.log.w2lgDvlp("-----------Item.chainGetIDs : NO HEADERS FOUND" )    
                return chainList                              # no header found: there is no chain. just return the root-element-id

            header = headers[0]
            self.log.w2lgDvlp("-----------Item.chainGetIDs : header.item.base-ID  : " + header['_ID'].ToString() )    
            self.log.w2lgDvlp("-----------Item.chainGetIDs : header.parent-ID     : " + header['_parentID'].ToString() )    
            self.log.w2lgDvlp("-----------Item.chainGetIDs : header.follower-ID   : " + header['_followerID'].ToString() )    

            if header['_followerID'] == System.String.Empty : return chainList      # header has no follower. should not happn in the real world

            row = self.itemTbl.Rows.Find( header['_followerID'] )

            # 2. get the elemnts of the chain
            while 1:
                chainList.Add( row )
                self.log.w2lgDvlp("-----------Item.chainGetIDs : added to row-list         : " + row['_id'].ToString() )    
                if not row['_followerID'] : break
                row = self.itemTbl.Rows.Find( row['_followerID'].ToString() )                

            self.log.w2lgDvlp("-----------Item.chainGetIDs ended   --------------------------------------------------------------------------------------" )    
            return chainList
            

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    ## * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    ## chainLoad( ... )  :   load the detail-data of all elements ( except header. has no data to print ) an build useable HTML from that
    ##
    ## parameter :  root_elem   is the _id of the root-element of the chain
    ##
    ## return :     string with the HTML-code of the chain
    ##
    ## 21.12.2012   - bervie-      initial realese
    ## 30.01.2013   - bervie-      added parameter creatorGuid to get the items of a different user thann whom is logged-in
    ##
    ## * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    #def chainLoad( self, rootElemID, HdrTypname, creatorGuid = None ):
    #    try:
    #        chain = self.chainGetIDs( rootElemID , HdrTypname, creatorGuid  )
    #        count = len(chain)
    #        if count == 0:
    #            raise Exception('Item.chainLoad : No items found  More than messages with follower = None found for header : ' )
    #            return
    #        horLi = ''
    #        outwurf = System.Text.StringBuilder()
    #        cltInfo = System.Globalization.CultureInfo('de-DE')
    #        idx = 0
    #        for item in chain:
    #            if idx > 0 : outwurf.Append('<br />')
    #            #outwurf.Append('<div class="row alert alert-info">')
    #            mongoId = item['_objectDetailID'].ToString()
    #            row = self.itemTbl.Rows.Find( item['_ID'].ToString() )
    #            meat = self.load( row )
    #            #outwurf.Append( '<small>' )
    #            #outwurf.Append( row['nickname'].ToString() )
    #            #outwurf.Append( '<br />' )
    #            #outwurf.Append( row['creationTime'].ToString() )
    #            #outwurf.Append( '</small>' )
    #            #outwurf.Append('</div>')
    #            #outwurf.Append( self.data['html'] )
    #            #outwurf.Append('<hr />')
    #            ## first coll who was the creator
    #            #outwurf.Append( '<div class="span4">' )
    #            #outwurf.Append( '<strong>Ersteller: ' )
    #            #outwurf.Append( row['nickname'].ToString() )
    #            #outwurf.Append( '</strong></div>' )
    #            ## second coll the begin-date
    #            #if row['from'] != System.DateTime.MinValue:
    #            #    outwurf.Append( '<div class="span2">' )
    #            #    outwurf.Append( 'Start-Termin: ' )
    #            #    outwurf.Append( row['from'].ToLocalTime().ToString('d',cltInfo) )
    #            #    outwurf.Append( '</div>' )
    #            ## third coll : the end date
    #            #if row['till'] != System.DateTime.MinValue:
    #            #    outwurf.Append( '<div class="span2">' )
    #            #    outwurf.Append( 'End-Termin: ' )
    #            #    outwurf.Append( row['till'].ToLocalTime().ToString('d',cltInfo) )
    #            #    outwurf.Append( '</div>' )
    #            ## fourth coll : creation Time
    #            #outwurf.Append( '<div class="span2">' )
    #            #outwurf.Append( 'erstellt am : ' )
    #            #outwurf.Append( row['creationTime'].ToLocalTime().ToString('d',cltInfo) )
    #            #outwurf.Append( '</div>' )
    #            #outwurf.Append( '</div>' )
    #            outwurf.Append( self.data['html'] )
    #            #outwurf.Append('<hr />')
    #            idx += 1
    #        return outwurf.ToString()
    #    except Exception,e:
    #        self.log.w2lgError(traceback.format_exc())





    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # chainLoad( ... )  :   load the detail-data of all elements ( except header. has no data to print ) an build useable HTML from from it
    #                       version 2 : creates an dict instead of an text with all data taht belongs to the item
    #
    # parameter :  root_elem   is the _id of the root-element of the chain
    #
    # return :     string with the HTML-code of the chain
    #
    # 21.12.2012   - bervie-      initial realese
    # 30.01.2013   - bervie-      added parameter creatorGuid to get the items of a different user thann whom is logged-in
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def chainLoad( self, rootElemID, HdrTypname, creatorGuid = None ):
        try:
            chainTxt = System.Text.StringBuilder()
            result = {}
            chain = self.chainGetIDs( rootElemID , HdrTypname, creatorGuid  )
            if len(chain) == 0:
                raise Exception('Item.chainLoad : No items found  More than messages with follower = None found for header : ' )
                return

            idx = 0
            for item in chain:
                mongoId = item['_objectDetailID'].ToString()
                row = self.itemTbl.Rows.Find( item['_ID'].ToString() )
                self.load( row )
                # if we have an answer add the creator-nickname to the header
                if idx > 0 : 
                    chainTxt.Append('<br />')
                    chainTxt.Append( '<small>' )
                    chainTxt.Append('<div class="row well">')
                    chainTxt.Append('beantwortet von : ')
                    chainTxt.Append( row['nickname'].ToString() )
                    chainTxt.Append( '</div></small>' )
                chainTxt.Append( self.data['html'] )
                chainTxt.Append('<hr />')
                idx += 1

            # load the cached data of the root-item of this chain
            row = self.itemTbl.Rows.Find( rootElemID )
            for col in self.itemTbl.Columns:
                result.Add(col.ColumnName , row[col] )

            result.Add('html',chainTxt.ToString())
            return result

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # getCoords( ... )  :   load the of the given root-elemnt
    #
    # parameter :  root_elem   is the _id of the root-element of the chain
    #
    # return :     tuple with the Lon and Lat or None if no coords are defined for the item
    #
    # 21.12.2012   - bervie-      initial realese
    # 30.01.2013   - bervie-      added parameter creatorGuid to get the items of a different user thann whom is logged-in
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def getCoords( self, rootElemID ):
        try:
            self.log.w2lgDvlp("Item.getCoords started -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  " )
            root = self.itemTbl.Rows.Find( rootElemID )
            lon = root['lon'].ToString()
            lat = root['lat'].ToString()

            if ( len(lon) > 0 ) and ( len(lat) > 0):
                self.log.w2lgDvlp("Lon (Laengengrad) : " + lon )
                self.log.w2lgDvlp("Lat (Breitengrad) : " + lat )
                self.log.w2lgDvlp("Item.getCoords ended   -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  " )

                return( lon ,lat )
            else:
                self.log.w2lgDvlp("no coord was found for " + unicode(rootElemID) )
                self.log.w2lgDvlp("Item.getCoords ended   -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  " )
                return None

            pass


        except Exception,e:
            self.log.w2lgError(traceback.format_exc())

