#  
#
#  
#  
#  
#  
#  
#
#  
from System.Web.Configuration import *

import System.Data
import System.Collections
import clr
import traceback                    # for better exception understanding
import mongoDbMgr                   # father : the acces to the database
from System import UriPartial




class ActimapDebateList( mongoDbMgr.mongoMgr ):
    # ***********************************************************************************************************************************************
    # constructor : the class is the tool for the Parameter_result_list
    #
    # 18.04.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def __init__(self, pg):
        try:
            self.Page = pg

            mongoDbMgr.mongoMgr.__init__(self, pg)      # wake up papa ; mother njbTools is included by inheritance!
            self.ui.getCtrlTree( self.Page )
            self.log.w2lgDvlp('constructor of class ActimapDebateList(Page) called !')

            # helper dict to store the parameter 
            self.srchPtrn = {}

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # PageLoad   : called when page is loaded for the first time
    #
    # valid URL-params for the webform parameter_result_list
    #
    # loc       = location like "DE|41836" (converted to a neighbouhood-list : LOCATION_LIST)
    # tags      = tags that should be used for filtering the list (TAG_LIST)
    # srchMd    = search-mode for filtering the tags : 
    #             AND means all items with any are displayed; OR means only items with all tags are displayed 
    # key       = the internal ID of a choosen rubric  RUBRIC
    # name      = the name of the rubric for displaying in the UI  RUBRIC_NAME
    #
    # 28.04.2013  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def PageLoad(self, sender, e):
        try:
            # hide the main-user-interface after a button-click and show  a please-wait sedativ
            self.ui.getCtrlTree( self.Page.Master )
            self.ui.hideFormAfterClick()

            if not self.Page.IsPostBack:
                # 1. get the data of the location given as URL-parameter and put data into the dropdown
                #    syntax of locationparameter must be : DE|41836
                locParam  = self.Page.Request.QueryString['loc']
                if locParam:
                    locations = self.defineLocation( locParam )
                    self.Page.ViewState['LOCATION_LIST'] = locations
                    self.Page.ViewState['LOCATION_PARAM'] = locParam

                # 2. get the taggs that should be used for search. if we have a couple of taggs they have 
                #    to be seperated by comma : karneval,rosenmotag,veranstaltung or #karneval,#rosenmotag,#veranstaltung 
                taggParam = self.Page.Request.QueryString['tags']
                if taggParam:
                    taggings = self.defineTagsFromParam( taggParam )
                    self.ui.getCtrl('txb_hashtags').Text = ','.join(taggings)
                    self.Page.ViewState['TAG_LIST'] = taggings

                # 3. get the key and name of a rubric to find all items that are labeled with this key-code: nejoba will also 
                #    load all data from- sub-rubrics that belong to the given one by checking the substring matches
                rubric = self.Page.Request.QueryString['key']
                if rubric:
                    self.Page.ViewState['RUBRIC'] = rubric
                name = self.Page.Request.QueryString['name']
                if name:
                    self.Page.ViewState['RUBRIC_NAME'] = name
                    self.ui.getCtrl('txb_rubricName').Text = name

                srchMd = self.Page.Request.QueryString['srchMd']
                if srchMd:
                    if srchMd in ['AND','OR']:
                        self.Page.ViewState['SEARCH_MODE'] = srchMd

                        # set the radio-knoops accordingally
                        if srchMd == 'AND':
                            self.ui.getCtrl('radio_searchOr').Checked = False
                            self.ui.getCtrl('radio_searchAnd').Checked = True
                        else:
                            self.ui.getCtrl('radio_searchOr').Checked = True
                            self.ui.getCtrl('radio_searchAnd').Checked = False

                # load list of debates into repeater
                self.LoadDebateList()

            # create the link for external calls and prepare the social-media-buttons
            self.PrepareExtLnk()

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # HandlBtnClick   : handler for button-clix
    #
    # 07.01.2013  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def ButtonHandler( self, sender, e ):
        url = None
        try:
            url = None
            buttonId = sender.ID
            self.log.w2lgDvlp( 'thing_list->  HandlBtnClick  BUTON pressed : ' + buttonId + ' - sender-id: ' + sender.ClientID.ToString() )

            # get the results for the given search-parameter
            if 'btn_loadList' == buttonId:
                self.LoadDebateList()
                self.gtCtl('external_link_div').Visible = False

            # show the div with the external link
            elif 'btn_showLink' == buttonId:
                self.gtCtl('external_link_div').Visible = True

            elif 'btn_openDebate' == buttonId:
                # when opening a debate the system goes to the editor for debates: debate_articel_editor.aspx
                # . so use can take action. the debate_editor shows the thread and has a simple text-editor
                clntIdComponents = sender.ClientID.ToString().split('_')
                arrIdx = clntIdComponents[3]
                dbIds = self.Page.ViewState['IdList']
                listIdx = dbIds[ int(arrIdx) ]
                # self.log.w2lgDvlp( 'Index  in db-array     : ' + str(arrIdx) )
                # self.log.w2lgDvlp( 'Index  for cache-table : ' + str(listIdx) )

                url = WebConfigurationManager.AppSettings['AddArticleToDebate']                         # search for debates
                if not self.usrDt.isLoggedIn():
                    url = WebConfigurationManager.AppSettings['DetailsForStrangers']                    # use view-detail-dialog for not logged in users
                url += '?item=' + listIdx

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())

        if url != None:
            self.Page.Response.Redirect(self.Page.ResolveUrl(url))



    # ***********************************************************************************************************************************************
    # defineLocation   : define a list of places near the startpoint ordered by distance and add the list to the dropdown
    #
    # 10.03.2013  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def defineLocation( self, urlLocParam ):
        try:
            callParam = urlLocParam.split('|')
            self.log.w2lgDvlp( 'defineLocation parameter : ' + callParam[0] + ' - ' + callParam[1] )

            areaSize  = WebConfigurationManager.AppSettings["areaSize"];
            cntry     = callParam[0]
            postcd    = callParam[1]
            locList = self.geoSrc.getPlacesByPostcode( cntry.ToString(), postcd.ToString(), areaSize.ToString() )

            drpDwn = self.ui.getCtrl('sel_lctn')
            for loc in locList:
                itmText = loc[0].ToString().replace('|',' ') + ' - ' + loc[4].ToString()
                itmVal = loc[1].ToString()
                lstItem = System.Web.UI.WebControls.ListItem( itmText, itmVal )
                drpDwn.Items.Add( lstItem )
                self.log.w2lgDvlp( 'found placename  : ' +  itmText + ' ' + itmVal )

            return locList

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # defineTagsFromParam  : get taggs from the url
    #                        they must be seperated by commas. they can start witrh a hashtag, they will be converted to lowwer-case
    #
    # 10.03.2013  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def defineTagsFromParam( self, taggParam ):
        try:
            # 2. search-parameter from the UI
            #    tags: we use the tags without  leading #
            tagString = taggParam.strip().ToLower()
            taggList = []

            if tagString != System.String.Empty:
                tagsRawInput = tagString.split(',')
                if len(tagsRawInput) > 0:
                    for itm in tagsRawInput:                        # remove hashtags
                        if itm[0] == '#':
                            taggList.Add( itm[1:].ToString() )
                        else:
                            taggList.Add( itm.ToString() )

                for tagg in taggList:
                    self.log.w2lgDvlp( 'found tagg  : ' +  tagg )

                self.ui.getCtrl('txb_hashtags').Text=tagString

            return taggList

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # LoadDebateList   : load a list with debates filtered by controll-data
    #
    # 07.01.2013  - bervie -     initial realese
    # 10.04.2013  - bervie -     nothing loaded when no tag given ; not all subitems are loaded if rubric was not given
    # 23.04.2013  - bervie -     added NoResultsFoundDiv to show user if nothing was found
    # ***********************************************************************************************************************************************
    def LoadDebateList( self ):
        try:
            # get first item in the dropdown-list
            drpDwn = self.ui.getCtrl('sel_lctn')
            locSlct = drpDwn.Items[0].Text.split(' - ')[0]  #.split(' ')[0]

            # get tags that will be used for search
            freeTagText = self.ui.getCtrl('txb_hashtags').Text.strip()
        
            if len(freeTagText) > 0: 
                # load matching items  
                resultTble = self.LoadDebatesFiltered(locSlct, freeTagText)
            else:
                # if no tags were given load all base-items for given location
                resultTble = self.LoadDebatesUnfiltered()

            # sorting: list should start with the newest items - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
            chronologicView = System.Data.DataView(resultTble)
            chronologicView.Sort = 'creationTime DESC'

            # store ids in order of apperance in the table into an array. we will get the _id by calling the index of this array
            listOfIds = []
            for item in chronologicView:
                listOfIds.Add(item['_ID'])

            if len(listOfIds) > 0 : self.ui.getCtrl('NoResultsFoundDiv').Visible = False        # if data was found show it 
            else : self.ui.getCtrl('NoResultsFoundDiv').Visible = True                          # if no data was found explain this to the user in the ui

            self.Page.ViewState['IdList'] = listOfIds

            # bind repeater to result data-table
            repeater = self.gtCtl('repDebateList')
            #repeater.DataSource = resultTble.DefaultView
            repeater.DataSource = chronologicView
            repeater.DataBind()

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
    # LoadDebatesUnfiltered   : if no tags  were given this function is called to load all base-items in the area
    #
    # 07.01.2013  - bervie -     initial realese
    # 10.04.2013  - bervie -     nothing loaded when no tag given ; not all subitems are loaded if rubric was not given
    # ***********************************************************************************************************************************************
    def LoadDebatesUnfiltered( self ):
        try:
            # 1. search-parameter from the UI
            #    locations : get the selected location
            tagTable    = self.appCch.dtSt.Tables["itemTags"]
            resultTble  = self.appCch.dtSt.Tables["items"].Clone()

            minAmount = System.Convert.ToInt16( WebConfigurationManager.AppSettings["MinNumOfDebates"] )

            # 2. create a list o0f locations ordered by the distance from selected value
            selectLocation = self.ui.getCtrl('sel_lctn')
            locList = []
            for itm in selectLocation.Items : 
                locId = itm.Value.ToString()
                if locId not in locList : locList.Add( locId )

            # helper-array to store all mongo-ids we have loaded from item-table
            idList = []

            for location in locList:
                # select all jobs in this area
                rows = self.appCch.dtVwLoctn.FindRows( location )
                for row in rows:
                    if row['objectType'] == 1:              # get all debates
                        self.log.w2lgDvlp( ' LoadDebatesUnfiltered: selectLocationItems ID found ' + row['_ID'].ToString() )
                        resultTble.ImportRow(row.Row)
                if len(idList) >= minAmount : break

            return resultTble

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
    # LoadDebatesFiltered   : load debates that match for a tag
    #
    # 20.04.2013  - bervie -     initial realese
    #
    # ***********************************************************************************************************************************************
    def LoadDebatesFiltered( self, locSlct, freeTagText ):
        try:
            # get the 
            tgLst = self.ui.convertTagsFromInput(freeTagText)

            # should the tags be filtered with AND-combined Tags or with OR
            flrtAnd = False
            if self.gtCtl('radio_searchAnd').Checked == True:
                flrtAnd = True

            itmIds = self.taggs.loadBaseItems( locSlct, tgLst, flrtAnd )

            resultTble  = self.appCch.dtSt.Tables["items"].Clone()
            for itm in itmIds:
                row = self.appCch.dtSt.Tables["items"].Rows.Find(itm)
                resultTble.ImportRow(row)

            return resultTble

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # ******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
    # PrepareExtLnk   : function is called in page-load to create the external link and put the data in the social-media-buttons
    #
    #
    # loc       = location like "DE|41836" (converted to a neighbouhood-list : LOCATION_LIST)
    # tags      = tags that should be used for filtering the list (TAG_LIST)
    # srchMd    = search-mode for filtering the tags : 
    #             AND means all items with any are displayed; OR means only items with all tags are displayed 
    # key       = the internal ID of a choosen rubric  RUBRIC
    # name      = the name of the rubric for displaying in the UI  RUBRIC_NAME
    #
    # 28.04.2013  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def PrepareExtLnk( self ):
        try:
            self.log.w2lgDvlp( 'thing_list->  PrepareExtLnk pressed ' )

            url = None
            tags        = self.gtCtl('txb_hashtags').Text.strip()
            srchAnd     = self.gtCtl('radio_searchAnd').Checked

            # url = unicode(WebConfigurationManager.AppSettings['simplePinnBoard'] )
            url = "parameter_result_list.aspx"
            locName = ''

            if self.Page.ViewState['LOCATION_PARAM']:
                url += '?loc=' + unicode( self.Page.ViewState['LOCATION_PARAM'] )
                locName = self.Page.ViewState['LOCATION_PARAM'].split('|')[1]
            else:
                # "NO LOCATION ????" that is absolutly impossible
                return 

            if len(tags) > 0:
                url += '&tags=' + tags

            if srchAnd is True:
                url += '&srchMd=AND'
            else:
                url += '&srchMd=OR'

            if self.Page.ViewState['RUBRIC']:
                url += '&key=' + unicode( self.Page.ViewState['RUBRIC'] )

            if self.Page.ViewState['RUBRIC_NAME']:
                url += '&name=' + unicode( self.Page.ViewState['RUBRIC_NAME'] )


            # the url will be added to the link-link and the social-media DIV
            url = self.Page.ResolveUrl(url)
            goal = System.Uri( self.Page.Request.Url, url).AbsoluteUri

            link                = self.gtCtl('hyli_callPinnboardWithLink')
            link.Text           = goal
            link.NavigateUrl    = goal
            link.Target         = "_blank" 

            twitterTxt = '''<a href="https://twitter.com/share" class="twitter-share-button" data-url="''' + goal + '''" data-text="Eine nejoba PinnWand " data-via="info_nejoba" data-lang="de" data-size="large" data-hashtags="nejoba">Twittern</a> <script>                                !function (d, s, id) { var js, fjs = d.getElementsByTagName(s)[0], p = /^http:/.test(d.location) ? 'http' : 'https'; if (!d.getElementById(id)) { js = d.createElement(s); js.id = id; js.src = p + '://platform.twitter.com/widgets.js'; fjs.parentNode.insertBefore(js, fjs); } } (document, 'script', 'twitter-wjs');</script>'''
            frazenbuchTxt = '''<div class="fb-like" id="facebook_button_div" data-href="''' + goal + '''" data-send="true" data-layout="box_count" data-width="450" data-show-faces="true"></div>'''

            # load the link in the social-media-buttons
            twittDiv = self.ui.findCtrl(self.Page, 'twitter_button')
            faceBkDiv = self.ui.findCtrl(self.Page, 'facebook_button')

            twittDiv.InnerHtml = twitterTxt
            faceBkDiv.InnerHtml = frazenbuchTxt

            # 04.05.2013 bervie the header-text should show the  search-parmeter
            pgNme = 'nejoba : ' + locName
            freeTagText = self.ui.getCtrl('txb_hashtags').Text.strip()
            if len(freeTagText) > 0:
                pgNme += ' : ' + freeTagText

            self.Page.Header.Title = pgNme

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())















tool = ActimapDebateList(Page)



# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 07.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    try:
        tool.PageLoad(sender, e)

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ***********************************************************************************************************************************************
# HandlBtnClick   : handler for button-clix
#
# 07.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def HandlBtnClick( sender, e ):
    url = None
    try:
        tool.ButtonHandler( sender, e )

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())

    if url != None:
        Response.Redirect(Page.ResolveUrl(url))

