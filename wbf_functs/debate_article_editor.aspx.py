#  
# editor.aspx.py 
#  
# the webform is used for creating new job offers for the community. user can define the location, the typ of the job and the time of action
#
#  03.10.2012   bevie    initial realese
#  
import System.DateTime
import System.Drawing.Color
import System.Guid
import traceback                    # for better exception understanding
import re                           # for finding the taggs
import mongoDbMgr                   # father : the acces to the database

from System.Web.Configuration import *
from srvcs.ItemDebateMsg import ItemDebateMsg
tool = ItemDebateMsg( Page )

mongoId = Page.Request.QueryString['item'] 
Page.ViewState['MongoID'] = mongoId             # used in the helper-classes. do not delete
rootElem = tool.itemTbl.Rows.Find( mongoId )    # load row into global var

# ------------------------------------------------------------------------------------------------------------------------------------------------##__aspn.net ------------------------------------------------
# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 18.03.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    try:
        rlnkUrl = System.String.Empty

        # hide the main-user-interface after a button-click and show  a please-wait sedativ
        tool.ui.getCtrlTree( Page.Master )
        tool.ui.hideFormAfterClick()

        if not Page.IsPostBack :
            ## user must be logged in
            #tool.usrDt.checkUserRigths( Page, 'free')

            # check checkbox if the user is logged-in and has an abo for the current debate
            if tool.usrDt.isLoggedIn():
                aboId = CheckIfAboExists()
                if aboId:
                    chkBx = tool.ui.findCtrl( Page.Master, 'cxbx_email_abo')
                    chkBx.Checked = True

            # if user is NOT looged in we switch to the visitor-webform
            else:
                rlnkUrl = Page.ResolveUrl(WebConfigurationManager.AppSettings['DetailsForStrangers']) 
                rlnkUrl += '?item=' + mongoId

            if rlnkUrl == System.String.Empty:
                chain = tool.chainLoad( mongoId , 'DEBATE_HEADER' )
                tool.ui.getCtrl( 'divShowThread').InnerHtml = chain['html']   # get the chain of messages for this discussion

                if tool.data.has_key('heading'):
                    Page.ViewState['PAGE_NAME'] = tool.data['heading'].ToString() 
                else:
                    Page.ViewState['PAGE_NAME'] = 'nejoba Bekanntmachung'

                # copy additional infos of thios item
                cltInfo = System.Globalization.CultureInfo('de-DE')
                Page.Header.Title = 'nejoba: ' +  chain['subject'].ToString()
                tool.ui.getCtrl( 'lbl_heading').Text        = chain['subject'].ToString() 
                tool.ui.getCtrl( 'lbl_nickname').Text       = chain['nickname'].ToString()
                tool.ui.getCtrl( 'lbl_creationTime').Text   = chain['creationTime'].ToLocalTime().ToString('d',cltInfo) 
                tool.ui.getCtrl( 'lbl_city').Text = chain['locationname'].ToString()

                if chain['from'] != System.DateTime.MinValue :
                    tool.ui.getCtrl( 'lbl_FromDate').Text = chain['from'].ToLocalTime().ToString('d',cltInfo) 
                else:
                    tool.ui.getCtrl( 'lbl_FromDate_lable').Visible = False

                if chain['till'] != System.DateTime.MinValue :
                    tool.ui.getCtrl( 'lbl_TillDate').Text = chain['till'].ToLocalTime().ToString('d',cltInfo) 
                else:
                    tool.ui.getCtrl( 'lbl_TillDate_lable').Visible = False

                #prepare the map-display
                if mongoId is not None:
                    coords = tool.getCoords(mongoId)
                    if coords is None:
                        # hide the map if not needed
                        tool.ui.findCtrl( Page, 'MAP_AREA').Visible = False
                    else:
                        # set the coords for javascript-functions
                        tool.ui.findCtrl( Page.Master, 'lbl_map_lon').Text = coords[0]
                        tool.ui.findCtrl( Page.Master, 'lbl_map_lat').Text = coords[1]

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())

    # if user isn't looged in he can only see the stuff in the "show_for_strangers" webform
    if rlnkUrl != System.String.Empty :
        Response.Redirect( rlnkUrl )


