# create_map_user : prepares creation of a new account. can be shown in the map or not
#
#
#   IMPORTANTE : this webformn is used for different usages
#                 
#                1. it can be used to add an user which is also shown in the map
#                
#                2. it can be used to show an user which is hidden in the map. 
#                
#                   if the account has an picture stored in ists dict { 'picturl' } it will be shown.
#                   the following divs must be hidden if the account won't be shown in the map:
#                   - div_picture_url_input
#                   - div_remark_input
#                   - div_coord_inpt
#
#            for inserting into website
#            url = Page.ResolveUrl( Page.Request.Url.AbsoluteUri )
#            goal = System.Uri( Page.Request.Url, url ).AbsoluteUri
#
#
#   not strings or not for the ui:
#
#     "CAPTCHA" : "fZ+BetM/",
#     "GUID" : "ac030296eb2d41f1b60255c1b90a122a",
#     "_id" : ObjectId("51b19d8f773e6f0b0c2d6846"),
#     "account_roles" : ["free"],
#     "areasize" : "17",
#     "cities" : ["50c23447773e6f12e0075554", "50c234b1773e6f12e007575f", "50c234b1773e6f12e0075760", "50c234b0773e6f12e007575e", "50c23447773e6f12e0075555", "50c234b1773e6f12e0075761", "50c23446773e6f12e0075550", "50c234af773e6f12e0075759", "50c234b0773e6f12e007575a", "50c234b0773e6f12e007575d", "50c234af773e6f12e0075758", "50c23446773e6f12e007554e", "50c23448773e6f12e007555b", "50c234af773e6f12e0075757", "50c2344a773e6f12e0075568", "50c234b0773e6f12e007575b", "50c23449773e6f12e0075560", "50c218b1773e6f12e006dd1c", "50c218b1773e6f12e006dd1b", "50c218b1773e6f12e006dd1d", "50c218b1773e6f12e006dd1e", "50c23446773e6f12e007554f", "50c2344a773e6f12e0075567", "50c24447773e6f12e0078e7a", "50c24447773e6f12e0078e7b", "50c24447773e6f12e0078e7c", "50c24447773e6f12e0078e7d", "50c24447773e6f12e0078e7e", "50c24447773e6f12e0078e7f", "50c24447773e6f12e0078e80", "50c24447773e6f12e0078e81", "50c24447773e6f12e0078e82", "50c24447773e6f12e0078e83", "50c218b0773e6f12e006dd16"],
#     "creation_time" : "2013-06-07T08:44:56.003Z",
#     "password" : "Y2TPAEVTJDscoNnhGbxHN5qHTRcy90TN0uxp+7ZjaDmzrtDShs2o+/wFwD7lcshOtJ0nACDQO9SKuryuv6HO0Q==",
#     "post_code_key" : "DE|52222",
#     "languagecode" : "de",            !!! DropDown !!!  currently hidden
#     "marker_line" : "",
#     "item_type" : "human",            !!! DropDown !!!  used only in the initiative-webform
#
#   data that has a carresponding textbox or dropdown in the UI
#     
#     "nickname" : "Werner Broesel",
#     "picturl" : "http://guikblog.com/wp-content/uploads/2012/08/anonymus-logo-.png",
#     "info" : "",
#     "countrycode" : "DE",             !!! DropDown !!!
#     "postcode" : "52222",
#     "email" : "njb01@t-online.de",
#     "emailconfirm" : "njb01@t-online.de",
#     "txbx_pwd1"                       special: is not copied 1:1 to database. only the hash will be stored once
#     "txbx_pwd2"                       special: is not copied 1:1 to database. only the hash will be stored once
#     "lat" : "50.7896933455",
#     "lon" : "6.22481537726",
#     "website" : "http://www.werner.de"
#     "twitter" : "",
#     "facebook" : "",
#     "google_plus" : "werner_g+",
#     "skype" : "",
#     "mobile" : "",
#     "phone" : "",
#     "fax" : "5455455445",
#     "forename" : "",
#     "familyname" : "",
#     "street" : "",
#     "housenumber" : "",
#     "locationname" : "[DE] 52222 Stolberg (Rheinland)"
#
#
#
#
#
#
#
#
#
#
import System
from System.Web.Configuration import *          # web.config will be used
from System import Guid                         # CREATE GLOBAL UNIQUE id
from System import Text
from System import DateTime
from System.Net import *
from System.Net.Mail import *
from System import UriPartial

import traceback                                # for better exception understanding
import random
import re                                       # check for float in lat- and lon- input
import mongoDbMgr                               # father : the acces to the database

import clr                                                      # external libraries
clr.AddReference('MongoDB.Bson')                                # mongo-db
clr.AddReference('MongoDB.Driver')
from MongoDB.Bson import *
from MongoDB.Driver import *



# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
#
# helper for wbf_activemap/create_map_user.aspx.py
#  
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
#class LOCALCreateMapUser(mongoDbMgr.mongoMgr):
#    # ***********************************************************************************************************************************************
#    # constructor : call the base class constructor to initialize log, cache, ui-helper and page-member
#    #
#    # 28.11.2011    berndv  initial realese
#    # ***********************************************************************************************************************************************
#    def __init__(self, pg):
#        try:
#            mongoDbMgr.mongoMgr.__init__(self, pg)      # wake up papa ; mother njbTools is included by inheritance!
#            self.ui.getCtrlTree( pg )
#            self.confirmUrl = None
#            # self.log.w2lgDvlp('constructor of class CreateMapUser(Page) called!')

