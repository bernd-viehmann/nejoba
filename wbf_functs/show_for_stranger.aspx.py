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

from srvcs.ctrl_ItemClasses import ItemMngr
tool = ItemMngr( Page )


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
            mongoId = Page.Request.QueryString['item']
            Page.ViewState['MongoID'] =  mongoId            # remeber what item was called
            dataItm = tool.loadItem(mongoId)
            writeItemDetails( dataItm )
            writeCachedInfos( dataItm )

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())





# ------------------------------------------------------------------------------------------------------------------------------------------------##__Functions for displaying data
# ***********************************************************************************************************************************************
#  writeItemDetails : function is called to insert the detail-data of the item
#
#  29.10.2013  - bervie -     initial realese
#  05.12.2013  - bervie -     lbl_heading and corresponding row was outcommented. heading was shown twice
# ***********************************************************************************************************************************************
def writeItemDetails( dataItem ):
    try:
        heading = unicode(dataItem['heading'] )
        Page.Header.Title = 'nejoba: ' + heading 
        # tool.ui.getCtrl( 'lbl_heading').Text = heading 
        tool.ui.getCtrl( 'divShowMain').InnerHtml = dataItem['html']

        coords = tool.getCoords(dataItem['_ID'])
        if coords is None:
            # hide the map if not needed
            tool.ui.getCtrl( 'MAP_AREA').Visible = False
        else:
            # set the coords for javascript-functions
            tool.ui.getCtrl( 'lbl_map_lon').Text = coords[0]
            tool.ui.getCtrl( 'lbl_map_lat').Text = coords[1]

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ------------------------------------------------------------------------------------------------------------------------------------------------
# ***********************************************************************************************************************************************
#  writeCachedInfos : put the informations fromthe cache on the screen
#
#  29.10.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def writeCachedInfos( dataItem ):
    try:
        cltInfo = System.Globalization.CultureInfo('de-DE')
        tool.ui.getCtrl( 'lbl_nickname').Text = dataItem['nickname'].ToString()
        tool.ui.getCtrl( 'lbl_creationTime').Text = dataItem['creationTime'].ToLocalTime().ToString('d',cltInfo)
        tool.ui.getCtrl( 'lbl_city').Text = dataItem['locationname'].ToString()

        if dataItem['from'] != System.DateTime.MinValue :
            tool.ui.getCtrl( 'lbl_FromDate').Text = dataItem['from'].ToLocalTime().ToString('d',cltInfo) 
        else:
            tool.ui.getCtrl( 'lbl_FromDate_lable').Visible = False

        if dataItem['till'] != System.DateTime.MinValue :
            tool.ui.getCtrl( 'lbl_TillDate').Text = dataItem['till'].ToLocalTime().ToString('d',cltInfo) 
        else:
            tool.ui.getCtrl( 'lbl_TillDate_lable').Visible = False

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())




    #col = itemTable.Columns.Add("_ID", System.String )
    #col = itemTable.Columns.Add("objectType", System.Int32 )
    #col = itemTable.Columns.Add("_objectDetailID", System.String )
    #col = itemTable.Columns.Add("_hostGUID", System.String )
    #col = itemTable.Columns.Add("_rootElemGUID", System.String )
    #col = itemTable.Columns.Add("_parentID", System.String )
    #col = itemTable.Columns.Add("_followerID", System.String )
    #col = itemTable.Columns.Add("_creatorGUID", System.String )
    #col = itemTable.Columns.Add("creationTime", System.DateTime )
    #col = itemTable.Columns.Add("_locationID", System.String )
    #col = itemTable.Columns.Add("from", System.DateTime )
    #col = itemTable.Columns.Add("till", System.DateTime )
    #col = itemTable.Columns.Add("subject", System.String )
    #col = itemTable.Columns.Add("body", System.String )
    ## added 14.02.2013 bervie
    #col = itemTable.Columns.Add("nickname", System.String )
    #col = itemTable.Columns.Add("locationname", System.String )
    ## added 21.06.2013 bervie map-data
    #col = itemTable.Columns.Add("tagZero", System.String )
    #col = itemTable.Columns.Add("lat", System.String )
    #col = itemTable.Columns.Add("lon", System.String )






