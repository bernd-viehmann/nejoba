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

from srvcs.tls_WbFrmClasses import GetCitiesByCountryAndName

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
# get place-list by country-code and city-name
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

#class LOCALGetCitiesByCountryAndName( mongoDbMgr.mongoMgr ):
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
#            # self.log.w2lgDvlp('# # # LOCALGetCitiesByCountryAndName->pgLoad has been called !')

#            # prepare UTF-8 output
#            context = System.Web.HttpContext.Current
#            context.Response.ContentType = "text/plain; charset=utf-8"
#            context.Response.Charset = "utf-8"
#            context.Response.Clear()
#            context.Response.HeaderEncoding = System.Text.UTF8Encoding(False)
#            context.Response.ContentEncoding = System.Text.UTF8Encoding(False)

#            cntryCode = self.Page.Request.QueryString['ctry'].upper()
#            cityName = self.Page.Request.QueryString['city'].upper()

#            queryKey = cntryCode + '|' + cityName

#            temp = System.Text.StringBuilder()              # build the list with all cities
#            result = ''
#            result = []
#            temp.Append('{"cities":[\n')

#            for row in self.geoSrc.locTable.Rows:
#                if row['keyCity'].ToString() == queryKey:
#                    #tool.log.w2lgDvlp('dataSource__countryPostCode.aspx.py   found postcode     ' + row['postalCode'].ToString() )
#                    #tool.log.w2lgDvlp('dataSource__countryPostCode.aspx.py   found placename    ' + row['placeName'].ToString() )
#                    #tool.log.w2lgDvlp('dataSource__countryPostCode.aspx.py   found countrycode  ' + row['countryCode'].ToString() )
#                    #tool.log.w2lgDvlp('dataSource__countryPostCode.aspx.py   found mongoID      ' + row['mngId'].ToString() )
#                    #tool.log.w2lgDvlp('---------------------------------------------------------------------------------------------')

#                    temp.Append( '{' )
#                    temp.Append( '"postalCode":"' + row['postalCode'].ToString() + '",' )
#                    temp.Append( '"placeName":"' + row['placeName'].ToString() + '",' )
#                    temp.Append( '"countryCode":"' + row['countryCode'].ToString() + '",' )
#                    temp.Append( '"mngId":"' + row['mngId'].ToString() + '",' )
#                    temp.Append( '"lat":"' + row['latitude'].ToString() + '",' )
#                    temp.Append( '"lon":"' + row['longitude'].ToString() + '"},\n')

#            if temp.Length == 0:
#                result = '{ "cities":[{}] }'
#            else:
#                temp.Length = temp.Length - 2
#                temp.Append('\n]}')
#                result = temp.ToString()

#            out = System.Text.Encoding.UTF8.GetBytes( result )
#            context.Response.OutputStream.Write(out, 0, out.Length)
#            context.Response.Flush()
#            context.Response.End()

#        except Exception,e:
#            self.log.w2lgError(traceback.format_exc())



# *******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
# *******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************

#tool = LOCALGetCitiesByCountryAndName( Page )
tool = GetCitiesByCountryAndName( Page )


# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 07.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    # tool.log.w2lgDvlp('dataSource__countryPostCode.aspx.py->Page_Load(sender, e) has been called !')
    tool.pgLoad()
    return 
