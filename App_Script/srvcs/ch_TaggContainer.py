# ***********************************************************************************************************************************************
# ch_TaggContainer.py : class manages the cached hashtaggs used in nejoba 
#                       <https://docs.google.com/drawings/d/1f43GjperG20dl_-wI6mS20LeuyL0ZecjT1Y2Ec7u724/edit>
#                    
#                       we need a fast access to the hashtags, that are used in the nejoba-cache.
#
#                       1. the strings used for tagging are stored in an array : TaggList
#                          ["bahnhof","karate","tafeln",.....]
#                          the index of a string is used in the next data-container to represent the tagg. every tagg is unique in the array
#
#                       2. a python dictonary is used to combine the taggs with the locations : LocDict
#                          { 10236 : { 1 : ['a872cf...','abde6567...',...] , 30976 : 2 , 10236 : 1 ,..... }
#                          the key in the LocDict is alway the index of the location in the location-cache-table and the value is another dictionary 
#                          that has the list of items for every tagg. explained in the following.
#
#                       3. a couple of dictionaries is used to combine taggs with an array of items : ItemDict
#                          every location in the LocDict has one ItemDict as value. this dict stores for every tagg that is used at that location an array 
#                          with item-ids from item.base.
#                          That means:
#                          LocDict['Hückelhoven_TblIdx'].keys()     = Array zu einer Stadt mit allen Table-Indexen der verwendeten Taggs 
#                          LocDict['Hückelhoven_TblIdx'][0]         = ein Array mit allen Items ( base.item['_ID'] unabhängig vom Projekttyp ) an einem bestimmten Ort = Liste der 
#
#
## ***********************************************************************************************************************************************
import clr
clr.AddReference('MongoDB.Bson')
clr.AddReference('MongoDB.Driver')
from MongoDB.Bson import *
from MongoDB.Driver import *
from System.Web.Configuration import *
import System.Text
import System.Guid
import System
import traceback
import re
import codecs
import tls_LogCache
import ch_geoCache
import ch_AppCache


