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

from System.Web.Configuration import *
from System import UriPartial
from System import DateTime
import traceback                                # for better exception understanding
import mongoDbMgr                               # father : the acces to the database

#from srvcs.tls_WbFrmClasses import ConfirmUser  # helper class for this dialog
#tool = ConfirmUser(Page)

# **********************************************************************************************************************************************************************************************************************************************************************************************
# **********************************************************************************************************************************************************************************************************************************************************************************************
# **********************************************************************************************************************************************************************************************************************************************************************************************

class ConfirmMapUser(mongoDbMgr.mongoMgr):

    # ***********************************************************************************************************************************************
    # constructor : call the base class constructor to initialize log, cache, ui-helper and page-member
    #
    # attribute:
    #    self.initialData  :  the user-data coming from pre-account-approved-collection  'user.initial'
    #
    # 28.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def __init__(self, pg):
        try:
            mongoDbMgr.mongoMgr.__init__(self, pg)      # wake up papa ; mother njbTools is included by inheritance!
            self.ui.getCtrlTree( self.Page )
            self.log.w2lgDvlp('ConfirmUser( .. ) constructor called')
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # LoadInitialData : load initial data for the user-account from collection user.initial
    #
    # 28.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def LoadInitialData( self, guid ):
        try:
            ctrlDict = {'collection':'user.initial','slctKey':'GUID','slctVal': guid }
            self.readDoc(ctrlDict)
            self.initialData = ctrlDict['data']
            self.Page.ViewState['INITIAL_USER_DATA'] = ctrlDict['data']
            self.ui.getCtrl('txbx_email').Text = self.initialData['email'].ToString()

            #for ky in self.initialData:
            #    self.log.w2lgDvlp('ConfirmUser(Page)  key  : ' + unicode(ky) + ' ;  val : ' + unicode( self.initialData[ky] ) )
            
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())
    

    # ***********************************************************************************************************************************************
    # ActivateAccount : load initial data for the user-account from collection user.initial
    #
    # 28.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def ActivateAccount( self ):
        try:
            self.initialData = self.Page.ViewState['INITIAL_USER_DATA']     # get data from load-on-page-not-postback
            self.CopyToFinalCollection()                                    # put it into the final collection
            # self.UpdateMapUserCache()
            self.DeleteInInitialCollection()                                # after account is approved delete it in the initital collection 

            self.LogInAndStart()                                            # go to the home-screen where user will be logged in

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # CopyToFinalCollection : store data of the user into final user-collection
    #
    # 28.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def CopyToFinalCollection( self ):
        try:
            data = {}

            # define accountr as basic-account, which means "not payed"
            accTypConf = WebConfigurationManager.AppSettings['accountRoles']     
            objSeperator = WebConfigurationManager.AppSettings['stringSeperator']     
            
            accountTypes = accTypConf.split(objSeperator)
            accType = []
            accType.Add(accountTypes[0])

            for itm in self.initialData:
                if itm != '_id' and itm != 'creationtime':
                    val = self.initialData[itm]
                    data.Add(itm, val)
                data.Add('creation_time', DateTime.UtcNow )
                data.Add('account_roles', accType )

            for itm in data:
                key = itm 
                val = data[itm]
                typDef = unicode(type(data[itm]))
                self.log.w2lgDvlp('for itm in data - key ' + unicode( key ) + ' type : ' + typDef + ' val : ' + unicode( val ) )

            ctrlDict = {'collection':'user.final' }
            ctrlDict.update({'slctKey': None})
            ctrlDict.update({'data': data})

            newId = self.insertDoc(ctrlDict)

            self.log.w2lgDvlp('ConfirmUser( .. ) CopyToFinalCollection succesfully written to collection user.final : ' + unicode( newId ) )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # DeleteInInitialCollection : delete temporary user-registration-data
    #
    # 13.12.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def DeleteInInitialCollection( self ):
        try:
            delet = {}
            delet.update({'collection':'user.initial'})
            delet.update({'slctVal':self.initialData['_id']})
            delItemId = self.delDoc(delet)

            self.log.w2lgDvlp('user_confirm->DeleteInInitialCollection : deleted item : ' + unicode(delItemId))

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # LogInAndStart : go to the home-screen. the session will be initiated here, so user will be logged in
    #
    # 28.11.2011    berndv  initial realese
    # 19.12.2012    berndv  added login via session on next webform !!
    # ***********************************************************************************************************************************************
    def LogInAndStart( self ):
        try:
            url = None

            # on the 'next' webform user_hame.aspx the user-data will be loaded if session-var 
            # 'LOGGEDIN_EMAIL' contains ther email of the user we have created
            self.Page.Session['LOGGEDIN_EMAIL'] = self.ui.getCtrl('txbx_email').Text.strip()
            url = self.Page.ResolveUrl( WebConfigurationManager.AppSettings['UserMainPage'] )                        # get link for adding new user

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())

        if url:
            self.Page.Response.Redirect( self.Page.ResolveUrl( url ) )


