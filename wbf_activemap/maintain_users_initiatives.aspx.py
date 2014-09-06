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
import traceback                                    # for better exception understanding
import mongoDbMgr                                   # father : the acces to the database
import System.Text
from System.Net.Mail import *
from System.Net import NetworkCredential 


tool = mongoDbMgr.mongoMgr( Page )


# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 18.03.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    try:
        # tool.ui.getCtrlTree( Page.Master )
        # tool.ui.hideFormAfterClick()

        pass

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return



# ***********************************************************************************************************************************************
# HndlrButtonClick    : handler for button-click-events. chose button by ID
#
# 18.11.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def HndlrButtonClick(sender, e):
    try:
        url = None

        if sender.ID == 'btnSendReport':
            # tool.log.w2lgDvlp('der schickma buttton wurde gerade gedr?ckt')
            sendToNejobaTeam()

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return

    if url != None :
        Response.Redirect(urlNext)




