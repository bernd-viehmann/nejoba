# ***********************************************************************************************************************************************
# ch_AppCache.py : class is a DataSet that holds the tabless for the application-cache regarding the announcments and discussions
#                  this class is also responsible for slicing the endless line of items in the server
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#
#  16.11.2012  - bervie -     initial realese
#  12.07.2013  - bervie -     added slicing-mechanism to the class
#                             the nejoba-items build a kinf of timeline as the projil of a facebook-user
#                             this endless line of items is dividet into smaller pieces that will be used for finding 
#                             
# ***********************************************************************************************************************************************
from System.Collections.Generic import *
from System.Web.Configuration import *
import System.Data 
import System.Data.SqlTypes 
from System import Array
from System.Text import StringBuilder

import clr
clr.AddReference('MongoDB.Bson')
clr.AddReference('MongoDB.Driver')
from MongoDB.Bson import *
from MongoDB.Driver import *

import traceback            # for better exception understanding
from time import *
from string import *
import re
import ch_TaggContainer



class AppCache():
    '''
    AppCache Class 
       this class provides the dat-set that holds the tables that are stored in the application 
       cache:
       locations    : the locations used by nejoba
       items        : the items belonging to a place, tagging and time-point 
       
       this class does also the slicing. this means it is dividet into a couple of portions as defined in web.config->SliceDuration
        
       '''


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # constructor. takes the base-configuration of the system in the dict config
    #
    # param:
    #
    #       Page  : pointer to the Page-instance
    #
    # attributes of the class
    #
    #       self.mongoServer    : the nosql-database server-connection 
    #       self.mongoDb        : the database used 
    #
    #       self.dtVwCreator    : find items by creator-data-view
    #       self.dtVwLoctn      : find items by location-data-view
    #       self.dtVwRootElem   : the root-element of an object to find dependencies between items as fast as possible
    #       self.dtVwTags       : a DataView for the tags in 'itemTags' DataTable
    #
    # 16.11.2012   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def __init__(self, pg):
        try:
            self.Page = pg 

            # init logging
            self.log = pg.Application['njbLOG']
            if self.log == None:
                self.log = srvcs.tls_LogCache.LogCache(pg.Application)
                pg.Application['njbLOG'] = self.log

            # managment-class for accessing taggings taken from the app-cache
            self.taggCntnr = self.Page.Application['njbTaggs']

            # prepare the slicing  13.07.2013
            self.StartTime      = System.DateTime.UtcNow                                                            # the base-date for all slicing calculations
            self.SliceDuration  = System.Convert.ToInt16( WebConfigurationManager.AppSettings['SliceDuration'] )    # the duration-period of a slice in days

            # create tables -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  
            self.dtSt = System.Data.DataSet()
            self.createTablesItems()            # define 'naked' tables and relations for announcements
            #self.createTableLocations()         # define 'naked' table for location 

            # prepare mongo-db connection
            connString = WebConfigurationManager.AppSettings['mongoConn']
            dbName     = WebConfigurationManager.AppSettings['dbName']

            self.mongoServer = MongoServer.Create(connString)
            self.mongoDb = self.mongoServer.GetDatabase(dbName)

            # fill data from mongo into data_set -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
            self.fillTablesItems()              # load data from mongo into the items-table (nejoba main-part)

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # createTablesItems :   adds the tables and relations to this data-set that are needed for the items that are of interest in nejoba
    #                       DataTable("items")      has base-administration data of the items stored in nejoba
    #                       DataTable("itemTags")   has the taggings for each item. it is a 1:n relation. one item can have 5 tags
    #
    # 16.11.2012   - bervie -      initial realese
    # 14.02.2013   - bervie -      added new cols to item-data-table : _creatorNickname and _creatorLocation
    # 19.04.2013   - bervie -      changed sort-order of self.dtVwLocObj to _locationID,creationTime DESC
    # 21.06.2013   - bervie -      added tagZero and coordinates for making nejoba to a map-application
    #                              tagZero is the first tag in the collection. it is used to decide which marker should be used in the map   
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def createTablesItems(self):
        try:
            # 1. create a data-table for the main-announcments
            itemTable = System.Data.DataTable("items")
            col = itemTable.Columns.Add("_ID", System.String )
            col = itemTable.Columns.Add("objectType", System.Int32 )
            col = itemTable.Columns.Add("_objectDetailID", System.String )
            col = itemTable.Columns.Add("_hostGUID", System.String )
            col = itemTable.Columns.Add("_rootElemGUID", System.String )
            col = itemTable.Columns.Add("_parentID", System.String )
            col = itemTable.Columns.Add("_followerID", System.String )
            col = itemTable.Columns.Add("_creatorGUID", System.String )
            col = itemTable.Columns.Add("creationTime", System.DateTime )
            col = itemTable.Columns.Add("_locationID", System.String )
            col = itemTable.Columns.Add("from", System.DateTime )
            col = itemTable.Columns.Add("till", System.DateTime )
            col = itemTable.Columns.Add("subject", System.String )
            col = itemTable.Columns.Add("body", System.String )
            # added 14.02.2013 bervie
            col = itemTable.Columns.Add("nickname", System.String )
            col = itemTable.Columns.Add("locationname", System.String )
            # added 21.06.2013 bervie map-data
            col = itemTable.Columns.Add("tagZero", System.String )
            col = itemTable.Columns.Add("lat", System.String )
            col = itemTable.Columns.Add("lon", System.String )
            
            self.dtSt.Tables.Add(itemTable)


            # add primary key to use find on table   http://csharp-guide.blogspot.de/2012/04/adonet-datatableselect-vs.html
            # example for usage : DataRow dr1 = dsEmpInfo.Tables["dtEmpInfo"].Rows.Find("1");
            kyCol = Array.CreateInstance(System.Data.DataColumn, 1) 
            kyCol[0] = self.dtSt.Tables['items'].Columns['_ID'] 
            self.dtSt.Tables['items'].PrimaryKey = kyCol

            # add DataViews as class-attribute
            #
            # add an data-view to find the creator of an item by his GUID in collection 'item.base'
            self.dtVwCreator = System.Data.DataView(self.dtSt.Tables['items'])
            self.dtVwCreator.Sort = '_creatorGUID'

            # add an data-view to find the location of an item by the mongo-id of the location in collection 'item.base'
            self.dtVwLoctn = System.Data.DataView(self.dtSt.Tables['items'])
            self.dtVwLoctn.Sort = '_locationID'

            # add an data-view to find the root-element of an item. this is needed to find sequences of items
            self.dtVwRootElem = System.Data.DataView(self.dtSt.Tables['items'])
            self.dtVwRootElem.Sort = '_rootElemGUID'

            #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
            # removed ( i think not longer used ;-) ) bervie 13.07.2013
            # add an data-view to find the root-element of an item. this is needed to find sequences of items
            #self.dtVwLocObj = System.Data.DataView(self.dtSt.Tables['items'])
            #self.dtVwLocObj.Sort = '_locationID,creationTime DESC'
            #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

            # HINT :
            # col = self.itemTable.Columns.Add("taggingLabels
            # the TAGGING-LABLES of the items are outsourced to a special table 
            # where we have them as 1:n relation pointing to a special item
            # 2. create table with the taggings of each item in "items"-table
            tagTable = System.Data.DataTable("itemTags")
            col = System.Data.DataColumn()
            col = tagTable.Columns.Add("_ID", System.String )
            col = tagTable.Columns.Add("_locationID", System.String )
            col = tagTable.Columns.Add("tag", System.String )
            self.dtSt.Tables.Add(tagTable)

            # add an data-view to find the root-element of an item. this is needed to find sequences of items
            self.dtVwTagList = System.Data.DataView(self.dtSt.Tables['itemTags'])
            self.dtVwTagList.Sort = '_ID'

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # fillTablesItems : this function loads the items from the mongo-db into the cache
    #
    # 16.11.2012   - bervie -      initial realese
    # 22.12.2012   - bervie -      BsonNull.Value is an empty-string now instead of '<BsonNull>'
    # 14.02.2013   - bervie -      added nickname and location_id
    # 17.03.2023   - bervie -      added new tagging-manager class TaggContainer
    # 27.07.2013   - bervie -      rewritten the data-row import. only the timeslices that should be cahced will be imported
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def fillTablesItems(self):
        try:
            slicesToCache = System.Convert.ToInt16( WebConfigurationManager.AppSettings['SlicesCached'] ) - 1
            DateBounds = self.getSliceBounce( slicesToCache )

            leftTime = DateBounds[0]
            rightTime  = DateBounds[1]

            self.log.w2lgDvlp('number of slices cached                        :' + slicesToCache.ToString() )
            self.log.w2lgDvlp('CachedDataSource.fillTablesItems START (left)  :' + leftTime.ToString() )
            self.log.w2lgDvlp('CachedDataSource.fillTablesItems END   (rigth) :' + rightTime.ToString()  )

            # query = Builders.Query.GT( "creationTime", leftTime ).LTE( rightTime )
            query = Builders.Query.LTE( "creationTime", rightTime ).GT( leftTime )
            
            coll = self.mongoDb.GetCollection("item.base")

            # for item in coll.Find(query).SetSortOrder( Builders.SortBy.Descending("$natural") ) :
            for item in coll.Find(query).SetSortOrder( Builders.SortBy.Ascending("$natural") ):
                row = self.dtSt.Tables["items"].NewRow()
                row["objectType"]       = item["objectType"]
                row["creationTime"]     = item["creationTime"]
                row["_ID"]              = self.convNullToEmpty(item["_id"])                 #strings DB-Nulls will be converted to an empty-sting
                row["_objectDetailID"]  = self.convNullToEmpty(item["_objectDetailID"])
                row["_hostGUID"]        = self.convNullToEmpty(item["_hostGUID"])
                row["_rootElemGUID"]    = self.convNullToEmpty(item["_rootElemGUID"])
                row["_parentID"]        = self.convNullToEmpty(item["_parentID"])
                row["_followerID"]      = self.convNullToEmpty(item["_followerID"])
                row["_creatorGUID"]     = self.convNullToEmpty(item["_creatorGUID"])
                row["_locationID"]      = self.convNullToEmpty(item["_locationID"])

                row["nickname"]         = self.convNullToEmpty(item["nickname"])            # 14.02.2013
                row["locationname"]     = self.convNullToEmpty(item["locationname"])

                row["tagZero"]          = self.convNullToEmpty(item["tagZero"])             # 25.05.2013
                row["lon"]              = self.convNullToEmpty(item["lon"])
                row["lat"]              = self.convNullToEmpty(item["lat"])

                # if from or till aren't set we use System.DateTime.MinValue to supress beeing displayed
                timeFrom = item["from"]
                if timeFrom != BsonNull.Value : 
                    row["from"] = item["from"]
                else:
                    row["from"] = System.DateTime.MinValue
                timeTill = item["till"]
                if timeTill != BsonNull.Value : 
                    row["till"] = item["till"]
                else:
                    row["from"] = System.DateTime.MinValue
                self.dtSt.Tables["items"].Rows.Add(row)

                # put tagging-lables in the tagging container
                taggs = item["taggingLabels"]
                if str(taggs) != 'BsonNull' :
                    for tag in taggs:

                        # 17.03.2013 added to replace the tagging-table by a handler - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
                        self.taggCntnr.storeTagg( tag.ToString(), item["_locationID"].ToString(), item["_id"].ToString())
                        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

                        tagRow                = self.dtSt.Tables["itemTags"].NewRow()
                        tagRow["_ID"]         = item["_id"].ToString()
                        tagRow["_locationID"] = item["_locationID"].ToString()
                        tagRow["tag"]         = tag.ToString()
                        self.dtSt.Tables["itemTags"].Rows.Add(tagRow)
                        # self.log.w2lgDvlp('tag added  : ' + tagRow["_ID"].ToString() + ' - ' + tagRow["tag"].ToString() )

            # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  change bervie
            #
            # change 13.01.2013 bervie :  rewritten after redesign
            #
            #
            #                              !!!!!!!! MUST BE CHANGED   ToDo !!!
            #                              !!!!!!!! MUST BE CHANGED   ToDo !!!
            #                 the datatable is checked twice to get the detail-data   !!
            #                              !!!!!!!! MUST BE CHANGED   ToDo !!!
            #                              !!!!!!!! MUST BE CHANGED   ToDo !!!
            #
            #
            ## 2. load the headline and beginning of the body into the cached table
            objTypConf = WebConfigurationManager.AppSettings['objectTypes']     
            objSeperator = WebConfigurationManager.AppSettings['stringSeperator']     
            objectTypes = objTypConf.split(objSeperator)
            objectType = objectTypes.index('JOB_ROOT')

            # load headings and bodys of JOBS into the cache
            self.log.w2lgDvlp('------- LOADING JOB_ROOT INTO cache ------' )
            self.log.w2lgDvlp('_objectDetailID  : ' + str(objectType) )

            coll = self.mongoDb.GetCollection('item.JOB_ROOT')
            for itemRow in self.dtSt.Tables["items"].Rows:
                if itemRow['objectType'] == objectType:                                         
                    key = '_id'
                    val = BsonObjectId(itemRow['_objectDetailID'].ToString())

                    # self.log.w2lgDvlp('row loaded by _id : ' + itemRow['_id'].ToString() )
                    # self.log.w2lgDvlp('_objectDetailID   : ' + val.ToString() )

                    qry  = QueryDocument(key,val)                                               # get the root-document (an JOB) for this item
                    doc = coll.FindOne(qry)

                    subj = doc['heading'].ToString()[:200]
                    subj = subj.replace( '"' , "'" )

                    body = self.RemoveHtml(doc['body'].ToString()).strip()[:300]
                    body = body.replace( '"' , "'" )

                    itemRow['subject']  = subj
                    itemRow['body']     = body

            # load headings and bodys of DEBATES into the cache
            objectType = objectTypes.index('DEBATE_ROOT')
            coll = self.mongoDb.GetCollection('item.DEBATE_ROOT')
            for itemRow in self.dtSt.Tables["items"].Rows:
                if itemRow['objectType'] == objectType:                                         
                    
                    key = '_id'
                    val = BsonObjectId(itemRow['_objectDetailID'].ToString())
                    # self.log.w2lgDvlp('_objectDetailID  : ' + val.ToString() )

                    qry  = QueryDocument(key,val)                                               # get the root-document (an DEBATE) for this item
                    doc = coll.FindOne(qry)

                    subj = doc['heading'].ToString()[:200]
                    subj = subj.replace( '"' , "'" )

                    body = self.RemoveHtml(doc['body'].ToString()).strip()[:300]
                    body = body.replace( '"' , "'" )

                    itemRow['subject']  = subj
                    itemRow['body']     = body

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())




    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # convNullToEmpty : NULL or BsonNull will be converted to an empty string
    #
    # 22.12.2012   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def convNullToEmpty(self, inVal):
        try:
            if inVal == BsonNull.Value:
                return System.String.Empty

            if inVal == System.DBNull.Value:
                return System.String.Empty

            return inVal.ToString()

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # RemoveHtml(str)
    #
    # prepares the class for her job. stores an array with the object-types and a reference to the item-cache-table
    #
    # parameter :   string : the input should be HTML formated text
    #
    # returns   :   string : the text without html-tags
    #
    # 23.11.2012   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def RemoveHtml(self, inTxt):
        try:
            regEx = re.compile("<[^>]*>")
            return regEx.sub("", inTxt )
            pass
            
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # getSliceBounce(int)
    #
    # calculate the days that are represent the beginning and the ens of the given slice. 
    # 
    # HINT : will be used to load date-slices in mongo : http://cookbook.mongodb.org/patterns/date_range/ 
    #
    # parameter :   int : the id of the slice that should be calculated
    # returns   :   tupple with start(left in timebeam)- and end(rigth_in_timebeam)-date
    #
    # 12.07.2013   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def getSliceBounce(self, IdOfSlice ):
        try:
            RigthDiff   = - (IdOfSlice * self.SliceDuration)                        # number of days the end of the timeslice (rigth on timebeam) differs from start
            LeftDiff    = RigthDiff - self.SliceDuration                            # number of days the begin of the timeslice (left on timebeam) differs from start
            LeftDay     = self.StartTime.AddDays( LeftDiff )
            RigthDay    = self.StartTime.AddDays( RigthDiff )

            self.log.w2lgDvlp('-----------------------------------    getSliceBounce     -----------------------------------------' )
            self.log.w2lgDvlp('slice index                           : ' + str( IdOfSlice ) )
            self.log.w2lgDvlp('start-day    left  in timebeam        : ' + LeftDay.ToString() )
            self.log.w2lgDvlp('end-day      rigth in timebeam        : ' + RigthDay.ToString() )
            self.log.w2lgDvlp('-----------------------------------    getSliceBounce     -----------------------------------------' )

            return ( LeftDay, RigthDay )
            
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



