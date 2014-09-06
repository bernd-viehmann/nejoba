#  
#
#  
from System.Web.Configuration import *
import System.Data
import System.Collections
from System.Web.Configuration import *
import clr
import traceback                    # for better exception understanding

# import srvcs.tls_Billing
# tool = srvcs.tls_Billing.Billing( Page )

from srvcs.tls_WbFrmClasses import BillingTool      # helper class for all payment-webforms
tool = BillingTool(Page)


tool.ui.getCtrlTree( Page.Master )
startFrame         = tool.ui.getCtrl('divStartFrame')
initSmallBusiness  = tool.ui.getCtrl('divInitSmallBusiness')
initBigCompany     = tool.ui.getCtrl('divInitBigCompany')

dataDict = {}

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
            # tool.usrDt.checkUserRigths(Page, 'free')

            startFrame.Visible        = True
            initSmallBusiness.Visible = False
            initBigCompany.Visible    = False

        tool.errorMessage('')
    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return


# ***********************************************************************************************************************************************
# HndlrButtonClick    : handler for button-click-events. chose button by ID
#
# in this webform only a redirection will be done depending on the button, that were pressed
#
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# there are 2 url-parameter used:
#
# duration=1            for one month premium-time
# duration=12           for one year of premium-time
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# employee=-1           for a private service-provider or a mini-company     10 EUR/month
# employee=0            for a company without extra-employees to pay         15 EUR/month
# employee=XX           number of employees of the company                 ( 15 EUR + XX * 5 EUR )/month
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#
# 18.11.2012  - bervie -     initial realese
#
# ***********************************************************************************************************************************************
def HndlrButtonClick(sender, e):
    try:
        urlNext = None

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        # open different div on same webform 
        # btn_smallTrade
        # btn_bigCompany
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        # btn_bank_small_month
        # btn_bank_small_year
        # btn_bank_big_month
        # btn_bank_big_year
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        # btn_payPal_small_month
        # btn_payPal_small_year
        # btn_payPal_big_month
        # btn_payPal_big_year
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - frames of the machine
        # divStartFrame
        # divInitSmallBusiness
        # divInitBigCompany
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

        tool.log.w2lgDvlp('Default.aspx.py->HndlrButtonClick ID of pressed button : ' + sender.ID)

        if "btn_smallTrade" == sender.ID:
            # toogle on the hidden-DIV to order a small-company-premium-account 
            startFrame.Visible        = False
            initSmallBusiness.Visible = True
            initBigCompany.Visible    = False
            return 

        elif "btn_bigCompany" in sender.ID:
            # toogle on the hidden-DIV to order a big-company-premium-account 
            startFrame.Visible        = False
            initSmallBusiness.Visible = False
            initBigCompany.Visible    = True
            return 

        # decide what webform should be called next
        if "_payPal_" in sender.ID:
            urlNext = WebConfigurationManager.AppSettings['InitPayPalPayment']
        elif "_bank_" in sender.ID:
            urlNext = WebConfigurationManager.AppSettings['PrintMoneyTransfer']

        # get the num of employees that are in the database
        numOfEmployees = unicode(tool.ui.getCtrl('txbx_employees').Text)

        # check input of user --  START  -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        if not numOfEmployees.isnumeric():
            tool.errorMessage(tool.ui.getCtrl('msg_notNumericInput').Text)
            return
        if int(numOfEmployees) != int( float( numOfEmployees ) ):
            tool.errorMessage(tool.ui.getCtrl('msg_useIntegerVals').Text)
            return
        if int(numOfEmployees) < 0 :
            tool.errorMessage(tool.ui.getCtrl('msg_useIntegerVals').Text)
            return
        # check input of user --  END   -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

        

        # define the url-parameter for the next webform
        if sender.ID == "btn_bank_small_month":
            days            = '31'
            numOfEmployees  = '-1'
            moneyAmount     = '9.95'
            #urlNext += '?days=31&employees=-1&amount=9.95'

        if sender.ID == "btn_bank_small_year":
            days            = '365'
            numOfEmployees  = '-1'
            moneyAmount     = '99.95'
            #urlNext += '?days=365&employees=-1&amount=99.95'

        if sender.ID == "btn_bank_big_month":
            days            = '31'
            moneyAmount     = '14.95'
            #urlNext += '?days=31&employees=' + numOfEmployees + '&amount=' + moneyAmount

        if sender.ID == "btn_bank_big_year":
            days            = '365'
            moneyAmount     = '149.95'
            # urlNext += '?days=365&employees=' + numOfEmployees + '&amount=' + moneyAmount

        if sender.ID == "btn_payPal_small_month":
            days            = '31'
            numOfEmployees  = '-1'
            moneyAmount     = '9.95'
            #urlNext += '?days=31&employees=-1&amount=9.95'

        if sender.ID == "btn_payPal_small_year":
            days            = '365'
            numOfEmployees  = '-1'
            moneyAmount     = '99.95'
            # urlNext += '?days=365&employees=-1&amount=99.95'

        if sender.ID == "btn_payPal_big_month":
            days            = '31'
            moneyAmount     = '14.95'
            # urlNext += '?days=31&employees=' + numOfEmployees + '&amount=' + moneyAmount

        if sender.ID == "btn_payPal_big_year":
            days            = '365'
            moneyAmount     = '149.95'
            # urlNext += '?days=365&employees=' + numOfEmployees + '&amount=' + moneyAmount

        # calculate money-amount if needed
        if int(numOfEmployees) > 0:
            moneyAmount = tool.calcMoneyAmount(numOfEmployees, int(days) )  # calculate the money thet user have to pay to be a part of the neighbourhood

        urlNext += '?days=' + days + '&employees=' + numOfEmployees + '&amount=' + moneyAmount

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return

    if urlNext != None :
        Response.Redirect( Page.ResolveUrl( urlNext ) )