#        except Exception,e:
#            self.log.w2lgError(traceback.format_exc())


#    # ***********************************************************************************************************************************************
#    # createUser : function strats user registration process (incl. MailCaptcha)
#    #
#    # 29.11.2011    berndv  initial realese
#    # 05.05.2013    berndv  added location-check
#    # ***********************************************************************************************************************************************
#    def createUser(self):
#        try:
#            self.okFlag = True                                                  # indicator if something went wrong
#            if self.okFlag is True : self.okFlag = self.checkDoubles()          # check password and email input
#            if self.okFlag is True : self.okFlag = self.checkInput()            # check input (all edits must be filled)
#            if self.okFlag is True : self.okFlag = self.checkAlreadyExisting()  # if eMail allready taken warn user about ( later option: change password !!)
#            if self.okFlag is True : self.okFlag = self.createSessionDict()     # copy the user input into the session-cache self.ui.usrdata[]
#            if self.okFlag is True : self.okFlag = self.createCodes()           # generate captcha and GUID for the user
#            if self.okFlag is True : self.okFlag = self.createNickName()        # if user has not added a nickname the function creates the name displayed in the system
#            if self.okFlag is True : self.okFlag = self.createPlaceList()       # convert seperated-string-list to arrays. this makes it possible 2 add indexes in the mongo-db
#            if self.okFlag is True : self.okFlag = self.createMarker()          # function cretes the document-elements needed to diplay the markers in the map
#            if self.okFlag != True : return False
#            self.okFlag = self.writeUser2Db()                                   # store stuff into database

#            # send the user an email with the confirmation-code and the link to end the registration-process
#            if self.okFlag is True : self.okFlag = self.prepMail()
#            if self.okFlag is True : self.okFlag = self.sendMail()

#            if self.okFlag != True : 
#                self.log.w2lgDvlp('error when creating user account. writing to DB or sending email was not working for : ' + str( self.usrDt.userDict['email'] ) )
#                return False

#            return True

#        except Exception,e:
#            self.log.w2lgError(traceback.format_exc())


#    # ***********************************************************************************************************************************************
#    # checkDoubles : function checks the input that must be given double:
#    #                email and password
#    #
#    # 29.11.2011    berndv  initial realese
#    # 07.06.2013    berndv  added new check-function
#    # ***********************************************************************************************************************************************
#    def checkDoubles(self):
#        try:
#            # check users password choice
#            pwd1 = self.ui.getCtrl(  'txbx_pwd1').Text
#            pwd2 = self.ui.getCtrl(  'txbx_pwd2').Text
#            email1 = self.ui.getCtrl('txbx_email').Text
#            email2 = self.ui.getCtrl('txbx_emailconfirm').Text

#            if ( pwd1 != pwd2 ) :
#                self.errorMessage( self.ui.getCtrl('msg_pwdNotMatch').Text )
#                return False

#            if ( len(pwd1) < 5) :
#                self.errorMessage( self.ui.getCtrl('msg_pwdToShort').Text  )
#                return False

#            if ( email1 != email2 ) :
#                self.errorMessage( self.ui.getCtrl('msg_emailNotMatch').Text )
#                return False

#            # check mail is a valid address
#            if not re.match( '[^@]+@[^@]+\.[^@]+' , email1 ) :
#                self.errorMessage( self.ui.getCtrl('msg_emailWrongFormat').Text )
#                self.log.w2lgDvlp('wrong email formating  regular expression : ' + email1 )
#                return False

#            if len(email1) < 7:
#                self.errorMessage( self.ui.getCtrl('msg_emailWrongFormat').Text )
#                self.log.w2lgDvlp('wrong email formating  less than 7 chars  : ' + email1 )
#                return False

#            return True

#        except Exception,e:
#            self.log.w2lgError(traceback.format_exc())
#            self.okFlag = False


#    # ***********************************************************************************************************************************************
#    # checkInput : check users input and stop process if he has forgotten some stuff
#    #
#    # 29.11.2011    berndv  initial realese
#    # 07.06.2013    berndv  added new check-function
#    # ***********************************************************************************************************************************************
#    def checkInput(self):
#        try:
#            txtExsts = 1
            
#            # get the input of the needed edits
#            include = ['txbx_nickname','txbx_postcode','txbx_email','txbx_emailconfirm','txbx_pwd1','txbx_pwd2']
#            self.ui.getCtrlTxt('txbx_')
#            for item in self.ui.ctrlDict.keys():
#                if item not in include : break
#                txt = self.ui.ctrlDict[item].Text.strip()
#                if len( txt ) == 0: 
#                    return False

#            if (txtExsts != 1) :
#                self.errorMessage( self.ui.getCtrl('msg_inputGap').Text )
#                return False

#            # check if user accepst data-protection-agreement
#            if self.ui.getCtrl('ckbx_accept_privacy_statement').Checked == False:
#                self.errorMessage( self.ui.getCtrl('msg_accept_privacy').Text )
#                return False

#            return True

#        except Exception,e:
#            self.log.w2lgError(traceback.format_exc())
#            self.okFlag = False


