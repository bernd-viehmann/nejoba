#  
#  
#
#  
from System.Web.Configuration import *
from System import UriPartial
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
        # hide the main-user-interface after a button-click and show  a please-wait sedativ
        tool.ui.getCtrlTree( Page.Master )
        tool.ui.hideFormAfterClick()

        # get the url-parameter that decides what webform should be used for redirect if a job-type was clicked
        nxtWbFrmSwtch = Page.Request.QueryString['next']

        if nxtWbFrmSwtch == 'offer' :
            page.ViewState['NEXT_FORM'] = 'OfferJob'
            tool.ui.getCtrl('offerJobDiv').Visible = True
            tool.ui.getCtrl('searchJobDiv').Visible = False
        else:
            page.ViewState['NEXT_FORM'] = 'SearchJob'
            tool.ui.getCtrl('offerJobDiv').Visible = False
            tool.ui.getCtrl('searchJobDiv').Visible = True

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return


# ***********************************************************************************************************************************************
# HndlrLinkClick : handler for button-click-events. chose button by ID
#
# 18.11.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def HndlrLinkClick(sender, e):
    try:
        urlNext = None
        parameter = sender.ID.split('_')[1]

        tool.log.w2lgDvlp('IntroWork.aspx.py->HndlrLinkClick parameter from pressed link-button : ' + parameter )

        url = WebConfigurationManager.AppSettings[ page.ViewState['NEXT_FORM'] ]
        urlNext = Page.ResolveUrl(url) + '?class=' + parameter
        tool.log.w2lgDvlp('IntroWork.aspx.py jump-url in click-handler : ' + urlNext)

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return

    if urlNext != None :
        Response.Redirect(urlNext)
