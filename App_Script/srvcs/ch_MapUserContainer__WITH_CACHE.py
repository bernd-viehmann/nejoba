# ***********************************************************************************************************************************************
# ch_MapUserContainer.py :   class holds an array with user-data shown in the map 
#
#                            
#   data in the container to work with
#                            
#            website
#            languagecode
#            creation_time
#            nickname
#            adress_add
#            google_plus
#            long
#            cities
#            CAPTCHA
#            phone
#            account_roles
#            emailconfirm
#            item_type
#            _id
#            facebook
#            forename
#            postcode
#            city
#            street
#            countrycode
#            picturl
#            familyname
#            email
#            mobile
#            info
#            areasize
#            twitter
#            skype
#            lat
#            housenumber
#            password
#            GUID
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
import System.Guid
import System
import traceback
import re
import codecs
import tls_LogCache
import ch_geoCache
import ch_AppCache


# ***********************************************************************************************************************************************
# string is the HTML-TEMPLATE for creating the popup of an item in the map
#
# 22.05.2013    berndv  initial realese
# ***********************************************************************************************************************************************
popUpHtmlTmplt ='<table class="table table-bordered" style="vertical-align: middle"><tbody><tr><td><img src="#@#picturl#@#" class="img-polaroid" height="96" width="96" align="middle"></td><td><a href="mailto:#@#email#@#?Subject=AktiMap-Message">Email senden an:<br />#@#email#@#</a><br /><a href="#@#website#@#" target="_blank"><h6>Website:<br />#@#website#@#</h6></a></td></tr><tr><td colspan="2"><a href="http://www.nejoba.net/njb_02/wbf_topic/parameter_result_list.aspx?loc=#@#forumlocation#@#" target="_blank"><h6>zum nejoba Forum</h6></a><p><small>Das Forum ist eine öffentliche<br /> Diskussions- und Informationsstelle</small></p></td></tr><tr><td colspan="2"><h6>Mitteilung:</h6><p>#@#info#@#</p></td></tr><!--#@#additional_contact_info#@#--></tbody></table>'

# ***********************************************************************************************************************************************
# stuff for creating the HTML-table with the contact-info
#
# 22.05.2013    berndv  initial realese
# ***********************************************************************************************************************************************
# the keys in the user-data-dict
keyDict =   { 'facebook' : 'facebook-Profil',
              'google_plus' : 'google+ Profil',
              'twitter' : 'twitter-Konto',
              'skype' : 'Skype-Konto',
              'mobile' : 'Mobiltelefon',
              'phone' : 'Telefon',
              'forename' : 'Vorname',
              'familyname' : 'Nachname',
              'street' : 'Straße',
              'housenumber' : 'Hausnummer',
              'city' : 'Stadt',
              'adress_add' : 'Zusatz' }

rplcAdditionalInfo = '<!--#@#additional_contact_info#@#-->'                                     # this string must be replaced to add some rows to the table
tblRowTmplt = '<tr><td><strong>#@#dict_key#@#</strong></td><td>#@#dict_val#@#</td></tr>'        # the tmplate-string to create a single row in the container





