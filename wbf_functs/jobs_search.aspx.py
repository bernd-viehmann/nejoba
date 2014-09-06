#
# job_search.aspx.py  :  define the search-pattern and redirect to joblist
#
#
from System.Web.Configuration import *
from System import UriPartial
import System
import traceback
import mongoDbMgr                                   # i am your father, luke
from srvcs.tls_UiHelper import LocDefiner
from srvcs.tls_WbFrmClasses import JobSearch


## **********************************************************************************************************************************************************************************************************************************************************************************************
##
## class JobLoader reads the jobs as given in parameters
##
## **********************************************************************************************************************************************************************************************************************************************************************************************
#class JobSearch( mongoDbMgr.mongoMgr ):
#    # ***********************************************************************************************************************************************
#    # constructor : store members for loading
#    #
#    # parameter :  
#    #   pg      :       the pointer to the webform-page instance is stored in self.Page 
#    #   locDef  :       the location-definer instance [type LocDefiner] used in the current web-page
#    #
#    # attributes:
#    #   RsltTbl :       DataTable with the results found by last load-function
#    #
#    # 10.12.2011    berndv  initial realese
#    # ***********************************************************************************************************************************************
#    def __init__(self, pg, locDef ):
#        try:
#            mongoDbMgr.mongoMgr.__init__(self, pg)      # wake up papa ; mother njbTools is included by inheritance!

#            self.locDef = locDef                        # instance of LocDefinere
#            self.prprTbl = None                         # DataTable with results of last load

#            self.ui.getCtrlTree( self.Page.Master )
#            # self.log.w2lgDvlp('constructor of class job_search.aspx.py->(Page, jobTag, LocId ) aufgefufen!')

#        except Exception,e:
#            self.log.w2lgError(traceback.format_exc())


#    # ***********************************************************************************************************************************************
#    # loadJobsOfType : one kind of job is wanted for the givern postcode
#    #
#    # 10.12.2011    berndv  initial realese
#    # ***********************************************************************************************************************************************
#    def loadJobsOfType( self ):
#        try:
#            # self.logMsg('job_search.aspx.py->JobSearch.loadJobsOfType called ' )
#            tgLst = self.ui.convertTagsFromInput(self.jobTag)

#            # create the link to the data-display webform
#            destUrl = ''
#            if not self.usrDt.isLoggedIn() : destUrl = WebConfigurationManager.AppSettings['DetailsForStrangers']       # use the detail-viewer for visitors that aren't looged in
#            else : destUrl = WebConfigurationManager.AppSettings['AddToTrialThread']                                    # go to detail-viewer for logged in users

#            #self.log.w2lgDvlp('job_search.aspx.py->JobSearch.loadJobsOfType locId    : ' + unicode( self.locId  ) )
#            #self.log.w2lgDvlp('job_search.aspx.py->JobSearch.loadJobsOfType tgLst    : ' + unicode( tgLst ) )
#            postCode = self.locDef.getCtryPstCd(self.locId)
#            itmIds = self.taggs.loadBaseItems( postCode , tgLst, False )
#            #self.log.w2lgDvlp('job_search.aspx.py->JobSearch.loadJobsOfType postcode : ' + unicode( postCode  ) )
#            #self.log.w2lgDvlp('job_search.aspx.py->JobSearch.loadJobsOfType itmIds   : ' + unicode( itmIds ) )

#            itemTable   = self.appCch.dtSt.Tables["items"]
#            resultTble  = itemTable.Clone()

#            for itm in itmIds:
#                row = itemTable.Rows.Find(itm)
#                resultTble.ImportRow(row)
#                # HACK tagZero in the temporary result-table will store the link to the detailview  # added 11-08-2013 bervie
#                itmLnk = destUrl + '?item=' + row['_ID'].ToString()
#                resultTble.Rows[resultTble.Rows.Count - 1]['tagZero'] = itmLnk

#            # store ids in order of apperance in the table into an array. we will get the _id by calling the index of this array
#            #self.Page.ViewState['IdList'] = itmIds

#            if resultTble.Rows.Count == 0:
#                self.prprTbl = None
#            else:
#                self.prprTbl = resultTble

#        except Exception,e:
#            self.log.w2lgError(traceback.format_exc())


