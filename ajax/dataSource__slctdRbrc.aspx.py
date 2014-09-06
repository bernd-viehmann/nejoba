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

#from srvcs.tls_WbFrmClasses import CachedRubricSource

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

class LOCALCachedRubricSource( mongoDbMgr.mongoMgr ):
    '''
    todo

    '''
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # constructor. 
    #
    # 30.08.2013   -bervie-    initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def __init__(self, page ):
        try:
            mongoDbMgr.mongoMgr.__init__(self, page )                                                                       # wake up papa ; mother njbTools is included by inheritance!

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # pgLoad is called from PageLoad to create the data-collection
    #
    # 27.06.2013   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def pgLoad( self ):
        try:
            # self.log.w2lgDvlp('# # # CachedDataSource.pgLoad( self ) has been called !')
            # prepare UTF-8 output
            context = System.Web.HttpContext.Current
            context.Response.ContentType = "text/plain; charset=utf-8"
            context.Response.Charset = "utf-8"
            context.Response.Clear()
            context.Response.HeaderEncoding = System.Text.UTF8Encoding(False)
            context.Response.ContentEncoding = System.Text.UTF8Encoding(False)

            source = ''
            # the key is selected in the matrix-manager : $("a[id*='CoPlaBottom_hyli_select']").click(function (event) { ...............
            switchr = { 'ANNONCE'          : 'ANNONCE_MATRIX' ,
                        'ASSOCIATION'      : 'ASSOCIATION_MATRIX' ,
                        'BUSINESS'         : 'BUSINESS_MATRIX' ,
                        'DEMOCRACY'        : 'DEMOCRACY_MATRIX' ,
                        'EVENT'            : 'EVENT_MATRIX' ,
                        'HOBBY'            : 'HOBBY_MATRIX' ,
                        'INITIATIVE'       : 'INITIATIVE_MATRIX' ,
                        'LOCATION'         : 'LOCATION_MATRIX' ,
                        'LONELY_HEARTS_AD' : 'LONELY_HEARTS_AD_MATRIX' ,
                        'PET'              : 'PET_MATRIX' ,
                        'RIDE_SHARING'     : 'RIDE_SHARING_MATRIX' ,
                        'STARTUP'          : 'STARTUP_MATRIX' ,
                        'SWAP'             : 'SWAP_MATRIX' ,
                        'FAMILY'           : 'FAMILY_MATRIX' }

            if 'rbrc' in self.Page.Request.QueryString:
                rbrc = self.Page.Request.QueryString['rbrc'].strip()
                if rbrc in switchr.keys():
                    selctor = switchr[rbrc]
                    source = self.ui.rubricDict[selctor] 

            out = System.Text.Encoding.UTF8.GetBytes(source)
            context.Response.OutputStream.Write(out, 0, out.Length)
            context.Response.Flush()
            context.Response.End()

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



# *******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
# *******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************

tool = LOCALCachedRubricSource( Page )
#tool = CachedRubricSource( Page )


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