# ------------------------------------------------------------------------------------------------------------------------------------------------##__handler ------------------------------------------------
# ***********************************************************************************************************************************************
# HndlrButtonClick      : handler for button-clicks
#
# 18.11.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def HndlrButtonClick(sender, e):
    try:
        urlNext = None                          # redirection-url

        if sender.ID == 'btnPublish':
            # save to item.base; the cache and detail-collection
            newId = tool.save ()            

            # add the new item to the job-trial-thread ( for jobs )
            newElem  = tool.itemTbl.Rows.Find( newId )
            tool.chainAdd( rootElem, newElem, 'DEBATE_HEADER' )

            # send mails to the guys having an abo
            tool.notify( rootElem, newElem )
            
            # get the thread and update the UI with the new inserted item
            LoadDebateThread()            

        elif sender.ID == 'cxbx_email_abo':
            # set or reset a abonement for a discussion
            ChangeAbo()

        elif sender.ID == 'btnGetPremiumAccount':
            urlNext = Page.ResolveUrl(WebConfigurationManager.AppSettings['StartPayment']) 

        elif sender.ID == 'btnBecomeMember':
            urlNext = Page.ResolveUrl(WebConfigurationManager.AppSettings['CreateAccount']) 

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())

    if urlNext != None :
        Response.Redirect(urlNext)


# ------------------------------------------------------------------------------------------------------------------------------------------------##__functions ------------------------------------------------
# ***********************************************************************************************************************************************
# LoadDebateThread      : load the debate-thread ( full html of all stuff )
#
# 15.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def LoadDebateThread():
    try:
        meat = tool.chainLoad( mongoId , 'DEBATE_HEADER' )['html']
        canvas = tool.ui.findCtrl( Page.Master, 'divShowThread' )
        canvas.InnerHtml = meat

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ***********************************************************************************************************************************************
# ChangeAbo      : an abo is like a bookmark. the item can be found in a list by the user. he can receive mails for it
#
# 15.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def ChangeAbo():
    try:
        tool.log.w2lgDbg("ChangeAbo started ")

        chkBx = tool.ui.findCtrl( Page.Master, 'cxbx_email_abo')
        stts = "n.a."
        if chkBx.Checked:
            # check if abo allready exist. in that case we do not need a n abo again
            aboId = CheckIfAboExists()
            if aboId: return

            userId          = tool.usrDt.getItem('_id')
            debateId        = Page.ViewState['MongoID']
            userGuid        = tool.usrDt.getItem('GUID')
            userMail        = tool.usrDt.getItem('email')
            userLangCode    = tool.usrDt.getItem('languagecode')

            # ...if no entry found add a new abo for the current user
            wrtData = {}
            wrtData.update({ 'userId'       : userId       })
            wrtData.update({ 'debateId'     : debateId     })
            wrtData.update({ 'GUID'         : userGuid     })
            wrtData.update({ 'email'        : userMail     })
            wrtData.update({ 'languagecode' : userLangCode })

            # try to write a document #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  
            writing = {}
            writing.update({'collection':'user.abo'})
            writing.update({'slctKey':None})
            writing.update({'data' : wrtData })
            inserted = tool.insertDoc(writing)

        else:
            # check if abo allready exist
            aboId = CheckIfAboExists()
            if not aboId: return

            delet = {}
            delet.update({'collection':'user.abo'})
            delet.update({'slctVal':aboId})
            deletedId = tool.delDoc(delet)
            tool.log.w2lgDbg("ABO just been deleted : " + deletedId )

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ***********************************************************************************************************************************************
# CheckIfAboExists      : returns _id if there is already an abo for the user/debate
#
# 15.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def CheckIfAboExists():
    try:
        hasAbo      = None
        userId      = tool.usrDt.getItem('_id')
        debateId    = Page.ViewState['MongoID']

        # check if there is already a abo for the user
        accesor = {}
        accesor.update({'collection':'user.abo'})
        accesor.update({'slctKey':'userId'})
        accesor.update({'slctVal':userId})
        length = tool.slctDocs(accesor)
            
        for doc in accesor['data']:
            debateAlreadyOrdered =  doc['debateId'].ToString()
            tool.log.w2lgDbg("Debate found in the user.abo-collection : " + debateAlreadyOrdered)
            if debateAlreadyOrdered == debateId:
                tool.log.w2lgDbg("Hurray for ABO ; Debate-ID  : " + debateAlreadyOrdered)
                hasAbo = doc['_id'].ToString()
                break

        return hasAbo

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())




