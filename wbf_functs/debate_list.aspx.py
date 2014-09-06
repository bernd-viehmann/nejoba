#  debate_list.aspx.py
#
#  show a filterable list of discussions for a location
#  
#  
#  14.01.2013  initial realese
#
#  
import System.Data
import System.Collections
import clr
import traceback                    # for better exception understanding
import mongoDbMgr                   # father : the acces to the database
from System import UriPartial
from srvcs.ctrl_ItemClasses import *

tool = mongoDbMgr.mongoMgr(Page)

searchPattern = Page.Session['SEARCH_PATTERN']
Page.ViewState['SEARCH_PATTERN'] = searchPattern
Page.Session['SEARCH_PATTERN']   = None
search = Page.Request.QueryString['search']

# ### handler ############################################################################################################################################################################################################################################################

# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 07.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    try:
        # hide the main-user-interface after a button-click and show  a please-wait sedativ
        tool.ui.getCtrlTree( Page.Master )
        tool.ui.hideFormAfterClick()

        if not Page.IsPostBack:
            # the webforms debate_list.aspx and jobs_list.aspx can be called from different forrunners
            #
            # 1. the form can be called directly from the main-menue. than the location is given from user-configuration
            #    in that case we have no URL-parameter "search=custom" 
            #    the page_load function must check if user is already logged-in.
            #
            # 2. the user is a visitor. he is not logged in and the webform was called from the search-preselection-webform
            #    the webform has an URL-parameter "search=custom" 
            #    it can be viewed from any visitor. nor user-login check will be peformed
            #
            #    search = Page.Request.QueryString['search']
            #
            if not search:
                tool.usrDt.checkUserRigths( Page, 'free' )

            LoadDataIntoCtrls()
            LoadDebateList()

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ***********************************************************************************************************************************************
# HandlBtnClick   : handler for button-clix
#
# 07.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def HandlBtnClick( sender,e ):
    url = None
    try:
        url = None
        buttonId = sender.ID
        tool.log.w2lgDvlp( 'thing_list->  HandlBtnClick  BUTON pressed : ' + buttonId )

        if 'openDebate' in buttonId:
            # when opening a debate the system goes to the editor for debates: debate_articel_editor.aspx
            # . so use can take action. the debate_editor shows the thread and has a simple text-editor
            clntIdComponents = sender.ClientID.ToString().split('_')
            arrIdx = clntIdComponents[4]
            dbIds = Page.ViewState['IdList']
            listIdx = dbIds[ int(arrIdx) ]
            # tool.log.w2lgDvlp( 'Index  in db-array     : ' + str(arrIdx) )
            # tool.log.w2lgDvlp( 'Index  for cache-table : ' + str(listIdx) )

            url = WebConfigurationManager.AppSettings['AddArticleToDebate']   # search for debates
            if not tool.usrDt.isLoggedIn():
                url = WebConfigurationManager.AppSettings['DetailsForStrangers']   # use view-detail-dialog for not logged in users
            url += '?item=' + listIdx

        elif 'changeLocation' in buttonId:
            # go back to the debate_search-webform to change search-parameter
            # url = Page.Request.Url.GetLeftPart(UriPartial.Authority)
            url = WebConfigurationManager.AppSettings["SearchDebate"] 

        elif 'search' in buttonId:
            # reload list by given settings in the controls
            LoadDebateList()

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())

    if url != None:
        Response.Redirect( Page.ResolveUrl( url ) )




# ### Data-Handling ############################################################################################################################################################################################################################################################


