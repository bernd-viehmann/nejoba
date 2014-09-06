#
# job_search.aspx.py  :  define the search-pattern and redirect to joblist
#
#
#
from System.Web.Configuration import *
from System import UriPartial
import System
import traceback
import mongoDbMgr                               # father : the acces to the database

tool = mongoDbMgr.mongoMgr(Page)
srchPtrn = {}

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

        if (not Page.IsPostBack):
            # if webform was called with param mode=tagg the redirect will go to the hashtagg-definition-webform : topic_set_tagging.aspx
            # if webform was called with param mode=findFreetag the redirect will go to the find-free-hashtagg : topic_display_taggs.aspx

            mode = Page.Request.QueryString['mode'] 
            if mode is not None:
                Page.ViewState['MODE'] = mode

            # save the key; will be send to the next webform !!
            rubric = Page.Request.QueryString['key'] 
            if rubric is not None:
                if len(rubric) < 25:
                    Page.ViewState['RUBRIC'] = rubric
                    # tool.log.w2lgDvlp('define_locationa.aspx.py->Page_Load : '+ unicode(rubric) )

            # save the key; will be send to the next webform !!
            rubricName = Page.Request.QueryString['name'] 
            if rubricName is not None:
                if len(rubricName) < 25:
                    Page.ViewState['RUBRIC_NAME'] = rubricName
                    # tool.log.w2lgDvlp('define_locationa.aspx.py->Page_Load : '+ unicode(rubric) )

            # this is a public webpage !!
            # fill country-dropdown
            selCountries = tool.ui.getCtrl('sel_country')
            tool.fillCountryList( selCountries, 'DE' )

            # insert location-data of currently logged in user
            if tool.usrDt.isLoggedIn():
                usrCntry = tool.usrDt.getItem('countrycode').ToString()
                usrPstcd = tool.usrDt.getItem('postcode').ToString()
                selCountries.SelectedValue = usrCntry
                plzTxtBx = tool.ui.getCtrl('txbx_postCode')
                plzTxtBx.Text = usrPstcd

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ***********************************************************************************************************************************************
# HndlrStartSearch : handler for the button to start a search.
#
# 18.03.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def HndlrStartSearch(sender, e):
    try:
        if checkInputOk() is not True: return           # check valid input

        urlNext = None  

        # if postcode was selected in the dropdown use the selection
        postCodeSelector = tool.ui.getCtrl('sel_mulitPostCode')
        if len(postCodeSelector.Items) > 0 and (postCodeSelector.SelectedIndex > 0):
            # get the monog_id in geo-cache for selection
            srchPtrn['locationId'] = postCodeSelector.SelectedValue.strip()
            postcode = postCodeSelector.SelectedItem.Text.strip()
            tool.ui.getCtrl('txbx_postCode').Text = str(postcode)
            tool.log.w2lgDvlp('job_search.aspx.py->HandlerButton: Location-ID choosen by sel_mulitPostCode : ' + srchPtrn['locationId'] + ' PostCode = : ' + str(postcode) )

        # if there is nothing in the postcode-selector use the text-input in txbx_postCode
        else:
            postcode = tool.ui.getCtrl('txbx_postCode').Text.strip()
            if len(postcode) > 0 :
                reslt = FindByPostCode()
                srchPtrn['locationId'] = reslt[0]
                srchPtrn['cityname']  = reslt[1]
                tool.ui.getCtrl('txb_cityname').Text = srchPtrn['cityname']
                tool.log.w2lgDvlp('job_search.aspx.py->HandlerButton: Location-ID found with FindByPostCode() : ' + srchPtrn['locationId'] )

        
        if not srchPtrn.has_key('locationId'): findByCity()         # if no postcode given try to load the country by its name and set a value in srchPtrn['pstcode']
        if not srchPtrn.has_key('locationId'): return               # if no postcode was found abort the computation
        createPlaceList()                                           # create array with the place-ids from user input

        rubric = ''
        if Page.ViewState['RUBRIC'] is not None:
            rubric = '&key=' + Page.ViewState['RUBRIC'].ToString()
            rubric += '&name=' + Page.ViewState['RUBRIC_NAME'].ToString()

            # create location-name from edits
            postCode = ''
            cntryCode = ''
            if tool.ui.getCtrl('PostCodeSelect').Visible == True:
                postCode = tool.ui.getCtrl('sel_mulitPostCode').SelectedItem.Text.strip()
            else:
                postCode = tool.ui.getCtrl('txbx_postCode').Text

            cntryCode = tool.ui.getCtrl('sel_country').SelectedValue
            urlPrm = '?loc=' + cntryCode + '|' + postCode + rubric
            urlNext = Page.ResolveUrl(WebConfigurationManager.AppSettings['ShowFromUrl']) + urlPrm

        elif Page.ViewState['MODE'] is not None:
            if Page.ViewState['MODE'] == 'tagg':
                # create location-name from edits
                postCode = ''
                cntryCode = ''
                if tool.ui.getCtrl('PostCodeSelect').Visible == True:
                    postCode = tool.ui.getCtrl('sel_mulitPostCode').SelectedItem.Text.strip()
                else:
                    postCode = tool.ui.getCtrl('txbx_postCode').Text

                cntryCode = tool.ui.getCtrl('sel_country').SelectedValue
                urlPrm = '?loc=' + cntryCode + '|' + postCode
                urlNext = Page.ResolveUrl(WebConfigurationManager.AppSettings['DisplayHashTaggs']) + urlPrm

            elif Page.ViewState['MODE'] == 'findFreetag':

                urlNext = Page.ResolveUrl(WebConfigurationManager.AppSettings['DisplayHashTaggs']) + urlPrm









    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())

    if urlNext != None :
        Response.Redirect( Page.ResolveUrl( urlNext ) ) 


