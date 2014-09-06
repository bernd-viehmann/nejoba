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
import traceback                                    # for better exception understanding
import mongoDbMgr                                   # father : the acces to the database


from System.Web.Configuration import *
import traceback                                # for better exception understanding
import random
import mongoDbMgr                               # father : the acces to the database

tool = mongoDbMgr.mongoMgr(Page)

# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#                    this is the webform that loads the user-data after log-in or initial user-creation. it is the main-entry of the
#                    application. 
#
# 10.12.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    try:
        # user must be logged in
        tool.usrDt.checkUserRigths( Page, 'free')

        # hide the main-user-interface after a button-click and show  a please-wait sedativ
        tool.ui.getCtrlTree( Page.Master )
        tool.ui.hideFormAfterClick()




    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ***********************************************************************************************************************************************
# HndlrButtonClick    : handler for button-click-events. chose button by ID
#
# 18.11.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def HndlrButtonClick(sender, e):
    try:
        pass
    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return

