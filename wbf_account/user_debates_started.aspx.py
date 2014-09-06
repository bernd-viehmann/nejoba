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
        userGUID        = tool.usrDt.getItem('GUID').ToString()                 # USER GUID

        itemTable   = tool.appCch.dtSt.Tables['items'] 
        offerTable  = DataTable()                                                # the data-destination
        offerTable  = itemTable.Clone()

        # 1. get the 'JOB_HEADER' the user created and load the root_elements by their _parents
        slctStr = "_creatorGUID = '" + userGUID + "' AND objectType = 1"
        sortStr = "creationTime ASC"
        rows = itemTable.Select( slctStr , sortStr )

        dbtRootIdLst = []                                                                       # the _parnentID in the header points to the ID of the root_element which we are looking for
        for row in rows: 
            dbtRootIdLst.Add( row['_ID'].ToString() )
            offerTable.ImportRow( row )

        # 2. bind repeater to data-table
        repeater = tool.gtCtl('repUsrOwnDbtsLst')
        repeater.DataSource = offerTable
        repeater.DataBind()

        Page.ViewState['ID_LIST'] = dbtRootIdLst

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())



# ***********************************************************************************************************************************************
# HndlrReactionClick : handler for buttons that initiate a reaction on a given announcement
#
# 18.03.2012  - bervie -     initial realese
# 23.09.2013  - bervie -     added delete function
# ***********************************************************************************************************************************************
def HndlrReactionClick(sender, e):
    try:
        url = None

        commandPartList = sender.ClientID.ToString().split('_') 
        aboId           = commandPartList[-1]                       # index-id of item to call
        commandStrng    = commandPartList[-2]                       # command to select webform
        idList          = Page.ViewState['ID_LIST']
        aboMogoId       = idList[ System.Convert.ToInt32(aboId) ]   # id of the offeror

        if commandStrng == "CallDebate" :
            url = WebConfigurationManager.AppSettings["AddArticleToDebate"]   + '?item=' + aboMogoId
            tool.logMsg('user_debates.aspx.HndlrReactionClick : redirect to' + unicode( url ) )

        if commandStrng == 'DelDebate':
            url = WebConfigurationManager.AppSettings["CancelOffer"]   + '?item=' + aboMogoId
            tool.logMsg('user_debates.aspx.HndlrReactionClick : redirect to' + unicode( url ) )

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())

    if url:
        Response.Redirect( Page.ResolveUrl( url ) )



