#  
# user_announces shows the anfragen from the logged in user
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

        if( not Page.IsPostBack ):
            # user must be logged in
            tool.usrDt.checkUserRigths(Page, 'free')

            # display the announces of the user
            ShowUsersJobs()

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())



# ***********************************************************************************************************************************************
# GetList       : create a list of all annonces the user made and send them to the repeater
#
# 01.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def ShowUsersJobs():
    try:
        objTypConfig    = WebConfigurationManager.AppSettings['objectTypes']
        strngSeperator  = WebConfigurationManager.AppSettings['stringSeperator']
        objectTypes     = objTypConfig.split(strngSeperator)

        objectType      = objectTypes.index('JOB_ROOT')                     # get the object_type_ID of JOB_OFFERS
        userGUID        = tool.usrDt.getItem('GUID').ToString()             # USER GUID

        itemTable = tool.appCch.dtSt.Tables['items']                        # the data-source
        offerTable = DataTable()                                            # the data-destination
        offerTable = itemTable.Clone()

        #slctStr = "_creatorGUID = '" + userGUID.ToString() + "' AND objectType = " + str(objectType)
        #sortStr = "creationTime DESC"
        #rows = itemTable.Select( slctStr , sortStr )

        rows = tool.appCch.dtVwCreator.FindRows(userGUID)

        idxLst = []
        for row in rows: 
            if row['objectType'] == objectType:
                offerTable.ImportRow( row.Row )
                idxLst.Add( row['_ID'].ToString())

        offerTable.DefaultView.Sort = "creationTime ASC"

        # 3. bind repeater to data-table
        if offerTable.Rows.Count == 0:
            # no data was found
            tool.errorMessage('<br/><br/>Es wurden keine Daten gefunden !<br/><br/><br/>')
        else:
            # bind repeater to result data-table
            repeater = tool.gtCtl('repUserJobsList')
            repeater.DataSource = offerTable
            repeater.DataBind()

            Page.ViewState['ID_LIST'] = idxLst

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
        switcher = { "DeleteComplete"  : "CancelOffer"   ,
                     "ViewTrialList"   : "ListJobTrials" }
        
        idList          = Page.ViewState['ID_LIST']                 # get _mongo_id of clicked item
        commandPartList = sender.ClientID.ToString().split('_') 
        clntId          = commandPartList[-1]                       # mongo_ID of item to call
        commandStrng    = commandPartList[-2]                       # command to select webform

        dbId            = idList[ System.Convert.ToInt32(clntId) ]
        callWebForm     = switcher[commandStrng ]
        
        # tool.logMsg('user_offers.aspx -> HndlrReactionClick  : Clicked ID  ' + System.Convert.ToString( dbId ) )
        # tool.logMsg('user_offers.aspx -> HndlrReactionClick  : Command     ' + commandStrng  )
        # tool.logMsg('user_offers.aspx -> HndlrReactionClick  : CallWebForm ' + callWebForm   )

        url = WebConfigurationManager.AppSettings[callWebForm]                  # search for debates
        url += '?item=' + System.Convert.ToString( dbId )

        tool.logMsg('user_debates.aspx.HndlrReactionClick : redirect to' + str( url ) )

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())

    if url:
        Response.Redirect( Page.ResolveUrl( url ) )