#    # ***********************************************************************************************************************************************
#    # alreadyExisting : this function checks if we already have a user with the given mailadress
#    #
#    # 02.12.2011    berndv  initial realese
#    # 07.06.2013    berndv  added new check-function
#    # ***********************************************************************************************************************************************
#    def checkAlreadyExisting(self):
#        try:
#            # check in collection user.final if user allread exists, which means email allready in use
#            # if so later we will open a renew-password weform
#            userLogin = self.ui.getCtrl('txbx_email').Text
#            coll = self.database.GetCollection('user.final')                # set the collection to be accesed
#            qry  = QueryDocument('email',userLogin)                         # prepare the query to search the needed document
#            doc = coll.Find(qry)                                     
#            count = doc.Count()
#            self.log.w2lgDvlp('number of found docs in the user.final-collection - ' + str(count) + ' for : ' + userLogin )

#            if count != 0 :                 # email is already in use : later nejoba will open a renew-password-dialog here (with email-captcha)
#                self.errorMessage( self.ui.getCtrl('msg_userAlreadyExists').Text )
#                self.log.w2lgDvlp( 'there is already an account for ' + userLogin + '! Account can not be created !' )
#                return False

#            return True

#        except Exception,e:
#            self.log.w2lgError(traceback.format_exc())
#            self.okFlag = False


#    # ***********************************************************************************************************************************************
#    # createSessionDict : write users input into the User-Data dictionary
#    #
#    # 29.11.2011    berndv  initial realese
#    # 07.06.2013    berndv  added new check-function
#    # ***********************************************************************************************************************************************
#    def createSessionDict(self):
#        try:
#            # 1.  copy the stuff from the inputs (filled by user or ajax) into the session-cache of the user
#            self.ui.getCtrlTxt('txbx_')
#            for item in self.ui.ctrlDict.keys():
#                if (item != None) and ('txbx_pwd' not in item):
#                    # get the textboxes
#                    if item.find('txbx_') == 0:
#                        key = item[5:]
#                        value = self.ui.ctrlDict[item].Text.strip()
#                        self.usrDt.addNewItem(key, value)

#            # 2. if no picture given we add a default pict (anonymus)
#            if len( self.usrDt.getItem('picturl')) == 0:
#                anonymusPictUrl = 'http://guikblog.com/wp-content/uploads/2012/08/anonymus-logo-.png'
#                #anonymusPictUrl = './img/anonymous_logo_small.png'
#                self.usrDt.userDict['picturl'] = anonymusPictUrl
            
#            # 3. add special-items that are not editable
#            # key = 'creationtime'
#            # value = System.DateTime.UtcNow
#            # self.usrDt.addNewItem(key, value)
#            key = 'countrycode'
#            value = self.ui.ctrlDict['drpd_countrycode'].SelectedValue
#            self.usrDt.addNewItem(key, value)
#            key = 'languagecode'
#            value = self.ui.ctrlDict['drpd_language'].SelectedValue
#            self.usrDt.addNewItem(key, value)
#            key = 'areasize'
#            value = WebConfigurationManager.AppSettings['areaSize']
#            self.usrDt.addNewItem(key, value)
#            key = 'item_type'
#            value = self.ui.ctrlDict['drpd_item_type'].SelectedValue
#            self.usrDt.addNewItem(key, value)
#            key = 'password'
#            value = self.EncryptSHA512Managed( self.ui.getCtrl('txbx_pwd1').Text.strip() )
#            self.usrDt.addNewItem(key, value)

#            # 4.  write the items in the user-cache to the log for debugging-reasons
#            self.log.w2lgDvlp('-- start -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- what is in the user-session dict after createSessionDict' )
#            for item in self.usrDt.userDict.keys():
#                self.log.w2lgDvlp( 'name of ctrl : ' + item + '     | text-value  : ' + unicode(self.usrDt.userDict[item]) )
#            self.log.w2lgDvlp('-- end   -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- what is in the user-session dict after createSessionDict' )

#            return True

#        except Exception,e:
#            self.log.w2lgError(traceback.format_exc())
#            self.okFlag = False


#    # **********************************************************************************************************************************************************************************************************************************************************************************************
#    # createCodes : create an random captcha code and a GUID for the mail. the guid is used as url-parameter 
#    #
#    # 29.11.2011    berndv  initial realese
#    # 07.06.2013    berndv  added new check-function
#    # ***********************************************************************************************************************************************
#    def createCodes(self):
#        try:
#            guid = System.Guid.NewGuid().ToString('N')                                              # global unique ID
            
#            codeSource         = WebConfigurationManager.AppSettings['CodeGenQueue']                # get configuration from web.config
#            lengthCaptchaStrng = int(WebConfigurationManager.AppSettings['captchaStrngLngth'])
            
#            captcha = ''                                                                            # create captcha code
#            for a in range(lengthCaptchaStrng):
#                apd = random.choice(codeSource)
#                captcha += apd
            
#            self.usrDt.addNewItem('GUID', guid)                                                     # save to session cache
#            self.usrDt.addNewItem('CAPTCHA', captcha)

#            return True

#        except Exception,e:
#            self.log.w2lgError(traceback.format_exc())
#            self.okFlag = False


