# ***********************************************************************************************************************************************
# ch_GeoCache.py : class stores the geolocation of the postcodes/city in a ADO.NET DataSet
#
# geographic stuff based based on http://www.geonames.org/ 
#
# content of the collection db.location_city in MongoDB:
#  
#        { 
#        "_id" : ObjectId("4eae453fc9a3710f1cebe719"), 
#        "countryCode" : "AD", 
#        "postalCode" : "AD100", 
#        "pstlCounty" : "AD100AD", 
#        "placeName" : "Canillo", 
#        "adminName1" : "", 
#        "adminCode1" : "", 
#        "adminName2" : "", 
#        "adminCode2" : "", 
#        "adminName3" : "", 
#        "adminCode3" : "", 
#        "loc" : [ 42.5833, 1.6667 ], 
#        "latitude" : 42.5833, 
#        "longitude" : 1.6667, 
#        "accuracy" : "6\n" 
#        }
#
# design of the cache datatable 'locationsTable'
#
#        "keyCity"      : "DE|HÜCKELHOVEN",
#        "keyStrng"     : "DE|41836",                               this item will be dropped in the future !!
#        "mngId"        : ObjectId("4eae453fc9a3710f1cebe719"), 
#        "countryCode"  : "DE", 
#        "postalCode"   : "41836", 
#        "placeName"    : "Hückelhoven", 
#        "latitude"     : 6.2197
#        "longitude"    : 51.0608
#
#  18.11.2011  - bervie -     initial realese
#  15.12.2011  - bervie -     added search-key in this form : "DE|41836|H"UCKELHOVEN
#                             the placename is uppercase. before query the user input is also turned into upperecase 
#                             so we are not case sensitiv
#  07.12.2013  - bervie -     ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! 
#                             THE DATA-LOAD-FUNCTIONS in this class are DEPRECREATED !!!! 
#                             IN THE FUTURE WE USE LocDefiner 
#                             ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! 
#
## ***********************************************************************************************************************************************
import clr
clr.AddReference('MongoDB.Bson')
clr.AddReference('MongoDB.Driver')

from MongoDB.Bson import *
from MongoDB.Driver import *
from System.Collections.Generic import *
from System.Web.Configuration import *
from System.Data import *
from System import Array
from System import Convert
from System.Text import StringBuilder
from time import *
from string import *

import traceback            # for better exception understanding
import re
import random
import tls_GeoCalc

