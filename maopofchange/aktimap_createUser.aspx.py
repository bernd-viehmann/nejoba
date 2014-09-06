#  aktmap_CreateUser creates a user-account with marker on the map or a new map-marker
#
#  map-markers can only be set by users that are allready logged-in
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
import mongoDbMgr                               # father : the acces to the database

import clr                                                      # external libraries
clr.AddReference('MongoDB.Bson')                                # mongo-db
clr.AddReference('MongoDB.Driver')
from MongoDB.Bson import *
from MongoDB.Driver import *

#from srvcs.tls_WbFrmClasses import CreateUser   # helper class for this dialog
#tool = CreateUser(Page)

class CreateMapUser(mongoDbMgr.mongoMgr):

    # ***********************************************************************************************************************************************
    # constructor : call the base class constructor to initialize log, cache, ui-helper and page-member
    #
    # 28.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def __init__(self, pg):
        try:
            mongoDbMgr.mongoMgr.__init__(self, pg)      # wake up papa ; mother njbTools is included by inheritance!
            self.okFlag = 1                     # flag indicates if the input was correct
            self.confirmUrl = None

            self.log.w2lgDvlp('constructor of class CreateMapUser(Page) aufgefufen!')

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # createUser : function strats user registration process (incl. MailCaptcha)
    #
    # 29.11.2011    berndv  initial realese
    # 05.05.2013    berndv  added location-check
    # ***********************************************************************************************************************************************
    def createUser(self):
        try:
            # check if input is valid to be used for a new account
            self.checkDoubles()                             # check password input from user
            self.checkInput()                               # check input (all edits must be filled)
            self.checkAlreadyExisting()                     # if eMail allready taken warn user about ( later option: change password !!)

            if self.okFlag == 0:
                self.log.w2lgError('user create was aborted for : ' + self.ui.getCtrl('txbx_email').Text )
                return;

            self.storeInput()                               # copy the user input into the input-cache

            # create artificial user-account-attributes
            self.createCodes()                              # generate captcha and GUID for the user
            self.createNickName()                           # if user has not added a nickname the function creates the name displayed in the system
            self.createPlaceList()                          # convert seperated-string-list to arrays. this makes it possible 2 add indexes in the mongo-db


            if self.okFlag == 0:
                self.log.w2lgError('user create was aborted for : ' + self.ui.getCtrl('txbx_email').Text )
                return 0;

            # 05.05.2013 if no locations were found abort process
            if not self.usrDt.userDict.has_key('cities'):
                self.log.w2lgError('user create was aborted for : ' + self.ui.getCtrl('txbx_email').Text + ' : NO CITIES FOUND ' )
                return 0;
            
            self.writeUser2Db()                             # store stuff into database

            # send the user an email with the confirmation-code and the link to end the registration-process
            self.prepMail()
            self.sendMail()

            return self.okFlag

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # checkDoubles : function checks the input that must be given double:
    #                email and password
    #
    # 29.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def checkDoubles(self):
        try:
            # check users password choice
            # REMARK: we are using hidden asp.net lable-controlls for the status messages to make the internationalization of the application more easy
            pwd1 = self.ui.getCtrl(  'txbx_pwd1').Text
            pwd2 = self.ui.getCtrl(  'txbx_pwd2').Text
            email1 = self.ui.getCtrl('txbx_email').Text
            email2 = self.ui.getCtrl('txbx_emailconfirm').Text

            if ( pwd1 != pwd2 ) :
                errStr = self.ui.getCtrl('msg_pwdNotMatch').Text 
                self.errorMessage(errStr)
                self.okFlag = 0
                return
            if ( len(pwd1) < 5) :
                errStr = self.ui.getCtrl('msg_pwdToShort').Text 
                self.errorMessage(errStr)
                self.okFlag = 0
                return

            if ( email1 != email2 ) :
                errStr = self.ui.getCtrl('msg_emailNotMatch').Text 
                self.errorMessage(errStr)
                self.okFlag = 0
                return
            if '@' not in email1:
                errStr = self.ui.getCtrl('msg_emailWrongFormat').Text 
                self.errorMessage(errStr)
                self.okFlag = 0
                return

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # checkInput : check users input and stop process if he has forgotten some stuff
    #
    # 29.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def checkInput(self):
        try:
            txtExsts = 1

            # check text-fields
            if len(self.ui.getCtrl('txbx_nickname').Text) < 1: txtExsts = 0
            if len(self.ui.getCtrl('txbx_info').Text) < 1: txtExsts = 0
            if len(self.ui.getCtrl('txbx_postcode').Text) < 1: txtExsts = 0
            if len(self.ui.getCtrl('txbx_email').Text) < 1: txtExsts = 0
            if len(self.ui.getCtrl('txbx_emailconfirm').Text) < 1: txtExsts = 0
            if len(self.ui.getCtrl('txbx_pwd1').Text) < 1: txtExsts = 0
            if len(self.ui.getCtrl('txbx_pwd2').Text) < 1: txtExsts = 0
            #if len(self.ui.getCtrl('txbx_website').Text) < 1: txtExsts = 0
            #if len(self.ui.getCtrl('txbx_picturl').Text) < 1: txtExsts = 0
            #if len(self.ui.getCtrl('txbx_twitter').Text) < 1: txtExsts = 0
            #if len(self.ui.getCtrl('txbx_skype').Text) < 1: txtExsts = 0
            #if len(self.ui.getCtrl('txbx_mobile').Text) < 1: txtExsts = 0
            #if len(self.ui.getCtrl('txbx_phone').Text) < 1: txtExsts = 0
            #if len(self.ui.getCtrl('txbx_forename').Text) < 1: txtExsts = 0
            #if len(self.ui.getCtrl('txbx_familyname').Text) < 1: txtExsts = 0
            #if len(self.ui.getCtrl('txbx_street').Text) < 1: txtExsts = 0
            #if len(self.ui.getCtrl('txbx_housenumber').Text) < 1: txtExsts = 0
            #if len(self.ui.getCtrl('txbx_city').Text) < 1: txtExsts = 0
            #if len(self.ui.getCtrl('txbx_adress_add').Text) < 1: txtExsts = 0

            if (txtExsts != 1) :
                errStr = self.ui.getCtrl('msg_inputGap').Text 
                self.errorMessage(errStr)
                self.okFlag = 0

            # check if user accepst data-protection-agreement
            if self.ui.getCtrl('ckbx_accept_privacy_statement').Checked == False:
                errStr = self.ui.getCtrl('msg_accept_privacy').Text 
                self.errorMessage(errStr)
                self.okFlag = 0

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # alreadyExisting : this function checks if we already have a user with the given mailadress
    #
    # 02.12.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def checkAlreadyExisting(self):
        try:
            # check in collection user.final if user allread exists, which means email allready in use
            # if so later we will open a renew-password weform
            userLogin = self.ui.getCtrl('txbx_email').Text
            coll = self.database.GetCollection('user.final')                # set the collection to be accesed
            qry  = QueryDocument('email',userLogin)                         # prepare the query to search the needed document
            doc = coll.Find(qry)                                     
            count = doc.Count()
            self.log.w2lgDvlp('number of found docs in the user.final-collection - ' + str(count) + ' for : ' + userLogin )

            if count == 0:
                # email adress is available for a new account
                self.log.w2lgDvlp( 'no account found for ' + userLogin + '. user-account can be created !' )

            else:
                # email is already in use : later nejoba will open a renew-password-dialog here (with email-captcha)
                errStr = self.ui.getCtrl('msg_userAlreadyExists').Text 
                self.errorMessage(errStr)
                self.log.w2lgDvlp( 'there is already an account for ' + userLogin + '. creation denied !' )
                self.okFlag = 0

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # storeInput : write users inpuit into the User-Data dictionary
    #
    # 29.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def storeInput(self):
        try:
            # 1.  copy the stuff from the inputs (filled by user or ajax) into the session-cache of the user
            self.ui.getCtrlTxt('txbx_')
            for item in self.ui.ctrlDict.keys():
                if (item != None) and ('txbx_pwd' not in item):
                    # get the textboxes
                    if item.find('txbx_') == 0:
                        key = item[5:]
                        value = self.ui.ctrlDict[item].Text.strip()
                        self.usrDt.addNewItem(key, value)

            # 2. add special-items to the user-data-dictionary
            key = 'password'
            value = self.EncryptSHA512Managed(self.ui.getCtrl('txbx_pwd1').Text)
            self.usrDt.addNewItem(key, value)
            key = 'areasize'
            value = WebConfigurationManager.AppSettings['areaSize']
            self.usrDt.addNewItem(key, value)
            key = 'countrycode'
            value = self.ui.ctrlDict['drpd_country'].SelectedValue
            self.usrDt.addNewItem(key, value)
            key = 'languagecode'
            value = self.ui.ctrlDict['drpd_language'].SelectedValue
            self.usrDt.addNewItem(key, value)
            key = 'creationtime'
            value = System.DateTime.UtcNow
            self.usrDt.addNewItem(key, value)
            key = 'item_type'
            value = self.ui.ctrlDict['drpd_item_type'].SelectedValue
            self.usrDt.addNewItem(key, value)

            # 3. if no picture given we add a default pict (anonymus)
            if len( self.usrDt.getItem('picturl')) == 0:
                # anonymusPictUrl = 'http://guikblog.com/wp-content/uploads/2012/08/anonymus-logo-.png'
                anonymusPictUrl = './img/anonymous_logo_small.png'
                self.usrDt.userDict['picturl'] = anonymusPictUrl
            
            # 4.  write the items in the user-cache to the log for debugging-reasons
            self.log.w2lgDvlp('-- start -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- what is in the user-session dict after storeInput' )
            for item in self.usrDt.userDict.keys():
                self.log.w2lgDvlp( 'name of ctrl : ' + item + '     | text-value  : ' + unicode(self.usrDt.userDict[item]) )
            self.log.w2lgDvlp('-- end   -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- what is in the user-session dict after storeInput' )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # **********************************************************************************************************************************************************************************************************************************************************************************************
    # createCodes : create an random captcha code and a GUID for the mail. the guid is used as url-parameter 
    #
    # 29.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def createCodes(self):
        try:
            guid = System.Guid.NewGuid().ToString('N')         # global unique ID

            # get configuration from web.config
            codeSource         = WebConfigurationManager.AppSettings['CodeGenQueue']
            lengthCaptchaStrng = int(WebConfigurationManager.AppSettings['captchaStrngLngth'])

            # create captcha code
            captcha = ''
            for a in range(lengthCaptchaStrng):
                apd = random.choice(codeSource)
                captcha += apd

            # save to session cache
            self.usrDt.addNewItem('GUID', guid)
            self.usrDt.addNewItem('CAPTCHA', captcha)

            return guid

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # writeUser2Db : store the user data in the mongo databases. the copy to the sql-server membership db will be done in verify_user.py 
    #
    # 09.01.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def createNickName(self):
        try:
            # check if there is a display-name chosen by the user. if not there will be created one automatically
            nckname = self.usrDt.userDict['nickname']
            if (len(nckname) < 1):
                # create a nickname from User input
                nckname = self.usrDt.userDict['forename'] + ' ' + self.usrDt.userDict['familyname']
                self.usrDt.userDict['nickname'] = nckname
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # createPlaceList : user has gave aus a country-code and a post-code. this will be the middle of his service-area where he can check be active
    #                   this function generates a list with the ids of all cities that are inside the area-size that is configured in web.config area-size
    #
    #                   the list will contain the ids of the cities that are of interest
    #                   
    #
    # 08.12.2012    berndv  initial realese
    # 07.01.2013    bervie  changed getPlacesByPostcode
    #                       function now returns all data than only a part. the index has changed
    #                       cities.Add(item[0]) to cities.Add(item[1])
    #
    # ***********************************************************************************************************************************************
    def createPlaceList(self):
        try:
            # self.log.w2lgDvlp('CreateMapUser.createPlaceList creating a array with the places that belong to this account !!')
            
            areaSize        = self.usrDt.userDict['areasize']
            countryCode     = self.usrDt.userDict['countrycode']
            postCode        = self.usrDt.userDict['postcode']

            self.log.w2lgDvlp('areaSize        = ' + areaSize)
            self.log.w2lgDvlp('countryCode     = ' + countryCode)
            self.log.w2lgDvlp('postCode        = ' + postCode )

            # get an sorted array with the service-area of the user and store it into the usr-session
            places = self.geoSrc.getPlacesByPostcode( countryCode, postCode, areaSize )

            cities = []
            for item in places:
                cities.Add(item[1])

            # if no cities were found abort insert
            if len(cities) == 0:
                errStr = self.ui.getCtrl('msg_unknownPlace').Text 
                self.errorMessage(errStr)
                self.okFlag = 0
                return
            else:
                self.usrDt.addNewItem('cities', cities)

                # 21.05.2013 add the coordinates for the marker in the map ------------------------------------------------------------------------
                # 'latitude'               6
                # 'longitude'              7
                hometown = places[0]
                lat = float(hometown[5])
                lon = float(hometown[6])
                rndDstnc = float( WebConfigurationManager.AppSettings['mapRndDistance'] )

                point = self.geoSrc.getRandomPoint( lat, lon, rndDstnc )
                self.usrDt.addNewItem('lat' , str( point.lat ) )
                self.usrDt.addNewItem('long', str( point.lon ) )

                # write it to the log for deverloping aid
                self.log.w2lgDvlp('CreateMapUser.createPlaceList added marker coordinates : lat ' + self.usrDt.getItem('lat') + ' - long: ' + self.usrDt.getItem('long') )
                # 21.05.2013 ** END **  ------------------------------------------------------------------------ ----------------------------------

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # **********************************************************************************************************************************************************************************************************************************************************************************************
    # writeUser2Db : store the user data in the mongo databases. the collection "user.initial" will be used to store all accounts that where created 
    #                when approved the data will be copied to user.final
    #
    # 09.01.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def writeUser2Db(self):
        try:
            # self.log.w2lgDvlp('CreateUser.writeUser2Db called to store the user-data into mongo collection: user.initial')
            ctrlDct = {'collection':'user.initial','slctKey':None,'data':self.usrDt.userDict}
            newObjId = self.insertDoc(ctrlDct)

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # prepMail : to finalize the user-registration an email with a captcha code is send to the user. the user must enter this captcha code and 
    #            his password in the verification webform AppSettings['captchaWebForm']. the message for that mail is porepared here
    #
    # 25.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def prepMail( self ):
        try:
            # load the template for the HTML-mail
            template = self.Page.Server.MapPath( WebConfigurationManager.AppSettings['ConfirmUserHtmlBody'] )
            self.log.w2lgDvlp('ConfirmUser->prepMail      = ' + template )
            file = open(template)
            mailBody = file.read()
            file.close()

            # get the configuration from the session cache
            cptch = self.usrDt.getItem('CAPTCHA')
            guid  = self.usrDt.getItem('GUID')

            captchaWebForm = self.Page.ResolveUrl(WebConfigurationManager.AppSettings['confirmMapUserLink'])
            self.confirmUrl = self.Page.Request.Url.GetLeftPart( UriPartial.Authority )
            self.confirmUrl += captchaWebForm + "?key=" + guid

            # get mail-strings from the UI
            mailSubj = self.ui.getCtrl('msg_mailSubject').Text
            mailBody = mailBody.replace('###body###'  , cptch)
            mailBody = mailBody.replace('###link###'  , self.confirmUrl)
            mailBody = mailBody.replace('###link2###' , self.confirmUrl)

            # self.log.w2lgDvlp(mailBody)

            self.mailSubj = unicode(mailSubj)
            self.mailBody = unicode(mailBody)
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # sendMail : to finalize the user-registration an email with a captcha code is send to the user. the user must enter this captcha code and 
    #            his password in the verification webform AppSettings['captchaWebForm']. the message for that mail is porepared here
    #
    #            IMPORTANT: it migth be necesary to change the iis configuration
    #            http://forums.asp.net/t/1404427.aspx/1
    #
    #            http://celestialdog.blogspot.com/2011/04/how-to-send-e-mail-using-ironpython.html
    #
    # 25.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def sendMail( self ):
        try:
            smtpServer = WebConfigurationManager.AppSettings['smtpServer']
            smtpUser = WebConfigurationManager.AppSettings['smtpUser']
            smtpPwd = WebConfigurationManager.AppSettings['smtpPwd']
            fromAddr = WebConfigurationManager.AppSettings['cptchSndrAdrss']
            toAddrs = self.usrDt.getItem('email')

            try:
                #Create A New SmtpClient Object
                mailClient              = SmtpClient(smtpServer,25)
                mailClient.EnableSsl    = True
                mailCred                = NetworkCredential()
                mailCred.UserName       = smtpUser
                mailCred.Password       = smtpPwd
                mailClient.Credentials  = mailCred

                msg = MailMessage( fromAddr, toAddrs)
                msg.SubjectEncoding = System.Text.Encoding.UTF8
                msg.BodyEncoding =  System.Text.Encoding.UTF8
                msg.IsBodyHtml          = True
                msg.Subject = self.mailSubj
                msg.Body = self.mailBody

                mailClient.Send(msg)

            except Exception,e:
                self.log.w2lgError(traceback.format_exc())

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # changeUser( .. )  : function is called to change the data of an existing user-account
    #
    # 02.01.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def changeUser(self):
        try:
            self.log.w2lgDvlp( 'CreateUser->change user called !  !   !  !   !  !   !  !   !  !   !  !   !  !   !  !    ' )
            self.checkInptBeforeUpdt()
            if self.okFlag != 0 :
                self.updateUserData()

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # ***********************************************************************************************************************************************
    # checkInptBeforeUpdt( .. )  :  check input before write to data-base
    #
    # 02.01.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def checkInptBeforeUpdt(self):
        try:
            # check users password choice
            # REMARK: we are using hidden asp.net lable-controlls for the status messages to make the internationalization of the application more easy
            pwd1 = self.ui.getCtrl('txbx_pwd1').Text
            pwd2 = self.ui.getCtrl('txbx_pwd2').Text
            self.log.w2lgDvlp('password             : ' + pwd1 )
            self.log.w2lgDvlp('password confirmation: ' + pwd1 )

            # if password-fields are left empty change of the pwd wanted
            if (( pwd1 == System.String.Empty ) and ( pwd2 == System.String.Empty )):
                self.okFlag = 1
                return

            if ( pwd1 != pwd2 ) :
                errStr = self.ui.getCtrl('msg_pwdNotMatch').Text 
                self.errorMessage(errStr)
                self.okFlag = 0
                return
            if ( len(pwd1) < 5) :
                errStr = self.ui.getCtrl('msg_pwdToShort').Text
                self.errorMessage(errStr)
                self.okFlag = 0
                return
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # ***********************************************************************************************************************************************
    # updateUserData( .. )  : get input from userInterface
    #
    # 02.01.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def updateUserData(self):
        try:
            # 1.  copy the stuff from the inputs (filled by user or ajax) into the session-cache of the user
            self.ui.getCtrlTxt('txbx_')
            for item in self.ui.ctrlDict.keys():
                if (item != None) and ('txbx_pwd' not in item):

                    # get the textboxes
                    if (item.find('txbx_') == 0) and ('password' not in item):
                        key = item[5:]
                        value = self.ui.ctrlDict[item].Text
                        self.log.w2lgDvlp( 'KEY : ' + key + '    \t | value  : ' + value )

                        self.usrDt.userDict[key] = value

                        updt = {}
                        updt.update({'collection':'user.final'})
                        updt.update({'slctKey': '_id' })
                        updt.update({'slctVal':self.usrDt.getItem('_id')})

                        updt.update({'updatKey':key})
                        updt.update({'updatVal':value})
                        chngdId = self.updateDoc(updt)
                        self.log.w2lgDvlp( 'changed data of user.final-mongo-document : ' + chngdId )

            # special-case : if password is not empty update the password in crypted form
            password = self.ui.findCtrl(self.Page , 'txbx_pwd1').Text
            if password == System.String.Empty:
                return

            password = self.EncryptSHA512Managed(self.ui.getCtrl('txbx_pwd1').Text)
            self.usrDt.userDict['password'] = password

            updt = {}
            updt.update({'collection':'user.final'})
            updt.update({'slctKey': '_id' })
            updt.update({'slctVal':self.usrDt.getItem('_id')})

            updt.update({'updatKey':'password' })
            updt.update({'updatVal': password  })
            chngdId = self.updateDoc(updt)
            self.log.w2lgDvlp( 'changed password crypted of user.final-mongo-document : ' + chngdId )


        except Exception,e:
            self.log.w2lgError(traceback.format_exc())













