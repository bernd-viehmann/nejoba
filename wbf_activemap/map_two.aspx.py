#  
#  MapTwo is the main-map that is also used as default-page
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




class MapTwo ( mongoDbMgr.mongoMgr ):
    '''
    MapTwo is the helper-class for the main-map webform
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
            self.log.w2lgDvlp('MapTwo( .. ) constructor called')

            self.param = {}                                                 # the URL-parameters are stored in member-attribute param = {}
            #self.param.Add('ItemType', None)
            #self.param.Add('SliceActive', None)
            #self.param.Add('CrsCmd', None)
            #self.param.Add('ResultLength', None)
            self.param.Add('Loc', None)
            self.param.Add('Tags', None)
            self.param.Add('SrchMd', None)
            self.param.Add('StartDate', None)
            self.param.Add('EndDate', None)

            # 10.08.2013 bervie switched to UI-Helper for rubric loading
            ## loads EVENT sources ( items with a date-definition )
            #tmpltPath = self.Page.Server.MapPath( WebConfigurationManager.AppSettings['EventMatrixDefinition'] )
            #f = codecs.open(tmpltPath, "r", "utf-8")
            #activitySource = f.read()
            #f.close()
            #actvities = self.ui.findCtrl(self.Page, 'date_event_div')
            #actvities.InnerHtml = activitySource

            ## loads LOCATION sources ( items with a date-definition )
            #tmpltPath = self.Page.Server.MapPath( WebConfigurationManager.AppSettings['LocationMatrixDefinition'] )
            #f = codecs.open(tmpltPath, "r", "utf-8")
            #activitySource = f.read()
            #f.close()
            #actvities = self.ui.findCtrl(self.Page, 'location_div')
            #actvities.InnerHtml = activitySource

            ## loads EVENT sources ( items with a date-definition )
            #tmpltPath = self.Page.Server.MapPath( WebConfigurationManager.AppSettings['AnnonceMatrixDefinition'] )
            #f = codecs.open(tmpltPath, "r", "utf-8")
            #activitySource = f.read()
            #f.close()
            #actvities = self.ui.findCtrl(self.Page, 'annonce_div')
            #actvities.InnerHtml = activitySource

            ## loads EVENT sources ( items with a date-definition )
            #tmpltPath = self.Page.Server.MapPath( WebConfigurationManager.AppSettings['InitiativeMatrixDefinition'] )
            #f = codecs.open(tmpltPath, "r", "utf-8")
            #activitySource = f.read()
            #f.close()
            #actvities = self.ui.findCtrl(self.Page, 'initiative_div')
            #actvities.InnerHtml = activitySource

            ## loads EVENT sources ( items with a date-definition )
            #tmpltPath = self.Page.Server.MapPath( WebConfigurationManager.AppSettings['BusinessMatrixDefinition'] )
            #f = codecs.open(tmpltPath, "r", "utf-8")
            #activitySource = f.read()
            #f.close()
            #actvities = self.ui.findCtrl(self.Page, 'business_div')
            #actvities.InnerHtml = activitySource

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

            # the link that will be created by javascript depends on loggin-status of the user
            # if logged in he can comment an item, if not he only can take a look
            url = WebConfigurationManager.AppSettings['AddArticleToDebate']                         # search for debates
            if not self.usrDt.isLoggedIn():
                url = WebConfigurationManager.AppSettings['DetailsForStrangers']                    # use view-detail-dialog for not logged in users
            url += '?item='
            self.ui.findCtrl(self.Page, 'lbl_display_url').Text = '..' + url[1:]

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())




    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    #
    # user_interface_functions
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def pgLoad( self ):
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

            # 10.08.2013 predefine hometown of user if he is logged in . . .. . .. .. .
            self.insrtUsersHomeTown()
            
            # but if we have location-definition in the URL-parameter use that
            if self.param['Loc'] !=  None:
                locLst = self.param['Loc'].strip().split('|')
                self.ui.getCtrl( 'sel_country'  ).SelectedValue = locLst[0]
                self.ui.getCtrl( 'txbx_postCode' ).Text = locLst[1]

            if self.param['Tags'] !=  None :        self.ui.getCtrl( 'txbx_hashtag'  ).Text = self.param['Tags']
            if self.param['StartDate']  !=  None: self.ui.getCtrl( 'txbx_timeFrom' ).Text = self.param['StartDate'].ToString('dd.MM.yyyy')
            if self.param['EndDate']    !=  None: self.ui.getCtrl( 'txbx_timeTo'   ).Text = self.param['EndDate'].ToString('dd.MM.yyyy')


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



tool = MapTwo( Page )




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

