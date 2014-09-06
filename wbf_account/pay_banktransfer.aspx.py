#  
#
#  
#  
from System.Web.Configuration import *
import traceback                                    # for better exception understanding
import System.Web.Security
from System import DateTime
from System.Text import StringBuilder

#import srvcs.tls_Billing
#tool = srvcs.tls_Billing.Billing( Page )

from srvcs.tls_WbFrmClasses import BillingTool  # helper class for all payment-webforms
tool = BillingTool(Page)


# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 03.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    try:
        # hide the main-user-interface after a button-click and show  a please-wait sedativ
        tool.ui.getCtrlTree( Page.Master )
        tool.ui.hideFormAfterClick()

        if( not Page.IsPostBack ):
            # user must be logged in
            tool.usrDt.checkUserRigths(Page, 'free')

            # copy URL-params into viewstate to avoid billing-manipulation
            amount = Page.Request.QueryString['amount']
            days = Page.Request.QueryString['days']
            emps = Page.Request.QueryString['employees']

            Page.ViewState['MONEY_AMOUNT']  = amount
            Page.ViewState['PREMIUM_DAYS']  = days
            Page.ViewState['NUM_EMPLOYS' ]  = emps

            if int(emps) <= 0:
                emps = tool.ui.getCtrl('msg_noEmployessGiven').Text

            tool.ui.getCtrl('txbx_duration').Text      = days
            tool.ui.getCtrl('txt_employees').Text      = emps
            tool.ui.getCtrl('txbx_amountOfMoney').Text = amount


        PrintInfo()

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ***********************************************************************************************************************************************
# HndlrButtonClick      : handler for button-clicks
#
# 05.02.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def HndlrButtonClick(sender, e):
    try:
        nextUrl = None

        # user want to change his order
        if sender.ID == 'btn_changeOrder':
            nextUrl = Page.ResolveUrl( WebConfigurationManager.AppSettings[ 'StartPayment' ] )
            tool.log.w2lgDvlp('pay_banktransfer.aspx.py : redirecting to webform           : ' + nextUrl )

        # user want to order. be happy. money will come soon
        if sender.ID == 'btn_acceptData':
            # cretae order-number; store stuff in database
            #tool.prepareOrder()

            tool.ui.getCtrl('checkInputDiv').Visible = False
            tool.ui.getCtrl('PaymentDetails').Visible = True


        # accept check box must be checked : user confirms data-protection and buisiness-rules
        if sender.ID == 'ckbx_accept':
            chkBx       = tool.ui.getCtrl('ckbx_accept')
            payBtn      = tool.ui.getCtrl('btnStartBankPay')
            acceptDiv   = tool.ui.getCtrl('accept')
            orderDiv    = tool.ui.getCtrl('order')
            if chkBx.Checked == 1:
                payBtn.Enabled = 1
                acceptDiv.Visible = 0
                orderDiv.Visible = 1
            else:
                payBtn.Enabled = 0

        # when banking-order payment was initiated store data in billing.initial
        if sender.ID == 'btnStartBankPay':
            tool.storeInitialPayment()

            # go on to the information webform that payment was started
            nextUrl = Page.ResolveUrl( WebConfigurationManager.AppSettings[ 'paymentFinished' ] )
            tool.log.w2lgDvlp('pay_banktransfer.aspx.py : redirecting to webform           : ' + nextUrl )
 
    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())

    if nextUrl != None :
        Response.Redirect( nextUrl )


# ***********************************************************************************************************************************************
# GetConfig  : put the infos for the bank-transfer into the webform
#
# 04.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def PrintInfo():
    try:
        tool.ui.getCtrl('txbx_bankname').Text       = WebConfigurationManager.AppSettings[ 'bankname' ]
        tool.ui.getCtrl('txbx_accountowner').Text   = WebConfigurationManager.AppSettings[ 'accountowner' ]

        tool.ui.getCtrl('txbx_bankcode').Text       = WebConfigurationManager.AppSettings[ 'bankcode' ]
        tool.ui.getCtrl('txbx_accountnumber').Text  = WebConfigurationManager.AppSettings[ 'accountnumber' ]
        
        tool.ui.getCtrl('txbx_designated_one').Text = WebConfigurationManager.AppSettings[ '' ]
        tool.ui.getCtrl('txbx_designated_two').Text = WebConfigurationManager.AppSettings[ '' ]

        tool.ui.getCtrl('txbx_amount').Text         = Page.ViewState['MONEY_AMOUNT']


    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return



















