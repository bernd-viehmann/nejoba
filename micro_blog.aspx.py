#
#
#
#
#
#
#
from System.Web.Configuration import *
from System import UriPartial
import System
import traceback                                    # for better exception understanding
import mongoDbMgr                                   # father : the acces to the database


tool = mongoDbMgr.mongoMgr( Page )

# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 18.03.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    try:
        tool.ui.getCtrlTree( Page.Master )
        tool.ui.hideFormAfterClick()

        # try to add actual content to avoid teh firefox back-button problem
        # tool.ui.getCtrl('timeIsNow').Text = System.DateTime.Now.ToString()

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
        urlNext = None
        tool.log.w2lgDvlp('Default.aspx.py->HndlrButtonClick ID of pressed button : ' + sender.ID)

        switcher = {}
        switcher.update( {"btn_offerJob"   : "OfferJob"  } )
        switcher.update( {"btn_searchJob"  : "SearchJob"  } )
        

        if sender.ID not in switcher.keys():
            return

        url = WebConfigurationManager.AppSettings[ switcher[sender.ID].ToString() ]
        urlNext = Page.ResolveUrl(url)

        if sender.ID == "btn_offerJob"  : urlNext += '?next=offer'
        if sender.ID == "btn_searchJob" : urlNext += '?next=search'

        tool.log.w2lgDvlp('Default.aspx.py jump-url in click-handler : ' + urlNext)

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return

    if urlNext != None :
        tool.usrDt.measurePeformance('HndlrButtonClick of webform Default.aspx before redirection')
        Response.Redirect( Page.ResolveUrl( urlNext ) )