class MapUserContainer():
    '''
    MapUserContainer Class: the class for storing in the application-cache

    the class read the data into an array and provides fast access to it when needed




    '''

    # ***********************************************************************************************************************************************
    # constructor of MapUserContainer : the class that manages the UserList for the map
    #
    # parameter : pg : Page-Instance to get access to the Application- and Session-Cache
    #
    # 22.05.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def __call__( self ):
        self.__init__()

    def __init__( self, pg ):
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

            self.UserText   = System.Text.StringBuilder( self.createHeader() )      # string for OSM-vector-map with user-data needed to construct. 
            self.actionText = System.Text.StringBuilder( self.createHeader() )      # list with action-data items ( in german it is called Initiativen )

            self.userData = self.Page.Session['njbUsrDt']                           # store the user-session-data
            self.loadFromMongo()                                                    # load data of users from mongo. they will be cached in the StringBuilders 

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # ***********************************************************************************************************************************************
    # createHeader : called in constructor to add header to the tsv-output string
    #
    # 24.05.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def createHeader( self ):
        try:
            header  = ''
            header += 'point' + '\t'
            header += 'title' + '\t'
            header += 'description' + '\t'
            header += 'icon' + '\t'
            header += 'iconSize' + '\t'
            header += 'iconOffset' + '\n'

            return header

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # ***********************************************************************************************************************************************
    # loadUsersFromMongo : when class is created this function  loads the data into the container
    #
    # 22.05.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def loadFromMongo( self ):
        try:
            mngConnStrng = WebConfigurationManager.AppSettings['mongoConn']     # connection 2 database
            dbName = WebConfigurationManager.AppSettings['dbName']              # get name of db from conf
            server = MongoServer.Create(str( mngConnStrng ) )
            njbDb = server.GetDatabase(dbName)
            collection = njbDb.GetCollection("user.final")

            self.log.w2lgDvlp( 'MapUserContainer->loadFromMongo started with reading all data ' )
            for item in collection.FindAll():
                self.log.w2lgDvlp( 'loadFromMongo ' + item['_id'].ToString() )
                self.addUserFromMongo(item)

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # ***********************************************************************************************************************************************
    # addUserFromSession : writes the data of a new created user into this cache. this is done during user-account is confirmed 
    #
    # parameter:     : dataItem
    #                  if dataItem is None take the data from the user-dict in session-cache
    #                  if dataitem has a value it is an array coming from the mongo-DB
    #
    #
    # 22.05.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def addUserFromSession( self, dataItem ):
        try:
            self.log.w2lgDvlp( 'MapUserContainer->addUserFromSession was called to add from userdict into the map-user-cache' )
            html = self.extendOsmLayerText( dataItem )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # addUserFromSession : writes the data of a new created user into this cache. this is done during system-initialization
    #                  function converts from BsonDocument to py-dict
    #
    # parameter:     : dataItem   python-dict with dataof the user
    #
    #
    # 22.05.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def addUserFromMongo( self, dataItem ):
        try:
            self.log.w2lgDvlp( 'MapUserContainer->addUserFromMongo was called to add from mongoDB into the map-user-cache' )
            if dataItem is None:    item = self.userData.userDict           # use session-data 
            item = {}
            for elem in dataItem.Elements:
                key = elem.Name
                val = elem.Value.ToString()
                item[key] = val

            html = self.extendOsmLayerText( item )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # ***********************************************************************************************************************************************
    # extendOsmLayerText : function extends the given string with vector-layer data by the incoming value
    #
    # 22.05.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def extendOsmLayerText( self, dataItem ):
        try:
            self.log.w2lgDvlp( 'MapUserContainer->extendOsmLayerText was called to add from userdict into the map-user-cache' )
            #for key in dataItem.keys():
            #    self.log.w2lgDvlp( 'key :  ' + key + ' ; value : ' + dataItem[key].ToString() )

            htmlPart = self.createMarkerPopUp(dataItem)

            # create a new Line
            nwLine = System.Text.StringBuilder()
            nwLine.Append( dataItem['lat'] )
            nwLine.Append( ',' )
            nwLine.Append( dataItem['lon'] )
            nwLine.Append( '\t' )
            nwLine.Append( '<h4>' + dataItem['nickname'] + '</h4>' )
            nwLine.Append( '\t' )
            nwLine.Append( htmlPart )
            nwLine.Append( '\t' )
            nwLine.Append( 'http://maps.google.com/intl/en_us/mapfiles/ms/micons/orange-dot.png' )
            nwLine.Append( '\t' )
            nwLine.Append( '32, 32' )
            nwLine.Append( '\t' )
            nwLine.Append( '-15,-30' )
            nwLine.Append( '\n' )

            # add the new data to the StringBuilder it belons to 
            self.UserText.Append(nwLine)


        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # ***********************************************************************************************************************************************
    # createMarkerPopUp : function creates the body of an marker-pop-up
    #
    # param    : the line of data
    # returns  : string with the nice marker-popup
    #
    # 22.05.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def createMarkerPopUp( self, dataItem ):
        try:
            self.log.w2lgDvlp( 'MapUserContainer->createMarkerPopUp will return a nice popup-marker')
            #for key in dataItem.keys():
            #    self.log.w2lgDvlp( 'key :  ' + key + ' ; value : ' + dataItem[key].ToString() )

            dynAddedInfoKeys = ['facebook', 'google_plus', 'twitter', 'skype', 'mobile', 'phone', 'forename', 'familyname', 'street', 'housenumber', 'city', 'adress_add' ]
            cntctTable = System.Text.StringBuilder()

            for itm in dynAddedInfoKeys:
                if itm in dataItem:
                    if len(dataItem[itm]) > 0:
                        rowCreator = tblRowTmplt
                        rowCreator = rowCreator.replace( '#@#dict_key#@#',  keyDict[itm].ToString() )
                        rowCreator = rowCreator.replace( '#@#dict_val#@#', dataItem[itm].ToString() )
                        cntctTable.Append( rowCreator )

            forumLocation = dataItem['countrycode'] + '|' + dataItem['postcode']
            info = dataItem['info'][:200]

            htmlPart = popUpHtmlTmplt
            htmlPart = htmlPart.replace( '#@#picturl#@#'                        , dataItem['picturl'] )
            htmlPart = htmlPart.replace( '#@#website#@#'                        , dataItem['website'] )
            htmlPart = htmlPart.replace( '#@#email#@#'                          , dataItem['email'] )
            htmlPart = htmlPart.replace( '#@#forumlocation#@#'                  , forumLocation       )
            htmlPart = htmlPart.replace( '#@#info#@#'                           , info )
            htmlPart = htmlPart.replace( '<!--#@#additional_contact_info#@#-->' , cntctTable.ToString() )

            self.log.w2lgDvlp( 'MapUserContainer->createMarkerPopUp additional contact info : ' + cntctTable.ToString() )
            self.log.w2lgDvlp( 'MapUserContainer->createMarkerPopUp main-table              : ' + htmlPart.ToString()   )

            return htmlPart

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())









