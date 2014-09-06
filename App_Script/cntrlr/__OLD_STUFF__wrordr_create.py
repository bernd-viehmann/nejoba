# ***********************************************************************************************************************************************
# createRequest      :  business logic for wrordr_create.py; prepare and write a new created request into the database
#                       
#                       the database logic is more complex and therefore implemented in an extra-class:
#                       
#                       wrordr_create_db_request
#
#  29.12.2011   - berndv -              initial release
#
# ***********************************************************************************************************************************************
#import mongoDbMgr                               # father : the acces to the database
import wrordr_create_db_request                 # data access base class
import traceback                                # for better exception understanding
import System.DateTime                          # to use System.DateTime.Now
from System.Web.Configuration import *          # get the web.config


class createRequest(wrordr_create_db_request.createWrordrRequest) :
    # ***********************************************************************************************************************************************
    # constructor : call the base class constructor to initialize log, cache, ui-helper and page-member
    #
    # 29.12.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def __init__(self, pg):
        wrordr_create_db_request.createWrordrRequest.__init__(self, pg)     # wake up papa
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
            self.buildLocationSelector()            # insert the locations of this user as source for the fancy dropdown box
            self.buildClassSelector()               # do the same for the classifications

            self.ui.getCtrl('txbx_send2server_place_id').Text = self.hometown   # by default the user searches for his hometown




            ## # # LOCATIONS 
            #rows = []                                                       # rows from location-cache with the neigbourhood of the user
            #out = unicode('')                                               # unicode written to panel in the webform
            #geoRows = self.geoSrc.findPlacesById(self.locations)            # write the data into the hidden panel in the UI

            ## we read the location-rows from geo-cache
            #for row in geoRows:
            #    rows.append( row ) 
            #    # JSON-output to the webform
            #    out += unicode('{')
            #    out += "mongoid: '" + row[1] + "' ,"        #1 4eae4547c9a3710f1ced24f5
            #    out += "searcher: '" + row[0] + "' ,"       #0 DE|49356|DIEPHOLZ
            #    out += "postcode: '" + row[3] + "' ,"       #3 49356
            #    out += "placename: '" + row[4] + "' ,"      #4 Diepholz
            #    out += "lati: " + str(row[5]) + " ,"        #5 52.6076
            #    out += "long: " + str(row[6]) + " ,"        #6 8.3663
            #    out += "dstnc: '" + "NA" + "'"              # Not Available will be peplaces with distance to center
            #    out += unicode('};')

            #    # self.log.w2lgDvlp('searchRequest(mongoDbMgr.mongoMgr)->insertToWebForm(self): row = ' + str(row))
            #self.log.w2lgDvlp('searchRequest(mongoDbMgr.mongoMgr)->insertToWebForm(self):' + out)

            #self.ui.getCtrl('jvscr_server_location').Text = out # put info from the first roe [index 0] into the edit by default
            #i = 0
            #for item in rows[0]:
            #    self.log.w2lgDvlp(unicode(i) + 'item =   :  ' + unicode(item))
            #    i += 1

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # buildLocationSelector : build a selector with the 
    #
    # 07.02.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def buildLocationSelector(self):
        try:
            # # # LOCATIONS 
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
            i = 0
            for item in rows[0]:
                self.log.w2lgDvlp(unicode(i) + 'item =   :  ' + unicode(item))
                i += 1

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
            rqstClsTyps = '*;' + WebConfigurationManager.AppSettings['requestClasses']
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


    # ***********************************************************************************************************************************************
    # storeInput: save the data given by the user in textboxes to a helper-dict (attribute of this class)
    #              
    #
    # 13.02.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def storeInput(self):
        try:
            # 1.  copy the stuff from the inputs (filled by user or ajax) into the helper dict self.formInpt
            self.formInpt = {};
            self.ui.getCtrlTxt('txbx_')
            for item in self.ui.ctrlDict.keys():
                if item != None:
                    # get the textboxes
                    if item.find('txbx_') == 0:
                        key = item[5:]
                        value = self.ui.ctrlDict[item].Text
                        self.formInpt.update( { key : value } )

            # 2.  write the collected data to the user-log
            self.log.w2lgDvlp('-- start -- createRequest.storeInput   -- -- -- -- -- -- -- -- -- -- -- what is in the user-session dict after storeInput' )
            for item in self.formInpt.keys():
                self.log.w2lgDvlp( 'name of ctrl : ' + item + '     | text-value  : ' + self.formInpt[item] )
            self.log.w2lgDvlp('-- end   -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- what is in the user-session dict after storeInput \n' )

            # 3. create the documents in the database
            self.createDcmnts()

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())

















