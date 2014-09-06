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

# import mongoDbMgr                   # father : the acces to the database
# tool = mongoDbMgr.mongoMgr(Page);

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
            canvas = tool.ui.findCtrl( Page, 'divShowMain')
            Page.ViewState['MongoID'] = mongoId     # used to call external sides from this editor
            itm = tool.loadItem(mongoId)
            canvas.InnerHtml = itm['html'].ToString()

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
        url = WebConfigurationManager.AppSettings[ 'CancelOffer' ]  # search for debates
        url += '?item=' + Page.ViewState['MongoID']
        tool.logMsg('show_details.aspx.HndlrReactionClick : redirect to' + str( url ) )

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())

    if url:
        Response.Redirect( Page.ResolveUrl( url ) )




# ------------------------------------------------------------------------------------------------------------------------------------------------##__Methodes ------------------------------------------------
# ***********************************************************************************************************************************************
# LoadAndDisplayData(mongoId) : load the details of an item from the database and write it to the DIV-container for output
#
# 28.11.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
#def LoadAndDisplayData( dbId ):
#    try:
#        # ctrlDict = {'collection':'item.announcment','slctKey':'_id','slctVal':dbId}
#        ctrlDict = {'collection':'item.announcment','slctVal':dbId}
#        tool.readDoc(ctrlDict)
#        result = ctrlDict['data']

#        heading = result['heading'].ToString()
#        body = result['body'].ToString()

#        outPut = '<h2>' + heading + '</h2><br/><br/>'
#        outPut += body + '<br/><br/>'

#        canvas = tool.ui.findCtrl(Page, 'divShowMain')
#        canvas.InnerHtml = outPut

#    except Exception,e:
#        tool.log.w2lgError(traceback.format_exc())



























































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