#    # ***********************************************************************************************************************************************
#    # writeUser2Db : store the user data in the mongo databases. the copy to the sql-server membership db will be done in verify_user.py 
#    #
#    # 09.01.2012    berndv  initial realese
#    # 07.06.2013    berndv  added new check-function
#    # ***********************************************************************************************************************************************
#    def createNickName(self):
#        try:
#            nckname = self.usrDt.userDict['nickname']                   # check if there is a display-name chosen by the user. if not there will be created one automatically
#            if (len(nckname) < 1):
#                self.usrDt.userDict['nickname'] = 'Anonymus'            # nckname = self.usrDt.userDict['forename'] + ' ' + self.usrDt.userDict['familyname']
#            return True

#        except Exception,e:
#            self.log.w2lgError(traceback.format_exc())
#            self.okFlag = False


#    # ***********************************************************************************************************************************************
#    # createPlaceList : user has gave aus a country-code and a post-code. this will be the middle of his service-area where he can check be active
#    #                   this function generates a list with the ids of all cities that are inside the area-size that is configured in web.config area-size
#    #
#    #                   the list will contain the ids of the cities that are of interest
#    #                   
#    #
#    # 08.12.2012    berndv  initial realese
#    # 07.01.2013    bervie  changed getPlacesByPostcode
#    #                       function now returns all data than only a part. the index has changed
#    #                       cities.Add(item[0]) to cities.Add(item[1])
#    # 07.06.2013    berndv  added new check-function
#    # ***********************************************************************************************************************************************
#    def createPlaceList(self):
#        try:
#            areaSize        = self.usrDt.userDict['areasize']                               # self.log.w2lgDvlp('CreateMapUser.createPlaceList creating a array with the places that belong to this account !!')
#            countryCode     = self.usrDt.userDict['countrycode']
#            postCode        = self.usrDt.userDict['postcode']

#            self.log.w2lgDvlp('areaSize        = ' + areaSize   )
#            self.log.w2lgDvlp('countryCode     = ' + countryCode)
#            self.log.w2lgDvlp('postCode        = ' + postCode   )
#            places = self.geoSrc.getPlacesByPostcode( countryCode, postCode, areaSize )     # get an sorted array with the service-area of the user and store it into the usr-session

#            cities = []
#            for item in places : cities.Add(item[1])

#            # if no cities were found abort insert
#            if len(cities) == 0:
#                errStr = self.ui.getCtrl('msg_unknownPlace').Text 
#                self.errorMessage(errStr)
#                self.okFlag = 0
#                return

#            self.usrDt.userDict['cities'] = cities
#            self.log.w2lgDvlp('cities added    = ' + str(type(cities)) + ' number of items : ' + str(len(cities)) )

#            # 21.05.2013 add the coordinates for the marker in the map ------------------------------------------------------------------------
#            # 'latitude'               6
#            # 'longitude'              7
#            hometown = places[0]
#            lat = float(hometown[5])
#            lon = float(hometown[6])

#            return self.applyGeoCoords(lat,lon)

#        except Exception,e:
#            self.log.w2lgError(traceback.format_exc())
#            self.okFlag = False


#    # **********************************************************************************************************************************************************************************************************************************************************************************************
#    # applyGeoCoords : store the coordinates for the item. if we have no user input the function will create a random-point.
#    #
#    # param : lat    : the geographical latitude
#    #         lon    : the geographical longitude
#    #
#    # returns nothing
#    #
#    # 31.05.2013    bervie  initial realese
#    # 07.06.2013    berndv  added new check-function
#    # ***********************************************************************************************************************************************
#    def applyGeoCoords(self, lat, lon ):
#        try:
#            inptLat = self.ui.getCtrl('txbx_lat').Text.strip()
#            inptLon = self.ui.getCtrl('txbx_lon').Text.strip()
            
#            # check if the input for lat and long are floats. if correct system will use users input
#            if ( re.match("^\d+?\.\d+?$", inptLat ) ) and ( re.match("^\d+?\.\d+?$", inptLon ) ) : return True

#            # input must be valid float (checked before) or empty. if some chars were found in the edits this is an error
#            if ( (len(inptLat) > 0 ) or  (len(inptLon) > 0 )) : 
#                errStr = self.ui.getCtrl('msg_stupid_coords').Text 
#                self.errorMessage(errStr)
#                self.okFlag = 0
#                return False

#            # create a random-point in the area of the user
#            rndDstnc = float( WebConfigurationManager.AppSettings['mapRndDistance'] )
#            point = self.geoSrc.getRandomPoint( lat, lon, rndDstnc )
#            self.usrDt.userDict['lat'] = str( point.lat )
#            self.usrDt.userDict['lon'] = str( point.lon )
#            self.ui.getCtrl('txbx_lat').Text = str( point.lat )
#            self.ui.getCtrl('txbx_lon').Text = str( point.lon )

#            # write it to the log for deverloping aid
#            self.log.w2lgDvlp('CreateMapUser.applyGeoCoords added marker coordinates by random function in self.geoSrc.getRandomPoint : lat ' + self.usrDt.getItem('lat') + ' - long: ' + self.usrDt.getItem('lon') )

#            return True

#        except Exception,e:
#            self.log.w2lgError(traceback.format_exc())
#            self.okFlag = False


