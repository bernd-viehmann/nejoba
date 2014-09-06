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
from System import UriPartial
import System.Data
import System.Web
import System.Collections
import System.Text

import clr
import traceback                    # for better exception understanding
import mongoDbMgr                   # father : the acces to the database

tool = mongoDbMgr.mongoMgr(Page)

# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 07.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    try:
        context = System.Web.HttpContext.Current


        #context.Response.Clear()
        #context.Response.ContentType = "text/csv; charset=UTF-8"
        #context.Response.Charset = "UTF-8"
        #context.Response.ContentEncoding = System.Text.Encoding.UTF8
        #context.Response.BinaryWrite( System.Text.Encoding.UTF8.GetPreamble() )
        #context.Response.Flush()

        #s = unicode("Mömo Käßtschaktor")
        #bytes = System.Text.Encoding.UTF8.GetBytes(s);
        #context.Response.OutputStream.Write(bytes, 0, bytes.Length);
        #context.Response.HeaderEncoding = System.Text.Encoding.GetEncoding("utf-8")


        context.Response.ContentType = "text/plain; charset=utf-8"
        context.Response.Charset = "utf-8"
        context.Response.Clear()
        context.Response.HeaderEncoding = System.Text.UTF8Encoding(False)
        context.Response.ContentEncoding = System.Text.UTF8Encoding(False)
        # write som stuff to the context

        dataSource = Page.Application['njbMapUser']

        text = dataSource.load()

        out = System.Text.Encoding.UTF8.GetBytes(text)
        context.Response.OutputStream.Write(out, 0, out.Length)
        context.Response.Flush()


    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())

    context.Response.End()
