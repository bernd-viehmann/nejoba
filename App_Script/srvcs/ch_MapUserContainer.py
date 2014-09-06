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

            self.userData = self.Page.Session['njbUsrDt']                           # reference to the user-session-data

            # create database-connection
            self.mngConnStrng   = WebConfigurationManager.AppSettings['mongoConn']              # connection 2 database
            self.dbName         = WebConfigurationManager.AppSettings['dbName']                 # get name of db from conf
            self.server         = MongoServer.Create(str( self.mngConnStrng ) )
            self.njbDb          = self.server.GetDatabase( self.dbName )

            # define the types of initiatives that are possible
            self.markerTypes = ['communities','politics','monetary','giveandswap','sustainable_business','agriculture','environmental','initiatives','charities','associations']

            # string is the HTML-TEMPLATE for creating the popup of an item in the map
            self.popUpHtmlTmplt ='<table class="table table-bordered" style="vertical-align: middle"><tbody><tr><td><img src="#@#picturl#@#" class="img-polaroid" height="96" width="96" align="middle"></td><td><a href="mailto:#@#email#@#?Subject=AktiMap-Message">Email senden an:<br />#@#email#@#</a><br /><a href="#@#website#@#" target="_blank"><h6>Website:<br />#@#website#@#</h6></a></td></tr><tr><td colspan="2"><a href="http://www.nejoba.net/njb_02/wbf_topic/parameter_result_list.aspx?loc=#@#forumlocation#@#" target="_blank"><h6>zum nejoba Forum</h6></a><p><small>Das Forum ist eine öffentliche<br /> Diskussions- und Informationsstelle</small></p></td></tr><tr><td colspan="2"><h6>Mitteilung:</h6><p>#@#info#@#</p></td></tr><!--#@#additional_contact_info#@#--></tbody></table>'

            # stuff for creating the HTML-table with the contact-info
            self.keyDict =   { 'facebook' : 'facebook-Profil',
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

            self.rplcAdditionalInfo = '<!--#@#additional_contact_info#@#-->'                                     # this string must be replaced to add some rows to the table
            self.tblRowTmplt = '<tr><td><strong>#@#dict_key#@#</strong></td><td>#@#dict_val#@#</td></tr>'        # the tmplate-string to create a single row in the container


        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # ***********************************************************************************************************************************************
    # createHeader : function creates the header needed for the ascii-output. 
    #                the header defines what kind of data we have in the corresponding columnn
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
    # load  : function is called by the map-marker-data-source-web-form
    #
    # param : 
    #                 amount: number of records taht will be returned
    #
    #                 types : csv-string which defines what type of data will be returned. 
    #                         if None all data will be returned 
    #
    # 01.06.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def load( self, postcode=None, amount=2000, types='*' ):
        try:
            # set the types that will b e loaded
            self.typesToLoad = types.strip().split(',')

            return self.readDataIntoDict( postcode, amount )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())





    # ***********************************************************************************************************************************************
    # loadUsersFromMongo : when class is created this function  loads the data into the container
    #
    # parameter : 
    #             postcode : like DE|41836 for germany->hueckelhoven by postcode
    #             amount   : the number of items that should be read
    #
    # returns   : list of lists with the needed data for creating the output
    #
    # 22.05.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def readDataIntoDict( self, postcode, amount ):
        try:
            self.points = {}                                        # dict with the stuff from the database ordered used by the loader-functions as data-container
                                                                    # by the type ('human','communities','politics' and so on.....)
    
            # load the users who want to be connected
            if 'human' in self.typesToLoad or '*' in self.typesToLoad:
                self.loadUsers( postcode )                          # load the users stored in user.final-collection

            # the initiatives are loaded in this function
            self.loadInititaives( postcode )            # load the inititives stored in map.initiatives-collection

            # create a resulting string with all loaded data in it
            rslt = []
            for lst in self.points.values():
                rslt.extend(lst)


            # build the result-string
            rsltTxt = System.Text.StringBuilder()
            rsltTxt.Append( self.createHeader() )

            for itm in rslt:
                rsltTxt.Append( itm )

            return rsltTxt.ToString()

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())





    # ***********************************************************************************************************************************************
    # loadUsersFromMongo : when class is created this function  loads the data into the container
    #
    # parameter : postcode like DE|41836 for germany->hueckelhoven by postcode
    # returns   : none
    #             the received data is stored in an class-attribute self.points = {}
    #
    # 22.05.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def loadUsers( self, postcode ):
        try:
            self.log.w2lgDvlp( 'MapUserContainer->loadUsers started  ' )
            collection      = self.njbDb.GetCollection('user.final')            #get the collection with final user data

            data = []
            if postcode is None:
                # get all items
                for item in collection.FindAll():
                    self.log.w2lgDvlp( 'loadFromMongo ' + item['_id'].ToString() )
                    data.Add( item['marker_line'].ToString() )
                    
            # get the items for a given postcode
            else:
                qry  = QueryDocument( 'post_code_key',postcode)
                for itm in collection.Find(qry) :                              # get the docs found for query
                    data.Add( item['marker_line'].ToString() )

            self.points['human'] = data

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())




    # ***********************************************************************************************************************************************
    # loadInititaives : function loads all initiatives from the collection 
    #
    # parameter : postcode like DE|41836 for germany->hueckelhoven by postcode
    # returns   : none
    #             the received data is stored in an class-attribute self.points = {}
    #
    # 22.05.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def loadInititaives( self, postcode=None ):
        try:
            self.log.w2lgDvlp( 'MapUserContainer->loadInititaives started  ' )
            collection      = self.njbDb.GetCollection('initiatives.final')            #get the collection with final user data

            data = []
            if postcode is None:
                # get all items
                for item in collection.FindAll():
                    self.log.w2lgDvlp( 'MapUserContainer : loadInititaives ' + item['_id'].ToString() )
                    data.Add( item['marker_line'].ToString() )
                    
                # get the items for a given postcode
            else:
                qry  = QueryDocument( 'post_code_key',postcode)
                for itm in collection.Find(qry) :                              # get the docs found for query
                    data.Add( item['marker_line'].ToString() )

            self.points['human'] = self.points['human'] + data

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())














    # ***********************************************************************************************************************************************
    # createMarkerLine : function extends the given string with vector-layer data by the incoming value
    #
    # 22.05.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def createMarkerLine( self, dctWthUsrData ):
        try:
            self.log.w2lgDvlp( 'MapUserContainer->createMarkerLine was called to add from userdict into the map-user-cache' )

            #for key in dctWthUsrData.keys():
            #    self.log.w2lgDvlp( 'key :  ' + key + ' ; value : ' + dctWthUsrData[key].ToString() )

            nwLine = System.Text.StringBuilder()                # create a new Line
            htmlPart = self.createMarkerPopUp(dctWthUsrData)    # get the formated HTML-part for pop-up

            nwLine.Append( dctWthUsrData['lat'] )
            nwLine.Append( ',' )
            nwLine.Append( dctWthUsrData['lon'] )
            nwLine.Append( '\t' )
            nwLine.Append( '<h4>' + dctWthUsrData['nickname'] + '</h4>' )
            nwLine.Append( '\t' )
            nwLine.Append( htmlPart )
            nwLine.Append( '\t' )
            nwLine.Append( 'http://maps.google.com/intl/en_us/mapfiles/ms/micons/orange-dot.png' )
            nwLine.Append( '\t' )
            nwLine.Append( '32, 32' )
            nwLine.Append( '\t' )
            nwLine.Append( '-15,-30' )
            nwLine.Append( '\n' )

            # return the new line which defines the setting of a marker
            return nwLine.ToString()

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # ***********************************************************************************************************************************************
    # createMarkerPopUp : function creates the body of an marker-pop-up
    #
    # inputContainer  : the data typed in by the user as dictionary
    # returns         : string with the nice marker-popup
    #
    # 22.05.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def createMarkerPopUp( self, inputContainer ):
        try:
            self.log.w2lgDvlp( 'MapUserContainer->createMarkerPopUp will return a nice popup-marker')
            for key in inputContainer.keys():
                self.log.w2lgDvlp( 'key :  ' + key + ' ; value : ' + inputContainer[key].ToString() )

            dynAddedInfoKeys = ['facebook', 'google_plus', 'twitter', 'skype', 'mobile', 'phone', 'forename', 'familyname', 'street', 'housenumber', 'city', 'adress_add' ]
            cntctTable = System.Text.StringBuilder()

            for keySelctd in dynAddedInfoKeys:
                self.log.w2lgDvlp( 'MapUserContainer->createMarkerPopUp will add an item for  :' + unicode(keySelctd) )
                if keySelctd in inputContainer.keys():
                    if inputContainer[keySelctd] is None : break    # ignor Nonesense. No idea where they came from

                    if len( inputContainer[keySelctd].ToString().strip() ) > 0:
                        rowCreator = self.tblRowTmplt
                        rowCreator = rowCreator.replace( '#@#dict_key#@#',    self.keyDict[keySelctd].ToString() )
                        rowCreator = rowCreator.replace( '#@#dict_val#@#',  inputContainer[keySelctd].ToString() )
                        cntctTable.Append( rowCreator )

            forumLocation = inputContainer['countrycode'] + '|' + inputContainer['postcode']
            info = inputContainer['info'][:500]

            htmlPart = self.popUpHtmlTmplt
            htmlPart = htmlPart.replace( '#@#picturl#@#'                        , inputContainer[ 'picturl' ] )
            htmlPart = htmlPart.replace( '#@#website#@#'                        , inputContainer[ 'website' ] )
            htmlPart = htmlPart.replace( '#@#email#@#'                          , inputContainer[ 'email'   ] )
            htmlPart = htmlPart.replace( '#@#forumlocation#@#'                  , forumLocation       )
            htmlPart = htmlPart.replace( '#@#info#@#'                           , info )
            htmlPart = htmlPart.replace( '<!--#@#additional_contact_info#@#-->' , cntctTable.ToString() )

            self.log.w2lgDvlp( 'MapUserContainer->createMarkerPopUp additional contact info : ' + cntctTable.ToString() )
            self.log.w2lgDvlp( 'MapUserContainer->createMarkerPopUp main-table              : ' + htmlPart.ToString()   )

            return htmlPart

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())






