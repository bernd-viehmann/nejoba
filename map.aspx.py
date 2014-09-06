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

import System.Data
import System.Collections
import clr
import traceback                    # for better exception understanding
import mongoDbMgr                   # father : the acces to the database
from System import UriPartial




# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 07.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    try:
        # check if we have a string for the mail-adress of the user
        if type( Page.Session['LOGGEDIN_EMAIL']) != type('a'):
            # no user is logged-in.show controls for loggin or create a new user
            pass
        else:
            # user is already logged-in. show controls for changing the user-data or logging-of
            pass



        #if (Session["LOGGEDIN_EMAIL"] != null)
        #{
        #    accountdiv.Visible = true;
        #    logindiv.Visible = false;

        #    // change the link "start_page" from Default.aspx to user_home.aspx
        #    // hyLnk_nejoba.NavigateUrl = "~/wbf_account/user_home.aspx";
        #}
        #else
        #{
        #    accountdiv.Visible = false;
        #    logindiv.Visible = true;

        #    hyLnk_userHome.Visible = false;
        #    hyLnk_maintainAccount.Text = "Konto erstellen";
        #}














    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ***********************************************************************************************************************************************
# HandlBtnClick   : handler for button-clix
#
# 07.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def HandlBtnClick( sender, e ):
    url = None
    try:
        pass

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())

    if url != None:
        Response.Redirect(Page.ResolveUrl(url))

