#  
# editor.aspx.py 
#  
# the webform is used for creating new job offers for the community. user can define the location, the typ of the job and the time of action
#
#  03.10.2012   bevie    initial realese
#  
import clr
clr.AddReference('MongoDB.Bson')
clr.AddReference('MongoDB.Driver')
from MongoDB.Bson import *
from MongoDB.Driver import *
from System.Web.Configuration import *
from System.Globalization import *
import System.Text
import traceback            # for better exception understanding
import System.Guid
import re
import codecs


# ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ##
# ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ##
from srvcs.Item import *    # base-class for data-objects
class ItemDebateRoot ( Item ):
    '''
    ItemDebateRoot is a member of a debate-thread
    '''

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # constructor. 
    #
    #
    # 16.01.2013   - bervie-      initial realese
    # 14.06.2013   - bervie-      added load of matrix-definitions from a file
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def __init__(self, page ):
        try:
            Item.__init__(self, page )                                      # wake up papa ; mother njbTools is included by inheritance!
            self.objTypIdx = self.getObjectTypeId( 'DEBATE_ROOT' )          # define what kind of object we have by setting the object_type_id as integer

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    #
    # user_interface_functions
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def pgLoad( self ):
        try:
            pass

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # chainCreateHeader()  :   creating a new header for a discussion-thread : DEBATE_HEADER
    #
    # parameter     :  rootElemID           : the root-elem we are looking for
    # return        :  createdHeaderId      : the new created ID of the Header
    #
    # HINT : the initiator is the creator of the root-element. In this case it means the guy who asked for some help in his neighbouhood
    #        the prospect is the guy who is interested in getting the job. for every initiator/prospect-pair there is chain 
    #
    #
    #
    #
    # 21.12.2012   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def chainCreateHeader( self  ):
        try:
            rootElemId      = self.Page.ViewState['MongoID']
            headerTypeId    = self.getObjectTypeId('ROOT_HEADER')
            self.log.w2lgDvlp("ItemDebateMsg.chainCreateHeader called for  " + rootElemId + " of TypeId : " + unicode(headerTypeId) )
            root = self.itemTbl.Rows.Find( rootElemId )

            # 1. write the detail-data-ID
            initiatorGUID       = root['_creatorGUID']              # the creator of the root-elem
            prospectGUID        = self.usrDt.getItem('GUID')        # current user
            headerCreated       = System.DateTime.UtcNow            # time of header-creation

            lastUpdateInitiator = System.DBNull.Value               # last insert from job-offerer
            lastUpdateprospect  = System.DateTime.UtcNow            # last insert from service-provider interested in the job
            lastVisitInitiator  = System.DBNull.Value               # last visit from job-offerer
            lastVisitProspect   = System.DBNull.Value               # last visit from service-provider interested in the job

            # 2. write the item.base-data
            self.objTypIdx       = headerTypeId
            self.objectDetailID  = newDebateHeaderDetailId

            headerId = self.storeGeneralBase()
            self.setMembrAttrb()

            # self.data is not changed for HEADER-elements
            return headerId


        except Exception,e:
            self.log.w2lgError(traceback.format_exc())
# ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ##
# ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ##



# ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ##
# ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ##
#from srvcs.tls_UiHelper import geoMth
from srvcs.tls_UiHelper import LocDefiner
lcDfnr = LocDefiner( Page )            # the helper class for location-stuff
# ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ##
# ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ##


tool = ItemDebateRoot( Page )


