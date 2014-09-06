#
#
#  
#  
#  
from System.Data import *
import System.Collections
from System.Web.Configuration import *
import clr
import traceback                    # for better exception understanding

import mongoDbMgr                   # father : the acces to the database
tool = mongoDbMgr.mongoMgr(Page)


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

        if not Page.IsPostBack :
            # user must be logged in
            tool.usrDt.checkUserRigths(Page, 'free')

            # display the announces of the user
            ShowUsersOffers()

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ***********************************************************************************************************************************************
# HndlrReactionClick : handler for buttons that initiate a reaction on a given announcement
#
# 18.03.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def HndlrReactionClick(sender, e):
    try:
        url = None
        switcher = { "OpenTrial"   : "AddToTrialThread" ,
                     "CancleOffer" : "CancelOffer"      ,
                     "ReportOffer" : "MessageViolation" }
        
        idList          = Page.ViewState['ID_LIST']                 # get _mongo_id of clicked item
        commandPartList = sender.ClientID.ToString().split('_') 
        clntId          = commandPartList[-1]                       # mongo_ID of item to call
        commandStrng    = commandPartList[-2]                       # command to select webform

        dbId            = idList[ System.Convert.ToInt32(clntId) ]
        callWebForm     = switcher[commandStrng ]
        
        # tool.logMsg('user_offers.aspx -> HndlrReactionClick  : Clicked ID  ' + System.Convert.ToString( dbId ) )
        # tool.logMsg('user_offers.aspx -> HndlrReactionClick  : Command     ' + commandStrng  )
        # tool.logMsg('user_offers.aspx -> HndlrReactionClick  : CallWebForm ' + callWebForm   )

        url = WebConfigurationManager.AppSettings[callWebForm]          # search for debates
        url += '?item=' + System.Convert.ToString( dbId )

        # deletion of the offer needs the GUID of current user
        if callWebForm == 'CancelOffer':
            userGUID = tool.usrDt.getItem('GUID')
            url += '&offerer=' + userGUID

        tool.logMsg('user_debates.aspx.HndlrReactionClick : redirect to' + str( url ) )

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())

    if url:
        Response.Redirect( Page.ResolveUrl( url ) )



# ***********************************************************************************************************************************************
# ShowUsersOffers       : create a list with all offers the user made for existing job-requests (find JOB_HEADER of user )
#
# 01.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def ShowUsersOffers():
    try:
        objTypConfig    = WebConfigurationManager.AppSettings['objectTypes']
        strngSeperator  = WebConfigurationManager.AppSettings['stringSeperator']
        objectTypes     = objTypConfig.split(strngSeperator)

        objectType      = objectTypes.index('JOB_HEADER')                       # get the object_type_ID of JOB_OFFERS
        userGUID        = tool.usrDt.getItem('GUID').ToString()                 # USER GUID

        itemTable = tool.appCch.dtSt.Tables['items']                            # the data-source
        offerTable = DataTable()                                                # the data-destination
        offerTable = itemTable.Clone()

        # 1. get the 'JOB_HEADER' the user created and load the root_elements by their _parents
        slctStr = "_creatorGUID = '" + userGUID.ToString() + "' AND objectType = " + str(objectType) + " AND _creatorGUID = '"  + tool.usrDt.getItem('GUID') + "'"
        sortStr = "creationTime ASC"
        tool.logMsg('user_offers.aspx->ShowuserOffers ' + slctStr )
        rows = itemTable.Select( slctStr , sortStr )

        # 2. the _parentID field of every JOB_HEADER-item points to the root-element it is associated with
        #parentIdLst = []
        #for row in rows: 
        #    # add the GUIDs of the root-elemnts
        #    parentID = row['_parentID'].ToString()
        #    parentIdLst.Add(parentID)
        # 
        # correction bervie : 
        # 09.02.2013
        # added check if item is already in the collection
        #
        parentIdLst = []
        for row in rows: 
            # add the GUIDs of the root-elemnts
            parentID = row['_parentID'].ToString()
            if parentID not in parentIdLst:
                parentIdLst.Add(parentID)

        # 3. get the root-element-rows by the parentIDs found in the JOB_HEADERS
        idxLst = []
        for rootId in parentIdLst:            
            tool.logMsg('user_offers.aspx->ShowuserOffers - root-ID for parent : ' + rootId )
            rootRow = itemTable.Rows.Find( rootId )
            tool.logRow(rootRow)
            offerTable.ImportRow( rootRow )
            idxLst.Add( rootRow['_ID'].ToString() )

        # 3. bind repeater to data-table
        if offerTable.Rows.Count == 0:
            # no data was found
            tool.errorMessage('<br/><br/>Es wurden keine Daten gefunden !<br/><br/><br/>')
        else:
            # bind repeater to result data-table
            repeater = tool.gtCtl('repUserOfferList')
            repeater.DataSource = offerTable
            repeater.DataBind()

            Page.ViewState['ID_LIST'] = idxLst

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())

