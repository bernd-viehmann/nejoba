# **********************************************************************************************************************************************************************************************************************************************************************************************
# njbTools module
# ***********************************************************************************************************************************************
#
# 13.08.2011  - bervie -     initial realese
# ***********************************************************************************************************************************************
# 
# this module allows access to the tools and cache classes as member-attributes
#
# self.ui     : ui-tools from tools.tls_UiHelper : functions oftenly used when working with the asp.net stuff
#               
# self.log    : logging to filebased logging ( error and messages are seperated )
#
# self.usrDt  : access the current user-session-cache
#
# self.geoSrc : the cache with all places of the world referenced py their post-code and basic geo-calculations
#
# 28.11.2011  - bervie -     initial realese
#
# ***********************************************************************************************************************************************
import srvcs.tls_UiHelper
import srvcs.tls_LogCache
import srvcs.tls_UserData
import srvcs.ch_geoCache
import srvcs.ch_AppCache
import srvcs.ch_TaggContainer
import srvcs.ch_MapUserContainer

import System.Security.Cryptography
import System.Text
from System import *
from System import UriPartial
from System.Web.Configuration import *

import traceback                           # for better exception understanding

# **********************************************************************************************************************************************************************************************************************************************************************************************
# NjbBasic : class with fundamental functions of the Tools which are needed frequently
#
# 28.11.2011  - bervie -     initial realese
# ***********************************************************************************************************************************************
class NjbBasic:

    # ***********************************************************************************************************************************************
    # constructor with 'Page' as parameter
    # create an instance of the fundamental helper class. the attributes of the class live in the IIS-cache (application or session)
    # 
    # param :      Page ( IPY Scripting Page instance : to get access to the application cache)
    #
    # member :    
    #              self.log    :    the cached based logging
    #              self.ui     :    helpers for the user-interface
    #              self.page   :    reference to the scripting-page instance for accessing common stuff
    #              self.usrDt  :    data for this user-session living in the session-cache
    #              self.taggs  :    the class to get access to the taggs defined for the objects stored in item.base collection
    #
    # 28.11.2011   bervie      initial realese
    # 03.10.2012   bervie      changed constructor : controls of the page are allways copied into the ctrl-tree
    #                          added function wrtLog : write a text to the development-log
    #                          added getCtrl : Get a control of the webform from the internal ctrl-dict
    # 17.03.2013   bervie      added new tagging-manager "TaggContainer" that will replace the tagging-table in the AppCache
    #                          memory-usage will be much lesser and access will be faster by using python-dictionaries
    # 22.05.2013   bervie      added a helper-class to get fast access to user-data for the map
    #
    #
    #
    # ***********************************************************************************************************************************************
    def __init__(self, pg):
        try:
            self.Page = pg                      # we migth need the Page more often in the future

            # -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   - 
            # prepare the cached classes
            # -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   - 
            # the logging 
            self.log = pg.Application['njbLOG']
            if self.log == None:
                self.log = srvcs.tls_LogCache.LogCache(pg.Application)
                pg.Application['njbLOG'] = self.log

            # helper for working with the user-interface
            self.ui = pg.Application['njbUi']
            if self.ui == None:
                self.ui = srvcs.tls_UiHelper.UiTools(pg)
                pg.Application['njbUi'] = self.ui

            self.ui.getCtrlTree(pg.Master)      # load all controlls of the webform into a ctrl-dict

            # application-cache with the managment-class for accessing taggings
            self.taggs = pg.Application['njbTaggs']
            if self.taggs == None:
                self.taggs = srvcs.ch_TaggContainer.TaggContainer(pg)
                pg.Application['njbTaggs'] = self.taggs

            # application cache with the items and the location
            self.appCch = pg.Application['njbAppCache']
            if self.appCch == None:
                self.appCch = srvcs.ch_AppCache.AppCache(pg)
                pg.Application['njbAppCache'] = self.appCch

            # create an ADO.NET datatable with the geolocations for the postcodes that can be entered by the user. source for the data is geonames.org
            self.geoSrc = pg.Application['njbGeoSrc']
            if self.geoSrc == None:
                self.geoSrc = srvcs.ch_geoCache.GeoCache(pg)
                pg.Application['njbGeoSrc'] = self.geoSrc

            # session cache with important data for the session/user
            self.usrDt = pg.Session['njbUsrDt']
            if self.usrDt == None:
                self.usrDt = srvcs.tls_UserData.UserData(pg)
                pg.Session['njbUsrDt'] = self.usrDt

            # create an ADO.NET datatable with the geolocations for the postcodes that can be entered by the user. source for the data is geonames.org
            self.mapUser = pg.Application['njbMapUser']
            if self.mapUser == None:
                self.mapUser = srvcs.ch_MapUserContainer.MapUserContainer(pg)
                pg.Application['njbMapUser'] = self.mapUser

            # cache all jobs from the database into the application-cache
            #self.jobSrc = pg.Application['njbJobSrc']
            #if self.jobSrc == None:
            #    self.jobSrc = srvcs.ch_jobCache.JobCache(pg) 
            #    pg.Application['njbJobSrc'] = self.jobSrc

            # we have a flag that indicates if order-process is in progress
            self.orderInProgress = False


        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # gtCtl  copy control 
    #
    #
    # 03.10.2012   bervie  initial realease
    # ***********************************************************************************************************************************************
    def gtCtl(self, ctrlId ):
        try:
            ctrl = self.ui.getCtrl(ctrlId)
            return ctrl

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # errorMessage  :  show the error_message_div and show error 
    #   
    # parameter : error-text as string. empty string hides the error-div !!
    #
    #
    # 03.01.2012   bervie  initial realease
    # ***********************************************************************************************************************************************
    def errorMessage(self, errorText ):
        try:
            if errorText != System.String.Empty:
                self.ui.getCtrl('errorMsgBox').Visible = True
                self.ui.getCtrl('lbl_messageBox').Text = errorText
            else:
                self.ui.getCtrl('errorMsgBox').Visible = False
                self.ui.getCtrl('lbl_messageBox').Text = ''
            return 

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # print table : helper to write the data of a DataRow to the log
    #
    #
    # 03.10.2012   bervie  initial realease
    # ***********************************************************************************************************************************************
    def logRow(self, row ):
        try:
            for col in row.Table.Columns:
                self.log.w2lgDbg( "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -start" )
                self.log.w2lgDbg( "Name of col : " + col.ColumnName )
                self.log.w2lgDbg( "Type of col : " + col.DataType.ToString()  )
                self.log.w2lgDbg( "Column-Data : " + unicode(row[col.ColumnName])  )
                self.log.w2lgDbg( "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -end" )
            self.log.w2lgDbg( "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -" )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())

    # ***********************************************************************************************************************************************
    # print table : helper to write the data of a DataRow to the log
    #
    #
    # 03.10.2012   bervie  initial realease
    # ***********************************************************************************************************************************************
    def logMsg(self, txt ):
        try:
            self.log.w2lgDbg( txt)

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # checkIfNullInCache : special-case : DataCache Table can be filled from Mongo-DB during initialization or can be changed
    #                      during runtime
    #                      if from mongo-db we have 'BsonNull' as string in the cell
    #                      if done during runtime we have a System.String.Empty in the cell
    #
    #                      both means NULL! 
    #
    # param:   itm : the value to check
    #
    # return :   false : value is not NULL
    #            true  : value is NULL
    #
    #
    # 03.10.2012   bervie  initial realease
    # ***********************************************************************************************************************************************
    def checkIfNullInCache( self, item ):
        if ( item != 'BsonNull') and ( item != String.Empty ):
            return False
        else :
            return True


    # ***********************************************************************************************************************************************
    # EncryptSHA512Managed : http://stackoverflow.com/questions/1678555/password-encryption-decryption-code-in-net
    #                        http://msdn.microsoft.com/en-us/library/system.security.cryptography.sha512managed.aspx
    #
    #                        encrypt a password. used to store the pwd encrypted into the database and compare user-input on login with this value
    #
    #                        You can use the managed .Net cryptography library, then save the 
    #                        encrypted string into the database. When you want to verify the 
    #                        password you can compare the stored database string with the hashed 
    #                        value of the user input. See here for more info about SHA512Managed
    #
    # param:      string to crypt
    #
    # return :    crypted string
    #
    #
    # 03.10.2012   bervie  initial realease
    # ***********************************************************************************************************************************************
    def EncryptSHA512Managed(self, password):
        try:
            uEncode = System.Text.UnicodeEncoding();
            bytPassword = uEncode.GetBytes(password);
            sha = System.Security.Cryptography.SHA512Managed();
            hash = sha.ComputeHash(bytPassword);

            return Convert.ToBase64String(hash);

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # ***********************************************************************************************************************************************
    # fillCountryList  : fill a dropdown list with a list of given countries
    #
    # param    
    # dropDown      : reference to the drop-down to fill
    # ctryFlag='DE' : selector for the language
    # returns  = a list with prepared items for the drop-down fillup
    #
    # 22.06.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def fillCountryList( self, dropDown, ctryFlag='DE' ):
        '''
        read the config and create a list with key/value-pairs for filling up a coun try-dropdown
        param    = ctryFlag='DE' selector for the language
        returns  = a dictionary with the dropdown configuration
        '''
        try:
            seperator = WebConfigurationManager.AppSettings['stringSeperator']
            key = 'nationNames_' + ctryFlag
            drpDwnText   = WebConfigurationManager.AppSettings[key].split(seperator)
            drpDwnValue  = WebConfigurationManager.AppSettings['nationList'].split(seperator)
            for itm in drpDwnText:
                idx = drpDwnText.index(itm)
                lstItem = System.Web.UI.WebControls.ListItem(unicode(drpDwnText[idx]),unicode(drpDwnValue[idx]))
                dropDown.Items.Add(lstItem)

            # pre-select the country-code of the user
            dropDown.Items.FindByValue(ctryFlag).Selected = 1

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # fillJobTypes  : creates a dictionary from the web.config
    #
    # param    
    # dropDown      : reference to the drop-down to fill
    # ctryFlag='DE' : selector for the language
    # returns  = a list with prepared items for the drop-down fillup
    #
    # 22.06.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def fillJobTypes( self, dropDown, ctryFlag='DE' ):
        '''
        read the config and create a dictonary as source for job-type drop-down boxes
        param    = ctryFlag='DE' selector for the language
        returns  = a dictionary with the dropdown configuration

        ##### OBSOLETE ##### OBSOLETE ##### OBSOLETE ##### OBSOLETE ##### OBSOLETE ##### OBSOLETE ##### OBSOLETE ##### OBSOLETE ##### OBSOLETE ##### OBSOLETE ##### 
        ##### OBSOLETE ##### OBSOLETE ##### OBSOLETE ##### OBSOLETE ##### OBSOLETE ##### OBSOLETE ##### OBSOLETE ##### OBSOLETE ##### OBSOLETE ##### OBSOLETE ##### 
        ##### OBSOLETE ##### OBSOLETE ##### OBSOLETE ##### OBSOLETE ##### OBSOLETE ##### OBSOLETE ##### OBSOLETE ##### OBSOLETE ##### OBSOLETE ##### OBSOLETE ##### 
        '''
        try:
            seperator = WebConfigurationManager.AppSettings['stringSeperator']

            key = 'jobType_' + ctryFlag
            drpDwnText   = WebConfigurationManager.AppSettings[key].split(seperator)
            drpDwnValue  = WebConfigurationManager.AppSettings['jobTypeValue'].split(seperator)
            for itm in drpDwnText:
                idx = drpDwnText.index(itm)
                lstItem = System.Web.UI.WebControls.ListItem(unicode(drpDwnText[idx]),unicode(drpDwnValue[idx]))
                dropDown.Items.Add(lstItem)

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # ***********************************************************************************************************************************************
    # fillUserLocations  : fill the location-drop-down with the locations coming from the user-array
    #
    # param    
    # dropDown                 : reference to the drop-down to fill
    # ctryFlag='DE'            : selector for the language
    #
    # dropdown is filled internally with the locations of the user
    #
    # 22.06.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def fillUserLocations( self, dropDown, locString ):
        '''
        functions fill´s a given dropdown with the locations given by the users session-data
        param 
        dropDown                 : reference to the drop-down to fill
        ctryFlag='DE'            : selector for the language
        '''
        try:
            # convert string to array
            cities = []
            locs = locString[1:-1].split(',')
            for location in locs :
                loc = location.strip()
                # self.log.w2lgDvlp( ' Location for dropdown : "' + unicode( loc ) + '"' )
                cities.Add(loc)

                row = self.geoSrc.locTable.Rows.Find(loc)
                locRslt = row['postalCode'].ToString() + ' ' + row['placeName'].ToString()
                # self.log.w2lgDvlp( ' Location for dropdown : "' + unicode( locRslt ) + '"' )

                lstItem = System.Web.UI.WebControls.ListItem(unicode(locRslt),unicode(loc))
                dropDown.Items.Add(lstItem)

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())
