class TaggContainer():
    '''
    TaggContainer Class: the class that manages the HashTaggs used in nejoba

    functions:
    addTaggToList       : if tagg is not already in the TaggList it will be added to the list                
                          used during initialization of te class
    storeTagg           : the function stores a tag and the item.base-ID for a loccation                
                          1. get the ItemDict for the location the data belongs to
                             if no ItemDict available create a new for the location
                          2. add the item.base-ID of the data to the array that belongs to 
                             the hashtagg-index

    getTaggsByLocName           : gets an array of all locations that are available for a location -> LocDict['Hückelhoven_TblIdx'].keys()
    getItemIdxForTagg           : get an array with all item.base-IDs that belong to a given 
    getIndexForLocString        : get the position-index for a location by location-name-identifier
    
    '''

    # ***********************************************************************************************************************************************
    # constructor of TaggContainer : the class that manages the HashTaggs used ion nejoba
    #
    # parameter : pg : Page-Instance to get access to the Application-Cache.
    #
    # 16.03.2013    berndv  initial realese
    # 12.04.2013    bervie  added self.CommandDict to store all  commands with their index into a  
    # 21.04.2013    bervie  added flag that shows if we have an unknown tag in the query. if so the results for AND should be empty
    #
    # ***********************************************************************************************************************************************
    def __call__( self ):
        self.__init__()

    def __init__( self, pg):
        try:
            self.Page = pg 

            # init logging
            self.log = pg.Application['njbLOG']
            if self.log == None:
                self.log = tls_LogCache.LogCache(pg.Application)
                pg.Application['njbLOG'] = self.log

            # init the geo-source if we need it
            self.geoSrc = pg.Application['njbGeoSrc']
            if self.geoSrc == None:
                self.geoSrc = ch_geoCache.GeoCache(pg)
                pg.Application['njbGeoSrc'] = self.geoSrc

            self.TaggList       = []        # list with all tags. the index in the arry is used as key
            self.CommandDict    = {}        # dict with all commands. KEY= string ;  value = index in self.TaggList (12.04.2013)
            self.LocDict        = {}        # a dict with the Item-Dicts given for a location

            self.loadTagIdxFile()           # load the tagging-index into a multi-array

            # self.ItemDict is created when a new hashtag is added to a location LocDict{ locationIdx : {} }

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # loadTagIdxFile : helper-function loads the tagg-index into a muiltidimensional matrix
    #
    # 18.03.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def loadTagIdxFile( self ):
        try:
            tmpltPath = self.Page.Server.MapPath( WebConfigurationManager.AppSettings['TaggingMatrixDefinition'] )
            f = codecs.open(tmpltPath, "r", "utf-8")
            lns = f.readlines()
            f.close()
            mxItems = 20
            self.mtrx = [[[[[[ None ] for a in range(mxItems)  ] for b in range(mxItems) ] for c in range(mxItems) ] for d in range(mxItems) ] for e in range(mxItems) ] 
            keys = [ 0, 0, 0, 0, 0]

            for ln in lns:
                lngth = len( ln.split('\t') )
                tagg = unicode(ln.strip())
                if lngth == 0 :
                    pass
                elif lngth == 1 :
                    keys[1] = keys[2] = keys[3] = keys[4] = 0
                    keys[0] = keys[0] + 1
                    self.mtrx[ keys[0] ] [ keys[1] ] [ keys[2] ] [ keys[3] ] [ keys[4] ] = tagg
                    #self.log.w2lgDvlp( unicode(keys) +  ' - ' + unicode(lngth) +  ' - ' + unicode(tagg) )
                elif lngth == 2 :
                    keys[2] = keys[3] = keys[4]  = 0
                    keys[1] = keys[1] + 1
                    self.mtrx[ keys[0] ] [ keys[1] ] [ keys[2] ] [ keys[3] ] [ keys[4] ] = tagg
                    #self.log.w2lgDvlp( '\t' + unicode(keys) +  ' - ' + unicode(lngth) +  ' - ' + unicode(tagg) )
                elif lngth == 3 :
                    keys[3] = keys[4] = 0
                    keys[2] = keys[2] + 1
                    self.mtrx[ keys[0] ] [ keys[1] ] [ keys[2] ] [ keys[3] ] [ keys[4] ] = tagg
                    #self.log.w2lgDvlp( '\t\t' + unicode(keys) +  ' - ' + unicode(lngth) +  ' - ' + unicode(tagg) )
                elif lngth == 4 :
                    keys[4] = 0
                    keys[3] = keys[3] + 1
                    self.mtrx[ keys[0] ] [ keys[1] ] [ keys[2] ] [ keys[3] ] [ keys[4] ] = tagg
                    #self.log.w2lgDvlp( '\t\t\t' + unicode(keys) +  ' - ' + unicode(lngth) +  ' - ' + unicode(tagg) )
                elif lngth == 5 :
                    # nothing left
                    keys[4] = keys[4] + 1
                    self.mtrx[ keys[0] ] [ keys[1] ] [ keys[2] ] [ keys[3] ] [ keys[4] ] = tagg
                    #self.log.w2lgDvlp( '\t\t\t\t' + unicode(keys) +  ' - ' + unicode(lngth) +  ' - ' + unicode(tagg) )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # addTaggToList : add a string to the tagg-container if not already present.
    #
    # parameter :  taggString is the tagg that should be added to the array
    # returns   :  the position-index of the tagg in the tagging-array
    #
    # 16.03.2013    berndv  initial realese
    # 12.04.2013    bervie  added a dictonary where all commands [tag starting with a § like rubrics or stuff] are stored 
    #                       so there is no need to check the wholt tagg-list to get the substrings of a given rubric
    #
    # ***********************************************************************************************************************************************
    def addTaggToList(self, taggStrg):
        try:
            taggString = taggStrg.ToString()

            if  not self.TaggList.Contains(taggString) : 
                self.TaggList.Add( taggString )
                position = len(self.TaggList) - 1

                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
                # 12.04.2013 if we have added a command (startrting with a '§', the position will be stored in a dict to have faster access to it
                #            sometimes we have to check for substrings of a command. without the command-dictonary we had to check the whole list all the time
                # self.log.w2lgDvlp( u'TaggContainer.addTaggToList - line 174   TagString = ' + unicode( taggString ) )
                if taggString[0] == '§': self.CommandDict[taggString] = position

                self.log.w2lgDvlp( 'TaggContainer.addTaggToList     : taggString = %s ; position = %u  ' % (unicode(taggString),position) )

                return position
            else:
                return self.TaggList.IndexOf(taggString)

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # storeTagg : put a new tagging-item into the cache. the function takes care if new containers must be created automatically
    #
    #
    # parameter :
    #     taggString   - the tagg to add to the managment
    #     locMongoId   - the id of the location in the locations-table
    #     itemBaseID   - the _ID of the document in the base.item collection
    #
    # returns :
    #     nix
    #
    # https://docs.google.com/drawings/d/1f43GjperG20dl_-wI6mS20LeuyL0ZecjT1Y2Ec7u724/edit
    #
    # 16.03.2013    berndv  initial realese
    #
    # ***********************************************************************************************************************************************
    def storeTagg(self, taggString, locMongoId, itemBaseID):
        try:
            # find the position-index in location-table by asking with the keystring "DE|41836"
            tbl    = self.geoSrc.locTable
            row    = tbl.Rows.Find(locMongoId)
            locKey = row['keyStrng'].ToString()         # key to the locations is a string like 'DE|41836'
            taggIdx = self.addTaggToList(taggString)    # position.index of tagg-sting in the local-member taggList. Used as key in the ItemDict dictionary

            # self.log.w2lgDvlp(' TaggContainer->storeTagg  location-Idx : '  + locKey + ' for locID ' + unicode(locMongoId) + ' ; tagg-id: ' + unicode(taggIdx) + ' for tagg  : ' + taggString)    

            ItemDict = None
            if self.LocDict.has_key(locKey):                            # is there allready a dictionary for the location locIdx  ? ?
                ItemDict = self.LocDict[locKey]                         # get the dict for the location

                if ItemDict.has_key(taggIdx):                           # is there already a array for the given tagg?
                    ItemDict[taggIdx].Add(itemBaseID)                   # then add the item.base-IID to the already existing item-array
                else:                                                   
                    ItemDict[taggIdx] = [itemBaseID]                    # if  the tagg is new for the location begin a new array with item.base-IDs
            else:
                ItemDict = { taggIdx : [itemBaseID] }                   # create a new dictionary for a new location
                self.LocDict[locKey] = ItemDict
            # self.log.w2lgDvlp(' for taggstring : ' + taggString + ' found ' + row[0].ToString() + ' ' + row[4].ToString() + ' @index : ' + str(locIdx) )
            return

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # getTaggsByLocName :  fnctn is called with the location-call-string like 'de|41836' or the mongo_id (checked by locStrng[2] == '|'
    #                      it returns an array with tupples:
    #                                      
    #                                      [('tagg_name1',amount_1),('tagg_name2',amount_2),('tagg_name2',amount_2),('tagg_name2',amount_2)....]
    #
    # parameter :  locString               : "DE|41836" or mongoID
    #              strtChr = None          : filter for a beginning character in the tagg. if defined the functzion will return only 
    #                                        taggs with the given start-character
    #
    # returns   :  array with tuple of taggs with their amount of apperance  : [ ('bahnhof',2) ,('karneval',3),('sportverein',92),......]
    #
    # 23.03.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def getTaggsByLocName(self, locStrng, strtChr=None  ):
        try:
            ky = self.getIndexForLocString( locStrng )
            rslt = []

            # load the taggs we have from the given location and 
            # the amount of items belonging to the given hashtagg
            if ky is not None:
                if self.LocDict.has_key( ky ):
                    itemDct = self.LocDict[ky]

                    for taggIdx in itemDct.keys():
                        taggName       = self.TaggList[taggIdx]
                        amountOfTaggs  = len(itemDct[taggIdx])
                        
                        if strtChr is None:
                            tgTpl = [taggName, amountOfTaggs]
                            rslt.Add(tgTpl)
                        else:
                            if strtChr == taggName[0]:
                                tgTpl = [taggName, amountOfTaggs]
                                rslt.Add(tgTpl)
            return rslt

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # getItemIdxForTagg :  main-function to load the base.items._IDs for a tagg at a location
    #                      get an array of mongo_IDs with the item.base-IDs of the items which are tagged by the taggString for a given location
    #
    # parameter:
    #    locStrng   : the locNameIdentifier like 'de|41836' or the _ID of the location
    #    taggStrng  : the tagg that we are loocing for example 'tenninsverein-blau-weiss'
    #
    # returns
    #    array with the base-item-ids of all items that match the given query
    #
    # 23.03.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def getItemIdxForTagg( self, locStrng, taggStrng ):
        try:
            baseItmIds     = []         # result-list with the base.item._IDs
            posInTaggArray = []         # the index of the hshtagg in the array 

            ky = self.getIndexForLocString( locStrng )
            tgPosIdx = self.TaggList.IndexOf( taggStrng )

            if (ky is None) or ( tgPosIdx < 0 ) : return baseItmIds

            # load the taggs we have from the given location and 
            # the amount of items belonging to the given hashtagg
            if self.LocDict.has_key(ky):
                itemDct = self.LocDict[ky]
                if itemDct.has_key(tgPosIdx):
                    baseItmIds = itemDct[tgPosIdx]
            return baseItmIds

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # getIndexForLocString : helper-function returns a keyStrng for a given mongo_ID
    #
    # parameter :   the named identifier for a location like 'DE|41836' or the _ID in the dataTabe used als key : the MongoId
    # returns   :   the position-index of the location in the cached location-table
    #
    # 23.03.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def getIndexForLocString( self, locStrng ):
        try:
            posIdx = None
            # get the place-index of the location in the cache
            if locStrng[2] != '|':
                # get the location by name : 'de|41836'
                row = self.geoSrc.locTable.Rows.Find(locStrng.strip())
                locStrng = row['keyStrng'].ToString()

            return locStrng.upper().strip()

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # loadBaseItems : function returns a list of base.item-IDs that are  matching a tagg in a given location
    #
    # parameter :   locKeyName   :  the named identifier for a location like 'DE|41836' 
    #               HashTaggList :  the list of hashtaggs that we are searchinh for 
    #               andOrNot     :  if true the tags will be AND-combined. that means only the items 
    #                               will be found that have all of the given tasks. Default is false = OR means any tagg will be added
    #
    # returns   :   list with the results. IDs are unique
    #
    # 24.03.2013    berndv  initial realese
    # 11.04.2013    bervie  if we have hashtags with a rubric they are now  associated by an AND !!
    #
    # ***********************************************************************************************************************************************
    def loadBaseItems( self, locKeyName, HashTaggList, useANDCombine=False ):
        try:
            # HashTaggList is stored for comparing it with the tags we found for location
            self.HshTgInpt = HashTaggList

            # get the configurtion : number of items before area-search stops and size that should be searched
            minAmount = System.Convert.ToInt16( WebConfigurationManager.AppSettings["MinNumOfDebates"] )
            areaSize  = WebConfigurationManager.AppSettings["areaSize"];

            locList = self.geoSrc.getPlacesByPostcode( locKeyName[:2], locKeyName[3:], areaSize.ToString() )
            itmIds = []

            foundItms = []
            if len(HashTaggList) > 0:
                foundItms = self.askTagCache( locList, HashTaggList, useANDCombine )

            return foundItms

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # askTagCache :  this function loads the matching base-item-ids for a given tag- & location-list
    #
    # parameter:
    #    locStrng   : the locNameIdentifier like 'de|41836' or the _ID of the location
    #    taggStrng  : the tagg that we are loocing for example 'tenninsverein-blau-weiss'
    #    combAnd    : the hashtaggs must be used in all items to be added to the list. default is 'FALSE'
    #
    # returns
    #    unsorted unique list with the base-item-ids of all items that match the given rubric-tagg or the master-rubric (higher in harachy)
    #
    # 10.04.2013    berndv  initial realese
    # 21.04.2013    berndv  if a hashtag is not given for an item an empty list will be returned
    # ***********************************************************************************************************************************************
    def askTagCache( self, locKeyList, HashTaggList, useANDCombine=False ):
        try:
            lstTagIdx       = self.askForTagIdxList( HashTaggList )                         # get the index-IDs of the hashtags in self.TaggList
            dictItemCntnr   = self.askForItemContainer( locKeyList, lstTagIdx )             # get the dict of items for hashtags depending on location from self.LocDict
            #self.log.w2lgDvlp('TaggContainer->askTagCache         locKeyList      : ' + unicode( locKeyList ) )
            #self.log.w2lgDvlp('TaggContainer->askTagCache         HashTaggList    : ' + unicode( HashTaggList ) )
            #self.log.w2lgDvlp('TaggContainer->askTagCache         lstTagIdx       : ' + unicode( lstTagIdx ) )
            #self.log.w2lgDvlp('TaggContainer->askTagCache         dictItemCntnr   : ' + unicode( dictItemCntnr ) )

            # decide what kind of boolean combination has to be used : AND ( all items must have all hashtags)
            #                                                          OR  ( every item that has a hashtag will be shown )
            itemsToDisplay = []
            if useANDCombine == False: 
                itemsToDisplay = self.askForItemsHaveOneHashTag( dictItemCntnr )
            else:
                itemsToDisplay = self.askForItemsHaveAllHashTag( dictItemCntnr )

            self.log.w2lgDvlp('TaggContainer->askTagCache         RESULTS          : ' + unicode( itemsToDisplay ) )

            return itemsToDisplay

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # ***********************************************************************************************************************************************
    # askForTagIdxList : get a list with all idx of the tags that were asked for 
    #
    # parameter
    #   rsltDict       : dictionary with all results in the container
    #
    # 13.04.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def askForTagIdxList( self, HashTaggList ):
        try:
            self.log.w2lgDvlp('# # # TaggContainer->askForTagIdxList called ' )
            result = []

            # remove empty strings
            try :  
                while type(HashTaggList.index(System.String.Empty)) == int : HashTaggList.remove(System.String.Empty)
            except : pass

            for tag in HashTaggList:
                # all command-tags will also be found that start with the given string as startin substring
                if tag.startswith('§'): 
                    for cmnd in self.CommandDict.keys():
                        if (cmnd.startswith( tag )) and (cmnd != tag) : 
                            result.Add( self.CommandDict[cmnd] )

                if tag in self.TaggList : 
                    result.Add( self.TaggList.index(tag) )            # if the tag is known in the TagList the index will be added 

            self.log.w2lgDvlp('#     TaggContainer->askForTagIdxList   result-array : ' )
            for itm in result:
                self.log.w2lgDvlp('#     TaggContainer->askForTagIdxList   tag : ' + unicode( self.TaggList[itm] ) + ' ;  index : ' + unicode(itm) )
            self.log.w2lgDvlp('#     TaggContainer->askForTagIdxList                  ' )
            return result

        #try:
        #    result = []
        #    for tag in HashTaggList:
        #        self.log.w2lgDvlp('TaggContainer->askForTagIdxList called with HashTags ' + unicode(tag) )

        #        # if the tag is known in the TagList the index will be added 
        #        if tag in self.TaggList : 
        #            result.Add( self.TaggList.index(tag) )

        #    # if we have a rubric-request (the  rubric is alleawy inserted as first item )
        #    # the function will also check substrings to get all the substrings to get the
        #    if HashTaggList[0].startswith('§'): 
        #        rbrcKey = HashTaggList[0]
        #        for cmnd in self.CommandDict.keys():
        #            if cmnd.startswith( HashTaggList[0] ): 
        #                result.Add(self.CommandDict[cmnd])

        #    # result = list( set( result ))

        #    for index in result:
        #        self.log.w2lgDvlp('TaggContainer->askForTagIdxList TAG-POSITION-FOUND ' + unicode(index) )

        #    return result

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # ***********************************************************************************************************************************************
    # askForItemContainer : creates a dict of item-dictionaries for the given llocations and tags
    #
    # parameter
    #   locKeyList       : a list with all location-arrays of the locations in the neighbouhood
    #   lstTagIdx        : a list with the positions of the tags in the hashtag-list
    #
    # returns:
    #   a dictionary with the hashtag-ID and a list of items. the list contains all base-item-ids of all locations that were requested
    #
    # example:
    #   askForItemContainer TAG TO ADD TO LIST : 0
    #   askForItemContainer LOC-DEP LIST ADDED : [['51654389773e6f0cdc4c009d', '51654619773e6f0cdc4c00a1']]
    #   askForItemContainer TAG TO ADD TO LIST : 32
    #   askForItemContainer LOC-DEP LIST ADDED : [['51655700773e6f0cdc4c00a7']]
    #
    # 13.04.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def askForItemContainer( self, locKeyList, lstTagIdx ):
        try:
            result = {}

            # 1. go through the neighbourhood. get  -  this is a sigthseeing-tour
            #    as a result we will get the ItemDict for the given location. key of that dict is the HashTagIndex ; value is a list containing all items for that hashTag
            for loctn in locKeyList:
                ky = self.getIndexForLocString( loctn[0] )
                if ky is not None:
                    if self.LocDict.has_key(ky):
                        itemDict = self.LocDict[ky]
                        self.log.w2lgDvlp('TaggContainer->askForItemContainer   LOCATION-FOUND   : ' + unicode(ky) )
                        self.log.w2lgDvlp('TaggContainer->askForItemContainer   ITEMS-FOUND      : ' + unicode(itemDict) )

                        # all lists with base-item-IDs, that match the lstTagIdx, are copied to a result-dictionary
                        # this result dict has the hashtag-posId as key and the list of the list from the locations as value
                        for tagPosIdx in lstTagIdx:
                            if itemDict.has_key( tagPosIdx ):
                                itemBaseIdListDependingOnLocation = None
                                if result.has_key(tagPosIdx):
                                    # itemBaseIdListDependingOnLocation = itemDict[tagPosIdx]
                                    itemBaseIdListDependingOnLocation = itemDict[tagPosIdx]
                                    result[tagPosIdx].Add( itemBaseIdListDependingOnLocation )
                                else:
                                    # itemBaseIdListDependingOnLocation = [itemDict[tagPosIdx]]
                                    itemBaseIdListDependingOnLocation = [itemDict[tagPosIdx]]
                                    result[tagPosIdx] = itemBaseIdListDependingOnLocation

                                self.log.w2lgDvlp('TaggContainer->askForItemContainer TAG TO ADD TO LIST : ' + unicode(tagPosIdx) + ' - ' +  unicode(self.TaggList[tagPosIdx]))
                                self.log.w2lgDvlp('TaggContainer->askForItemContainer LOC-DEP LIST ADDED : ' + unicode(itemBaseIdListDependingOnLocation) )
            return result

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())




    # ***********************************************************************************************************************************************
    # askForItemsHaveOneHashTag :  get all item-base-ids for the locations and hashtags. this functio is for OR combination
    #
    #
    # 13.04.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def askForItemsHaveOneHashTag( self, itemsByHashTag ):
        try:
            result = []
            for tagId in itemsByHashTag.keys():
                for lst in itemsByHashTag[tagId]:
                    result += lst
            return list( set( result ) )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # ***********************************************************************************************************************************************
    # askForItemsHaveAllHashTag :  gets the base-item that have all hashtags that were asked for. this function is for boolean AND-combination
    #
    # 13.04.2013    berndv  initial realese
    # 21.04.2013    berndv  added  correcting: nothing will be displayes if an unknown tag is given
    # ***********************************************************************************************************************************************
    def askForItemsHaveAllHashTag( self, itemsByHashTag ):
        try:
            rbrkId = []                     # a list with the tag-IDs of the rubric-indexes (the §*-Command)
            tagStrngLst = []                # list with all tags we have in the dict (except the §*-Command)

            # get the list with rubric-taggs
            for tagId in itemsByHashTag.keys():
                tagName = self.TaggList[tagId]
                if tagName.startswith('§*R'):
                    rbrkId.Add( tagId )
                else:
                    tagStrngLst.Add( tagName )

            # 21.04.2013 berndv : bugfix
            # check if one or more tags missing compared to the input: then nothing will be displayed
            if len( tagStrngLst ) != len( self.HshTgInpt[1:] ):
                #self.log.w2lgDvlp('askForItemsHaveAllHashTag tags found in result-dict are not same as found in input  ! ')
                #self.log.w2lgDvlp('askForItemsHaveAllHashTag tags in result-dict : ' + unicode(len( tagStrngLst )))
                #self.log.w2lgDvlp('askForItemsHaveAllHashTag tags in input       : ' + unicode(len( self.HshTgInpt )))
                return []

            listRubrics = []                                    # list with all items 
            listHashTags = []                                   # list of the lists for every tag
            for tagId in itemsByHashTag.keys():
                if tagId in rbrkId:
                    for lst in itemsByHashTag[tagId]:
                        for item in lst:
                            listRubrics.Add(item)
                else:
                    lstSrc = []
                    for lst in itemsByHashTag[tagId]:
                        listHashTags.Add(lst)
                        #for item in lst:
                        #    listHashTags.Add(item)

            self.log.w2lgDvlp('TaggContainer->AllHashTag  RUBRICS       LIST : ' + unicode( listRubrics  ))
            for lstByTag in listHashTags:
                self.log.w2lgDvlp('TaggContainer->AllHashTag  NORMAL TAGS   ITEM : ' + self.TaggList[tagId] + ' LIST : ' + unicode( lstByTag ))

            # get items that are in both intersect
            setSource = set( listRubrics  )
            for lstByTag in listHashTags:
                setSource = setSource.intersection( set(lstByTag) )

            result = list( setSource )
            self.log.w2lgDvlp('TaggContainer->AllHashTag  RESULTS     result : ' + unicode( result ))

            return result

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())











            # controls loaded from the webpage --------------------------------------------------------------------------
            #txbx_info
            #txbx_postcode
            #txbx_email
            #txbx_emailconfirm
            #txbx_pwd1
            #txbx_pwd2
            #txbx_website
            #txbx_picturl
            #txbx_facebook
            #txbx_google_plus
            #txbx_twitter
            #txbx_skype
            #txbx_mobile
            #txbx_phone
            #txbx_forename
            #txbx_familyname
            #txbx_street
            #txbx_housenumber
            #txbx_city
            #txbx_adress_add

            #drpd_item_type
            #drpd_country
            #drpd_language
            # -----------------------------------------------------------------------------------------------------------





