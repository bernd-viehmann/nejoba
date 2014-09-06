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
import traceback                    # for better exception understanding
import re                           # for finding the taggs
import mongoDbMgr                   # father : the acces to the database

from srvcs.ItemJobMsg import *
tool = ItemJobMsg( Page )


# ------------------------------------------------------------------------------------------------------------------------------------------------##__aspn.net ------------------------------------------------
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

        # user must be logged in
        tool.usrDt.checkUserRigths( Page, 'free')

        if not Page.IsPostBack :
            # set the mongo_id of the current location
            # tool.ui.getCtrl('txbx_location_id').Text = tool.usrDt.userDict['LCDFNR_MONGOID'].ToString()

            Page.ViewState['ROOTELEM_ID']   = Page.Request.QueryString['item'] 
            tool.logMsg('job_trial_editor.aspx.Page_Load: mongoId     ' + Page.ViewState['ROOTELEM_ID'] )
            
            # meaninh of Page.ViewState['CRTR_GUID']
            #
            # ViewState['CRTR_GUID'] is the user_GUID of the man who is answering to a help-request aka. joboffer. 
            # when the webform is called by the service-provider the GUID from the currently logged-in user is used as 
            # tag for this trial
            # if the job_trial_editor webform is called from the job_provider asking for help the GUID of the user is given as 
            # url-parameter. that must be used for calling the trial of that particular service-provider
            Page.ViewState['CREATOR_GUID'] = tool.usrDt.getItem('GUID')
            if Page.Request.QueryString['offerer'] :
                Page.ViewState['CREATOR_GUID'] = Page.Request.QueryString['offerer'] 
                tool.logMsg('job_trial_editor.aspx.Page_Load: offerorGuid ' + Page.ViewState['CREATOR_GUID']  )
                tool.OfferorGuid = Page.ViewState['CREATOR_GUID']


        LoadJobTrialThread()                                # get the thread and render it

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ------------------------------------------------------------------------------------------------------------------------------------------------##__handler ------------------------------------------------
# ***********************************************************************************************************************************************
# usrLoggedIn      : called after user succesfully logged in
#
# 18.11.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def HndlrButtonClick(sender, e):
    try:
        urlNext = None

        if sender.ID == 'btn_Publish':
            # save to item.base; the cache and detail-collection
            newId = tool.save()

            # add the new item to the job-trial-thread ( for jobs )
            rootElem = tool.itemTbl.Rows.Find( Page.ViewState['ROOTELEM_ID'] )
            newElem  = tool.itemTbl.Rows.Find( newId )
            creatorGUID = Page.ViewState['CREATOR_GUID']
            tool.chainAdd( rootElem, newElem, 'JOB_HEADER', creatorGUID )
            tool.OfferorGuid = None

            # send email if new item was added
            tool.notify( rootElem, newElem )
            
            # get the thread and update the UI with the new inserted item
            LoadJobTrialThread()            

            # show user that data was loaded and hide the editor
            tool.ui.getCtrlTree( Page.Master )
            tool.ui.getCtrl('YES_WE_CAN').Visible = False
            tool.ui.getCtrl('ownOfferDiv').Visible = False
            tool.ui.getCtrl('SuccessDiv').Visible = True


        elif sender.ID == 'btn_GetPremiumAccount':
            urlNext = WebConfigurationManager.AppSettings['StartPayment']

        elif sender.ID == 'btn_BecomeMember':
            urlNext = WebConfigurationManager.AppSettings['CreateAccount']

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())

    if urlNext != None :
        Response.Redirect( Page.ResolveUrl( urlNext ) )




# ***********************************************************************************************************************************************
# LoadJobTrialThread      : load the list with the thread of given job-trail
#
# 18.11.2012  - bervie -     initial realese
# 06.03.2013  - bervie -     check if user is same than creator. if so we disable the editor and show a message
# ***********************************************************************************************************************************************
def LoadJobTrialThread():
    try:
        # if webform was called with creator-guid call the load with the creator_guid
        headerCreatorGuid   = Page.ViewState['CREATOR_GUID']
        meat                = tool.chainLoad( Page.ViewState['ROOTELEM_ID'] , 'JOB_HEADER', headerCreatorGuid )['html']
        canvas              = tool.ui.findCtrl( Page.Master, 'divShowThread' )
        canvas.InnerHtml    = meat


        # CR from ULLA 06.03.2013 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        # bervie did the job. like most of the time
        if not Page.IsPostBack :
            rootElem = tool.itemTbl.Rows.Find( Page.ViewState['ROOTELEM_ID'] )

            tool.ui.findCtrl( Page.Master, 'lbl_headline').Text = rootElem['subject'].ToString()

            creatorGuid = rootElem['_creatorGUID'].ToString()
            userGuid = tool.usrDt.getItem('GUID').ToString()

            #tool.logMsg('job_trial_editor.aspx.LoadJobTrialThread : creatorGuid : ' + creatorGuid )
            #tool.logMsg('job_trial_editor.aspx.LoadJobTrialThread : userGuid    : ' + userGuid )
            if creatorGuid == userGuid :
                tool.ui.getCtrlTree( Page.Master )
                # tool.ui.getCtrl('YES_WE_CAN').Visible = False
                tool.ui.getCtrl('ownOfferDiv').Visible = True
                #
                # 'YES_WE_CAN' is not hidden because we have to answer 
                # to other offers also. so editor is needed !!
                #


        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