#    # **********************************************************************************************************************************************************************************************************************************************************************************************
#    # createMarker : function creates and stores the data-elements that are needed to display the marker in the map
#    #
#    # returns nothing
#    #
#    # 31.05.2013    bervie  initial realese
#    # 05.06.2013    bervie  if 'ckbx_map_confirmation' is nit checked the "marker_line" in the DB will be empty. 
#    #                       the account won't be displayed in the map in that case
#    # 07.06.2013    berndv  added new check-function
#    # ***********************************************************************************************************************************************
#    def createMarker( self ):
#        try:
#            countrycode = self.ui.ctrlDict['drpd_countrycode'].SelectedValue
#            postcode = self.ui.ctrlDict['txbx_postcode'].Text.strip()
#            postkey = countrycode + '|' + postcode

#            # add the postcode-key ['DE|41836']
#            self.usrDt.addNewItem( 'countrycode'  , countrycode )
#            self.usrDt.addNewItem( 'postcode'     , postcode )
#            self.usrDt.addNewItem( 'post_code_key', postkey)

#            marker = System.String.Empty
#            if self.ui.getCtrl('ckbx_map_confirmation').Checked is True:                #  05.06.13 only insert a marker-line for the map when the user wants to be added to the map
#                marker = self.mapUser.createMarkerLine( self.usrDt.userDict )

#            self.usrDt.addNewItem( 'marker_line', marker )

#            return True

#        except Exception,e:
#            self.log.w2lgError(traceback.format_exc())
#            self.okFlag = False


#    # **********************************************************************************************************************************************************************************************************************************************************************************************
#    # writeUser2Db : store the user data in the mongo databases. the collection "user.initial" will be used to store all accounts that where created 
#    #                when approved the data will be copied to user.final
#    #
#    # 09.01.2012    berndv  initial realese
#    # 07.06.2013    berndv  added new check-function
#    # ***********************************************************************************************************************************************
#    def writeUser2Db(self):
#        try:
#            # self.log.w2lgDvlp('CreateUser.writeUser2Db called to store the user-data into mongo collection: user.initial')
#            ctrlDct = {'collection':'user.initial','slctKey':None,'data':self.usrDt.userDict}
#            newObjId = self.insertDoc(ctrlDct)

#            return True

#        except Exception,e:
#            self.log.w2lgError(traceback.format_exc())
#            self.okFlag = False


#    # ***********************************************************************************************************************************************
#    # prepMail : to finalize the user-registration an email with a captcha code is send to the user. the user must enter this captcha code and 
#    #            his password in the verification webform AppSettings['captchaWebForm']. the message for that mail is porepared here
#    #
#    # 25.11.2011    berndv  initial realese
#    # 07.06.2013    berndv  added new check-function
#    # ***********************************************************************************************************************************************
#    def prepMail( self ):
#        try:
#            # load the template for the HTML-mail
#            template = self.Page.Server.MapPath( WebConfigurationManager.AppSettings['ConfirmUserHtmlBody'] )
#            self.log.w2lgDvlp('ConfirmUser->prepMail      = ' + template )
#            file = open(template)
#            mailBody = file.read()
#            file.close()

#            # get the configuration from the session cache
#            cptch = self.usrDt.getItem('CAPTCHA')
#            guid  = self.usrDt.getItem('GUID')

#            captchaWebForm = self.Page.ResolveUrl(WebConfigurationManager.AppSettings['confirmUserForMap'])
#            self.confirmUrl = self.Page.Request.Url.GetLeftPart( UriPartial.Authority )
#            self.confirmUrl += captchaWebForm + "?key=" + guid

#            # get mail-strings from the UI
#            mailSubj = self.ui.getCtrl('msg_mailSubject').Text
#            mailBody = mailBody.replace('###body###'  , cptch)
#            mailBody = mailBody.replace('###link###'  , self.confirmUrl)
#            mailBody = mailBody.replace('###link2###' , self.confirmUrl)

#            self.mailSubj = unicode(mailSubj)
#            self.mailBody = unicode(mailBody)

#            return True

#        except Exception,e:
#            self.log.w2lgError(traceback.format_exc())
#            self.okFlag = False


#    # ***********************************************************************************************************************************************
#    # sendMail : to finalize the user-registration an email with a captcha code is send to the user. the user must enter this captcha code and 
#    #            his password in the verification webform AppSettings['captchaWebForm']. the message for that mail is porepared here
#    #
#    #            IMPORTANT: it migth be necesary to change the iis configuration
#    #            http://forums.asp.net/t/1404427.aspx/1
#    #
#    #            http://celestialdog.blogspot.com/2011/04/how-to-send-e-mail-using-ironpython.html
#    #
#    # 25.11.2011    berndv  initial realese
#    # 07.06.2013    berndv  added new check-function
#    # ***********************************************************************************************************************************************
#    def sendMail( self ):
#        try:
#            smtpServer = WebConfigurationManager.AppSettings['smtpServer']
#            smtpUser = WebConfigurationManager.AppSettings['smtpUser']
#            smtpPwd = WebConfigurationManager.AppSettings['smtpPwd']
#            fromAddr = WebConfigurationManager.AppSettings['cptchSndrAdrss']
#            toAddrs = self.usrDt.getItem('email')

