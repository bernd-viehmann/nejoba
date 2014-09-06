#  
#  projector_DebateMap is the main-map that is also used as default-page
#  
#  
#  
#  
#  
#
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
import codecs
import mongoDbMgr                   # father : the acces to the database
from srvcs.tls_UiHelper import LocDefiner

# from srvcs.tls_WbFrmClasses import MapProjector




# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
#
# helper for ~/projector_DebateMap : THE card showing stuff
#  
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -

class LOCALMapProjector ( mongoDbMgr.mongoMgr ):
    '''
    MapProjector is the helper-class for the main-map webform
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
            self.ui.getCtrlTree( self.Page )
            self.lcDfnr = LocDefiner( page )                # the helper class for location-stuff

            self.log.w2lgDvlp('LOCALMapProjector( .. ) constructor called')

            self.param = {}                                                 # the URL-parameters are stored in member-attribute param = {}
            #self.param.Add('ItemType', None)
            #self.param.Add('SliceActive', None)
            #self.param.Add('CrsCmd', None)
            #self.param.Add('ResultLength', None)

            self.param.Add('Loc', None)
            self.param.Add('City', None)
            self.param.Add('Tags', None)
            self.param.Add('SrchMd', None)
            self.param.Add('StartDate', None)
            self.param.Add('EndDate', None)


            # the link that will be created by javascript depends on loggin-status of the user
            # if logged in he can comment an item, if not he only can take a look
            url = WebConfigurationManager.AppSettings['AddArticleToDebate']                         # search for debates
            if not self.usrDt.isLoggedIn():
                url = WebConfigurationManager.AppSettings['DetailsForStrangers']                    # use view-detail-dialog for not logged in users

            url += '?item='
            self.ui.findCtrl(self.Page, 'lbl_display_url').Text = '.' + url[1:]

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    #
    # user_interface_functions
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def pgLoad( self ):
        try:
            # 01.12.2013 fill the country-select box
            cntrySel = self.ui.getCtrl('sel_country')
            cntrySel.Items.Clear()
            self.lcDfnr.uiFillCtrySlct(cntrySel)

            # copy the URL-parameter into local dict if available
            if len(self.Page.Request.QueryString) > 0 : 
                self.storeUrlParams()

            self.insrtLocConfg()

            # 01.12.2013  OBSOLETE : LocDefiner is used now
            ## but if we have location-definition in the URL-parameter use that
            #if self.param['Loc'] !=  None:
            #    locLst = self.param['Loc'].strip().split(',')
            #    self.ui.getCtrl( 'sel_country'  ).SelectedValue = locLst[0]
            #    self.ui.getCtrl( 'txbx_postCode' ).Text = locLst[1]
            #if self.param['City'] !=  None :        self.ui.getCtrl( 'txbx_city'   ).Text = self.param['City']

            if self.param['Tags'] !=  None :        self.ui.getCtrl( 'txbx_hashtag').Text = self.param['Tags']
            if self.param['StartDate']  !=  None: self.ui.getCtrl( 'txbx_timeFrom' ).Text = self.param['StartDate'].ToString('dd.MM.yyyy')
            if self.param['EndDate']    !=  None: self.ui.getCtrl( 'txbx_timeTo'   ).Text = self.param['EndDate'].ToString('dd.MM.yyyy')

            ## 17.09.2013 bervie changed for facebook-posts
            #if self.param['Tags'] != None :
            #    placeStrng = 'in' 
            #    if self.ui.getCtrl( 'txbx_postCode' ).Text != '' : placeStrng = ' PLZ: ' + self.ui.getCtrl( 'txbx_postCode' ).Text 
            #    if self.ui.getCtrl( 'txbx_city' ).Text != '' : placeStrng += ' ' + self.ui.getCtrl( 'txbx_city' ).Text
            #    if placeStrng == 'in' : placeStrng = ''
            #    self.Page.Header.Title =  self.param['Tags'].replace(',',' ').upper() + ' ' + placeStrng.upper() + ' auf der nejoba-Karte'
            ## 17.09.2013 bervie end


            # 17.09.2013 bervie changed for facebook-posts ----------------------------------------------------------------------------------------
            if self.param['Tags'] != None :
                placeStrng = 'in'
                if self.ui.getCtrl( 'txbx_postCode' ).Text != '' : placeStrng = ' PLZ: ' + self.ui.getCtrl( 'txbx_postCode' ).Text 
                if self.ui.getCtrl( 'txbx_city' ).Text != '' : placeStrng += ' ' + self.ui.getCtrl( 'txbx_city' ).Text
                if placeStrng == 'in' : placeStrng = ''
                self.Page.Header.Title =  self.param['Tags'].replace(',',' ').upper() + ' ' + placeStrng.upper() + ' auf der nejoba-Karte'
            else:
                if (self.ui.getCtrl( 'txbx_postCode' ).Text != '') or (self.ui.getCtrl( 'txbx_city' ).Text != ''):
                    placeStrng = ''
                    if self.ui.getCtrl( 'txbx_postCode' ).Text != '' : placeStrng = ' PLZ: ' + self.ui.getCtrl( 'txbx_postCode' ).Text 
                    if self.ui.getCtrl( 'txbx_city' ).Text != '' : placeStrng += ' ' + self.ui.getCtrl( 'txbx_city' ).Text
                    self.Page.Header.Title = 'nejoba-Karte :  ' + placeStrng.upper()
            # 17.09.2013 bervie end ----------------------------------------------------------------------------------------------------------------

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())




    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # storeUrlParams 
    # 
    # 02.12.2013  -bervie-  initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def storeUrlParams( self ):
        try:
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

            if ('City' in self.Page.Request.QueryString.Keys):
                if len(self.Page.Request.QueryString['City']) != System.String.Empty:
                    self.param['City'] = self.Page.Request.QueryString['City']

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

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    #
    # insrtUsersData : if user is logged in his hometown will be inserted into the modal-dialog
    #
    # 08.09.2013 bervie if we have url-parameter the hometown of the user should not be inserted. use the query-parameter instead
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def insrtLocConfg( self ):
        try:
            if self.Page.Request.QueryString['Loc'] !=  None:
                locLst = self.param['Loc'].strip().split(',')
                self.ui.getCtrl( 'sel_country'  ).SelectedValue = locLst[0]
                self.ui.getCtrl( 'txbx_postCode' ).Text = locLst[1]
                self.ui.getCtrl('txbx_city').Text = self.param['City']
            else:
                # 01.12.2013 Bervie CR : use the location defined in the LocDefiner
                lctnCnfg = self.lcDfnr.uiInitProjector()

                self.ui.getCtrl('sel_country').SelectedValue = lctnCnfg['COUNTRY']
                self.ui.getCtrl('txbx_city').Text = lctnCnfg['CITY']
                self.ui.getCtrl('txbx_postCode').Text = lctnCnfg['POSTCODE']
                # 01.12.2013 Bervie CR : use the location defined in the LocDefiner
                return 

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())






















# tool = MapProjector( Page )
tool = LOCALMapProjector( Page )




# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 07.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    try:
        # add javascript to handle change of a country
        cntryDrpDwn = tool.ui.getCtrl('sel_country')
        cntryDrpDwn.Attributes.Add("onChange", "return countrySelectChanged();") 

        tool.pgLoad()

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())

