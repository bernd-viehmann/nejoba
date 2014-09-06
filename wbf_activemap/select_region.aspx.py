#
# Select Region is the webform to center the map to some given coords.
# the card will be called with the lat/long values and the country|postcode String as URL-parameter
# and the it will be centered there
#
#
#
#from System.Web.Configuration import *
#import System
#import traceback                                    # for better exception understanding
#import mongoDbMgr                                   # father : the acces to the database



from System.Web.Configuration import *
import System
import System.Text
import System.Guid
import re
import clr
clr.AddReference('MongoDB.Bson')
clr.AddReference('MongoDB.Driver')
from MongoDB.Bson import *
from MongoDB.Driver import *
from System.Net import *
from System.Net.Mail import *
from System import UriPartial
import traceback                                # for better exception understanding
import random
import mongoDbMgr                               # father : the acces to the database


# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
#
# helper for logIn.aspx.py : the form used to log-in or to change to the account-creation-webform
#  
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -

class SelectRegion( mongoDbMgr.mongoMgr ):
    # ***********************************************************************************************************************************************
    # constructor : the class is the tool for the OinBoard webform
    #
    # 18.04.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def __init__(self, pg):
        try:
            mongoDbMgr.mongoMgr.__init__(self, pg)      # wake up papa ; mother njbTools is included by inheritance!
            self.ui.getCtrlTree( self.Page.Master )
            self.log.w2lgDvlp('constructor of class ConfirmUser(Page) aufgefufen!')

            # helper dict to store the parameter 
            self.srchPtrn = {}

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -


    # ***********************************************************************************************************************************************
    # HndlrStartSearch : handler for the button to display the list of matching results.
    #
    # 18.04.2013  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def HndlrStartSearch(self, sender, e):
        try:
            if self.checkInputOk() is not True: return           # check valid input

            urlNext = None  

            # if postcode was selected in the dropdown use the selection
            postCodeSelector = self.ui.getCtrl('sel_mulitPostCode')
            if len(postCodeSelector.Items) > 0 and (postCodeSelector.SelectedIndex > 0):
                # get the monog_id in geo-cache for selection
                self.srchPtrn['locationId'] = postCodeSelector.SelectedValue.strip()
                postcode = postCodeSelector.SelectedItem.Text.strip()
                self.ui.getCtrl('txbx_postCode').Text = str(postcode)
                self.log.w2lgDvlp('job_search.aspx.py->HandlerButton: Location-ID choosen by sel_mulitPostCode : ' + self.srchPtrn['locationId'] + ' PostCode = : ' + str(postcode) )

            # if there is nothing in the postcode-selector use the text-input in txbx_postCode
            else:
                postcode = self.ui.getCtrl('txbx_postCode').Text.strip()
                if len(postcode) > 0 :
                    reslt = self.FindByPostCode()

                    # 05.05.2013 check if the system found a location. if None there was nothing 
                    if reslt == None:
                        errStr = self.ui.getCtrl('msg_unknownPostCode').Text 
                        self.errorMessage(errStr)
                        return

                    self.srchPtrn['locationId'] = reslt[0]
                    self.srchPtrn['cityname']  = reslt[1]
                    self.ui.getCtrl('txb_cityname').Text = self.srchPtrn['cityname']
                    self.log.w2lgDvlp('job_search.aspx.py->HandlerButton: Location-ID found with FindByPostCode() : ' + self.srchPtrn['locationId'] )

            if not self.srchPtrn.has_key('locationId'): self.findByCity()                # if no postcode given try to load the country by its name and set a value in srchPtrn['pstcode']
            if not self.srchPtrn.has_key('locationId'): return                           # if no postcode was found abort the computation

            self.createPlaceList()                                                  # create array with the place-ids from user input
            locStrng = self.ui.getCtrl('sel_country').SelectedValue
            locStrng += '|'
            locStrng += self.ui.getCtrl('txbx_postCode').Text.strip()
            urlNext = WebConfigurationManager.AppSettings['RootDirMap'] + '?loc=' + locStrng

            return urlNext

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # ***********************************************************************************************************************************************
    # findByCity : there is only the name of the city available. function gets postcode from it 
    #                   
    # param : dict with search-parameter
    #
    # 18.04.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def findByCity(self):
        try:
            self.log.w2lgDvlp('job_search.aspx.py->findByCity tries to get postcode from city-name !')

            cntry   = self.ui.getCtrl('sel_country').SelectedValue
            city    = self.ui.getCtrl('txb_cityname').Text.strip()
            pstcodeFromCity = self.geoSrc.getRowsForCity( cntry, city )

            self.log.w2lgDvlp('job_search.aspx.py->findByCity : number of found postcodes :  ' + str( len(pstcodeFromCity) ) )

            if len(pstcodeFromCity) == 0:
                # system has not found an matching postcode for cityname
                self.log.w2lgDvlp('job_search.aspx.py->findByCity : city unknown' + unicode(city) + ' ' + unicode(cntry))
                self.errorMessage(self.ui.getCtrl('msg_unknownPostCode').Text)
            
            elif len(pstcodeFromCity) == 1:
                # found exactly one plz for given placename: can be used srchPtrn['pstcode'] will be set
                self.log.w2lgDvlp('job_search.aspx.py->findByCity : city found :'+ unicode(city) + ' ' + unicode(cntry))

                self.srchPtrn['locationId'] = pstcodeFromCity[0][0]
                self.srchPtrn['postcode']= pstcodeFromCity[0][1].ToString()
                self.ui.getCtrl('txbx_postCode').Text = self.srchPtrn['postcode']

                self.ui.getCtrl('PostCodeText').Visible = True
                self.ui.getCtrl('PostCodeSelect').Visible = False

            elif len(pstcodeFromCity) > 1:
                # if more than one postcode was found show a drop-down to select the wanted one
                self.log.w2lgDvlp('job_search.aspx.py->findByCity : more than one city found :'+ unicode(city) + ' ' + unicode(cntry))

                self.ui.getCtrl('PostCodeText').Visible = False
                self.ui.getCtrl('PostCodeSelect').Visible = True
                self.ui.getCtrl('sel_country').Enabled = False 
                self.ui.getCtrl('txb_cityname').Enabled = False

                drpDwn = self.ui.getCtrl('sel_mulitPostCode')
                for item in pstcodeFromCity:
                    lstItem = System.Web.UI.WebControls.ListItem(unicode(item[1]),unicode(item[0]))
                    drpDwn.Items.Add(lstItem)
                # add 'header' to drop-down in a language-independent manner
                startItm = self.ui.getCtrl('msg_pleaseSelPostCode').Text
                drpDwn.Items.Insert( 0, startItm )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # ***********************************************************************************************************************************************
    # FindByPostCode : get the mongo_id of a location by the countrycode|postcode-information
    #                   
    # param : dict with search-parameter
    #
    # 07.01.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def FindByPostCode(self):
        try:
            cntry   = self.ui.getCtrl('sel_country').SelectedValue
            pstCd   = self.ui.getCtrl('txbx_postCode').Text.strip()

            # result will be 'MongoId|PlaceName'
            rslt = self.geoSrc.findIdByPostCode( cntry, pstCd )

            if rslt == 'not found':
                # throw error-messsage
                return None
            else:
                arr = rslt.split('|')
                return arr[0]

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())




    # ***********************************************************************************************************************************************
    # createPlaceList : user has gave aus a country-code and a post-code. this will be the middle of his service-area where he can check be active
    #                   this function generates a list with the ids of all cities that are inside the area-size that is configured in web.config area-size
    #
    #                   the list will contain the ids of the cities that are of interest
    #                   
    #
    # 08.12.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def createPlaceList(self):
        try:
            self.log.w2lgDvlp('PinBoard.py->PinBoard.createPlaceList creating a array with the places that belong to the input !')

            areaSize = WebConfigurationManager.AppSettings["areaSize"];
            postcd  = self.ui.getCtrl('txbx_postCode').Text.strip()
            city    = self.ui.getCtrl('txb_cityname').Text.strip()
            cntry   = self.ui.getCtrl('sel_country').SelectedValue
            places  = self.geoSrc.getPlacesByPostcode( cntry.ToString(), postcd.ToString(), areaSize.ToString() )


            # 'mngId'                  0 
            # 'keyStrng'               1
            # 'keyCity'                2
            # 'countryCode'            3
            # 'postalCode'             4
            # 'placeName'              5
            # 'latitude'               6
            # 'longitude'              7
            # calculated distance      8

            #for newItem in places:
            #    self.log.w2lgDvlp('getPlacesByPostcode item to append ' + unicode(newItem[4]) + '   ' + unicode(newItem[5]) + ' - distance : ' + unicode(newItem[8]) )

            self.srchPtrn.Add( 'cities', places )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # checkInputOk() : checks user input 
    #                  
    #
    # 29.12.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def checkInputOk(self):
        try:
            # item 0 in post-code dropdown selcted : must be >= 1
            postCodeSelector = self.ui.getCtrl('sel_mulitPostCode')
            if len(postCodeSelector.Items) > 0 and (postCodeSelector.SelectedIndex < 1 ):
                self.log.w2lgDvlp('item 0 selected in sel_mulitPostCode')
                self.errorMessage( self.ui.getCtrl('msg_pleaseSelPostCode').Text )
                return False

            return True

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())





tool = SelectRegion( Page )
tool.ui.getCtrlTree( Page.Master )

# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 18.03.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    try:
        # hide the main-user-interface after a button-click and show  a please-wait sedativ
        tool.ui.hideFormAfterClick()
        tool.errorMessage('')

        if not Page.IsPostBack:
            # load countries into the country list
            selCountries = tool.ui.getCtrl('sel_country')
            tool.fillCountryList( selCountries, 'DE' )

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return


# ***********************************************************************************************************************************************
# HndlrButtonClick    : handler for button-click-events. chose button by ID
#
# 18.11.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def HndlrButtonClick(sender, e):
    try:
        urlNext = tool.HndlrStartSearch(sender, e)

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return

    if urlNext != None :
        Response.Redirect( Page.ResolveUrl( urlNext ) )