#    # ***********************************************************************************************************************************************
#    # loadJbsOfLoctn : if no job-type is filtered ( jobtype == * ) this function crerates a list with all stuff of a given location
#    #
#    # 10.12.2011    berndv  initial realese
#    # ***********************************************************************************************************************************************
#    def loadJbsOfLoctn( self ):
#        try:
#            # 1. search-parameter from the UI
#            #    locations : get the selected location
#            tagTable    = self.appCch.dtSt.Tables["itemTags"]
#            itemTable   = self.appCch.dtSt.Tables["items"]
#            resultTble  = itemTable.Clone()
#            #minAmount = System.Convert.ToInt16( WebConfigurationManager.AppSettings["MinNumOfDebates"] )

#            # create the link to the data-display webform
#            destUrl = ''
#            if not self.usrDt.isLoggedIn() : destUrl = WebConfigurationManager.AppSettings['DetailsForStrangers']       # use the detail-viewer for visitors that aren't looged in
#            else : destUrl = WebConfigurationManager.AppSettings['AddToTrialThread']                                    # go to detail-viewer for logged in users

#            # 2. create a list of locations ordered by the distance from selected value
#            locList = self.locDef.loadCityArea( False )

#            # helper-array to store all mongo-ids we have loaded from item-table
#            # idList = []

#            for location in locList:
#                # select all jobs in this area
#                rows = self.appCch.dtVwLoctn.FindRows( location )
#                #self.logMsg('jobs_list.aspx.py-LoadAllJobs location_id : ' + str(location) )

#                for row in rows:
#                    if row['objectType'] == 0:              # get all jobs   objectType 0 = job is defined in the web.config
#                        resultTble.ImportRow(row.Row)
#                        #idList.Add( row['_ID'].ToString() )
#                        #self.log.w2lgDvlp('jobs_list.aspx.py-LoadAllJobs item loaded : ' + row['_ID'].ToString() )
#                        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                        # HACK tagZero in the temporary result-table will store the link to the detailview   # added 11-08-2013 bervie
#                        itmLnk = destUrl + '?item=' + row['_ID'].ToString()
#                        resultTble.Rows[resultTble.Rows.Count - 1]['tagZero'] = itmLnk

#            # store ids in order of apperance in the table into an array. we will get the _id by calling the index of this array
#            #self.Page.ViewState['IdList'] = idList            

#            # 3. store the result in the class attribute
#            if resultTble.Rows.Count == 0:
#                self.prprTbl = None
#            else:
#                self.prprTbl = resultTble

#        except Exception,e:
#            self.log.w2lgError(traceback.format_exc())


#    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
#    # loadWthoutLctn :  load all jobs without filtering for a postcode-area. this function is called when no country has been specified or a whole 
#    #                   country should be displayed
#    #
#    # parameter : jobtag  : the internal job-type identifier
#    #
#    #
#    # 17.12.2013   - bervie-      initial realese
#    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
#    def loadWthoutLctn( self, jobTag = None ):
#        try:
#            # get the current country-selection
#            cntrySlctn = self.usrDt.userDict['LCDFNR_SLCTSTR'].split('|')[0].ToString()
#            resultTble  = self.appCch.dtSt.Tables["items"].Clone()
#            if jobTag is not None: jobTag = jobTag.upper()

#            # create the link to the data-display webform
#            destUrl = ''
#            if not self.usrDt.isLoggedIn() : destUrl = WebConfigurationManager.AppSettings['DetailsForStrangers']       # use the detail-viewer for visitors that aren't looged in
#            else : destUrl = WebConfigurationManager.AppSettings['AddToTrialThread']                                    # go to detail-viewer for logged in users

#            #for cntr in range( self.appCch.dtSt.Tables["items"].Rows.Count )[::-1]:                 # go reverse through the list
#            for cntr in range( self.appCch.dtSt.Tables["items"].Rows.Count ):
#                row = self.appCch.dtSt.Tables["items"].Rows[cntr]
                
#                # if row is not a job it is also not interesting
#                if row['objectType'] != 0 : continue

#                # if country is selected check if row is for same country : this is NOT a postcode-check ! this query is postcode independent
#                if cntrySlctn != '*' :
#                    cntryOfRow = self.locDef.getCtryPstCd( row['_locationID'] ).split('|')[0]
#                    if cntryOfRow != cntrySlctn : 
#                        continue

#                # check if we have a matching job-type
#                if (jobTag is not None) and (jobTag != '*'):
#                    if row['tagZero'].ToString() != jobTag : 
#                        continue

