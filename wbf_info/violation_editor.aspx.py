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
import System.Web.UI.WebControls
import System.Guid
import traceback                    # for better exception understanding
import re                           # for finding the taggs
import mongoDbMgr                   # father : the acces to the database

from srvcs.ctrl_ItemClasses import *
tool = ItemMngr( Page )

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

        if( not Page.IsPostBack ):
            # user must be logged in
            tool.usrDt.checkUserRigths(Page, 'free')

            # fill locations-dropdown
            locations = tool.usrDt.getItem('cities')
            tool.log.w2lgDvlp( ' Location for dropdown : ' + unicode(locations) )
            selLocations = tool.ui.getCtrl('sel_location')
            tool.fillUserLocations( selLocations, locations )

            # fill the job-type-dropdown
            selTypeOfJob = tool.ui.getCtrl('sel_type')
            tool.fillJobTypes(selTypeOfJob, 'DE')
            

            #drpDwnText   = WebConfigurationManager.AppSettings['jobType_DE'].split(',')
            #drpDwnValue  = WebConfigurationManager.AppSettings['jobTypeValue'].split(',')
            #for itm in drpDwnText:
            #    idx = drpDwnText.index(itm)
            #    lstItem = System.Web.UI.WebControls.ListItem(unicode(drpDwnText[idx]),unicode(drpDwnValue[idx]))
            #    selTypeOfJob.Items.Add(lstItem)




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
        if sender.ID == 'btnSave':
            tool.saveItem('ROOT_JOB')

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())



