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
from System.Data import *
import traceback                    # for better exception understanding
import re                           # for finding the taggs

from srvcs.Item import Item
tool = Item( Page )

# ------------------------------------------------------------------------------------------------------------------------------------------------##__aspn.net ------------------------------------------------
# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 28.03.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    try:
        # hide the main-user-interface after a button-click and show  a please-wait sedativ
        tool.ui.getCtrlTree( Page.Master )
        tool.ui.hideFormAfterClick()

        if( not Page.IsPostBack ):
            itemId = Page.Request.QueryString['item'] 
            Page.ViewState['itemId'] = itemId     # used to call external sides from this editor

            rootRow = tool.appCch.dtSt.Tables['items'].Rows.Find( itemId )

            tool.logMsg('job_trial_list.aspx.page_Load : item-parameter is ' + rootRow['_ID'].ToString() )

            # show detail-data of the root-elem JOB_ROOT
            canvas = tool.ui.findCtrl( Page, 'divShowMain')
            itm = tool.load( rootRow )
            htmlToPrint = tool.data['html']
            canvas.InnerHtml = htmlToPrint

        # get the list with offerors
        loadOfferorList()

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ------------------------------------------------------------------------------------------------------------------------------------------------##__init ------------------------------------------------
# ***********************************************************************************************************************************************
# loadOfferorList : load all offerors for the current job !!
#
# 30.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def loadOfferorList():
    try:
        # 1. get the items of type 'JOB_HEADER' for the given JOB_ROOT
        #    parentID of the Header is the ID of the job_root
        offerorTbl = System.Data.DataTable("offerors")
        createTable( offerorTbl )

        # 2. bind repeater to data-table or send error-message
        if offerorTbl.Rows.Count == 0:
            # no data was found
            msgTxt  = tool.gtCtl('msg_no_offers_available').Text
            tool.errorMessage( msgTxt )
        else:
            # bind repeater to result data-table
                repeater = tool.gtCtl('repJobTrials')
                repeater.DataSource = offerorTbl
                repeater.DataBind()

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ***********************************************************************************************************************************************
# loadOfferorList : load all offerors for the current job !!
#
# param : offertable
#
# 30.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def createTable( offerorTbl ):
    try:
        # 1. create a data-table for the offerors that are offering :-)
        col = offerorTbl.Columns.Add("_ID",          System.String )
        col = offerorTbl.Columns.Add("nickname",     System.String )
        col = offerorTbl.Columns.Add("postcode",     System.String )
        # col = offerorTbl.Columns.Add("city",         System.String )
        col = offerorTbl.Columns.Add("_creatorGUID", System.String )
        
        # 2. get the list of headers 
        objTypConfig    = WebConfigurationManager.AppSettings['objectTypes']
        strngSeperator  = WebConfigurationManager.AppSettings['stringSeperator']
        objectTypes     = objTypConfig.split(strngSeperator)
        objectType      = objectTypes.index('JOB_HEADER')                       # get the object_type_ID of JOB_OFFERS
        parentId        = Page.ViewState['itemId']

        itemTbl = tool.appCch.dtSt.Tables['items']                           # the data-source
        slctStr = "_parentID = '" + parentId + "' AND objectType = " + str(objectType)
        sortStr = "creationTime ASC"
        rows = itemTbl.Select( slctStr , sortStr )
        creatorLst = []                                                            # the _parnentID in the header points to the ID of the root_element which we are looking for
        for row in rows: 
            creatorGuid = row['_creatorGUID'].ToString()
            creatorLst.Add( creatorGuid )

        # 3. get the offeror-date from the database
        idxLst = []
        for item in creatorLst:
            # try to read a document #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  
            accesor = {}
            accesor.update({'collection':'user.final'})
            accesor.update({'slctKey' : 'GUID'})
            accesor.update({'slctVal' : item})
            loaded = tool.readDoc(accesor)

            mongoId         = accesor['data']['_id'].ToString() 
            nickname        = accesor['data']['nickname'].ToString() 
            postcode        = accesor['data']['postcode'].ToString() 
            # city            = accesor['data']['city'].ToString() 
            creatorGuid     = item

            row = offerorTbl.NewRow()
            row['_ID']          = mongoId
            row['nickname']     = nickname
            row['postcode']     = postcode
            # row['city']         = city
            row['_creatorGUID'] = creatorGuid
            idxLst.Add( creatorGuid )
            offerorTbl.Rows.Add(row)

            #tool.logMsg('job_trial_list.aspx.loadOfferorList() : Found _id      : ' + mongoId    )
            #tool.logMsg('job_trial_list.aspx.loadOfferorList() : Found nickname : ' + nickname   )
            #tool.logMsg('job_trial_list.aspx.loadOfferorList() : Found postcode : ' + postcode   )
            #tool.logMsg('job_trial_list.aspx.loadOfferorList() : Found city     : ' + city       )

        Page.ViewState['ID_LIST'] = idxLst

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())



# ------------------------------------------------------------------------------------------------------------------------------------------------##__handler ------------------------------------------------
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
        offrId          = commandPartList[-1]                       # mongo_ID of item to call
        commandStrng    = commandPartList[-2]                       # command to select webform

        offrGuid        = idList[ System.Convert.ToInt32(offrId) ]  # id of the offeror
        callWebForm     = switcher[commandStrng ]
        
        # tool.logMsg('user_offers.aspx -> HndlrReactionClick  : Clicked ID  ' + System.Convert.ToString( offrGuid ) )
        # tool.logMsg('user_offers.aspx -> HndlrReactionClick  : Command     ' + commandStrng  )
        # tool.logMsg('user_offers.aspx -> HndlrReactionClick  : CallWebForm ' + callWebForm   )

        url = WebConfigurationManager.AppSettings[callWebForm]          #  search for debates
        url += '?item=' + Page.ViewState['itemId']
        url += '&offerer=' + System.Convert.ToString( offrGuid )
        tool.logMsg('user_debates.aspx.HndlrReactionClick : redirect to' + str( url ) )

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())

    if url:
        Response.Redirect( Page.ResolveUrl( url ) )



