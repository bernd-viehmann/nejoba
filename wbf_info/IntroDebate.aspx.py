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


# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 18.03.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    try:
        # hide the main-user-interface after a button-click and show  a please-wait sedativ
        #tool.ui.getCtrlTree( Page.Master )
        #tool.ui.hideFormAfterClick()
        pass
    except Exception,e:
        #tool.log.w2lgError(traceback.format_exc())
        pass
        return

