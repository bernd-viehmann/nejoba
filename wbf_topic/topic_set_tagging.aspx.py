#  debate_list.aspx.py
#
#  show a filterable list of discussions for a location
#  
#  
#  14.01.2013  initial realese
#
#  
import System.Data
import System.Collections
import System.Web.UI.WebControls
import clr
import traceback                    # for better exception understanding
import mongoDbMgr                   # father : the acces to the database
from System import UriPartial
from srvcs.ctrl_ItemClasses import *

from srvcs.tls_WbFrmClasses import SetTagging      # helper class for all payment-webforms
tool = SetTagging(Page)


# tool = mongoDbMgr.mongoMgr(Page)

# ### handler ############################################################################################################################################################################################################################################################

# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 07.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    try:
        tool.PgLoad(Page)

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ***********************************************************************************************************************************************
# HandlBtnClick   : handler for button-clix
#
# 07.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def HandlBtnClick( sender,e ):
    try:
        tool.HandlBtnClick(Page,sender,e)

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())