#                resultTble.ImportRow(row)       # it seems to be a valid row !!  !!!!   !!!!!! follow the white rabbit

#                # HACK tagZero in the temporary result-table will store the link-parameter to the detailview; the final redirection-link will be build in javascript
#                LnkParam = destUrl + '?item=' + row['_ID'].ToString()
#                resultTble.Rows[resultTble.Rows.Count - 1]['tagZero'] = LnkParam

#            if resultTble.Rows.Count == 0:
#                resultTble.Rows
#                self.prprTbl = None
#            else:
#                self.prprTbl = resultTble

#        except Exception,e:
#            self.log.w2lgError(traceback.format_exc())


#    # ***********************************************************************************************************************************************
#    # loadJobsByLctn : load-kickstarter : a data-table with all results will be created : self.resultTbl
#    #  ++ remark ++ : the result of the load will be stored in the member-attribute self.resultTbl
#    #
#    #
#    # 10.12.2011    berndv  initial realese
#    # ***********************************************************************************************************************************************
#    def loadJobsByLctn(self, jobTag = None , locId = None ):
#        try:
#            self.jobTag = jobTag
#            self.locId = locId

#            # if something was selceted filter the job-types
#            if self.jobTag != '*' : 
#                self.loadJobsOfType()
#            # if no job was selected we load all stuff
#            else : 
#                self.loadJbsOfLoctn()

#        except Exception,e:
#            self.log.w2lgError(traceback.format_exc())


#    # ***********************************************************************************************************************************************
#    # getJobIdtfr() : get the real-name and the internal tag for a given job-type like : ('PC und Internet', '?*JTD01_computer' )
#    #                 if the jobtype in the url is unknown it retunrs ('Ohne Filter', '*')
#    #
#    # 10.12.2013    berndv  initial realese
#    # ***********************************************************************************************************************************************
#    def getJobIdtfr(self):
#        try:
#            # jobRealName is the real-name of the given job-type
#            if self.Page.Request.QueryString['jobtype'] != None:
#                jobRealName = self.Page.Request.QueryString['jobtype'] 
#            else:
#                return ('Ohne Filter', '*')

#            seperator = WebConfigurationManager.AppSettings['stringSeperator']
#            names = WebConfigurationManager.AppSettings['jobType_DE'].split(seperator)
#            values = WebConfigurationManager.AppSettings['jobTypeValue'].split(seperator)

#            #check if we have a valid parameter 
#            if jobRealName not in names : return ('Ohne Filter', '*')

#            jobTagName = values[ names.index(jobRealName) ]
#            return (jobRealName,jobTagName)             # returns ('PC und Internet', '?*JTD01_computer' )

#        except Exception,e:
#            self.log.w2lgError(traceback.format_exc())


#    # ***********************************************************************************************************************************************
#    # load :   this functions loads the data as a slice.
#    #
#    # 27.12.2011    berndv  initial realese
#    # ***********************************************************************************************************************************************
#    def load(self):
#        try:
#            self.log.w2lgDvlp('job_search.aspx.py->JobSearch.load(self) - - - - - - - - - - - - - - - ')

#            # 1. check if location-selection was invalid. if so we cannot display jobs
#            if self.usrDt.userDict['LCDFNR_MONGOID'] == 'not found' : 
#                self.errorMessage(self.ui.getCtrl('msg_wrong_location').Text )
#                return False

#            locDbId = self.locDef.mongoId
#            jbTg = self.getJobIdtfr()[1]

#            #self.log.w2lgDvlp('job_search.aspx.py->JobSearch.load(self)  location-id DB :      ' + unicode(locDbId) )
#            #self.log.w2lgDvlp('job_search.aspx.py->JobSearch.load(self)  job-tag        :      ' + unicode(jbTg) )


#            # 2. if location was specified load with location; if not load without.
#            if self.usrDt.userDict['LCDFNR_MONGOID'] == 'not available' : 
#                self.loadWthoutLctn(jbTg)
#            else:
#                self.loadJobsByLctn(jbTg,locDbId)

#            if self.prprTbl == None:
#                return None

#            # generate the part of result needed
#            return self.createSlice()

#        except Exception,e:
#            self.log.w2lgError(traceback.format_exc())


