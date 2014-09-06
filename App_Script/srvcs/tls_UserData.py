
# ***********************************************************************************************************************************************
# UserData:  basically a hashtable that stores the often used session-informations of an user
#
#  example of user data - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
#  debug
#  requestClassification        [education, homework, personalhygiene, craft]
#  sqlUserId                    sqlserver membership info not available yet
#  lngSttngs                    DE
#  confirmPassword              hanahSchigulaSmellsLikeFish1234?!
#  nickname                     Götz Clarin
#  email                        joba-zwei@t-online.de
#  geo_answer                   [4eae4547c9a3710f1ced26e6, 4eae4547c9a3710f1ced26f0, 4eae4547c9a3710f1ced26ed, 4eae4547c9a3710f1ced26e7, 4eae4547c9a3710f1ced26e8, 4eae4547c9a3710f1ced2671, 4eae4547c9a3710f1ced26ef, 4eae4547c9a3710f1ced2670, 4eae4547c9a3710f1ced2673, 4eae4547c9a3710f1ced25a4, 4eae4547c9a3710f1ced25a3, 4eae4547c9a3710f1ced2672, 4eae4547c9a3710f1ced25a7, 4eae4547c9a3710f1ced25a5, 4eae4547c9a3710f1ced25a2, 4eae4547c9a3710f1ced25a0]
#  lastname                     Clarin
#  CAPTCHA                      wY4Xdofk
#  ajax_result
#  placeIds
#  passwordQuestion             Nenne bitte Deinen nejoba-Aktivierungscode aus der ersten Email vom System. 
#  streetWithNumber             Gut Dämme Strasse 12
#  _id                          4f1413fac9a3710ea0d0dd3c
#  GUID                         8071a760d95b4968b77352357957f181
#  password                     hanahSchigulaSmellsLikeFish1234?!
#  forename                     Götz
#  postcode                     41836
#  city                         Hückelhoven
#  areaSize                     22
#  end example of user data -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# 02.08.2011  - bervie -     initial realese
# 14.02.2013  - bervie -     added new item to user-cache 
#                            locationname is a string representation of the user-home
#                            for example '[DE] 41836 Hückelhoven' for the main-developer
#
# ***********************************************************************************************************************************************
import System.Threading                     # used to change language settings of the server
from System import DateTime                 # set log-in time
from System.Web.Configuration import *      # web.config will be used
from System import UriPartial               # generate base-url

import clr                                  # external libraries
clr.AddReference('MongoDB.Bson')            # mongo-db
clr.AddReference('MongoDB.Driver')
from MongoDB.Bson import *
from MongoDB.Driver import *

import mongoDbMgr
import traceback                            # for better exception understanding
import copy                                 # make a deep breath

