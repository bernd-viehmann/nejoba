#
# debate_projector.aspx.py
# 
#  the list of items available in the nejoba-database
#
import clr
clr.AddReference('MongoDB.Bson')
clr.AddReference('MongoDB.Driver')
from MongoDB.Bson import *
from MongoDB.Driver import *
from System.Web.Configuration import *
from System.Globalization import *
import System.Text
import System.Data
import System.Collections
import traceback                    # for better exception understanding
import System.Guid
import re
import mongoDbMgr                   # father : the acces to the database


# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
#
# helper for debatzeProjector.aspx.py : the form used to log-in or to change to the account-creation-webform
#  
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
class DebateProjector( mongoDbMgr.mongoMgr ):
    '''
    DebateProjector is the helper-class for the neighbour-forum
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
            mongoDbMgr.mongoMgr.__init__(self, page )      # wake up papa ; mother njbTools is included by inheritance!
            self.log.w2lgDvlp('DebateProjector( .. ) constructor called')

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    #
    # rubricWriteConfToDivs : called in page-load to copy the mem-cache with the rubric-configuration into the divs (used by map- debate-profector and debate-editor)
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def rubricWriteConfToDivs( self ):
        try:
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

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    #
    # insrtUsersHomeTown : if user is logged in his hometown will be inserted into the modal-dialog
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def insrtUsersHomeTown( self ):
        try:
            if self.usrDt.isLoggedIn():
                self.ui.getCtrl( 'sel_country'  ).SelectedValue = self.usrDt.userDict['countrycode'].ToString()
                self.ui.getCtrl( 'txbx_postCode' ).Text = self.usrDt.userDict['postcode'].ToString()

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    #
    # hndlUrlParam : this function checks if we have URL-parameter and stores the in the corresponding edit-fields
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def hndlUrlParam( self ):
        try:
            #http://localhost:1572/njb_2/wbf_activemap/map_two.aspx?SliceActive=1&CrsCmd=end_of_data&ResultLength=2500&ItemType=map&Loc=0|&StartDate=&EndDate=&SrchMd=OR&Tags=,&#

            self.param = {}                                                 # the URL-parameters are stored in member-attribute param = {}
            self.param.Add('ItemType'       , None)         # map,list or date
            self.param.Add('SliceActive'    , None)         # which slice is active on the db
            self.param.Add('CrsCmd'         , None)         # cursor-positioning-command
            self.param.Add('ResultLength'   , None)         # length to receive
            self.param.Add('Loc'            , None)
            self.param.Add('Tags'           , None)
            self.param.Add('SrchMd'         , None)
            self.param.Add('StartDate'      , None)
            self.param.Add('EndDate'        , None)

            if ('ItemType' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['ItemType'] != System.String.Empty:
                    self.param['ItemType'] = self.Page.Request.QueryString['ItemType']

            # SliceActive is not used in the CACHE. we always check the whole data in the cache
            if ('SliceActive' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['SliceActive'] != System.String.Empty:
                    self.param['SliceActive'] = System.Convert.ToInt32( self.Page.Request.QueryString['SliceActive'])

            if ('CrsCmd' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['CrsCmd'] != System.String.Empty:
                    self.param['CrsCmd'] = self.Page.Request.QueryString['CrsCmd']

            if ('ResultLength' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['ResultLength'] != System.String.Empty:
                    self.param['ResultLength'] = System.Convert.ToInt32( self.Page.Request.QueryString['ResultLength'])

            if ('Loc' in self.Page.Request.QueryString.Keys):
                if len(self.Page.Request.QueryString['Loc']) > 2 :      # even if Loc = '0|' or 'de|41836' the location is not representing a postcode-area
                    self.param['Loc'] = self.Page.Request.QueryString['Loc']

            if ('Tags' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['Tags'] != ',' :       # if no Tags were send we get ','. dont ask why :-)
                    self.param['Tags'] = self.Page.Request.QueryString['Tags']

            if ('SrchMd' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['SrchMd'] != System.String.Empty:
                    self.param['SrchMd'] = self.Page.Request.QueryString['SrchMd']

            if ('StartDate' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['StartDate'] != System.String.Empty:
                    self.param['StartDate'] = System.Convert.ToDateTime( self.Page.Request.QueryString['StartDate'] )
            if ('EndDate' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['EndDate'] != System.String.Empty:
                    self.param['EndDate'] = System.Convert.ToDateTime( self.Page.Request.QueryString['EndDate'] )

            if self.param['Loc'] !=  None:
                locLst = self.param['Loc'].strip().split('|')
                self.ui.getCtrl( 'sel_country'  ).SelectedValue = locLst[0]
                self.ui.getCtrl( 'txbx_postCode' ).Text = locLst[1]
            if self.param['StartDate']  !=  None: self.ui.getCtrl( 'txbx_timeFrom' ).Text = self.param['StartDate'].ToString('dd.MM.yyyy')
            if self.param['EndDate']    !=  None: self.ui.getCtrl( 'txbx_timeTo'   ).Text = self.param['EndDate'].ToString('dd.MM.yyyy')
            if self.param['Tags']       !=  None: 
                commaPos = self.param['Tags'].find(',')                                         # get the hashtags given by the user found after the first comma
                self.ui.getCtrl( 'txbx_hashtag'  ).Text = self.param['Tags'][commaPos:]
                if commaPos != 0:                                                               # get the rubric-tac. that is the stringpart before the first comma
                    self.ui.getCtrl( 'txbx_tagforitem'  ).Text = self.param['Tags'][:commaPos]
                    # REMEMBER : the hashtag is only written in the hidden txt-box. 
                    #            in future there must be a javascript-function that gets the 
                    #            corresponding tag for the parameter out of the configuration-div

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())




    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    #
    # pgLoad: called from page-load event:       define the display-webform logged in users see the one with comment-editor-fuinctionality
    #                                            gets the hometown of the user in the modal-dialog if logged in 
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def pgLoad( self ):
        try:
            # the link that will be created by javascript depends on loggin-status of the user
            # if logged in he can comment an item, if not he only can take a look
            url = WebConfigurationManager.AppSettings['AddArticleToDebate']                         # search for debates
            if not self.usrDt.isLoggedIn():
                url = WebConfigurationManager.AppSettings['DetailsForStrangers']                    # use view-detail-dialog for not logged in users
            url += '?item='
            self.ui.findCtrl(self.Page, 'lbl_display_url').Text = '..' + url[1:]

            self.rubricWriteConfToDivs()                # write the rubric-configuration into the divs
            self.insrtUsersHomeTown()                   # if user is logged in his hometown will be p?laced in the modal-dialog location-part
            self.hndlUrlParam()                         # copy the url-parameter we have received into the modal-dialog

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



tool = DebateProjector( Page )  # #   --  #  #   --  #  #   --  #  #   --  #  #   --  #  #   --  #  #   --  #  #   --  #  #   --  #  #   --  #  #   --  #  #   --  #  #   --  #  #   --  #  #   --  #  #   --  #  



# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 07.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    try:
        tool.pgLoad()

    except Exception,e:
        self.log.w2lgError(traceback.format_exc())