# ***********************************************************************************************************************************************
# findByCity : there is only the name of the city available. function gets postcode from it 
#                   
# param : dict with search-parameter
#
# 07.01.2013    berndv  initial realese
# ***********************************************************************************************************************************************
def findByCity():
    try:
        tool.log.w2lgDvlp('job_search.aspx.py->findByCity tries to get postcode from city-name !')

        cntry   = tool.ui.getCtrl('sel_country').SelectedValue
        city    = tool.ui.getCtrl('txb_cityname').Text.strip()
        pstcodeFromCity = tool.geoSrc.getRowsForCity( cntry, city )

        tool.log.w2lgDvlp('job_search.aspx.py->findByCity : number of found postcodes :  ' + str( len(pstcodeFromCity) ) )

        if len(pstcodeFromCity) == 0:
            # system has not found an matching postcode for cityname
            tool.log.w2lgDvlp('job_search.aspx.py->findByCity : city unknown' + unicode(city) + ' ' + unicode(cntry))
            tool.errorMessage(tool.ui.getCtrl('msg_unknownPostCode').Text)
            
        elif len(pstcodeFromCity) == 1:
            # found exactly one plz for given placename: can be used srchPtrn['pstcode'] will be set
            tool.log.w2lgDvlp('job_search.aspx.py->findByCity : city found :'+ unicode(city) + ' ' + unicode(cntry))

            srchPtrn['locationId'] = pstcodeFromCity[0][0]
            srchPtrn['postcode']= pstcodeFromCity[0][1].ToString()
            tool.ui.getCtrl('txbx_postCode').Text = srchPtrn['postcode']

            tool.ui.getCtrl('PostCodeText').Visible = True
            tool.ui.getCtrl('PostCodeSelect').Visible = False

        elif len(pstcodeFromCity) > 1:
            # if more than one postcode was found show a drop-down to select the wanted one
            tool.log.w2lgDvlp('job_search.aspx.py->findByCity : more than one city found :'+ unicode(city) + ' ' + unicode(cntry))

            tool.ui.getCtrl('PostCodeText').Visible = False
            tool.ui.getCtrl('PostCodeSelect').Visible = True
            tool.ui.getCtrl('sel_country').Enabled = False 
            tool.ui.getCtrl('txb_cityname').Enabled = False

            drpDwn = tool.ui.getCtrl('sel_mulitPostCode')
            for item in pstcodeFromCity:
                lstItem = System.Web.UI.WebControls.ListItem(unicode(item[1]),unicode(item[0]))
                drpDwn.Items.Add(lstItem)
            # add 'header' to drop-down in a language-independent manner
            startItm = tool.ui.getCtrl('msg_pleaseSelPostCode').Text
            drpDwn.Items.Insert( 0, startItm )

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())



# ***********************************************************************************************************************************************
# FindByPostCode : get the mongo_id of a location by the countrycode|postcode-information
#                   
# param : dict with search-parameter
#
# 07.01.2013    berndv  initial realese
# ***********************************************************************************************************************************************
def FindByPostCode():
    try:
        cntry   = tool.ui.getCtrl('sel_country').SelectedValue
        pstCd   = tool.ui.getCtrl('txbx_postCode').Text.strip()

        # result will be 'MongoId|PlaceName'
        rslt = tool.geoSrc.findIdByPostCode( cntry, pstCd )

        if rslt == 'not found':
            # throw error-messsage
            pass
        else:
            arr = rslt.split('|')
            return arr[0]

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())



# ***********************************************************************************************************************************************
# createPlaceList : user has gave aus a country-code and a post-code. this will be the middle of his service-area where he can check be active
#                   this function generates a list with the ids of all cities that are inside the area-size that is configured in web.config area-size
#
#                   the list will contain the ids of the cities that are of interest
#                   
#
# 08.12.2012    berndv  initial realese
# ***********************************************************************************************************************************************
def createPlaceList():
    try:
        tool.log.w2lgDvlp('job_search.aspx.py->createPlaceList creating a array with the places that belong to the input !')

        areaSize = WebConfigurationManager.AppSettings["areaSize"];
        postcd  = tool.ui.getCtrl('txbx_postCode').Text.strip()
        city    = tool.ui.getCtrl('txb_cityname').Text.strip()
        cntry   = tool.ui.getCtrl('sel_country').SelectedValue
        places  = tool.geoSrc.getPlacesByPostcode( cntry.ToString(), postcd.ToString(), areaSize.ToString() )


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
        #    tool.log.w2lgDvlp('getPlacesByPostcode item to append ' + unicode(newItem[4]) + '   ' + unicode(newItem[5]) + ' - distance : ' + unicode(newItem[8]) )

        srchPtrn.Add( 'cities', places )

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ***********************************************************************************************************************************************
# checkInputOk() : checks user input 
#                  
#
# 29.12.2012    berndv  initial realese
# ***********************************************************************************************************************************************
def checkInputOk():
    try:
        # item 0 in post-code dropdown selcted : must be >= 1
        postCodeSelector = tool.ui.getCtrl('sel_mulitPostCode')
        if len(postCodeSelector.Items) > 0 and (postCodeSelector.SelectedIndex < 1 ):
            tool.log.w2lgDvlp('item 0 selected in sel_mulitPostCode')
            tool.errorMessage( tool.ui.getCtrl('msg_pleaseSelPostCode').Text )
            return False

        return True

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
