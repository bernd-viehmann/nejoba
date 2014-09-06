#
# Default.aspx  main entry page of the application : define a location and redirect to a projector-webform
#
#
from System.Web.Configuration import *
from System import UriPartial
import System
import traceback                                    # for better exception understanding
import mongoDbMgr                                   # father : the acces to the database
import math
from srvcs.tls_UiHelper import LocDefiner
tool = mongoDbMgr.mongoMgr( Page )
tool.ui.getCtrlTree( Page.Master )
lcDfnr = LocDefiner( Page )            # the helper class for location-stuff

# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 18.03.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    try:
        tool.errorMessage('')
        tool.ui.hideFormAfterClick()

        if not Page.IsPostBack : 
            lcDfnr.uiInitLocIntfc()

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return


# ***********************************************************************************************************************************************
# HndlrButtonClick    : handler for button-click-events. chose button by ID
#
# 14.10.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def HandlBtnClick(sender, e):
    try:
        url = None

        buttonId = sender.ID

        fndLoc = defineLocation()                         # set the location-info 
        if fndLoc is False : 
            tool.errorMessage(' <br />Es wurde keine Stadt oder Postleitzahl gefunden! <br />Hast Du ein Land ausgew&auml;hlt? Bitte Eingaben kontrollieren. <br />')
            return                 #stop computation if no location was found

        # go to the list with all infos on 'openList'
        elif 'hyLnk_openMap' in buttonId:
            # the system will guide you to the list
            url = WebConfigurationManager.AppSettings["debateMap"]
            url = url + '?' + lcDfnr.getLoctnPrmtr() 

        # go to the list with all infos on 'openList'
        elif 'hyLnk_openBlgLst' in buttonId:
            # the system will guide you to the list
            url = WebConfigurationManager.AppSettings["debateProjector"]
            url = url + '?' + lcDfnr.getLoctnPrmtr() 

        # go to the list with all infos on 'openList'
        elif 'hyLnk_openBlog' in buttonId:
            # the system will guide you to the list
            url = WebConfigurationManager.AppSettings["MicroBlog"]
            url = url + '?' + lcDfnr.getLoctnPrmtr() 

        # go to the functions with all infos on 'openList'
        elif 'hyLnk_openJobs' in buttonId:
            # the system will guide you to the list
            url = WebConfigurationManager.AppSettings["JobMarket"]

        # go to the list with all infos on 'openList'
        elif 'hyLnk_listOfJobs' in buttonId:
            # the system will guide you to the list
            url = WebConfigurationManager.AppSettings["SearchJob"]

        tool.log.w2lgDbg( 'Default.aspx->HandlBtnClick URL: ' + url)

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())

    if url != None:
        Response.Redirect( Page.ResolveUrl( url ) )


# ***********************************************************************************************************************************************
# defineLocation : the function gets the locations for the input. the global location-definer class will be initialized
#
#   param   : None
#   returns : False
#             the loc-definer has not found anything !!
#             True
#             jawohl herr kaleu
#
# 15.11.2013  bervie  initial realease
# ***********************************************************************************************************************************************
def defineLocation():
    try:
        countryCode     = tool.ui.getCtrl('sel_country').SelectedValue 
        cityIdentifier  = tool.ui.getCtrl('txbx_city').Text
        lcDfnr.setLocByInpt( countryCode , cityIdentifier ) 

        if lcDfnr.getValidLoctn() is None:
            return False

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


