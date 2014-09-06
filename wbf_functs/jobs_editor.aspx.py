#  
# editor.aspx.py 
#  
# the webform is used for creating new job offers for the community. user can define the location, the typ of the job and the time of action
#  
#
#  03.10.2012   bevie    initial realese
#  13.01.2013   bevie    redesign to new Item_class partition
#
#
#  
from System.Web.Configuration import *
import System.DateTime
import System.Drawing.Color
import System.Web.UI.WebControls
import System.Guid
import traceback                    # for better exception understanding
import re                           # for finding the taggs
import mongoDbMgr                   # father : the acces to the database

from srvcs.ItemJobRoot import *
from srvcs.tls_UiHelper import LocDefiner

lcDfnr = LocDefiner( Page )            # the helper class for location-stuff
tool = ItemJobRoot( Page )

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
        tool.errorMessage('')

        if( not Page.IsPostBack ):
            # user must be logged in
            tool.usrDt.checkUserRigths( Page, 'free' )


        # added 18.11.2013 bervie 
        # the location-select is currently not implemented for the editors.
        # this will be done later
        #
        #
        #
        #chngDiv = tool.ui.getCtrl('div_slct_loctn')
        #chngDiv.Attributes["style"] = " display: none";
        #
        #
        # added 18.11.2013 bervie 

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ***********************************************************************************************************************************************
# Page_PreRender    : initializer after button_click
#
# 18.11.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_PreRender(sender, e):
    try:
        # the currently valid location infos shold be in the textfields used for saving the item
        tool.ui.getCtrl('txbx_location_id').Text = System.String.Empty
        tool.ui.getCtrl('txbx_location_name').Text = System.String.Empty
        lcDfnr.uiInitLocIntfc()
        tool.ui.getCtrl('txbx_location_id').Text = lcDfnr.mongoId
        tool.ui.getCtrl('txbx_location_name').Text = lcDfnr.getCityName()

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return


# ------------------------------------------------------------------------------------------------------------------------------------------------##__handler ------------------------------------------------
# ***********************************************************************************************************************************************
# usrLoggedIn      : called after user succesfully logged in
#
# 18.11.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def HandlBtnClick(sender, e):
    try:
        urlNext = None
        # button for changing session-stored location was pressed  18.11.2013
        if sender.ID == 'btn_select_slct_loctn':
            countryCode     = tool.ui.getCtrl('sel_country').SelectedValue 
            cityIdentifier  = tool.ui.getCtrl('txbx_city').Text
            lcDfnr.setLocByInpt( countryCode , cityIdentifier ) 

            if lcDfnr.getValidLoctn() is None:
                tool.errorMessage(' <br />Es wurde keine Stadt oder Postleitzahl gefunden! <br />Hast du das richtige Land ausgew&auml;hlt?<br />')
                return False

        if sender.ID == 'btn_Save':
            # was all needed stuff given?
            if checkInput() == False:
                return

            else:
                # changed 18.11.2013 : the dropdown now is replaced by an hidden textfield : txbx_jobType
                #                      this textedit is filled by javascript 
                #
                newId = tool.save()
                urlNext = WebConfigurationManager.AppSettings['ViewDetailForm'] + '?item=' + unicode( newId )
                tool.log.w2lgDvlp( ' jobs_editor_save redirects to  : ' + unicode(urlNext) )
                #
                #
                # end of change 18.11.2013 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())

    if urlNext != None :
        Response.Redirect( Page.ResolveUrl( urlNext ) )




# ***********************************************************************************************************************************************
# checkInput : check users input jobtype must be selcted
#
# 29.11.2011    bervie  initial realese
# 08.02.2013    bervie  removed txtMain-Check on wish of stefan. user should be able to use only the header as complete text
# ***********************************************************************************************************************************************
def checkInput():
    try:
        # a location must be present
        if len(tool.ui.getCtrl('txbx_tagforitem').Text) < 1:
            errStr = tool.ui.getCtrl('msg_slectJobType').Text
            errStr += tool.ui.getCtrl('msg_errorfooter').Text
            tool.errorMessage( errStr )
            return False
        
        # at least a header-text must be present. he will be used as headline in the lists (no map-jobs are supported yet)
        if len(tool.ui.getCtrl('txbHeader').Text) < 1:
            errStr = tool.ui.getCtrl('msg_defineHeader').Text  
            errStr += tool.ui.getCtrl('msg_errorfooter').Text
            tool.errorMessage( errStr )
            return False

        # location must be choosen. checking the location-id field
        if 'not' in tool.ui.getCtrl('txbx_location_id').Text.ToString():
            errStr = tool.ui.getCtrl('msg_missingLocation').Text  
            errStr += tool.ui.getCtrl('msg_errorfooter').Text
            tool.errorMessage( errStr )
            return False

        # if no location was found this must be changed from the user
        if lcDfnr.getValidLoctn() is None:
            errStr = tool.ui.getCtrl('msg_wrong_location').Text  
            
            tool.errorMessage( errStr )
            return False

        return True

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