#            try:
#                #Create A New SmtpClient Object
#                mailClient              = SmtpClient(smtpServer,25)
#                mailClient.EnableSsl    = True
#                mailCred                = NetworkCredential()
#                mailCred.UserName       = smtpUser
#                mailCred.Password       = smtpPwd
#                mailClient.Credentials  = mailCred

#                msg = MailMessage( fromAddr, toAddrs)
#                msg.SubjectEncoding = System.Text.Encoding.UTF8
#                msg.BodyEncoding =  System.Text.Encoding.UTF8
#                msg.IsBodyHtml          = True
#                msg.Subject = self.mailSubj
#                msg.Body = self.mailBody

#                mailClient.Send(msg)

#            except Exception,e:
#                self.log.w2lgError(traceback.format_exc())
#                self.okFlag = False

#            return True

#        except Exception,e:
#            self.log.w2lgError(traceback.format_exc())
#            self.okFlag = False


#    # ***********************************************************************************************************************************************
#    # changeUser( .. )  : function is called to change the data of an existing user-account
#    #
#    # 02.01.2013    berndv  initial realese
#    # ***********************************************************************************************************************************************
#    def changeUser(self):
#        try:
#            self.log.w2lgDvlp( 'CreateUser->change user called !  !   !  !   !  !   !  !   !  !   !  !   !  !   !  !    ' )
#            self.checkInptBeforeUpdt()
#            if self.okFlag == True :
#                self.updateUserData()
#                tool.ui.getCtrl('divPwdChanged').Visible = True
#                tool.ui.getCtrl('btn_Create').Visible = False

#        except Exception,e:
#            self.log.w2lgError(traceback.format_exc())
#            self.okFlag = True


#    # ***********************************************************************************************************************************************
#    # checkInptBeforeUpdt( .. )  :  check input before write to data-base
#    #
#    # 02.01.2013    berndv  initial realese
#    # ***********************************************************************************************************************************************
#    def checkInptBeforeUpdt(self):
#        try:
#            self.okFlag = True
#            # check users password choice
#            # REMARK: we are using hidden asp.net lable-controlls for the status messages to make the internationalization of the application more easy
#            pwd1 = self.ui.getCtrl('txbx_pwd1').Text
#            pwd2 = self.ui.getCtrl('txbx_pwd2').Text
#            self.log.w2lgDvlp('password             : ' + pwd1 )
#            self.log.w2lgDvlp('password confirmation: ' + pwd1 )

#            if ( pwd1 != pwd2 ) :
#                errStr = self.ui.getCtrl('msg_pwdNotMatch').Text 
#                self.errorMessage(errStr)
#                self.okFlag = False
#                return self.okFlag
#            if ( len(pwd1) < 5) :
#                errStr = self.ui.getCtrl('msg_pwdToShort').Text
#                self.errorMessage(errStr)
#                self.okFlag = 0
#                return self.okFlag

#            return self.okFlag

#        except Exception,e:
#            self.log.w2lgError(traceback.format_exc())


#    # ***********************************************************************************************************************************************
#    # updateUserData( .. )  : used to change the user-data of an existing account
#    #
#    # 02.01.2013    berndv  initial realese
#    # ***********************************************************************************************************************************************
#    def updateUserData(self):
#        try:
#            self.ui.getCtrlTxt('txbx_')
#            for item in self.ui.ctrlDict.keys():
#                if (item != None) and ('txbx_pwd' not in item):

#                    # get the textboxes
#                    if (item.find('txbx_') == 0) and ('password' not in item):
#                        key = item[5:]
#                        value = self.ui.ctrlDict[item].Text.strip()
#                        if value != System.String.Empty:
#                            self.usrDt.addNewItem(key,value)
#                            self.log.w2lgDvlp( 'create_map_user->updateUserData : KEY : ' + key + '    \t | value  : ' + value )

#            self.usrDt.userDict[ 'areasize' ]       = WebConfigurationManager.AppSettings['areaSize']
#            self.usrDt.userDict[ 'countrycode' ]    = self.ui.ctrlDict['drpd_countrycode'].SelectedValue
#            self.usrDt.userDict[ 'languagecode' ]   = self.ui.ctrlDict['drpd_language'].SelectedValue
#            self.usrDt.userDict[ 'creationtime' ]   = System.DateTime.UtcNow
#            self.usrDt.userDict[ 'item_type' ]      = self.ui.ctrlDict['drpd_item_type'].SelectedValue

#            # if no picture is given we use a default pict (anonymus)
#            if len( self.usrDt.getItem('picturl')) == 0:
#                anonymusPictUrl = 'http://guikblog.com/wp-content/uploads/2012/08/anonymus-logo-.png'
#                #anonymusPictUrl = './img/anonymous_logo_small.png'
#                self.usrDt.userDict[ 'picturl'] = anonymusPictUrl


#            for ky in self.usrDt.userDict.keys():
#                self.log.w2lgDvlp( 'cretae_map_user -> updateUserData : check dict data      : ' + str(ky) + ' ; value : ' + self.usrDt.userDict[ky].ToString()  )

#            self.createMarker()         # create a new marker for the map if user wants to
            
#            ignore = ['_id','cities','account_roles']   # update does insert all stuff as strings !! so some parts of the dictoonary should NOT be updated
#            for keyInDct in self.usrDt.userDict.keys():
#                ky = keyInDct.ToString()
#                vl = self.usrDt.userDict[keyInDct].ToString()
#                if ky in ignore : break

