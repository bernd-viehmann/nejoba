#  dataSource__cache.aspx.py
#  
#  AJAX datasource webform to send the data from app-cache for some given parameters
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
from srvcs.tls_WbFrmClasses import CachedHashTagSource

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

#class LOCALCachedHashTagSource( mongoDbMgr.mongoMgr ):
#    '''
#    todo
#    '''


#    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
#    # constructor. 
#    #
#    # member-attributes 
#    #
#    #    self.Workbench        string-builder for generating the return-output
#    #    self.LocationList     string with the locations-detail-data in the neighboerhood
#    #    self.CrsCmd       amount of items-cursor. stores the offset from the end of cache-item-table
#    #    self.ActvSliceIdx    the data in the database is devides in pages. page 0 is the mem-cache in the application-cache of IIS. 
#    #                          the following pages are in the database. they are seperated by dates. so every page has a defined num 
#    #                          of days which belonges to it
#    #
#    # 27.06.2013   - bervie-      initial realese
#    # 27.07.2013   - bervie-      added self.SlicesCached : the definition of how many slides are stored in the cache. when the number
#    #
#    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
#    def __init__(self, page ):
#        try:
#            mongoDbMgr.mongoMgr.__init__(self, page )                                                                       # wake up papa ; mother njbTools is included by inheritance!

#        except Exception,e:
#            self.log.w2lgError(traceback.format_exc())


#    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
#    # pgLoad is called from PageLoad to create the data-collection
#    #
#    # 27.06.2013   - bervie-      initial realese
#    #
#    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
#    def pgLoad( self ):
#        try:
#            # self.log.w2lgDvlp('# # # CachedDataSource.pgLoad( self ) has been called !')

#            # prepare UTF-8 output
#            context = System.Web.HttpContext.Current
#            context.Response.ContentType = "text/plain; charset=utf-8"
#            context.Response.Charset = "utf-8"
#            context.Response.Clear()
#            context.Response.HeaderEncoding = System.Text.UTF8Encoding(False)
#            context.Response.ContentEncoding = System.Text.UTF8Encoding(False)

#            result = []
#            query = self.Page.Request.QueryString['query'].lower()
#            for tg in self.taggs.TaggList:
#                tag = tg.ToString().lower()
#                if tag.startswith(query):
#                    result.Add( '"' + tag + '"' )
#            rsltStrng = ', '.join(result)
#            text = '{ "options": [' + rsltStrng + ']}'

#            out = System.Text.Encoding.UTF8.GetBytes(text)
#            context.Response.OutputStream.Write(out, 0, out.Length)
#            context.Response.Flush()
#            context.Response.End()

#        except Exception,e:
#            self.log.w2lgError(traceback.format_exc())



# *******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
# *******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
tool = CachedHashTagSource( Page )
#tool = LOCALCachedHashTagSource( Page )



# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 07.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    # try:
    tool.log.w2lgDvlp('dataSource__hashtag.aspx.py->Page_Load(sender, e) has been called !')
    tool.pgLoad()
    return 

    #except Exception,e:
    #    tool.log.w2lgError(traceback.format_exc())
