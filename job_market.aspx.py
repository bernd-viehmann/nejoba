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
        #tool.log.w2lgDvlp('Default.aspx.py->HndlrButtonClick ID of pressed button : ' + sender.ID)

        if sender.ID == 'hyLnk_go' :
            fctnDef = tool.ui.getCtrl("txbx_functn_type").Text.strip()

            if fctnDef == 'offer_job':
                urlNext = WebConfigurationManager.AppSettings[ "OfferJob" ]
            else:
                jobName = '*'
                urlNext = WebConfigurationManager.AppSettings['SearchJob'] + '?jobtype='
                urlNext += Page.Server.UrlEncode( jobName )

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return

    if urlNext != None :
        #tool.usrDt.measurePeformance('HndlrButtonClick of webform Default.aspx before redirection')
        Response.Redirect( Page.ResolveUrl( urlNext ) )







# ***********************************************************************************************************************************************
# HndlrHyLnkClick   : handler is called when a job_type link was clicked
#
# 14.12.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def HndlrHyLnkClick(sender, e):
    try:
        urlNext = None

        # check if job should be offered or searched:
        fctnDef = tool.ui.getCtrl("txbx_functn_type").Text.strip()

        if fctnDef == '':
            return
        if fctnDef == 'offer_job':
            urlNext = WebConfigurationManager.AppSettings[ "OfferJob" ]

        elif fctnDef == 'search_job':
            # get the current job_type_tag from the link_id
            jobTypeTag = sender.ID.split('_')[-1].ToString().upper()
            jobTaggs =  WebConfigurationManager.AppSettings['jobTypeValue'].split(';')[1:]

            jobName = '*'
            for tag in jobTaggs:
                if jobTypeTag in tag:
                    idx = jobTaggs.index(tag) + 1
                    jobName = WebConfigurationManager.AppSettings['jobType_DE'].split(';')[idx]

            tool.log.w2lgDvlp('job_search.aspx.py->HandlLnkBtn : job_type selected :  ' +  jobName )

            urlNext = WebConfigurationManager.AppSettings['SearchJob'] + '?jobtype='
            urlNext += Page.Server.UrlEncode( jobName )

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return

    if urlNext != None :
        tool.usrDt.measurePeformance('HndlrButtonClick of webform Default.aspx before redirection')
        Response.Redirect( Page.ResolveUrl( urlNext ) )