#                value = self.usrDt.userDict[key].ToString()
#                self.log.w2lgDvlp( '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -- - - - - - - -- - - - - - - -- - - - - - - -- - - - - - - - ' )
#                self.log.w2lgDvlp( 'cretae_map_user -> updateUserData : item to update               : ' + ky )
#                self.log.w2lgDvlp( 'cretae_map_user -> updateUserData : value of the item            : ' + vl )
#                self.log.w2lgDvlp( '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -- - - - - - - -- - - - - - - -- - - - - - - -- - - - - - - - ' )
#                updt = {}
#                updt.update({'collection':'user.final'})
#                updt.update({'slctKey': '_id' })
#                updt.update({'slctVal':self.usrDt.getItem('_id')})

#                updt.update({'updatKey':ky })
#                updt.update({'updatVal':vl })
#                chngdId = self.updateDoc(updt)
#                self.log.w2lgDvlp( 'changed data of user.final-mongo-document : ' + chngdId + ' key  ' + ky + ' val  ' + vl )


#            # special-case : if password is not empty update the password in crypted form
#            password = self.ui.findCtrl(self.Page , 'txbx_pwd1').Text
#            if password == System.String.Empty:
#                return

#            password = self.EncryptSHA512Managed(self.ui.getCtrl('txbx_pwd1').Text)
#            self.usrDt.userDict['password'] = password

#            updt = {}
#            updt.update({'collection':'user.final'})
#            updt.update({'slctKey': '_id' })
#            updt.update({'slctVal':self.usrDt.getItem('_id')})

#            updt.update({'updatKey':'password' })
#            updt.update({'updatVal': password  })
#            chngdId = self.updateDoc(updt)
#            self.log.w2lgDvlp( 'changed password crypted of user.final-mongo-document : ' + chngdId )

#        except Exception,e:
#            self.log.w2lgError(traceback.format_exc())

















































































from srvcs.tls_WbFrmClasses import CreateMapUser
tool = CreateMapUser(Page)

#tool = LOCALCreateMapUser(Page) 

# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 18.03.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    try:
        # hide the main-user-interface after a button-click and show  a please-wait sedativ
        tool.ui.hideFormAfterClick()
        tool.errorMessage('')

        for item in tool.usrDt.userDict.keys():
            tool.log.w2lgDvlp( 'create_map_user.aspx.py->Page_Load                                name of ctrl : ' + item + '     | text-value  : ' + unicode(tool.usrDt.userDict[item]) )


        # if user is logged_in use edit-mode for enable change of user_data
        if not IsPostBack:
            if Page.Request.QueryString['insert'] == 'map' :
                tool.ui.getCtrl('ckbx_map_confirmation').Checked = True
                tool.ui.getCtrl('div_picture_url_input').Visible = True
                tool.ui.getCtrl('div_remark_input').Visible = True
                tool.ui.getCtrl('div_coord_inpt').Visible = True
            else:
                # tool.ui.getCtrl('ckbx_map_confirmation').Checked = False #
                tool.ui.getCtrl('div_picture_url_input').Visible = False
                tool.ui.getCtrl('div_remark_input').Visible = False
                tool.ui.getCtrl('div_coord_inpt').Visible = False

            if tool.usrDt.isLoggedIn():
                ToggleEditMode()                                                        # switch machine to the edit-mode

                cntryCode = tool.usrDt.userDict['countrycode'].ToString()               # set the country of the user
                tool.ui.getCtrl('drpd_countrycode').SelectedValue = cntryCode

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ------------------------------------------------------------------------------------------------------------------------------------------------##__handler ------------------------------------------------
# ***********************************************************************************************************************************************
# HndlrButtonClick    : handler for button-click-events. chose button by ID
#
# 18.11.2012  - bervie -     initial realese
# 05.05.2013  - bervie -     added check if invalif postcode was given
# ***********************************************************************************************************************************************
def HndlrButtonClick(sender, e):
    try:
        if sender.ID == 'btn_Create':
            if tool.usrDt.isLoggedIn():
                tool.changeUser()               # change the data of logged-in user
            else:
                tool.createUser()               # create a new user-account

        
        if sender.ID == 'ckbx_map_confirmation':                                        # the checkbox was activated
            if tool.ui.getCtrl('ckbx_map_confirmation').Checked == True:                # toogle visibility of controls needed for the map
                tool.ui.getCtrl('div_picture_url_input').Visible = True
                tool.ui.getCtrl('div_remark_input').Visible = True
                tool.ui.getCtrl('div_coord_inpt').Visible = True
            else:
                tool.ui.getCtrl('div_picture_url_input').Visible = False
                tool.ui.getCtrl('div_remark_input').Visible = False
                tool.ui.getCtrl('div_coord_inpt').Visible = False

            return

        # when there was an mistake in user create do not make an redirect
        if tool.okFlag != 1 :
            return

        # check if we had a valid postcode. if not make no redirect
        if not tool.usrDt.userDict.has_key('cities'):
            errStr = tool.ui.getCtrl('msg_unknownPlace').Text
            tool.errorMessage(errStr)
            return

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return

    if tool.confirmUrl != None :
        tool.log.w2lgDvlp('CreateUser redirects to : ' +  unicode(tool.confirmUrl) )
        Response.Redirect( Page.ResolveUrl( tool.confirmUrl ) )