#    # ***********************************************************************************************************************************************
#    # createSlice :   generate a part of the self.result-table needed for the display (easy name for that is paging)
#    #                 
#    #
#    # parameter : None ( the ViewState is used to figure out direction )
#    # returns   : DataTable : The function creaes a data-table that can be bound as datasource to a ctrl/widget
#    #
#    # 27.12.2011    berndv  initial realese
#    # ***********************************************************************************************************************************************
#    def createSlice(self):
#        try:
#            #return self.prprTbl

#            # 1. get the rahmenbedingungen
#            firstRow    = lastRow = rng = None
#            pgngDrctn   = self.Page.ViewState['PAGING_DIRECTION']                       # what is the direction for the next page of data
#            jbPgLngth   = int(WebConfigurationManager.AppSettings[ 'JobPageLength' ])    # the amount of job-items that should be displayed at once
#            rsltLength  = self.prprTbl.Rows.Count                                        # length of the result-table

#            if (self.Page.ViewState['NWST_ITM'] == System.String.Empty) and (self.Page.ViewState['OLDST_ITM'] == System.String.Empty):
#                firstRow = rsltLength - jbPgLngth
#                lastRow = rsltLength
#            else :
#                if pgngDrctn =='BACKWARD':
#                    firstRow = self.Page.ViewState['OLDST_ITM'] - jbPgLngth
#                    lastRow = firstRow + jbPgLngth
#                if pgngDrctn =='FORWARD':
#                    firstRow = self.Page.ViewState['OLDST_ITM'] + jbPgLngth
#                    lastRow = firstRow + jbPgLngth

#            # # # check bounds
#            # 1. if result-table is shorter than the defined displayitem-amount display the whole table
#            if rsltLength < jbPgLngth:
#                firstRow = 0
#                lastRow = rsltLength
#            if lastRow > rsltLength : 
#                lastRow = rsltLength
#            if firstRow < 0 : 
#                firstRow = 0

#            self.Page.ViewState['OLDST_ITM'] = firstRow
#            self.Page.ViewState['NWST_ITM'] = lastRow

#            self.ui.getCtrl('hyLnk_pageOlderJobs').Visible = True
#            self.ui.getCtrl('hyLnk_pageNewerJobs').Visible= True
#            if firstRow <= 0:
#                self.ui.getCtrl('hyLnk_pageOlderJobs').Visible = False
#            if lastRow >= rsltLength:
#                self.ui.getCtrl('hyLnk_pageNewerJobs').Visible = False
#            self.log.w2lgDvlp('job_search.aspx.py- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ')
#            self.log.w2lgDvlp('job_search.aspx.py->createSlice       : direction    ' + unicode( pgngDrctn ) )
#            self.log.w2lgDvlp('job_search.aspx.py->createSlice       : firstRow     ' + unicode( firstRow ) )
#            self.log.w2lgDvlp('job_search.aspx.py->createSlice       : lastRow      ' + unicode( lastRow ) )
#            self.log.w2lgDvlp('job_search.aspx.py- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ')

#            # copy the data in REVERSE order. the newest entry should be displayed as first entry
#            outputTable = self.prprTbl.Clone()
#            for idx in reversed(range( firstRow, lastRow )):
#                #self.log.w2lgDvlp('job_search.aspx.py->createSlice       : import Index   ' + unicode(idx) )
#                outputTable.ImportRow( self.prprTbl.Rows[idx] )
#            return outputTable

#        except Exception,e:
#            self.log.w2lgError(traceback.format_exc())

#    # ***********************************************************************************************************************************************
#    # HndlrButtonClick    : handler for button-click-events. chose button by ID
#    #
#    # 14.10.2013  - bervie -     initial realese
#    # ***********************************************************************************************************************************************
#    def HandlBtnClick(self, sender, e):
#        try:
#            urlNext = None
#            if sender.ID not in ['btn_select_slct_loctn','btn_show_job_list','hyLnk_pageOlderJobs','hyLnk_pageNewerJobs'] : return False

#            # # # BUTTON paging : display newer jobs ('forward-button') later in Page_PreRender
#            if sender.ID == 'hyLnk_pageNewerJobs':
#                self.Page.ViewState['PAGING_DIRECTION'] = 'FORWARD'
#                return True

#            # # # BUTTON paging : display older jobs ('backward-button') later in Page_PreRender
#            elif sender.ID == 'hyLnk_pageOlderJobs':
#                self.Page.ViewState['PAGING_DIRECTION'] = 'BACKWARD'
#                return True

