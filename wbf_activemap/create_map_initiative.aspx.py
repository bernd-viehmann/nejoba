# create_map_initiative.aspx.py
#
# create or edit an initiative. they are stored in the collection 
#  
#  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  
#   available types of initiatives
#
#   Gemeinschaften und Kommunen                     communities                   http://maps.google.com/mapfiles/marker_grey.png
#   Politik und Justiz                              politics                      http://maps.google.com/mapfiles/marker_orange.png
#   regionales Geld / Wirtschaft                    monetary                      http://maps.google.com/mapfiles/marker_black.png
#   Tauschen und Schenken                           giveandswap                   http://maps.google.com/mapfiles/marker_purple.png
#   nachhaltige Unternehmen                         sustainable_business          http://maps.google.com/mapfiles/marker_black.png
#   alternative Landwirtschaft / Urban Gardening    agriculture                   http://maps.google.com/mapfiles/marker_green.png
#   Umwelt- und Tierschutz                          environmental                 http://maps.google.com/mapfiles/marker_green.png
#   sonstige B?rgerinitiativen                      initiatives                   http://maps.google.com/mapfiles/marker_yellow.png
#   Hilfsorganisationen                             charities                     http://maps.google.com/mapfiles/marker_white.png
#   Vereine und Selbsthilfegruppen                  associations                  http://maps.google.com/mapfiles/marker_yellow.png
#  
#  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  
#
#  
from System.Web.Configuration import *
import traceback                                    # for better exception understanding
import mongoDbMgr                                   # father : the acces to the database
import System.Text
from System.Net.Mail import *
from System.Net import NetworkCredential 
import re

tool = mongoDbMgr.mongoMgr( Page )


# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 02.06.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    try:
        # hide the main-user-interface after a button-click and show  a please-wait sedativ
        tool.ui.hideFormAfterClick()
        tool.errorMessage('')

        # if user is logged_in use edit-mode for enable change of user_data
        if not IsPostBack:
            # user must be logged in
            tool.usrDt.checkUserRigths( Page, 'free')

            # check if we have to edit or create an item
            if Page.Request.QueryString['initiative'] != None :
                initvId = Page.Request.QueryString['initiative']
                loadExistingItem(initvId)

            else:
                pass

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())



# ***********************************************************************************************************************************************
# HndlrButtonClick    : handler for button-click-events. chose button by ID
#
# 02.06.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def HndlrButtonClick(sender, e):
    try:
        url = None

        if sender.ID == 'btn_Create':
            # tool.log.w2lgDvlp('der schickma buttton wurde gerade gedr?ckt')
            if checkNumberOfItems():
                saveItemFromUI()
            else:
                tool.errorMessage('Die Anzahl der möglichen Initiativen die mit einem Benutzerkonto <br />erstellt werden können hast du erreicht.')

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return

    if url != None :
        Response.Redirect(urlNext)



# ***********************************************************************************************************************************************
# loadExistingItem  : load an existing item from the database and put it in the UI
#
# 02.06.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def loadExistingItem( initiativeId ):
    try:
        # load the data from the mongo-db
        collectionName  = 'initiatives.final'
        selectKey       = '_id'
        selectValue     = initiativeId

        readCfg = {'collection':collectionName, 'slctKey':selectKey, 'slctVal':selectValue}
        tool.readDoc(readCfg)
        result = readCfg['data']

        # add the kind of the initiative (needed to select a corresponding marker
        marker = result['type']
        tool.ui.getCtrl('drpd_item_type').SelectedValue = marker.ToString()
        del result['type']

        # set the country from data
        tool.ui.getCtrl('drpd_country').SelectedValue = result['country_code'].ToString()
        del result['country_code']
        
        # data that can not be found in the dictionary
        del result['creator_GUID']           # remove the creator identifier
        del result['_id']                    # remove the mongo_id
        del result['marker']                 # remove the selected value from the dropdown
        del result['marker_line']            # remove the line created for the map-vector-layer
        del result['location_key']           # remove 'de|41836'

        # .....and put the data into the edits
        tool.ui.getCtrlTree( Page )
        for itm in result.keys():
            tool.log.w2lgDvlp('create_map_initiative.aspx.py->loadExistingItem : found : ' + str(itm) )
            if itm is not None : tool.ui.getCtrl( itm ).Text = result[itm].ToString()


    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return