# ------------------------------------------------------------------------------------------------------------------------------------------------##__handler ------------------------------------------------
# ***********************************************************************************************************************************************
# ToggleEditMode    : create user is in change-mode
#
# 18.11.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def ToggleEditMode():
    try:
        # change headline from create to edit user
        newTxt = tool.gtCtl('edit_headline_label').Text
        lable = tool.gtCtl('lbl_headline')
        lable.Text = newTxt

        # change button-lable to change-user
        newTxt = tool.gtCtl('hidden_button_edit_text').Text
        button = tool.gtCtl('btn_Create')
        button.Text = newTxt

        # disable unchangeable data
        emailTxBx = tool.gtCtl('txbx_email')
        emailTxBx.Enabled = False
        emailTxBxCnf = tool.gtCtl('txbx_emailconfirm')
        emailTxBxCnf.Enabled = False
        nickTxBx = tool.gtCtl('txbx_nickname')
        nickTxBx.Enabled = False
        tool.gtCtl('messagebox').Visible = False

        #tool.gtCtl('messageemailsend').Visible = False
        tool.gtCtl('messageacceptprivacy').Visible = False

        # check the invisible checkbox to pass the input-validation
        tool.gtCtl('ckbx_accept_privacy_statement').Checked = True

        # the location can also not be changed afterwards
        tool.gtCtl('txbx_postcode').Enabled = False
        tool.gtCtl('txbx_locationname').Text = tool.usrDt.userDict['locationname'].ToString()           # display the city-name
        tool.gtCtl('txbx_locationname').Enabled = False

        # 17.08.2013 country should also be disabeled
        tool.gtCtl('drpd_countrycode').Enabled = False

        # remove notes for "create_user"
        #tool.gtCtl('lbl_headmsg01').Visible = False
        #tool.gtCtl('lbl_headmsg02').Visible = False
        tool.gtCtl('lbl_whatisthenejobaname').Visible = False

        UserDataToUi()

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return


# ***********************************************************************************************************************************************
# UserDataToUi    : get data from the user-session-dict ans copy it into the webform
#
# 18.11.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def UserDataToUi():
    try:
        # set the country of user
        tool.ui.getCtrl('drpd_countrycode').SelectedValue = tool.usrDt.getItem('countrycode')
        # put dict-data to the webform
        tool.ui.getCtrl('txbx_nickname').Text       = tool.usrDt.getItem('nickname')
        tool.ui.getCtrl('txbx_picturl').Text        = tool.usrDt.getItem('picturl')
        tool.ui.getCtrl('txbx_info').Text           = tool.usrDt.getItem('info')
        tool.ui.getCtrl('txbx_postcode').Text       = tool.usrDt.getItem('postcode')
        tool.ui.getCtrl('txbx_email').Text          = tool.usrDt.getItem('email')
        tool.ui.getCtrl('txbx_emailconfirm').Text   = tool.usrDt.getItem('emailconfirm')
        tool.ui.getCtrl('txbx_lon').Text            = tool.usrDt.getItem('lon')
        tool.ui.getCtrl('txbx_lat').Text            = tool.usrDt.getItem('lat')
        tool.ui.getCtrl('txbx_website').Text        = tool.usrDt.getItem('website')
        tool.ui.getCtrl('txbx_twitter').Text        = tool.usrDt.getItem('twitter')
        tool.ui.getCtrl('txbx_facebook').Text       = tool.usrDt.getItem('facebook')
        tool.ui.getCtrl('txbx_google_plus').Text    = tool.usrDt.getItem('google_plus')
        tool.ui.getCtrl('txbx_skype').Text          = tool.usrDt.getItem('skype')
        tool.ui.getCtrl('txbx_mobile').Text         = tool.usrDt.getItem('mobile')
        tool.ui.getCtrl('txbx_phone').Text          = tool.usrDt.getItem('phone')
        tool.ui.getCtrl('txbx_fax').Text            = tool.usrDt.getItem('fax')
        tool.ui.getCtrl('txbx_forename').Text       = tool.usrDt.getItem('forename')
        tool.ui.getCtrl('txbx_familyname').Text     = tool.usrDt.getItem('familyname')
        tool.ui.getCtrl('txbx_street').Text         = tool.usrDt.getItem('street')
        tool.ui.getCtrl('txbx_housenumber').Text    = tool.usrDt.getItem('housenumber')
        tool.ui.getCtrl('txbx_locationname').Text   = tool.usrDt.getItem('locationname')

        # special-case : if we have a marker-line the checkbox for "showing-data-in-map" will be checked
        # we also have to show the map-specific controls
        if len( tool.usrDt.userDict['marker_line'].ToString().strip() ) > 0 :
            tool.ui.getCtrl('ckbx_map_confirmation').Checked = True
            tool.ui.getCtrl('div_picture_url_input').Visible = True
            tool.ui.getCtrl('div_remark_input').Visible = True
            tool.ui.getCtrl('div_coord_inpt').Visible = True

        tool.ui.getCtrl('txbx_pwd1').Text   = ''
        tool.ui.getCtrl('txbx_pwd2').Text   = ''

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return

