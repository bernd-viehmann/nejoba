# ***********************************************************************************************************************************************
# UiTools : class comprised the functions that help to survive the daily asp.net confusion
#
# 28.06.2011  - bervie -     initial realese
# ***********************************************************************************************************************************************
import traceback                           # for better exception understanding
import codecs
import math
from System.Web.Configuration import *
import System.Web.UI.WebControls

# ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  
# ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  
class geoMth:
    '''
    geoMth Class: common functions to work with geographical information
    calculate distances, generate points and stuff like that; ported from a java-script class found with google

    toRad               convert DEG to RAD
    toDeg               convert RAD to DEG
    distanceTo          the distance between two points in kilometer
    destinationPoint    go to a point by given angle and distance
    getAreaCorners      generate a rectangel. used for defining search-area

    '''
    # ***********************************************************************************************************************************************
    # constructor : the class will use the python math library and uses a spherical point of view to our planet
    #
    # 13.12.2011  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def __init__(self, page, lat, lon, rad = 6371.0 ):
        try:
            # rad is the radius of our homeplanet. so if you do not have any jobs to promote on mars you must not change this value
            # but nejoba will definitivly ised in outer-space because of the beauty of the code
            self.page = page
            self.log = page.Application['njb_Log']        # get the applicationwide logging mechanism

            # self.log.w2lgDvlp('geoMth - constructor was called !')
            self.lat = lat
            self.lon = lon
            self.radius = rad

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # converting functions for RAD and degres
    #
    # 19.12.2011  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def toRad( self, number ): return float(number) * math.pi / 180.0
    def toDeg( self, number ): return float(number) * 180.0 / math.pi 
    

    # ***********************************************************************************************************************************************
    #
    # function distanceTo ( self, point ):
    #
    # Returns the distance from this point to the supplied point, in km 
    # (using Haversine formula)
    # 
    #  from: Haversine formula - R. W. Sinnott, "Virtues of the Haversine",
    #        Sky and Telescope, vol 68, no 2, 1984
    # 
    #  @param   {LatLon} point: Latitude/longitude of destination point
    #  @returns {Number} Distance in km between this point and destination point
    # 
    # 13.12.2011  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def distanceTo( self, point ):
        try:
            # self.log.w2lgDvlp('geoMth.distanceTo was called ')
            R = self.radius
            lat1 = math.radians(self.lat) 
            lon1 = math.radians(self.lon)
            lat2 = math.radians(point.lat)
            lon2 = math.radians(point.lon)
            dLat = lat2 - lat1
            dLon = lon2 - lon1

            a = math.sin(dLat/2.0) * math.sin(dLat/2.0) + math.cos(lat1) * math.cos(lat2) * math.sin(dLon/2.0) * math.sin(dLon/2.0)
            c = 2.0 * math.atan2( math.sqrt(a), math.sqrt(1.0-a))
            d = R * c

            return d

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    #
    # destinationPoint(self, bearing , distnc):
    #
    # Returns the destination point from this point having travelled the given distance (in km) on the 
    # given initial bearing (bearing may vary before destination is reached)
    #
    #   see http://williams.best.vwh.net/avform.htm#LL
    #
    # @param   {Number} brng: Initial bearing in degrees
    # @param   {Number} dist: Distance in km
    # @returns {LatLon} Destination point
    #
    # 19.12.2011  -bervie-   initial realese
    #
    # ***********************************************************************************************************************************************
    def destinationPoint(self, bearing , distnc):
        try:
            dist = float(distnc)/self.radius  # convert dist to angular distance in radians
            brng = math.radians( bearing )

            lat1 = self.toRad( self.lat )
            lon1 = self.toRad( self.lon )

            lat2 = math.asin( math.sin(lat1) * math.cos(dist) + math.cos(lat1) * math.sin(dist) * math.cos(brng) )
            lon2 = lon1 + math.atan2( math.sin(brng) * math.sin(dist) * math.cos(lat1), math.cos(dist) - math.sin(lat1) * math.sin(lat2))
            lon2 = (lon2 + 3 * math.pi) % ( 2 * math.pi) - math.pi   # normalize to -180/+180 

            result = geoMth( self.page, self.toDeg(lat2), self.toDeg(lon2) )

            return result

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    #
    # getAreaCorners(self, middle , length):
    #
    # The function returns the upper-left and lower-rigth corner of the area. For calculating this you have to tell the middle and the length 
    # of a tangent in the rectangle.
    #
    # param:
    # middle (geoMth) :        the middle of the rectangle
    # length           :        the half-length of the box-size in kilometer
    #
    # returns:
    # geoMth[]        :        an array with the top-left[0] and rigth-down[1]] points of the rectangle
    #
    #   see http://williams.best.vwh.net/avform.htm#LL
    #
    # 20.12.2011  -bervie-   initial realese
    #
    # ***********************************************************************************************************************************************
    def getAreaCorners(self, length):
        try:
            # self.log.w2lgDvlp('geoMth.getAreaCorners was called ')

            northwest = self.destinationPoint( 315.0 ,length )
            southeast = self.destinationPoint( 135.0 ,length )

            # rslt = str(northwest.lat) + ';' + str(northwest.lon) + ';' + str(southeast.lat)  + ';' + str(southeast.lon)
            rslt = ( northwest, southeast )

            return rslt

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())




# ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ##
# ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ##
class LocDefiner:
    '''
    class manages location-infos in nejoba via the session-cacheed user-data-dictionary


Description:

Since november 2013 a decsision was made. from now on nejoba will always use the same location. regardless where it was defined (in which webform),
the saystem will remeber users last choice and will display data for that location or will store new created articles for that location.

To make this possible the LocDefiner-class is responsible. it is used in every webform tha depends on locations and gets current location or stores 
a newly choosen location in the session-cache.

To make it easy the class stores the current used location in the session-cache. there is a dict in the userData-class which already have configuration 
for the session in the session-cache: 
    self.usrData             = page.Session['njbUsrDt'] to access to the session-cache with the user-datacurrent user-configuration
    self.usrData.userDict    = the dictionary with the available config for the current user-session

the LocDefiner-class will use 2 strings in the user-dict to alwas remeber what location we are currently working on :

    - self.usrData.userDict['LCDFNR_MONGOID'] : databse-ID (or a flag showing special state)
    - self.usrData.userDict['LCDFNR_SLCTSTR'] : select-string (stores users input)


    1. LCDFNR_MONGOID
    this string can have three different values 
        '50c2344b773e6f12e007556c' is the mongo-ID of the location nejoba is currently working on.

        'not available' is used if no loc-db-id is available. this is the case if all data (no country, selector = *) or all data 
                        of a country ('DE' for germany) is selected.

        'not found' is used if user tried to define a location (gave a name or postcode) but for the given input there was no entry in the database


    2. LCDFNR_SLCTSTR
    this string can have following values:
        '*|' this means all data should be selected. will not be filteres by location. corresponding LCDFNR_MONGOID-value : 'not available'

        'DE|' means a whole country should be selected. all items for germany for example. corresponding LCDFNR_MONGOID-value : 'not available'

        'DE|41836' user has selected a location by its postcode.example of corresponding LCDFNR_MONGOID-value : '50c2344b773e6f12e007556c'

        'DE|hückelhoven' user has selecteda location by the city-name. example of corresponding LCDFNR_MONGOID-value : '50c2344b773e6f12e007556c'

    the difference between 'DE|hückelhoven' and 'DE|41836':

    it makes a difference if user choose the postcode or the city-name.ifpostcode was choosen ('DE|41836') this postcode-location end the 
    neighbours in the area  will be selected.
    if the user chooses a city-name 'DE|hückelhoven' nejoba will get the first location with that name in the db and adds the neighbour-postcodeareas. 
    additionaly all locations with the same name in the same country will be added also. this is very usefull for big-citieslike Hamburg wherenot 
    all post-code-areas would be choosen if only the items inside the search-area would be added.

    webforms currently using this class :
        C:\Develop\njb_2\Default.aspx.py
  
        C:\Develop\njb_2\Search_Appointment.aspx.py
        C:\Develop\njb_2\Search_Hashtag.aspx.py
        C:\Develop\njb_2\Search_Rubric.aspx.py

        C:\Develop\njb_2\wbf_functs\debate_editor.aspx.py
        C:\Develop\njb_2\wbf_functs\jobs_editor.aspx.py
        C:\Develop\njb_2\wbf_functs\jobs_list.aspx.py
        C:\Develop\njb_2\wbf_functs\jobs_search.aspx.py

    LocDefiner( mongoDbMgr ,countryCode,cityIdentifier,areaSize )  : constructor to load data as given (normaly by user-input)
                                                                     this constructor uses loadFull(..) for loading all places with 
                                                                     the same name and the complete neighbourhood

    Attributes -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  

    self.areaSize   : the size of the rectangle that will be loaded also as neighbourhood

    self.log        : logging-helper class
    self.usrData    : the session-cache-opject with current user/session-data
    self.geoCache   : the cached location-managment
    self.ui         : the ui-helper

    Functions  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  
    
    setLocByInpt        set the class-configuration by string-parameters 
    setLocByDbId        set the class-configuration by a database-id
    
    loadPostCode        the function loads data if postcode was used for the query: it gives a list with the mongoIds of all locations in the area
    loadCityName        if user has given a city-name this function loads all citys of the same country with the same name. use self.getMongoId
    loadCityArea        aggregation of postcode- nad cityname-load. this fct. should be used to load locations when a name is used for query
    
    getValidLoctn         returns True if we have a mongoId in self.MongoId
    
    getLctnsByDstnc     load all post-code-IDs of cities with the same name as ther one given as parameter
    getMongoId          get the databse-id of a location from a given country-code and location-identifier (name or postcode)
    getCityName         get the place-name of first item in the location-list . returns "Aachen" for example
    getPostCode         get the postcode of first item in the location-list . returns "52066" for Burtscheid in Aachen
    getCtryPstCd        returns a string like [DE|41836] (the pair of the country-code and the postcode ) for a given mongo-ID
    getLoctnPrmtr        get the location-parameter used in URLs to make an AJAX-call
    
    checkIfPostCode     returns true if we have a valif postcode for given country 
    itmsFrLocSlct       items for location select : make the population of a location-dropdown-box with one function-call
    itmsFrCtrySlct      items for country-select : populate a country-drop-down-select wih one function call
    createJSON          creates a JSON-encoded string form the array of mongo-ID items given as parameter

    uiFillCtrySlct      fill a country-select dropdown
    uiFillLocSlct       fill a location-select dropdown
    uiInitLocIntfc      init the locations-interface the Page_PreRender function

    '''

    # ***********************************************************************************************************************************************
    # constructor   : helper-class for location-data. the current location comes from the session-cache
    # 
    # param  :  page            : ASP.net WebPage-Calss for accessing the application-cache
    #           areaSize        : the area that is used to find the neighbours (it is a rectangle used for the search)
    #                             if None (nothing defined) function will use the settings in the web.config
    #
    # 06.11.2013    bervie  initial realese
    #
    # ***********************************************************************************************************************************************
    def __init__( self , page , areaSize = None ):
        # store the parameter 
        self.Page       = page                      # ASP.net Page-instance
        if areaSize is not None:
            self.areaSize = areaSize                # the size of the rectangle that will be loaded also as neighbourhood
        else:
            self.areaSize = System.Convert.ToDecimal( WebConfigurationManager.AppSettings['areaSize'] )

        self.log        = page.Application['njbLOG']        # get the applicationwide logging mechanism
        self.usrData    = page.Session['njbUsrDt']          # access to the session-cache with all the user-data
        self.geoCache   = page.Application['njbGeoSrc']     # the source of locations
        self.ui         = page.Application['njbUi']         # helper for the user-interface

        # self.mongoid stores the value form userDict['LCDFNR_MONGOID']
        # self.select stores the value form userDict['LCDFNR_SLCTSTR']
        #
        # insert location-infos from the session-cache. if there is nothing stored yet insert the default to select all
        if self.usrData.userDict.has_key('LCDFNR_MONGOID'):
            self.mongoId = self.usrData.userDict['LCDFNR_MONGOID']
        else:
            # nothing in the usr-data-cache : we insert the default for session-startup
            self.usrData.userDict['LCDFNR_MONGOID'] = 'not available'
            self.mongoId = 'not available'

        if self.usrData.userDict.has_key('LCDFNR_SLCTSTR'):
            self.select = self.usrData.userDict['LCDFNR_SLCTSTR']
        else:
            # nothing in the usr-data-cache : we insert the default for session-startup 
            # '*|' means show all data location-independent
            self.usrData.userDict['LCDFNR_SLCTSTR'] = '*|'
            self.select = '*|'


    # ***********************************************************************************************************************************************
    # setLocByInpt :    set the class-configuration by string-parameters 
    #                   if a postcode was given the function loads the postcode and the neighbours
    #                   if a city-name was given the function returns the list of cities with the given name
    #                   it retunrs a list of rows in the location-table. ordered by distance
    #
    # parameter    : countryCode     : 'DE' for germany
    #                cityIdentifier  : can be the postcode or the city-name
    #
    # returns      : Nothing 
    #
    # 28.11.2013    bervie  initial realese
    #
    # ***********************************************************************************************************************************************
    def setLocByInpt( self, countryCode , cityIdentifier ): 
        try:
            # if no city-name or postcode is defined we have a super-select
            # '*|' means that the select does not depend on the location ( THE LIST-ITEM VALUE OF THE COUNTRY-SELECT MUST BE '*' )
            # 'DE|' means we have a to select all data of a country
            if len(cityIdentifier.strip() ) == 0:
                self.usrData.userDict['LCDFNR_MONGOID'] = self.mongoId = 'not available'
                self.usrData.userDict['LCDFNR_SLCTSTR'] = self.select = countryCode + '|'
                return

            # check if input makes scense and a location exists for the input
            self.mongoId = self.getMongoId( countryCode, cityIdentifier )

            # if no location was found mark that in the session-cache
            if self.mongoId is False:
                self.usrData.userDict['LCDFNR_MONGOID'] = self.mongoId = 'not found'
                self.usrData.userDict['LCDFNR_SLCTSTR'] = self.select = System.String.Empty

                self.log.w2lgError('LocDefiner->setLocByInpt : no location found for countryCode : ' + countryCode + ' ;cityIdentifier : ' + cityIdentifier )
                return False

            else:
                self.usrData.userDict['LCDFNR_SLCTSTR'] = self.select = countryCode.strip() + '|' + cityIdentifier.strip()  # 'DE|41835' or 'DE|ERKELENZ'
                self.usrData.userDict['LCDFNR_MONGOID'] = self.mongoId                                                      # '5c6776f32....'

                if self.checkIfPostCode( countryCode, cityIdentifier ) is True:
                    return self.loadPostCode()                  # load the List of neighbours by postcode
                else:
                    return self.loadCityName()                  # load all places with same name and the neighbours nearer than defined in areasize 

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # setLocByDbId : set the class-configuration by a database-id
    #                 it retunrs a list of rows in the location-table. ordered by distance
    #
    # parameter    : countryCode     : 'DE' for germany
    #                cityIdentifier  : can be the postcode or the city-name
    #                loadByPostCode = True : the locations in the neighbourhood are loaded
    #                                 False : Cities with the same name are loaded
    #
    # returns      : List with the db-ids ordered by distance from start-town 
    #
    # 28.11.2013    bervie  initial realese
    #
    # ***********************************************************************************************************************************************
    def setLocByDbId( self, mongoPrmId, loadByPostCode = True ): 
        try:
            self.mongoId = mongoPrmId
            loctnRw = self.geoCache.locTable.Rows.Find( mongoPrmId )

            # if no location was found mark that in the session-cache
            if loctnRw is None:
                self.usrData.userDict['LCDFNR_MONGOID'] = self.mongoId = 'not found'
                self.usrData.userDict['LCDFNR_SLCTSTR'] = self.select = System.String.Empty
                self.log.w2lgError('LocDefiner->setLocByDbId : no location found for mongoID : ' + mongoPrmId )
                return False

            if loadByPostCode is True:
                self.select = loctnRw['countryCode'].ToString() + '|' + loctnRw['postalCode'].ToString()
            else:
                self.select = loctnRw['countryCode'].ToString() + '|' + loctnRw['placeName'].ToString()

            self.usrData.userDict['LCDFNR_SLCTSTR'] = self.select
            self.usrData.userDict['LCDFNR_MONGOID'] = self.mongoId

            if loadByPostCode is True:
                return self.loadPostCode()                  # load the List of neighbours by postcode
            else:
                return self.loadCityName()                  # load all places with same name and the neighbours nearer than defined in areasize 

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # loadPostCode : the function loads data if postcode was used for the query: it gives a list with the mongoIds of all locations in the area
    #
    # parameter        getRows = True   : the complete rows are returned as List
    #                            False  : only the DB-Ids are returned as List
    #
    # returns          a list with the rows from location table sorted by distance
    #                  HINT : the area-size defined in constructor is used for getting the neighbours needed
    #
    # 28.11.2013    bervie  initial realese
    # ***********************************************************************************************************************************************
    def loadPostCode( self, getRows = True ):
        try:
            centralCity = self.geoCache.locTable.Rows.Find( self.mongoId )

            # if no location was found we have an error !
            if centralCity is None:
                # no location found. this is marked in the session-cache with 'not found'
                self.log.w2lgError('LocDefine.loadPostCode : location not found  : ' + self.mongoId )
                self.usrData.userDict['LCDFNR_MONGOID'] = self.mongoId = 'not found'
                self.usrData.userDict['LCDFNR_SLCTSTR'] = self.select = System.String.Empty
                return

            middle = geoMth(self.Page, centralCity['latitude'] ,centralCity['longitude'] )
            edges = middle.getAreaCorners( self.areaSize  )
            northwest = edges[0]
            southeast = edges[1]

            # create the geo-rectangle. all locations inside will be added as neighbourhood
            expr = "((latitude > " + str(southeast.lat) + " AND latitude < "  + str(northwest.lat) + " )"
            expr += " AND ( longitude > " + str(northwest.lon) + " AND longitude < " + str(southeast.lon) + " ))" 
            #self.log.w2lgDbg('LocDefiner.loadPostCode() query-expression : ' + expr )

            rws = self.geoCache.locTable.Select(expr)
            return self.getLctnsByDstnc( middle, rws, getRows )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # loadCityName : if user has given a city-name this function loads all citys of the same country with the same name. use self.getMongoId  
    #                to figure out what parameter must be given (mongoID)
    #
    # parameter        getRows = True   : the complete rows are returned as List
    #                            False  : only the DB-Ids are returned as List
    #                  
    # returns          a list with the rows from location table sorted by distance
    #
    # 28.11.2013    bervie  initial realese
    # ***********************************************************************************************************************************************
    def loadCityName( self, getRows = True ):
        try:
            cityByName = self.geoCache.locTable.Rows.Find( self.mongoId )

            # if no location was found we have an error !
            if cityByName is None:
                # no location found. this is marked in the session-cache with 'not found'
                self.log.w2lgError('LocDefine.loadPostCode : location not found  : ' + self.mongoId )
                self.usrData.userDict['LCDFNR_MONGOID'] = self.mongoId = 'not found'
                self.usrData.userDict['LCDFNR_SLCTSTR'] = self.select = System.String.Empty
                return

            cityKey = cityByName['keyCity'].ToString()
            middle = geoMth(self.Page, cityByName['latitude'] ,cityByName['longitude'] )

            vwOnPlcNms = self.geoCache.viewDict['keyStrng']
            filter = "keyCity = '" + cityKey + "'"
            vwOnPlcNms.RowFilter = filter

            return self.getLctnsByDstnc( middle, vwOnPlcNms, getRows )


        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # loadCityArea : aggregation of postcode- nad cityname-load. this fct. should be used to load locations when a name is used for query
    # 
    # parameter    : getRows = True  : if true the function returns the complete row-data sorted by distance
    #                          False : if False the function returns the database-ids of the locations
    #
    # returns      : a list with the rows found in the 
    #
    # 28.11.2013    bervie  initial realese
    # ***********************************************************************************************************************************************
    def loadCityArea( self, getRows = True ): 
        try:
            centralCity = self.geoCache.locTable.Rows.Find( self.mongoId )
            # if no location was found we have an error !
            if centralCity is None:
                # no location found. this is marked in the session-cache with 'not found'
                self.log.w2lgError('LocDefine.loadCityArea : location not found  : ' + self.mongoId )
                self.usrData.userDict['LCDFNR_MONGOID'] = self.mongoId = 'not found'
                self.usrData.userDict['LCDFNR_SLCTSTR'] = self.select = System.String.Empty
                return

            middle = geoMth(self.Page, centralCity['latitude'] ,centralCity['longitude'] )

            # create a list of smae-name-locations and the neighbours in the area
            pstCdLst = self.loadPostCode( self.mongoId )
            cityList = self.loadCityName( self.mongoId )
            mergedLst = cityList
            for itm in pstCdLst:
                if itm not in mergedLst:
                    mergedLst.Add(itm)

            rows = []
            for itm in mergedLst:
                row = self.geoCache.locTable.Rows.Find( itm )
                rows.Add(row)

            rowsByDistnce = self.getLctnsByDstnc( middle, rows, True )

            if getRows : return rowsByDistnce

            dbIds = []
            for item in rowsByDistnce:
                #self.log.w2lgDbg('  ---  for item in rowsByDistnce:  -- : ' + str(item) )
                dbIds.Add( item['mngId'].ToString() )

            return dbIds

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # getValidLoctn : returns True if we the last search was succesfull or we have a valid location/country or search_all_location flag
    #
    # parameter    : none
    #
    # returns      : None   : there was an error in the last location-search
    #                '*|'  : currently all locations were selected ('*|')
    #                'DE'   : the country-ISO code is retrurned if currently a country like 'DE"=germany is valid
    #                '5c89...' : a mongo_id as string is rreturned if currently a location is valid (=postcode-area)
    #
    # HINT : if you want need to check for mongo-id (exact location is valid) just check for [  if (len(returnValue) > 2):  ]
    #
    # 30.11.2013    bervie  initial realese
    #
    # ***********************************************************************************************************************************************
    def getValidLoctn( self ): 
        try:
            if self.mongoId == 'not found' :           # (self.mongoId != 'not available') is not a failure->therefor not mentioned here
                return None
            elif self.mongoId == 'not available' :
                if self.select =='*|':
                    return '*|'
                else:
                    return self.select.split('|')[0]    # return the ISO-country-code like 'DE'

            return self.mongoId

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # getLctnsByDstnc : load all post-code-IDs of cities with the same name as ther one given as parameter
    #
    #
    # parameter    :middle  : the middlepoint as instance of geoMth-class 
    #               rows    : rows from the location-table sorted
    #               getRows : boolean flag 
    #                         if "True" the function returns the rows
    #                         if "False" the function only returns the database-ids
    #
    # returns      : a list of the mongo-ids sorted by distance
    #
    # 10.11.2013    bervie  initial realese
    #
    # ***********************************************************************************************************************************************
    def getLctnsByDstnc( self, middle, rows, getRows = False  ): 
        try:
            # create a list of tuples : ( row, distance_in_kilometer )
            tempRslt = []
            for snglRw in rows:
                pointOfLoc = geoMth( self.Page, snglRw['latitude'], snglRw['longitude'])
                distance = middle.distanceTo( pointOfLoc )
                newby = (snglRw['mngId'],distance)
                tempRslt.Add(newby)

            # sort the result-set by distance and create a list of db_items
            sortedByDistance = sorted(tempRslt, key=lambda tup: tup[1])

            if getRows == True:
                # if the complete data is needed create a list of rows sorted by distance
                rows = []
                for tpl in sortedByDistance : rows.Add( self.geoCache.locTable.Rows.Find(tpl[0]) )
                return rows
            else:
                # if only the database-ids are wanted:
                mongoIds = []
                for tpl in sortedByDistance : mongoIds.Add( tpl[0] )
                return mongoIds

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # getMongoId : get the databse-id of a location from a given country-code and location-identifier (name or postcode)
    #
    # parameter    : countryCode     ISO-code of the coutry ('DE' for deutschland
    #                cityIdentifier  can be a kind of digit for the postcode
    #                                or the name of the city as string (first occurence in the database will be taken )
    #
    # returns      : String with the mongoID of the item
    #                HINT: if a name of city was given the function finds the first occurence of this name
    #
    # 09.11.2013    bervie  initial realese
    #
    # ***********************************************************************************************************************************************
    def getMongoId( self, countryCode, cityIdentifier ):
        try:
            cityIdentifier = cityIdentifier.strip()
            countryCode = countryCode.strip()

            # check if country is supported on this server 
            if countryCode not in self.geoCache.nationLst:
                return False

            if self.checkIfPostCode( countryCode, cityIdentifier ) is True:         # if we have a postcode (numeric) get ID by postcode
                dtVw = self.geoCache.viewDict['postalCode']
                filter = "postalCode = '" + cityIdentifier + "'"
                dtVw.RowFilter = filter
            else:                                                                   # if we have the city-name get id by "DE|H?CKELHOVEN"
                dtVw = self.geoCache.viewDict['keyCity']
                filter = "keyCity = '" + countryCode + "|" + cityIdentifier + "'"
                dtVw.RowFilter = filter

            # if nothing was found return false
            if dtVw.Count == 0 :
                self.log.w2lgError('LocDefine.getMongoId : location not found ! country-code : ' + countryCode + ' ; ' + cityIdentifier )
                return False

            # we have to check if the countryCode in results is same then user-search-input
            for row in dtVw:
                if row['countryCode'] == countryCode.ToString().strip():
                    mongoId = row['mngId'].ToString()
                    #self.log.w2lgDvlp('LocDefiner.getMongoId() : ' + countryCode + "|" + cityIdentifier + "'" + ' was succesfull, mongoId = ' + mongoId)
                    return mongoId

            # when there was no row with matching country-code the user migth choose the wrong country
            #self.log.w2lgDvlp('LocDefiner.getMongoId() : ' + countryCode + "|" + cityIdentifier + "'" + '   WAS NOT FOUND BECUASE OF countryCode ! ')
            return False
            

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # getCityName : get the place-name of first item in the location-list . returns "Aachen" for example
    #
    # parameter    : string with a mongo-id. 
    #                if no string is given the functions gets the first mongo-ID in the local list
    # returns      : String with the Name of the location (human-readable for the UI)
    #
    # 06.11.2013    bervie  initial realese
    #
    # ***********************************************************************************************************************************************
    def getCityName( self, mongoId = None ):
        try:
            if mongoId is None:
                if self.mongoId.startswith('not '):
                    return System.String.Empty
                mongoId = self.mongoId
            
            city = self.geoCache.locTable.Rows.Find( mongoId )
            return city['placeName'].ToString()

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # getPostCode : get the postcode of first item in the location-list . returns "52066" for Burtscheid in Aachen
    #
    # parameter    : string with a mongo-id. 
    #                if no string is given the functions gets the first mogo-ID in the local list
    # returns      : String with the postcode of the location ( without country-code )
    #
    # 06.11.2013    bervie  initial realese
    #
    # ***********************************************************************************************************************************************
    def getPostCode( self, mongoId = None ):
        try:
            if mongoId is None:
                if self.mongoId.startswith('not '):
                    return System.String.Empty
                mongoId = self.mongoId
            
            city = self.geoCache.locTable.Rows.Find( mongoId )
            return city['postalCode'].ToString()

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # ***********************************************************************************************************************************************
    # getCtryPstCd : returns a string like [DE|41836] (the pair of the country-code and the postcode ) for a given mongo-ID
    #
    # parameter    : string with a mongo-id. 
    #                if no string is given the functions gets the first mogo-ID in the local list
    # returns      : String with the country-code | post-code pair  'DE|41836'
    #
    # 27.11.2013    bervie  initial realese
    #
    # ***********************************************************************************************************************************************
    def getCtryPstCd( self, mongoId = None ):
        try:
            if mongoId is None:
                if self.mongoId.startswith('not '):
                    return System.String.Empty

                mongoId = self.mongoId
            
            city = self.geoCache.locTable.Rows.Find( mongoId )
            rslt = city['countryCode'].ToString() + '|' + city['postalCode'].ToString()
            return rslt

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # getLoctnPrmtr : get the location-parameter used in URLs to make an AJAX-call
    #
    # parameter    : string with a mongo-id. 
    #                if no string is given the functions delivers the string build in the constructor
    # returns      : String with the AJAX-Param of the location ( without country-code )
    #
    # 06.11.2013    bervie  initial realese
    #
    # ***********************************************************************************************************************************************
    def getLoctnPrmtr( self, mongoId = None ):
        try:
            if mongoId is None : 
                if self.mongoId.startswith('not '):
                    return System.String.Empty
                mongoId = self.mongoId
            
            city = self.geoCache.locTable.Rows.Find( mongoId )
            paramStrng = 'Loc=' + city['countryCode'].ToString() 
            paramStrng += ',' + city['postalCode'].ToString() 
            paramStrng += '&City=' + city['placeName'].ToString()
            return paramStrng

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # checkIfPostCode : returns true if we have a valif postcode for given country 
    #                   false if the string is not formated as postcode
    #
    # parameter    : string countryCode 'DE' (used later, not all countries have digits as postcode)
    #                string cityIdentifier '41836' or 'neuss'
    #
    # returns      : boolean True  : string is valid postcode for given country
    #                        False : not a postcode
    #
    # 06.11.2013    bervie  initial realese
    #
    # ***********************************************************************************************************************************************
    def checkIfPostCode( self, countryCode, cityIdentifier ):
        try:
            if cityIdentifier.isdigit() : return True
            else : return False

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # itmsFrLocSlct : items for location select : make the population of a location-dropdown-box with one function-call
    #                 the neighbour-postcode-areas. every item is a key-value pair like : 
    #                 the value  : a string representing the CNTRY PSTCD LCTNNM  : "DE 41836 Hueckelhoven"
    #                 the key    : the mongo-ID of the location. 
    #
    #                 can be used to fill up a select in the web-UI
    #
    # parameter :   loadCity = False : loads the locations for postcode
    #                          True  : loads the locations with cityArea
    #
    # returns   :   array with the key/value pairs
    #
    # 06.11.2013    bervie  initial realese
    # ***********************************************************************************************************************************************
    def itmsFrLocSlct( self, loadCity = True ):
        try:
            if loadCity is True:
                locRows = self.loadCityArea()
            else:
                locRows = self.loadPostCode()

            rslt = []

            for itm in locRows:
                text = itm['countryCode'].ToString() + '-' + itm['postalCode'].ToString() + '  ' + itm['placeName'].ToString()
                value = itm['mngId'].ToString()
                #self.log.w2lgDvlp('LocDefiner.itmsFrLocSlct MongoID : ' + value + ' - ' + text )
                rslt.Add( (text,value) )
            return rslt

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # itmsFrCtrySlct : items for country-select : populate a country-drop-down-select wih one function call
    #
    #                  the value  : a string representing the COUNTRY_NAME  : "Dutschland"
    #                  the key    : the ISO-Code of the country
    #
    # parameter :   none
    # returns   :   array with the key/value pairs
    #
    # 15.11.2013    bervie  initial realese
    # ***********************************************************************************************************************************************
    def itmsFrCtrySlct( self ):
        try:
            countryNames = WebConfigurationManager.AppSettings['nationNames_DE'].split(';')
            cntryCds = WebConfigurationManager.AppSettings['nationList'].split(';')
            ctryLst = zip( countryNames, cntryCds )
            return ctryLst

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # createJSON : creates a JSON-encoded string form the array of mongo-ID items given as parameter
    #
    #
    # parameter  : sourceArray : an array of mongo-id-items
    # result     : a string with the array-data coded as JSON
    #
    #
    # 06.11.2013    bervie  initial realese
    #
    # ***********************************************************************************************************************************************
    def createJSON( self , sourceArray ):
        try:
            pass

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # uiFillCtrySlct : fill a country-select dropdown
    #
    # Param             : cntrySelct    : pointer to the asp.net dropdown ctrl
    # returns           :  none
    #
    # 15.11.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def uiFillCtrySlct( self, cntrySelct ):
        try:
            # fill the country-select with the available countries
            cntrySelct.Items.Add( System.Web.UI.WebControls.ListItem('alle vorhandenen','*') )

            for itm in self.itmsFrCtrySlct():
                cntrySelct.Items.Add( System.Web.UI.WebControls.ListItem(itm[0],itm[1]) )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # ***********************************************************************************************************************************************
    # uiFillLocSlct : fill a location-select dropdown
    #
    # TO DO  !  !   TO DO  !  !   TO DO  !  !   TO DO  !  !   TO DO  !  !   TO DO  !  !   TO DO  !  !   TO DO  !  !   TO DO  !  !   TO DO  !  !
    #
    # Param             : lctnSelct    : pointer to the asp.net dropdown ctrl
    # returns           :  none
    #
    # 15.11.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def uiFillLocSlct( self, lctnSelct ):
        try:
            pass
            ## fill the country-select with the available countries
            #cntrySelct.Items.Add( System.Web.UI.WebControls.ListItem('alle vorhandenen','*') )

            #for itm in self.itmsFrCtrySlct():
            #    cntrySelct.Items.Add( System.Web.UI.WebControls.ListItem(itm[0],itm[1]) )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # uiInitLocIntfc : init the locations-interface the Page_PreRender function
    #                  if user has already selected a location it will be inserted into the UI
    #
    # Param             :  none
    # returns           :  none
    #
    # 15.11.2013    berndv  initial realese
    #
    # ***********************************************************************************************************************************************
    def uiInitLocIntfc( self ):
        try:
            self.log.w2lgDvlp('LocDefiner.uiInitLocDef was called '  )

            # pre-fill controls with data from the session-cache
            cntrySel = self.ui.getCtrl('sel_country')
            cntrySel.Items.Clear()
            self.uiFillCtrySlct(cntrySel)

            # toggle viewability of the location-interface to normal mode
            chngDiv = self.ui.getCtrl('div_slct_loctn')
            nrmlDiv = self.ui.getCtrl('div_show_loctn')

            # if no valid location is given show the controls to choose a new location
            curntLoc = self.getValidLoctn()
            if ( curntLoc is None ): # or ( curntLoc == '*|' ): 
                # show location-select- DIV instead of the man-div
                nrmlDiv.Attributes["style"] = " display: none";
                chngDiv.Attributes["style"] = " display: inline";
                return

            # normaly the change-div is hidden, the display-div is shown
            chngDiv.Attributes["style"] = " display: none";
            nrmlDiv.Attributes["style"] = " display: inline";

            currntCntry = self.select.split('|')[0]
            self.ui.getCtrl('sel_country').Items.FindByValue( currntCntry ).Selected = True

            crrntLocSelctn = self.select.split('|')[1]
            if not self.checkIfPostCode( currntCntry, crrntLocSelctn ):
                crrntLocSelctn = self.getCityName()

            if self.ui.ctrlDict.has_key('txbx_city'):
                self.ui.getCtrl('txbx_city').Text = crrntLocSelctn
            if self.ui.ctrlDict.has_key('txbx_location'):
                self.ui.getCtrl('txbx_location').Text = self.getCityName()

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # uiInitProjector : used to initialize a projector: it returns a dict with all config-parameter for chosing the location
    #
    # Param             :  mongoId or none for internal job
    # returns           :  {} dict with the configuration for the controls:
    #                         ['COUNTRY']
    #                         ['CITY']
    #                         ['POSTCODE']
    #
    # 01.12.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def uiInitProjector( self, mongoId = None ):
        try:
            if mongoId == None:
                mongoId = self.mongoId

            reslt = {}

            locn = self.getValidLoctn()

            self.log.w2lgDvlp('LocDefiner.uiInitProjector called with mongoId ' + str(mongoId) )
            self.log.w2lgDvlp('LocDefiner.uiInitProjector called with locn    ' + str(locn) )

            if locn == None:
                # there was an unsuccesfull search for a location
                self.log.w2lgError('LocDefiner->uiInitProjector : Error : no valid location available')
                return None

            # 1. user has no location specified but wants to see all locations available
            if locn == '*|':
                reslt['COUNTRY']  = '*'
                reslt['CITY']     = ''
                reslt['POSTCODE'] = ''

            # 2. user has no location specified but wants to see all locations of a specified country
            if len(locn) == 2:
                reslt['COUNTRY']  = locn
                reslt['CITY']     = ''
                reslt['POSTCODE'] = ''

            # 3. last possibility: we have a valid mongo-id : get the needed stuff from the DB
            if len(locn) > 2:
                slct = self.select.split('|')
                cntry = slct[0]
                locIdf = slct[1]

                if self.checkIfPostCode(cntry,locIdf):
                    reslt['COUNTRY']  = cntry
                    reslt['CITY']     = ''
                    reslt['POSTCODE'] = locIdf
                else:
                    reslt['COUNTRY']  = cntry
                    reslt['CITY']     = locIdf
                    reslt['POSTCODE'] = ''

            return reslt

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())







# ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ##
# ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ##



























# ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  
# ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  
class UiTools:
    '''
    UiTools Class: common functions to work with the userinterface
    provides easy access to the userinterface
    provides email-captcha-system

    num( string )           convert string to numeric
    getCtrlTree             read all control-pointers into an dictonary for easier access
    getCtrl                 find a control from the getCtrlTree-container  HINT : getCtrlTree MUST BE CALLED BEFORE
    findCtrl                find a control by its ID on a nested ASP.NET page
    getCtrlTxt( suffix )    creates a dict with all Text-Attributes of given controls with suffix into a container
    hideFormAfterClick      show a wait-div to prevent user from clicking dump around
    showDivsForUser         user-mngmnt : check the user-rigths and toggle the DIVs depending on the user-permissions
    convertTagsFromInput    create a list of tags from users input
    shorterCoordinate       cut the digits after the comma to 5 digits
    rubricLoadConfiguration function loads the text-files with the definitions for rubrics
    locSearchDefinition     store the current location-info (city that was typed in by the user) into the session-class userData

    '''

    # ***********************************************************************************************************************************************
    # constructor : the class from application-cache is taken if available
    #
    # 29.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def __init__(self, pg):
        try:
            appl = pg.Application
            self.ctrlDict = {}                          # a dictionary with all controls of the webform
            self.inptDict = {}                          # dictionary with txbx-ids as keys and input as values (keys without "txbx_"-suffix
            self.Page = pg                              # logging inside the application cache
            self.log = pg.Application['njb_Log']        # get the applicationwide logging mechanism
            self.user = pg.Session['']

            self.rubricDict = {}                        # memory-container to store the configuration for the rubrics loaded from file
                                                        # used in map-projector; debate-projector and debate-editor webforms
            self.rubricLoadConfiguration()              # load rubric configuration

            self.getCtrlTree( self.Page )            # get the controls data of the given webform

            self.log.w2lgMsg('new UiTools instance created !')
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # num : convert a string to a numeric value
    #
    # 22.06.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def num (self, s):
        try:
            return int(s)
        except exceptions.ValueError:
            return float(s)
        finally:
            return None


    # ***********************************************************************************************************************************************
    # getCtrlTree : read all control-pointers into an dictonary for easier access
    #
    # 13.08.2011  bervie    initial realese
    # ***********************************************************************************************************************************************
    def getCtrlTree( self, rootCtrl ):
        '''
        this function put all IDs and their related contrls into a py-dict
        so we do not have to start a search for them each time we need one
        destination -> self.ctrlDict

        it has to be executed to make the other ctrl-find helper functions useable

        example:
        ui.getCtrlTree( Page.Master )
        ui.getCtrl('txbx_email').Text = mailAdr

        '''
        try:
            if rootCtrl is not None:
                if rootCtrl.HasControls():
                    for ctrl in rootCtrl.Controls:
                        self.ctrlDict.update( {ctrl.ID:ctrl} )
                        self.getCtrlTree(ctrl)
                else:
                    self.ctrlDict.update( {rootCtrl.ID:rootCtrl} )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # findCtrl : find a control by its ID on a nested ASP.NET page
    #
    # 22.06.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def findCtrl(self, starter, id):
        '''
        find a control by its ID on a nested ASP.NET page

        usage : ui.findCtrl(Page.Master , ID-NAME)
        '''
        try:
            self.startCtrl = starter
            self.identy = id

            if starter == None:
                return 

            if starter.ID == id:
                return starter
            else:
                for c in self.startCtrl.Controls:
                    fnd = self.findCtrl(c, self.identy)
                    if fnd != None:
                        return fnd
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # getCtrl  find a control from the getCtrlTree-container
    #
    # 27.06.2011  bervie    initial realese
    # ***********************************************************************************************************************************************
    def getCtrl( self, ctrlName ):
        '''
        gives back a reference to the asked control
        !!! YOU MUST HAVE STARTED getCtrlTree BEFORE !!!

        usage :  getCtrl( "ID OF THE CTRL YOU ARE LOOKING FOR" )

        example:
        uih.getCtrlTree( Page.Master )
        uih.getCtrl('txbx_email').Text = mailAdr
        '''
        if self.ctrlDict.ContainsKey( ctrlName ):
            return self.ctrlDict[ ctrlName ]
        else:
            return None


    # ***********************************************************************************************************************************************
    # getCtrlTxt   creates a dict with all Text-Attributes of a given control into container
    #
    # 22.06.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def getCtrlTxt(self, suffx='txbx_' ):
        '''
        search for all controls with a given suffix in the name and copy 
        the Text-Property with bare-control name into a dictionary
        destination -> self.inptDict

        example
        getCtrlTxt( 'SUFFIX_OF_THE_CTRL_ID' )
        '''
        try:
            ids = self.ctrlDict.keys()

            for itm in ids:
                if itm == None:
                    break

                if itm.count(suffx,0, (len(suffx)) ) > 0:
                    # fill the dict. the keys are the ID without the suffix
                    ky = itm.lstrip(suffx)
                    vl = self.ctrlDict[itm].Text

                    self.inptDict.update( {ky:vl} )
                    # self.log.w2lgDvlp("getCtrlTxt : " + ky + ";" + vl )
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # setCtrlTxt    fills all controls with a given ID-Suffix with the values of dictionary 
    #
    # 22.06.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def setCtrlTxt(self, info, delSuffx = '@', addSfx = 'txbx_'):
        '''
        function fills all controls with a given ID-Suffix with the values 
        of dictionary. fct is able to delete chars at the beginning matching 
        the delSuffx

        param:
         infoDict  = the parameter-dictionary.  
         delSuffx  = the string given here will be delete from the key-params 
                     normaly it is used to delete the leading @ from the sql-parameter
         addSfx    = the string will be added in front of the ID-string
             
        you have to take care of the naming-conventions in the system:
        without their leading suffixes the control-ID must be same as the SQL-paramters 

        example:
        answer = bsLg.readUser(mailAdr)     # gives a dict. with the data for UI
        uih.setCtrlTxt(answer)

        '''
        try:
            for ky in info:
                # build a key matching the ctrl-name
                ctrlId = addSfx + ky.lstrip(delSuffx)
                self.ctrlDict[ctrlId].Text = unicode(info[ky])
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # hideFormAfterClick : show a wait-div to prevent user from clicking dump around
    #
    # 22.06.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def hideFormAfterClick( self ):
        '''
        function toggles between main-canvas div and hidden div to ask user to wait.
        this will be prevent dump stupids to press the button a thousand times while server is meditating

        function depends on javascript-function in master-page that hides the normal and shows the please 
        '''
        try:
            # define naming-parts that should lead into a disabeled input state
            disbl = ['btn_','hyLnk_','setRbrc_']
            for id in self.ctrlDict:
                if id:
                    for abbrv in disbl:
                        if id.Contains( abbrv ):
                            # self.log.w2lgDvlp( ' UI.hideFormAfterClick ID found : ' + str(id))
                            self.getCtrl(id).Attributes.Add("onclick", "hideAfterClick();")

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # showDivsForUser : check the user-rigths and toggle the DIVs depending on the user-permissions
    #
    # 22.06.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def showDivsForUser( self, row , currentPage):
        '''
        the function showDivsForUser is used to show/hide the DIVS in the editors that the user is allowed to see
        part of user-managment

            DIVS with following IDs are used: 

            YES_WE_CAN              : this div will be shown if user is allowed to use the functions
            INVITE_VISITOR          : the user is only a visitor. invite him to nejoba
            OFFER_PREMIUM_ACCOUNT   : user has account but is not a payer. ask him to spend money to get functions directly

         param : 
               row         : the row that should be displayed will be asked when it was created
               currentPage : the currently active webpage for getting ctrls out of it
        '''
        try:
            # special-case : if we are in the job-trial-editor and no iother user has made an offer 
            # the user should not be able to send an offer to himself
            #
            # WILL BE MADE IN THE NEAR FUTURE
            #

            # prepare UI stuff
            uiHlp = self.Page.Application['njbUi']
            uiHlp.getCtrlTree(currentPage)
            YesWeCan                = uiHlp.getCtrl('YES_WE_CAN')
            InviteVisitor           = uiHlp.getCtrl('INVITE_VISITOR')
            OfferPremiumAccount     = uiHlp.getCtrl('OFFER_PREMIUM_ACCOUNT')
            YourOwnOffer            = uiHlp.getCtrl('YOUR_OWN_OFFER')

            if (not YesWeCan) or (not InviteVisitor) or (not OfferPremiumAccount) or (not YourOwnOffer) : return

            # we have an visitor. means he isn't logged in. show him stuff in 'INVITE_VISITOR' DIV
            if not self.userDict.Contains('account_roles'):
                YesWeCan.Visible            = False
                InviteVisitor.Visible       = True
                OfferPremiumAccount.Visible = False
                YourOwnOffer.Visible        = False
                return

            # when user is a payer he can use stuff in 'YES_WE_CAN' DIV
            elif self.userDict['account_roles'].Contains('premium'):
                YesWeCan.Visible            = True
                InviteVisitor.Visible       = False
                OfferPremiumAccount.Visible = False
                YourOwnOffer.Visible        = False
                return

            # user has a free account. check if the premium periode is offer or not
            elif not self.userDict['account_roles'].Contains('premium'):
                # calculate time difference to make the item public
                premiumHours = System.Convert.ToInt64( WebConfigurationManager.AppSettings['PremiumAdvantageHours'] )
                hours   = System.TimeSpan( premiumHours, 0, 0 )
                premEnd = row['creationTime'].Add( hours ) 
                now     = System.DateTime.UtcNow
                diff    = premEnd.Subtract(now).Ticks

                # the item is public if the difference between premiumEnd - now is < 0  => show the editor
                if diff < 0:
                    YesWeCan.Visible            = True
                    InviteVisitor.Visible       = False
                    OfferPremiumAccount.Visible = False
                    YourOwnOffer.Visible        = False
                    return
                # if item still is not public show the user the 'OFFER_PREMIUM_ACCOUNT'-div
                else:
                    YesWeCan.Visible            = False
                    InviteVisitor.Visible       = False
                    OfferPremiumAccount.Visible = True
                    YourOwnOffer.Visible        = False
                    return
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # convertTagsFromInput : function makes a useable list from the input in a hashtag
    #
    #
    # 22.06.2011    berndv  initial realese
    # 28.04.2013    berndv  added remove of leading '#'
    # ***********************************************************************************************************************************************
    def convertTagsFromInput(self, usrInpt):
        '''
            generate a list with all hashtags in a given text
            Param : userInput : the string given in the edit
            returns : a list with all tags as seperate item
        '''
        try:
            result = []
            #tags = usrInpt.lower().split(',')
            # 
            tags = usrInpt.upper().split(',')
            #
            #
            #
            #
            for itm in tags:
                itm.strip()

                # remove leading '#'
                while itm[0] == '#':
                    itm = itm[1:]

                if len(itm) > 0:
                    result.Add( itm )
                
            return result

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())

    # ***********************************************************************************************************************************************
    # shorterCoordinate : function truncates the length os a coordinate given by the user. 5 places after the comma is enough :D
    #
    # Param : userInput : the string given in the textbox
    # returns           : a string with only 5 digits
    #
    # 22.06.2011    berndv  initial realese
    # 28.04.2013    berndv  added remove of leading '#'
    # ***********************************************************************************************************************************************
    def shorterCoordinate(self, usrInpt):
        try:
            rslt = usrInpt + '0000000'
            locOfComma = rslt.find('.')
            return rslt[:locOfComma + 7].strip('0')

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # rubricLoadConfiguration : load rubric-configuration from the files in AppDate and put it into a simple memory-cache [ self.rubricDict = {} ]
    #
    # Param             :  none
    # returns           :  none
    #
    # 28.04.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def rubricLoadConfiguration( self ):
        try:
            tmpltPath = self.Page.Server.MapPath( WebConfigurationManager.AppSettings['ANNONCE_MATRIX'] )
            f = codecs.open(tmpltPath, "r", "utf-8")
            activitySource = f.read()
            f.close()
            self.rubricDict['ANNONCE_MATRIX'] = activitySource

            tmpltPath = self.Page.Server.MapPath( WebConfigurationManager.AppSettings['ASSOCIATION_MATRIX'] )
            f = codecs.open(tmpltPath, "r", "utf-8")
            activitySource = f.read()
            f.close()
            self.rubricDict['ASSOCIATION_MATRIX'] = activitySource

            tmpltPath = self.Page.Server.MapPath( WebConfigurationManager.AppSettings['BUSINESS_MATRIX'] )
            f = codecs.open(tmpltPath, "r", "utf-8")
            activitySource = f.read()
            f.close()
            self.rubricDict['BUSINESS_MATRIX'] = activitySource

            tmpltPath = self.Page.Server.MapPath( WebConfigurationManager.AppSettings['DEMOCRACY_MATRIX'] )
            f = codecs.open(tmpltPath, "r", "utf-8")
            activitySource = f.read()
            f.close()
            self.rubricDict['DEMOCRACY_MATRIX'] = activitySource

            tmpltPath = self.Page.Server.MapPath( WebConfigurationManager.AppSettings['EVENT_MATRIX'] )
            f = codecs.open(tmpltPath, "r", "utf-8")
            activitySource = f.read()
            f.close()
            self.rubricDict['EVENT_MATRIX'] = activitySource

            tmpltPath = self.Page.Server.MapPath( WebConfigurationManager.AppSettings['HOBBY_MATRIX'] )
            f = codecs.open(tmpltPath, "r", "utf-8")
            activitySource = f.read()
            f.close()
            self.rubricDict['HOBBY_MATRIX'] = activitySource

            tmpltPath = self.Page.Server.MapPath( WebConfigurationManager.AppSettings['INITIATIVE_MATRIX'] )
            f = codecs.open(tmpltPath, "r", "utf-8")
            activitySource = f.read()
            f.close()
            self.rubricDict['INITIATIVE_MATRIX'] = activitySource

            tmpltPath = self.Page.Server.MapPath( WebConfigurationManager.AppSettings['LOCATION_MATRIX'] )
            f = codecs.open(tmpltPath, "r", "utf-8")
            activitySource = f.read()
            f.close()
            self.rubricDict['LOCATION_MATRIX'] = activitySource

            tmpltPath = self.Page.Server.MapPath( WebConfigurationManager.AppSettings['LONELY_HEARTS_AD_MATRIX'] )
            f = codecs.open(tmpltPath, "r", "utf-8")
            activitySource = f.read()
            f.close()
            self.rubricDict['LONELY_HEARTS_AD_MATRIX'] = activitySource

            tmpltPath = self.Page.Server.MapPath( WebConfigurationManager.AppSettings['PET_MATRIX'] )
            f = codecs.open(tmpltPath, "r", "utf-8")
            activitySource = f.read()
            f.close()
            self.rubricDict['PET_MATRIX'] = activitySource

            tmpltPath = self.Page.Server.MapPath( WebConfigurationManager.AppSettings['RIDE_SHARING_MATRIX'] )
            f = codecs.open(tmpltPath, "r", "utf-8")
            activitySource = f.read()
            f.close()
            self.rubricDict['RIDE_SHARING_MATRIX'] = activitySource

            tmpltPath = self.Page.Server.MapPath( WebConfigurationManager.AppSettings['STARTUP_MATRIX'] )
            f = codecs.open(tmpltPath, "r", "utf-8")
            activitySource = f.read()
            f.close()
            self.rubricDict['STARTUP_MATRIX'] = activitySource

            tmpltPath = self.Page.Server.MapPath( WebConfigurationManager.AppSettings['SWAP_MATRIX'] )
            f = codecs.open(tmpltPath, "r", "utf-8")
            activitySource = f.read()
            f.close()
            self.rubricDict['SWAP_MATRIX'] = activitySource

            tmpltPath = self.Page.Server.MapPath( WebConfigurationManager.AppSettings['FAMILY_MATRIX'] )
            f = codecs.open(tmpltPath, "r", "utf-8")
            activitySource = f.read()
            f.close()
            self.rubricDict['FAMILY_MATRIX'] = activitySource



            # ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   
            # ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   
            tmpltPath = self.Page.Server.MapPath( WebConfigurationManager.AppSettings['FAMILY_MATRIX'] )
            f = codecs.open(tmpltPath, "r", "utf-8")
            activitySource = f.read()
            f.close()
            self.rubricDict['FAMILY_MATRIX'] = activitySource
            # ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   
            # ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---   
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # loadLocationSlct : define what kind a location user is locking for ( not used in the projectors )
    #
    # Param             : geoSrc        : pointer to the geo-cache (needed for the LocDefiner-instance)
    #                     idOfLocSlct   : string with the ID of the select-control that will be loaded
    # returns           :  none
    #
    # 15.11.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def loadLocationSlct( self, mongoMgr, idOfLocSlct = 'sel_country' ):
        try:
            lcDfnr = LocDefiner( self.Page )

            # fill the country-select with the available countries
            cntrySelct = self.getCtrl( idOfLocSlct )
            cntrySelct.Items.Add( System.Web.UI.WebControls.ListItem('alle vorhandenen','*') )
            for itm in lcDfnr.itmsFrCtrySlct():
                cntrySelct.Items.Add( System.Web.UI.WebControls.ListItem(itm[0],itm[1]) )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())




