# ------------------------------------------------------------------------------------------------------------------------------------------------##__handler ------------------------------------------------
# ***********************************************************************************************************************************************
# HndlrReactionClick : handler for buttons that initiate a reaction on a given announcement
#
# 18.03.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def HndlrReactionClick(sender, e):
    try:
        url = None

        url = WebConfigurationManager.AppSettings[ 'CancelOffer' ]   # search for debates
        url += '?item=' + Page.ViewState['MongoID']
        tool.logMsg('show_details.aspx.HndlrReactionClick : redirect to' + str( url ) )

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
    if url:
        Response.Redirect( Page.ResolveUrl( urlNext ) )

















































            #tool.log.w2lgDvlp('JobCache->addCol was called !')

            #creation_date = System.DateTime.Now                                     

            ## 1. get users input
            #dayGiven = tool.gtCtl('txbTimeOfAction').Text
            #if len(dayGiven) == 0 :
            #    slctDay = System.DBNull.Value
            #else :
            #    slctDay = System.DateTime.Parse( tool.gtCtl('txbTimeOfAction').Text )
            #    tool.log.w2lgMsg('type of day_selection = ' + str(type(slctDay)) )

            #slctLocation = tool.gtCtl('selLocation').SelectedValue.ToString()
            #if slctLocation == -1:
            #    slctLocation = System.DBNull.Value
            #    pass    # no location selected : error message should be shown

            #slctType = tool.gtCtl('selJobType').SelectedValue.ToString() 
            #if slctType == -1:
            #    slctType = System.DBNull.Value
            #    pass    # no location selected : error message should be shown


            #tableIdx = tool.jobSrc.jobTable.Rows.Count - 1
            #data = {"GUID"          : System.Guid.NewGuid().ToString(),

            #        "locationID"    : slctLocation ,
            #        "jobTypeID"     : slctType ,
            #        "timeOfAction"  : slctDay, 
                    
            #        "headerTxt"     : tool.gtCtl('txbHeader').Text ,
            #        "bodyTxt"       : tool.gtCtl('txtMain').Text ,
                    
            #        "created"       : creation_date,
            #        "creator"       : 1,
            #        "from"          : creation_date,
            #        "till"          : System.DBNull.Value }

            #ctrlDct = {'collection':'job.main','slctKey':None,'data': data}
            #newObjId = tool.insertDoc(ctrlDct)

            ## 2. write the new data also in the cached table in the application-cache
            ##    we use a string containing the location- and type id to find the data later
            #newRow = tool.jobSrc.jobTable.NewRow();

            #newRow["rowIdx"] = tableIdx
            #newRow["mongoID"] = newObjId
            #newRow['GUID'] = data['GUID']
            #newRow['locationID'] = data['locationID']
            #newRow['jobTypeID'] = data['jobTypeID']
            #newRow['timeOfAction'] = data['timeOfAction']
            #newRow['created'] = data['created']
            #newRow['creator'] = data['creator']
            #newRow["headerTxt"] = data["headerTxt"]
            #newRow["bodyTxt"] = data["bodyTxt"]
            #tool.jobSrc.jobTable.Rows.Add(newRow)

            ## show that job was done  and hide the edit 
            #tool.gtCtl("lblStatusMsg").Visible = True
            #tool.gtCtl("lblStatusMsg").ForeColor = System.Drawing.Color.Green
            #tool.gtCtl("lblStatusMsg").Text = "Vielen Dank. Ihre Eingaben wurden erfolgreich gespeichert.";
            #tool.gtCtl("divStatus").Visible = True
            #tool.gtCtl("divEditArea").Visible = False