# ***********************************************************************************************************************************************
# checkNumberOfItems  : check the number of initiatives that are already created by the user
#
# 02.06.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def checkNumberOfItems():
    try:
        collectionName  = 'initiatives.final'
        selectKey       = 'creator_GUID'
        selectValue     = tool.usrDt.getItem('GUID')

        readCfg = {'collection':collectionName, 'slctKey':selectKey, 'slctVal':selectValue}
        amountOfFoundItems = tool.slctDocs(readCfg)
        result = readCfg['data']
        tool.log.w2lgDvlp('create_map_initiative.aspx.py->checkNumberOfItems : number of items found for user : ' + str( amountOfFoundItems ) )

        # number of allowed inserts for a single user
        maximum = System.Convert.ToInt16( WebConfigurationManager.AppSettings['MaxOfInitiativesForOneUser'] )

        if amountOfFoundItems >= maximum:
            return False
        else:
            return True


    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return



# ***********************************************************************************************************************************************
# loadExistingItem  : load an existing item from the database and put it in the UI
#
# 02.06.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def saveItemFromUI():
    try:
        inpt = {}
        tool.ui.getCtrlTree( Page )

        # if no pict was given use the anonymous standart picture
        inpt['txbx_picturl'] = tool.ui.ctrlDict['txbx_picturl'].Text[:333]
        if len( inpt['txbx_picturl'].strip() ) < 1:
                anonymusPictUrl = 'http://guikblog.com/wp-content/uploads/2012/08/anonymus-logo-.png'
                #anonymusPictUrl = './img/anonymous_logo_small.png'
                inpt['txbx_picturl'] = anonymusPictUrl
        
        for key in tool.ui.ctrlDict.keys():
            if key is not None and key.startswith('txbx_'):
                val = tool.ui.ctrlDict[key].Text[:333].strip()

                if ( val is not None ) and (len(unicode(val)) > 0 ):
                    inpt[key] = val
                    tool.log.w2lgDvlp('create_map_initiative.aspx.py->saveItemFromUI : found : ' + unicode(key) + ' - ' + unicode(val) )

        # add who has created the data
        guid = tool.usrDt.getItem('GUID')
        inpt['creator_GUID'] = guid

        # save selcted country
        countryCode = tool.ui.getCtrl('drpd_country').SelectedValue
        inpt['country_code'] = countryCode

        # add the kind of the initiative (needed to select a corresponding marker
        switcher = { 'communities'          :'http://maps.google.com/mapfiles/marker_grey.png',
                     'politics'             :'http://maps.google.com/mapfiles/marker_orange.png',
                     'monetary'             :'http://maps.google.com/mapfiles/marker_black.png',
                     'giveandswap'          :'http://maps.google.com/mapfiles/marker_purple.png',
                     'sustainable_business' :'http://maps.google.com/mapfiles/marker_black.png',
                     'agriculture'          :'http://maps.google.com/mapfiles/marker_green.png',
                     'environmental'        :'http://maps.google.com/mapfiles/marker_green.png',
                     'initiatives'          :'http://maps.google.com/mapfiles/marker_yellow.png',
                     'charities'            :'http://maps.google.com/mapfiles/marker_white.png',
                     'associations'         :'http://maps.google.com/mapfiles/marker_yellow.png'} 
        type = tool.ui.getCtrl('drpd_item_type').SelectedValue
        inpt['type'] = type
        inpt['marker'] = switcher[type]
        inpt['location_key'] = inpt['country_code'] + '|' + inpt['txbx_postcode']

        createPlaceList()
        inpt['txbx_lat'] = tool.ui.getCtrl('txbx_lat').Text
        inpt['txbx_lon'] = tool.ui.getCtrl('txbx_lon').Text

        inpt['marker_line'] = createMarkerLine( inpt )           # create a line that will be used in the marker-definitions-file

        # try to write a document #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  
        writing = {}
        collectionName  = 'initiatives.final'
        writing.update({'collection':collectionName})
        writing.update({'slctKey':None})
        writing.update({'data' : inpt })
        inserted = tool.insertDoc(writing)


    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return


# ************************************************************************************************************************************************************ MARKER
# ************************************************************************************************************************************************************ MARKER
# ************************************************************************************************************************************************************ MARKER


