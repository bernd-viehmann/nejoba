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
import traceback                                    # for better exception understanding
import mongoDbMgr                                   # father : the acces to the database
import System.Text
from System.Net.Mail import *
from System.Net import NetworkCredential 


tool = mongoDbMgr.mongoMgr( Page )


# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 18.03.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    try:
        # tool.ui.getCtrlTree( Page.Master )
        # tool.ui.hideFormAfterClick()

        pass

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return



# ***********************************************************************************************************************************************
# HndlrButtonClick    : handler for button-click-events. chose button by ID
#
# 18.11.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def HndlrButtonClick(sender, e):
    try:
        url = None

        if sender.ID == 'btnSendReport':
            # tool.log.w2lgDvlp('der schickma buttton wurde gerade gedr?ckt')
            sendToNejobaTeam()

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return

    if url != None :
        Response.Redirect(urlNext)




# ***********************************************************************************************************************************************
# sendToNejobaTeam    : send a mesage to the nejoba-team via email-helper-class
#
# 18.11.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def sendToNejobaTeam():
        try:
            # get the textdata  for mail
            tool.ui.getCtrlTree( Page.Master )
            mailSubj = tool.ui.getCtrl('txbHeader').Text 
            mailBody = tool.ui.getCtrl('txtMain').Text 

            smtpServer      = WebConfigurationManager.AppSettings['smtpServer']
            smtpUser        = WebConfigurationManager.AppSettings['smtpUser']
            smtpPwd         = WebConfigurationManager.AppSettings['smtpPwd']
            fromAddr        = WebConfigurationManager.AppSettings['cptchSndrAdrss']

            #Create A New SmtpClient Object
            mailClient              = SmtpClient(smtpServer,25)
            mailClient.EnableSsl    = True
            mailCred                = NetworkCredential()
            mailCred.UserName       = smtpUser
            mailCred.Password       = smtpPwd
            mailClient.Credentials  = mailCred

            sendTo = 'info.nejoba@gmail.com'
            msg = MailMessage()
            msg.From                = MailAddress('anonymus@anonymus.org')
            msg.ReplyTo             = MailAddress('anonymus@anonymus.org')
            msg.To.Add( MailAddress( sendTo ) )
            msg.SubjectEncoding     = System.Text.Encoding.UTF8
            msg.BodyEncoding        = System.Text.Encoding.UTF8
            msg.IsBodyHtml          = False


            msg.Subject = mailSubj
            msg.Body = mailBody

            mailClient.Send(msg)

            # toogle divs to show message was send
            tool.ui.getCtrl('mailSendSuccesfullyMessage').Visible = True
            tool.ui.getCtrl('divEditArea').Visible = False

        except Exception,e:
            tool.log.w2lgError(traceback.format_exc())
                 

