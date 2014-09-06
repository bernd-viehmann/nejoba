# ***********************************************************************************************************************************************
# wrordr_search :  business logic for wrordr_search.py
#                  class supports the search for requests in the system
# 
# 24.01.2012    berndv  initial realese
# ***********************************************************************************************************************************************
import mongoDbMgr           # father : the acces to the database
import traceback            # for better exception understanding
from System.Web.Configuration import *
from System.DateTime import Now


class searchRequest(mongoDbMgr.mongoMgr) :
    # ***********************************************************************************************************************************************
    # constructor : call the base class constructor to initialize log, cache, ui-helper and page-member
    #
    # 24.01.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def __init__(self, pg):
        mongoDbMgr.mongoMgr.__init__(self, pg)              # wake up papa
        self.getUserDefaults()          # ask the location-cache for infos of given location-IDs
        self.getLocationDetails()       # copy the received data into the 
        self.insertToWebForm()          # put the stuff into the webform


    # ***********************************************************************************************************************************************
    # getUserDefaults : get the defaults for the user from the cache 
    #
    # 24.01.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def getUserDefaults(self):
        try:
            self.postCode  = self.usrDt.getItem('postcode').strip()
            self.city      = self.usrDt.getItem('city').strip()
            self.classes   = self.usrDt.getItem('requestClassification').strip()

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # getLocationDetails : ask the location cache for the informations we need
    #
    # 24.01.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def getLocationDetails(self):
        try:
            self.locations = self.usrDt.getItem('geo_answer')[1:-1].split(',')
            self.hometown  = self.locations[0]
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # insertToWebForm : write the results into the form
    #
    # 24.01.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def insertToWebForm(self):
        try:
            self.buildLocationSelector()            # LOCATIONS
            self.buildClassSelector()               # TYPES OF CLASSES

            # insert default values into the ajax-reqauest-parameter-edits
            self.ui.getCtrl('txbx_clssfctn_key').Text = '*'
            self.ui.getCtrl('txbx_place_id').Text = self.hometown

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # buildLocationSelector : build a selector the is be used for the fancy selector
    #
    # 07.02.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def buildLocationSelector(self):
        try:
            rows = []                                                       # rows from location-cache with the neigbourhood of the user
            out = unicode('')                                               # unicode written to panel in the webform
            geoRows = self.geoSrc.findPlacesById(self.locations)            # write the data into the hidden panel in the UI

            # we read the location-rows from geo-cache
            for row in geoRows:
                rows.append( row ) 
                # JSON-output to the webform
                out += unicode('{')
                out += "mongoid: '" + row[1] + "' ,"        #1 4eae4547c9a3710f1ced24f5
                out += "searcher: '" + row[0] + "' ,"       #0 DE|49356|DIEPHOLZ
                out += "postcode: '" + row[3] + "' ,"       #3 49356
                out += "placename: '" + row[4] + "' ,"      #4 Diepholz
                out += "lati: " + str(row[5]) + " ,"        #5 52.6076
                out += "long: " + str(row[6]) + " ,"        #6 8.3663
                out += "dstnc: '" + "NA" + "'"              # Not Available will be peplaces with distance to center
                out += unicode('};')

                # self.log.w2lgDvlp('searchRequest(mongoDbMgr.mongoMgr)->insertToWebForm(self): row = ' + str(row))
            self.log.w2lgDvlp('searchRequest(mongoDbMgr.mongoMgr)->insertToWebForm(self):' + out)

            self.ui.getCtrl('jvscr_server_location').Text = out # put info from the first roe [index 0] into the edit by default
            
            # ## ## ## Log the found items ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## 
            #i = 0
            #for item in rows[0]:
            #    self.log.w2lgDvlp(unicode(i) + 'item =   :  ' + unicode(item))
            #    i += 1


        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # buildClassSelector : build a selector the is be used for the fancy selector
    #
    # 07.02.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def buildClassSelector(self):
        try:
            # insert server-side classes descriptors [* means select all]
            rqstClsTyps = '*;' + WebConfigurationManager.AppSettings['requestClasses']          # '*' is used as a flag to get all data unfiltered
            self.ui.getCtrl('txbx_clssfctn_key').Text = rqstClsTyps

            # insert the client-names (language dependent)
            rqstUiNames = self.ui.getCtrl('data_themClassesClient').Text

            # compbine the stuff to a dict
            serverNms = rqstClsTyps.split(';')
            clntsNms = rqstUiNames.split(';')
            combined = zip(serverNms,clntsNms)

            # build the source-select widget
            out = unicode('<select id="sourceClasses">')
            for item in combined:
                out += '<option value="' + item[0] + '">' + item[1] + '</option>'
                pass
            out += '</select>'

            outCanvas = rqstUiNames = self.ui.getCtrl('pnl_selectables').Controls[0]
            outCanvas.Text = out;

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())