#            # # # BUTTON location was changed ('Ort ?ndern')
#            elif sender.ID == 'btn_select_slct_loctn':
#                countryCode     = self.ui.getCtrl('sel_country').SelectedValue 
#                cityIdentifier  = self.ui.getCtrl('txbx_city').Text
#                self.locDef.setLocByInpt( countryCode , cityIdentifier ) 
#                if self.locDef.getValidLoctn() is None:
#                    self.errorMessage(self.ui.getCtrl('msg_noLocFound').Text )
#                    return False

#                # reset the paging
#                self.Page.ViewState['PAGING_DIRECTION']  = System.String.Empty           # read data from beginning ...
#                self.Page.ViewState['NWST_ITM'] = System.String.Empty
#                self.Page.ViewState['OLDST_ITM'] = System.String.Empty

#            # # # BUTTON . reload list data ('neu laden') : if all input valid just load the stuff again
#            elif sender.ID == 'btn_show_job_list' :
#                # check if input is correct
#                if self.checkInput() is not True:
#                    self.log.w2lgDvlp('job_search.aspx.py->HandlBtnClick : Input-Error  ')
#                    return False
#                self.Page.ViewState['PAGING_DIRECTION']  = System.String.Empty           # read data from beginning ...
#                self.Page.ViewState['NWST_ITM']  = System.String.Empty                   # ... and resets the paging
#                self.Page.ViewState['OLDST_ITM'] = System.String.Empty

#            # page will be reloaded
#            urlNext = WebConfigurationManager.AppSettings['SearchJob'] + '?jobtype='
#            urlNext += self.Page.Server.UrlEncode( self.getJobIdtfr()[0] )

#        except Exception,e:
#            self.log.w2lgError(traceback.format_exc())
#            return

#        if urlNext != None :
#            # self.usrDt.measurePeformance('HndlrButtonClick of webform Default.aspx before redirection')
#            Response.Redirect( self.Page.ResolveUrl( urlNext ) )


#    # ***********************************************************************************************************************************************
#    # HandlLnkBtn    : handler for the link-buttons. they call same webform with different parameter for job-type
#    #
#    # 10.12.2013  - bervie -     initial realese
#    # ***********************************************************************************************************************************************
#    def HandlLnkBtn(self, sender, e):
#        try:
#            urlNext = None

#            # get the current job_type_tag from the link_id
#            jobTypeTag = sender.ID.split('_')[-1].ToString().upper()
#            jobTaggs =  WebConfigurationManager.AppSettings['jobTypeValue'].split(';')[1:]
#            tool.log.w2lgDvlp('job_search.aspx.py->HandlLnkBtn -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  ' )
#            tool.log.w2lgDvlp('job_search.aspx.py->HandlLnkBtn : jobTypeTag   :  ' +  jobTypeTag )
#            tool.log.w2lgDvlp('job_search.aspx.py->HandlLnkBtn : jobTaggs     :  ' +  unicode(jobTaggs) )

#            jobName = '*'
#            for tag in jobTaggs:
#                if jobTypeTag in tag:
#                    idx = jobTaggs.index(tag) + 1
#                    jobName = WebConfigurationManager.AppSettings['jobType_DE'].split(';')[idx]

#            tool.log.w2lgDvlp('job_search.aspx.py->HandlLnkBtn : job_type selected :  ' +  jobName )
#            tool.log.w2lgDvlp('job_search.aspx.py->HandlLnkBtn -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  ' )
#            # go to the listing of jobs with the search-parameter
#            urlNext = WebConfigurationManager.AppSettings['SearchJob'] + '?jobtype='
#            urlNext += Page.Server.UrlEncode( jobName )

#        except Exception,e:
#            tool.log.w2lgError(traceback.format_exc())
#            return

#        if urlNext != None :
#            Response.Redirect( Page.ResolveUrl( urlNext ) )

#    # ***********************************************************************************************************************************************
#    # checkInput() : checks user input 
#    #
#    # 29.12.2012    berndv  initial realese
#    # ***********************************************************************************************************************************************
#    def checkInput(self):
#        try:
#            # check if a valid location is selcted
#            if tool.usrDt.userDict['LCDFNR_MONGOID'] == 'not found' : 
#                tool.errorMessage(tool.ui.getCtrl('msg_wrong_location').Text )
#                return False

#            return True

#        except Exception,e:
#            tool.log.w2lgError(traceback.format_exc())


