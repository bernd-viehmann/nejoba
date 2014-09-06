#
# pay_paypalOrder.aspx.py : pay the nejoba bill with paypal
# 
# there is a issue to use a different form inside the main-webform generated from the master-page:
# solution : remove the form-tag from the pay-pal part and use a image-button with postback url to the paypal server
#
# http://stackoverflow.com/questions/2587403/asp-pages-and-paypal-button
# <asp:ImageButton ID="btnPayNow" runat="server" ImageUrl="~/images/Purchase/payNowButton.jpg" PostBackUrl="https://www.paypal.com/cgi-bin/webscr"/>
#
# 
#
#
#  
from System.Web.Configuration import *
import traceback                                    # for better exception understanding
import System.Web.Security
from System import DateTime
from System.Text import StringBuilder

from srvcs.tls_WbFrmClasses import BillingTool      # helper class for all payment-webforms
tool = BillingTool(Page)

pymntData = Page.Session['BILLING_INFO']

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
        
    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ***********************************************************************************************************************************************
# GetConfig  : put the infos for the bank-transfer into the webform
#
# 04.01.2013  - bervie -     initial realese
# ***********************************************************************************************************************************************
def PayPalSettings():
    try:
        paypalform = """
        <input type="hidden" name="cmd" value="_xclick">
        <input type="hidden" name="business" value="###_CONF_business_email_###">
        <input type="hidden" name="item_name" value="###_CONF_item_name_###">
        <input type="hidden" name="item_number" value="###_CONF_item_number_###">
        <input type="hidden" name="amount" value="###_CONF_amount_###">
        <input type="hidden" name="no_shipping" value="###_CONF_no_shipping_###">
        <input type="hidden" name="no_note" value="###_CONF_no_note_###">
        <input type="hidden" name="currency_code" value="###_CONF_currency_code_###">
        <input type="hidden" name="lc" value="###_CONF_language_code_###">
        <input type="hidden" name="bn" value="PP-BuyNowBF">
        <a href="javascript:theForm.__VIEWSTATE.value='';
        theForm.encoding='application/x-www-form-urlencoded';
        theForm.action='https://www.paypal.com/cgi-bin/webscr';theForm.submit();">
           <img src="images/buynow.gif" border="0"></a>
        """

        # 1. get the pay-pal configuration from the web.config!
        confDict = {}
        confDict['###_CONF_business_email_###']      = pymntData['BusinessEmail']
        confDict['###_CONF_no_shipping_###']         = pymntData['NoShipping']
        confDict['###_CONF_no_note_###']             = pymntData['NoNote']
        confDict['###_CONF_currency_code_###']       = pymntData['CurrencyCode'] 
        confDict['###_CONF_notify_url_###']          = pymntData['NotifyUrl']
        confDict['###_CONF_undefined_quantity_###']  = pymntData['UndefinedQuantity']
        confDict['###_CONF_language_code_###']       = pymntData['language_code']

        confDict['###_CONF_item_name_###']           = pymntData['ItemName']
        confDict['###_CONF_item_number_###']         = pymntData['ItemNumber']
        confDict['###_CONF_on0_###']                 = pymntData['On0']
        confDict['###_CONF_on1_###']                 = pymntData['On1']
        confDict['###_CONF_amount_###']              = pymntData['price'].ToString()

        # 2. replace the strings fpr playpal
        for key in confDict:
            # tool.logMsg( ' key          : ' + str(key) + ' value              ' + confDict[key].ToString() )
            paypalform = paypalform.replace(str(key), confDict[key].ToString())
                    
        # 3. insert the data into the UI
        tool.ui.getCtrl('txbx_accountowner').Text       = pymntData['ItemName']
        tool.ui.getCtrl('txbx_billGui').Text            = pymntData['ItemNumber']
        tool.ui.getCtrl('txbx_payedPeriodLength').Text  = System.Convert.ToString(pymntData['days'])
        tool.ui.getCtrl('txbx_amountOfMoney').Text      = System.String.Format("{0:C}", pymntData['price'] )

        return paypalform

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())



# ------------------------------------------------------------------------------------------------------------------------------------------------##__handler ------------------------------------------------
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
            nextUrl = WebConfigurationManager.AppSettings[ 'StartPayment' ] 
            tool.log.w2lgDvlp('pay_banktransfer.aspx.py : redirecting to webform           : ' + nextUrl )

        if sender.ID == 'ckbx_accept':
            chkBx       = tool.ui.getCtrl('ckbx_accept')
            payBtn      = tool.ui.getCtrl('btnPayNow')
            acceptDiv   = tool.ui.getCtrl('accept')
            orderDiv    = tool.ui.getCtrl('order')

            if chkBx.Checked == 1:
                payBtn.Enabled = 1
                acceptDiv.Visible = 0
                orderDiv.Visible = 1
                tool.storeInitialPayment()              # write data to billing.initial collection
            else:
                payBtn.Enabled = 0
 
    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())

    if nextUrl != None :
        Response.Redirect( Page.ResolveUrl( nextUrl ) )




