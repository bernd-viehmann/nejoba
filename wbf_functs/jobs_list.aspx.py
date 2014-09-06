#  
# joblist : MOST IMPORTANT WEBFORM 
#           displays a list with jobs and makes them accesible
#  
# 16.11.2012        bv      started wit srious working
#  
#  HINT:  
#   
#  the webform uses the view-state to store all jobs for this webform.
#  it displays only a part of it
#
# 
from System.Web.Configuration import *
from System import UriPartial
import System
import traceback
import mongoDbMgr                                   # i am your father, luke
from srvcs.tls_UiHelper import LocDefiner
tool = mongoDbMgr.mongoMgr( Page )
lcDfnr = LocDefiner( Page )                         # the helper class for location-stuff
srchPtrn = {}

destUrl = None
if not tool.usrDt.isLoggedIn():
    destUrl = WebConfigurationManager.AppSettings['DetailsForStrangers']        # use the detail-viewer for visitors that aren't looged in
else:
    destUrl = WebConfigurationManager.AppSettings['AddToTrialThread']           # go to detail-viewer for logged in users


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
        tool.errorMessage('')

        if not Page.IsPostBack:
            # jobtype comes per URL-parameter
            jbTypeDef = Page.Request.QueryString['jobtype'] 
            tool.ui.getCtrl('txbx_jobName').Text = jbTypeDef
            if jbTypeDef != '*':
                jbTpHshTg = getJobType( jbTypeDef )
                tool.logMsg( 'jbTypeDef = Page.Request.QueryString["jobtype"]  : ' + jbTypeDef )
                tool.logMsg( 'jbTypeDef = Hashtag found by getJobType          : ' + jbTpHshTg )
                tool.ui.getCtrl('txbx_jobType').Text = jbTpHshTg

            # location can come as URL-parameter : re-initialyze the location-definer
            loctn = System.String.Empty
            if Page.Request.QueryString['Loc'] != None:
                loctn = Page.Request.QueryString['Loc']
                lcDfnr.setLocByDbId( loctn )

        else:
            # clear items in reppeater
            repeater = tool.gtCtl('repJobList')
            repeater.DataSource = None
            repeater.DataBind()


        tool.ui.getCtrl('txbx_location_id').Text = lcDfnr.mongoId
        tool.ui.getCtrl('txbx_location_name').Text = lcDfnr.getCityName()
        tool.logMsg( 'lobs_list_aspx.py->PageLoad->txbx_location_id   : ' + lcDfnr.mongoId )
        tool.logMsg( 'lobs_list_aspx.py->PageLoad->txbx_location_name : ' + lcDfnr.getCityName() )

        if not Page.IsPostBack : LoadJobList()

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ***********************************************************************************************************************************************
# Page_PreRender    : initializer after button_click
#
# 18.11.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_PreRender(sender, e):
    try:
        # insert curretn location from the session-cache
        lcDfnr.uiInitLocIntfc()


    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return


# ***********************************************************************************************************************************************
# HndlrButtonClick    : handler for button-click-events. chose button by ID
#
# 14.10.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def HandlBtnClick(sender, e):
    try:
        url = None
        # 
        # handle location-change button
        # 
        if sender.ID == 'btn_select_slct_loctn':
            countryCode     = tool.ui.getCtrl('sel_country').SelectedValue 
            cityIdentifier  = tool.ui.getCtrl('txbx_city').Text

            tool.logMsg( 'lobs_list_aspx.py->HandlBtnClick->countryCode     : ' + countryCode )
            tool.logMsg( 'lobs_list_aspx.py->HandlBtnClick->cityIdentifier  : ' + cityIdentifier )


            lcDfnr.setLocByInpt( countryCode , cityIdentifier ) 

            if lcDfnr.getValidLoctn() is None:
                tool.errorMessage(' <br />Es wurde keine Stadt oder Postleitzahl gefunden! <br />Hast du das richtige Land ausgew&auml;hlt?<br />')
                return

            LoadJobList()

        # 
        # handle location-change button
        # 
        elif sender.ID == 'btn_load_list':
            LoadJobList()

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return

    if url != None :
        # tool.usrDt.measurePeformance('HndlrButtonClick of webform Default.aspx before redirection')
        Response.Redirect( Page.ResolveUrl( urlNext ) )