# ***********************************************************************************************************************************************
# LoadDataIntoCtrls   : fill controlls with data
#                       if called from search-webform the session.cache object will be used
#                       else the function uses the locations from the user-session-data-object
#
#
#
# 07.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def LoadDataIntoCtrls():
    try:
        # if url-PARAM search was given the webform loads the list filtered by the settings from debate_search-webform
            
        if search == 'custom' :
            LoadSettingsFromSearch()                            # if no param given the function loads the settings for the logged in user
        else:
                tool.usrDt.checkUserRigths(Page, 'free')           # user-specific search only makes sence if a user is logged - in
                LoadLoctnsFromUser()                               # get data from the user-session-cache-data

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ***********************************************************************************************************************************************
# LoadSettingsFromSearch   : get the settings for filtering the list from the session-var published by "search"-webform
#
# 08.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def LoadSettingsFromSearch():
    try:
        # get data from the SEARCH_PATTERN 
        drpDwn = tool.ui.getCtrl('sel_lctn')
        for cityRow in searchPattern['cities']:
            itmText = cityRow[3].ToString() + ' ' + cityRow[4].ToString() + '     [' + cityRow[2].ToString() + ']'          # 41836 Hueckelhoven [DE]
            itmVal = cityRow[1].ToString()                                                                                  # mongo_id
            lstItem = System.Web.UI.WebControls.ListItem( itmText, itmVal )
            # tool.log.w2lgDvlp( 'thing_list->LoadLoctnsFromUser adding to sel_lctn DropDownBox   : ' + itmText + ' - ' + itmVal )
            drpDwn.Items.Add( lstItem )

        # put hashtags in the edit
        hashTags = searchPattern['hashtags']
        tool.ui.getCtrl('txb_hashtags').Text = hashTags

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ***********************************************************************************************************************************************
# LoadLoctnsFromUser   : get the locations from user-session-data and write it into the drop-down-box
#
# 07.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def LoadLoctnsFromUser():
    try:
        drpDwn = tool.ui.getCtrl('sel_lctn')
        cities = tool.usrDt.userDict['cities']

        for item in cities:
            mongoId = item.ToString()
            rowFnd = tool.geoSrc.locTable.Rows.Find(mongoId)
            itmText = rowFnd[3].ToString() + ' ' + rowFnd[4].ToString() + '     [' + rowFnd[2].ToString() + ']'          # 41836 Hueckelhoven [DE]
            itmVal =  rowFnd[1].ToString()                                                                                  # mongo_id
            lstItem = System.Web.UI.WebControls.ListItem( itmText, itmVal )
            drpDwn.Items.Add( lstItem )
            # tool.log.w2lgDvlp( 'debate_list->LoadLoctnsFromUser try to load locations for ' + itmText.ToString() + ' - ' + itmVal.ToString() )

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ***********************************************************************************************************************************************
# LoadDebateList   : load a list with debates filtered by controll-data
#
# 07.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def LoadDebateList():
    try:
        # 1. search-parameter from the UI
        #    locations : get the selected location
        tagTable    = tool.appCch.dtSt.Tables["itemTags"]
        itemTable   = tool.appCch.dtSt.Tables["items"]
        resultTble  = itemTable.Clone()
        minAmount = System.Convert.ToInt16( WebConfigurationManager.AppSettings["MinNumOfDebates"] )

        # 2. search-parameter from the UI
        #    tags: we use the tags without  leading #
        tagString = tool.ui.getCtrl('txb_hashtags').Text.strip()    # get user input
        tagsFromSearch = []                                         # list with hashtags without '#'
        if tagString != System.String.Empty:
            tagsRawInput = tagString.split(',')
            if len(tagsRawInput) > 0:
                for itm in tagsRawInput:                        # remove hashtags
                    if itm[0] == '#':
                        tagsFromSearch.Add( itm[1:] )
                    else:
                        tagsFromSearch.Add( itm )

        for tgGvn in tagsFromSearch:
            tool.log.w2lgDvlp( 'tag   : ' +  tgGvn )

        # 1. create a list o0f locations ordered by the distance from selected value
        selectLocation = tool.ui.getCtrl('sel_lctn')
        selIndex = selectLocation.SelectedIndex
        locList = []
    
        for itm in selectLocation.Items : locList.Add( itm.Value.ToString() )

        front = locList[0:selIndex]
        front.reverse()
        back = locList[selIndex:]
        backLen = len(back)
        frontlen = len(front)
        
        locations = []
        idx = 0
        for loc in locList:
            if idx < backLen:  locations.Add( back[idx].ToString() )
            if idx < frontlen: locations.Add( front[idx].ToString() )
            idx += 1

        # helper-array to store all mongo-ids we have loaded from item-table
        idList = []

        for location in locations:
            # select all jobs in this area
            rows = tool.appCch.dtVwLoctn.FindRows( location )

            for row in rows:
                if row['objectType'] == 1:              # get all debates

                    if not tagsFromSearch:
                        resultTble.ImportRow(row.Row)
                        idList.Add( row['_ID'].ToString() )

                    else :
                        # get all the tags for the given item and checks if the row-type is contained. 
                        # than the item.base-ow will be added to the output-table 
                        tagRws = tool.appCch.dtVwTagList.FindRows( row['_ID'].ToString() )

                        tagList = []
                        for tagRow in tagRws:
                            tagList.Add(tagRow['tag'].ToString())
                            tool.log.w2lgDvlp( 'found Tag : ' +  tagRow['tag'].ToString() + '   for _ID : ' +  tagRow['_ID'].ToString()+ '   for _locationID : ' +  tagRow['_locationID'].ToString() )
                       
                        # intersection generates the schnittmege of two given lists (python battery)
                        compare = set( tagsFromSearch )
                        cmpRslt = compare.intersection(tagList)

                        if len( cmpRslt ) > 0:                              # if we have consonant with search add the row to the result-table
                            resultTble.ImportRow(row.Row)
                            idList.Add( row['_ID'].ToString() )

            if len(idList) >= minAmount : break

        # store ids in order of apperance in the table into an array. we will get the _id by calling the index of this array
        Page.ViewState['IdList'] = idList            

        # 3. bind repeater to result data-table
        repeater = tool.gtCtl('repDebateList')
        repeater.DataSource = resultTble.DefaultView
        repeater.DataBind()

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())