#    # ***********************************************************************************************************************************************
#    # getParamter() : store URL-parameter in the helper-ctrls
#    #
#    # checking this URL-Parameter:
#    #  Loc        : the locationa as database-id
#    #  jobtype    : the type of jobs that should be selected
#    #
#    # 10.12.2013    berndv  initial realese
#    # ***********************************************************************************************************************************************
#    def getParamter(self):
#        try:
#            # location can come as URL-parameter : re-initialyze the location-definer
#            loctn = System.String.Empty
#            if self.Page.Request.QueryString['Loc'] != None:
#                loctn = self.Page.Request.QueryString['Loc']
#                self.locDef.setLocByDbId( loctn )

#            # check and store jobtype-parameter
#            jobIdntfr = tool.getJobIdtfr()
#            tool.ui.getCtrl('txbx_jobName').Text = jobIdntfr[0]
#            tool.ui.getCtrl('txbx_jobType').Text = jobIdntfr[1]
 
#        except Exception,e:
#            tool.log.w2lgError(traceback.format_exc())


#    # ***********************************************************************************************************************************************
#    # Page_Load        : initializer of the webpage
#    #
#    # 18.03.2012  - bervie -     initial realese
#    # ***********************************************************************************************************************************************
#    def Page_Load(self, sender, e):
#        try:
#            # hide the main-user-interface after a button-click and show  a please-wait sedativ
#            self.ui.getCtrlTree( self.Page.Master )
#            self.ui.hideFormAfterClick()
#            self.errorMessage('')

#            if( not self.Page.IsPostBack ):
#                repeater = self.gtCtl('repJobList')                             # disable view-state for the repeater 
#                repeater.EnableViewState = False                                # ...(!! only display the data from current search !!)

#                self.Page.ViewState['NWST_ITM'] = System.String.Empty                # currently the job-display has a paging which is applied on the server. 
#                self.Page.ViewState['OLDST_ITM'] = System.String.Empty               # these are the bounds of table that are displayed on screen

#                self.Page.ViewState['PAGING_DIRECTION'] = System.String.Empty        # the direction of the paging [FORWARD]: show newer; [BACKWARD]: show older

#        except Exception,e:
#            self.log.w2lgError(traceback.format_exc())


#    # ***********************************************************************************************************************************************
#    # Page_PreRender    : initializer after button_click
#    #
#    # 18.11.2013  - bervie -     initial realese
#    # ***********************************************************************************************************************************************
#    def Page_PreRender(self, sender, e):
#        try:
#            # insert curretn location from the session-cache
#            self.getParamter()                                                  # use URL-parameter for data-select to make the page bookmarkable
#            lcDfnr.uiInitLocIntfc()                                             # init the location-select area

#            # resultTble = getSlcOfJbs( getJobTable() , False )                 # get the data needed to fill the repeater  IT IS A DATA-VIEW, NOT A TABLE !!

#            resultTble = self.load()                                            # load the data from the helper-class. 

#            if (resultTble == None) or (resultTble.Rows.Count == 0):
#                self.errorMessage(self.ui.getCtrl('msg_noDataFound').Text )
#                return False
#            else:
#                repeater = self.gtCtl('repJobList')
#                repeater.DataSource = resultTble
#                repeater.DataBind()
#                return True

#        except Exception,e:
#            self.log.w2lgError(traceback.format_exc())
#            return


# ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ 
# ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ 
# ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ 
# ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ 
# ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ # ** -- ++ 

lcDfnr = LocDefiner( Page )                         # the helper class for location-stuff
tool = JobSearch(Page, lcDfnr )                     # helper class for job-searching


# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 18.03.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    try:
        tool.Page_Load(sender, e)

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ***********************************************************************************************************************************************
# Page_PreRender    : initializer after button_click
#
# 18.11.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_PreRender(sender, e):
    try:
        tool.Page_PreRender(sender, e)

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return

# ***********************************************************************************************************************************************
# HndlrButtonClick    : handler for button-click-events. chose button by ID
#
# 14.10.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def HandlBtnClick(sender, e):
    try:
        tool.HandlBtnClick(sender, e)

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return

# ***********************************************************************************************************************************************
# HandlLnkBtn    : handler for the link-buttons. they call same webform with different parameter for job-type
#
# 10.12.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def HandlLnkBtn(sender, e):
    try:
        tool.HandlLnkBtn( sender, e)

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return
