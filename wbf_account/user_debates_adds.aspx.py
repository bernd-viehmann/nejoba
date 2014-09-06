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
            ShowUserDebates()

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())



# ***********************************************************************************************************************************************
# GetList       : create a list of all annonces the user made and send them to the repeater
#
# 01.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def ShowUserDebates():
    try:
        objTypConfig    = WebConfigurationManager.AppSettings['objectTypes']
        strngSeperator  = WebConfigurationManager.AppSettings['stringSeperator']
        objectTypes     = objTypConfig.split(strngSeperator)

        objectType      = objectTypes.index('DEBATE_MSG')                       # get the object_type_ID of JOB_OFFERS
        userGUID        = tool.usrDt.getItem('GUID').ToString()                 # USER GUID

        itemTable = tool.appCch.dtSt.Tables['items']                            # the data-source
        offerTable = DataTable()                                                # the data-destination
        offerTable = itemTable.Clone()

        # 1. get the 'JOB_HEADER' the user created and load the root_elements by their _parents
        slctStr = "_creatorGUID = '" + userGUID.ToString() + "' AND objectType = 11"
        sortStr = "creationTime ASC"
        rows = itemTable.Select( slctStr , sortStr )

        tool.logMsg( 'user_debates_adds->ShowUserDebates() number of rows found : ' + str(len(rows)) )

        dbtRootIdLst = []                                                                       # the _parnentID in the header points to the ID of the root_element which we are looking for
        for row in rows: 
            # how to get the root-element this MESSAGE belongs to:
            #    DEBATE.MSG._rootElemGUID  ->   DEBATE.HEADER._rootElemGUID
            # DEBATE.HEADER._parentID      ->     DEBATE_ROOT._id
            #
            # The DEBATE_ROOT._id should only appear once in the list. check if NOT present before insert

            objectType = objectTypes.index('DEBATE_HEADER')
            guid =  row['_rootElemGUID'].ToString()
            slctStr = "_rootElemGUID  = '" + guid + "' AND objectType = " + str(objectType)
            tool.logMsg('select 1 ' +  slctStr)
            headers = itemTable.Select( slctStr , sortStr )

            objectType = objectTypes.index('DEBATE_ROOT')
            parent =  headers[0]['_parentID'].ToString()
            slctStr = "_ID = '" + parent + "' AND objectType = " + str(objectType)
            tool.logMsg('select 2 ' +  slctStr)
            rootElem = itemTable.Select( slctStr , sortStr )
            tool.logMsg(str(len(rootElem)))

            # if no element was found continue with the next element
            # 28.11.2013 bervie
            if len(rootElem) == 0:
                tool.log.w2lgError('user_debates_adds->ShowUserDebates : rootElem not found for select : ' + slctStr )
                continue

            debateRootId = rootElem[0]['_id'].ToString()
            tool.logMsg('Found root_elem for debate ' +  debateRootId )

            if not dbtRootIdLst.Contains(debateRootId):
                tool.logMsg('Found root_elem for debate ' +  debateRootId )
                dbtRootIdLst.Add(debateRootId)
                rootRow = itemTable.Rows.Find( debateRootId )

                offerTable.ImportRow( rootRow )

        # 2. bind repeater to data-table
        if offerTable.Rows.Count == 0:
            # no data was found
            tool.errorMessage('<br/><br/>Es wurden keine Daten gefunden !<br/><br/><br/>')
        else:
            # bind repeater to result data-table
            repeater = tool.gtCtl('repUsrDbtsLst')
            repeater.DataSource = offerTable
            repeater.DataBind()
            Page.ViewState['ID_LIST'] = dbtRootIdLst

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

        # get _mongo_id of clicked item
        idList = Page.ViewState['ID_LIST']
        clntId = sender.ClientID.ToString().split('_')[-1]
        dbId = idList[ System.Convert.ToInt32(clntId) ]
        # tool.logMsg('HndlrReactionClick : Clicked ID ' + str( dbId ) )

        url = WebConfigurationManager.AppSettings['AddArticleToDebate']   # search for debates
        url += '?item=' + System.Convert.ToString( dbId )
        tool.logMsg('user_debates.aspx.HndlrReactionClick : redirect to' + str( url ) )

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())

    if url:
        Response.Redirect( Page.ResolveUrl( url ) )
