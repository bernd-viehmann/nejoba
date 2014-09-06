# ***********************************************************************************************************************************************
# ItemDebateMsg.py :        class for messages added to an debate-chain
# 
# parent :                  Item
#
#
#  16.01.2012  - bervie -     initial realese
#
#
# ***********************************************************************************************************************************************
from System.Web.Configuration import *
from System import Text
from System.Net import *
from System.Net.Mail import *
from System import UriPartial
import System.Guid
import traceback            # for better exception understanding
import re
import clr
clr.AddReference('MongoDB.Bson')
clr.AddReference('MongoDB.Driver')
from MongoDB.Bson import *
from MongoDB.Driver import *

from Item import *       # base-class for data-objects
from ItemDebateHeader import *       # base-class for data-objects


class ItemDebateMsg ( Item ):
    '''
    ItemDebateMsg is a member of a debate-thread
    '''

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # constructor. 
    #
    #
    # 16.01.2013   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def __init__(self, page ):
        try:
            Item.__init__(self, page )                                      # wake up papa ; mother njbTools is included by inheritance!
            self.objTypIdx = self.getObjectTypeId( 'DEBATE_MSG' )        # define what kind of object we have by setting the object_type_id as integer

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # chainCreateHeader()  :   creating a new header for a discussion-thread : DEBATE_HEADER
    #
    # parameter     :  rootElemID           : the root-elem we are looking for
    # return        :  createdHeaderId      : the new created ID of the Header
    #
    # HINT : the initiator is the creator of the root-element. in this case it means the guy who started the discussion
    #        the prospect is the guy who is taking part in the discussion
    #
    #
    #
    #
    # 21.12.2012   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def chainCreateHeader( self, rootElemRow, HdrTypeName ):
        try:
            self.log.w2lgDvlp("ItemDebateMsg.chainCreateHeader started with root_elem_id " + rootElemRow['_ID'].ToString() + " , objType = " + HdrTypeName )

            rootElemId      = rootElemRow['_ID'].ToString() 
            headerTypeId    = self.getObjectTypeId('DEBATE_HEADER')

            # 1. write the detail-data-ID
            detailData = {}
            detailData['initiator_GUID']    = rootElemRow['_creatorGUID'].ToString()
            detailData['prospect_GUID']     = self.usrDt.getItem('GUID')
            detailData['creation_time']     = System.DateTime.UtcNow

            destColl = self.typeToColl[headerTypeId]
            storeDataDct = {'collection': destColl ,'slctKey': None ,'data': detailData}
            detlObjId = self.insertDoc(storeDataDct)

            self.log.w2lgDvlp("ItemDebateMsg.chainCreateHeader detail-data-element ID is : " + unicode( detlObjId )+ " ;Type of data : " + unicode( self.getObjectTypeString(headerTypeId)) )

            # 2. write the item.base-data
            self.objTypIdx       = headerTypeId
            self.objectDetailID  = detlObjId
            self.parentID        = self.Page.ViewState['MongoID']
            self.rootElemGUID    = System.Guid.NewGuid().ToString('N')      
            self.locationID      = rootElemRow['_locationID']

            headerId = self.storeGeneralBase()
            self.setMembrAttrb()                        # reset member-attributes after insert.
            hdrRw = self.itemTbl.Rows.Find( headerId )
            return hdrRw

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # notify : function send emails to the participants on a discussion 
    #
    # parameter   : rootElemRow   :   the row with data of the root-element
    #
    #
    # 03.10.2012   bervie  initial realease
    # ***********************************************************************************************************************************************
    def notify(self, rootElemRow, lastItemRow ):
        try:
            self.log.w2lgDvlp("ItemDebateMsg.notify called for  root_elemnt : " + rootElemRow['_ID'].ToString() )
            self.log.w2lgDvlp("ItemDebateMsg.notify called for  last_item   : " + lastItemRow['_ID'].ToString() )

            # load the template for the HTML-mail
            tmpltPath = self.Page.Server.MapPath( WebConfigurationManager.AppSettings['DebateNotifyHtmlBody'] )
            self.log.w2lgDvlp('ItemDebateMsg->sendMail   = ' + tmpltPath )
            file = open(tmpltPath)
            mailBody = file.read()
            file.close()

            # 2. get all abonements for the current debate
            # debateID == _ID of root_element
            accesor = {}
            accesor.update({'collection':'user.abo' })
            accesor.update({'slctKey':'debateId'    })
            accesor.update({'slctVal':rootElemRow['_ID'].ToString() })
            length = self.slctDocs(accesor)

            abonentAdresses = MailAddressCollection()
            userMail = self.usrDt.getItem('email')
            for doc in accesor['data']:
                #if debateAlreadyOrdered == debateId:
                userId       = doc['userId'].ToString()
                debateId     = doc['debateId'].ToString()
                GUID         = doc['GUID'].ToString()
                email        = doc['email'].ToString()
                languagecode = doc['languagecode'].ToString()
                self.log.w2lgDbg("ItemDebateMsg.notify Found in the user.abo-collection : userId       :" + userId )
                self.log.w2lgDbg("ItemDebateMsg.notify Found in the user.abo-collection : debateId     :" + debateId )
                self.log.w2lgDbg("ItemDebateMsg.notify Found in the user.abo-collection : GUID         :" + GUID )
                self.log.w2lgDbg("ItemDebateMsg.notify Found in the user.abo-collection : email        :" + email )
                self.log.w2lgDbg("ItemDebateMsg.notify Found in the user.abo-collection : languagecode :" + languagecode )

                if email != userMail : abonentAdresses.Add( MailAddress(email) )    # do not send this to yourself

            # 3. get the text that was added to the debate-thread
            msgDetailIdx = lastItemRow['_objectDetailID'].ToString()
            accesor = {}
            accesor.update({'collection': 'item.DEBATE_MSG'})
            accesor.update({'slctVal'   : msgDetailIdx})
            readId = self.readDoc(accesor)
            msgBody =  accesor['data']['body'].ToString()
            
            # 4. prepare message
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
            # added 24.02.2013
            nextUrl = self.Page.ResolveUrl(WebConfigurationManager.AppSettings['AddArticleToDebate'])
            lnkAdr  =  self.Page.Request.Url.GetLeftPart( UriPartial.Authority )
            lnkAdr  += nextUrl + '?item=' + rootElemRow['_ID'].ToString() 
            self.log.w2lgDvlp('ItemJobMsg.notify link-address  : ' + lnkAdr )
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

            mailBody = mailBody.replace('###header###' , self.ui.getCtrl('msg_mailSubject').Text )
            mailBody = mailBody.replace('###body###'   , msgBody)
            mailBody = mailBody.replace('###link###'   , lnkAdr)
            
            # 6.....and finaly send the messages to the abonennts
            self.sendMail( mailBody, abonentAdresses)

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # sendMail : to finalize the user-registration an email with a captcha code is send to the user. the user must enter this captcha code and 
    #            his password in the verification webform AppSettings['captchaWebForm']. the message for that mail is porepared here
    #
    #            IMPORTANT: it migth be necesary to change the iis configuration
    #            http://forums.asp.net/t/1404427.aspx/1
    #
    #            http://celestialdog.blogspot.com/2011/04/how-to-send-e-mail-using-ironpython.html
    #
    # 25.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def sendMail( self , body , toAddrs ):
        try:
            smtpServer = WebConfigurationManager.AppSettings['smtpServer']
            smtpUser = WebConfigurationManager.AppSettings['smtpUser']
            smtpPwd = WebConfigurationManager.AppSettings['smtpPwd']
            fromAddr = WebConfigurationManager.AppSettings['cptchSndrAdrss']

            #Create A New SmtpClient Object
            mailClient              = SmtpClient(smtpServer,25)
            mailClient.EnableSsl    = True
            mailCred                = NetworkCredential()
            mailCred.UserName       = smtpUser
            mailCred.Password       = smtpPwd
            mailClient.Credentials  = mailCred

            msg = MailMessage()
            msg.From                = MailAddress(fromAddr)
            for toAddr in toAddrs:
                msg.To.Add(toAddr)
            msg.SubjectEncoding     = Text.Encoding.UTF8;
            msg.BodyEncoding        = Text.Encoding.UTF8;
            msg.IsBodyHtml          = True

            msg.Subject = 'Bertifft nejoba'
            msg.Body = body

            mailClient.Send(msg)

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


