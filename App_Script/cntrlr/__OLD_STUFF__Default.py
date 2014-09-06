# ***********************************************************************************************************************************************
# Default : business logic for Default.aspx.py
#           used for login and starting user_registration
# 
#  15.11.2011   - berndv -              initial release
# ***********************************************************************************************************************************************
from System.Web.Security import *

import traceback                    # for better exception understanding
import mongoDbMgr                   # father : the acces to the database


class Default(mongoDbMgr.mongoMgr):
    # ***********************************************************************************************************************************************
    # constructor : call the base class constructor to initialize log, cache, ui-helper and page-member
    #
    # 19.03.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def __init__(self, pg):
        mongoDbMgr.mongoMgr.__init__(self, pg)      # wake up papa ; mother njbTools is included by inheritance!
        self.okFlag = 1                     # flag indicates if the input was correct
        self.log.w2lgDvlp('constructor of class Default(mongoDbMgr.mongoMgr) aufgefufen!')


    # ***********************************************************************************************************************************************
    # startRegistration : called by registration-click handler. start the registration-process
    #
    # 19.03.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def startRegistration(self):
        self.ui.getCtrl("lbl_register_status_message").Text = ""

        self.regOk = self.checkInput()                  # check user input
        if (self.regOk): self.regOk = self.alreadyInUse()            # check if the mail is already registered in nejoba
        if (self.regOk): self.regOk = self.sendCodeToUser()          # create and send the access-code to the users email adress
        if (self.regOk): self.regOk = self.redirectToCreate()        # go on to the webform "create_user.aspx"


    # ***********************************************************************************************************************************************
    # checkInput : check if the input-data makes sense
    #
    # 19.03.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def checkInput(self):
        try:
            # check if user has typed in some data
            lenForeName     = len(self.ui.getCtrl("txbx_forename").Text)
            lenFamilyName   = len(self.ui.getCtrl("txbx_familyname").Text)
            lenEmail        = len(self.ui.getCtrl("txbx_email").Text)
            lenEmailConfirm = len(self.ui.getCtrl("txbx_emailconfirm").Text)

            if ( lenForeName < 1 ) and (lenFamilyName < 1) and (lenEmail < 1) and (lenEmailConfirm < 1):
                message = self.ui.getCtrl("msg_input_not_complete").Text
                self.ui.getCtrl("lbl_register_status_message").Text = message
                return False

            validMail = self.ui.getCtrl("regexEmailValid1").IsValid
            validMailConfirm = self.ui.getCtrl("regexEmailValid2").IsValid

            if ((bool(validMail) != True) or (bool(validMailConfirm) != True)):
                self.log.w2lgDvlp('invalid email or email confirm in logic/Default->checkInput')
                return False

            # email confirm ok?
            email           = self.ui.ctrlDict["txbx_email"].Text
            emailconfirm    = self.ui.ctrlDict["txbx_emailconfirm"].Text

            if email != emailconfirm:
                self.log.w2lgDvlp('email and email confirm not the same in  logic/Default->checkInput')
                self.log.w2lgDvlp('email         ' + email)
                self.log.w2lgDvlp('email confirm ' + emailconfirm)
                message = self.ui.getCtrl("msg_mailaddresses_not_equal").Text
                self.ui.getCtrl("lbl_register_status_message").Text = message

                return False

            return True

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # alreadyInUse : check if the mail is already taken
    #
    # 19.03.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def alreadyInUse( self ):
        userLogin = self.ui.getCtrl('txbx_email').Text

        if( len(Membership.FindUsersByName(userLogin)) > 0  ):
            errStr = '<font color="#FF0000"><b>' + self.ui.getCtrl('msg_user_exists').Text + '</b></font>'
            self.ui.getCtrl("lbl_register_status_message").Text = errStr
            return False
        
        return True



    # ***********************************************************************************************************************************************
    # sendCodeToUser : create a captcha-code and send it to the user
    #
    # 19.03.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def sendCodeToUser( self ):
        return True


    # ***********************************************************************************************************************************************
    # redirectToCreate : send the browser to create_user.aspx
    #
    # 19.03.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def redirectToCreate(self):
        try:
            # 0. get all the shit into local vars
            self.ui.getCtrlTxt()
            forename        = self.Page.Server.UrlEncode( self.ui.inptDict["forename"] )
            familyname      = self.Page.Server.UrlEncode( self.ui.inptDict["familyname"] )
            email           = self.Page.Server.UrlEncode( self.ui.inptDict["email"] )
            emailconfirm    = self.Page.Server.UrlEncode( self.ui.inptDict["emailconfirm"] )

            self.log.w2lgDvlp('forename = ' + forename)

            # 3. finally send the user to the weform for registration-finalyzation
            targetUrl = "create_user.aspx?forename=" + forename + "&familyname=" + familyname + "&email=" + email 
            self.Page.Response.Redirect(targetUrl)

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())













