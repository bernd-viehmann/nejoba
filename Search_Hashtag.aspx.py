#
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
import System
import traceback                                    # for better exception understanding
import mongoDbMgr                                   # father : the acces to the database
from srvcs.tls_UiHelper import LocDefiner

tool = mongoDbMgr.mongoMgr( Page )
lcDfnr = LocDefiner( Page )            # the helper class for location-stuff

# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 18.03.2012  - bervie -     initial realese
# 14.20.2013  - bervie -     added the session-cached input for cntry/city/postcode
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    try:
        tool.errorMessage('')
        tool.ui.getCtrlTree( Page.Master )
        tool.ui.hideFormAfterClick()

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return


# ***********************************************************************************************************************************************
# Page_PreRender    : initializer after button_click
#
# 18.11.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_PreRender(sender, e):
    try:
        # insert curretn location from the session-cache
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

        # button for changing session-stored location was pressed 
        if sender.ID == 'btn_select_slct_loctn':
            countryCode     = tool.ui.getCtrl('sel_country').SelectedValue 
            cityIdentifier  = tool.ui.getCtrl('txbx_city').Text
            lcDfnr.setLocByInpt( countryCode , cityIdentifier ) 

            if lcDfnr.getValidLoctn() is None:
                tool.errorMessage(' <br />Es wurde keine Stadt oder Postleitzahl gefunden! <br />Hast du das richtige Land ausgew&auml;hlt?<br />')
                return

        # go to data-projector 
        elif 'btn_show_loctn_map' in sender.ID : url = WebConfigurationManager.AppSettings["debateMap"]                     # go to the map on 'openMap'
        elif 'btn_show_loctn_list' in sender.ID : url = WebConfigurationManager.AppSettings["debateProjector"]              # go to the list with all infos on 'openList'
        
        # buil URL-parameter for data-filtering
        param = '?' + lcDfnr.getLoctnPrmtr() 
        param += '&Tags=' 
        param +=  ','                                                                                                       # this is magic I KNOW. will be fixed somewhere, sometimes
        param += tool.ui.getCtrl('txbx_hashtag').Text 
        # param = Page.Server.UrlEncode( param )

        url += param
        tool.log.w2lgDvlp('search_hashtag_handle_button . Url Param : ' + param)

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())

    if url != None:
        Response.Redirect( Page.ResolveUrl( url ) )


