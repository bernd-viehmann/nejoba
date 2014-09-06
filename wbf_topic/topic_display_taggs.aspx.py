#  topic_display_taggs.aspx.py
#
#  function shows a list with all available locations of a given location
#  
#  
#  14.01.2013  initial realese
#
#  
import System.Data
import System.Text
import System.Collections
import clr
import traceback                    # for better exception understanding
import mongoDbMgr                   # father : the acces to the database
from System import UriPartial

from srvcs.tls_WbFrmClasses import DisplayTags
tool = DisplayTags(Page)


# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 07.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    try:
        tool.PageLoad(sender, e)
    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())



# ***********************************************************************************************************************************************
# HandlBtnClick   : handler for button-clix
#
# 07.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def HandlBtnClick( sender, e ):
    try:
        tool.HandlBtnClick(sender, e)
    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


