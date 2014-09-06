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
import traceback                                    # for better exception understanding
import mongoDbMgr                                   # father : the acces to the database


from System.Web.Configuration import *
import traceback                                # for better exception understanding
import random
import mongoDbMgr                               # father : the acces to the database

class UserHome(mongoDbMgr.mongoMgr):

    # ***********************************************************************************************************************************************
    # constructor : call the base class constructor to initialize log, cache, ui-helper and page-member
    #
    # 28.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def __init__(self, pg):
        try:
            mongoDbMgr.mongoMgr.__init__(self, pg)      # wake up papa ; mother njbTools is included by inheritance!
            self.ui.getCtrlTree( self.Page.Master )
            self.log.w2lgDvlp('constructor of class UserHome(Page) aufgefufen!')
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # FillUsrCache : fillup the user-data-cache IF NOT ALREADY DONE
    #
    # 28.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def FillUsrCache(self, mail):
        try:
            self.log.w2lgDvlp('UserHome( .. ) called FillUsrCache with mail ' +  unicode(mail) )

            # check if user-cache is empty. if so load data from the db
            if not self.usrDt.isLoggedIn():
                self.usrDt.LoadUserData( mail )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())

tool = UserHome(Page)



# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#                    this is the webform that loads the user-data after log-in or initial user-creation. it is the main-entry of the
#                    application. 
#
# 10.12.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    try:
        # hide the main-user-interface after a button-click and show  a please-wait sedativ
        tool.ui.getCtrlTree( Page.Master )
        tool.ui.hideFormAfterClick()

        if( not Page.IsPostBack ):

            # the "start-page" of the user user_home.aspx is called after user-account was created or user has logged in. 
            # these webform set the Session-Atribute 'LOGGEDIN_EMAIL'. 
            # this startpage checks if these attribute is set and loads the data of the user into the session-cache.
            # after this the attribute in the session  is deleted and user can work with his account.
            if Page.Session['LOGGEDIN_EMAIL'] != None:
                mail = unicode(Session['LOGGEDIN_EMAIL'])
                tool.FillUsrCache(mail)

            # user must be logged in
            tool.usrDt.checkUserRigths( Page, 'free')


    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ***********************************************************************************************************************************************
# HndlrButtonClick    : handler for button-click-events. chose button by ID
#
# 18.11.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def HndlrButtonClick(sender, e):
    try:
        urlNext = None

        tool.log.w2lgDvlp('Default.aspx.py->HndlrButtonClick ID of pressed button : ' + sender.ID)

        switcher = {}
        switcher.update( {"btn_helpwanted"  : "OfferJob"         } )
        switcher.update( {"btn_debate"      : "debateProjector"  } )  
        switcher.update( {"btn_work"        : "SearchJob"        } )
        switcher.update( {"btn_help"        : "OnlineHelp"       } )
        switcher.update( {"btn_ownlists"    : "ChooseList"       } )
        switcher.update( {"btn_premium"     : "StartPayment"     } )

        if sender.ID not in switcher.keys():
            return

        urlNext = WebConfigurationManager.AppSettings[ switcher[sender.ID] ]
        tool.log.w2lgDvlp('Default.aspx.py jump-url in click-handler : ' + urlNext)

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return

    if urlNext != None :
        Response.Redirect( Page.ResolveUrl( urlNext ) )

