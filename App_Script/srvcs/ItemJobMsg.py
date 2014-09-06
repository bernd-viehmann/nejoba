# ***********************************************************************************************************************************************
# ItemJobMsg.py :        class for job-messaged added 
# 
# parent :                  Item
#
#
#  16.01.2012  - bervie -     initial realese
#
#
# ***********************************************************************************************************************************************
import clr
clr.AddReference('MongoDB.Bson')
clr.AddReference('MongoDB.Driver')
from MongoDB.Bson import *
from MongoDB.Driver import *
from System.Web.Configuration import *
from System.Net.Mail import *
from System.Net import NetworkCredential 
from System import UriPartial
import System.Text
import traceback            # for better exception understanding
import System.Guid
import re

from Item import *       # base-class for data-objects

class ItemJobMsg ( Item ):
    '''
    ItemJobMsg is the helper to organize discussions between provider and offerer
    '''

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # constructor. 
    #
    #
    # 16.01.2013   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def __init__(self, page ):
        try:
            Item.__init__(self, page )                              # wake up papa ; mother njbTools is included by inheritance!
            self.objTypIdx = self.getObjectTypeId( 'JOB_MSG' )      # define what kind of object we have by setting the object_type_id as integer
            self.log.w2lgDvlp( 'ItemJobMsg.constructor called' )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # chainCreateHeader()  :   creating a new header for a discussion-thread : DEBATE_HEADER
    #
    # parameter     :  rootElemID           : the root-elem we are looking for
    # return        :  createdHeaderId      : the new created ID of the Header
    #
    # HINT : the initiator is the creator of the root-element. in this case it is the guy ho asked his neighbouhood for some help
    #        the prospect is the guy who is interested in the job. he can become the service-provider if the initiator choose him
    #
    #        for every JOB_ROOT / PROSPECT-user there is one dialog-hread
    #
    #
    # 21.12.2012   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def chainCreateHeader( self, rootElemRow, HdrTypeName ):
        try:
            clientGuid = rootElemRow['_creatorGUID'].ToString()
            clnt = {}
            clnt.update({'collection':'user.final'})
            clnt.update({'slctKey'   :'GUID'})
            clnt.update({'slctVal'   :clientGuid})
            self.readDoc(clnt)
            clntData = clnt['data'] 

            #for itm in clientUser['data'].items():
            #    strOut = 'Loaded for CLIENT in ItemJobMsg.chainCreateHeader : ' + unicode(itm[0]) + '\t' + unicode(itm[1]) + '\t'
            #    self.log.w2lgDvlp(strOut)

            # 1. write the detail-data COLLECTION ITEM:JOB_HEADER
            detailData = {}
            detailData['client_GUID']           = clntData['GUID'].ToString()
            detailData['client_ID']             = clntData['_id'].ToString()
            detailData['client_mail']           = clntData['email'].ToString()
            detailData['client_local']          = clntData['languagecode'].ToString()
            detailData['client_nickname']       = clntData['nickname'].ToString()
            detailData['client_postcode']       = clntData['postcode'].ToString()
            #detailData['client_city']           = clntData['city'].ToString()
            
            detailData['client_lastVisit']      = None
            detailData['client_lastUpdate']     = None

            detailData['provider_GUID']         = self.usrDt.getItem('GUID').ToString()
            detailData['provider_ID']           = self.usrDt.getItem('_id').ToString()
            detailData['provider_mail']         = self.usrDt.getItem('email').ToString()
            detailData['provider_local']        = self.usrDt.getItem('languagecode').ToString()
            detailData['provider_nickname']     = self.usrDt.getItem('nickname').ToString()
            detailData['provider_postcode']     = self.usrDt.getItem('postcode').ToString()
            #detailData['provider_city']         = self.usrDt.getItem('city').ToString()
            detailData['provider_lastVisit']    = None
            detailData['provider_lastUpdate']   = None

            detailData['creation_time']         = System.DateTime.UtcNow
            # DO NOT FORGET : ADD AN INDEX IN THE USER.FINAL-COLLECTION FOR 'guid'
            # DO NOT FORGET : ADD AN INDEX IN THE USER.FINAL-COLLECTION FOR 'guid'
            # DO NOT FORGET : ADD AN INDEX IN THE USER.FINAL-COLLECTION FOR 'guid'
            # DO NOT FORGET : ADD AN INDEX IN THE USER.FINAL-COLLECTION FOR 'guid'

            headerTypeId = self.getObjectTypeId(HdrTypeName)
            destColl = self.typeToColl[headerTypeId]
            storeDataDct = {'collection': destColl ,'slctKey': None ,'data': detailData}
            detlObjId = self.insertDoc(storeDataDct)

            self.log.w2lgDvlp("ItemDebateMsg.chainCreateHeader detail-data-element ID is : " + unicode( detlObjId )+ " ;Type of data : " + unicode( self.getObjectTypeString(headerTypeId)) + ' coll : ' + destColl )

            # 2. write the item.base-data
            self.objTypIdx       = headerTypeId
            self.objectDetailID  = detlObjId
            self.followerID      = None 
            
            self.parentID        = self.Page.ViewState['ROOTELEM_ID']       # parent_id of header points to the root_element of the thread
            self.rootElemGUID    = System.Guid.NewGuid().ToString('N')      
            
            headerId = self.storeGeneralBase()
            self.setMembrAttrb()                        # reset member-attributes after insert.
            hdrRw = self.itemTbl.Rows.Find( headerId )
            return hdrRw

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # notify()  :   send an email to the potentioal business-partner
    #
    # parameter     :   rootElemRow         : the root-element ROW 
    #                   newItemRow          : the message-row inserted just before
    #
    # return        :   createdHeaderId     : the new created ID of the Header
    #
    # HINT : the client   is the creator of the root-element. in this case it is the guy ho asked his neighbouhood for some help
    #        the provider is the guy who is interested in the job. he can become the service-provider if the initiator choose him
    #
    #        for every JOB_ROOT / PROSPECT-user there is one dialog-hread
    #
    # 27.01.2013   - bervie-      initial realese
    # 07.03.2013   - bervie-      FIX  add the GUID of the client ti find the correct thread for a purchaser
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def notify( self, rootElemRow, newItemRow ):
        try:
            # get header for the discussion
            headerGUID = newItemRow['_rootElemGUID'].ToString()
            hdrElemRow = self.itemTbl.Select("_rootElemGUID = '" + headerGUID + "' AND objectType = 5")[0]
            
            headDtl = {}
            detailId = hdrElemRow['_objectDetailID'].ToString()
            headDtl.update({'collection':'item.JOB_HEADER' })
            headDtl.update({'slctKey'   :'_id' })
            headDtl.update({'slctVal'   :detailId })
            self.readDoc(headDtl)
            headerData = headDtl['data'] 

            # debugging output _____________________________________________________________________________________________________________________________________________________________________________________________
            for item in headerData:
                key    = item.ToString()
                value  = headerData[key].ToString()
                self.log.w2lgDvlp('ItemJobMsg.sendNotification loaded header-data in sendNotification : ' +  key + ' -  : ' + value )
            # debugging output _____________________________________________________________________________________________________________________________________________________________________________________________

            dataDtl = {}
            dataDtlId = newItemRow['_objectDetailID'].ToString()
            dataDtl.update({'collection':'item.JOB_MSG' })
            dataDtl.update({'slctKey'   :'_id' })
            dataDtl.update({'slctVal'   :dataDtlId })
            self.readDoc(dataDtl)
            msgData = dataDtl['data'] 

            # debugging output _____________________________________________________________________________________________________________________________________________________________________________________________
            for item in msgData:
                key    = item.ToString()
                value  = msgData[key].ToString()
                self.log.w2lgDvlp('ItemJobMsg.sendNotification loaded message-data in sendNotification : ' +  key + ' -  : ' + value )
            # debugging output _____________________________________________________________________________________________________________________________________________________________________________________________

            currentUserGuid     = self.usrDt.getItem('GUID')
            clientGUID          = headerData['client_GUID'].ToString()
            provider_GUID       = headerData['provider_GUID'].ToString()
            
            body                =  'Anbieter : ' + hdrElemRow['nickname'].ToString() 
            body                += " schreibt : <br/><br/>"
            body                += msgData['body'].ToString()

            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
            # added 24.02.2013
            #header  = hdrElemRow['subject'].ToString()
            header  = rootElemRow['subject'].ToString()
            
            nextUrl = self.Page.ResolveUrl(WebConfigurationManager.AppSettings['AddToTrialThread'])
            lnkAdr  =  self.Page.Request.Url.GetLeftPart( UriPartial.Authority )
            lnkAdr  += nextUrl + '?item=' + hdrElemRow['_parentID'].ToString() 
            self.log.w2lgDvlp('ItemJobMsg.notify link-address  : ' + lnkAdr )
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

            # figure out who should receive the notification-mail. the client or the provider
            sendToAddr = ''
            replyToAdr = ''
            if currentUserGuid == clientGUID:
                sendToAddr = headerData['provider_mail'].ToString()
                replyToAdr = headerData['client_mail'].ToString()
            else:
                sendToAddr = headerData['client_mail'].ToString()
                replyToAdr = headerData['provider_mail'].ToString()

                # FIX 07.03.2013 add the GUID of the client ti find the correct thread for a purchaser
                lnkAdr  += "&offerer=" + currentUserGuid

            self.log.w2lgDvlp('ItemJobMsg.sendNotification receiver of the notificaton is  : ' + sendToAddr )

            self.sendNote( sendToAddr, replyToAdr, header, body, lnkAdr )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # sendNote()  :   send an email to the potentioal business-partner.reply-address is set to the email of the other participant
    #
    # parameter     :   rootElemRow         : the email we should send to
    #                   hdrElemRow          : the header-row
    #
    # return        :   createdHeaderId     : the new created ID of the Header
    #
    #
    # 27.01.2013   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def sendNote( self, sendTo, replyToAdr, headertext, bodyText, lnkAdr ):
        try:
            smtpServer      = WebConfigurationManager.AppSettings['smtpServer']
            smtpUser        = WebConfigurationManager.AppSettings['smtpUser']
            smtpPwd         = WebConfigurationManager.AppSettings['smtpPwd']
            fromAddr        = WebConfigurationManager.AppSettings['cptchSndrAdrss']

            # load the template for the HTML-mail
            tmpltPath = self.Page.Server.MapPath( WebConfigurationManager.AppSettings['JobTrialHtmlBody'] )
            self.log.w2lgDvlp('ItemJobMsg->sendNote   = ' + tmpltPath )
            file = open(tmpltPath)
            mailBody = file.read()
            file.close()

            #Create A New SmtpClient Object
            mailClient              = SmtpClient(smtpServer,25)
            mailClient.EnableSsl    = True
            mailCred                = NetworkCredential()
            mailCred.UserName       = smtpUser
            mailCred.Password       = smtpPwd
            mailClient.Credentials  = mailCred

            msg = MailMessage()
            msg.From                = MailAddress(fromAddr)
            msg.ReplyTo             = MailAddress(replyToAdr)
            msg.To.Add( MailAddress( sendTo ) )
            msg.SubjectEncoding     = System.Text.Encoding.UTF8
            msg.BodyEncoding        = System.Text.Encoding.UTF8
            msg.IsBodyHtml          = True

            mailSubj = self.ui.getCtrl('msg_mailSubject').Text + headertext
            mailBody = mailBody.replace('###header###' , headertext   )
            mailBody = mailBody.replace('###body###'   , bodyText     )
            mailBody = mailBody.replace('###link###'   , lnkAdr      )
            self.log.w2lgDvlp('ItemJobMsg.sendNote link-address  : ' + lnkAdr )

            msg.Subject = mailSubj
            msg.Body = mailBody

            mailClient.Send(msg)

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())
                 
                 
                 
                 
                 
                 
                 
                 
                 
                         





