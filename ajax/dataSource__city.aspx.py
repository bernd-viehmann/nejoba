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
from srvcs.tls_WbFrmClasses import CachedCitySource

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

#class LOCALCachedCitySource( mongoDbMgr.mongoMgr ):
#    '''
#    todo

#    '''


#    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
#    # constructor. 
#    #
#    # 30.08.2013   -bervie-    initial realese
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

#            tagpart = self.Page.Request.QueryString['tagpart']
#            query = self.Page.Request.QueryString['query'].lower()

#            result = []
#            for citySrc in self.geoSrc.locTable.Rows:
#                city = citySrc['placename'].ToString().lower()
                
#                if city.startswith(query):
#                    itemToAdd = '"' + citySrc['placename'   ].ToString() + '"'
#                    if itemToAdd not in result:
#                        result.Add( itemToAdd )

#            # generate result string
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

#tool = LOCALCachedCitySource( Page )
tool = CachedCitySource( Page )


# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 07.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    # try:
    tool.log.w2lgDvlp('dataSource__city.aspx.py->Page_Load(sender, e) has been called !')
    tool.pgLoad()
    return 

    #except Exception,e:
    #    tool.log.w2lgError(traceback.format_exc())
