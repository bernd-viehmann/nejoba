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
            Page.ViewState['MongoID'] = mongoId     # used to call external sides from this editor

            tool.log.w2lgDvlp('show_details->PageLoad : root_elem_id stored in the viewstate : ' + str(Page.ViewState['MongoID']) )


            canvas = tool.ui.findCtrl( Page, 'divShowMain')
            itm = tool.loadItem(mongoId)
            canvas.InnerHtml = itm['html']

            #Page.ViewState['ObjType'] = itm['objectType']
            #tool.log.w2lgDvlp('show_details->PageLoad : type of item loaded : ' + str(itm['objectType']) )
            


    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ------------------------------------------------------------------------------------------------------------------------------------------------##__handler ------------------------------------------------
# ***********************************************************************************************************************************************
# HndlrReactionClick : handler for buttons to redirect to a webform with different functionality (am i brainfucking ?!?)
#
# 18.03.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def HndlrReactionClick(sender, e):
    try:
        # get the needed informations from the ID by seperating string by '_'. 
        clntIdComponents = sender.ClientID.ToString().split('_')
        swtchStr = clntIdComponents[1][3:]
        itemId = Page.ViewState['MongoID'] 

        urlNext = None

        #if Page.ViewState['ObjType'] == 0:
        #    list = Page.ResolveUrl( WebConfigurationManager.AppSettings["ListJobs"] )
        #    add  = Page.ResolveUrl( WebConfigurationManager.AppSettings["AddToTrialThread"] )
        #else:
        #    list = Page.ResolveUrl( WebConfigurationManager.AppSettings["ListDebates"] )
        #    add  = Page.ResolveUrl( WebConfigurationManager.AppSettings["AddArticleToDebate"] )


        itemId = Page.ViewState['MongoID']
        if   swtchStr == 'List': 
            urlNext = list
            tool.log.w2lgDvlp('show_details->HndlrReactionClick : List was clicked - url from config: ' + urlNext )

        elif swtchStr == 'Offr': 
            urlNext = add + "?item=" + itemId
            tool.log.w2lgDvlp('show_details->HndlrReactionClick : Offr was clicked - url from config: ' + urlNext )

        elif swtchStr == 'Rprt': 
            urlNext = WebConfigurationManager.AppSettings["MessageViolation"] + "?item=" + itemId
            tool.log.w2lgDvlp('show_details->HndlrReactionClick : Rprt was clicked - url from config: ' + urlNext )

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return

    if urlNext != None :
        Response.Redirect( Page.ResolveUrl( urlNext ) )



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



