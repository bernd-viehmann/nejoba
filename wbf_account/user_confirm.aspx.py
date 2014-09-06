#  
# webform user_confirm 
#
# with ConfirmUser Helper-class
#  
#  
#  
#  
#  
#
#  
from System.Web.Configuration import *
from System import UriPartial
from System import DateTime
import traceback                                # for better exception understanding
import random
import mongoDbMgr                               # father : the acces to the database

from srvcs.tls_WbFrmClasses import ConfirmUser  # helper class for this dialog
tool = ConfirmUser(Page)


# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 18.03.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    try:
        # hide the main-user-interface after a button-click and show  a please-wait sedativ
        tool.ui.getCtrlTree( Page.Master )
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
            addMsg = tool.ui.getCtrl('lbl_explain').Text

            if len(tool.ui.getCtrl('txbx_password').Text) < 1:
                addMsg += tool.ui.getCtrl('lbl_missing_password').Text
                tool.ui.getCtrl('lbl_explain').Text = addMsg
                return False
                
            if len(tool.ui.getCtrl('txbx_captcha').Text) < 1:
                addMsg += tool.ui.getCtrl('lbl_missing_captcha').Text
                tool.ui.getCtrl('lbl_explain').Text = addMsg
                return False
                
            if tool.ui.getCtrl('chbx_accepted').Checked != True:
                addMsg += tool.ui.getCtrl('lbl_agb_not_accepted').Text
                tool.ui.getCtrl('lbl_explain').Text = addMsg
                return False

            # get user-data from view-state
            initData = Page.ViewState['INITIAL_USER_DATA'] 
            if initData is None:
                addMsg += tool.ui.getCtrl('lbl_no_data_found').Text
                tool.ui.getCtrl('lbl_explain').Text = addMsg
                return False

            # check password encrypted
            pwdFromInitial = initData['password']
            pwdFromUi = tool.EncryptSHA512Managed(tool.ui.getCtrl('txbx_password').Text)
            if pwdFromInitial.ToString().strip() != pwdFromUi.strip() :
                addMsg += tool.ui.getCtrl('lbl_wrong_password').Text
                tool.ui.getCtrl('lbl_explain').Text = addMsg
                return False

            # check captcha-input
            captchaFromInitial = initData['CAPTCHA']
            captchaFromUi = tool.ui.getCtrl('txbx_captcha').Text
            if captchaFromInitial.ToString().strip() != captchaFromUi.strip() :
                addMsg += tool.ui.getCtrl('lbl_wrong_captcha').Text
                tool.ui.getCtrl('lbl_explain').Text = addMsg
                return False

            return True    

        except Exception,e:
            tool.log.w2lgError(traceback.format_exc())









