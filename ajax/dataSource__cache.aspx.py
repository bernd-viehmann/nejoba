#  dataSource__cache.aspx.py
#  
#  AJAX datasource webform to send the data from app-cache for some given parameters
#
# 16.09.2013  bv      changed the slice-paging from the server
#                     last item reached py paging seems not to be loaded properly
#
#
#
#
#  
from System.Web.Configuration import *
from System import UriPartial
import System.Data
import System.Web
import System.Collections
import System.Text

import clr
clr.AddReference('MongoDB.Bson')                                # mongo-db
clr.AddReference('MongoDB.Driver')
from MongoDB.Bson import *
from MongoDB.Driver import *

import traceback                    # for better exception understanding
import mongoDbMgr                   # father : the acces to the database
from srvcs.tls_WbFrmClasses import CachedDataSource

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

#class LOCALCachedDataSource( mongoDbMgr.mongoMgr ):
  #  '''
  #  CachedDataSource : class that pre-select the items before it checks the additional filtering as defined in the URL-Parameter
    
  #  loads all items from the app-cache and creates JSON from it. It is a special-text-returning webform (ironpython is not capable to use webservices !
  #  the results depends on URL-parameter:
  #  description of the URL-PARAMETER for loading webform behind DataURL
 
  # 'http://../njb_2/wbf_topic/mapTwo_dataSource.aspx?loc=DE%7C41836&Tags=world&SrchMd=OR'
 
  # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

  #  URL-parameter for the data-select:
  #      ItemType        : what type of item do we have? preselect before filtering 
  #                          can be :
  #                            1. map     item must have coordes
  #                            2. date    item must have start-date
  #                            3. list    any item allowed without filtering
  #      SliceActive     : receive which was the last slice the client read from
  #      CrsCmd       : the offset from startingpoint to continue reading at the rigth place
  #      ResultLength    : the number of items that should be send by the datasource
  #      Loc             : the geo-location as sting like "de|41836". if only "de|" is given all german 
  #                        results are send to the client from data-source
  #      Tags            : the Tags we are locking for. list is comma-seperated
  #      SrchMd          : OR means display all items with any tag; AND menas display only tags 
  #                        that are labeled with all keywords
  #      StartDate       : a string-coded date-object to define when the event starts
  #      EndDate         : a string-representation of the end of the event

  # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

  #  class-attributes and their meaning
  #      self.Workbench      : string-builder for generating the return-output
  #      self.LocationList   : string with the locations-detail-data in the neighboerhood
  #      self.CrsCmd     : stores the last item that was loaded when maximum amount was reached. this value is send to the client
  #                            and will be used as startpoint for the next read.
  #                            HINT : if reading in cache the attribute stores the row-index; if we are reading in the mongo-id the 
  #                            item stores the _mongoID used in the database.
  #      self.ActvSliceIdx  : set to TRUE if end of the cache was reached. is returned to caller to change to database-access

  #      self.AmntSnd  : max-amount of items to send back to caller . value is a definition in the web.config
  #      self.SlicesCached   : the number of slices that are cached in the IIS. if we have a lot of data per day we can increrase the 
  #                            amount of days in a slice. so we have a faster DB-access and also a bigger amount of davys in the cache

  # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

  #  member-functions and their job-description (in order of apperance)

  #      self.selQueryFunction           :   the functions is the entry-point. the parameter send to the data-source are used to 
  #                                          deceide what function is called

  #      self.idxLstByTags               :   function selects items with a tag when no postcode-area was defined
                                    
  #      self.idxLstByLocatedTags        :   function creates the list of row-endexes for taged items for a given postcode-area

  #      self.idxLstByLocation           :   get the row-indexes of all items in a postcode-area

  #      self.idxLstWithoutPreConditions :   if no tags and no locations were given this function goes through the table. it 
  #                                          checks ( if needed ) the country-code [example: "de for germany"]

  #      self.checkParamMatch            :   this function is used by all 'idxLst'-functions to check if all additional parameters 
  #                                          are matching the given row.

  #      self.cutSlice                :   the function cuts the needed page out of the result-array

  #      self.addDataItems               :   add the found data-items as JSON-code to the result-string-builder

  #      self.addConfigParam           :   add the controling parameter needed for the ListExtractor 

  #'''


  #  # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
  #  # constructor. 
  #  #
  #  # member-attributes 
  #  #
  #  #    self.Workbench        string-builder for generating the return-output
  #  #    self.LocationList     string with the locations-detail-data in the neighboerhood
  #  #    self.CrsCmd       amount of items-cursor. stores the offset from the end of cache-item-table
  #  #    self.ActvSliceIdx    the data in the database is devides in pages. page 0 is the mem-cache in the application-cache of IIS. 
  #  #                          the following pages are in the database. they are seperated by dates. so every page has a defined num 
  #  #                          of days which belonges to it
  #  #
  #  # 27.06.2013   - bervie-      initial realese
  #  # 27.07.2013   - bervie-      added self.SlicesCached : the definition of how many slides are stored in the cache. when the number
  #  #
  #  # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
  #  def __init__(self, page ):
  #      try:
  #          mongoDbMgr.mongoMgr.__init__(self, page )                                                                       # wake up papa ; mother njbTools is included by inheritance!

  #          self.Workbench      = System.Text.StringBuilder()                                                               # string-builder for generating the return-output
  #          self.LocationList   = []                                                                                        # string with the locations-detail-data in the neighboerhood
  #          self.SlicesCached   = System.Convert.ToInt32( WebConfigurationManager.AppSettings['SlicesCached'])              # the number of slices that are cached. 
  #          self.CrsCmd         = System.String.Empty                                                                       # the mongo-id of the item the lst read-process stopped
  #          self.ActvSliceIdx   = 0                                                                                         # the id of the slice we currently read
  #          self.AmntSnd        = System.Convert.ToInt32( WebConfigurationManager.AppSettings['InitialResponseLength'])     # max-amount of items to send back to caller 

  #          self.param = {}                                                 # the URL-parameters are stored in member-attribute param = {}
  #          self.param.Add('ItemType', None)
  #          self.param.Add('SliceActive', None)
  #          self.param.Add('CrsCmd', None)
  #          self.param.Add('ResultLength', None)
  #          self.param.Add('Loc', None)
  #          self.param.Add('City', None)
  #          self.param.Add('Tags', None)
  #          self.param.Add('SrchMd', None)
  #          self.param.Add('StartDate', None)
  #          self.param.Add('EndDate', None)
  #          self.param.Add('usrId', None)
  #          self.rowIdxList = []                                     # the result will contain the row-indexes in the AppCach DataTable "items" matching the query

  #          #self.itemPreFilter = {'map'  : self.preCheckMap,        # define the checkfunction depending of the item-type. it is given as url-parameter
  #          #                      'date' : self.preCheckDate,
  #          #                      'list' : self.preCheckList  }

  #          # testfunction ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  
  #          #for a in (0,1,2,3,4,5,6,7,8,9) :
  #          #    tool.appCch.getSliceBounce( a )
  #          # END  testfunction ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  

  #          # developer help : the data inside
  #          #rowIndx = 0
  #          #for row in self.appCch.dtSt.Tables["items"].Rows :
  #          #    self.log.w2lgDvlp('CachedDataSource._init_ DATA in the CACHE : RowIndex : ' + str(rowIndx) + ' --  subject :' + row['subject'].ToString() )
  #          #    rowIndx += 1


  #      except Exception,e:
  #          self.log.w2lgError(traceback.format_exc())


  #  # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
  #  # pgLoad is called from PageLoad to create the data-collection
  #  #
  #  # 27.06.2013   - bervie-      initial realese
  #  #
  #  # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
  #  def pgLoad( self ):
  #      # try:
  #      self.log.w2lgDvlp('# # # CachedDataSource.pgLoad( self ) has been called !')

  #      # prepare UTF-8 output
  #      context = System.Web.HttpContext.Current
  #      context.Response.ContentType = "text/plain; charset=utf-8"
  #      context.Response.Charset = "utf-8"
  #      context.Response.Clear()
  #      context.Response.HeaderEncoding = System.Text.UTF8Encoding(False)
  #      context.Response.ContentEncoding = System.Text.UTF8Encoding(False)

  #      self.selQueryFunction()     # lets see what parameters were send and what function must be loaded
  #      self.cutSlice()             # get the needed part the complete-result-array 
  #      self.addDataItems()         # put the data into result
  #      self.addConfigParam()       # add the controling parameter needed for the ListExtractor 

  #      text = '{' + self.Workbench.ToString() + '}'

  #      out = System.Text.Encoding.UTF8.GetBytes(text)
  #      context.Response.OutputStream.Write(out, 0, out.Length)
  #      context.Response.Flush()
  #      context.Response.End()

  #      #except Exception,e:
  #      #    self.log.w2lgError(traceback.format_exc())


  #  # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
  #  # function selQueryFunction  :    the functions is the entry-point. the parameter send to the data-source are used to 
  #  #                               deceide what function is called
  #  #
  #  # 21.07.2013   - bervie-      initial realese
  #  # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
  #  def selQueryFunction( self ):
  #      try:
  #          self.log.w2lgDvlp('# # # CachedDataSource.selQueryFunction( .. ) has been called !')

  #          #for parm in self.Page.Request.QueryString.Keys:
  #          #     self.log.w2lgDvlp('#    CachedDataSource.selQueryFunction( .. ) URL-PARM received     :' + parm + ' - ' + self.Page.Request.QueryString[parm])

  #          # special case : if user-id is given the system only 
  #          # shows the data of the given user
  #          # other checks are not made.
  #          if ('usrId' in self.Page.Request.QueryString.Keys):
  #              if self.Page.Request.QueryString['usrId'] != System.String.Empty:
  #                  self.param['usrId'] = self.Page.Request.QueryString['usrId']

  #          if ('ItemType' in self.Page.Request.QueryString.Keys):
  #              if self.Page.Request.QueryString['ItemType'] != System.String.Empty:
  #                  self.param['ItemType'] = self.Page.Request.QueryString['ItemType']

  #          # SliceActive is not used in the CACHE. we always check the whole data in the cache
  #          if ('SliceActive' in self.Page.Request.QueryString.Keys):
  #              if self.Page.Request.QueryString['SliceActive'] != System.String.Empty:
  #                  self.param['SliceActive'] = System.Convert.ToInt32( self.Page.Request.QueryString['SliceActive'])
  #                  self.ActvSliceIdx = self.param['SliceActive']

  #          if ('CrsCmd' in self.Page.Request.QueryString.Keys):
  #              if self.Page.Request.QueryString['CrsCmd'] != System.String.Empty:
  #                  self.param['CrsCmd'] = System.Convert.ToString( self.Page.Request.QueryString['CrsCmd'] )
  #                  self.CrsCmd = self.param['CrsCmd']

  #          if ('ResultLength' in self.Page.Request.QueryString.Keys):
  #              if self.Page.Request.QueryString['ResultLength'] != System.String.Empty:
  #                  self.param['ResultLength'] = System.Convert.ToInt32( self.Page.Request.QueryString['ResultLength'])
  #                  self.AmntSnd = self.param['ResultLength']

  #          if ('Loc' in self.Page.Request.QueryString.Keys):
  #              if len(self.Page.Request.QueryString['Loc']) > 3 :      # even if Loc = '0|' or 'de|41836' the location is not representing a postcode-area
  #                  self.param['Loc'] = self.Page.Request.QueryString['Loc']

  #          if ('City' in self.Page.Request.QueryString.Keys):
  #              if self.Page.Request.QueryString['City'] != System.String.Empty:
  #                  self.param['City'] = self.Page.Request.QueryString['City']

  #          if ('Tags' in self.Page.Request.QueryString.Keys):
  #              if self.Page.Request.QueryString['Tags'] != ',' :       # if no Tags were send we get ','. dont ask why :-)
  #                  self.param['Tags'] = self.Page.Request.QueryString['Tags']

  #          if ('SrchMd' in self.Page.Request.QueryString.Keys):
  #              if self.Page.Request.QueryString['SrchMd'] != System.String.Empty:
  #                  self.param['SrchMd'] = self.Page.Request.QueryString['SrchMd']

  #          if ('StartDate' in self.Page.Request.QueryString.Keys):
  #              if self.Page.Request.QueryString['StartDate'] != System.String.Empty:
  #                  # we work with UTC in the database
  #                  self.param['StartDate'] = System.DateTime.Parse(self.Page.Request.QueryString['StartDate'] ).ToUniversalTime()
  #              else:
  #                  self.param['StartDate'] = System.DateTime.MinValue
  #          if ('EndDate' in self.Page.Request.QueryString.Keys):
  #              if self.Page.Request.QueryString['EndDate'] != System.String.Empty:
  #                  self.param['EndDate'] = System.DateTime.Parse(self.Page.Request.QueryString['EndDate'] ).ToUniversalTime()
  #              else:
  #                  self.param['EndDate'] = System.DateTime.MinValue

  #          Loctn = None
  #          if ( (self.param['Loc'] is not None) or (self.param['City'] is not None) ):
  #              Loctn = 'WeHaveALocation'
  #              self.log.w2lgDvlp('self.param["Loc"]    :  "' + unicode(self.param['Loc']) + '"' )
  #              self.log.w2lgDvlp('self.param["City"]   :  "' + unicode(self.param['City']) + '"')


  #          # call the rigth selector-function for cached data to read the items the caller is looking for.......
  #          if   (self.param['usrId'] is not None)                          :   self.idxLstForUser()
  #          elif (self.param['Tags' ] is not None) and (Loctn is None)      :   self.idxLstByTags()
  #          elif (self.param['Tags' ] is not None) and (Loctn is not None)  :   self.idxLstByLocatedTags()
  #          elif (self.param['Tags' ] is None)     and (Loctn is not None)  :   self.idxLstByLocation()
  #          elif (self.param['Tags' ] is None)     and (Loctn is None)      :   self.idxLstWithoutPreConditions()

  #          #if   (self.param['usrId'] is not None)                                       :   self.idxLstForUser()
  #          #elif (self.param['Tags' ] is not None) and (self.param['Loc'] is None)       :   self.idxLstByTags()
  #          #elif (self.param['Tags' ] is not None) and (self.param['Loc'] is not None)   :   self.idxLstByLocatedTags()
  #          #elif (self.param['Tags' ] is None) and (self.param['Loc'] is not None)       :   self.idxLstByLocation()
  #          #elif (self.param['Tags' ] is None) and (self.param['Loc'] is None)           :   self.idxLstWithoutPreConditions()

  #      except Exception,e:
  #          self.log.w2lgError(traceback.format_exc())


  #  # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
  #  # function idxLstForUser  :  if   (self.param['usrId'] is not None)
  #  #
  #  #                           get all items for a given user by his _ID
  #  #
  #  # 19.08.2013   - bervie-      initial realese
  #  # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
  #  def idxLstForUser( self ):
  #      try:
  #          self.log.w2lgDvlp('# # # CachedDataSource.idxLstForUser( self ) called ' )
  #          self.log.w2lgDvlp('#  ' )
  #          self.log.w2lgDvlp('#  ' )
  #          self.dtVwCreator = System.Data.DataView(self.dtSt.Tables['items'])
  #          self.dtVwCreator.Sort = '_creatorGUID'

  #          creatingUserView = self.appCch.dtVwCreator
  #          creatingUserView.RowFilter = '_creatorGUID = ' + self.param['usrId']

  #          for row in creatingUserView:
  #              mongoId = row['_id'].ToString()
  #              rowIndex = self.appCch.dtSt.Tables["items"].Rows.IndexOf(self.appCch.dtSt.Tables["items"].Rows.Find(mongoId))     # convert BSON-ID into row-index 
  #              if self.checkParamMatch( rowIndex ):
  #                  self.rowIdxList.Add( rowIndex )
  #                  self.log.w2lgDvlp('#     CachedDataSource.idxLstForUser( self ) row-idx added : ' + rowIndex.ToString() )

  #          #
  #          #   ToDo  
  #          ##  ToDo  #  ToDo  
  #          ##  ToDo  #  ToDo  #  ToDo  
  #          ##  ToDo  #  ToDo  #  ToDo  #  ToDo  
  #          ##  ToDo  #  ToDo  #  ToDo  
  #          ##  ToDo  #  ToDo  
  #          #   ToDo  
  #          #

  #      except Exception,e:
  #          self.log.w2lgError(traceback.format_exc())


  #  # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
  #  # function idxLstByTags  :  (self.param['Tags'] is not None) and (self.param['Loc'] is None)
  #  #
  #  #                           function selects items with a tag when no postcode-area was defined. it uses the tag-container helper class
  #  #
  #  #                            HINT:  the 'Loc'-parameter (in the member-dictionary) migth be none even if we have a country-code selcted. 
  #  #                                   so this functions check the url-parameter again to filter for a special country.
  #  #
  #  #                                   the function always creates a list with all row-idx of theitems that match. 
  #  #                                   the paging is done afterwards in cutSlice. 
  #  #                                   this is costly but till now there was no better idea.
  #  #
  #  #
  #  #
  #  # 16.08.2013   - bervie-      initial realese
  #  # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
  #  def idxLstByTags( self ):
  #      try:
  #          country = self.Page.Request.QueryString['Loc'].split(',')[0].strip()                                                                # get current country-code
  #          self.log.w2lgDvlp('# # # CachedDataSource.idxLstByTags( self ) called ' )
  #          self.log.w2lgDvlp('#     CachedDataSource.idxLstByTags( self ) TAGS is GIVEN & LOC is NONE' )
  #          self.log.w2lgDvlp('#     CachedDataSource.idxLstByTags( self )                country-code : ' + country )
            
  #          mngoIds = []                            # the results as mongo-ids

  #          if country == '0':
  #              for tagId in self.createTagList():
  #                  # if we do not have to check the country get all items for the given tag

  #                      for itmDct in self.taggs.LocDict.values():
  #                          if itmDct.has_key(tagId):
  #                              mngoIds.extend(itmDct[tagId])

  #          # if country was selected we have to filter the dicts that have a location index for the givewn country
  #          else:
  #              for locId in self.taggs.LocDict.keys():
  #                  if locId.startswith(country):
  #                      self.log.w2lgDvlp('#     CachedDataSource.idxLstByTags( self )  locId matching country     : ' + locId.ToString() )
  #                      itmDct = self.taggs.LocDict[locId]
  #                      for tagId in self.createTagList():
  #                              if itmDct.has_key(tagId):
  #                                  mngoIds.extend(itmDct[tagId])

  #          for mongoId in mngoIds:
  #              rowIndex = self.appCch.dtSt.Tables["items"].Rows.IndexOf(self.appCch.dtSt.Tables["items"].Rows.Find(mongoId))     # convert BSON-ID into row-index 
  #              if rowIndex not in self.rowIdxList:
  #                  if self.checkParamMatch( rowIndex ):
  #                      self.rowIdxList.Add( rowIndex )
  #                      self.log.w2lgDvlp('#     CachedDataSource.idxLstByTags( self ) row-idx added : ' + rowIndex.ToString() )
  #          return

  #      except Exception,e:
  #          self.log.w2lgError(traceback.format_exc())


  #  # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
  #  # function idxLstByLocatedTags        :   function creates the list of row-endexes for taged items for a given postcode-area
  #  #
  #  # 21.07.2013   - bervie-      initial realese
  #  # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
  #  def idxLstByLocatedTags( self ):
  #      try:
  #          self.log.w2lgDvlp('CachedDataSource.idxLstByLocatedTags() called         TAGS is GIVEN & LOC is GIVEN    ' )

  #          # if no cities were found stop processing
  #          if not self.createCityList():
  #              return

  #          for tagId in self.createTagList() :
  #              for loc in self.LocationList:
  #                  LocationIdentifier = loc[0]
  #                  self.log.w2lgDvlp('CachedDataSource.idxLstByLocatedTags() searching the postcode area : ' + LocationIdentifier )
  #                  ItemDct = self.taggs.LocDict[LocationIdentifier]    # ItemDct is a dict where the tagname-ids are the keys
  #                  if ItemDct.has_key(tagId):
  #                      dbIdList = ItemDct[tagId]
  #                      for mongoId in dbIdList:
  #                          rowIndex = self.appCch.dtSt.Tables["items"].Rows.IndexOf(self.appCch.dtSt.Tables["items"].Rows.Find(mongoId))     # convert BSON-ID into row-index for better performance
  #                          if rowIndex not in self.rowIdxList:
  #                              if self.checkParamMatch( rowIndex ):
  #                                  self.rowIdxList.Add( rowIndex )
  #                                  self.log.w2lgDvlp('CachedDataSource.idxLstByLocatedTags( self ) row-idx added : ' + str(rowIndex) )

  #      except Exception,e:
  #          self.log.w2lgError(traceback.format_exc())


  #  # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
  #  # function idxLstByLocation           :   get the row-indexes of all items in a postcode-area when no tags are given
  #  #
  #  # 21.07.2013   - bervie-      initial realese
  #  # 09.09.2013   - bervie-      DISCARDED : function based on hashtag-container. so untagged items was not found. rewritten 
  #  #                                         see newer fct idxLstByLocation:
  #  #
  #  # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
  #  def idxLstByLocation_DISCARDED( self ):
  #      try:
  #          self.log.w2lgDvlp('CachedDataSource.idxLstByLocation( self ) called         TAGS is NONE & LOC is GIVEN    ')
  #          self.rowIdxList = []                        # the result will contain all row-idx of the rows that match
            
  #          # if no cities were found stop processing
  #          if not self.createCityList():
  #              return

  #          mongoIdLst = []
  #          for loc in self.LocationList:
  #              cityToRead = loc[0].ToString()

  #              #self.log.w2lgDvlp('CachedDataSource.idxLstByLocation( self ) locationList listing  : ' + cityToRead )
                
  #              if self.taggs.LocDict.has_key( cityToRead ) :
  #                  #self.log.w2lgDvlp('CachedDataSource.idxLstByLocation( self ) location reading : ' + cityToRead )
  #                  ItemDct = self.taggs.LocDict[cityToRead]
                
  #                  for idList in ItemDct.values():                         # get all items we have for the location
  #                      mongoIdLst.extend( idList )

  #                  for mongoId in mongoIdLst:                              # add the row-indx-ids unique. there can be doubles because when a item will occure as often sa it has tags
  #                      rowIdx = self.appCch.dtSt.Tables["items"].Rows.IndexOf(self.appCch.dtSt.Tables["items"].Rows.Find(mongoId))
  #                      if rowIdx not in self.rowIdxList:
  #                          if self.checkParamMatch( rowIdx ):
  #                              self.rowIdxList.Add(rowIdx)
  #                              self.log.w2lgDvlp('CachedDataSource.idxLstByLocation( self ) rowIdx added : ' + str(rowIdx) )

  #      except Exception,e:
  #          self.log.w2lgError(traceback.format_exc())




  #  # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
  #  # function idxLstByLocation           :   get the row-indexes of all items in a postcode-area 
  #  #
  #  # 09.09.2013   - bervie-      initial realese
  #  #                             old function based on hashtag-container. so untagged items was not found. rewritten 
  #  #                             now the function is made easier. it goes through the table and adds all items that have 
  #  #                             the rigth location-id
  #  #
  #  # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
  #  def idxLstByLocation( self ):
  #      try:
  #          self.log.w2lgDvlp('CachedDataSource.idxLstByLocation( self ) called        TAGS is NONE & LOC is given    ')
  #          country = self.Page.Request.QueryString['Loc'].split('|')[0].strip().upper()

  #          # 1. get all matching column s from the cache
  #          countAcceptedLines = 0

  #          if self.createCityList() is False:
  #              return

  #          locMngIds = []
  #          for loc in self.LocationList:
  #              mngIDofLoc = loc[1].ToString()
  #              # self.log.w2lgDvlp('CachedDataSource.idxLstByLocatedTags() searching the postcode area : ' + mngIDofLoc )
  #              locMngIds.Add( mngIDofLoc )

  #          for cntr in range( self.appCch.dtSt.Tables["items"].Rows.Count )[::-1]:                 # go reverse through the list
  #              row = self.appCch.dtSt.Tables["items"].Rows[cntr]
  #              if row['_locationID'] in locMngIds:
  #                  rowIndex = self.appCch.dtSt.Tables["items"].Rows.IndexOf(row)     # convert into row-index for better performance
  #                  if self.checkParamMatch(rowIndex) == True:
  #                      self.rowIdxList.Add( rowIndex )

  #      except Exception,e:
  #          self.log.w2lgError(traceback.format_exc())


  #  # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
  #  # function idxLstWithoutPreConditions :     if no Tags and no locations were given this function goes through the table. it 
  #  #                                           checks ( if needed ) the country-code [example: "de for germany"]
  #  #
  #  # 21.07.2013   - bervie-      initial realese
  #  # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
  #  def idxLstWithoutPreConditions( self ):
  #      try:
  #          self.log.w2lgDvlp('CachedDataSource.idxLstWithoutPreConditions( self ) called        TAGS is NONE & LOC is NONE    ')
  #          country = self.Page.Request.QueryString['Loc'].split(',')[0].strip().upper()

  #          # 1. get all matching column s from the cache
  #          countAcceptedLines = 0
            
  #          for cntr in range( self.appCch.dtSt.Tables["items"].Rows.Count )[::-1]:                 # go reverse through the list
  #              row = self.appCch.dtSt.Tables["items"].Rows[cntr]
  #              addFlg = True                                                # switch-flag is true if item should be added.

  #              if row['_locationID'] == System.String.Empty:                   # if row has no root-element it has no location-id and should not be added 
  #                  addFlg = False
  #              else:
  #                  if country != '0':                                          # '0' means all items should be checked, so we do not have to check if country matches
  #                      coutryOfRow = self.geoSrc.getKeyStrngFromId( row['_locationID'] )
  #                      if country[0:2] != coutryOfRow[0:2] : addFlg = False
  #                      # self.log.w2lgDvlp('CachedDataSource.idxLstWithoutPreConditions    country-abbrevation : ' + coutryOfRow )
  #                      # if coutryOfRow.ToString() != country:                    # if country does not match we do not have to check this postcode-area

  #              if addFlg == True:
  #                  # rowIndex = self.appCch.dtSt.Tables["items"].Rows.IndexOf(self.appCch.dtSt.Tables["items"].Rows.Find(mongoId))     # convert BSON-ID into row-index for better performance
  #                  rowIndex = self.appCch.dtSt.Tables["items"].Rows.IndexOf(row)     # convert into row-index for better performance

  #                  if self.checkParamMatch(rowIndex) == True:
  #                      self.rowIdxList.Add( rowIndex )
  #                      # self.log.w2lgDvlp('CachedDataSource.idxLstWithoutPreConditions  added rowIndx : ' + str(rowIndex ) )

  #      except Exception,e:
  #          self.log.w2lgError(traceback.format_exc())


  #  # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
  #  # cutSlice :     the function cuts the part of needed data from the fuu result array in the IIS cached table.
  #  #                it starts at the offset (the endpoint-of read in the last reading-process) and ends with the item by result-length
  #  #
  #  #                when the end of the cache is reached the function stops adding items and sends 'end_of_data' as CrsCmd
  #  #
  #  #
  #  #
  #  # 21.07.2013   - bervie-      initial realese
  #  # 30.07.2013   - bervie-      added inidcator if end of cache was reached.
  #  # 15.08.2013   - bervie-      reverse row-idx list to become the newest items first
  #  #
  #  # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
  #  def cutSlice( self ):
  #      try:
  #          totalyFound = len( self.rowIdxList )    # store the number of items in the list before cutting
  #          self.log.w2lgDvlp('CachedDataSource.cutSlice( self ) has been called , len of the result-list : ' + unicode( totalyFound))
  #          if totalyFound == 0 : return

  #          self.rowIdxList.sort(reverse=True)

  #          for dtRowIdx in self.rowIdxList : 
  #              row = self.appCch.dtSt.Tables["items"].Rows[dtRowIdx]
  #              self.log.w2lgDvlp('cutSlice( .. )  data-rows found in list                                        : ' + unicode( dtRowIdx ) + ' - _id ' + row['_id'] )

  #          # self.rowIdxList = self.rowIdxList[::-1]     # reverse the list to get newest items first and oldest last

  #          # get the first item where to start with the result-list by the mongo-ID
  #          # REMARK: the cache in the IIS memory chages while the requrest from the client comes. by using the mongoID we can be sure that this 
  #          #         will not affect the result. the items that we send to the client are sliced by the moment the first request was send. 
  #          #         regardless how much items were added to it in the meantime

  #          leftStart = 0
  #          if self.CrsCmd != System.String.Empty : 
  #              startRowIndex = self.appCch.dtSt.Tables["items"].Rows.IndexOf(self.appCch.dtSt.Tables["items"].Rows.Find( self.CrsCmd ))
  #              leftStart = self.rowIdxList.IndexOf( startRowIndex  )
  #              #self.log.w2lgDvlp('CachedDataSource.cutSlice( self ) left-start : ' + unicode( leftStart ) + '  for cursor-command  : ' + unicode( self.CrsCmd ) )
  #          else : 
  #              # remind the client where is conquer was started
  #              self.CrsCmd = self.appCch.dtSt.Tables["items"].Rows[self.rowIdxList[0]]['_id']
  #              #self.log.w2lgDvlp('CachedDataSource.cutSlice( self ) cursor-command  is string.empty . starting point set to ' + self.CrsCmd )

  #          sliceBegin = leftStart + ( self.ActvSliceIdx * self.AmntSnd )
  #          slicedEnd  = sliceBegin + self.AmntSnd
  #          if slicedEnd >= len(self.rowIdxList) : 
  #              slicedEnd = len(self.rowIdxList)
  #              self.CrsCmd = 'end_of_data'

  #          butchersKnife = self.rowIdxList[ sliceBegin : slicedEnd ]

  #          self.rowIdxList = butchersKnife

  #          #self.log.w2lgDvlp('cutSlice results before sending data - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  ' )
  #          #self.log.w2lgDvlp('cutSlice( .. )  start of the slice                  [sliceBegin]                : ' + unicode( sliceBegin ) )
  #          #self.log.w2lgDvlp('cutSlice( .. )  end   of the slice                  [slicedEnd ]                : ' + unicode( slicedEnd ) )
  #          #self.log.w2lgDvlp('cutSlice( .. )  amount of items to load             [self.AmntSnd ]             : ' + unicode( self.AmntSnd ) )
  #          #self.log.w2lgDvlp('cutSlice( .. )  results found before cutting        [len(self.rowIdxList)]      : ' + unicode( totalyFound ) )
  #          #self.log.w2lgDvlp('cutSlice( .. )  length of the cutted result-list    [self.rowIdxList]           : ' + unicode( len(self.rowIdxList)) )
  #          #self.log.w2lgDvlp('cutSlice( .. )  length defined by query-parameter   [self.AmntSnd]              : ' + unicode( self.AmntSnd ) )
  #          #self.log.w2lgDvlp('cutSlice( .. )  cursor-command (mongoid/string)     [self.CrsCmd]               : ' + unicode( self.CrsCmd     ) )
  #          #self.log.w2lgDvlp('cutSlice( .. )  slice active after load finished    [self.ActvSliceIdx]         : ' + unicode( self.ActvSliceIdx   ) )
  #          #for dtRowIdx in self.rowIdxList : self.log.w2lgDvlp('cutSlice( .. )  result item in list                                             : ' + unicode( dtRowIdx ) )
  #          #self.log.w2lgDvlp('CachedDataSource.cutSlice( .. ) - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ' )

  #          # increase slice-index. next round-trip will send next data because of this 
  #          self.ActvSliceIdx = self.ActvSliceIdx + 1

  #      except Exception,e:
  #          self.log.w2lgError(traceback.format_exc())


  #  # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
  #  # function checkParamMatch   this function is used by all 'idxLst'-functions to check if the URL-parameters 
  #  #                            does match the given data in the row.
  #  #                            this is currently the date-check and the check if all needed data for the data-type is available
  #  #
  #  # param : rowToCheck is the row to be analyzed
  #  #
  #  # returns : true mean the row matches the selection criterias
  #  #           false means the row does not match 
  #  #
  #  # 21.07.2013   - bervie-      initial realese
  #  # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
  #  def checkParamMatch( self , rowIndx ):
  #      try:
  #          rowToCheck = self.appCch.dtSt.Tables["items"].Rows[rowIndx]
  #          if self.param['ItemType'] == 'list' : 
  #              # self.log.w2lgDvlp('CachedDataSource.checkParamMatch()    RETURN TRUE item-type = item found')
  #              if (rowToCheck['objectType'] != 1) : 
  #                  #self.log.w2lgDvlp('CachedDataSource.checkParamMatch()    RETURN False : not an debateitem : rowToCheck["objectType"] != 1)')
  #                  return False    

  #          # check if map-item has geo-data
  #          if self.param['ItemType'] == 'map':
  #              if (rowToCheck['lon'].ToString() == System.String.Empty) or (rowToCheck['lat'].ToString() == System.String.Empty):
  #                  #self.log.w2lgDvlp('CachedDataSource.checkParamMatch() missing geographical data for map for ' + rowToCheck['_ID'].ToString())
  #                  return False

  #          # date-items must have a date at least
  #          if self.param['ItemType'] == 'date':
  #              if rowToCheck['from'].CompareTo( System.DateTime.MinValue) == 0 :
  #                  #self.log.w2lgDvlp('CachedDataSource.checkParamMatch()    RETURNING FALSE  : no rowToCheck[from] given!')
  #                  return False

  #          if (self.param['StartDate'].CompareTo( System.DateTime.MinValue) == 0) : 
  #              # self.log.w2lgDvlp('CachedDataSource.checkParamMatch()    RETURNING FALSE  : URL-param Start-Date is not given')
  #              return True                            # if there were no parameter given for start-date we don not have to check 
  #          #if rowToCheck['from'].ToString() is System.DateTime.MinValue : return False      # if from is NULL the item has no date-information

  #          chckDateFlag = False

  #          #self.log.w2lgDvlp('CachedDataSource.checkParamMatch()    TimeSpan Compare just started ')
  #          #self.log.w2lgDvlp('CachedDataSource  self.param["EndDate"]' + self.param['EndDate'].ToString() )
  #          #self.log.w2lgDvlp('CachedDataSource  self.param["StartDate"]' + self.param['StartDate'].ToString() )
  #          #self.log.w2lgDvlp('CachedDataSource  rowToCheck["from"]' + rowToCheck['from'].ToString() )
  #          #self.log.w2lgDvlp('CachedDataSource  rowToCheck["till"]' + rowToCheck['till'].ToString() )

  #          # we compare only timespans !
  #          if (self.param['EndDate'].CompareTo( System.DateTime.MinValue) == 0) : self.param['EndDate'] = self.param['StartDate']
  #          if (rowToCheck['till'].CompareTo( System.DateTime.MinValue) == 0)    : rowToCheck['till'] = rowToCheck['from']

  #          # create date-comparing-result ONCE
  #          # < 0   :  first   BEFORE   CompareTo-Item
  #          # == 0  :  first   EQUAL    CompareTo-Item
  #          # > 0   :  first   AFTER    CompareTo-Item
  #          #
  #          startToFrom = self.param['StartDate'].CompareTo( rowToCheck['from'] )
  #          endToFrom = self.param['EndDate'].CompareTo( rowToCheck['from'] )
  #          startToTill = self.param['StartDate'].CompareTo( rowToCheck['till'] )
  #          endToTill = self.param['EndDate'].CompareTo( rowToCheck['till'] )

  #          if ( (startToFrom == 0) or (endToFrom == 0) or (startToTill == 0) or (endToTill == 0) ) : return True       # 0 equality 
  #          if (startToFrom > 0) and ( startToTill < 0 ) : return True                                                  # 1 start inbetween row_to_check
  #          if (endToFrom > 0  ) and ( endToTill < 0   ) : return True                                                  # 2 end   inbetween row_to_check
  #          if (startToFrom < 0) and ( endToTill > 0   ) : return True                                                  # 3 row inbetween user selection
  #          return False

  #      except Exception,e:
  #          self.log.w2lgError(traceback.format_exc())


  #  # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
  #  # function addDataItems               :   add the found data-items as JSON-code to the result-string-builder
  #  #
  #  # 21.07.2013   - bervie-      initial realese
  #  # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
  #  def addDataItems( self ):
  #      try:
  #          self.log.w2lgDvlp('CachedDataSource.addDataItems( self ) has been called !')

  #          # nothing found
  #          self.Workbench.Append('\n"items":[\n')
  #          if len(self.rowIdxList) == 0:
  #              self.Workbench.Length = self.Workbench.Length - 1
  #              self.Workbench.Append('{}],')
  #              return

  #          # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - DEVELOPMENT HELPER start
  #          #self.log.w2lgDvlp('CachedDataSource.addDataItems   # # # # # # # # # # # # # # # # # # start result-list of AJAX loader ')
  #          #for dtRowIdx in self.rowIdxList:
  #          #    row = self.appCch.dtSt.Tables["items"].Rows[dtRowIdx]
  #          #    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
  #          #    self.log.w2lgDvlp('CachedDataSource.addDataItems               : RowIndex : ' + str(dtRowIdx) + ' --  subject :' + row['subject'].ToString() + ' --  tagZero :' + row['tagZero'].ToString() )
  #          #    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
  #          #self.log.w2lgDvlp('CachedDataSource.addDataItems   # # # # # # # # # # # # # # # # # # end result-list of AJAX loader ')
  #          # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - DEVELOPMENT HELPER end

  #          for dtRowIdx in self.rowIdxList:
  #              row = self.appCch.dtSt.Tables["items"].Rows[dtRowIdx]

  #              # change DateTime of the row to a useable string
  #              fromDate = ''
  #              tillDate = ''
  #              cratDate = ''
  #              if (row['from'] != System.DateTime.MinValue ):
  #                  fromDate = System.TimeZone.CurrentTimeZone.ToLocalTime(row['from']).ToString('dd MMMM yyyy')
  #              if (row['till'] != System.DateTime.MinValue ):
  #                  tillDate = System.TimeZone.CurrentTimeZone.ToLocalTime(row['till']).ToString('dd MMMM yyyy')
  #              if (row['creationTime'] != System.DateTime.MinValue  ):
  #                  cratDate = System.TimeZone.CurrentTimeZone.ToLocalTime(row['creationTime']).ToString('dd MMMM yyyy H:mm:ss')

  #              self.Workbench.Append( '{' )
  #              self.Workbench.Append( '"_ID":"' + row['_ID'].ToString() + '",' )
  #              #self.Workbench.Append( '"objectType":"' + row['objectType'].ToString() + '",\n' )
  #              self.Workbench.Append( '"_objectDetailID":"' + row['_objectDetailID'].ToString() + '",' )
  #              #self.Workbench.Append( '"_hostGUID":"' + row['_hostGUID'].ToString() + '",\n' )
  #              #self.Workbench.Append( '"_rootElemGUID":"' + row['_rootElemGUID'].ToString() + '",\n' )
  #              #self.Workbench.Append( '"_parentID":"' + row['_parentID'].ToString() + '",\n' )
  #              #self.Workbench.Append( '"_followerID":"' + row['_followerID'].ToString() + '",\n' )
  #              self.Workbench.Append( '"_creatorGUID":"' + row['_creatorGUID'].ToString() + '",' )
  #              self.Workbench.Append( '"creationTime":"' + cratDate + '",' )
  #              self.Workbench.Append( '"_locationID":"' + row['_locationID'].ToString() + '",' )
  #              self.Workbench.Append( '"from":"' + fromDate + '",' )
  #              self.Workbench.Append( '"till":"' + tillDate + '",' )
  #              self.Workbench.Append( '"subject":"' + row['subject'].ToString() + '",' )
  #              #self.Workbench.Append( '"body":"' + row['body'].ToString() + '",\n' )
  #              self.Workbench.Append( '"nickname":"' + row['nickname'].ToString() + '",' )
  #              self.Workbench.Append( '"locationname":"' + row['locationname'].ToString() + '",' )
  #              self.Workbench.Append( '"tagZero":"' + row['tagZero'].ToString() + '",' )
  #              self.Workbench.Append( '"lat":"' + row['lat'].ToString() + '",' )
  #              self.Workbench.Append( '"lon":"' + row['lon'].ToString() + '"},\n')

  #          # remove last chars because they are not used, gringo
  #          if self.Workbench.Length > len('"items":['):
  #             self.Workbench.Length = self.Workbench.Length - 2
  #          self.Workbench.Append('\n],')

  #      except Exception,e:
  #          self.log.w2lgError(traceback.format_exc())


  #  # ***********************************************************************************************************************************************
  #  # createCityList   : define a list of postcode-areas in the neighbourhood . the function will add the list to the JSON-object 
  #  #
  #  # 10.03.2013  - bervie -     initial realese
  #  # ***********************************************************************************************************************************************
  #  def createCityList( self ):
  #      try:
  #          self.log.w2lgDvlp('CacheDataSource.createCityList( self ) has been called ! ')
  #          self.log.w2lgDvlp('CacheDataSource.createCityList( self ) loc url param   : ' + str(self.Page.Request.QueryString['Loc']))

  #          # check for country or city. if only a country is given we load all items 
  #          # for a given countrycode like 'de|' for germany or 'at|' for austria

  #          areaSize  = WebConfigurationManager.AppSettings["areaSize"].ToString()
  #          callParam = self.Page.Request.QueryString['Loc'].split(',')
  #          cntry     = callParam[0].ToString().strip()
  #          postcd    = callParam[1].ToString().strip()
  #          city      = self.Page.Request.QueryString['City'].strip()

  #          self.log.w2lgDvlp( 'createCityList parameter :   country : ' + unicode(cntry) + ' ; postcode : ' + unicode(postcd) + ' ; city : ' + unicode( city ) + ' ; areasize (form web.config ) : ' + str(areaSize) )
  #          self.LocationList = self.geoSrc.getPlacesByPlacename( cntry, postcd, city, areaSize )

  #          # if no cities were found LocationList is None 
  #          if ( self.LocationList == None ) or ( len( self.LocationList ) == 0 ):
  #              self.LocationList = None
  #              return False

  #          # the data of the cities in th neighbourhood are added to the result-string (which is a class-attribute)
  #          self.Workbench.Append('\n"places": [\n')
  #          if len(self.LocationList) == 0:
  #              self.Workbench.Append('{}\n]')
  #              return

  #          for loc in self.LocationList:
  #              dstnc = '"NULL"'
  #              if loc[8] != None:
  #                  dstnc = unicode(loc[8])

  #              self.Workbench.Append( '{' )
  #              self.Workbench.Append( '"locSelector":"' + unicode(loc[0]) + '",' )
  #              self.Workbench.Append( '"mongoID":"' + unicode(loc[1]) + '",' )
  #              self.Workbench.Append( '"countryCode":"' + unicode(loc[2]) + '",' )
  #              self.Workbench.Append( '"postCode":"' + unicode(loc[3]) + '",' )
  #              self.Workbench.Append( '"placeName":"' + unicode(loc[4]) + '",' )
  #              self.Workbench.Append( '"latitude":' + unicode(loc[5]) + ',' )
  #              self.Workbench.Append( '"longitude":' + unicode(loc[6]) + ',' )
  #              self.Workbench.Append( '"COUNTRYandCITY":"' + unicode(loc[7]) + '",' )
  #              self.Workbench.Append( '"distance":' + dstnc + '},\n')

  #          self.Workbench.Length = self.Workbench.Length -2
  #          self.Workbench.Append('\n],\n')

  #          return True

  #      except Exception,e:
  #          self.log.w2lgError(traceback.format_exc())


  #  # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
  #  # function .addConfigParam  :   add the configuration parametzer needed by the ListExtractor
  #  #
  #  # 21.07.2013   - bervie-      initial realese
  #  # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
  #  def addConfigParam( self ):
  #      try:
  #          self.log.w2lgDvlp('CachedDataSource.addConfigParam() called !')

  #          self.Workbench.Append('\n"config":')
  #          self.Workbench.Append( '{' )

  #          self.CrsCmd
  #          self.ActvSliceIdx
  #          self.AmntSnd
            
  #          self.Workbench.Append( '"ItemType":"'    + self.param['ItemType'] + '",' )
  #          self.Workbench.Append( '"SliceActive":"' + self.ActvSliceIdx.ToString() + '",' )
  #          self.Workbench.Append( '"CrsCmd":"'      + self.CrsCmd.ToString() + '"' )

  #          self.Workbench.Append( '}\n' )

  #      except Exception,e:
  #          self.log.w2lgError(traceback.format_exc())


  #  # ***********************************************************************************************************************************************
  #  # createTagList  : generate a lsit of tags from the given url-parameter
  #  #
  #  # 10.03.2013  - bervie -     initial realese
  #  # 14.08.2013  - bervie -     add leading '§' to rubric-tags 
  #  #                            it was removed before transmission from client to server
  #  # 15.08.2013  - bervie -     ussing-tag-cache functions
  #  #
  #  # ***********************************************************************************************************************************************
  #  def createTagList( self ):
  #      try:
  #          tagIds = []
  #          tagLst = self.param['Tags'].strip().lower().split(',')

  #          if tagLst[0] != System.String.Empty : tagLst[0] = '§' + tagLst[0].upper()       # leading '§' are removed before transmission to AJAX-fnct. add it again and turn tag to upper. caommand-tags MUST be UPPER
  #          tagIds = self.taggs.askForTagIdxList( tagLst )

  #          return tagIds

  #      except Exception,e:
  #          self.log.w2lgError(traceback.format_exc())







# *******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
# *******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
#tool = LOCALCachedDataSource( Page )
tool = CachedDataSource( Page )




# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 07.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    # try:
    # tool.log.w2lgDvlp('dataSource__cache.aspx.py->Page_Load(sender, e) has been called !')
    tool.pgLoad()
    return 

    #except Exception,e:
    #    tool.log.w2lgError(traceback.format_exc())