class GeoCache:
    '''
    GeoCache Class: nejobas geolocation is based on post-codes
                    this class stores all post-codes and the geo-coordinates of them.
                    locating is based on http://www.geonames.org/
                    to avoid disc-i/o this class has all the stuff in a dataset. 
                    it also supports the geographical calculations by using an instance of the geocalc class
    '''
    # ***********************************************************************************************************************************************
    # constructor 
    #
    # GeoCache is the class that holds all geo-postcode-infos. it is based on a ado.net datatable. for each nation that abbrevation is given in 
    # AppSettings -> nationList it creates a new table with an indexed DataView to search for the postal code
    #
    # 01.11.2011    berndv  initial realese
    # 07.11.2013    bervie  added postcode and placename as dataview
    # ***********************************************************************************************************************************************
    def __call__(self):
        self.__init__()

    def __init__(self, pag):
        try:
            self.log = pag.Application['njbLOG']            # 4 logging
            self.page = pag 
            self.viewDict = {}                              # we create more tha one dataview to speed up searching
            self.regex = re.compile("\s+")                  # split a string to avoid multiple words in the placename

            self.nationLst      = WebConfigurationManager.AppSettings['nationList'].split(';')          # string with national abbrevetions
            self.mngConnStrng   = WebConfigurationManager.AppSettings['mongoConn']                      # connection 2 database
            dbName              = WebConfigurationManager.AppSettings['dbName']                         # get name of db from conf
            self.server = MongoServer.Create(str( self.mngConnStrng) )
            self.njbDb = self.server.GetDatabase(dbName)
            self.collection = self.njbDb.GetCollection("geo.cities")

            self.locTable = DataTable('locationsTable')
            self.prepareTable()                             # create a datatble 4 storing the 

            for nation in self.nationLst:                   # load all data for the nations 
                self.fillTable( nation )

            # ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###    06.01.2013
            kyCol = Array.CreateInstance( DataColumn, 1 ) 
            kyCol[0] = self.locTable.Columns['mngId'] 
            self.locTable.PrimaryKey = kyCol
            # ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  

            # we create the needed dataviews here and add them to our search dictionary
            dtVwGeo = DataView(self.locTable)
            dtVwGeo.Sort = 'latitude, longitude'
            self.viewDict.update({'geo':dtVwGeo})
        
            # 07.11.2013 bervie START
            # added replacement : will search by POSTLEITZAHL or STADTNAME in the future
            #
            #
            dtVwPstCd = DataView(self.locTable)
            dtVwPstCd.Sort = 'postalCode'
            self.viewDict.update({'postalCode': dtVwPstCd })

            dtVwPlcName = DataView(self.locTable)
            dtVwPlcName.Sort = 'placeName'
            self.viewDict.update({ 'geo':dtVwPlcName })
            #
            #
            # 07.11.2013 bervie END

            dtVwPlaceName = DataView(self.locTable)
            dtVwPlaceName.Sort = 'keyCity'
            self.viewDict.update({'keyCity':dtVwPlaceName})

            # !!!  DEPRECATED will not be supported in the future !!!   !!!   !!!   !!!   !!!   !!!   !!!   !!!   !!!   !!!   !!!
            # !!!  DEPRECATED will not be supported in the future !!!   !!!   !!!   !!!   !!!   !!!   !!!   !!!   !!!   !!!   !!!
            # !!!  DEPRECATED will not be supported in the future !!!   !!!   !!!   !!!   !!!   !!!   !!!   !!!   !!!   !!!   !!!
            dtVwKeyStrng = DataView(self.locTable)
            dtVwKeyStrng.Sort = 'keyStrng'
            self.viewDict.update({'keyStrng':dtVwKeyStrng})
            # !!!  DEPRECATED will not be supported in the future !!!   !!!   !!!   !!!   !!!   !!!   !!!   !!!   !!!   !!!   !!!
            # !!!  DEPRECATED will not be supported in the future !!!   !!!   !!!   !!!   !!!   !!!   !!!   !!!   !!!   !!!   !!!
            # !!!  DEPRECATED will not be supported in the future !!!   !!!   !!!   !!!   !!!   !!!   !!!   !!!   !!!   !!!   !!!

            # tell finished
            # self.log.w2lgDbg( 'GeoCache up and running ! Elements in table : ' + str( self.locTable.Rows.Count ) )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # prepareTable( self ): generates a empty datatable for caching all the stuff in the 
    #
    # design of the cache datatable 'locationsTable'
    #
    #        "keyStrng"     : "DE|41836",
    #        "mngId"        : ObjectId("4eae453fc9a3710f1cebe719"), 
    #        "countryCode"  : "DE", 
    #        "postalCode"   : "41836", 
    #        "placeName"    : "Hückelhoven", 
    #        "latitude"     : 6.2197
    #        "longitude"    : 51.0608
    #        "keyCity"      : "DE|HÜCKELHOVEN",
    #
    # 15.12.2011    berndv  initial realese
    # 06.01.2013    bervie  added keyCity to find city by placename
    #
    # ***********************************************************************************************************************************************
    def prepareTable(self):
        col = DataColumn()
        col = self.locTable.Columns.Add("keyStrng", type("String") )
        col = self.locTable.Columns.Add("mngId", type("String") )
        col = self.locTable.Columns.Add("countryCode", type("String") )
        col = self.locTable.Columns.Add("postalCode", type("String") )
        col = self.locTable.Columns.Add("placeName", type("String") )
        col = self.locTable.Columns.Add("latitude", type(1.1) )
        col = self.locTable.Columns.Add("longitude", type(1.1) )
        col = self.locTable.Columns.Add("keyCity", type("String") )

    # ***********************************************************************************************************************************************
    # fillTable : put the data from the mongoDB dictonary into the local datatable. we make an extra-query for each configured nation
    #             this function creates and adds a special-search col to the datatabel : keyStrng = "DE|41836|HÜCKELHOVEN"
    #
    # 15.12.2011    berndv  initial realese
    # 29.12.2011    berndv  added var placeFullName . we only have the first string of the placenam in the key
    #                       the full-name of the place is also stored in the table
    # 01.09.2013    bervie  removed splitting of the keystring
    # 
    # ***********************************************************************************************************************************************
    def fillTable(self, nation):
        try:
            query = QueryDocument("countryCode",nation)
            for city in self.collection.Find(query) :

                # get the strings for creating a special search string
                mongoId = city['_id'].ToString()
                lndCd = city['countryCode'].ToString().upper()
                plz = city['postalCode'].ToString().upper()

                # some plcaNames in the database having more than 1 word in the string. for these special-cases we split the string by whitespaces.
                # this is also done when feeding the location-cache data-table. So for 'Stolberg (Rheinland)' the input 'Stolberg' will be suviciend
                # place = self.regex.split( str(city['placeName']),1 )[0] ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! 
                # example : "DE|HÜCKELHOVEN"
                #placeFullName = city['placeName'].ToString()
                #place = unicode(upper(lndCd + '|' + self.regex.split( placeFullName ,1 )[0] ).upper())
                
                # changed 01.09.2013 : 
                placeFullName = city['placeName'].ToString()
                place = unicode(upper(lndCd + '|' + placeFullName.upper() ) )

                # we create a string with all needed info for querieing a place
                # kyStr = unicode(upper(lndCd + '|' + plz + '|' + place))
                kyStr = unicode(upper(lndCd + '|' + plz))
                
                row = self.locTable.NewRow()
                row['mngId'] = mongoId
                row['keyStrng'] = kyStr
                row['keyCity'] = place
                row['countryCode'] = lndCd
                row['postalCode'] = plz
                row['placeName'] = placeFullName
                row['latitude'] = city['latitude']
                row['longitude'] = city['longitude']
                self.locTable.Rows.Add(row)

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # getCoords : methode is called from client to search for city by a given postal-code and nation-abbrevation 
    #             [example : "DE|41836|HÜCKELHOVEN" ]
    #             THIS METHODE IS USED FOR AJAX CALLS !! !! !! !!
    #
    # 01.11.2011    bervie  initial realese
    # 21.12.2011    bervie  added regEx spliting for placename
    #
    # ***********************************************************************************************************************************************
    def getCoords(self, cntryCd, plz, dorf ):
        try:
            self.log.w2lgDvlp('GeoCache.getCoords() to get the coordinates of encoded:' + dorf )

            # make a unicode string from the with encode translated string (by javascript on the webform)
            countryCode = unicode(self.page.Server.UrlDecode( cntryCd ) )
            postalCode = unicode(self.page.Server.UrlDecode( plz ) )
            place = unicode(self.page.Server.UrlDecode( dorf ) )

            # some plcaNames in the database having mor than 1 word in the string. for these special-cases we split the string by whitespaces.
            # this is also done when feeding the location-cache data-table. So for 'Stolberg (Rheinland)' the input 'Stolberg' will be suviciend
            place = self.regex.split(place,1)[0]
 
            keyStrng = unicode( strip(countryCode) + '|' + strip(postalCode) + '|' + strip(place) )
            keyStrng = upper(keyStrng)
 
            # we are using a dataView for the keystring
            vw = self.viewDict['keyStrng']
            rowIdx = vw.Find(keyStrng)
 
            if rowIdx < 0 :
                self.log.w2lgDvlp('getCoords() not found')
                return 'not found'
            else:
                rslt = str(vw[rowIdx]['latitude'])
                rslt += ';'
                rslt += str(vw[rowIdx]['longitude'])
                self.log.w2lgDvlp('GeoCache - getCoords(): -----  ' + rslt  )

                return rslt 
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # getCoordsByPostcode :     methode is called from client to search for city by a given postal-code and nation-abbrevation 
    #                           [example : "DE|41836" ]
    #
    # 08.12.2012    bervie  initial realese
    # 23.03.2013    bervie  added return of row-idx for the TaggContainer helper class
    # ***********************************************************************************************************************************************
    def getCoordsByPostcode(self, countryCode, postalCode ):
        try:
            keyStrng = upper(unicode( strip(countryCode) + '|' + strip(postalCode) ))
            self.log.w2lgDvlp('GeoCache.getCoordsByPostcode() to get the coordinates of encoded:' + keyStrng )
             
            vwOnPlcNms = self.viewDict['keyStrng']
            filter = "keyStrng = '" + keyStrng + "'"
            vwOnPlcNms.RowFilter = filter

            if vwOnPlcNms.Count == 0 :
                self.log.w2lgDvlp('getCoordsByPostcode() ' + keyStrng + ' NOT FOUND ! ! ')
                return 'not found'
            else:
                rslt = [] 
                rslt.Add( vwOnPlcNms[0]['latitude']  ) 
                rslt.Add( vwOnPlcNms[0]['longitude'] ) 

                rowInTbl = self.locTable.Rows.Find( vwOnPlcNms[0]['mngId'].ToString() )
                tableIdx = self.locTable.Rows.IndexOf( rowInTbl )
                rslt.Add( tableIdx )        # 23.03.2013    bervie  added return of row-idx for the TaggContainer helper class

                # self.log.w2lgDvlp('GeoCache - getCoords(): -----  ' + str(rslt[0]) + ' - ' + str(rslt[1]) )
                return rslt 

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # getPlaces : methode is called from client to get the mongo_ids of places that are inside the given borders.
    #             the places-ids are seperated by ';'
    #             THIS METHODE IS USED FOR AJAX CALLS !! !! !! !!
    #
    # 20.12.2011    berndv  initial realese
    # 30.01.2012    berndv  home-place of the user will be first in the list now
    # ***********************************************************************************************************************************************
    def getPlaces( self, cntryCd, plz, dorf, areaSize):
        try:
            self.log.w2lgDvlp('GeoCache.getPlaces() called with :' + cntryCd + plz + dorf + areaSize )
            coords = self.getCoords(cntryCd, plz, dorf).split(';')

            # prepare the fucking middle of the service area
            theMiddle = tls_GeoCalc.GeoCalc(self.page, coords[0], coords[1] )
            corners = theMiddle.getAreaCorners(areaSize).split(';')

            # get the places inside the borders
            expr = "((latitude > " + str(corners[2]) + " AND latitude < "  + str(corners[0] + " )")
            expr += " AND ( longitude > " + str(corners[1]) + " AND longitude < " + str(corners[3]) + " ))" 

            rws = self.locTable.Select(expr)
            # self.log.w2lgDvlp('GeoCache - getPlaces() Params : -----  ' + expr  )
            # self.log.w2lgDvlp('GeoCache - getPlaces() Number of answers : -----  ' + str(len(rws) )  )

            bldLst = []
            placename = upper(dorf)
            for r in rws:
                newItem = unicode(r[1] + "|" + r[0] + "|" + unicode(r[5]) + "|" + unicode(r[6]) + ';')
                self.log.w2lgDvlp('GeoCache - getPlaces() item to add     ' + newItem )

                self.log.w2lgDvlp('GeoCache - getPlaces() newItem ' + newItem )
                if r[0].find(plz) > 0 :
                    if r[0].find(placename) > 0 :
                        # self.log.w2lgDvlp('GeoCache - getPlaces() inserted first  ' + newItem )
                        bldLst.insert(0,newItem)
                    else:
                        # self.log.w2lgDvlp('GeoCache - getPlaces()       inserted  ' + newItem )
                        bldLst.append(newItem)
                else:
                    # self.log.w2lgDvlp('GeoCache - getPlaces()       inserted  ' + newItem )
                    bldLst.append(newItem)

            self.log.w2lgDvlp('GeoCache - getPlaces() length of list  ' + str(len(bldLst)) )

            # old fashioned type - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            result = unicode('')
            for itm in bldLst :
                result += itm 
            return result
            # old fashioned type - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

            # new fashioned type - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            #rsltAsTxt = StringBuilder(200)
            #for itm in bldLst : 
            #    rsltAsTxt.Append( unicode( itm ) )
            #return rsltAsTxt.ToString()
            ## new fashioned type - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # getPlacesByPostcode :     methode is called from client to get the mongo_ids of places that are inside the area of the user
    #                           it returns a list orderd by distance to the hometown. this will be added to user-data
    #
    #  parameter : 
    #  cntryCd    - ISO country code
    #  plz       - postcode
    #  areaSize  - size of sqaure which represents the service area size
    #
    #  returns a list with list. the items of the list have the following structure
    #
    #    'mngId'               0 
    #    'keyStrng'            1
    #    'keyCity'             2
    #    'countryCode'         3
    #    'postalCode'          4
    #    'placeName'           5
    #    'latitude'            6
    #    'longitude'           7
    #    calculated distance   8  distance from the middle that were used in the function-call
    #
    #  distance from the middle that were used in the function-call
    #
    # 08.12.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def getPlacesByPostcode( self, cntryCd, plz, areaSize):
        try:
            # self.log.w2lgDvlp('GeoCache.getPlacesByPostcode() called with :' + cntryCd + plz + areaSize )
            coords = self.getCoordsByPostcode(cntryCd, plz )

            if coords == 'not found' : return []    # when nothing was found just return an empty result

            # prepare the fucking middle of the service area
            theMiddle = tls_GeoCalc.GeoCalc(self.page, coords[0], coords[1] )
            corners = theMiddle.getAreaCorners(areaSize).split(';')

            # get the places inside the borders
            expr = "((latitude > " + str(corners[2]) + " AND latitude < "  + str(corners[0] + " )")
            expr += " AND ( longitude > " + str(corners[1]) + " AND longitude < " + str(corners[3]) + " ))" 
            rws = self.locTable.Select(expr)

            bldLst = []
            for r in rws:
                pointInArea = tls_GeoCalc.GeoCalc(self.page, r[5], r[6] )
                distance = theMiddle.distanceTo( pointInArea )
                # newItem = [ r[1], r[0], r[4] ,r[5], r[6], distance ]   # used with user_create.aspx
                newItem = [ r[0], r[1], r[2] ,r[3], r[4],r[5], r[6],r[7], distance ]
                # 'mngId'                  0 
                # 'keyStrng'               1
                # 'keyCity'                2
                # 'countryCode'            3
                # 'postalCode'             4
                # 'placeName'              5
                # 'latitude'               6
                # 'longitude'              7
                # calculated distance      8
                bldLst.append(newItem)

            sortedByDistance = sorted(bldLst, key=lambda tup: tup[8])
            return sortedByDistance

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # ***********************************************************************************************************************************************
    # getPlacesByPlacename :     methode is called from client to get all data of rows with a given placename
    #                            it returns a list orderd by distance to the hometown. this will be added to user-data
    #                            REMARK: the function creates a list with all locations with the given placename. also it adds the post-code-areas
    #                                    that are inside the area-size in kilometers 
    #
    #
    #  parameter : 
    #  cntryCd    - ISO country code
    #  postcode   - postcode
    #  placename  - name of city  [if empty the function olnly returns the area-size
    #  areaSize  -  size of sqaure which represents the service area size
    #
    #  returns a list with CityKeys in that form : DE|41836
    #
    # 30.08.2013    berndv  initial realese
    #
    # 07.11.2013  DEPRECATED  we now have locLstByCity(..)
    #
    # ***********************************************************************************************************************************************
    def getPlacesByPlacename( self, cntryCd, postcode, placename, areaSize ):
        try:
            byPlaceName = []
            byPostCode = []
            
            # 1. get all places with the same placename
            if placename != '':
                reslt = []

                #self.log.w2lgDvlp('GeoCache.getPlacesByPlacename  placename = ' + unicode(placename) + '  is running ' )
                #self.log.w2lgDvlp('GeoCache.getPlacesByPlacename  only place given - postcode:  ' + postcode )
                #self.log.w2lgDvlp('GeoCache.getPlacesByPlacename  only place given - country :  ' + cntryCd  )

                vwOnPlcNms = self.viewDict['keyStrng']
                filter = "keyCity = '" + cntryCd.ToString().upper() + '|' + placename.ToString().upper() + "'"
                vwOnPlcNms.RowFilter = filter

                iCount = 0
                for r in vwOnPlcNms:
                    if postcode is '' :
                        postcode = r[3].ToString()

                    if iCount == 0:
                        coords = self.getCoordsByPostcode(cntryCd, postcode )
                        theMiddle = tls_GeoCalc.GeoCalc(self.page, coords[0], coords[1] )           # prepare the fucking middle of the service area

                    #self.log.w2lgDvlp('-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -' )
                    #self.log.w2lgDvlp('GeoCache.getPlacesByPlacename  only place given - lat     :  ' + unicode(r[5]) )
                    #self.log.w2lgDvlp('GeoCache.getPlacesByPlacename  only place given - lon     :  ' + unicode(r[6]) )
                    #self.log.w2lgDvlp('GeoCache.getPlacesByPlacename  only place given - KeyCity :  ' + unicode(r[7]) )

                    pointInArea = tls_GeoCalc.GeoCalc(self.page, r[5], r[6] )
                    distance = theMiddle.distanceTo( pointInArea )
                    newItem = [ r[0], r[1], r[2] ,r[3], r[4],r[5], r[6],r[7], distance ]
                    byPlaceName.append( newItem )
                    iCount += 1

                byPostCode = self.getPlacesByPostcode( cntryCd, postcode, areaSize)

                # avoid adding the same place twice : generate a list with all CityKeys we have
                keyCities = []
                for place in byPlaceName:
                    keyCities.Add( place[1] )
                    # self.log.w2lgDvlp('GeoCache.getPlacesByPlacename() PLACE found by PLACE-NAME:  ' + place[7].ToString() + ' | ' + place[0].ToString() + ' | ' + place[1].ToString() )

                for place in byPostCode:
                    #self.log.w2lgDvlp('GeoCache.getPlacesByPlacename() PLACE found by POST-CODE:' + place[7].ToString() + ' before adding !!' + ' ' + place[0].ToString() )
                    if place[1] not in keyCities:
                        #self.log.w2lgDvlp('GeoCache.getPlacesByPlacename() PLACE added by POST-CODE:' + place[7].ToString() + ' ' + place[0].ToString() )
                        byPlaceName.Add(place)

                return byPlaceName

            else:
                # get the list with the neigbbourhood by distance
                return self.getPlacesByPostcode( cntryCd, postcode, areaSize)

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # getRowsForCity :     rows of a city 
    #                      
    #  parameter : 
    #  cntryCd     - ISO country code
    #  cityname    - name of the city as given in textbox
    #
    #  returns rows-Array that match the selection-criteria
    #
    # 06.01.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def getRowsForCity( self, cntryCd, cityname ):
        try:
            key = unicode(upper(cntryCd + '|' + self.regex.split( cityname ,1 )[0] ).upper())
            view = self.viewDict['keyCity']
            rslt = view.FindRows(key)

            rows = [] 
            if len(rslt) < 1 :
                self.log.w2lgDvlp('no city found in geoCache.getRowsForCity()')
                return rows
            elif len(rslt) >= 1 :
                for row in rslt:
                    rows.Add( ( [row['mngId'],row['postalCode']] ) )
                    # self.log.w2lgDvlp('geoCache.getRowsForCity() added city : ' + unicode(row['postalCode']) )
                return rows

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # ***********************************************************************************************************************************************
    # findId : get the mongo_Id for a placename
    #
    # 29.12.2011    bervie  initial realese
    # 26.10.2013    bervie  reivented
    # ***********************************************************************************************************************************************
    def findIdByName(self, cntryCode, cityName ):
        try:
            qryStrng = cntryCode + '|' + cityName;
            qryStrng = qryStrng.upper()

            vw = self.viewDict['keyCity']
            rowIdx = vw.Find(qryStrng)
            if rowIdx < 0 :
                self.log.w2lgDvlp('findId.getCoords : error UNKNOWN city no ID was found for ' + qryStrng )
                return False
            else:
                return unicode(vw[rowIdx]['mngId'])

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # ***********************************************************************************************************************************************
    # findIdByPostCode : read the DB-id for a city given by country-code and postcode
    #
    # param : country-code (ISO) &  postcode
    #
    # returns : string :'mongoID|Hueckelhoven'
    #
    # 29.12.2011    bervie  initial realese
    #
    # ***********************************************************************************************************************************************
    def findIdByPostCode(self, cntryCd, postalCode ):
        try:
            self.log.w2lgDvlp('GeoCache.findIdByPostCode() to get the MONGO-Idof encoded:' + unicode(cntryCd) + ' - ' + unicode(postalCode) )

            keyStrng = unicode( strip(cntryCd) + '|' + strip(postalCode)  )
            keyStrng = upper(keyStrng)
 
            vwOnPlcNms = self.viewDict['keyStrng']
            filter = "keyStrng = '" + keyStrng + "'"
            vwOnPlcNms.RowFilter = filter
 
            if vwOnPlcNms.Count == 0 :
                self.log.w2lgDvlp('getCoords() not found for ' + keyStrng )
                return 'not found'
            else:
                rslt = unicode(vwOnPlcNms[0]['mngId'])
                rslt += unicode('|')
                rslt += unicode(vwOnPlcNms[0]['placeName'])
                return rslt 
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # findPlacesById : get the place-data for a given id
    #
    # parameter :  idList       array with mongo_bb_ids
    # returns :    rslt         array with rows of the queried data
    #
    # 30.12.2011    bervie  initial realese
    #
    # ***********************************************************************************************************************************************
    def findPlacesById(self, idList ):
        try:
            self.log.w2lgDvlp('GeoCache.findPlacesById() to get the Data for  :' + str(idList) )
            vw = self.viewDict['mongoId']
            rslt = [] 

            for locId in idList:
                rowIdx = vw.Find(str(locId).strip())
                if rowIdx < 0 :
                    self.log.w2lgDvlp('data not found for ' + str(locId) )
                else:
                    rslt.append( vw[rowIdx].Row.ItemArray )
                    self.log.w2lgDvlp('HURRAY : Found for ' + str(vw[rowIdx].Row) )

            return rslt
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # getRandomPoint : gets a random point near the given starting-point. used for "anonymus" markers on the map
    #
    # parameter :  
    #  lat    : a geographical latitude
    #  long   : a geographical longitude
    #  dist   : distance from the middle
    #
    #
    # returns :
    #  array with geiographical point-data
    #
    #
    # 21.05.2013    bervie  initial realese
    #
    # ***********************************************************************************************************************************************
    def getRandomPoint(self, lat, long, dist ):
        try:
            self.log.w2lgDvlp('GeoCache.getRandomPoint() called to create a new point in the near of' )

            theMiddle = tls_GeoCalc.GeoCalc(self.page, lat, long )

            bearing  = random.uniform( 0.0, 360.0 )
            distance = random.uniform( 0.0, float(dist) )

            self.log.w2lgDvlp('GeoCache.getRandomPoint() PARAM bearing (0-360 deg)  : ' + str( bearing  ) )
            self.log.w2lgDvlp('GeoCache.getRandomPoint() PARAM distance in km       : ' + str( distance ) )
            rndPoint  = theMiddle.destinationPoint( bearing, distance )
            self.log.w2lgDvlp('GeoCache.getRandomPoint() RESULT bearing (0-360 deg)  : ' + str( rndPoint.lat  ) )
            self.log.w2lgDvlp('GeoCache.getRandomPoint() RESULT distance in km       : ' + str( rndPoint.lon ) )



            return rndPoint

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # getKeyStrngFromId : get the keystring by the mongo-id of a place
    #
    # parameter :  
    #  idList       array with mongo_bb_ids
    #
    # returns :
    #  rslt         array with rows of the queried data
    #
    #
    # 30.12.2011    bervie  initial realese
    #
    # ***********************************************************************************************************************************************
    def getKeyStrngFromId(self, mongoId ):
        try:
            row = self.locTable.Rows.Find(mongoId)
            if row == None : return None
            else : return row['keyStrng'].ToString()

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())