# ------------------------------------------------------------------------------------------------------------------------------------------------##__handler ------------------------------------------------


# ***********************************************************************************************************************************************
# copyToSessionCache : store payment-infos into session for webforms 'pay_banktransfer.aspx' and 'pay_payPalOrder.aspx'
#
# 18.11.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
#def copyToSessionCache():
#    try:
#        # add static pay-pal vars
#        dataDict['BusinessEmail']       = WebConfigurationManager.AppSettings['PayPalBusinessEmail']
#        dataDict['NoShipping']          = WebConfigurationManager.AppSettings['PayPalNoShipping']
#        dataDict['NoNote']              = WebConfigurationManager.AppSettings['PayPalNoNote']
#        dataDict['CurrencyCode']        = WebConfigurationManager.AppSettings['PayPalCurrencyCode']
#        dataDict['UndefinedQuantity']   = WebConfigurationManager.AppSettings['PayPalUndefinedQuantity']
#        dataDict['NotifyUrl']           = WebConfigurationManager.AppSettings['PayPalNotifyUrl']
#        dataDict['bankcode']            = WebConfigurationManager.AppSettings['bankcode']
#        dataDict['accountnumber']       = WebConfigurationManager.AppSettings['accountnumber']
#        dataDict['accountowner']        = WebConfigurationManager.AppSettings['accountowner']
#        dataDict['language_code']       = tool.usrDt.getItem('languagecode').ToString().upper()
        

#        # add dynamic vals
#        if tool.ui.getCtrl('rdb_year').Checked == True:
#            dataDict['price' ] = 99.90 
#            dataDict['days'  ] = 367  
#        else:
#            dataDict['price' ] = 9.95 
#            dataDict['days'  ] = 32

#        now                 = System.DateTime.UtcNow
#        procedureNumber     = tool.getProcedureNumber( now )
#        userId              = tool.usrDt.getItem('_id').ToString()
#        usermail            = tool.usrDt.getItem('email').ToString()

#        dataDict['ItemName']            = usermail
#        dataDict['ItemNumber']          = procedureNumber
#        dataDict['On0']                 = 'n.a.'
#        dataDict['On1']                 = 'n.a.'

#        Page.Session['BILLING_INFO'] = dataDict.copy()

#    except Exception,e:
#        tool.log.w2lgError(traceback.format_exc())
#        return




# ***********************************************************************************************************************************************
# HndlrButtonClick    : handler for button-click-events. chose button by ID
#
# 18.11.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
#def HndlrButtonClick(sender, e):
#    try:
#        nextUrl = None
#        dataDict    =  {}
#        price       = 0.0                                             
#        days        = 0

#        # get the type of payment
#        if tool.ui.getCtrl('payment_paypal').Checked == True:
#            nextUrl = WebConfigurationManager.AppSettings[ 'InitPayPalPayment' ]
#            dataDict['payment_type'] = 'PayPal' 
#        else:
#            nextUrl = WebConfigurationManager.AppSettings[ 'PrintMoneyTransfer' ]
#            dataDict['payment_type'] = 'BankTransfer'

#        copyToSessionCache()                    # store data in session-cache for displaying stuff in the next webform

#        # call selected webform ( banking-transaction or pay-pal )
#        nextUrl = Page.ResolveUrl( nextUrl )
#        tool.log.w2lgDvlp('pay_start.aspx.py : redirecting to webform           : ' + nextUrl )


#    except Exception,e:
#        tool.log.w2lgError(traceback.format_exc())
#        return

#    if nextUrl != None :
#        Response.Redirect( nextUrl )