# ***********************************************************************************************************************************************
# createMarkerLine  : creates the line for the marker-definition-file
#
# 02.06.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def createMarkerLine( input ):
    try:
        # marker-line does not make sense when the lat or long is not set
        if ( 'txbx_lat' not in input.keys() ) or ( 'txbx_lon' not in input.keys() ):
            return ''

        nwLine = System.Text.StringBuilder()        # create a new Line
        htmlPart = createHTML( input )              # get the formated HTML-part for pop-up
        createPlaceList()                           # generate a list with the cities in the neighbourhood
                                                    # and buid random coordinates if needed

        nwLine.Append( input['txbx_lat'] )
        nwLine.Append( ',' )
        nwLine.Append( input['txbx_lon'] )
        nwLine.Append( '\t' )
        nwLine.Append( '<h4>' + input['txbx_nickname'] + '</h4>' )
        nwLine.Append( '\t' )
        nwLine.Append( htmlPart )
        nwLine.Append( '\t' )
        nwLine.Append( input['marker'] )
        nwLine.Append( '\t' )
        nwLine.Append( '20, 34' )
        nwLine.Append( '\t' )
        nwLine.Append( '-10,-33' )
        nwLine.Append( '\n' )

        result = nwLine.ToString()
        tool.log.w2lgDvlp( 'create_map_initiative.aspx.py->createMarkerLine was called : ' + result )
        return result

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return


# ***********************************************************************************************************************************************
# createHTML  : creates the HTML for the marker-popup
#
#param : input : {} with the input from the ui. 
#
# 02.06.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def createHTML( input ):
    try:
        # string is the HTML-TEMPLATE for creating the popup of an item in the map
        popUpHtmlTmplt ='<div><img src="#@#pic_url#@#" class="img-polaroid" style="height: 180px; width: 180px;" alt="Profilbild" /><table class="table table-bordered" style="vertical-align: middle;width: 300px;"><tbody><tr><td colspan="2"><h6>Mitteilung:</h6><p>#@#info#@#</p></td></tr><tr><td colspan="2"><a href="http://www.nejoba.net/njb_02/wbf_topic/parameter_result_list.aspx?loc=#@#forumlocation#@#" target="_blank"><h6>regionales Forum</h6></a></td></tr><!--#@#additional_contact_info#@#--></tbody></table></div>'

        # stuff for creating the HTML-table with the contact-info
        tableAdds =   { 'txbx_forename'         : 'Vorname :',
                        'txbx_familyname'       : 'Zuname :',
                        'txbx_email'            : 'Mail :',
                        'txbx_postcode'         : 'PLZ :',
                        'txbx_city'             : 'Stadt :',
                        'txbx_street'           : 'Strasse :',
                        'txbx_housenumber'      : 'Hausnummer :',
                        'txbx_adress_add'       : 'Adr.-Zusatz :',
                        'txbx_mobile'           : 'Handy-Nr. :',
                        'txbx_phone'            : 'Telefon-Nr. :',

                        'txbx_website'          : 'Webseite :',
                        'txbx_socialnetwork'    : 'Soziales Netzwerk :',
                        'txbx_twitter'          : 'Twitter-Konto :',
                        'txbx_skype'            : 'Skype-Konto :',

                        'txbx_hashtag'          : 'Hashtag :' }

        tblRowTmplt = '<tr><td><strong>#@#dict_key#@#</strong></td><td>#@#dict_val#@#</td></tr>'        # the tmplate-string to create a single row in the container
        # will be added to the main-table
        # 'txbx_info'             : '',
        # 'txbx_email'            : '',
        #
        # link to nejoba-forum example with tag
        # http://www.nejoba.net/njb_02/wbf_topic/parameter_result_list.aspx?loc=DE%7C41836&tags=kinder&srchMd=OR
        #
        # 'country_code'
        # |
        # 'txbx_postcode'

        # create the additional table-stuff
        bldr = System.Text.StringBuilder()
        for dctKy in tableAdds.keys():
            if dctKy in input:
                if len( input[ dctKy ].ToString().strip() ) > 0:
                    newItm = tblRowTmplt
                    newItm = newItm.replace( '#@#dict_key#@#', tableAdds[ dctKy ] )
                    newItm = newItm.replace( '#@#dict_val#@#',     input[ dctKy ] )
                    bldr.Append( newItm )

        # create the main-div to build the marker-popup HTML
        popUpHtmlTmplt = popUpHtmlTmplt.replace( '<!--#@#additional_contact_info#@#-->' , bldr.ToString() )
        popUpHtmlTmplt = popUpHtmlTmplt.replace( '#@#pic_url#@#'        , input[ 'txbx_picturl' ] )
        popUpHtmlTmplt = popUpHtmlTmplt.replace( '#@#info#@#'           , input[ 'txbx_info' ] )
        forumLoc = input[ 'country_code'] + '|' + input[ 'txbx_postcode' ]
        popUpHtmlTmplt = popUpHtmlTmplt.replace( '#@#forumlocation#@#'  , forumLoc )

        return popUpHtmlTmplt

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return