tool = CreateMapUser(Page)




# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 18.03.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    try:
        # hide the main-user-interface after a button-click and show  a please-wait sedativ
        tool.ui.getCtrlTree( Page )
        tool.ui.hideFormAfterClick()

        tool.errorMessage('')

        # if user is logged_in use edit-mode for enable change of user_data
        if not IsPostBack:
            if tool.usrDt.isLoggedIn():
                ToggleEditMode()

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
                # change the data of logged-in user
                tool.changeUser()
            else:
                # create a new user-account
                tool.createUser()

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
        tool.gtCtl('alertbox').Visible = False

        # the location can also not be changed afterwards
        tool.gtCtl('txbx_postcode').Enabled = False
        tool.gtCtl('txbx_city').Enabled = False

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
        # put dict-data to the webform 
        tool.ui.getCtrl('txbx_website').Text = tool.usrDt.getItem('website')
        tool.ui.getCtrl('txbx_nickname').Text = tool.usrDt.getItem('nickname') 
        tool.ui.getCtrl('txbx_fax').Text = tool.usrDt.getItem('fax') 
        tool.ui.getCtrl('txbx_phone').Text = tool.usrDt.getItem('phone') 
        tool.ui.getCtrl('txbx_forename').Text = tool.usrDt.getItem('forename') 
        tool.ui.getCtrl('txbx_postcode').Text = tool.usrDt.getItem('postcode') 
        tool.ui.getCtrl('txbx_city').Text = tool.usrDt.getItem('city') 
        tool.ui.getCtrl('txbx_street').Text = tool.usrDt.getItem('street') 
        tool.ui.getCtrl('txbx_familyname').Text = tool.usrDt.getItem('familyname') 
        tool.ui.getCtrl('txbx_email').Text = tool.usrDt.getItem('email') 
        tool.ui.getCtrl('txbx_mobile').Text = tool.usrDt.getItem('mobile') 
        tool.ui.getCtrl('txbx_skype').Text = tool.usrDt.getItem('skype') 
        tool.ui.getCtrl('txbx_housenumber').Text = tool.usrDt.getItem('housenumber') 
        tool.ui.getCtrl('drpd_language').SelectedValue = tool.usrDt.getItem('languagecode')
        tool.ui.getCtrl('drpd_country').SelectedValue = tool.usrDt.getItem('countrycode')
        #tool.ui.getCtrl('').Text = tool.usrDt.getItem('GUID') 
        #tool.ui.getCtrl('').Text = tool.usrDt.getItem('password') 
        #tool.ui.getCtrl('').Text = tool.usrDt.getItem('areasize') 
        #tool.ui.getCtrl('').Text = tool.usrDt.getItem('cities') 

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return














        # txbx_info
        # txbx_postcode
        # txbx_email
        # txbx_emailconfirm
        # txbx_pwd1
        # txbx_pwd2
        # txbx_website
        # txbx_picturl
        # txbx_facebook
        # txbx_google_plus
        # txbx_twitter
        # txbx_skype
        # txbx_mobile
        # txbx_phone
        # txbx_forename
        # txbx_familyname
        # txbx_street
        # txbx_housenumber
        # txbx_city
        # txbx_adress_add

        # drpd_item_type
        # drpd_country
        # drpd_language
