#  
#
#  
#  
from System.Web.Configuration import *

import traceback                                    # for better exception understanding
import mongoDbMgr                                   # father : the acces to the database


tool = mongoDbMgr.mongoMgr( Page )



# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 18.03.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    pgTitle =  Page.ToString()

    tool.log.w2lgDvlp('agb.aspx found page-title : ' + pgTitle )

    pass

