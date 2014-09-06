# login.aspx.py  : webform to log-ion. is called if user was unable to login in the headline 
#
#
#  
from System.Web.Configuration import *
import traceback                                # for better exception understanding
import random
import mongoDbMgr                               # father : the acces to the database
from srvcs.tls_WbFrmClasses import LogIn        # helper class for this dialog

tool = LogIn(Page)

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

        if( Page.IsPostBack ):
            tool.CheckLogIn()
        else:
            pass
            # tool.usrDt.measurePeformance('pageLoad of webform login.aspx with NO_POSTBACK')

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ***********************************************************************************************************************************************
# HndlrButtonClick : handler for buttons
#
# 18.03.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def HndlrButtonClick(sender, e):
    try:
        url = None

        if sender.ID == 'btn_login':
            tool.CheckLogIn()
        elif sender.ID == 'btn_create':
            url = Page.ResolveUrl( WebConfigurationManager.AppSettings['CreateMapAccount'] )                        # get link for adding new user

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return

    if url != None :
        Response.Redirect( url )