# ------------------------------------------------------------------------------------------------------------------------------------------------##__aspn.net ------------------------------------------------
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

        if not Page.IsPostBack :
            # user must be logged in (uncommented during dev 12_06_2013_bervie
            tool.usrDt.checkUserRigths( Page, 'free')

            # put home data of user into the dropdown initialy
            drpDwn = tool.ui.getCtrl('sel_lctn')
            locations = tool.usrDt.getItem('cities')
            tool.fillUserLocations( drpDwn, locations )

            # set the place-name-id and name
            # 25.11.2013 REMOVED will be replaced with the stuff from LocDefiner
            #
            #
            #
            #tool.ui.getCtrl('txbx_location_id').Text = drpDwn.Items[0].Value
            #tool.ui.getCtrl('txbx_location_name').Text = drpDwn.Items[0].Text
            #
            #
            # 25.11.2013 REMOVED 


            #use germany as default
            drpDwnCtryCode = tool.ui.getCtrl('sel_country')
            drpDwnCtryCode.SelectedValue = 'DE'

            # set the country-code for javascript noatim query
            if tool.usrDt.isLoggedIn():
                lblCtryCode = tool.ui.getCtrl('lbl_countrycode')
                lblCtryCode.Text = tool.usrDt.getItem('countrycode')

            # remeber a given rubric if given
            if Page.Request.QueryString['key'] is not None:
                Page.ViewState['RUBRIC'] = Page.Request.QueryString['key']

        # added 18.11.2013 bervie 
        # the location-select is currently not implemented for the editors.
        # this will be done later
        #chngDiv = tool.ui.getCtrl('div_slct_loctn')
        #chngDiv.Attributes["style"] = " display: none";
        #if tool.usrDt.userDict.has_key('LCDFNR_UIP_NICENAME'):
        #    tool.ui.getCtrl('txbx_location').Text = tool.usrDt.userDict['LCDFNR_UIP_NICENAME'].ToString()
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
# HndlrButtonClick : called after user succesfully logged in
#
# 18.11.2012  - bervie -     initial realese
# 20.06.2013  - bervie -     store the rubric defined in the webform (javascript-multi-select-machinery) in the ViewStare
# ***********************************************************************************************************************************************
def HandlBtnClick(sender, e):
    try:
        urlNext = None 
        tool.ui.getCtrlTree( Page.Master )

        # button for changing session-the valid location   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        if sender.ID == 'btn_select_slct_loctn':
            countryCode     = tool.ui.getCtrl('sel_country').SelectedValue 
            cityIdentifier  = tool.ui.getCtrl('txbx_city').Text
            lcDfnr.setLocByInpt( countryCode , cityIdentifier ) 

            if lcDfnr.getValidLoctn() is None:
                msgTxt = tool.ui.getCtrl('msg_no_location_found').Text
                tool.errorMessage( msgTxt )
                return

        # save button -> store data into the database - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        if sender.ID == 'btn_Save':

            ## get the location-infos from the session-cache and store them into the UI
            #loctnInfo = lcDfnr.getSessionCacheLoc()
            #if loctnInfo is None:
            #    tool.ui.getCtrl('txbx_location_id').Text = System.String.Empty
            #    tool.ui.getCtrl('txbx_location_name').Text = System.String.Empty
            #    errorMsg = tool.ui.getCtrl('msg_no_location_found').Text
            #    tool.errorMessage( errorMsg )
            #    return

            # check if we have a valid mongo-ID in the session-cache
            if lcDfnr.getValidLoctn() is None:
                tool.ui.getCtrl('txbx_location_id').Text = System.String.Empty
                tool.ui.getCtrl('txbx_location_name').Text = System.String.Empty
                errorMsg = tool.ui.getCtrl('msg_no_location_found').Text
                tool.errorMessage( errorMsg )
                return

            else:
                tool.ui.getCtrl('txbx_location_id').Text = lcDfnr.mongoId
                tool.ui.getCtrl('txbx_location_name').Text = lcDfnr.getCityName()

            if checkInput() is not True:
                # message to user is created in the checkInput-function
                return

            # write the input into the cache and the db
            newId = tool.save()
            urlNext = Page.ResolveUrl(WebConfigurationManager.AppSettings['ViewDetailForm']) + '?item=' + unicode( newId )


    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())

    if urlNext != None :
        Response.Redirect(urlNext)





# ***********************************************************************************************************************************************
# checkInput    : check user input
#
# 24.06.2013  - bervie -     initial realese
#
# ***********************************************************************************************************************************************
def checkInput():
        try:

            # a header-text must be given. needed to be shown in the header-msg ---------------------------------------
            if len(tool.ui.getCtrl('txbHeader').Text.strip()) < 1:
                errorMsg = tool.ui.getCtrl('lbl_header_needed').Text
                tool.errorMessage( errorMsg )
                return False

            # check dates for start and end ---------------------------------------------------------------------------
            # txbx_timeFrom : check if given and is valif DateTime format
            deDe = CultureInfo("de-DE"); 

            dateFrom = None
            dateTo = None
            if len( tool.ui.getCtrl('txbx_timeFrom').Text.strip() ) > 0:
                try:
                    dateFrom = System.DateTime.ParseExact( tool.ui.getCtrl('txbx_timeFrom').Text.strip() , 'dd.MM.yyyy' , None )
                except SystemError:
                    errorMsg = tool.ui.getCtrl('lbl_time_from_invalid_format').Text
                    tool.errorMessage( errorMsg )
                    return False

            if len( tool.ui.getCtrl('txbx_timeTo').Text.strip() ) > 0:
                try:
                    dateTo   = System.DateTime.ParseExact( tool.ui.getCtrl('txbx_timeTo').Text.strip()   , 'dd.MM.yyyy' , None )
                except SystemError:
                    errorMsg = tool.ui.getCtrl('lbl_time_to_invalid_format').Text
                    tool.errorMessage( errorMsg )
                    return False
                
                if (dateTo != None) and (dateFrom == None):
                    errorMsg = tool.ui.getCtrl('lbl_missing_from_date').Text
                    tool.errorMessage( errorMsg )
                    return False
            
                if (dateTo != None) and (dateFrom != None):
                    cmpr = System.DateTime.Compare(dateFrom, dateTo)
                    if cmpr > 0:
                        errorMsg = tool.ui.getCtrl('lbl_from_date_after_to').Text
                        tool.errorMessage( errorMsg )
                        return False

            # check the coordinate-input ------------------------------------------------------------------------------
            latInp = tool.ui.getCtrl('txbx_lat').Text.strip()
            lonInp = tool.ui.getCtrl('txbx_lon').Text.strip()

            # both coordinates must be given
            if (( len( latInp) > 0) and ( len( lonInp) < 1)) or (( len( lonInp) > 0) and ( len( latInp) < 1)):
                errorMsg = tool.ui.getCtrl('lbl_need_both_coords').Text
                tool.errorMessage( errorMsg )
                return False

            # check for a valid location-ID
            loctnId = tool.ui.getCtrl('txbx_location_id').Text.strip()
            tool.log.w2lgDvlp("debate_Editor->check_input   : received location-id : " + loctnId )
            if 'not ' in loctnId :
                errorMsg = tool.ui.getCtrl('msg_no_location_found').Text
                tool.errorMessage( errorMsg )
                return False

            return True

        except Exception,e:
            tool.log.w2lgError(traceback.format_exc())
# ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ##
# ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ##
# ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ##
# ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ## -- ## ##


