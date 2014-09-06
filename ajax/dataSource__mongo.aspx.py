#  
#
#  
#  
#  
#  
#  
#
#  
from System.Web.Configuration import *
from System import UriPartial
import System.Data
import System.Web
import System.Collections
import System.Text

import clr
import traceback                    # for better exception understanding
import mongoDbMgr                   # father : the acces to the database

tool = mongoDbMgr.mongoMgr(Page)


class mapTwoSource( mongoDbMgr.mongoMgr ):
    '''
    mapTwoSource loads all items from the app-cache and creates JSON from it. It is a special-text-returning webform (ironpython is not capable to use webservices !
    the results depends on URL-parameter:


 #   description of the URL-PARAMETER for loading webform behind DataURL
 #
 #  'http://localhost:7258/njb_2/wbf_topic/mapTwo_dataSource.aspx?loc=DE%7C41836&tags=world&srchMd=OR'
 #
 #   amount      : the number of items that should be send by the datasource
 #   lastdbid    : the last database-id that was received by the client. data-source webform 
 #                 should start here.
 #   loc         : the geo-location as sting like "de|41836". if only "de|" is given all german 
 #                 results are send to the client from data-source
 #   tags        : the tags we are locking for. list is comma-seperated
 #   srchMd      : OR means display all items with any tag; AND menas display only tags 
 #                 that are labeled with all keywords
 #   startdate   : a string-coded date-object to define when the event starts
 #   enddate     : a string-representation of the end of the event



    '''

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # constructor. 
    #
    # 27.06.2013   - bervie-      initial realese
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def __init__(self, page ):
        try:
            mongoDbMgr.mongoMgr.__init__(self, page )                       # wake up papa ; mother njbTools is included by inheritance!

            self.workbench      = System.Text.StringBuilder()               # string-builder for generating the return-output
            self.locationList   = []                                        # string with the locations-detail-data in the neighboerhood

            # testfunction ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  
            for a in (0,1,2,3,4,5,6,7,8,9) :
                tool.appCch.getSliceBounce( a )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # pgLoad is called from PageLoad to create the data-collection
    #
    # 27.06.2013   - bervie-      initial realese
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def pgLoad( self ):
        try:
            # prepare UTF-8 output
            context = System.Web.HttpContext.Current

            context.Response.ContentType = "text/plain; charset=utf-8"
            context.Response.Charset = "utf-8"
            context.Response.Clear()
            context.Response.HeaderEncoding = System.Text.UTF8Encoding(False)
            context.Response.ContentEncoding = System.Text.UTF8Encoding(False)

            # get the data from the app-cache table (all there is in the first step)
            text = self.loadFromCache()

            out = System.Text.Encoding.UTF8.GetBytes(text)
            context.Response.OutputStream.Write(out, 0, out.Length)
            context.Response.Flush()
            context.Response.End()


        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # loadFromCache load all data from the cache in reverse order and creat a json object from it
    #
    # param           : 
    # returns  string : the json-code that will be send back to caller
    #
    # 27.06.2013   - bervie-      initial realese
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def loadFromCache( self ):
        try:

            # write the items from the query-string
            urlParam = {}
            for key in self.Page.Request.QueryString:
                urlParam.Add( key , self.Page.Request.QueryString[key] )
                self.log.w2lgDvlp('key in param-list      : ' + unicode( key ) + ' - ' + unicode( self.Page.Request.QueryString[key] ))

            # when the webform was called without parameters then we have to display all items in the datatable from bottom to top
            if self.Page.Request.QueryString.Keys.Count == 0:
                self.loadAllInitial()
            # load the data corresponding to the query-params
            else:
                self.loadFiltered()

            return '{' + self.workbench.ToString() + '}'

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # loadAllInitial loads the items with geo-coords from end to top for initial map-display. all countries in the DataTable will be visible
    #
    # 27.06.2013   - bervie-      initial realese
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def loadAllInitial( self ):
        try:
            self.log.w2lgDvlp('loadAllInitial called')
            itmTable = tool.appCch.dtSt.Tables['items']
            self.workbench.Append('"items": [')

            rowIdx = itmTable.Rows.Count-1

            while (rowIdx >= 0):
                row = itmTable.Rows[rowIdx]
                if len(row['lat'].ToString()) > 0:
                    self.workbench.Append( '{' )
                    self.workbench.Append( '"_ID":"' + row['_ID'].ToString() + '",' )
                    self.workbench.Append( '"objectType":"' + row['objectType'].ToString() + '",' )
                    self.workbench.Append( '"_objectDetailID":"' + row['_objectDetailID'].ToString() + '",' )
                    self.workbench.Append( '"_hostGUID":"' + row['_hostGUID'].ToString() + '",' )
                    self.workbench.Append( '"_rootElemGUID":"' + row['_rootElemGUID'].ToString() + '",' )
                    self.workbench.Append( '"_parentID":"' + row['_parentID'].ToString() + '",' )
                    self.workbench.Append( '"_followerID":"' + row['_followerID'].ToString() + '",' )
                    self.workbench.Append( '"_creatorGUID":"' + row['_creatorGUID'].ToString() + '",' )
                    self.workbench.Append( '"creationTime":"' + row['creationTime'].ToString() + '",' )
                    self.workbench.Append( '"_locationID":"' + row['_locationID'].ToString() + '",' )
                    self.workbench.Append( '"from":"' + row['from'].ToString() + '",' )
                    self.workbench.Append( '"till":"' + row['till'].ToString() + '",' )
                    self.workbench.Append( '"subject":"' + row['subject'].ToString() + '",' )
                    #self.workbench.Append( '"body":"' + row['body'].ToString() + '",' )
                    self.workbench.Append( '"nickname":"' + row['nickname'].ToString() + '",' )
                    self.workbench.Append( '"locationname":"' + row['locationname'].ToString() + '",' )
                    self.workbench.Append( '"tagZero":"' + row['tagZero'].ToString() + '",' )
                    self.workbench.Append( '"lat":"' + row['lat'].ToString() + '",' )
                    self.workbench.Append( '"lon":"' + row['lon'].ToString() + '"},\n')
                    tool.log.w2lgDvlp("found with geocoords :" + str(rowIdx)) 
                rowIdx -= 1

            self.workbench.Length = self.workbench.Length - 2
            self.workbench.Append(']')

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # loadFiltered : the functions returns the items from the cached table that match the selection-criterias
    #
    #   amount      : the number of items that should be send by the datasource
    #   lastdbid    : the last database-id that was received by the client. data-source webform 
    #                 should start here.
    #   loc         : the geo-location as sting like "de|41836". if only "de|" is given all german 
    #                 results are send to the client from data-source
    #   tags        : the tags we are locking for. list is comma-seperated
    #   srchMd      : OR means display all items with any tag; AND menas display only tags 
    #                 that are labeled with all keywords
    #   startdate   : a string-coded date-object to define when the event starts
    #   enddate     : a string-representation of the end of the event
    #
    # 04.07.2013   - bervie-      initial realese
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def loadFiltered( self ):
        try:
            self.log.w2lgDvlp('loadFiltered called')

            #check if needed params were given
            if ('amount' not in self.Page.Request.QueryString.Keys):
                self.log.w2lgError('error! loadFiltered amount')
                return 'error! loadFiltered amount'

            if ('loc' not in self.Page.Request.QueryString.Keys):
                self.log.w2lgError('error! loadFiltered loc')
                return 'error! loadFiltered loc'

            else:
                self.defineLocation( self.Page.Request.QueryString['loc'].ToString() )      # add data cities in the neighjbourhood 
                self.getItemsByLocation()                                                   # load the items for a given location


        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # ***********************************************************************************************************************************************
    # defineLocation   : define a list of places near the startpoint ordered by distance and add the list to the dropdown
    #
    # 10.03.2013  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def defineLocation( self, urlLocParam ):
        try:
            # check for country or city. if only a country is given we load all items 
            # for a given countrycode like 'de|' for germany or 'at|' for austria
            callParam = urlLocParam.split('|')
            self.log.w2lgDvlp( 'defineLocation parameter : ' + callParam[0] + ' - ' + callParam[1] )

            areaSize  = WebConfigurationManager.AppSettings["areaSize"];
            cntry     = callParam[0]
            postcd    = callParam[1]
            self.locationList = self.geoSrc.getPlacesByPostcode( cntry.ToString(), postcd.ToString(), areaSize.ToString() )

            #for loc in locList:
            #    self.log.w2lgDvlp( 'line           : ' + unicode(loc) )
            #    self.log.w2lgDvlp( ' -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --  '  )
            #    self.log.w2lgDvlp( 'loc_selector   : ' + unicode(loc[0]) )        # 'mngId'                  0 
            #    self.log.w2lgDvlp( 'mongo_ID       : ' + unicode(loc[1]) )        # 'keyStrng'               1
            #    self.log.w2lgDvlp( 'country-code   : ' + unicode(loc[2]) )        # 'keyCity'                2
            #    self.log.w2lgDvlp( 'post-code      : ' + unicode(loc[3]) )        # 'countryCode'            3
            #    self.log.w2lgDvlp( 'place-name     : ' + unicode(loc[4]) )        # 'postalCode'             4
            #    self.log.w2lgDvlp( 'latitude       : ' + unicode(loc[5]) )        # 'placeName'              5
            #    self.log.w2lgDvlp( 'longitude      : ' + unicode(loc[6]) )        # 'latitude'               6
            #    self.log.w2lgDvlp( 'COUNTRY|CITY   : ' + unicode(loc[7]) )        # 'longitude'              7
            #    self.log.w2lgDvlp( 'distance       : ' + unicode(loc[8]) )        # calculated distance      8

            # the data of the cities in th neighbourhood are added to the result-string (which is a class-attribute)
            self.workbench.Append('"places": [')
            for loc in self.locationList:
                self.workbench.Append( '{' )
                self.workbench.Append( '"locSelector" : ' + unicode(loc[0]) + '",' )
                self.workbench.Append( '"mongoID": ' + unicode(loc[1]) + '",' )
                self.workbench.Append( '"countryCode" : ' + unicode(loc[2]) + '",' )
                self.workbench.Append( '"postCode" : ' + unicode(loc[3]) + '",' )
                self.workbench.Append( '"placeName" : ' + unicode(loc[4]) + '",' )
                self.workbench.Append( '"latitude" : ' + unicode(loc[5]) + '",' )
                self.workbench.Append( '"longitude" : ' + unicode(loc[6]) + '",' )
                self.workbench.Append( '"COUNTRYandCITY" : ' + unicode(loc[7]) + '",' )
                self.workbench.Append( '"distance" : ' + unicode(loc[8]) + '"},\n')
            self.workbench.Append(']')
            return 

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())




    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # getItemsByLocation : the functions loads all cached items matching given selection-criteria
    #
    #   amount      : the number of items that should be send by the datasource
    #   lastdbid    : the last database-id that was received by the client. data-source webform 
    #                 should start here.
    #   loc         : the geo-location as sting like "de|41836". if only "de|" is given all german 
    #                 results are send to the client from data-source
    #   tags        : the tags we are locking for. list is comma-seperated
    #   srchMd      : OR means display all items with any tag; AND menas display only tags 
    #                 that are labeled with all keywords
    #   startdate   : a string-coded date-object to define when the event starts
    #   enddate     : a string-representation of the end of the event
    #
    # 04.07.2013   - bervie-      initial realese
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def getItemsByLocation( self ):
        try:
            self.log.w2lgDvlp( 'mapTwoSource.getItemsByLocation is been started gewesen ' )

            self.amount      = self.Page.Request.QueryString['amount']
            self.lastdbid    = self.Page.Request.QueryString['lastdbid']
            self.loc         = self.Page.Request.QueryString['loc']
            self.tags        = self.Page.Request.QueryString['tags']
            self.srchMd      = self.Page.Request.QueryString['srchMd']
            self.startdate   = self.Page.Request.QueryString['startdate']
            self.enddate     = self.Page.Request.QueryString['endate']

            self.log.w2lgDvlp( '  amount     : ' + unicode(self.amount    ))
            self.log.w2lgDvlp( '  lastdbid   : ' + unicode(self.lastdbid  ))
            self.log.w2lgDvlp( '  loc        : ' + unicode(self.loc       ))
            self.log.w2lgDvlp( '  tags       : ' + unicode(self.tags      ))
            self.log.w2lgDvlp( '  srchMd     : ' + unicode(self.srchMd    ))
            self.log.w2lgDvlp( '  startdate  : ' + unicode(self.startdate ))
            self.log.w2lgDvlp( '  enddate    : ' + unicode(self.enddate   ))

            return

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


# create a helper to handle this webform  ***********************************************************************************************************************************************
tool = mapTwoSource( Page )
# ***************************************************************************************************************************************************************************************


# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 07.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    try:
        tool.pgLoad()
        return 

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())

    context.Response.End()
