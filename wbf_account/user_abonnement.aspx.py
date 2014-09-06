#  
# user_announces shows the anfragen from the logged in user
#  
#
from System.Data import *
from System.Web.Configuration import *

import System.Collections
import clr
import traceback                    # for better exception understanding
import mongoDbMgr                   # father : the acces to the database

tool = mongoDbMgr.mongoMgr(Page)


# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 18.03.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    try:
        # hide the main-user-interface after a button-click and show  a please-wait sedativ
        tool.ui.getCtrlTree( Page.Master )
        tool.ui.hideFormAfterClick()

        if( not Page.IsPostBack ):
            # user must be logged in
            tool.usrDt.checkUserRigths(Page, 'free')

            # display the announces of the user
            loadAbonnements()

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())




# ------------------------------------------------------------------------------------------------------------------------------------------------##__handler ------------------------------------------------
# ***********************************************************************************************************************************************
# HndlrReactionClick : handler for buttons that initiate a reaction on a given announcement
#
# 18.03.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def HndlrReactionClick(sender, e):
    try:
        url = None

        commandPartList = sender.ClientID.ToString().split('_') 
        aboId           = commandPartList[-1]                       # mongo_ID of item to call
        commandStrng    = commandPartList[-2]                       # command to select webform
        idList          = Page.ViewState['ID_LIST']
        aboMogoId       = idList[ System.Convert.ToInt32(aboId) ]   # id of the offeror

        if commandStrng == "CallDebate" :
            url = WebConfigurationManager.AppSettings["AddArticleToDebate"]   + '?item=' + aboMogoId
            tool.logMsg('user_debates.aspx.HndlrReactionClick : redirect to' + unicode( url ) )

        if commandStrng == 'DelDebate':
            deleteAbo( aboMogoId )

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())

    if url:
        Response.Redirect( Page.ResolveUrl( url ) )




