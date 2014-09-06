#  
# user_home.aspx.py  : webform is the home-plkace of the user.
#                      from here he can start exploring his nejoba expirience
#  
#  
#  
#  
#  
#
#  
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
        if( not Page.IsPostBack ):
            # end the user-session by deleting the data in the cache
            tool.usrDt.LoggOut()

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


