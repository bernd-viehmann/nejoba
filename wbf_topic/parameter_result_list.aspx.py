#  debate_list.aspx.py
#
#  show a filterable list of discussions for a location
#  
#  
#  14.01.2013  initial realese
#
#  
from System.Web.Configuration import *

import System.Data
import System.Collections
import clr
import traceback                    # for better exception understanding
import mongoDbMgr                   # father : the acces to the database
from System import UriPartial

from srvcs.tls_WbFrmClasses import ParamResultList
tool = ParamResultList(Page)

# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 07.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    try:
        tool.PageLoad(sender, e)

        #return

        ## hide the main-user-interface after a button-click and show  a please-wait sedativ
        #tool.ui.getCtrlTree( Page.Master )
        #tool.ui.hideFormAfterClick()

        #if not Page.IsPostBack:
        #    # 1. get the data of the location given as URL-parameter and put data into the dropdown
        #    #    syntax of locationparameter must be : DE|41836
        #    locParam  = Page.Request.QueryString['loc']
        #    if locParam:
        #        locations = tool.defineLocation( locParam )
        #        Page.ViewState['LOCATION_LIST'] = locations 

        #    # 2. get the taggs that should be used for search. if we have a couple of taggs they have 
        #    #    to be seperated by comma : karneval,rosenmotag,veranstaltung or #karneval,#rosenmotag,#veranstaltung 
        #    taggParam = Page.Request.QueryString['tags']
        #    if taggParam:
        #        taggings = tool.defineTagsFromParam( taggParam )
        #        tool.ui.getCtrl('txb_hashtags').Text = ','.join(taggings)
        #        Page.ViewState['TAG_LIST'] = taggings

        #    # 3. get the key and name of a rubric to find all items that are labeled with this key-code: nejoba will also 
        #    #    load all data from- sub-rubrics that belong to the given one by checking the substring matches
        #    rubric = Page.Request.QueryString['key']
        #    if rubric:
        #        Page.ViewState['RUBRIC'] = rubric
        #    name = Page.Request.QueryString['name']
        #    if name:
        #        Page.ViewState['RUBRIC_NAME'] = name
        #        tool.ui.getCtrl('txb_rubricName').Text = name

        ## load list of debates into repeater
        #tool.LoadDebateList()

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ***********************************************************************************************************************************************
# HandlBtnClick   : handler for button-clix
#
# 07.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def HandlBtnClick( sender, e ):
    url = None
    try:
        tool.ButtonHandler( sender, e )

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())

    if url != None:
        Response.Redirect(Page.ResolveUrl(url))