# ------------------------------------------------------------------------------------------------------------------------------------------------##__init ------------------------------------------------
# ***********************************************************************************************************************************************
# loadOfferorList : load all offerors for the current job !!
#
# 30.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def loadAbonnements():
    try:
        # get all abonements of the user
        userId = tool.usrDt.getItem('_id')

        accesor = {}
        accesor.update({'collection':'user.abo' })
        accesor.update({'slctKey': 'userId'    })
        accesor.update({'slctVal': userId })
        length = tool.slctDocs(accesor)
        
        debates = []
        for doc in accesor['data']:
            debates.Add( doc['debateId'].ToString() )
            tool.logMsg('abo-mongoID found : ' + unicode(doc['debateId'].ToString()))

        destUrl = WebConfigurationManager.AppSettings["AddArticleToDebate"]
        itemTable = tool.appCch.dtSt.Tables["items"]
        resltTbl = itemTable.Clone()

        for mngId in debates:
            tool.logMsg('mngId we are locking for : ' + unicode(mngId))
            row = itemTable.Rows.Find(mngId)
            
            if row is None:
                tool.log.w2lgError('in der user_abo collection wurde ein unbekannter beitrag entdeckt. er ist wohl in der item.base geloescht aber nicht in der user.abo')
                tool.log.w2lgError('mongo_ID des beitrags' + str(mngId))
            else:
                resltTbl.ImportRow(row)
                navLnk = destUrl + '?item=' + mngId
                resltTbl.Rows[ resltTbl.Rows.Count - 1]['tagZero'] = navLnk
                # HACK tagZero in the temporary result-table will store the link to the detailview
                # added 11-08-2013 bervie

        # 2. bind repeater to data-table
        if resltTbl.Rows.Count == 0:
            # no data was found
            tool.errorMessage('<br/><br/>Es wurden keine Daten gefunden !<br/><br/><br/>')
        else:
            # bind repeater to result data-table
            repeater = tool.gtCtl('repAboList')
            repeater.DataSource = resltTbl
            repeater.DataBind()

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ***********************************************************************************************************************************************
# loadOfferorList : load all offerors for the current job !!
#
# param : offertable
#
# 30.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def createTable( offerorTbl ):
    try:
        # 1. create a data-table for the offerors that are offering :-)
        col = offerorTbl.Columns.Add("_ID",          System.String )
        col = offerorTbl.Columns.Add("nickname",     System.String )
        col = offerorTbl.Columns.Add("postcode",     System.String )
        col = offerorTbl.Columns.Add("city",         System.String )
        col = offerorTbl.Columns.Add("_creatorGUID", System.String )
        
        # 2. get the list of headers 
        objTypConfig    = WebConfigurationManager.AppSettings['objectTypes']
        strngSeperator  = WebConfigurationManager.AppSettings['stringSeperator']
        objectTypes     = objTypConfig.split(strngSeperator)
        objectType      = objectTypes.index('JOB_HEADER')                       # get the object_type_ID of JOB_OFFERS
        parentId        = Page.ViewState['itemId']

        itemTbl = tool.appCch.dtSt.Tables['items']                           # the data-source
        slctStr = "_parentID = '" + parentId + "' AND objectType = " + str(objectType)
        sortStr = "creationTime ASC"
        rows = itemTbl.Select( slctStr , sortStr )
        creatorLst = []                                                            # the _parnentID in the header points to the ID of the root_element which we are looking for
        for row in rows: 
            creatorGuid = row['_creatorGUID'].ToString()
            creatorLst.Add( creatorGuid )

        # 3. get the offeror-date from the database
        for item in creatorLst:
            # try to read a document #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  
            accesor = {}
            accesor.update({'collection':'user.final'})
            accesor.update({'slctKey' : 'GUID'})
            accesor.update({'slctVal' : item})
            loaded = tool.readDoc(accesor)

            mongoId         = accesor['data']['_id'].ToString() 
            nickname        = accesor['data']['nickname'].ToString() 
            postcode        = accesor['data']['postcode'].ToString() 
            city            = accesor['data']['city'].ToString() 
            creatorGuid     = item

            row = offerorTbl.NewRow()
            row['_ID']          = mongoId
            row['nickname']     = nickname
            row['postcode']     = postcode
            row['city']         = city
            row['_creatorGUID'] = creatorGuid
            offerorTbl.Rows.Add(row)

            #tool.logMsg('job_trial_list.aspx.loadOfferorList() : Found _id      : ' + mongoId    )
            #tool.logMsg('job_trial_list.aspx.loadOfferorList() : Found nickname : ' + nickname   )
            #tool.logMsg('job_trial_list.aspx.loadOfferorList() : Found postcode : ' + postcode   )
            #tool.logMsg('job_trial_list.aspx.loadOfferorList() : Found city     : ' + city       )

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ------------------------------------------------------------------------------------------------------------------------------------------------##functions ------------------------------------------------
# ***********************************************************************************************************************************************
# deleteAbo : delete an abo for the given user and refresh the displaying
#
# param:    mongoIdOfDebate  RootElemId
#
# 18.03.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def deleteAbo( mongoIdOfDebate ):
    try:
        # check if abo allready exist
        aboId = CheckIfAboExists(mongoIdOfDebate)
        if not aboId: return

        delet = {}
        delet.update({'collection':'user.abo'})
        delet.update({'slctVal':aboId})
        deletedId = tool.delDoc(delet)
        tool.log.w2lgDbg("ABO just been deleted : " + deletedId )

        # update abo-list of user after deletition was done
        loadAbonnements()

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ***********************************************************************************************************************************************
# CheckIfAboExists      : returns _id if there is already an abo for the user/debate
#
# 15.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def CheckIfAboExists(mongoIdOfDebate):
    try:
        hasAbo      = None
        userId      = tool.usrDt.getItem('_id')
        debateId    = mongoIdOfDebate

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