# ***********************************************************************************************************************************************
# createPlaceList : user has gave aus a country-code and a post-code. this will be the middle of his service-area where he can check be active
#                   this function generates a list with the ids of all cities that are inside the area-size that is configured in web.config area-size
#
#                   the list will contain the ids of the cities that are of interest
#                   
#
# 08.12.2012    berndv  initial realese
# 07.01.2013    bervie  changed getPlacesByPostcode
#                       function now returns all data than only a part. the index has changed
#                       cities.Add(item[0]) to cities.Add(item[1])
#
# ***********************************************************************************************************************************************
def createPlaceList():
    try:
        # tool.log.w2lgDvlp('CreateMapUser.createPlaceList creating a array with the places that belong to this account !!')
        key = 'areasize'
        value = WebConfigurationManager.AppSettings['areaSize']
        tool.usrDt.userDict[ key ] = value

        areaSize        = tool.usrDt.userDict['areasize']
        countryCode     = tool.ui.getCtrl('drpd_country').SelectedValue
        postCode        = tool.ui.getCtrl('txbx_postcode').Text

        tool.log.w2lgDvlp('create_map_initiative - createPlaceList : areaSize        = ' + areaSize)
        tool.log.w2lgDvlp('create_map_initiative - createPlaceList : countryCode     = ' + countryCode)
        tool.log.w2lgDvlp('create_map_initiative - createPlaceList : postCode        = ' + postCode )

        # get an sorted array with the service-area of the user and store it into the usr-session
        places = tool.geoSrc.getPlacesByPostcode( countryCode, postCode, areaSize )

        cities = []
        for item in places:
            cities.Add(item[1])

        # if no cities were found abort insert
        if len(cities) == 0:
            errStr = tool.ui.getCtrl('msg_unknownPlace').Text 
            tool.errorMessage(errStr)
            return
        else:
            tool.usrDt.addNewItem('cities', cities)


            # 21.05.2013 add the coordinates for the marker in the map ------------------------------------------------------------------------
            # 'latitude'               6
            # 'longitude'              7
            hometown = places[0]
            lat = float(hometown[5])
            lon = float(hometown[6])
                
            applyGeoCoords(lat,lon)
                

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())



# **********************************************************************************************************************************************************************************************************************************************************************************************
# applyGeoCoords : store the coordinates for the item. if we have no user input the function will create a random-point.
#
# param : lat    : the geographical latitude
#         lon    : the geographical longitude
#
# returns nothing
#
# 31.05.2013    bervie  initial realese
# ***********************************************************************************************************************************************
def applyGeoCoords( lat, lon ):
    try:
        rndDstnc = float( WebConfigurationManager.AppSettings['mapRndDistance'] )

        # check if the input for lat and long are floats
        if (re.match("^\d+?\.\d+?$", tool.ui.getCtrl('txbx_lat').Text )) and (re.match("^\d+?\.\d+?$", tool.ui.getCtrl('txbx_lon').Text ) is not None) : return

        point = tool.geoSrc.getRandomPoint( lat, lon, rndDstnc )
        tool.ui.getCtrl('txbx_lat').Text = str( point.lat )
        tool.ui.getCtrl('txbx_lon').Text = str( point.lon )

        # write it to the log for deverloping aid
        tool.log.w2lgDvlp('CreateMapUser.applyGeoCoords added marker coordinates by random function in self.geoSrc.getRandomPoint : lat ' + str( point.lat ) + ' - long: ' + str( point.lon ) )

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


