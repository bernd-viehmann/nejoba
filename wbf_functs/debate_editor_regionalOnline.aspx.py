#  
# editor.aspx.py 
#  
# the webform is used for creating new job offers for the community. user can define the location, the typ of the job and the time of action
#  
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
            destination = self.ui.findCtrl(self.Page, 'date_event_div')
            destination.InnerHtml = self.ui.rubricDict['date_event_div']
            destination = self.ui.findCtrl(self.Page, 'location_div')
            destination.InnerHtml = self.ui.rubricDict['location_div']
            destination = self.ui.findCtrl(self.Page, 'annonce_div')
            destination.InnerHtml = self.ui.rubricDict['annonce_div']
            destination = self.ui.findCtrl(self.Page, 'initiative_div')
            destination.InnerHtml = self.ui.rubricDict['initiative_div']
            destination = self.ui.findCtrl(self.Page, 'business_div')
            destination.InnerHtml = self.ui.rubricDict['business_div']
            # 10.08.2013 bervie  END 

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


tool = ItemDebateRoot( Page )


# ------------------------------------------------------------------------------------------------------------------------------------------------##__aspn.net ------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------##__aspn.net ------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------##__aspn.net ------------------------------------------------
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

            # fill in the dropdowns
            drpDwn = tool.ui.getCtrl('sel_lctn')
            locations = tool.usrDt.getItem('cities')
            tool.fillUserLocations( drpDwn, locations )

            # set the country-code for javascript noatim query
            if tool.usrDt.isLoggedIn():
                lblCtryCode = tool.ui.getCtrl('lbl_countrycode')
                lblCtryCode.Text = tool.usrDt.getItem('countrycode')

            # remeber a given rubric if given
            if Page.Request.QueryString['key'] is not None:
                Page.ViewState['RUBRIC'] = Page.Request.QueryString['key']

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ------------------------------------------------------------------------------------------------------------------------------------------------##__handler ------------------------------------------------
# ***********************************************************************************************************************************************
# usrLoggedIn      : called after user succesfully logged in
#
# 18.11.2012  - bervie -     initial realese
# 20.06.2013  - bervie -     store the rubric defined in the webform (javascript-multi-select-machinery) in the ViewStare
# ***********************************************************************************************************************************************
def HndlrButtonClick(sender, e):
    try:
        urlNext = None 
        tool.ui.getCtrlTree( Page.Master )

        if sender.ID == 'btn_Save':
            if ValidateWebform() == True:
                # ---------------------------------------------------------------------------------------------
                newId = tool.save()
                urlNext = Page.ResolveUrl(WebConfigurationManager.AppSettings['ViewDetailForm']) + '?item=' + unicode( newId )


    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())

    if urlNext != None :
        Response.Redirect(urlNext)





# ***********************************************************************************************************************************************
# ValidateWebform    : check user input
#
# 24.06.2013  - bervie -     initial realese
#
# ***********************************************************************************************************************************************
def ValidateWebform():
        try:

            # a header-text must be given. needed to be shown in the header-msg ---------------------------------------
            if len(tool.ui.getCtrl('txbHeader').Text.strip()) < 1:
                errorMsg = tool.ui.getCtrl('lbl_header_needed').Text
                tool.errorMessage( errorMsg )
                return False

            # check dates for start and end ---------------------------------------------------------------------------
            # txbx_timeFrom : check if given and is valif DateTime format
            deDe = CultureInfo("de-DE"); 


            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
            #timeFrom = tool.ui.getCtrl('txbx_timeFrom').Text.strip()
            #if len( timeFrom ) > 0:
            #    # currently we only support german date-format
            #    if System.DateTime.TryParseExact(timeFrom, "dd.MM.yyyy", deDe, DateTimeStyles.None )[0] != True:
            #        errorMsg = tool.ui.getCtrl('lbl_time_from_invalid_format').Text
            #        tool.errorMessage( errorMsg )
            #        return False

            #timeTo = tool.ui.getCtrl('txbx_timeTo').Text.strip()
            #if len( timeTo ) > 0:
            #    # check if a timeFrom value is given
            #    if len( timeFrom ) < 1:
            #        errorMsg = tool.ui.getCtrl('lbl_missing_from_date').Text
            #        tool.errorMessage( errorMsg )
            #        return False

            #    # currently we only support german date-format
            #    if System.DateTime.TryParseExact(timeTo, "dd.MM.yyyy", deDe, DateTimeStyles.None )[0] != True:
            #        errorMsg = tool.ui.getCtrl('lbl_time_to_invalid_format').Text
            #        tool.errorMessage( errorMsg )
            #        return False
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

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

            return True

        except Exception,e:
            tool.log.w2lgError(traceback.format_exc())


