#  
# editor.aspx.py 
#  
# the webform is used for creating new job offers for the community. user can define the location, the typ of the job and the time of action
#  
#
#  03.10.2012   bevie    initial realese
#  
 
import System.DateTime
import System.Drawing.Color
import System.Guid
from System.Web.Configuration import *
from System import UriPartial

import traceback                    # for better exception understanding
import re                           # for finding the taggs

from srvcs.Item import Item
tool = Item( Page )

# ------------------------------------------------------------------------------------------------------------------------------------------------##__aspn.net ------------------------------------------------
# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 28.03.2012  - bervie -     initial realese
# 08.02.2013  - bervie -     changed webform to new item-form
#
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    try:
        # hide the main-user-interface after a button-click and show  a please-wait sedativ
        tool.ui.hideFormAfterClick()

        if( not Page.IsPostBack ):
            Page.ViewState['MongoID']       = Page.Request.QueryString['item'] 
            Page.ViewState['creatorGUID']   = Page.Request.QueryString['offerer'] 

            tool.log.w2lgDvlp('user_offer_cancle.aspx->PageLoad : webform called for item.base-ID : ' + Page.ViewState['MongoID'] )
            tool.ui.getCtrlTree( Page.Master )
            canvas = tool.ui.getCtrl('divShowMain')

            row = tool.itemTbl.Rows.Find( Page.ViewState['MongoID'] )
            itm = tool.load( row )
            canvas.InnerHtml = tool.data['html']

            #Page.ViewState['ObjType'] = itm['objectType']
            #tool.log.w2lgDvlp('show_details->PageLoad : type of item loaded : ' + str(itm['objectType']) )

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ------------------------------------------------------------------------------------------------------------------------------------------------##__handler ------------------------------------------------
# ***********************************************************************************************************************************************
# HndlrButtonClick    : handler for button-click-events. chose button by ID
#
# 18.11.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def HndlrButtonClick(sender, e):
    try:
        tool.logMsg('user_offer_cancle.aspx->HndlrButtonClick : ID clicked control  = ' + unicode(sender.ID) )

        if sender.ID == 'btnCancelOffer':
            mongoId         = Page.ViewState['MongoID']
            creatorGuid     = Page.ViewState['creatorGUID']

            headerTypeName = None
            if creatorGuid is not None:
                headerTypeName = 'JOB_HEADER'

            row = tool.itemTbl.Rows.Find( mongoId )

            tool.delete( row, headerTypeName, creatorGuid )

            # display succesfull-cpmpleted-message
            tool.ui.getCtrlTree( Page.Master )
            tool.ui.getCtrl('buttonDiv').Visible = False
            tool.ui.getCtrl('messageDiv').Visible = True

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return