# ***********************************************************************************************************************************************
# getJobType    : the URL-param send s the jobtype in german. we need the type from the webconfig
#
# 26.11.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def getJobType( jbName ):
    try:
        seperator = WebConfigurationManager.AppSettings['stringSeperator']
        names = WebConfigurationManager.AppSettings['jobType_DE'].split(seperator)
        values = WebConfigurationManager.AppSettings['jobTypeValue'].split(seperator)

        idx = names.index(jbName)

        return values[idx]

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ***********************************************************************************************************************************************
# LoadJobeList   : load a list with debates filtered by controll-data
#
# 07.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def LoadJobList():
    try:
        tagTable    = tool.appCch.dtSt.Tables["itemTags"]
        itemTable   = tool.appCch.dtSt.Tables["items"]
        resultTble  = itemTable.Clone()                                                                 # destination-table connected with the repeater

        #minAmount = System.Convert.ToInt16( WebConfigurationManager.AppSettings["MinNumOfJobs"] )       # min of results that should be displayed
        #jobTyp = tool.ui.getCtrl('sel_type').SelectedValue.ToString()           # get the wanted job-type from the job-type dropdown box

        # if jobtype is selected we have to filter the results
        selectJobType = Page.Request.QueryString['jobtype']

        if selectJobType != '*':
            LoadJobsOfType()                # if something was selceted filter the job-types
        
        else:
            LoadAllJobs()                   # if no job was selected we load all stuff

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
# LoadAllJobs   : when no job-type is selected this function loads all jobs for a given region
#
# 19.04.2013  - bervie -     initial realese
# 
# ***********************************************************************************************************************************************
def LoadAllJobs():
    try:
        tool.logMsg('jobs_list.aspx.py-LoadAllJobs' )

        # 1. search-parameter from the UI
        #    locations : get the selected location
        tagTable    = tool.appCch.dtSt.Tables["itemTags"]
        itemTable   = tool.appCch.dtSt.Tables["items"]
        resultTble  = itemTable.Clone()
        #minAmount = System.Convert.ToInt16( WebConfigurationManager.AppSettings["MinNumOfDebates"] )

        # 2. create a list o0f locations ordered by the distance from selected value
        locList = lcDfnr.loadCityArea( False )

        # helper-array to store all mongo-ids we have loaded from item-table
        idList = []

        for location in locList:
            # select all jobs in this area
            rows = tool.appCch.dtVwLoctn.FindRows( location )
            tool.logMsg('jobs_list.aspx.py-LoadAllJobs location_id : ' + str(location) )

            for row in rows:
                if row['objectType'] == 0:              # get all jobs
                    resultTble.ImportRow(row.Row)
                    idList.Add( row['_ID'].ToString() )
                    tool.logMsg('jobs_list.aspx.py-LoadAllJobs item loaded : ' + row['_ID'].ToString() )

                    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
                    # HACK tagZero in the temporary result-table will store the link to the detailview
                    # added 11-08-2013 bervie
                    itmLnk = destUrl + '?item=' + row['_ID'].ToString()
                    resultTble.Rows[resultTble.Rows.Count - 1]['tagZero'] = itmLnk
                    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

            #if len(idList) >= minAmount : break

        # store ids in order of apperance in the table into an array. we will get the _id by calling the index of this array
        Page.ViewState['IdList'] = idList            

        # 3. bind repeater to result data-table
        if resultTble.DefaultView.Count == 0:
            # no data was found
            tool.errorMessage(tool.ui.getCtrl('msg_no_jobs_found').Text)
        else:
            # bind repeater to result data-table
            repeater = tool.gtCtl('repJobList')
            repeater.DataSource = resultTble.DefaultView
            repeater.DataBind()

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ***********************************************************************************************************************************************
# LoadJobsOfType   : load a list with jobs matching a given job-type
#
# 19.04.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def LoadJobsOfType():
    try:
        # we need the location-id as country|postcode pair [for example : DE|41836]
        locId = lcDfnr.getCtryPstCd()
        jobType = tool.ui.getCtrl('txbx_jobType').Text            # get selected location
        tgLst = tool.ui.convertTagsFromInput(jobType)

        for tgIdx in tgLst:
            tool.logMsg('jobs_list.aspx.py-LoadJobsOfType->tag-index found for job-list-parameter  : ' + unicode(tgIdx) )

        itmIds = tool.taggs.loadBaseItems( locId, tgLst, False )

        itemTable   = tool.appCch.dtSt.Tables["items"]
        resultTble  = itemTable.Clone()

        for itm in itmIds:
            row = itemTable.Rows.Find(itm)
            resultTble.ImportRow(row)
            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
            #
            # HACK tagZero in the temporary result-table will store the link to the detailview
            # added 11-08-2013 bervie
            #
            itmLnk = destUrl + '?item=' + row['_ID'].ToString()
            resultTble.Rows[resultTble.Rows.Count - 1]['tagZero'] = itmLnk

        # store ids in order of apperance in the table into an array. we will get the _id by calling the index of this array
        Page.ViewState['IdList'] = itmIds

        if resultTble.DefaultView.Count == 0:
            # no data was found
            tool.errorMessage(tool.ui.getCtrl('msg_no_jobs_found').Text)
        else:
            # bind repeater to result data-table
            repeater = tool.gtCtl('repJobList')
            repeater.DataSource = resultTble.DefaultView
            repeater.DataBind()

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