class UserData:
    '''
    class has its living-room inside the session cache. it is used to store the session-informations for the current user
    '''

    # ***********************************************************************************************************************************************
    # constructor 
    # 
    # param  :  Page to access webform
    #
    # important attributes of the class
    #
    #   self.userDict :                             the data of the account stored in the database
    #                                               if userDict =='None' : there is currently no one logged in
    #    
    #   self.sid = pg.Session.SessionID             current session id from IIS
    #   self.ipadr = pg.Request.UserHostAddress     IP adress of the client-PC
    #   self.locale                                 locale (language)-settings    
    #
    # 17.02.2013    berndv  added member-attributes to measure peformance : lastStepMsg and lastStepTime
    #
    # ***********************************************************************************************************************************************
    def __init__( self , pg):
        self.Page = pg                              # store current page in the instance	
        self.userDict = {}                          # a dictionary with data for current session/user
        # we need a currently-location-value-cache also for users that are NOT logged in

        self.log    = self.Page.Application['njb_Log']          # get the applicationwide logging mechanism
        self.sid    = self.Page.Session.SessionID               # current session id
        self.ipadr  = self.Page.Request.UserHostAddress         # IP adress of the user

        self.locale = None                          # will contain the LOCALE-settings of the webbrowser like 'de-DE'

        self.setUserLang()                          # methode stores browser language settings as an attribute in self.locale
        self.SessionLogIn = None                    # when did session start ( will be dattime after succesfully logged in )

        # helper vars to measure performance  17.02.2013
        self.lastStepTime = System.DateTime.UtcNow
        self.lastStepMsg = "user-data-constructor (initial creation in app-cache)" 


        # remark the new session in the log-file
        self.log.w2lgMsg('New UserData instance created with ID = ' + unicode(self.sid) + ' IP: ' + unicode(self.ipadr) + ' Local: ' + unicode(self.locale))

    def __call__(self ):
        self.__init__()


    # ***********************************************************************************************************************************************
    # LoadUserData( self, mail ) : get data of the user from mongo-db by his/her email (dont forget to make an index on the collection user.final)
    #
    # store the local-info in the class as member and changes the culture settings for the current session
    #
    # 02.08.2011  - bervie -     initial realese
    # 14.02.2013  - bervie       added additional entries : locationname
    # 26.10.2013  - bervie       add 2 additional values to user-dict after loaded
    #                            the values are :   CRRNT_LCTN_ID   :   mongo-id of a location
    #                                               CRRNT_LCTNCNTRY :   the CURRENT country-code
    #                                               CRRNT_CITYNAME  :   name of the CURRENT city
    #                                               CRRNT_POSTCODE  :   postcode of the current location
    #                            these CURRENT-values store the last input of the user. so when he jumps throught the application-forms
    #                            there is always his last input pre-inserted. here in the load-function the hometown of the user is copied in 
    #                            the attributes. so a looged-in user can always see his hometown
    # ***********************************************************************************************************************************************
    def LoadUserData( self, mail ):
        '''
        load the data of an user by given email. 
        '''
        try:
            # try to read a document #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  
            connection = WebConfigurationManager.AppSettings["mongoConn"];
            dbname = WebConfigurationManager.AppSettings["dbName"];

            server = MongoServer.Create(connection);
            db = server.GetDatabase(dbname);
            collection = db.GetCollection("user.final");
            query = Builders.Query.EQ("email", mail);
            doc = collection.FindOne(query);

            data = {}
            for elem in doc :                                           # copy all found elements into an dictionary
                data.update({elem.Name:elem.Value})

            # 14.02.2013 create user-location from existing data
            userLocation = self.createUserLocationString(doc)
            data['locationname'] = userLocation
            self.userDict = copy.deepcopy(data)

            self.SessionLogIn = DateTime.UtcNow                             # self.SessionLogIn IS VERY important. it is used as flag to indicate if user is already logged-in or not : store log-in time of the user.
            self.Page.Session['LOGGEDIN_EMAIL'] = self.userDict['email']    # used in the master-pge to check if the user is logged-in

            # 26.10.2013 bervie : addeded new values for the currently choosen location.
            #                     on startup we copy the defualt-stuff 
            self.userDict['CRRNT_LCTN_ID']      = data['cities'][0].ToString()              # mongo-id of hometown
            self.userDict['CRRNT_LCTNCNTRY']    = data['countrycode'].ToString()            # ISO-code of the country ('DE')
            self.userDict['CRRNT_CITYNAME']     = System.String.Empty                       # 
            self.userDict['CRRNT_POSTCODE']     = data['postcode'].ToString()               # postcode like '41836'

            self.log.w2lgDvlp('user-data read from mongo and copied into the user-dict !!')
            for itm in self.userDict.items():
                self.log.w2lgDvlp('KEY : ' + unicode(itm[0]) + '\t  VALUE : ' + unicode(itm[1]) + '\t')

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # function setUserLang(self, page)(self, Page)
    #
    # store the local-info in the class as member and changes the culture settings for the current session
    #
    # 22.08.2013  added default "de-DE" if None comes from browser.
    # 
    # ***********************************************************************************************************************************************
    def setUserLang(self):
        '''store the browser-language settings for the user in the attribute self.locale and change the server-local setting for this session
        ["locale"] = "de-DE"
        '''
        try:
            if self.Page.Request.UserLanguages is None:
                loc = 'de-DE'
            else:
                loc = self.Page.Request.UserLanguages[0]             # get user-broser setting 
                if len(loc) < 3: loc = loc + '-' + loc.upper()

            self.locale = loc    # store the local-info as an attribute
            # server can take care of users languagae settings
            System.Threading.Thread.CurrentThread.CurrentCulture = System.Globalization.CultureInfo(self.locale)  
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # function createUserLocationString(self, doc)
    #
    # generate a string to show where user comes from by loading first item in location-info and  creating a string from it
    # ***********************************************************************************************************************************************
    def createUserLocationString( self, doc ):
        try:
            # get the id of first town user comes from
            homeCity =  doc.GetElement('cities').Value[0].ToString()
            self.log.w2lgDvlp('userData.createUserLocationString found for user-home-town : ' +  homeCity )

            # ....and load the data of his home-town
            connection = WebConfigurationManager.AppSettings["mongoConn"];
            dbname = WebConfigurationManager.AppSettings["dbName"];

            server = MongoServer.Create(connection);
            db = server.GetDatabase(dbname);
            collection = db.GetCollection("geo.cities");
            query = Builders.Query.EQ("_id", ObjectId(homeCity) );
            homeData = collection.FindOne(query);

            userLocation = '[' + homeData['countryCode'].ToString() + '] '
            userLocation += homeData['postalCode'].ToString() + ' ' + homeData['placeName'].ToString()

            self.log.w2lgDvlp('userData.createUserLocationString found for user-home-town    : ' + userLocation )

            return userLocation
                
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # function addNewItem(self, key, value)
    #
    # adds a new key/value pair to the internal dictionary
    # 06.06.2013  bervie changed to [] instead of update
    # ***********************************************************************************************************************************************
    def addNewItem(self, key, value):
        #self.userDict.update({key:value})
        self.userDict[key] = value


    # ***********************************************************************************************************************************************
    # function getItem(self, key)
    #
    # return an object from the user-data bag
    # ***********************************************************************************************************************************************
    def getItem(self, key):
        item = self.userDict[key].ToString()
        return item


    # ***********************************************************************************************************************************************
    # function isLoggedIn(self )
    #
    # return true if a user is logged in and flase if no one gave us login informations
    # ***********************************************************************************************************************************************
    def isLoggedIn(self):
        if self.SessionLogIn == None: return False
        else: return True


    # ***********************************************************************************************************************************************
    # function LoggOut(self )
    #
    # end the user-session by deleting the user-data in session
    # ***********************************************************************************************************************************************
    def LoggOut(self):
        try:
            self.SessionLogIn = None
            self.userDict = {}
            self.Page.Session["LOGGEDIN_EMAIL"] = None

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # checkUserRigths : function is called to check if user has the needed rigths to visit the webform.
    #                   the parameter role-name is verified in the user-array account-roles. if string is in the array user can visit the website
    #                   
    #                   the function makes an redirect to another webform 
    #                   if user is not logged-in the session will be redirected to the log-in webform
    #                   if user has no rigths to visit the webform session will be redirected to an error-page
    #
    # param:            page : the reference to the page 
    #                   roleName : the "role" that must be in the users role-array 
    #
    #
    # 03.10.2012   bervie  initial realease
    # ***********************************************************************************************************************************************
    def checkUserRigths( self, pge, roleName ):
        try:
            self.measurePeformance('Userdata.checkUserRigths - begin ')

            urlNext = None

            if self.isLoggedIn():
                # empty role-name means webform is for any logged.in user
                if roleName == System.String.Empty: return
                bsonRole = BsonString( roleName )                       # for check we need a BSONString
                rolesOfUser = self.userDict['account_roles']            # get the roles of the user ( Array of BSON Strings !!)
               
                if  bsonRole not in rolesOfUser: urlNext = pge.ResolveUrl( WebConfigurationManager.AppSettings['ForbiddenWebForm'] )    # user is not allowed to use webform
                    
            else:
                # redirect to login page
                urlCurrent = pge.Request.Url.AbsoluteUri
                pge.Session['REDIRECT_AFTER_LOGIN'] = urlCurrent
                urlNext = pge.ResolveUrl(WebConfigurationManager.AppSettings['LogIn'])
                
            self.measurePeformance('Userdata.checkUserRigths - end-of-try ')

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())

        if urlNext != None:
            #self.log.w2lgDbg( "checkUserRigths will send  url_for_redirect " + unicode(urlNext) )
            # self.Page.Response.Redirect(urlNext)
            self.measurePeformance('Userdata.checkUserRigths - before redirect ')
            pge.Response.Redirect(urlNext)





    # ***********************************************************************************************************************************************
    # checkPremiumTimeDiff : function is called to check if user has the needed rigths to visit the data.
    #                        only payed premium-accounts can see the details of a announce directly after creation
    #
    # param:                 page : ref to webform
    #                        creationTime : The timestamp the item was created. 
    #
    # 03.10.2012   bervie  initial realease
    # ***********************************************************************************************************************************************
    def checkPremiumTimeDiff( self, page, creationTime ):
        try:
            redrct = None
            return

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())

        if redrct != None:
            rdrctUrl += redrct;
            page.Response.Redirect( page.ResolveUrl( rdrctUrl ) )


    # ***********************************************************************************************************************************************
    # measurePeformance :   time-stop-watch for performance messurement
    #
    # param:                 remark : text to log
    #
    # 03.10.2012   bervie  initial realease
    # ***********************************************************************************************************************************************
    def measurePeformance( self, remark):
        try:
            now = System.DateTime.UtcNow
            difference = now - self.lastStepTime 
            self.lastStepTime = now

            self.log.w2lgDvlp('measurePeformance                      -> ' )
            self.log.w2lgDvlp('measurePeformance    last message was  -> ' + str(self.lastStepMsg) )
            self.log.w2lgDvlp('measurePeformance    new meaasage is   -> ' + str(remark)  )
            self.log.w2lgDvlp('measurePeformance - - - - - - - - - - --> ' + str(difference.Milliseconds))

            self.lastStepMsg = remark

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # storeLocCurrentlyChoosen : this function stores the location a user has choosen during runtime.
    #
    # param:                 
    #                        loctnCountry
    #                        locCityName
    #                        locPostCode
    #
    # 03.10.2012   bervie  initial realease
    # ***********************************************************************************************************************************************
    def storeLocCurrentlyChoosen( self, loctnCountry='', locCityName='', locPostCode='' ):
        try:
            self.userDict['CRRNT_LCTNCNTRY']    = loctnCountry
            self.userDict['CRRNT_CITYNAME']     = locCityName
            self.userDict['CRRNT_POSTCODE']     = locPostCode

            geoSrc = self.Page.Application['njbGeoSrc']       # the functions for the geo-calculation is in the geo_source

            mongoId = False
            if locPostCode != System.String.Empty:
                mongoId = geoSrc.findIdByPostCode(loctnCountry, locPostCode )
            else:
                mongoId = geoSrc.findIdByName(loctnCountry, locCityName )

            # if mongo-id still is false here there was nothing found for thwe given input
            if mongoId == False:
                self.userDict['CRRNT_LCTN_ID']      = System.String.Empty
                self.userDict['CRRNT_LCTNCNTRY']    = System.String.Empty
                self.userDict['CRRNT_CITYNAME']     = System.String.Empty
                self.userDict['CRRNT_POSTCODE']     = System.String.Empty
                self.log.w2lgError('UserData.storeLocCurrentlyChoosen : ERROR there was nothing in the geoCache for ' + loctnId + ' ' + loctnCountry + ' ' + locCityName + ' ' + locPostCode )
            else:
                self.userDict['CRRNT_LCTN_ID'] = mongoId

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())