tool = ConfirmMapUser(Page)


# *******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
# *******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
# *******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
# *******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************



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

        if( not Page.IsPostBack ):
            # get the GUID from URL and load the user-data from database
            initialUserGuid = Page.Request.QueryString['key'] 
            tool.log.w2lgDvlp('ConfirmUser(Page)  global-parameter-key  : ' + unicode(initialUserGuid) )
            tool.LoadInitialData( initialUserGuid )
    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ***********************************************************************************************************************************************
# HndlrButtonClick    : click handler for the buttons on the page
#
# 18.03.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def HndlrButtonClick(sender, e):
        try:
            if not ValidateWebform():          # check if input is correct
                return

            tool.ui.getCtrl('lbl_explain').Text = ''

            if sender.ID == 'btn_activate':
                tool.ActivateAccount()
            elif sender.ID == 'btn_generatenewcaptcha':
                tool.GenNewCaptcha()            # ToDo : GENERATE NEW CAPTCHA 
                return

        except Exception,e:
            tool.log.w2lgError(traceback.format_exc())

        tool.LogInAndStart()        # go to the home-screen where user will be logged in


# ***********************************************************************************************************************************************
# ValidateWebform    : check user input
#
# 18.03.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def ValidateWebform():
        try:
            tool.ui.getCtrlTree( Page.Master )
            addMsg = tool.ui.getCtrl('lbl_explain').Text

            if len(tool.ui.getCtrl('txbx_password').Text) < 1:
                addMsg += tool.ui.getCtrl('lbl_missing_password').Text + '<br />'
                
            if len(tool.ui.getCtrl('txbx_captcha').Text) < 1:
                addMsg += tool.ui.getCtrl('lbl_missing_captcha').Text
                
            if tool.ui.getCtrl('chbx_accepted').Checked != True:
                addMsg += tool.ui.getCtrl('lbl_agb_not_accepted').Text + '<br />'

            # get user-data from view-state
            initData = Page.ViewState['INITIAL_USER_DATA'] 
            if initData is None:
                addMsg += tool.ui.getCtrl('lbl_no_data_found').Text + '<br />'

            # check password encrypted
            pwdFromInitial = initData['password']
            pwdFromUi = tool.EncryptSHA512Managed(tool.ui.getCtrl('txbx_password').Text)
            if pwdFromInitial.ToString().strip() != pwdFromUi.strip() :
                addMsg += tool.ui.getCtrl('lbl_wrong_password').Text + '<br />'

            # check captcha-input
            captchaFromInitial = initData['CAPTCHA']
            captchaFromUi = tool.ui.getCtrl('txbx_captcha').Text

            if captchaFromInitial.ToString().strip() != captchaFromUi.strip() :
                addMsg += tool.ui.getCtrl('lbl_wrong_captcha').Text + '<br />'

            if addMsg == tool.ui.getCtrl('lbl_explain').Text:
                return True
            else:
                tool.errorMessage(addMsg)
                return False

        except Exception,e:
            tool.log.w2lgError(traceback.format_exc())











