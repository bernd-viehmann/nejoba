# --- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- -
# --- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- -
# 
# helper-classes for webforms
#
# --- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- -
# --- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- -
import System
import System.Text
import System.Guid
import re
import traceback                                # for better exception understanding
import random
import mongoDbMgr                               # father : the acces to the database
import collections

import clr
clr.AddReference('MongoDB.Bson')
clr.AddReference('MongoDB.Driver')
from MongoDB.Bson import *
from MongoDB.Driver import *
from System.Net import *
from System.Net.Mail import *
from System import UriPartial
from System.Web.Configuration import *
from System.Web.UI.WebControls import LinkButton
from System.Web.UI import LiteralControl

from srvcs.tls_UiHelper import LocDefiner               # location_definer is used by the projectors to handle session-cached location


# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
#
# helper for logIn.aspx.py : the form used to log-in or to change to the account-creation-webform
#  
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -

class LogIn( mongoDbMgr.mongoMgr ):
    # ***********************************************************************************************************************************************
    # constructor : call the base class constructor to initialize log, cache, ui-helper and page-member
    #
    # 28.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def __init__(self, pg):
        try:
            mongoDbMgr.mongoMgr.__init__(self, pg)      # wake up papa ; mother njbTools is included by inheritance!
            self.ui.getCtrlTree( self.Page.Master )
            self.log.w2lgDvlp('constructor of class ConfirmUser(Page) aufgefufen!')

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # CheckLogIn : get the user-data for a given email
    #
    # 28.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def CheckLogIn( self ):
        try:
            goBackUrl = None

            mail = self.ui.getCtrl("txbx_email").Text.strip()
            pwd = self.ui.getCtrl("txbx_password").Text.strip()

            if self.CheckForUser( mail, pwd ) is False: return

            # load data for the user and log him in
            if not self.usrDt.isLoggedIn():
                self.usrDt.LoadUserData( mail )

            # if the LogIn was called from another page inside the application go back to this
            goBackUrl = self.Page.Session['REDIRECT_AFTER_LOGIN']
            self.log.w2lgDvlp('login.aspx : redirect defined in session  : ' + unicode( goBackUrl )  )
            self.log.w2lgDvlp('login.aspx : succesfull login for         : ' + unicode( mail      )  )
            self.log.w2lgDvlp('login.aspx : send user back to page       : ' + unicode( goBackUrl )  )


        except Exception,e:
            self.log.w2lgError(traceback.format_exc())

        if goBackUrl != None:
            self.Page.Response.Redirect( self.Page.ResolveUrl( goBackUrl ) )        # redirect to user home after succesfully log-in. there the user-data will be copied to the session.cache



    # ***********************************************************************************************************************************************
    # CheckForUser : get the user-data for a given email
    #
    # 28.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def CheckForUser( self, mail, pwd ):
        try:
            reply = System.String.Empty

            connection = WebConfigurationManager.AppSettings["mongoConn"]
            dbname = WebConfigurationManager.AppSettings["dbName"]
            server = MongoServer.Create(connection)
            db = server.GetDatabase(dbname)

            collection = db.GetCollection("user.final")
            query = Builders.Query.EQ( "email", mail )
            item = collection.FindOne(query)

            if item is None: 
                # email is not present in the data-base
                
                self.errorMessage(self.ui.getCtrl('lbl_no_data_found').Text)
                self.log.w2lgDvlp('login.aspx : invalid login-email for : ' + unicode(mail))
                return False
            else:
                # check if password is correct
                dataBasePwd = item['password']
                pwdFromUi = self.EncryptSHA512Managed(pwd)
                #self.log.w2lgDvlp('login.aspx : password found in database     :' + unicode(dataBasePwd) )
                #self.log.w2lgDvlp('login.aspx : password crypted form ui       :' + unicode(pwdFromUi) )

                if unicode(pwdFromUi) != unicode(dataBasePwd) :
                    # tool.ui.getCtrl('lbl_explain').Text = tool.ui.getCtrl('lbl_wrong_password').Text
                    self.errorMessage(self.ui.getCtrl('lbl_wrong_password').Text)
                    self.log.w2lgDvlp('login.aspx : incorrect password for mail : ' + unicode(mail) + ':' + unicode(pwd)) 
                    return False

                return True

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


















































# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
#
# helper for user_confirm.aspx.py : the form tht finalyze the user-registrqation-process by copying the registration-data into the final user-collection (user.final)
#  
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
class ConfirmUser(mongoDbMgr.mongoMgr):

    # ***********************************************************************************************************************************************
    # constructor : call the base class constructor to initialize log, cache, ui-helper and page-member
    #
    # attribute:
    #    self.initialData  :  the user-data coming from pre-account-approved-collection  'user.initial'
    #
    # 28.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def __init__(self, pg):
        try:
            mongoDbMgr.mongoMgr.__init__(self, pg)      # wake up papa ; mother njbTools is included by inheritance!
            self.ui.getCtrlTree( self.Page.Master )
            self.log.w2lgDvlp('ConfirmUser( .. ) constructor called')
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # LoadInitialData : load initial data for the user-account from collection user.initial
    #
    # 28.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def LoadInitialData( self, guid ):
        try:
            ctrlDict = {'collection':'user.initial','slctKey':'GUID','slctVal': guid }
            self.readDoc(ctrlDict)
            self.initialData = ctrlDict['data']
            self.Page.ViewState['INITIAL_USER_DATA'] = ctrlDict['data']
            self.ui.getCtrl('txbx_email').Text = self.initialData['email'].ToString()

            #for ky in self.initialData:
            #    self.log.w2lgDvlp('ConfirmUser(Page)  key  : ' + unicode(ky) + ' ;  val : ' + unicode( self.initialData[ky] ) )
            
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())
    

    # ***********************************************************************************************************************************************
    # ActivateAccount : load initial data for the user-account from collection user.initial
    #
    # 28.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def ActivateAccount( self ):
        try:
            self.initialData = self.Page.ViewState['INITIAL_USER_DATA']          # get data from load-on-page-not-postback
            self.CopyToFinalCollection()                                    # put it into the final collection
            self.DeleteInInitialCollection()                                # after account is approved delete it in the initital collection 

            self.LogInAndStart()                                            # go to the home-screen where user will be logged in

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # CopyToFinalCollection : store data of the user into final user-collection
    #
    # 28.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def CopyToFinalCollection( self ):
        try:
            data = {}

            # define accountr as basic-account, which means "not payed"
            accTypConf = WebConfigurationManager.AppSettings['accountRoles']     
            objSeperator = WebConfigurationManager.AppSettings['stringSeperator']     
            
            accountTypes = accTypConf.split(objSeperator)
            accType = []
            accType.Add(accountTypes[0])

            for itm in self.initialData:
                if itm != '_id' and itm != 'creationtime':
                    val = self.initialData[itm]
                    data.Add(itm, val)
                data.Add('creation_time', System.DateTime.UtcNow )
                data.Add('account_roles', accType )

            for itm in data:
                key = itm 
                val = data[itm]
                typDef = unicode(type(data[itm]))
                self.log.w2lgDvlp('for itm in data - key ' + unicode( key ) + ' type : ' + typDef + ' val : ' + unicode( val ) )

            ctrlDict = {'collection':'user.final' }
            ctrlDict.update({'slctKey': None})
            ctrlDict.update({'data': data})

            newId = self.insertDoc(ctrlDict)

            self.log.w2lgDvlp('ConfirmUser( .. ) CopyToFinalCollection succesfully written to collection user.final : ' + unicode( newId ) )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # DeleteInInitialCollection : delete temporary user-registration-data
    #
    # 13.12.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def DeleteInInitialCollection( self ):
        try:
            delet = {}
            delet.update({'collection':'user.initial'})
            delet.update({'slctVal':self.initialData['_id']})
            delItemId = self.delDoc(delet)

            self.log.w2lgDvlp('user_confirm->DeleteInInitialCollection : deleted item : ' + unicode(delItemId))

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # LogInAndStart : go to the home-screen. the session will be initiated here, so user will be logged in
    #
    # 28.11.2011    berndv  initial realese
    # 19.12.2012    berndv  added login via session on next webform !!
    # ***********************************************************************************************************************************************
    def LogInAndStart( self ):
        try:
            url = None

            # on the 'next' webform user_hame.aspx the user-data will be loaded if session-var 
            # 'LOGGEDIN_EMAIL' contains ther email of the user we have created
            self.Page.Session['LOGGEDIN_EMAIL'] = self.ui.getCtrl('txbx_email').Text
            url = self.Page.ResolveUrl( WebConfigurationManager.AppSettings['UserMainPage'] )                        # get link for adding new user

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())

        if url:
            self.Page.Response.Redirect( self.Page.ResolveUrl( url ) )



# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
#
# helper for manging billing in the nejoba-machine
#  
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
class BillingTool(mongoDbMgr.mongoMgr):

    # ***********************************************************************************************************************************************
    # constructor : call the base class constructor to initialize log, cache, ui-helper and page-member
    #
    #
    # 28.02.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def __init__(self, pg):
        try:
            mongoDbMgr.mongoMgr.__init__(self, pg)      # wake up papa ; mother njbTools is included by inheritance!
            self.ui.getCtrlTree( self.Page.Master )
            self.log.w2lgDvlp('BillingTool( .. ) constructor called')

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # ***********************************************************************************************************************************************
    # createOder  : functions initiates a new order-process for a nejoba premium account
    #               function should only run ones to avoid double-order-numbers- this is done with the self.orderInProgress-Flag
    #               if another process is running the function should not statr but wait
    #               if no other order is running the function sets the flag to True to indicate a running order-process
    #               get the current date of the day
    #               get all billing
    #
    #               create a document in the mongo-db billing.initial with the data for the new bill. 
    #
    # param    
    # days         : length of the periode that will be can used as premium-schorschie
    #                an additional day will be added in the function to be contract-save
    #                a month should be 31 days
    #                a year should be 365 days
    #
    # employees    : number of emplyes
    # amount       : amount of money to pay
    #
    #  billing.initial-collection :
    #
    #    _id                = mongo_id 
    #    data_created       = date of creation of the dataset
    #    user_ID            = mongo_id of the user
    #
    #    user_mail          = mail-adress of the user
    #    order_number       = number created as order-number in the form YYYYMMDD.lfdNumber
    #
    #    data_created       = DateTime.UtcNow
    #    time_periode_days  = Number-of-daysthat will be added 
    #    employees          = number of employess in the company 
    #                         -1  : private customer                       :    9.95
    #                          0  : company without additional employees   :   14.95 
    #                         XX  : company with additional employees      :   14.95 + XX * 4.95 (example for month)
    #    amount_money       = total amount of money that should be received from the payment
    #    currency           = EUR / USD / GBP or whatever
    #
    # returns
    # dataDict : dictionary with the stuff written to the db
    #
    # 28.02.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def createOder( self, days, employees, amount):
        '''
        functions create a document in the mongo-db billing.initial with the data for the new bill. 
        will be copied later into billing.final when payed.
        '''
        try:
            # 1. write the data into the collection
            tmp = System.DateTime.UtcNow
            utcDay = System.DateTime( tmp.Year, tmp.Month, tmp.Day )

            writing = {}
            writing['data_created']      = utcDay
            writing['user_ID']           = self.usrDt.getItem('_id')
            writing['user_mail']         = self.usrDt.getItem('mail')
            writing['order_number']      = dateOfOrderNum
            writing['time_periode_days'] = day + 1
            writing['employees']         = employees
            writing['amount_money']      = amount
            writing['currency']          = 'EUR'

            insert = {}
            insert['collection']    = 'billing.initial'
            insert['slctKey']       = None
            insert['data']          = writing
            insertedId              = self.insertDoc(insert)

            # 2. get the procedure-number and store it into the collection
            orderNumber = self.getProcedureNumber(utcDay)

            # 3. update the order-number
            updt = {}
            updt.update({'collection':'billing.initial'})
            updt.update({'slctKey': '_id'              })
            updt.update({'slctVal': insertedId         })
            updt.update({'updatKey': 'order_number'})
            updt.update({'updatVal': orderNumber })
            chngdId = self.updateDoc(updt)

            self.log.w2lgDvlp( 'updated order_number in the billing.initial-collection ' + orderNumber )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # ***********************************************************************************************************************************************
    # getProcedureNmbr : function is used for payment. it creates a procedure-number for use in the payment-process. 
    #                    count the orders this customer made today and create a procedure-number like 'YYYYMMDD-lfdNr'
    #
    # parameter : now : current moment in UTC time
    #
    # returns   : formated string 
    #
    #
    # 05.01.2013  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def getProcedureNumber( self, utcDay ):
        try:
            # 1. get number of of  payment-preperations the user made today
            #
            # IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE 
            # IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE 
            #
            # add an index to collection  'billing.initial' !  !  !  !
            #
            # IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE 
            # IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE 
            #
            #
            #
            #
        
            accesor = {}
            userId = self.usrDt.getItem('_id').ToString()
            accesor.update({'collection':'billing.initial' })
            accesor.update({'slctKey':'data_created'    })
            accesor.update({'slctVal': utcNow })
            prePays = self.slctDocs(accesor)

            # 2. create the procedure-number for this payment ( only valid in combination with the email adress )
            dateOfOrder = utcDay.ToString('yyyyMMdd')
            orderNum    = dateOfOrder + '.' + unicode( prePays )
            return orderNum

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # ***********************************************************************************************************************************************
    # calcMoneyAmount  : this function calculates how much money has to be payed from the customner
    #                    
    #
    # parameter : numberOfEmployees ( self-explaining var-name  :-)
    #
    # returns   : string with the amount of money
    #
    #
    # 05.01.2013  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def calcMoneyAmount( self, numberOfEmployees, duration ):
        try:
            numEmps = float(numberOfEmployees)

            if duration == 31:
                result = (numEmps * 4.95) + 14.95
            elif duration == 365:
                result = (numEmps * 49.95) + 149.95 

            return result.ToString()

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # storeInitialPayment : function saves data of initial payment into the collection 
    #                    
    #
    #  billing.initial-collection :
    #    user_ID
    #    data_created
    #    time_periode_days
    #    amount_money
    #    currency
    #    status
    #    procedure_number
    #
    # parameter : now : current moment in UTC time
    #
    # returns   : formated string 
    #
    #
    # 05.01.2013  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    #def storeInitialPayment( self ):
    #    try:
    #        data = self.Page.Session['BILLING_INFO']

    #        for item in data.keys():
    #            key = item
    #            val = data[key]
    #            self.wrtLog( ' tls_Billing->storeInitialPayment   key : ' + key + '- \t -' + System.Convert.ToString( val ))

    #        writing = {}
    #        writing['user_ID']              = self.usrDt.getItem('_id')
    #        writing['data_created']         = System.DateTime.UtcNow
    #        writing['time_periode_days']    = data['days']
    #        writing['amount_money']         = data['price']
    #        writing['currency']             = data['CurrencyCode']
    #        writing['procedure_number']     = data['ItemNumber']

    #        insert = {}
    #        insert['collection']    = 'billing.initial'
    #        insert['slctKey']       = None
    #        insert['data']          = writing
    #        insertedId              = self.insertDoc(insert)
            
    #    except Exception,e:
    #        self.log.w2lgError(traceback.format_exc())



# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
#
# helper for manging billing in the nejoba-machine
#  
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
class SetTagging(mongoDbMgr.mongoMgr):

    # ***********************************************************************************************************************************************
    # constructor : call the base class constructor to initialize log, cache, ui-helper and page-member
    #
    #
    # 24.03.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def __init__(self, pg):
        try:
            mongoDbMgr.mongoMgr.__init__(self, pg)      # wake up papa ; mother njbTools is included by inheritance!
            self.ui.getCtrlTree( self.Page.Master )
            self.log.w2lgDvlp('SetTagging( .. ) constructor called')

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # PgLoad : page_load functions
    #
    #
    # 24.03.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def PgLoad(self, pg):
        try:
            # hide the main-user-interface after a button-click and show  a please-wait sedativ
            self.ui.getCtrlTree( pg.Master )
            self.ui.hideFormAfterClick()

            if not pg.IsPostBack:
                mode = pg.Request.QueryString['mode']
                pg.ViewState['MODE'] = mode

                # user must login if a new rubriced item will be inserted
                if mode == 'create':
                    # user must be logged in
                    self.usrDt.checkUserRigths( pg, 'free')

                self.FillListBox(0)

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # HandlBtnClick   : handler for button-clix
    #
    # 07.01.2013  - bervie -     initial realese
    # 11.04.2013  - bervie -     added parameter to enable search also when no rubric was given
    # ***********************************************************************************************************************************************
    def HandlBtnClick( self, pg , sender,e ):
        urlNext = None
        try:

            # handle a selection-cjhange in a listbox
            if 'setRbrc_' in  sender.ID:
                if pg.ViewState['MODE'] == "search": self.ui.getCtrl('btn_Next').Text = 'Ort festlegen'
                elif pg.ViewState['MODE'] == "create": self.ui.getCtrl('btn_Next').Text = 'Zum Editor'

                if 'setRbrc_1' ==  sender.ID : self.FillListBox(1)
                if 'setRbrc_2' ==  sender.ID : self.FillListBox(2)
                if 'setRbrc_3' ==  sender.ID : self.FillListBox(3)
                if 'setRbrc_4' ==  sender.ID : self.FillListBox(4)

                self.ui.getCtrl('lbl_show_selection').Text = self.ui.getCtrl(sender.ID).SelectedItem.Text

            # if button was pressed go to the debate-editor with the hex-coded parameter in the url
            if 'btn_Next' in  sender.ID:
                if pg.ViewState['MODE'] == "search": url = WebConfigurationManager.AppSettings[ 'DefineLocation' ]
                else:                                url = WebConfigurationManager.AppSettings[ 'StartDebate' ]

                if self.ui.getCtrl('lbl_indexKey').Text is not System.String.Empty:
                    if self.ui.getCtrl('btn_Next').Text != 'Alle Rubriken':
                        url += '?key='  + self.ui.getCtrl('lbl_indexKey').Text
                        url += '&name=' + self.ui.getCtrl('lbl_show_selection').Text

                    # 11.04.2013 load all rubricks  BUGFIX
                    else:
                        keyForAll = WebConfigurationManager.AppSettings['rubricCmdTagg'] 
                        url += '?key='  + keyForAll
                        url += '&name=' + 'Alle Rubriken'



                urlNext = pg.ResolveUrl( url )

                # tool.log.w2lgDvlp('topic_set_tagging.aspx.py jump-url in click-handler : ' + urlNext)

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())

        if urlNext != None:
            pg.Response.Redirect( urlNext )
            




    # ***********************************************************************************************************************************************
    # FillListBox : fill the listbox with the data from the item-matrix
    #
    # parameter : the index of the listbox taht should be filled 
    #
    # 07.01.2013  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def FillListBox( self, indexNum ):
        try:
            if indexNum == 0:
                for a in range(20):
                    item = self.taggs.mtrx[a][0][0][0][0]
                    #self.log.w2lgDvlp( 'PageLoad : for item ' + str(a) + ' type of matrix = ' + unicode(type(item)) )
                    # the undefined items are type of list
                    if type(item) == type('string'):
                        lstItm = System.Web.UI.WebControls.ListItem(  unicode(item), unicode(hex(a)))
                        # self.log.w2lgDvlp( 'PageLoad : opdate index-matrix ' + unicode(item) )
                        self.ui.getCtrl('setRbrc_1').Items.Add( lstItm )

            elif indexNum == 1:
                self.ui.getCtrl('setRbrc_2').Items.Clear()
                self.ui.getCtrl('setRbrc_3').Items.Clear()
                self.ui.getCtrl('setRbrc_4').Items.Clear()
            
                # update the follower
                indx = System.Convert.ToInt16( self.ui.getCtrl('setRbrc_1').SelectedIndex ) + 1
                for a in range(1,20):
                    item = self.taggs.mtrx[indx][a][0][0][0]
                    if type(item) == type('string'):
                        lstItm = System.Web.UI.WebControls.ListItem(item, str(hex(a)))
                        self.ui.getCtrl('setRbrc_2').Items.Add( lstItm )
                    

            elif indexNum == 2:
                self.ui.getCtrl('setRbrc_3').Items.Clear()
                self.ui.getCtrl('setRbrc_4').Items.Clear()

                # update the followers
                indx1 = System.Convert.ToInt16( self.ui.getCtrl('setRbrc_1').SelectedIndex ) + 1
                indx2 = System.Convert.ToInt16( self.ui.getCtrl('setRbrc_2').SelectedIndex ) + 1
                for a in range(1,20):
                    item = self.taggs.mtrx[indx1][indx2][a][0][0]
                    if type(item) == type('string'):
                        lstItm = System.Web.UI.WebControls.ListItem(item, str(hex(a)))
                        self.ui.getCtrl('setRbrc_3').Items.Add( lstItm )
                    

            elif indexNum == 3:
                self.ui.getCtrl('setRbrc_4').Items.Clear()

                # update the followers
                indx1 = System.Convert.ToInt16( self.ui.getCtrl('setRbrc_1').SelectedIndex ) + 1
                indx2 = System.Convert.ToInt16( self.ui.getCtrl('setRbrc_2').SelectedIndex ) + 1
                indx3 = System.Convert.ToInt16( self.ui.getCtrl('setRbrc_3').SelectedIndex ) + 1
                for a in range(1,20):
                    item = self.taggs.mtrx[indx1][indx2][indx3][a][0]
                    if type(item) == type('string'):
                        lstItm = System.Web.UI.WebControls.ListItem(item, str(hex(a)))
                        self.ui.getCtrl('setRbrc_4').Items.Add( lstItm )
                    

            elif indexNum == 4:
                # currently only 4 listboxes are displayed
                # the data-container supports one more
                pass

            # generate the selction-key and store him in a hiodden lable. the label will be read if user clickas confirm and send to the next webform. this is the url-parameter
            # IdxKeyStrng = 'R001_'
            IdxKeyStrng = WebConfigurationManager.AppSettings[ 'rubricCmdTagg' ]

            if indexNum == 1:
                IdxKeyStrng += self.ui.getCtrl('setRbrc_1').SelectedValue
            if indexNum == 2:
                IdxKeyStrng += self.ui.getCtrl('setRbrc_1').SelectedValue
                IdxKeyStrng += self.ui.getCtrl('setRbrc_2').SelectedValue
            if indexNum == 3:
                IdxKeyStrng += self.ui.getCtrl('setRbrc_1').SelectedValue
                IdxKeyStrng += self.ui.getCtrl('setRbrc_2').SelectedValue
                IdxKeyStrng += self.ui.getCtrl('setRbrc_3').SelectedValue
            if indexNum == 4:
                IdxKeyStrng += self.ui.getCtrl('setRbrc_1').SelectedValue
                IdxKeyStrng += self.ui.getCtrl('setRbrc_2').SelectedValue
                IdxKeyStrng += self.ui.getCtrl('setRbrc_3').SelectedValue
                IdxKeyStrng += self.ui.getCtrl('setRbrc_4').SelectedValue

            self.ui.getCtrl('lbl_indexKey').Text       = IdxKeyStrng
            #self.ui.getCtrl('lbl_show_selection').Text = IdxKeyStrng

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())




# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
#
# helper for logIn.aspx.py : the form used to log-in or to change to the account-creation-webform
#  
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -

# class ParamResultList( mongoDbMgr.mongoMgr ):
class ReuseListExternal( mongoDbMgr.mongoMgr ):
    # ***********************************************************************************************************************************************
    # constructor : the class is the tool for the Parameter_result_list
    #
    # 18.04.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def __init__(self, pg):
        try:
            self.Page = pg

            mongoDbMgr.mongoMgr.__init__(self, pg)      # wake up papa ; mother njbTools is included by inheritance!
            self.ui.getCtrlTree( self.Page.Master )
            self.log.w2lgDvlp('constructor of class ParamResultList(Page) called !')

            # helper dict to store the parameter 
            self.srchPtrn = {}

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # HandlBtnClick   : handler for button-clix
    #
    # 07.01.2013  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def ButtonHandler( self, sender, e ):
        url = None
        try:
            url = None
            buttonId = sender.ID
            self.log.w2lgDvlp( 'thing_list->  HandlBtnClick  BUTON pressed : ' + buttonId )

            # get the results for the given search-parameter
            if 'btn_loadList' == buttonId:
                self.LoadDebateList()

            # call webform to reuse the pinnwall for external usage like facebook or twttwer
            elif 'btn_reuseList' == buttonId:
                self.CallReuseForm()


            elif 'btn_openDebate' == buttonId:
                # when opening a debate the system goes to the editor for debates: debate_articel_editor.aspx
                # . so use can take action. the debate_editor shows the thread and has a simple text-editor
                clntIdComponents = sender.ClientID.ToString().split('_')
                arrIdx = clntIdComponents[4]
                dbIds = self.Page.ViewState['IdList']
                listIdx = dbIds[ int(arrIdx) ]
                # self.log.w2lgDvlp( 'Index  in db-array     : ' + str(arrIdx) )
                # self.log.w2lgDvlp( 'Index  for cache-table : ' + str(listIdx) )

                url = WebConfigurationManager.AppSettings['AddArticleToDebate']                         # search for debates
                if not self.usrDt.isLoggedIn():
                    url = WebConfigurationManager.AppSettings['DetailsForStrangers']                    # use view-detail-dialog for not logged in users
                url += '?item=' + listIdx




        except Exception,e:
            self.log.w2lgError(traceback.format_exc())

        if url != None:
            self.Page.Response.Redirect(self.Page.ResolveUrl(url))



    # ***********************************************************************************************************************************************
    # defineLocation   : define a list of places near the startpoint ordered by distance and add the list to the dropdown
    #
    # 10.03.2013  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def defineLocation( self, urlLocParam ):
        try:
            callParam = urlLocParam.split('|')
            self.log.w2lgDvlp( 'defineLocation parameter : ' + callParam[0] + ' - ' + callParam[1] )

            areaSize  = WebConfigurationManager.AppSettings["areaSize"];
            cntry     = callParam[0]
            postcd    = callParam[1]
            locList = self.geoSrc.getPlacesByPostcode( cntry.ToString(), postcd.ToString(), areaSize.ToString() )

            drpDwn = self.ui.getCtrl('sel_lctn')
            for loc in locList:
                itmText = loc[0].ToString().replace('|',' ') + ' - ' + loc[4].ToString()
                itmVal = loc[1].ToString()
                lstItem = System.Web.UI.WebControls.ListItem( itmText, itmVal )
                drpDwn.Items.Add( lstItem )
                # self.log.w2lgDvlp( 'found placename  : ' +  itmText + ' ' + itmVal )

            return locList

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # defineTagsFromParam  : get taggs from the url
    #                        they must be seperated by commas. they can start witrh a hashtag, they will be converted to lowwer-case
    #
    # 10.03.2013  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def defineTagsFromParam( self, taggParam ):
        try:
            # 2. search-parameter from the UI
            #    tags: we use the tags without  leading #
            tagString = taggParam.strip().ToLower()
            taggList = []

            if tagString != System.String.Empty:
                tagsRawInput = tagString.split(',')
                if len(tagsRawInput) > 0:
                    for itm in tagsRawInput:                        # remove hashtags
                        if itm[0] == '#':
                            taggList.Add( itm[1:].ToString() )
                        else:
                            taggList.Add( itm.ToString() )

                for tagg in taggList:
                    self.log.w2lgDvlp( 'found tagg  : ' +  tagg )

                self.ui.getCtrl('txb_hashtags').Text=tagString

            return taggList

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # LoadDebateList   : load a list with debates filtered by controll-data
    #
    # 07.01.2013  - bervie -     initial realese
    # 10.04.2013  - bervie -     nothing loaded when no tag given ; not all subitems are loaded if rubric was not given
    # 23.04.2013  - bervie -     added NoResultsFoundDiv to show user if nothing was found
    # ***********************************************************************************************************************************************
    def LoadDebateList( self ):
        try:
            # get selected location from the dropdown 
            drpDwn = self.ui.getCtrl('sel_lctn')
            locSlct = drpDwn.Items[0].Text.split(' - ')[0]  #.split(' ')[0]

            # get tags that will be used for search
            freeTagText = self.ui.getCtrl('txb_hashtags').Text.strip()
        
            if len(freeTagText) > 0: 
                # load matching items  
                resultTble = self.LoadDebatesFiltered(locSlct, freeTagText)
            else:
                # if no tags were given load all base-items for given location
                resultTble = self.LoadDebatesUnfiltered()

            # sorting: list should start with the newest items - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
            chronologicView = System.Data.DataView(resultTble)
            chronologicView.Sort = 'creationTime DESC'

            # store ids in order of apperance in the table into an array. we will get the _id by calling the index of this array
            listOfIds = []
            for item in chronologicView:
                listOfIds.Add(item['_ID'])

            if len(listOfIds) > 0 : self.ui.getCtrl('NoResultsFoundDiv').Visible = False        # if data was found show it 
            else : self.ui.getCtrl('NoResultsFoundDiv').Visible = True                          # if no data was found explain this to the user in the ui

            self.Page.ViewState['IdList'] = listOfIds

            # bind repeater to result data-table
            repeater = self.gtCtl('repDebateList')
            #repeater.DataSource = resultTble.DefaultView
            repeater.DataSource = chronologicView
            repeater.DataBind()


        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
    # LoadDebatesUnfiltered   : if no tags  were given this function is called to load all base-items in the area
    #
    # 07.01.2013  - bervie -     initial realese
    # 10.04.2013  - bervie -     nothing loaded when no tag given ; not all subitems are loaded if rubric was not given
    # ***********************************************************************************************************************************************
    def LoadDebatesUnfiltered( self ):
        try:
            # 1. search-parameter from the UI
            #    locations : get the selected location
            tagTable    = self.appCch.dtSt.Tables["itemTags"]
            resultTble  = self.appCch.dtSt.Tables["items"].Clone()

            minAmount = System.Convert.ToInt16( WebConfigurationManager.AppSettings["MinNumOfDebates"] )

            # 2. create a list o0f locations ordered by the distance from selected value
            selectLocation = self.ui.getCtrl('sel_lctn')
            locList = []
            for itm in selectLocation.Items : locList.Add( itm.Value.ToString() )

            # helper-array to store all mongo-ids we have loaded from item-table
            idList = []

            for location in locList:
                # select all jobs in this area
                rows = self.appCch.dtVwLoctn.FindRows( location )
                for row in rows:
                    if row['objectType'] == 1:              # get all debates
                        resultTble.ImportRow(row.Row)
                if len(idList) >= minAmount : break

            return resultTble

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
    # LoadDebatesFiltered   : load debates that match for a tag
    #
    # 20.04.2013  - bervie -     initial realese
    #
    # ***********************************************************************************************************************************************
    def LoadDebatesFiltered( self, locSlct, freeTagText ):
        try:
            # get the 
            tgLst = self.ui.convertTagsFromInput(freeTagText)

            itmIds = self.taggs.loadBaseItems( locSlct, tgLst, False )

            resultTble  = self.appCch.dtSt.Tables["items"].Clone()
            for itm in itmIds:
                row = self.appCch.dtSt.Tables["items"].Rows.Find(itm)
                resultTble.ImportRow(row)

            return resultTble

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # ******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
    # LoadDebatesFiltered   : load debates that match for a tag
    #
    # 20.04.2013  - bervie -     initial realese
    #
    # ***********************************************************************************************************************************************
    def CallReuseForm( self):
        try:
            url = None
            # reuseListExternal

            url = WebConfigurationManager.AppSettings['reuseListExternal']                         # search for debates
            self.log.w2lgDvlp( 'CallReuseForm was called in ParamResultList() to ' + unicode( url ) )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())

        if url != None:
            self.Page.Response.Redirect(self.Page.ResolveUrl(url))



# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
#
# helper for Topic_By_Parameter.aspx.py : the webform shows the debates
#  
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -

class TopicByParameter( mongoDbMgr.mongoMgr ):
    # ***********************************************************************************************************************************************
    # constructor : the class is the tool for the Parameter_result_list
    #
    # 18.04.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def __init__(self, pg):
        try:
            self.Page = pg
            mongoDbMgr.mongoMgr.__init__(self, pg)      # wake up papa ; mother njbTools is included by inheritance!
            self.ui.getCtrlTree( self.Page.Master )
            self.log.w2lgDvlp('constructor of class ParamResultList(Page) called !')

            # DestntUrl is the attribute which stores the destination-url
            if not self.usrDt.isLoggedIn():
                self.DestntUrl = WebConfigurationManager.AppSettings['DetailsForStrangers']                             # use view-detail-dialog for not logged in users
            else:
                self.DestntUrl = WebConfigurationManager.AppSettings['AddArticleToDebate']                              # detail-view url with debate option

            # helper dict to store the parameter 
            self.srchPtrn = {}

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # PageLoad : called when page is loaded
    #
    # 18.04.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def PageLoad( self, sender , e ):
        try:
            # hide the main-user-interface after a button-click and show  a please-wait sedativ
            self.ui.getCtrlTree( self.Page.Master )
            self.ui.hideFormAfterClick()

            if not self.Page.IsPostBack:
                # 1. get the data of the location given as URL-parameter and put data into the dropdown
                #    syntax of locationparameter must be : DE|41836
                locParam  = self.Page.Request.QueryString['loc']
                if locParam:
                    locations = self.defineLocation( locParam )
                    self.Page.ViewState['LOCATION_LIST'] = locations 

                # 2. get the taggs that should be used for search. if we have a couple of taggs they have 
                #    to be seperated by comma : karneval,rosenmotag,veranstaltung or #karneval,#rosenmotag,#veranstaltung 
                taggParam = self.Page.Request.QueryString['taggs']
                if taggParam:
                    taggings = self.defineTagsFromParam( taggParam )
                    self.ui.getCtrl('txb_hashtags').Text = ','.join(taggings)
                    self.Page.ViewState['TAGG_LIST'] = taggings

                # 3. get the key and name of a rubric to find all items that are labeled with this key-code: nejoba will also 
                #    load all data from- sub-rubrics that belong to the given one by checking the substring matches
                rubric = self.Page.Request.QueryString['key']
                if rubric:
                    self.Page.ViewState['RUBRIC'] = rubric
                name = self.Page.Request.QueryString['name']
                if name:
                    self.Page.ViewState['RUBRIC_NAME'] = name
                    self.ui.getCtrl('txb_rubricName').Text = name

                # load list of debates into repeater
                self.LoadDebateList()

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # HandlBtnClick   : handler for button-clix
    #
    # 07.01.2013  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def HandlBtnClick( self, sender, e ):
        url = None
        try:
            url = None
            buttonId = sender.ID
            # self.log.w2lgDvlp( 'thing_list->  HandlBtnClick  BUTON pressed : ' + buttonId )

            # go back to the debate_search-webform to change locations-middle
            if 'btn_changeLocation' == buttonId:
                url = WebConfigurationManager.AppSettings['DefineLocation'] 
                if self.Page.ViewState['RUBRIC']:
                    url += '?key=' + self.Page.ViewState['RUBRIC']
                if self.Page.ViewState['RUBRIC_NAME']:
                    url += '&name=' + self.Page.ViewState['RUBRIC_NAME']

            # create and display the HTML-Code for the nejoba button
            elif 'btn_getNejobaButton' == buttonId:
                ProvideNejobaKey()
                return

            # get the results for the given search-parameter
            elif 'btn_loadList' == buttonId:
                self.LoadDebateList()
                return

                # location is the string representation of the location
                url = WebConfigurationManager.AppSettings['ShowFromUrl'] 

                location = self.Page.Request.QueryString['loc']
                taggParam = self.ui.getCtrl('txb_hashtags').Text.strip()
                rubric = self.Page.ViewState['RUBRIC']
                name = self.Page.ViewState['RUBRIC_NAME']

                if location is not None:
                    url += '?loc=' + location
                if len(taggParam) > 0:
                    url += '&taggs=' + taggParam

                if rubric is not None:
                    url += '&key=' + rubric
                if name is not None:
                    url += '&name=' + name
                # --------------------------------------------------------------------------------------------------------------------------------------


            # replaced by Hyper-link control to enable target = '_blank'
            #elif 'btn_openDebate' == buttonId:
            #    # when opening a debate the system goes to the editor for debates: debate_articel_editor.aspx
            #    # . so use can take action. the debate_editor shows the thread and has a simple text-editor
            #    clntIdComponents = sender.ClientID.ToString().split('_')
            #    arrIdx = clntIdComponents[4]
            #    dbIds = self.Page.ViewState['IdList']
            #    listIdx = dbIds[ int(arrIdx) ]
            #    # self.log.w2lgDvlp( 'Index  in db-array     : ' + str(arrIdx) )
            #    # self.log.w2lgDvlp( 'Index  for cache-table : ' + str(listIdx) )

            #    url = WebConfigurationManager.AppSettings['AddArticleToDebate']                         # search for debates
            #    if not self.usrDt.isLoggedIn():
            #        url = WebConfigurationManager.AppSettings['DetailsForStrangers']                    # use view-detail-dialog for not logged in users
            #    url += '?item=' + listIdx

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())

        if url != None:
            # open in same window
            self.Page.Response.Redirect(self.Page.ResolveUrl(url))



    # ***********************************************************************************************************************************************
    # defineLocation   : define a list of places near the startpoint ordered by distance and add the list to the dropdown
    #
    # 10.03.2013  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def defineLocation( self, urlLocParam ):
        try:
            callParam = urlLocParam.split('|')
            self.log.w2lgDvlp( 'defineLocation parameter : ' + callParam[0] + ' - ' + callParam[1] )

            areaSize  = WebConfigurationManager.AppSettings["areaSize"];
            cntry     = callParam[0]
            postcd    = callParam[1]
            locList = self.geoSrc.getPlacesByPostcode( cntry.ToString(), postcd.ToString(), areaSize.ToString() )

            drpDwn = self.ui.getCtrl('sel_lctn')
            for loc in locList:
                itmText = loc[0].ToString().replace('|',' ') + ' - ' + loc[4].ToString()
                itmVal = loc[1].ToString()
                lstItem = System.Web.UI.WebControls.ListItem( itmText, itmVal )
                drpDwn.Items.Add( lstItem )
                # self.log.w2lgDvlp( 'found placename  : ' +  itmText + ' ' + itmVal )

            return locList

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # defineTagsFromParam  : get taggs from the url
    #                        they must be seperated by commas. they can start witrh a hashtag, they will be converted to lowwer-case
    #
    # 10.03.2013  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def defineTagsFromParam( self, taggParam ):
        try:
            # 2. search-parameter from the UI
            #    tags: we use the tags without  leading #
            tagString = taggParam.strip().ToLower()
            taggList = []

            if tagString != System.String.Empty:
                tagsRawInput = tagString.split(',')
                if len(tagsRawInput) > 0:
                    for itm in tagsRawInput:                        # remove hashtags
                        if itm[0] == '#':
                            taggList.Add( itm[1:].ToString() )
                        else:
                            taggList.Add( itm.ToString() )

                for tagg in taggList:
                    self.log.w2lgDvlp( 'found tagg  : ' +  tagg )

                self.ui.getCtrl('txb_hashtags').Text=tagString

            return taggList

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # LoadDebateList   : load a list with debates filtered by controll-data
    #
    # 07.01.2013  - bervie -     initial realese
    # 10.04.2013  - bervie -     nothing loaded when no tag given ; not all subitems are loaded if rubric was not given
    # 23.04.2013  - bervie -     added NoResultsFoundDiv if nothing was found
    # ***********************************************************************************************************************************************
    def LoadDebateList( self ):
        try:
            # get selected location from the dropdown 
            drpDwn = self.ui.getCtrl('sel_lctn')
            locSlct = drpDwn.Items[0].Text.split(' - ')[0]  #.split(' ')[0]

            # create a list with the taggs (rubric and users input in the textbox)
            tgLst = []

            # if we have a rubric defined the taggs are logical combined with an AND
            rbrcText    = self.ui.getCtrl('txb_rubricName').Text.strip()
            freeTagText = self.ui.getCtrl('txb_hashtags').Text.strip()

            if self.Page.ViewState['RUBRIC'] != None:
                # if a rubric is given we combine the rubrics with the free tags typed in by the user
                tgLst.Add( self.Page.ViewState['RUBRIC'].ToString() )

                if len(freeTagText) > 0: 
                    tgLst += self.ui.convertTagsFromInput(freeTagText)
                    for tag in tgLst : self.log.w2lgDvlp( 'tag used for query in LoadDebateList : ' +  unicode(tag) )

                itmIds = self.taggs.loadBaseItems( locSlct, tgLst, True )

            else:
                # if we  have no rubrics the free-tage will be combined with OR
                if len(freeTagText) > 0: 
                    tgLst += self.ui.convertTagsFromInput(freeTagText)
                    for tag in tgLst : self.log.w2lgDvlp( 'tag used for query in LoadDebateList : ' +  unicode(tag) )

                itmIds = self.taggs.loadBaseItems( locSlct, tgLst, False )

            # 10-04-2012

            # False for loadBaseItems : items of tags are OR-combined
            # itmIds = self.taggs.loadBaseItems( locSlct, tgLst, False ) # ++++++++++++++++++++++++++++++++++++++++++++++++
            # True for loadBaseItems : items of tags are AND-combined

            itemTable   = self.appCch.dtSt.Tables["items"]
            resultTble  = itemTable.Clone()

            for itm in itmIds:
                row = itemTable.Rows.Find(itm)
                resultTble.ImportRow(row)
                # tagzero is temporarly overwritten with the destination-url
                itmLnk = self.DestntUrl + '?item=' + resultTble.Rows[resultTble.Rows.Count - 1]['_ID'].ToString()
                resultTble.Rows[resultTble.Rows.Count - 1]['tagZero'] = itmLnk
    
            # sorting: list should start with the newest items
            chronologicView = System.Data.DataView(resultTble)
            chronologicView.Sort = 'creationTime DESC'

            # store ids in order of apperance in the table into an array. we will get the _id by calling the index of this array
            listOfIds = []
            for item in chronologicView:
                listOfIds.Add(item['_ID'])

            if len(listOfIds) > 0 : self.ui.getCtrl('NoResultsFoundDiv').Visible = False        # if data was found show it 
            else : self.ui.getCtrl('NoResultsFoundDiv').Visible = True                          # if no data was found explain this to the user in the ui

            self.Page.ViewState['IdList'] = listOfIds



            # bind repeater to result data-table
            repeater = self.gtCtl('repDebateList')
            #repeater.DataSource = resultTble.DefaultView
            repeater.DataSource = chronologicView
            repeater.DataBind()

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
#
# helper for ParamResultList.aspx.py : the webform shows the debates
#  
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -

class ParamResultList( mongoDbMgr.mongoMgr ):
    # ***********************************************************************************************************************************************
    # constructor : the class is the tool for the Parameter_result_list
    #
    # 18.04.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def __init__(self, pg):
        try:
            self.Page = pg

            mongoDbMgr.mongoMgr.__init__(self, pg)      # wake up papa ; mother njbTools is included by inheritance!
            self.ui.getCtrlTree( self.Page.Master )
            self.log.w2lgDvlp('constructor of class ParamResultList(Page) called !')

            # helper dict to store the parameter 
            self.srchPtrn = {}

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # PageLoad   : called when page is loaded for the first time
    #
    # valid URL-params for the webform parameter_result_list
    #
    # loc       = location like "DE|41836" (converted to a neighbouhood-list : LOCATION_LIST)
    # tags      = tags that should be used for filtering the list (TAG_LIST)
    # srchMd    = search-mode for filtering the tags : 
    #             AND means all items with any are displayed; OR means only items with all tags are displayed 
    # key       = the internal ID of a choosen rubric  RUBRIC
    # name      = the name of the rubric for displaying in the UI  RUBRIC_NAME
    #
    # 28.04.2013  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def PageLoad(self, sender, e):
        try:
            # hide the main-user-interface after a button-click and show  a please-wait sedativ
            self.ui.getCtrlTree( self.Page.Master )
            self.ui.hideFormAfterClick()

            if not self.Page.IsPostBack:
                # 1. get the data of the location given as URL-parameter and put data into the dropdown
                #    syntax of locationparameter must be : DE|41836
                locParam  = self.Page.Request.QueryString['loc']
                if locParam:
                    locations = self.defineLocation( locParam )
                    self.Page.ViewState['LOCATION_LIST'] = locations
                    self.Page.ViewState['LOCATION_PARAM'] = locParam

                # 2. get the taggs that should be used for search. if we have a couple of taggs they have 
                #    to be seperated by comma : karneval,rosenmotag,veranstaltung or #karneval,#rosenmotag,#veranstaltung 
                taggParam = self.Page.Request.QueryString['tags']
                if taggParam:
                    taggings = self.defineTagsFromParam( taggParam )
                    self.ui.getCtrl('txb_hashtags').Text = ','.join(taggings)
                    self.Page.ViewState['TAG_LIST'] = taggings

                # 3. get the key and name of a rubric to find all items that are labeled with this key-code: nejoba will also 
                #    load all data from- sub-rubrics that belong to the given one by checking the substring matches
                rubric = self.Page.Request.QueryString['key']
                if rubric:
                    self.Page.ViewState['RUBRIC'] = rubric
                name = self.Page.Request.QueryString['name']
                if name:
                    self.Page.ViewState['RUBRIC_NAME'] = name
                    self.ui.getCtrl('txb_rubricName').Text = name

                srchMd = self.Page.Request.QueryString['srchMd']
                if srchMd:
                    if srchMd in ['AND','OR']:
                        self.Page.ViewState['SEARCH_MODE'] = srchMd

                        # set the radio-knoops accordingally
                        if srchMd == 'AND':
                            self.ui.getCtrl('radio_searchOr').Checked = False
                            self.ui.getCtrl('radio_searchAnd').Checked = True
                        else:
                            self.ui.getCtrl('radio_searchOr').Checked = True
                            self.ui.getCtrl('radio_searchAnd').Checked = False

                # load list of debates into repeater
                self.LoadDebateList()

            # create the link for external calls and prepare the social-media-buttons
            self.PrepareExtLnk()

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # HandlBtnClick   : handler for button-clix
    #
    # 07.01.2013  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def ButtonHandler( self, sender, e ):
        url = None
        try:
            url = None
            buttonId = sender.ID
            self.log.w2lgDvlp( 'thing_list->  HandlBtnClick  BUTON pressed : ' + buttonId )

            # get the results for the given search-parameter
            if 'btn_loadList' == buttonId:
                self.LoadDebateList()
                self.gtCtl('external_link_div').Visible = False

            # show the div with the external link
            elif 'btn_showLink' == buttonId:
                self.gtCtl('external_link_div').Visible = True

            elif 'btn_openDebate' == buttonId:
                # when opening a debate the system goes to the editor for debates: debate_articel_editor.aspx
                # . so use can take action. the debate_editor shows the thread and has a simple text-editor
                clntIdComponents = sender.ClientID.ToString().split('_')
                arrIdx = clntIdComponents[4]
                dbIds = self.Page.ViewState['IdList']
                listIdx = dbIds[ int(arrIdx) ]
                # self.log.w2lgDvlp( 'Index  in db-array     : ' + str(arrIdx) )
                # self.log.w2lgDvlp( 'Index  for cache-table : ' + str(listIdx) )

                url = WebConfigurationManager.AppSettings['AddArticleToDebate']                         # search for debates
                if not self.usrDt.isLoggedIn():
                    url = WebConfigurationManager.AppSettings['DetailsForStrangers']                    # use view-detail-dialog for not logged in users
                url += '?item=' + listIdx

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())

        if url != None:
            self.Page.Response.Redirect(self.Page.ResolveUrl(url))



    # ***********************************************************************************************************************************************
    # defineLocation   : define a list of places near the startpoint ordered by distance and add the list to the dropdown
    #
    # 10.03.2013  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def defineLocation( self, urlLocParam ):
        try:
            callParam = urlLocParam.split('|')
            self.log.w2lgDvlp( 'defineLocation parameter : ' + callParam[0] + ' - ' + callParam[1] )

            areaSize  = WebConfigurationManager.AppSettings["areaSize"];
            cntry     = callParam[0]
            postcd    = callParam[1]
            locList = self.geoSrc.getPlacesByPostcode( cntry.ToString(), postcd.ToString(), areaSize.ToString() )

            drpDwn = self.ui.getCtrl('sel_lctn')
            for loc in locList:
                itmText = loc[0].ToString().replace('|',' ') + ' - ' + loc[4].ToString()
                itmVal = loc[1].ToString()
                lstItem = System.Web.UI.WebControls.ListItem( itmText, itmVal )
                drpDwn.Items.Add( lstItem )
                # self.log.w2lgDvlp( 'found placename  : ' +  itmText + ' ' + itmVal )

            return locList

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # defineTagsFromParam  : get taggs from the url
    #                        they must be seperated by commas. they can start witrh a hashtag, they will be converted to lowwer-case
    #
    # 10.03.2013  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def defineTagsFromParam( self, taggParam ):
        try:
            # 2. search-parameter from the UI
            #    tags: we use the tags without  leading #
            tagString = taggParam.strip().ToLower()
            taggList = []

            if tagString != System.String.Empty:
                tagsRawInput = tagString.split(',')
                if len(tagsRawInput) > 0:
                    for itm in tagsRawInput:                        # remove hashtags
                        if itm[0] == '#':
                            taggList.Add( itm[1:].ToString() )
                        else:
                            taggList.Add( itm.ToString() )

                for tagg in taggList:
                    self.log.w2lgDvlp( 'found tagg  : ' +  tagg )

                self.ui.getCtrl('txb_hashtags').Text=tagString

            return taggList

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # LoadDebateList   : load a list with debates filtered by controll-data
    #
    # 07.01.2013  - bervie -     initial realese
    # 10.04.2013  - bervie -     nothing loaded when no tag given ; not all subitems are loaded if rubric was not given
    # 23.04.2013  - bervie -     added NoResultsFoundDiv to show user if nothing was found
    # ***********************************************************************************************************************************************
    def LoadDebateList( self ):
        try:
            # get first item in the dropdown-list
            drpDwn = self.ui.getCtrl('sel_lctn')
            locSlct = drpDwn.Items[0].Text.split(' - ')[0]  #.split(' ')[0]

            # get tags that will be used for search
            freeTagText = self.ui.getCtrl('txb_hashtags').Text.strip()
        
            if len(freeTagText) > 0: 
                # load matching items  
                resultTble = self.LoadDebatesFiltered(locSlct, freeTagText)
            else:
                # if no tags were given load all base-items for given location
                resultTble = self.LoadDebatesUnfiltered()

            # sorting: list should start with the newest items - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
            chronologicView = System.Data.DataView(resultTble)
            chronologicView.Sort = 'creationTime DESC'

            # store ids in order of apperance in the table into an array. we will get the _id by calling the index of this array
            listOfIds = []
            for item in chronologicView:
                listOfIds.Add(item['_ID'])

            if len(listOfIds) > 0 : self.ui.getCtrl('NoResultsFoundDiv').Visible = False        # if data was found show it 
            else : self.ui.getCtrl('NoResultsFoundDiv').Visible = True                          # if no data was found explain this to the user in the ui

            self.Page.ViewState['IdList'] = listOfIds

            # bind repeater to result data-table
            repeater = self.gtCtl('repDebateList')
            #repeater.DataSource = resultTble.DefaultView
            repeater.DataSource = chronologicView
            repeater.DataBind()

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
    # LoadDebatesUnfiltered   : if no tags  were given this function is called to load all base-items in the area
    #
    # 07.01.2013  - bervie -     initial realese
    # 10.04.2013  - bervie -     nothing loaded when no tag given ; not all subitems are loaded if rubric was not given
    # ***********************************************************************************************************************************************
    def LoadDebatesUnfiltered( self ):
        try:
            # 1. search-parameter from the UI
            #    locations : get the selected location
            tagTable    = self.appCch.dtSt.Tables["itemTags"]
            resultTble  = self.appCch.dtSt.Tables["items"].Clone()

            minAmount = System.Convert.ToInt16( WebConfigurationManager.AppSettings["MinNumOfDebates"] )

            # 2. create a list o0f locations ordered by the distance from selected value
            selectLocation = self.ui.getCtrl('sel_lctn')
            locList = []
            for itm in selectLocation.Items : locList.Add( itm.Value.ToString() )

            # helper-array to store all mongo-ids we have loaded from item-table
            idList = []

            for location in locList:
                # select all jobs in this area
                rows = self.appCch.dtVwLoctn.FindRows( location )
                for row in rows:
                    if row['objectType'] == 1:              # get all debates
                        resultTble.ImportRow(row.Row)
                if len(idList) >= minAmount : break

            return resultTble

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
    # LoadDebatesFiltered   : load debates that match for a tag
    #
    # 20.04.2013  - bervie -     initial realese
    #
    # ***********************************************************************************************************************************************
    def LoadDebatesFiltered( self, locSlct, freeTagText ):
        try:
            # get the 
            tgLst = self.ui.convertTagsFromInput(freeTagText)

            # should the tags be filtered with AND-combined Tags or with OR
            flrtAnd = False
            if self.gtCtl('radio_searchAnd').Checked == True:
                flrtAnd = True

            itmIds = self.taggs.loadBaseItems( locSlct, tgLst, flrtAnd )

            resultTble  = self.appCch.dtSt.Tables["items"].Clone()
            for itm in itmIds:
                row = self.appCch.dtSt.Tables["items"].Rows.Find(itm)
                resultTble.ImportRow(row)

            return resultTble

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # ******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
    # PrepareExtLnk   : function is called in page-load to create the external link and put the data in the social-media-buttons
    #
    #
    # loc       = location like "DE|41836" (converted to a neighbouhood-list : LOCATION_LIST)
    # tags      = tags that should be used for filtering the list (TAG_LIST)
    # srchMd    = search-mode for filtering the tags : 
    #             AND means all items with any are displayed; OR means only items with all tags are displayed 
    # key       = the internal ID of a choosen rubric  RUBRIC
    # name      = the name of the rubric for displaying in the UI  RUBRIC_NAME
    #
    # 28.04.2013  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def PrepareExtLnk( self ):
        try:
            self.log.w2lgDvlp( 'thing_list->  PrepareExtLnk pressed ' )

            url = None
            tags        = self.gtCtl('txb_hashtags').Text.strip()
            srchAnd     = self.gtCtl('radio_searchAnd').Checked

            # url = unicode(WebConfigurationManager.AppSettings['simplePinnBoard'] )
            url = "parameter_result_list.aspx"
            locName = ''

            if self.Page.ViewState['LOCATION_PARAM']:
                url += '?loc=' + unicode( self.Page.ViewState['LOCATION_PARAM'] )
                locName = self.Page.ViewState['LOCATION_PARAM'].split('|')[1]
            else:
                # "NO LOCATION ????" that is absolutly impossible
                return 

            if len(tags) > 0:
                url += '&tags=' + tags

            if srchAnd is True:
                url += '&srchMd=AND'
            else:
                url += '&srchMd=OR'

            if self.Page.ViewState['RUBRIC']:
                url += '&key=' + unicode( self.Page.ViewState['RUBRIC'] )

            if self.Page.ViewState['RUBRIC_NAME']:
                url += '&name=' + unicode( self.Page.ViewState['RUBRIC_NAME'] )


            # the url will be added to the link-link and the social-media DIV
            url = self.Page.ResolveUrl(url)
            goal = System.Uri( self.Page.Request.Url, url).AbsoluteUri

            link                = self.gtCtl('hyli_callPinnboardWithLink')
            link.Text           = goal
            link.NavigateUrl    = goal
            link.Target         = "_blank" 

            twitterTxt = '''<a href="https://twitter.com/share" class="twitter-share-button" data-url="''' + goal + '''" data-text="Eine nejoba PinnWand " data-via="info_nejoba" data-lang="de" data-size="large" data-hashtags="nejoba">Twittern</a> <script>                                !function (d, s, id) { var js, fjs = d.getElementsByTagName(s)[0], p = /^http:/.test(d.location) ? 'http' : 'https'; if (!d.getElementById(id)) { js = d.createElement(s); js.id = id; js.src = p + '://platform.twitter.com/widgets.js'; fjs.parentNode.insertBefore(js, fjs); } } (document, 'script', 'twitter-wjs');</script>'''
            frazenbuchTxt = '''<div class="fb-like" id="facebook_button_div" data-href="''' + goal + '''" data-send="true" data-layout="box_count" data-width="450" data-show-faces="true"></div>'''

            # load the link in the social-media-buttons
            twittDiv = self.ui.findCtrl(self.Page, 'twitter_button')
            faceBkDiv = self.ui.findCtrl(self.Page, 'facebook_button')

            twittDiv.InnerHtml = twitterTxt
            faceBkDiv.InnerHtml = frazenbuchTxt

            # 04.05.2013 bervie the header-text should show the  search-parmeter
            pgNme = 'nejoba : ' + locName
            freeTagText = self.ui.getCtrl('txb_hashtags').Text.strip()
            if len(freeTagText) > 0:
                pgNme += ' : ' + freeTagText

            self.Page.Header.Title = pgNme

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
#
# helper for TopicDisplayTaggs.aspx.py : the webform shows the tags that are used in a given country
#  
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -

class DisplayTags( mongoDbMgr.mongoMgr ):

    # ***********************************************************************************************************************************************
    # constructor : the class is the tool for the Parameter_result_list
    #
    # 18.04.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def __init__(self, pg):
        try:
            self.Page = pg

            mongoDbMgr.mongoMgr.__init__(self, pg)      # wake up papa ; mother njbTools is included by inheritance!
            self.ui.getCtrlTree( self.Page.Master )
            self.log.w2lgDvlp('constructor of class ParamResultList(Page) called !')

            # helper dict to store the parameter 
            self.srchPtrn = {}

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # ***********************************************************************************************************************************************
    # Page_Load        : initializer of the webpage
    #
    # 07.01.2013  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def PageLoad( self, sender, e):
        try:
            # hide the main-user-interface after a button-click and show  a please-wait sedativ
            self.ui.getCtrlTree( self.Page.Master )
            self.ui.hideFormAfterClick()

            if not self.Page.IsPostBack:
                # disable the hashtagg edit-field before there is any character selected
                self.ui.getCtrl('txb_hashtags').Enabled=False

                # 1. get the data of the location given as URL-parameter and put data into the dropdown
                #    syntax of locationparameter must be : DE|41836
                locParam  = self.Page.Request.QueryString['loc']
                self.Page.ViewState['LOCATION_PARAMETER'] = locParam
                if locParam:
                    locations = self.defineLocation( locParam )
                    self.Page.ViewState['LOCATION_LIST'] = locations 

                # 2. get the taggs that should be used for search. if we have a couple of taggs they have 
                #    to be seperated by comma : karneval,rosenmotag,veranstaltung or #karneval,#rosenmotag,#veranstaltung 
                taggParam = self.Page.Request.QueryString['tagg']
                if taggParam:
                    self.Page.ViewState['FREE_TAG'] = taggParam
                    self.ui.getCtrl('txb_hashtags').Text = taggParam
        
            # if there is a start-char load the list of the available hashtags and bind the event-nahdelrs to the dynamically generated links
            strtChar = self.Page.Request.QueryString['char']
            if strtChar:
                prsdLnk = self.ui.getCtrl('hyLnk_char_' + strtChar)
                prsdLnk.CssClass = 'label label-inverse'

                # if a character was choosen the textbox is available to type the tagg directly
                self.ui.getCtrl('txb_hashtags').Enabled = True
                self.ui.getCtrl('lbl_startingChar').Text = self.ui.getCtrl('BeginningCharacterTextDefinition').Text + strtChar

                self.LoadTaggList( strtChar )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # defineLocation   : define a list of places near the startpoint ordered by distance 
    #
    # 10.03.2013  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def defineLocation( self, urlLocParam ):
        try:
            callParam = urlLocParam.split('|')
            self.log.w2lgDvlp( 'defineLocation parameter : ' + callParam[0] + ' - ' + callParam[1] )

            areaSize  = WebConfigurationManager.AppSettings["areaSize"]
            cntry     = callParam[0]
            postcd    = callParam[1]
            locList = self.geoSrc.getPlacesByPostcode( cntry.ToString(), postcd.ToString(), areaSize.ToString() )

            drpDwn = self.ui.getCtrl('sel_lctn')
            for loc in locList:
                itmText = loc[0].ToString().replace('|',' ') + ' - ' + loc[4].ToString()
                itmVal = loc[1].ToString()
                lstItem = System.Web.UI.WebControls.ListItem( itmText, itmVal )
                drpDwn.Items.Add( lstItem )
                self.log.w2lgDvlp( 'found placename  : ' +  itmText + ' ' + itmVal )

            return locList

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # HandlBtnClick   : handler for button-clix
    #
    # 07.01.2013  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def HandlBtnClick( self, sender, e ):
        try:
            urlNext = None 

            # user selected a char-button
            if sender.ID.startswith('hyLnk_char_'):
                # IMPORTANT HINT : DYNAMICALLYY ADDING CONTROLLS ALWAYS MUST BE DONE IN PAGE-LOAD to wire up the event-handler correctly
                choosenChar = self.ui.getCtrl(sender.ID).Text.lower()

                selLocTxt =  self.ui.getCtrl('sel_lctn').SelectedItem.Text
                selLocName = selLocTxt.split(' - ')[0].strip()
                selLocArray = selLocName.split(' ')
            
                urlNext = self.buildUrl( WebConfigurationManager.AppSettings[ 'DisplayHashTaggs' ] )
                urlNext += '&char=' + choosenChar
                urlNext += '&loc=' + selLocArray[0].strip() + '|' + selLocArray[1].strip()


            # a button was pressed ('change location' or 'go to list')
            if sender.ID.startswith('btn_'):
                if 'btn_Location'   ==  sender.ID:  
                    urlNext = self.buildUrl( WebConfigurationManager.AppSettings[ 'DefineLocation' ] ) 
                elif 'btn_Find'  ==  sender.ID:  
                    urlNext = self.buildUrl( WebConfigurationManager.AppSettings[ 'ShowFromUrl' ] ) 

                if 'btn_Find'  ==  sender.ID:
                    choosenTagg = self.ui.getCtrl('txb_hashtags').Text.strip()
                    if len( choosenTagg ) > 0:
                        urlNext += '&taggs=' + choosenTagg
                    else:
                        # no hashtagg given. show error msg and do not redirect
                        urlNext = None
                        self.errorMessage( self.ui.getCtrl('errorMsg_no_hashtag').Text )

            # a tagg ( created dynamcally ) was selected 
            if sender.ID.startswith('hyLnk_tagg_'):
                self.log.w2lgDvlp( 'a tagg ( created dynamcally ) was selected  ' + sender.ID )
                idxInLst = sender.ID.split('_')[2]
                foundTgs = self.Page.ViewState['TAGG_LIST']
                choosenTagg = foundTgs[ System.Convert.ToInt32( idxInLst )][0]

                urlNext = self.buildUrl( WebConfigurationManager.AppSettings[ 'ShowFromUrl' ] ) 
                urlNext += '&taggs=' + choosenTagg

                self.log.w2lgDvlp( 'a hashtagg-link was pressed directly .  URL : ' +  urlNext )


        except Exception,e:
            self.log.w2lgError(traceback.format_exc())

        if urlNext != None:
            self.Page.Response.Redirect( self.Page.ResolveUrl( urlNext ) )


    # ***********************************************************************************************************************************************
    # buildUrl  : this function gennerates an url for the redirection
    #
    # 07.01.2013  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def buildUrl( self, nextFormUrl ):
        try:
            urlNext = nextFormUrl
            urlNext += '?mode=tagg'
            selLocName = ''

            # add the location as parameter if the list should be displayed
            if nextFormUrl == WebConfigurationManager.AppSettings[ 'ShowFromUrl' ]:
                # text in list-elem looks like : "DE 52224 - Stolberg (Rheinland)"
                selLocTxt =  self.ui.getCtrl('sel_lctn').SelectedItem.Text
                selLocName = selLocTxt.split(' - ')[0].strip()
                selLocArray = selLocName.split(' ')
            
                urlNext += '&loc=' + selLocArray[0].strip() + '|' + selLocArray[1].strip()

            self.log.w2lgDvlp( 'URL build in buildUrl : ' +  urlNext )
            return urlNext

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # LoadTaggList   : this function get a list wih the hashtaggs of a given location
    #
    # 07.01.2013  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def LoadTaggList( self, startChr ):
        try:
            urlNext = None
            tmpBldr = System.Text.StringBuilder()

            # all command- or rubrics start with 'PARAGRAPH-Symbol' ( see webconfig "rubricCmdTagg" ). they should not be listed
            forbiddenChar = WebConfigurationManager.AppSettings["rubricCmdTagg"][0]
            if startChr == forbiddenChar : return

            # txtBld = System.Text.StringBuilder()
            mngoId =  self.ui.getCtrl('sel_lctn').SelectedValue
            foundTgs = self.taggs.getTaggsByLocName( mngoId , startChr )

            # sort by amount 
            sorted(foundTgs, key=lambda taggs: taggs[1])

            iCnt = 0                                                # count the number in the list
            iPos = 0                                                # helper var to define the row
            self.Page.ViewState['TAGG_LIST'] = foundTgs

            pnlChooser = { 0 : 'pnl_0' 
                          ,1 : 'pnl_1'
                          ,2 : 'pnl_2'
                          ,3 : 'pnl_3'}

            for itm in foundTgs: 
                # create a comma-seperated string for jquery auto complete edit
                tmpBldr.Append(itm[0])
                tmpBldr.Append(',')

                # add a linkbutton to the webform
                lnkBtn = LinkButton()
                lnkBtn.Text = itm[0]
                lnkBtn.ID = 'hyLnk_tagg_' + System.Convert.ToString( iCnt )
                lnkBtn.EnableViewState = False 
                lnkBtn.Click += self.HandlBtnClick

                pnlDest = self.ui.getCtrl( pnlChooser[iPos] )
                pnlDest.Controls.Add(lnkBtn)
                pnlDest.Controls.Add(LiteralControl('<br />'))

                iCnt += 1
                iPos += 1
                if iPos == 4 : iPos = 0
            
            self.ui.getCtrl('rawdata').InnerHtml = unicode( tmpBldr.ToString()[:-1] )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())

        if urlNext != None:
            self.Page.Response.Redirect( self.Page.ResolveUrl( urlNext ) )














# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
#
# helper for ~/projector_DebateMap : THE card showing stuff
#  
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -

class MapProjector ( mongoDbMgr.mongoMgr ):
    '''
    MapProjector is the helper-class for the main-map webform
    '''

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # constructor. 
    #
    #
    # 16.01.2013   - bervie-      initial realese
    # 14.06.2013   - bervie-      added load of matrix-definitions from a file
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def __init__(self, page ):
        try:
            mongoDbMgr.mongoMgr.__init__(self, page )      # wake up papa ; mother njbTools is included by inheritance!
            self.ui.getCtrlTree( self.Page )
            self.lcDfnr = LocDefiner( page )                # the helper class for location-stuff

            self.log.w2lgDvlp('MapProjector( .. ) constructor called')

            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
            #
            # currently the start-screen is the webform Default.aspx : there we will use a welcome message
            #
            # if rhe website is not visited for the first time we set as flag to avoid automatic opening of the help-modal
            #if page.Session['MAP_ALREADY_VISITED'] is None:
            #    page.Session['MAP_ALREADY_VISITED'] = 'YES'
            #else:
            #    self.ui.findCtrl(self.Page, 'lbl_already_visited').Text = 'YES'
            self.ui.findCtrl(self.Page, 'lbl_already_visited').Text = 'YES'
            #
            #
            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

            self.param = {}                                                 # the URL-parameters are stored in member-attribute param = {}
            #self.param.Add('ItemType', None)
            #self.param.Add('SliceActive', None)
            #self.param.Add('CrsCmd', None)
            #self.param.Add('ResultLength', None)

            self.param.Add('Loc', None)
            self.param.Add('City', None)
            self.param.Add('Tags', None)
            self.param.Add('SrchMd', None)
            self.param.Add('StartDate', None)
            self.param.Add('EndDate', None)

            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
            # 22.10.2013- CR bervie
            # the rubric-selection will done with an ajax-call in the future
            #
            #
            #destination = self.ui.findCtrl(self.Page, 'date_event_div')
            #destination.InnerHtml = self.ui.rubricDict['date_event_div']
            #destination = self.ui.findCtrl(self.Page, 'location_div')
            #destination.InnerHtml = self.ui.rubricDict['location_div']
            #destination = self.ui.findCtrl(self.Page, 'annonce_div')
            #destination.InnerHtml = self.ui.rubricDict['annonce_div']
            #destination = self.ui.findCtrl(self.Page, 'initiative_div')
            #destination.InnerHtml = self.ui.rubricDict['initiative_div']
            #destination = self.ui.findCtrl(self.Page, 'business_div')
            #destination.InnerHtml = self.ui.rubricDict['business_div']
            #
            #
            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


            # the link that will be created by javascript depends on loggin-status of the user
            # if logged in he can comment an item, if not he only can take a look
            url = WebConfigurationManager.AppSettings['AddArticleToDebate']                         # search for debates
            if not self.usrDt.isLoggedIn():
                url = WebConfigurationManager.AppSettings['DetailsForStrangers']                    # use view-detail-dialog for not logged in users
            url += '?item='
            self.ui.findCtrl(self.Page, 'lbl_display_url').Text = '.' + url[1:]

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    #
    # user_interface_functions
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def pgLoad( self ):
        try:
            if ('ItemType' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['ItemType'] != System.String.Empty:
                    self.param['ItemType'] = self.Page.Request.QueryString['ItemType']

            # SliceActive is not used in the CACHE. we always check the whole data in the cache
            if ('SliceActive' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['SliceActive'] != System.String.Empty:
                    self.param['SliceActive'] = System.Convert.ToInt32( self.Page.Request.QueryString['SliceActive'])

            if ('CrsCmd' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['CrsCmd'] != System.String.Empty:
                    self.param['CrsCmd'] = self.Page.Request.QueryString['CrsCmd']

            if ('ResultLength' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['ResultLength'] != System.String.Empty:
                    self.param['ResultLength'] = System.Convert.ToInt32( self.Page.Request.QueryString['ResultLength'])

            if ('Loc' in self.Page.Request.QueryString.Keys):
                if len(self.Page.Request.QueryString['Loc']) > 2 :      # even if Loc = '0|' or 'de|41836' the location is not representing a postcode-area
                    self.param['Loc'] = self.Page.Request.QueryString['Loc']

            if ('City' in self.Page.Request.QueryString.Keys):
                if len(self.Page.Request.QueryString['City']) != System.String.Empty:
                    self.param['City'] = self.Page.Request.QueryString['City']

            if ('Tags' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['Tags'] != ',' :       # if no Tags were send we get ','. dont ask why :-)
                    self.param['Tags'] = self.Page.Request.QueryString['Tags']

            if ('SrchMd' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['SrchMd'] != System.String.Empty:
                    self.param['SrchMd'] = self.Page.Request.QueryString['SrchMd']

            if ('StartDate' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['StartDate'] != System.String.Empty:
                    self.param['StartDate'] = System.Convert.ToDateTime( self.Page.Request.QueryString['StartDate'] )
            if ('EndDate' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['EndDate'] != System.String.Empty:
                    self.param['EndDate'] = System.Convert.ToDateTime( self.Page.Request.QueryString['EndDate'] )

            # 01.12.2013 predefine hometown of user if he is logged in . . .. . .. .. .
            # init the coutry-selector 
            cntrySel = self.ui.getCtrl('sel_country')
            cntrySel.Items.Clear()
            self.lcDfnr.uiFillCtrySlct(cntrySel)
            self.insrtLocConfg()
            
            # 01.12.2013  OBSOLETE : LocDefiner is used now
            ## but if we have location-definition in the URL-parameter use that
            #if self.param['Loc'] !=  None:
            #    locLst = self.param['Loc'].strip().split(',')
            #    self.ui.getCtrl( 'sel_country'  ).SelectedValue = locLst[0]
            #    self.ui.getCtrl( 'txbx_postCode' ).Text = locLst[1]
            #if self.param['City'] !=  None :        self.ui.getCtrl( 'txbx_city'   ).Text = self.param['City']

            if self.param['Tags'] !=  None :        self.ui.getCtrl( 'txbx_hashtag').Text = self.param['Tags']
            if self.param['StartDate']  !=  None: self.ui.getCtrl( 'txbx_timeFrom' ).Text = self.param['StartDate'].ToString('dd.MM.yyyy')
            if self.param['EndDate']    !=  None: self.ui.getCtrl( 'txbx_timeTo'   ).Text = self.param['EndDate'].ToString('dd.MM.yyyy')

            ## 17.09.2013 bervie changed for facebook-posts
            #if self.param['Tags'] != None :
            #    placeStrng = 'in' 
            #    if self.ui.getCtrl( 'txbx_postCode' ).Text != '' : placeStrng = ' PLZ: ' + self.ui.getCtrl( 'txbx_postCode' ).Text 
            #    if self.ui.getCtrl( 'txbx_city' ).Text != '' : placeStrng += ' ' + self.ui.getCtrl( 'txbx_city' ).Text
            #    if placeStrng == 'in' : placeStrng = ''
            #    self.Page.Header.Title =  self.param['Tags'].replace(',',' ').upper() + ' ' + placeStrng.upper() + ' auf der nejoba-Karte'
            ## 17.09.2013 bervie end


            # 17.09.2013 bervie changed for facebook-posts ----------------------------------------------------------------------------------------
            if self.param['Tags'] != None :
                placeStrng = 'in'
                if self.ui.getCtrl( 'txbx_postCode' ).Text != '' : placeStrng = ' PLZ: ' + self.ui.getCtrl( 'txbx_postCode' ).Text 
                if self.ui.getCtrl( 'txbx_city' ).Text != '' : placeStrng += ' ' + self.ui.getCtrl( 'txbx_city' ).Text
                if placeStrng == 'in' : placeStrng = ''
                self.Page.Header.Title =  self.param['Tags'].replace(',',' ').upper() + ' ' + placeStrng.upper() + ' auf der nejoba-Karte'
            else:
                if (self.ui.getCtrl( 'txbx_postCode' ).Text != '') or (self.ui.getCtrl( 'txbx_city' ).Text != ''):
                    placeStrng = ''
                    if self.ui.getCtrl( 'txbx_postCode' ).Text != '' : placeStrng = ' PLZ: ' + self.ui.getCtrl( 'txbx_postCode' ).Text 
                    if self.ui.getCtrl( 'txbx_city' ).Text != '' : placeStrng += ' ' + self.ui.getCtrl( 'txbx_city' ).Text
                    self.Page.Header.Title = 'nejoba-Karte :  ' + placeStrng.upper()
            # 17.09.2013 bervie end ----------------------------------------------------------------------------------------------------------------



        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    #
    # insrtUsersData : if user is logged in his hometown will be inserted into the modal-dialog
    #
    # 08.09.2013 bervie if we have url-parameter the hometown of the user should not be inserted. use the query-parameter instead
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def insrtLocConfg( self ):
        try:
            if len(self.Page.Request.QueryString) > 0 : 
                if self.param['Loc'] !=  None:
                    locLst = self.param['Loc'].strip().split(',')
                    self.ui.getCtrl( 'sel_country'  ).SelectedValue = locLst[0]
                    self.ui.getCtrl( 'txbx_postCode' ).Text = locLst[1]
            else:
                # 01.12.2013 Bervie CR : use the location defined in the LocDefiner
                lctnCnfg = self.lcDfnr.uiInitProjector()
                self.ui.getCtrl('sel_country').SelectedValue = lctnCnfg['COUNTRY']
                self.ui.getCtrl('txbx_city').Text = lctnCnfg['CITY']
                self.ui.getCtrl('txbx_postCode').Text = lctnCnfg['POSTCODE']
                # 01.12.2013 Bervie CR : use the location defined in the LocDefiner
                return 

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())























# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
#
# helper for debatzeProjector.aspx.py : the form used to log-in or to change to the account-creation-webform
#  
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
class DebateProjector( mongoDbMgr.mongoMgr ):
    '''
    DebateProjector is the helper-class for the neighbour-forum
    '''

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # constructor. 
    #
    #
    # 16.01.2013   - bervie-      initial realese
    # 14.06.2013   - bervie-      added load of matrix-definitions from a file
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def __init__(self, page ):
        try:
            mongoDbMgr.mongoMgr.__init__(self, page )      # wake up papa ; mother njbTools is included by inheritance!
            self.log.w2lgDvlp('DebateProjector( .. ) constructor called')

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    #
    # insrtUsersData : if user is logged in his hometown will be inserted into the modal-dialog
    #
    # 08.09.2013 bervie if we have url-parameter the hometown of the user should not be inserted. use the query-parameter instead
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def insrtUsersData( self ):
        try:
            if len(self.Page.Request.QueryString) > 0 : return       # 08.09.2013

            if self.usrDt.isLoggedIn():
                self.ui.getCtrl( 'sel_country'  ).SelectedValue = self.usrDt.userDict['countrycode'].ToString()
                self.ui.getCtrl( 'txbx_postCode' ).Text = self.usrDt.userDict['postcode'].ToString()
                self.ui.getCtrl( 'lbl_userId' ).Text = self.usrDt.userDict['_id'].ToString()

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    #
    # hndlUrlParam : this function checks if we have URL-parameter and stores the in the corresponding edit-fields
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def hndlUrlParam( self ):
        try:
            #http://localhost:1572/njb_2/wbf_activemap/map_two.aspx?SliceActive=1&CrsCmd=end_of_data&ResultLength=2500&ItemType=map&Loc=0,&StartDate=&EndDate=&SrchMd=OR&Tags=,&#

            self.param = {}                                                 # the URL-parameters are stored in member-attribute param = {}
            self.param.Add('ItemType'       , None)         # map,list or date
            self.param.Add('SliceActive'    , None)         # which slice is active on the db
            self.param.Add('CrsCmd'         , None)         # cursor-positioning-command
            self.param.Add('ResultLength'   , None)         # length to receive
            self.param.Add('Loc'            , None)
            self.param.Add('City'           , None)
            self.param.Add('Tags'           , None)
            self.param.Add('SrchMd'         , None)
            self.param.Add('StartDate'      , None)
            self.param.Add('EndDate'        , None)


            if ('ItemType' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['ItemType'] != System.String.Empty:
                    self.param['ItemType'] = self.Page.Request.QueryString['ItemType']

            # SliceActive is not used in the CACHE. we always check the whole data in the cache
            if ('SliceActive' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['SliceActive'] != System.String.Empty:
                    self.param['SliceActive'] = System.Convert.ToInt32( self.Page.Request.QueryString['SliceActive'])

            if ('CrsCmd' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['CrsCmd'] != System.String.Empty:
                    self.param['CrsCmd'] = self.Page.Request.QueryString['CrsCmd']

            if ('ResultLength' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['ResultLength'] != System.String.Empty:
                    self.param['ResultLength'] = System.Convert.ToInt32( self.Page.Request.QueryString['ResultLength'])

            if ('Loc' in self.Page.Request.QueryString.Keys):
                if len(self.Page.Request.QueryString['Loc']) > 2 :      # even if Loc = '0,' or 'de,41836' the location is not representing a postcode-area
                    self.param['Loc'] = self.Page.Request.QueryString['Loc']

            if ('City' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['City'] != System.String.Empty:
                    self.param['City'] = self.Page.Request.QueryString['City']

            if ('Tags' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['Tags'] != ',' :       # if no Tags were send we get ','. dont ask why :-)
                    self.param['Tags'] = self.Page.Request.QueryString['Tags']

            if ('SrchMd' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['SrchMd'] != System.String.Empty:
                    self.param['SrchMd'] = self.Page.Request.QueryString['SrchMd']

            if ('StartDate' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['StartDate'] != System.String.Empty:
                    self.param['StartDate'] = System.Convert.ToDateTime( self.Page.Request.QueryString['StartDate'] )
            if ('EndDate' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['EndDate'] != System.String.Empty:
                    self.param['EndDate'] = System.Convert.ToDateTime( self.Page.Request.QueryString['EndDate'] )

            if self.param['Loc'] !=  None:
                locLst = self.param['Loc'].strip().split(',')
                self.ui.getCtrl( 'sel_country'  ).SelectedValue = locLst[0]
                self.ui.getCtrl( 'txbx_postCode' ).Text = locLst[1]
            if self.param['City']  !=  None: self.ui.getCtrl( 'txbx_city' ).Text = self.param['City']

            if self.param['StartDate']  !=  None: self.ui.getCtrl( 'txbx_timeFrom' ).Text = self.param['StartDate'].ToString('dd.MM.yyyy')
            if self.param['EndDate']    !=  None: self.ui.getCtrl( 'txbx_timeTo'   ).Text = self.param['EndDate'].ToString('dd.MM.yyyy')
            if self.param['Tags']       !=  None: 
                commaPos = self.param['Tags'].find(',')                                         # get the hashtags given by the user found after the first comma
                self.ui.getCtrl( 'txbx_hashtag'  ).Text = self.param['Tags'][commaPos:]
                if commaPos != 0:                                                               # get the rubric-tac. that is the stringpart before the first comma
                    self.ui.getCtrl( 'txbx_tagforitem'  ).Text = self.param['Tags'][:commaPos]
                    # REMEMBER : the hashtag is only written in the hidden txt-box. 
                    #            in future there must be a javascript-function that gets the 
                    #            corresponding tag for the parameter out of the configuration-div

            # 17.09.2013 bervie changed for facebook-posts ----------------------------------------------------------------------------------------
            if self.param['Tags'] != None :
                placeStrng = 'in'
                if self.ui.getCtrl( 'txbx_postCode' ).Text != '' : placeStrng = ' PLZ: ' + self.ui.getCtrl( 'txbx_postCode' ).Text 
                if self.ui.getCtrl( 'txbx_city' ).Text != '' : placeStrng += ' ' + self.ui.getCtrl( 'txbx_city' ).Text
                if placeStrng == 'in' : placeStrng = ''
                self.Page.Header.Title =  self.param['Tags'].replace(',',' ').upper() + ' ' + placeStrng.upper() + ' im nejoba-Forum'
            else:
                if (self.ui.getCtrl( 'txbx_postCode' ).Text != '') or (self.ui.getCtrl( 'txbx_city' ).Text != ''):
                    placeStrng = ''
                    if self.ui.getCtrl( 'txbx_postCode' ).Text != '' : placeStrng = ' PLZ: ' + self.ui.getCtrl( 'txbx_postCode' ).Text 
                    if self.ui.getCtrl( 'txbx_city' ).Text != '' : placeStrng += ' ' + self.ui.getCtrl( 'txbx_city' ).Text
                    self.Page.Header.Title = 'nejoba-Forum :  ' + placeStrng.upper()
            # 17.09.2013 bervie end ----------------------------------------------------------------------------------------------------------------

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())




    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    #
    # pgLoad: called from page-load event:       define the display-webform logged in users see the one with comment-editor-fuinctionality
    #                                            gets the hometown of the user in the modal-dialog if logged in 
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def pgLoad( self ):
        try:
            # the link that will be created by javascript depends on loggin-status of the user
            # if logged in he can comment an item, if not he only can take a look
            url = WebConfigurationManager.AppSettings['AddArticleToDebate']                         # search for debates

            if not self.usrDt.isLoggedIn():
                url = WebConfigurationManager.AppSettings['DetailsForStrangers']                    # use view-detail-dialog for not logged in users
            url += '?item='
            self.ui.findCtrl(self.Page, 'lbl_display_url').Text = '.' + url[1:]

            self.insrtUsersData()                   # if user is logged in his hometown will be placed in the modal-dialog location-part
            self.hndlUrlParam()                     # copy the url-parameter we have received into the modal-dialog

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())

















# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
#
# helper for wbf_activemap/create_map_user.aspx.py
#  
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
class CreateMapUser(mongoDbMgr.mongoMgr):
    # ***********************************************************************************************************************************************
    # constructor : call the base class constructor to initialize log, cache, ui-helper and page-member
    #
    # 28.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def __init__(self, pg):
        try:
            mongoDbMgr.mongoMgr.__init__(self, pg)      # wake up papa ; mother njbTools is included by inheritance!
            self.ui.getCtrlTree( pg )
            self.confirmUrl = None
            # self.log.w2lgDvlp('constructor of class CreateMapUser(Page) called!')

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # createUser : function strats user registration process (incl. MailCaptcha)
    #
    # 29.11.2011    berndv  initial realese
    # 05.05.2013    berndv  added location-check
    # ***********************************************************************************************************************************************
    def createUser(self):
        try:
            self.okFlag = True                                                  # indicator if something went wrong
            if self.okFlag is True : self.okFlag = self.checkDoubles()          # check password and email input
            if self.okFlag is True : self.okFlag = self.checkInput()            # check input (all edits must be filled)
            if self.okFlag is True : self.okFlag = self.checkAlreadyExisting()  # if eMail allready taken warn user about ( later option: change password !!)
            if self.okFlag is True : self.okFlag = self.createSessionDict()     # copy the user input into the session-cache self.ui.usrdata[]
            if self.okFlag is True : self.okFlag = self.createCodes()           # generate captcha and GUID for the user
            if self.okFlag is True : self.okFlag = self.createNickName()        # if user has not added a nickname the function creates the name displayed in the system
            if self.okFlag is True : self.okFlag = self.createPlaceList()       # convert seperated-string-list to arrays. this makes it possible 2 add indexes in the mongo-db
            if self.okFlag is True : self.okFlag = self.createMarker()          # function cretes the document-elements needed to diplay the markers in the map
            if self.okFlag != True : return False
            self.okFlag = self.writeUser2Db()                                   # store stuff into database

            # send the user an email with the confirmation-code and the link to end the registration-process
            if self.okFlag is True : self.okFlag = self.prepMail()
            if self.okFlag is True : self.okFlag = self.sendMail()

            if self.okFlag != True : 
                self.log.w2lgDvlp('error when creating user account. writing to DB or sending email was not working for : ' + str( self.usrDt.userDict['email'] ) )
                return False

            return True

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # checkDoubles : function checks the input that must be given double:
    #                email and password
    #
    # 29.11.2011    berndv  initial realese
    # 07.06.2013    berndv  added new check-function
    # ***********************************************************************************************************************************************
    def checkDoubles(self):
        try:
            # check users password choice
            pwd1 = self.ui.getCtrl(  'txbx_pwd1').Text
            pwd2 = self.ui.getCtrl(  'txbx_pwd2').Text
            email1 = self.ui.getCtrl('txbx_email').Text
            email2 = self.ui.getCtrl('txbx_emailconfirm').Text

            if ( pwd1 != pwd2 ) :
                self.errorMessage( self.ui.getCtrl('msg_pwdNotMatch').Text )
                return False

            if ( len(pwd1) < 5) :
                self.errorMessage( self.ui.getCtrl('msg_pwdToShort').Text  )
                return False

            if ( email1 != email2 ) :
                self.errorMessage( self.ui.getCtrl('msg_emailNotMatch').Text )
                return False

            # check mail is a valid address
            if not re.match( '[^@]+@[^@]+\.[^@]+' , email1 ) :
                self.errorMessage( self.ui.getCtrl('msg_emailWrongFormat').Text )
                self.log.w2lgDvlp('wrong email formating  regular expression : ' + email1 )
                return False

            if len(email1) < 7:
                self.errorMessage( self.ui.getCtrl('msg_emailWrongFormat').Text )
                self.log.w2lgDvlp('wrong email formating  less than 7 chars  : ' + email1 )
                return False

            return True

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())
            self.okFlag = False


    # ***********************************************************************************************************************************************
    # checkInput : check users input and stop process if he has forgotten some stuff
    #
    # 29.11.2011    berndv  initial realese
    # 07.06.2013    berndv  added new check-function
    # ***********************************************************************************************************************************************
    def checkInput(self):
        try:
            txtExsts = 1
            
            # get the input of the needed edits
            include = ['txbx_nickname','txbx_postcode','txbx_email','txbx_emailconfirm','txbx_pwd1','txbx_pwd2']
            self.ui.getCtrlTxt('txbx_')
            for item in self.ui.ctrlDict.keys():
                if item not in include : break
                txt = self.ui.ctrlDict[item].Text.strip()
                if len( txt ) == 0: 
                    return False

            if (txtExsts != 1) :
                self.errorMessage( self.ui.getCtrl('msg_inputGap').Text )
                return False

            # check if user accepst data-protection-agreement
            if self.ui.getCtrl('ckbx_accept_privacy_statement').Checked == False:
                self.errorMessage( self.ui.getCtrl('msg_accept_privacy').Text )
                return False

            return True

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())
            self.okFlag = False


    # ***********************************************************************************************************************************************
    # alreadyExisting : this function checks if we already have a user with the given mailadress
    #
    # 02.12.2011    berndv  initial realese
    # 07.06.2013    berndv  added new check-function
    # ***********************************************************************************************************************************************
    def checkAlreadyExisting(self):
        try:
            # check in collection user.final if user allread exists, which means email allready in use
            # if so later we will open a renew-password weform
            userLogin = self.ui.getCtrl('txbx_email').Text
            coll = self.database.GetCollection('user.final')                # set the collection to be accesed
            qry  = QueryDocument('email',userLogin)                         # prepare the query to search the needed document
            doc = coll.Find(qry)                                     
            count = doc.Count()
            self.log.w2lgDvlp('number of found docs in the user.final-collection - ' + str(count) + ' for : ' + userLogin )

            if count != 0 :                 # email is already in use : later nejoba will open a renew-password-dialog here (with email-captcha)
                self.errorMessage( self.ui.getCtrl('msg_userAlreadyExists').Text )
                self.log.w2lgDvlp( 'there is already an account for ' + userLogin + '! Account can not be created !' )
                return False

            return True

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())
            self.okFlag = False


    # ***********************************************************************************************************************************************
    # createSessionDict : write users input into the User-Data dictionary
    #
    # 29.11.2011    berndv  initial realese
    # 07.06.2013    berndv  added new check-function
    # ***********************************************************************************************************************************************
    def createSessionDict(self):
        try:
            # 1.  copy the stuff from the inputs (filled by user or ajax) into the session-cache of the user
            self.ui.getCtrlTxt('txbx_')
            for item in self.ui.ctrlDict.keys():
                if (item != None) and ('txbx_pwd' not in item):
                    # get the textboxes
                    if item.find('txbx_') == 0:
                        key = item[5:]
                        value = self.ui.ctrlDict[item].Text.strip()
                        self.usrDt.addNewItem(key, value)

            # 2. if no picture given we add a default pict (anonymus)
            if len( self.usrDt.getItem('picturl')) == 0:
                anonymusPictUrl = 'http://guikblog.com/wp-content/uploads/2012/08/anonymus-logo-.png'
                #anonymusPictUrl = './img/anonymous_logo_small.png'
                self.usrDt.userDict['picturl'] = anonymusPictUrl
            
            # 3. add special-items that are not editable
            # key = 'creationtime'
            # value = System.DateTime.UtcNow
            # self.usrDt.addNewItem(key, value)
            key = 'countrycode'
            value = self.ui.ctrlDict['drpd_countrycode'].SelectedValue
            self.usrDt.addNewItem(key, value)
            key = 'languagecode'
            value = self.ui.ctrlDict['drpd_language'].SelectedValue
            self.usrDt.addNewItem(key, value)
            key = 'areasize'
            value = WebConfigurationManager.AppSettings['areaSize']
            self.usrDt.addNewItem(key, value)
            key = 'item_type'
            value = self.ui.ctrlDict['drpd_item_type'].SelectedValue
            self.usrDt.addNewItem(key, value)
            key = 'password'
            value = self.EncryptSHA512Managed( self.ui.getCtrl('txbx_pwd1').Text.strip() )
            self.usrDt.addNewItem(key, value)

            # 4.  write the items in the user-cache to the log for debugging-reasons
            self.log.w2lgDvlp('-- start -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- what is in the user-session dict after createSessionDict' )
            for item in self.usrDt.userDict.keys():
                self.log.w2lgDvlp( 'name of ctrl : ' + item + '     | text-value  : ' + unicode(self.usrDt.userDict[item]) )
            self.log.w2lgDvlp('-- end   -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- what is in the user-session dict after createSessionDict' )

            return True

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())
            self.okFlag = False


    # **********************************************************************************************************************************************************************************************************************************************************************************************
    # createCodes : create an random captcha code and a GUID for the mail. the guid is used as url-parameter 
    #
    # 29.11.2011    berndv  initial realese
    # 07.06.2013    berndv  added new check-function
    # ***********************************************************************************************************************************************
    def createCodes(self):
        try:
            guid = System.Guid.NewGuid().ToString('N')                                              # global unique ID
            
            codeSource         = WebConfigurationManager.AppSettings['CodeGenQueue']                # get configuration from web.config
            lengthCaptchaStrng = int(WebConfigurationManager.AppSettings['captchaStrngLngth'])
            
            captcha = ''                                                                            # create captcha code
            for a in range(lengthCaptchaStrng):
                apd = random.choice(codeSource)
                captcha += apd
            
            self.usrDt.addNewItem('GUID', guid)                                                     # save to session cache
            self.usrDt.addNewItem('CAPTCHA', captcha)

            return True

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())
            self.okFlag = False


    # ***********************************************************************************************************************************************
    # writeUser2Db : store the user data in the mongo databases. the copy to the sql-server membership db will be done in verify_user.py 
    #
    # 09.01.2012    berndv  initial realese
    # 07.06.2013    berndv  added new check-function
    # ***********************************************************************************************************************************************
    def createNickName(self):
        try:
            nckname = self.usrDt.userDict['nickname']                   # check if there is a display-name chosen by the user. if not there will be created one automatically
            if (len(nckname) < 1):
                self.usrDt.userDict['nickname'] = 'Anonymus'            # nckname = self.usrDt.userDict['forename'] + ' ' + self.usrDt.userDict['familyname']
            return True

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())
            self.okFlag = False


    # ***********************************************************************************************************************************************
    # createPlaceList : user has gave aus a country-code and a post-code. this will be the middle of his service-area where he can check be active
    #                   this function generates a list with the ids of all cities that are inside the area-size that is configured in web.config area-size
    #
    #                   the list will contain the ids of the cities that are of interest
    #                   
    #
    # 08.12.2012    berndv  initial realese
    # 07.01.2013    bervie  changed getPlacesByPostcode
    #                       function now returns all data than only a part. the index has changed
    #                       cities.Add(item[0]) to cities.Add(item[1])
    # 07.06.2013    berndv  added new check-function
    # ***********************************************************************************************************************************************
    def createPlaceList(self):
        try:
            areaSize        = self.usrDt.userDict['areasize']                               # self.log.w2lgDvlp('CreateMapUser.createPlaceList creating a array with the places that belong to this account !!')
            countryCode     = self.usrDt.userDict['countrycode']
            postCode        = self.usrDt.userDict['postcode']

            self.log.w2lgDvlp('areaSize        = ' + areaSize   )
            self.log.w2lgDvlp('countryCode     = ' + countryCode)
            self.log.w2lgDvlp('postCode        = ' + postCode   )
            places = self.geoSrc.getPlacesByPostcode( countryCode, postCode, areaSize )     # get an sorted array with the service-area of the user and store it into the usr-session

            cities = []
            for item in places : cities.Add(item[1])

            # if no cities were found abort insert
            if len(cities) == 0:
                errStr = self.ui.getCtrl('msg_unknownPlace').Text 
                self.errorMessage(errStr)
                self.okFlag = 0
                return

            self.usrDt.userDict['cities'] = cities
            self.log.w2lgDvlp('cities added    = ' + str(type(cities)) + ' number of items : ' + str(len(cities)) )

            # 21.05.2013 add the coordinates for the marker in the map ------------------------------------------------------------------------
            # 'latitude'               6
            # 'longitude'              7
            hometown = places[0]
            lat = float(hometown[5])
            lon = float(hometown[6])

            return self.applyGeoCoords(lat,lon)

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())
            self.okFlag = False


    # **********************************************************************************************************************************************************************************************************************************************************************************************
    # applyGeoCoords : store the coordinates for the item. if we have no user input the function will create a random-point.
    #
    # param : lat    : the geographical latitude
    #         lon    : the geographical longitude
    #
    # returns nothing
    #
    # 31.05.2013    bervie  initial realese
    # 07.06.2013    berndv  added new check-function
    # ***********************************************************************************************************************************************
    def applyGeoCoords(self, lat, lon ):
        try:
            inptLat = self.ui.getCtrl('txbx_lat').Text.strip()
            inptLon = self.ui.getCtrl('txbx_lon').Text.strip()
            
            # check if the input for lat and long are floats. if correct system will use users input
            if ( re.match("^\d+?\.\d+?$", inptLat ) ) and ( re.match("^\d+?\.\d+?$", inptLon ) ) : return True

            # input must be valid float (checked before) or empty. if some chars were found in the edits this is an error
            if ( (len(inptLat) > 0 ) or  (len(inptLon) > 0 )) : 
                errStr = self.ui.getCtrl('msg_stupid_coords').Text 
                self.errorMessage(errStr)
                self.okFlag = 0
                return False

            # create a random-point in the area of the user
            rndDstnc = float( WebConfigurationManager.AppSettings['mapRndDistance'] )
            point = self.geoSrc.getRandomPoint( lat, lon, rndDstnc )
            self.usrDt.userDict['lat'] = str( point.lat )
            self.usrDt.userDict['lon'] = str( point.lon )
            self.ui.getCtrl('txbx_lat').Text = str( point.lat )
            self.ui.getCtrl('txbx_lon').Text = str( point.lon )

            # write it to the log for deverloping aid
            self.log.w2lgDvlp('CreateMapUser.applyGeoCoords added marker coordinates by random function in self.geoSrc.getRandomPoint : lat ' + self.usrDt.getItem('lat') + ' - long: ' + self.usrDt.getItem('lon') )

            return True

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())
            self.okFlag = False


    # **********************************************************************************************************************************************************************************************************************************************************************************************
    # createMarker : function creates and stores the data-elements that are needed to display the marker in the map
    #
    # returns nothing
    #
    # 31.05.2013    bervie  initial realese
    # 05.06.2013    bervie  if 'ckbx_map_confirmation' is nit checked the "marker_line" in the DB will be empty. 
    #                       the account won't be displayed in the map in that case
    # 07.06.2013    berndv  added new check-function
    # ***********************************************************************************************************************************************
    def createMarker( self ):
        try:
            countrycode = self.ui.ctrlDict['drpd_countrycode'].SelectedValue
            postcode = self.ui.ctrlDict['txbx_postcode'].Text.strip()
            postkey = countrycode + '|' + postcode

            # add the postcode-key ['DE|41836']
            self.usrDt.addNewItem( 'countrycode'  , countrycode )
            self.usrDt.addNewItem( 'postcode'     , postcode )
            self.usrDt.addNewItem( 'post_code_key', postkey)

            marker = System.String.Empty
            if self.ui.getCtrl('ckbx_map_confirmation').Checked is True:                #  05.06.13 only insert a marker-line for the map when the user wants to be added to the map
                marker = self.mapUser.createMarkerLine( self.usrDt.userDict )

            self.usrDt.addNewItem( 'marker_line', marker )

            return True

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())
            self.okFlag = False


    # **********************************************************************************************************************************************************************************************************************************************************************************************
    # writeUser2Db : store the user data in the mongo databases. the collection "user.initial" will be used to store all accounts that where created 
    #                when approved the data will be copied to user.final
    #
    # 09.01.2012    berndv  initial realese
    # 07.06.2013    berndv  added new check-function
    # ***********************************************************************************************************************************************
    def writeUser2Db(self):
        try:
            # self.log.w2lgDvlp('CreateUser.writeUser2Db called to store the user-data into mongo collection: user.initial')
            ctrlDct = {'collection':'user.initial','slctKey':None,'data':self.usrDt.userDict}
            newObjId = self.insertDoc(ctrlDct)

            return True

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())
            self.okFlag = False


    # ***********************************************************************************************************************************************
    # prepMail : to finalize the user-registration an email with a captcha code is send to the user. the user must enter this captcha code and 
    #            his password in the verification webform AppSettings['captchaWebForm']. the message for that mail is porepared here
    #
    # 25.11.2011    berndv  initial realese
    # 07.06.2013    berndv  added new check-function
    # ***********************************************************************************************************************************************
    def prepMail( self ):
        try:
            # load the template for the HTML-mail
            template = self.Page.Server.MapPath( WebConfigurationManager.AppSettings['ConfirmUserHtmlBody'] )
            self.log.w2lgDvlp('ConfirmUser->prepMail      = ' + template )
            file = open(template)
            mailBody = file.read()
            file.close()

            # get the configuration from the session cache
            cptch = self.usrDt.getItem('CAPTCHA')
            guid  = self.usrDt.getItem('GUID')

            captchaWebForm = self.Page.ResolveUrl(WebConfigurationManager.AppSettings['confirmUserForMap'])
            self.confirmUrl = self.Page.Request.Url.GetLeftPart( UriPartial.Authority )
            self.confirmUrl += captchaWebForm + "?key=" + guid

            # get mail-strings from the UI
            mailSubj = self.ui.getCtrl('msg_mailSubject').Text
            mailBody = mailBody.replace('###body###'  , cptch)
            mailBody = mailBody.replace('###link###'  , self.confirmUrl)
            mailBody = mailBody.replace('###link2###' , self.confirmUrl)

            self.mailSubj = unicode(mailSubj)
            self.mailBody = unicode(mailBody)

            return True

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())
            self.okFlag = False


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
    # 07.06.2013    berndv  added new check-function
    # ***********************************************************************************************************************************************
    def sendMail( self ):
        try:
            smtpServer = WebConfigurationManager.AppSettings['smtpServer']
            smtpUser = WebConfigurationManager.AppSettings['smtpUser']
            smtpPwd = WebConfigurationManager.AppSettings['smtpPwd']
            fromAddr = WebConfigurationManager.AppSettings['cptchSndrAdrss']
            toAddrs = self.usrDt.getItem('email')

            try:
                #Create A New SmtpClient Object
                mailClient              = SmtpClient(smtpServer,25)
                mailClient.EnableSsl    = True
                mailCred                = NetworkCredential()
                mailCred.UserName       = smtpUser
                mailCred.Password       = smtpPwd
                mailClient.Credentials  = mailCred

                msg = MailMessage( fromAddr, toAddrs)
                msg.SubjectEncoding = System.Text.Encoding.UTF8
                msg.BodyEncoding =  System.Text.Encoding.UTF8
                msg.IsBodyHtml          = True
                msg.Subject = self.mailSubj
                msg.Body = self.mailBody

                mailClient.Send(msg)

            except Exception,e:
                self.log.w2lgError(traceback.format_exc())
                self.okFlag = False

            return True

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())
            self.okFlag = False


    # ***********************************************************************************************************************************************
    # changeUser( .. )  : function is called to change the data of an existing user-account
    #
    # 02.01.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def changeUser(self):
        try:
            self.log.w2lgDvlp( 'CreateUser->change user called !  !   !  !   !  !   !  !   !  !   !  !   !  !   !  !    ' )
            self.checkInptBeforeUpdt()
            if self.okFlag == True :
                self.updateUserData()
                self.ui.getCtrl('divPwdChanged').Visible = True
                self.ui.getCtrl('btn_Create').Visible = False

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())
            self.okFlag = True


    # ***********************************************************************************************************************************************
    # checkInptBeforeUpdt( .. )  :  check input before write to data-base
    #
    # 02.01.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def checkInptBeforeUpdt(self):
        try:
            self.okFlag = True
            # check users password choice
            # REMARK: we are using hidden asp.net lable-controlls for the status messages to make the internationalization of the application more easy
            pwd1 = self.ui.getCtrl('txbx_pwd1').Text
            pwd2 = self.ui.getCtrl('txbx_pwd2').Text
            self.log.w2lgDvlp('password             : ' + pwd1 )
            self.log.w2lgDvlp('password confirmation: ' + pwd1 )

            if ( pwd1 != pwd2 ) :
                errStr = self.ui.getCtrl('msg_pwdNotMatch').Text 
                self.errorMessage(errStr)
                self.okFlag = False
                return self.okFlag
            if ( len(pwd1) < 5) :
                errStr = self.ui.getCtrl('msg_pwdToShort').Text
                self.errorMessage(errStr)
                self.okFlag = 0
                return self.okFlag

            return self.okFlag

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # updateUserData( .. )  : used to change the user-data of an existing account
    #
    # 02.01.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def updateUserData(self):
        try:
            self.ui.getCtrlTxt('txbx_')
            for item in self.ui.ctrlDict.keys():
                if (item != None) and ('txbx_pwd' not in item):

                    # get the textboxes
                    if (item.find('txbx_') == 0) and ('password' not in item):
                        key = item[5:]
                        value = self.ui.ctrlDict[item].Text.strip()
                        if value != System.String.Empty:
                            self.usrDt.addNewItem(key,value)
                            self.log.w2lgDvlp( 'create_map_user->updateUserData : KEY : ' + key + '    \t | value  : ' + value )

            self.usrDt.userDict[ 'areasize' ]       = WebConfigurationManager.AppSettings['areaSize']
            self.usrDt.userDict[ 'countrycode' ]    = self.ui.ctrlDict['drpd_countrycode'].SelectedValue
            self.usrDt.userDict[ 'languagecode' ]   = self.ui.ctrlDict['drpd_language'].SelectedValue
            self.usrDt.userDict[ 'creationtime' ]   = System.DateTime.UtcNow
            self.usrDt.userDict[ 'item_type' ]      = self.ui.ctrlDict['drpd_item_type'].SelectedValue

            # if no picture is given we use a default pict (anonymus)
            if len( self.usrDt.getItem('picturl')) == 0:
                anonymusPictUrl = 'http://guikblog.com/wp-content/uploads/2012/08/anonymus-logo-.png'
                #anonymusPictUrl = './img/anonymous_logo_small.png'
                self.usrDt.userDict[ 'picturl'] = anonymusPictUrl


            for ky in self.usrDt.userDict.keys():
                self.log.w2lgDvlp( 'cretae_map_user -> updateUserData : check dict data      : ' + str(ky) + ' ; value : ' + self.usrDt.userDict[ky].ToString()  )

            self.createMarker()         # create a new marker for the map if user wants to
            
            ignore = ['_id','cities','account_roles']   # update does insert all stuff as strings !! so some parts of the dictoonary should NOT be updated
            for keyInDct in self.usrDt.userDict.keys():
                ky = keyInDct.ToString()
                vl = self.usrDt.userDict[keyInDct].ToString()
                if ky in ignore : break

                value = self.usrDt.userDict[key].ToString()
                self.log.w2lgDvlp( '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -- - - - - - - -- - - - - - - -- - - - - - - -- - - - - - - - ' )
                self.log.w2lgDvlp( 'cretae_map_user -> updateUserData : item to update               : ' + ky )
                self.log.w2lgDvlp( 'cretae_map_user -> updateUserData : value of the item            : ' + vl )
                self.log.w2lgDvlp( '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -- - - - - - - -- - - - - - - -- - - - - - - -- - - - - - - - ' )
                updt = {}
                updt.update({'collection':'user.final'})
                updt.update({'slctKey': '_id' })
                updt.update({'slctVal':self.usrDt.getItem('_id')})

                updt.update({'updatKey':ky })
                updt.update({'updatVal':vl })
                chngdId = self.updateDoc(updt)
                self.log.w2lgDvlp( 'changed data of user.final-mongo-document : ' + chngdId + ' key  ' + ky + ' val  ' + vl )


            # special-case : if password is not empty update the password in crypted form
            password = self.ui.findCtrl(self.Page , 'txbx_pwd1').Text
            if password == System.String.Empty:
                return

            password = self.EncryptSHA512Managed(self.ui.getCtrl('txbx_pwd1').Text)
            self.usrDt.userDict['password'] = password

            updt = {}
            updt.update({'collection':'user.final'})
            updt.update({'slctKey': '_id' })
            updt.update({'slctVal':self.usrDt.getItem('_id')})

            updt.update({'updatKey':'password' })
            updt.update({'updatVal': password  })
            chngdId = self.updateDoc(updt)
            self.log.w2lgDvlp( 'changed password crypted of user.final-mongo-document : ' + chngdId )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())

































































# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
#
# helper for user_create.aspx.py : the form for creating a user-account or change the settigs of a given account
#  
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
class CreateUser(mongoDbMgr.mongoMgr):

    # ***********************************************************************************************************************************************
    # constructor : call the base class constructor to initialize log, cache, ui-helper and page-member
    #
    # 28.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def __init__(self, pg):
        try:
            mongoDbMgr.mongoMgr.__init__(self, pg)      # wake up papa ; mother njbTools is included by inheritance!
            self.okFlag = 1                     # flag indicates if the input was correct
            self.confirmUrl = None

            self.log.w2lgDvlp('constructor of class CreateUser(Page) aufgefufen!')
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # createUser : function strats user registration process (incl. MailCaptcha)
    #
    # 29.11.2011    berndv  initial realese
    # 05.05.2013    berndv  added location-check
    # ***********************************************************************************************************************************************
    def createUser(self):
        try:
            # check if input is valid to be used for a new account
            self.checkDoubles()                             # check password input from user
            self.checkInput()                               # check input (all edits must be filled)
            self.checkAlreadyExisting()                     # if eMail allready taken warn user about ( later option: change password !!)

            if self.okFlag == 0:
                self.log.w2lgError('user create was aborted for : ' + self.ui.getCtrl('txbx_email').Text )
                return;

            self.storeInput()                               # copy the user input into the input-cache

            # create artificial user-account-attributes
            self.createCodes()                              # generate captcha and GUID for the user
            self.createNickName()                           # if user has not added a nickname the function creates the name displayed in the system
            self.createPlaceList()                          # convert seperated-string-list to arrays. this makes it possible 2 add indexes in the mongo-db


            if self.okFlag == 0:
                self.log.w2lgError('user create was aborted for : ' + self.ui.getCtrl('txbx_email').Text + ' : okFlag was ZERO Error occured in createUser ' )
                return 0;

            # 05.05.2013 if no locations were found abort process
            if not self.usrDt.userDict.has_key('cities'):
                self.log.w2lgError('user create was aborted for : ' + self.ui.getCtrl('txbx_email').Text + ' : NO CITIES FOUND ' )
                return 0;
            
            self.writeUser2Db()                             # store stuff into database

            # send the user an email with the confirmation-code and the link to end the registration-process
            self.prepMail()
            self.sendMail()

            return self.okFlag

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # checkDoubles : function checks the input that must be given double:
    #                email and password
    #
    # 29.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def checkDoubles(self):
        try:
            # check users password choice
            # REMARK: we are using hidden asp.net lable-controlls for the status messages to make the internationalization of the application more easy
            pwd1 = self.ui.getCtrl(  'txbx_pwd1').Text
            pwd2 = self.ui.getCtrl(  'txbx_pwd2').Text
            email1 = self.ui.getCtrl('txbx_email').Text
            email2 = self.ui.getCtrl('txbx_emailconfirm').Text

            if ( pwd1 != pwd2 ) :
                errStr = self.ui.getCtrl('msg_pwdNotMatch').Text 
                self.errorMessage(errStr)
                self.okFlag = 0
                return
            if ( len(pwd1) < 5) :
                errStr = self.ui.getCtrl('msg_pwdToShort').Text 
                self.errorMessage(errStr)
                self.okFlag = 0
                return

            if ( email1 != email2 ) :
                errStr = self.ui.getCtrl('msg_emailNotMatch').Text 
                self.errorMessage(errStr)
                self.okFlag = 0
                return
            if '@' not in email1:
                errStr = self.ui.getCtrl('msg_emailWrongFormat').Text 
                self.errorMessage(errStr)
                self.okFlag = 0
                return

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # checkInput : check users input and stop process if he has forgotten some stuff
    #
    # 29.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def checkInput(self):
        try:
            txtExsts = 1

            # if len(self.ui.getCtrl('txbx_nickname').Text) < 1: txtExsts = 0
            if len(self.ui.getCtrl('txbx_email').Text) < 1: txtExsts = 0
            if len(self.ui.getCtrl('txbx_emailconfirm').Text) < 1: txtExsts = 0
            if len(self.ui.getCtrl('txbx_pwd1').Text) < 1: txtExsts = 0
            if len(self.ui.getCtrl('txbx_pwd2').Text) < 1: txtExsts = 0
            if len(self.ui.getCtrl('txbx_forename').Text) < 1: txtExsts = 0
            if len(self.ui.getCtrl('txbx_familyname').Text) < 1: txtExsts = 0
            if len(self.ui.getCtrl('txbx_postcode').Text) < 1: txtExsts = 0
            if len(self.ui.getCtrl('txbx_city').Text) < 1: txtExsts = 0
            if len(self.ui.getCtrl('txbx_email').Text) < 1: txtExsts = 0

            if (txtExsts != 1) :
                errStr = self.ui.getCtrl('msg_inputGap').Text 
                self.errorMessage(errStr)
                self.okFlag = 0

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # alreadyExisting : this function checks if we already have a user with the given mailadress
    #
    # 02.12.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def checkAlreadyExisting(self):
        try:
            # check in collection user.final if user allread exists, which means email allready in use
            # if so later we will open a renew-password weform
            userLogin = self.ui.getCtrl('txbx_email').Text
            coll = self.database.GetCollection('user.final')                # set the collection to be accesed
            qry  = QueryDocument('email',userLogin)                         # prepare the query to search the needed document
            doc = coll.Find(qry)                                     
            count = doc.Count()
            self.log.w2lgDvlp('number of found docs in the user.final-collection - ' + str(count) + ' for : ' + userLogin )

            if count == 0:
                # email adress is available for a new account
                self.log.w2lgDvlp( 'no account found for ' + userLogin + '. user-account can be created !' )

            else:
                # email is already in use : later nejoba will open a renew-password-dialog here (with email-captcha)
                errStr = self.ui.getCtrl('msg_userAlreadyExists').Text 
                self.errorMessage(errStr)
                self.log.w2lgDvlp( 'there is already an account for ' + userLogin + '. creation denied !' )
                self.okFlag = 0

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # storeInput : write users inpuit into the User-Data dictionary
    #
    # 29.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def storeInput(self):
        try:
            # 1.  copy the stuff from the inputs (filled by user or ajax) into the session-cache of the user
            self.ui.getCtrlTxt('txbx_')
            for item in self.ui.ctrlDict.keys():
                if (item != None) and ('txbx_pwd' not in item):
                    # get the textboxes
                    if item.find('txbx_') == 0:
                        key = item[5:]
                        value = self.ui.ctrlDict[item].Text
                        self.usrDt.addNewItem(key, value)

            # 2. add special-items to the user-data-dictionary
            key = 'password'
            value = self.EncryptSHA512Managed(self.ui.getCtrl('txbx_pwd1').Text)
            self.usrDt.addNewItem(key, value)
            key = 'areasize'
            value = WebConfigurationManager.AppSettings['areaSize']
            self.usrDt.addNewItem(key, value)
            key = 'countrycode'
            value = self.ui.ctrlDict['drpd_country'].SelectedValue
            self.usrDt.addNewItem(key, value)
            key = 'languagecode'
            value = self.ui.ctrlDict['drpd_language'].SelectedValue
            self.usrDt.addNewItem(key, value)
            key = 'creationtime'
            value = System.DateTime.UtcNow
            self.usrDt.addNewItem(key, value)
            
            # 3.  write the items in the user-cache to the log for debugging-reasons
            self.log.w2lgDvlp('-- start -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- what is in the user-session dict after storeInput' )
            for item in self.usrDt.userDict.keys():
                self.log.w2lgDvlp( 'name of ctrl : ' + item + '     | text-value  : ' + unicode(self.usrDt.userDict[item]) )
            self.log.w2lgDvlp('-- end   -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- what is in the user-session dict after storeInput' )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # **********************************************************************************************************************************************************************************************************************************************************************************************
    # createCodes : create an random captcha code and a GUID for the mail. the guid is used as url-parameter 
    #
    # 29.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def createCodes(self):
        try:
            guid = System.Guid.NewGuid().ToString('N')         # global unique ID

            # get configuration from web.config
            codeSource         = WebConfigurationManager.AppSettings['CodeGenQueue']
            lengthCaptchaStrng = int(WebConfigurationManager.AppSettings['captchaStrngLngth'])

            # create captcha code
            captcha = ''
            for a in range(lengthCaptchaStrng):
                apd = random.choice(codeSource)
                captcha += apd

            # save to session cache
            self.usrDt.addNewItem('GUID', guid)
            self.usrDt.addNewItem('CAPTCHA', captcha)

            return guid

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # writeUser2Db : store the user data in the mongo databases. the copy to the sql-server membership db will be done in verify_user.py 
    #
    # 09.01.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def createNickName(self):
        try:
            # check if there is a display-name chosen by the user. if not there will be created one automatically
            nckname = self.usrDt.userDict['nickname']
            if (len(nckname) < 1):
                # create a nickname from User input
                nckname = self.usrDt.userDict['forename'] + ' ' + self.usrDt.userDict['familyname']
                self.usrDt.userDict['nickname'] = nckname
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # createPlaceList : user has gave aus a country-code and a post-code. this will be the middle of his service-area where he can check be active
    #                   this function generates a list with the ids of all cities that are inside the area-size that is configured in web.config area-size
    #
    #                   the list will contain the ids of the cities that are of interest
    #                   
    #
    # 08.12.2012    berndv  initial realese
    # 07.01.2013    bervie  changed getPlacesByPostcode
    #                       function now returns all data than only a part. the index has changed
    #                       cities.Add(item[0]) to cities.Add(item[1])
    #
    # ***********************************************************************************************************************************************
    def createPlaceList(self):
        try:
            self.log.w2lgDvlp('CreateUser.createPlaceList creating a array with the places that belong to this account !!')
            
            areaSize        = self.usrDt.userDict['areasize']
            countryCode     = self.usrDt.userDict['countrycode']
            postCode        = self.usrDt.userDict['postcode']

            self.log.w2lgDvlp('areaSize        = ' + areaSize)
            self.log.w2lgDvlp('countryCode     = ' + countryCode)
            self.log.w2lgDvlp('postCode        = ' + postCode )

            # get an sorted array with the service-area of the user and store it into the usr-session
            places = self.geoSrc.getPlacesByPostcode( countryCode, postCode, areaSize )

            cities = []
            for item in places:
                cities.Add(item[1])

            # if no cities were found abort insert
            if len(cities) == 0:
                errStr = self.ui.getCtrl('msg_unknownPlace').Text 
                self.errorMessage(errStr)
                self.okFlag = 0
                return
            else:
                self.usrDt.addNewItem('cities', cities)

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # **********************************************************************************************************************************************************************************************************************************************************************************************
    # writeUser2Db : store the user data in the mongo databases. the collection "user.initial" will be used to store all accounts that where created 
    #                when approved the data will be copied to user.final
    #
    # 09.01.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def writeUser2Db(self):
        try:
            # self.log.w2lgDvlp('CreateUser.writeUser2Db called to store the user-data into mongo collection: user.initial')
            ctrlDct = {'collection':'user.initial','slctKey':None,'data':self.usrDt.userDict}
            newObjId = self.insertDoc(ctrlDct)

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # prepMail : to finalize the user-registration an email with a captcha code is send to the user. the user must enter this captcha code and 
    #            his password in the verification webform AppSettings['captchaWebForm']. the message for that mail is porepared here
    #
    # 25.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def prepMail( self ):
        try:
            # load the template for the HTML-mail
            template = self.Page.Server.MapPath( WebConfigurationManager.AppSettings['ConfirmUserHtmlBody'] )
            self.log.w2lgDvlp('ConfirmUser->prepMail      = ' + template )
            file = open(template)
            mailBody = file.read()
            file.close()

            # get the configuration from the session cache
            cptch = self.usrDt.getItem('CAPTCHA')
            guid  = self.usrDt.getItem('GUID')

            captchaWebForm = self.Page.ResolveUrl(WebConfigurationManager.AppSettings['ConfirmAccount'])
            self.confirmUrl = self.Page.Request.Url.GetLeftPart( UriPartial.Authority )
            self.confirmUrl += captchaWebForm + "?key=" + guid

            # get mail-strings from the UI
            mailSubj = self.ui.getCtrl('msg_mailSubject').Text
            mailBody = mailBody.replace('###body###'  , cptch)
            mailBody = mailBody.replace('###link###'  , self.confirmUrl)
            mailBody = mailBody.replace('###link2###' , self.confirmUrl)

            # self.log.w2lgDvlp(mailBody)

            self.mailSubj = unicode(mailSubj)
            self.mailBody = unicode(mailBody)
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
    def sendMail( self ):
        try:
            smtpServer = WebConfigurationManager.AppSettings['smtpServer']
            smtpUser = WebConfigurationManager.AppSettings['smtpUser']
            smtpPwd = WebConfigurationManager.AppSettings['smtpPwd']
            fromAddr = WebConfigurationManager.AppSettings['cptchSndrAdrss']
            toAddrs = self.usrDt.getItem('email')

            try:
                #Create A New SmtpClient Object
                mailClient              = SmtpClient(smtpServer,25)
                mailClient.EnableSsl    = True
                mailCred                = NetworkCredential()
                mailCred.UserName       = smtpUser
                mailCred.Password       = smtpPwd
                mailClient.Credentials  = mailCred

                msg = MailMessage( fromAddr, toAddrs)
                msg.SubjectEncoding = System.Text.Encoding.UTF8
                msg.BodyEncoding =  System.Text.Encoding.UTF8
                msg.IsBodyHtml          = True
                msg.Subject = self.mailSubj
                msg.Body = self.mailBody

                mailClient.Send(msg)

            except Exception,e:
                self.log.w2lgError(traceback.format_exc())

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # changeUser( .. )  : function is called to change the data of an existing user-account
    #
    # 02.01.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def changeUser(self):
        try:
            self.log.w2lgDvlp( 'CreateUser->change user called !  !   !  !   !  !   !  !   !  !   !  !   !  !   !  !    ' )
            self.checkInptBeforeUpdt()
            if self.okFlag != 0 :
                self.updateUserData()

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # ***********************************************************************************************************************************************
    # checkInptBeforeUpdt( .. )  :  check input before write to data-base
    #
    # 02.01.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def checkInptBeforeUpdt(self):
        try:
            # check users password choice
            # REMARK: we are using hidden asp.net lable-controlls for the status messages to make the internationalization of the application more easy
            pwd1 = self.ui.getCtrl('txbx_pwd1').Text
            pwd2 = self.ui.getCtrl('txbx_pwd2').Text
            self.log.w2lgDvlp('password             : ' + pwd1 )
            self.log.w2lgDvlp('password confirmation: ' + pwd1 )

            # if password-fields are left empty no change of the pwd wanted
            if (( pwd1 == System.String.Empty ) and ( pwd2 == System.String.Empty )):
                self.okFlag = 1
                return

            if ( pwd1 != pwd2 ) :
                errStr = self.ui.getCtrl('msg_pwdNotMatch').Text 
                self.errorMessage(errStr)
                self.okFlag = 0
                return
            if ( len(pwd1) < 5) :
                errStr = self.ui.getCtrl('msg_pwdToShort').Text
                self.errorMessage(errStr)
                self.okFlag = 0
                return
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # ***********************************************************************************************************************************************
    # updateUserData( .. )  : get input from userInterface
    #
    # 02.01.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def updateUserData(self):
        try:
            # 1.  copy the stuff from the inputs (filled by user or ajax) into the session-cache of the user
            self.ui.getCtrlTxt('txbx_')
            for item in self.ui.ctrlDict.keys():
                if (item != None) and ('txbx_pwd' not in item):

                    # get the textboxes
                    if (item.find('txbx_') == 0) and ('password' not in item):
                        key = item[5:]
                        value = self.ui.ctrlDict[item].Text
                        self.log.w2lgDvlp( 'KEY : ' + key + '    \t | value  : ' + value )

                        self.usrDt.userDict[key] = value

                        updt = {}
                        updt.update({'collection':'user.final'})
                        updt.update({'slctKey': '_id' })
                        updt.update({'slctVal':self.usrDt.getItem('_id')})

                        updt.update({'updatKey':key})
                        updt.update({'updatVal':value})
                        chngdId = self.updateDoc(updt)
                        self.log.w2lgDvlp( 'changed data of user.final-mongo-document : ' + chngdId )

            # special-case : if password is not empty update the password in crypted form
            password = self.ui.findCtrl(self.Page.Master , 'txbx_pwd1').Text
            if password == System.String.Empty:
                return

            password = self.EncryptSHA512Managed(self.ui.getCtrl('txbx_pwd1').Text)
            self.usrDt.userDict['password'] = password

            updt = {}
            updt.update({'collection':'user.final'})
            updt.update({'slctKey': '_id' })
            updt.update({'slctVal':self.usrDt.getItem('_id')})

            updt.update({'updatKey':'password' })
            updt.update({'updatVal': password  })
            chngdId = self.updateDoc(updt)
            self.log.w2lgDvlp( 'changed password crypted of user.final-mongo-document : ' + chngdId )


        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


















# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
#
# helper for dataSource__cache.aspx.py : the ajaxloader webform
#  
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
class CachedDataSource( mongoDbMgr.mongoMgr ):
    '''
    CachedDataSource : class that pre-select the items before it checks the additional filtering as defined in the URL-Parameter
    
    loads all items from the app-cache and creates JSON from it. It is a special-text-returning webform (ironpython is not capable to use webservices !
    the results depends on URL-parameter:
    description of the URL-PARAMETER for loading webform behind DataURL
 
   'http://../njb_2/wbf_topic/mapTwo_dataSource.aspx?loc=DE%7C41836&Tags=world&SrchMd=OR'
 
   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

    URL-parameter for the data-select:
        ItemType        : what type of item do we have? preselect before filtering 
                            can be :
                              1. map     item must have coordes
                              2. date    item must have start-date
                              3. list    any item allowed without filtering
        SliceActive     : receive which was the last slice the client read from
        CrsCmd       : the offset from startingpoint to continue reading at the rigth place
        ResultLength    : the number of items that should be send by the datasource
        Loc             : the geo-location as sting like "de|41836". if only "de|" is given all german 
                          results are send to the client from data-source
        Tags            : the Tags we are locking for. list is comma-seperated
        SrchMd          : OR means display all items with any tag; AND menas display only tags 
                          that are labeled with all keywords
        StartDate       : a string-coded date-object to define when the event starts
        EndDate         : a string-representation of the end of the event

   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

    class-attributes and their meaning
        self.Workbench      : string-builder for generating the return-output
        self.LocationList   : string with the locations-detail-data in the neighboerhood
        self.CrsCmd     : stores the last item that was loaded when maximum amount was reached. this value is send to the client
                              and will be used as startpoint for the next read.
                              HINT : if reading in cache the attribute stores the row-index; if we are reading in the mongo-id the 
                              item stores the _mongoID used in the database.
        self.ActvSliceIdx  : set to TRUE if end of the cache was reached. is returned to caller to change to database-access

        self.AmntSnd  : max-amount of items to send back to caller . value is a definition in the web.config
        self.SlicesCached   : the number of slices that are cached in the IIS. if we have a lot of data per day we can increrase the 
                              amount of days in a slice. so we have a faster DB-access and also a bigger amount of davys in the cache

   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

    member-functions and their job-description (in order of apperance)

        self.selQueryFunction           :   the functions is the entry-point. the parameter send to the data-source are used to 
                                            deceide what function is called

        self.idxLstByTags               :   function selects items with a tag when no postcode-area was defined
                                    
        self.idxLstByLocatedTags        :   function creates the list of row-endexes for taged items for a given postcode-area

        self.idxLstByLocation           :   get the row-indexes of all items in a postcode-area

        self.idxLstWithoutPreConditions :   if no tags and no locations were given this function goes through the table. it 
                                            checks ( if needed ) the country-code [example: "de for germany"]

        self.checkParamMatch            :   this function is used by all 'idxLst'-functions to check if all additional parameters 
                                            are matching the given row.

        self.cutSlice                :   the function cuts the needed page out of the result-array

        self.addDataItems               :   add the found data-items as JSON-code to the result-string-builder

        self.addConfigParam           :   add the controling parameter needed for the ListExtractor 

  '''


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # constructor. 
    #
    # member-attributes 
    #
    #    self.Workbench        string-builder for generating the return-output
    #    self.LocationList     string with the locations-detail-data in the neighboerhood
    #    self.CrsCmd       amount of items-cursor. stores the offset from the end of cache-item-table
    #    self.ActvSliceIdx    the data in the database is devides in pages. page 0 is the mem-cache in the application-cache of IIS. 
    #                          the following pages are in the database. they are seperated by dates. so every page has a defined num 
    #                          of days which belonges to it
    #
    # 27.06.2013   - bervie-      initial realese
    # 27.07.2013   - bervie-      added self.SlicesCached : the definition of how many slides are stored in the cache. when the number
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def __init__(self, page ):
        try:
            mongoDbMgr.mongoMgr.__init__(self, page )                                                                       # wake up papa ; mother njbTools is included by inheritance!

            self.Workbench      = System.Text.StringBuilder()                                                               # string-builder for generating the return-output
            self.LocationList   = []                                                                                        # string with the locations-detail-data in the neighboerhood
            self.SlicesCached   = System.Convert.ToInt32( WebConfigurationManager.AppSettings['SlicesCached'])              # the number of slices that are cached. 
            self.CrsCmd         = System.String.Empty                                                                       # the mongo-id of the item the lst read-process stopped
            self.ActvSliceIdx   = 0                                                                                         # the id of the slice we currently read
            self.AmntSnd        = System.Convert.ToInt32( WebConfigurationManager.AppSettings['InitialResponseLength'])     # max-amount of items to send back to caller 

            self.param = {}                                                 # the URL-parameters are stored in member-attribute param = {}
            self.param.Add('ItemType', None)
            self.param.Add('SliceActive', None)
            self.param.Add('CrsCmd', None)
            self.param.Add('ResultLength', None)
            self.param.Add('Loc', None)
            self.param.Add('City', None)
            self.param.Add('Tags', None)
            self.param.Add('SrchMd', None)
            self.param.Add('StartDate', None)
            self.param.Add('EndDate', None)
            self.param.Add('usrId', None)
            self.rowIdxList = []                                     # the result will contain the row-indexes in the AppCach DataTable "items" matching the query

            #self.itemPreFilter = {'map'  : self.preCheckMap,        # define the checkfunction depending of the item-type. it is given as url-parameter
            #                      'date' : self.preCheckDate,
            #                      'list' : self.preCheckList  }

            # testfunction ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  
            #for a in (0,1,2,3,4,5,6,7,8,9) :
            #    tool.appCch.getSliceBounce( a )
            # END  testfunction ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  

            # developer help : the data inside
            #rowIndx = 0
            #for row in self.appCch.dtSt.Tables["items"].Rows :
            #    self.log.w2lgDvlp('CachedDataSource._init_ DATA in the CACHE : RowIndex : ' + str(rowIndx) + ' --  subject :' + row['subject'].ToString() )
            #    rowIndx += 1


        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # pgLoad is called from PageLoad to create the data-collection
    #
    # 27.06.2013   - bervie-      initial realese
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def pgLoad( self ):
        # try:
        self.log.w2lgDvlp('# # # CachedDataSource.pgLoad( self ) has been called !')

        # prepare UTF-8 output
        context = System.Web.HttpContext.Current
        context.Response.ContentType = "text/plain; charset=utf-8"
        context.Response.Charset = "utf-8"
        context.Response.Clear()
        context.Response.HeaderEncoding = System.Text.UTF8Encoding(False)
        context.Response.ContentEncoding = System.Text.UTF8Encoding(False)

        self.selQueryFunction()     # lets see what parameters were send and what function must be loaded
        self.cutSlice()             # get the needed part the complete-result-array 
        self.addDataItems()         # put the data into result
        self.addConfigParam()       # add the controling parameter needed for the ListExtractor 

        text = '{' + self.Workbench.ToString() + '}'

        out = System.Text.Encoding.UTF8.GetBytes(text)
        context.Response.OutputStream.Write(out, 0, out.Length)
        context.Response.Flush()
        context.Response.End()

        #except Exception,e:
        #    self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # function selQueryFunction  :    the functions is the entry-point. the parameter send to the data-source are used to 
    #                               deceide what function is called
    #
    # 21.07.2013   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def selQueryFunction( self ):
        try:
            self.log.w2lgDvlp('# # # CachedDataSource.selQueryFunction( .. ) has been called !')

            #for parm in self.Page.Request.QueryString.Keys:
            #     self.log.w2lgDvlp('#    CachedDataSource.selQueryFunction( .. ) URL-PARM received     :' + parm + ' - ' + self.Page.Request.QueryString[parm])

            # special case : if user-id is given the system only 
            # shows the data of the given user
            # other checks are not made.
            if ('usrId' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['usrId'] != System.String.Empty:
                    self.param['usrId'] = self.Page.Request.QueryString['usrId']

            if ('ItemType' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['ItemType'] != System.String.Empty:
                    self.param['ItemType'] = self.Page.Request.QueryString['ItemType']

            # SliceActive is not used in the CACHE. we always check the whole data in the cache
            if ('SliceActive' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['SliceActive'] != System.String.Empty:
                    self.param['SliceActive'] = System.Convert.ToInt32( self.Page.Request.QueryString['SliceActive'])
                    self.ActvSliceIdx = self.param['SliceActive']

            if ('CrsCmd' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['CrsCmd'] != System.String.Empty:
                    self.param['CrsCmd'] = System.Convert.ToString( self.Page.Request.QueryString['CrsCmd'] )
                    self.CrsCmd = self.param['CrsCmd']

            if ('ResultLength' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['ResultLength'] != System.String.Empty:
                    self.param['ResultLength'] = System.Convert.ToInt32( self.Page.Request.QueryString['ResultLength'])
                    self.AmntSnd = self.param['ResultLength']

            if ('Loc' in self.Page.Request.QueryString.Keys):
                if len(self.Page.Request.QueryString['Loc']) > 3 :      # even if Loc = '0|' or 'de|41836' the location is not representing a postcode-area
                    self.param['Loc'] = self.Page.Request.QueryString['Loc']

            if ('City' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['City'] != System.String.Empty:
                    self.param['City'] = self.Page.Request.QueryString['City']

            if ('Tags' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['Tags'] != ',' :       # if no Tags were send we get ','. dont ask why :-)
                    self.param['Tags'] = self.Page.Request.QueryString['Tags']

            if ('SrchMd' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['SrchMd'] != System.String.Empty:
                    self.param['SrchMd'] = self.Page.Request.QueryString['SrchMd']

            if ('StartDate' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['StartDate'] != System.String.Empty:
                    # we work with UTC in the database
                    self.param['StartDate'] = System.DateTime.Parse(self.Page.Request.QueryString['StartDate'] ).ToUniversalTime()
                else:
                    self.param['StartDate'] = System.DateTime.MinValue
            if ('EndDate' in self.Page.Request.QueryString.Keys):
                if self.Page.Request.QueryString['EndDate'] != System.String.Empty:
                    self.param['EndDate'] = System.DateTime.Parse(self.Page.Request.QueryString['EndDate'] ).ToUniversalTime()
                else:
                    self.param['EndDate'] = System.DateTime.MinValue

            Loctn = None
            if ( (self.param['Loc'] is not None) or (self.param['City'] is not None) ):
                Loctn = 'WeHaveALocation'
                self.log.w2lgDvlp('self.param["Loc"]    :  "' + unicode(self.param['Loc']) + '"' )
                self.log.w2lgDvlp('self.param["City"]   :  "' + unicode(self.param['City']) + '"')


            # call the rigth selector-function for cached data to read the items the caller is looking for.......
            if   (self.param['usrId'] is not None)                          :   self.idxLstForUser()
            elif (self.param['Tags' ] is not None) and (Loctn is None)      :   self.idxLstByTags()
            elif (self.param['Tags' ] is not None) and (Loctn is not None)  :   self.idxLstByLocatedTags()
            elif (self.param['Tags' ] is None)     and (Loctn is not None)  :   self.idxLstByLocation()
            elif (self.param['Tags' ] is None)     and (Loctn is None)      :   self.idxLstWithoutPreConditions()

            #if   (self.param['usrId'] is not None)                                       :   self.idxLstForUser()
            #elif (self.param['Tags' ] is not None) and (self.param['Loc'] is None)       :   self.idxLstByTags()
            #elif (self.param['Tags' ] is not None) and (self.param['Loc'] is not None)   :   self.idxLstByLocatedTags()
            #elif (self.param['Tags' ] is None) and (self.param['Loc'] is not None)       :   self.idxLstByLocation()
            #elif (self.param['Tags' ] is None) and (self.param['Loc'] is None)           :   self.idxLstWithoutPreConditions()

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # function idxLstForUser  :  if   (self.param['usrId'] is not None)
    #
    #                           get all items for a given user by his _ID
    #
    # 19.08.2013   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def idxLstForUser( self ):
        try:
            self.log.w2lgDvlp('# # # CachedDataSource.idxLstForUser( self ) called ' )
            self.log.w2lgDvlp('#  ' )
            self.log.w2lgDvlp('#  ' )
            self.dtVwCreator = System.Data.DataView(self.dtSt.Tables['items'])
            self.dtVwCreator.Sort = '_creatorGUID'

            creatingUserView = self.appCch.dtVwCreator
            creatingUserView.RowFilter = '_creatorGUID = ' + self.param['usrId']

            for row in creatingUserView:
                mongoId = row['_id'].ToString()
                rowIndex = self.appCch.dtSt.Tables["items"].Rows.IndexOf(self.appCch.dtSt.Tables["items"].Rows.Find(mongoId))     # convert BSON-ID into row-index 
                if self.checkParamMatch( rowIndex ):
                    self.rowIdxList.Add( rowIndex )
                    self.log.w2lgDvlp('#     CachedDataSource.idxLstForUser( self ) row-idx added : ' + rowIndex.ToString() )

            #
            #   ToDo  
            ##  ToDo  #  ToDo  
            ##  ToDo  #  ToDo  #  ToDo  
            ##  ToDo  #  ToDo  #  ToDo  #  ToDo  
            ##  ToDo  #  ToDo  #  ToDo  
            ##  ToDo  #  ToDo  
            #   ToDo  
            #

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # function idxLstByTags  :  (self.param['Tags'] is not None) and (self.param['Loc'] is None)
    #
    #                           function selects items with a tag when no postcode-area was defined. it uses the tag-container helper class
    #
    #                            HINT:  the 'Loc'-parameter (in the member-dictionary) migth be none even if we have a country-code selcted. 
    #                                   so this functions check the url-parameter again to filter for a special country.
    #
    #                                   the function always creates a list with all row-idx of theitems that match. 
    #                                   the paging is done afterwards in cutSlice. 
    #                                   this is costly but till now there was no better idea.
    #
    #
    #
    # 16.08.2013   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def idxLstByTags( self ):
        try:
            country = self.Page.Request.QueryString['Loc'].split(',')[0].strip()                                                                # get current country-code
            self.log.w2lgDvlp('# # # CachedDataSource.idxLstByTags( self ) called ' )
            self.log.w2lgDvlp('#     CachedDataSource.idxLstByTags( self ) TAGS is GIVEN & LOC is NONE' )
            self.log.w2lgDvlp('#     CachedDataSource.idxLstByTags( self )                country-code : ' + country )
            
            mngoIds = []                            # the results as mongo-ids

            # if country == '0':
            if country == '*':
                for tagId in self.createTagList():
                    # if we do not have to check the country get all items for the given tag

                        for itmDct in self.taggs.LocDict.values():
                            if itmDct.has_key(tagId):
                                mngoIds.extend(itmDct[tagId])

            # if country was selected we have to filter the dicts that have a location index for the givewn country
            else:
                for locId in self.taggs.LocDict.keys():
                    if locId.startswith(country):
                        self.log.w2lgDvlp('#     CachedDataSource.idxLstByTags( self )  locId matching country     : ' + locId.ToString() )
                        itmDct = self.taggs.LocDict[locId]
                        for tagId in self.createTagList():
                                if itmDct.has_key(tagId):
                                    mngoIds.extend(itmDct[tagId])

            for mongoId in mngoIds:
                rowIndex = self.appCch.dtSt.Tables["items"].Rows.IndexOf(self.appCch.dtSt.Tables["items"].Rows.Find(mongoId))     # convert BSON-ID into row-index 
                if rowIndex not in self.rowIdxList:
                    if self.checkParamMatch( rowIndex ):
                        self.rowIdxList.Add( rowIndex )
                        self.log.w2lgDvlp('#     CachedDataSource.idxLstByTags( self ) row-idx added : ' + rowIndex.ToString() )
            return

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # function idxLstByLocatedTags        :   function creates the list of row-endexes for taged items for a given postcode-area
    #
    # 21.07.2013   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def idxLstByLocatedTags( self ):
        try:
            self.log.w2lgDvlp('CachedDataSource.idxLstByLocatedTags() called         TAGS is GIVEN & LOC is GIVEN    ' )

            # if no cities were found stop processing
            if not self.createCityList():
                return

            for tagId in self.createTagList() :
                for loc in self.LocationList:
                    LocationIdentifier = loc[0]
                    self.log.w2lgDvlp('CachedDataSource.idxLstByLocatedTags() searching the postcode area : ' + LocationIdentifier )
                    ItemDct = self.taggs.LocDict[LocationIdentifier]    # ItemDct is a dict where the tagname-ids are the keys
                    if ItemDct.has_key(tagId):
                        dbIdList = ItemDct[tagId]
                        for mongoId in dbIdList:
                            rowIndex = self.appCch.dtSt.Tables["items"].Rows.IndexOf(self.appCch.dtSt.Tables["items"].Rows.Find(mongoId))     # convert BSON-ID into row-index for better performance
                            if rowIndex not in self.rowIdxList:
                                if self.checkParamMatch( rowIndex ):
                                    self.rowIdxList.Add( rowIndex )
                                    self.log.w2lgDvlp('CachedDataSource.idxLstByLocatedTags( self ) row-idx added : ' + str(rowIndex) )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # function idxLstByLocation           :   get the row-indexes of all items in a postcode-area when no tags are given
    #
    # 21.07.2013   - bervie-      initial realese
    # 09.09.2013   - bervie-      DISCARDED : function based on hashtag-container. so untagged items was not found. rewritten 
    #                                         see newer fct idxLstByLocation:
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def idxLstByLocation_DISCARDED( self ):
        try:
            self.log.w2lgDvlp('CachedDataSource.idxLstByLocation( self ) called         TAGS is NONE & LOC is GIVEN    ')
            self.rowIdxList = []                        # the result will contain all row-idx of the rows that match
            
            # if no cities were found stop processing
            if not self.createCityList():
                return

            mongoIdLst = []
            for loc in self.LocationList:
                cityToRead = loc[0].ToString()

                #self.log.w2lgDvlp('CachedDataSource.idxLstByLocation( self ) locationList listing  : ' + cityToRead )
                
                if self.taggs.LocDict.has_key( cityToRead ) :
                    #self.log.w2lgDvlp('CachedDataSource.idxLstByLocation( self ) location reading : ' + cityToRead )
                    ItemDct = self.taggs.LocDict[cityToRead]
                
                    for idList in ItemDct.values():                         # get all items we have for the location
                        mongoIdLst.extend( idList )

                    for mongoId in mongoIdLst:                              # add the row-indx-ids unique. there can be doubles because when a item will occure as often sa it has tags
                        rowIdx = self.appCch.dtSt.Tables["items"].Rows.IndexOf(self.appCch.dtSt.Tables["items"].Rows.Find(mongoId))
                        if rowIdx not in self.rowIdxList:
                            if self.checkParamMatch( rowIdx ):
                                self.rowIdxList.Add(rowIdx)
                                self.log.w2lgDvlp('CachedDataSource.idxLstByLocation( self ) rowIdx added : ' + str(rowIdx) )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())




    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # function idxLstByLocation           :   get the row-indexes of all items in a postcode-area 
    #
    # 09.09.2013   - bervie-      initial realese
    #                             old function based on hashtag-container. so untagged items was not found. rewritten 
    #                             now the function is made easier. it goes through the table and adds all items that have 
    #                             the rigth location-id
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def idxLstByLocation( self ):
        try:
            self.log.w2lgDvlp('CachedDataSource.idxLstByLocation( self ) called        TAGS is NONE & LOC is given    ')
            country = self.Page.Request.QueryString['Loc'].split('|')[0].strip().upper()

            # 1. get all matching column s from the cache
            countAcceptedLines = 0

            if self.createCityList() is False:
                return

            locMngIds = []
            for loc in self.LocationList:
                mngIDofLoc = loc[1].ToString()
                # self.log.w2lgDvlp('CachedDataSource.idxLstByLocatedTags() searching the postcode area : ' + mngIDofLoc )
                locMngIds.Add( mngIDofLoc )

            for cntr in range( self.appCch.dtSt.Tables["items"].Rows.Count )[::-1]:                 # go reverse through the list
                row = self.appCch.dtSt.Tables["items"].Rows[cntr]
                if row['_locationID'] in locMngIds:
                    rowIndex = self.appCch.dtSt.Tables["items"].Rows.IndexOf(row)     # convert into row-index for better performance
                    if self.checkParamMatch(rowIndex) == True:
                        self.rowIdxList.Add( rowIndex )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # function idxLstWithoutPreConditions :     if no Tags and no locations were given this function goes through the table. it 
    #                                           checks ( if needed ) the country-code [example: "de for germany"]
    #
    # 21.07.2013   - bervie-      initial realese
    # 01.12.2013   - bervie -     changed '0' to '*' to indicate that all items should be shown
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def idxLstWithoutPreConditions( self ):
        try:
            self.log.w2lgDvlp('CachedDataSource.idxLstWithoutPreConditions( self ) called        TAGS is NONE & LOC is NONE    ')
            country = self.Page.Request.QueryString['Loc'].split(',')[0].strip().upper()

            # 1. get all matching column s from the cache
            countAcceptedLines = 0
            
            for cntr in range( self.appCch.dtSt.Tables["items"].Rows.Count )[::-1]:                 # go reverse through the list
                row = self.appCch.dtSt.Tables["items"].Rows[cntr]
                addFlg = True                                                # switch-flag is true if item should be added.

                if row['_locationID'] == System.String.Empty:                   # if row has no root-element it has no location-id and should not be added 
                    addFlg = False
                else:
                    #if country != '0':                                          # '0' means all items should be checked, so we do not have to check if country matches
                    #
                    # 01.12.2013  changed from '0' to '*' as flag to ignore countries
                    #
                    if country != '*':                                          # '*' means all items should be checked, so we do not have to check if country matches
                        coutryOfRow = self.geoSrc.getKeyStrngFromId( row['_locationID'] )
                        if country[0:2] != coutryOfRow[0:2] : addFlg = False
                        # self.log.w2lgDvlp('CachedDataSource.idxLstWithoutPreConditions    country-abbrevation : ' + coutryOfRow )
                        # if coutryOfRow.ToString() != country:                    # if country does not match we do not have to check this postcode-area

                if addFlg == True:
                    # rowIndex = self.appCch.dtSt.Tables["items"].Rows.IndexOf(self.appCch.dtSt.Tables["items"].Rows.Find(mongoId))     # convert BSON-ID into row-index for better performance
                    rowIndex = self.appCch.dtSt.Tables["items"].Rows.IndexOf(row)     # convert into row-index for better performance

                    if self.checkParamMatch(rowIndex) == True:
                        self.rowIdxList.Add( rowIndex )
                        # self.log.w2lgDvlp('CachedDataSource.idxLstWithoutPreConditions  added rowIndx : ' + str(rowIndex ) )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # cutSlice :     the function cuts the part of needed data from the fuu result array in the IIS cached table.
    #                it starts at the offset (the endpoint-of read in the last reading-process) and ends with the item by result-length
    #
    #                when the end of the cache is reached the function stops adding items and sends 'end_of_data' as CrsCmd
    #
    #
    #
    # 21.07.2013   - bervie-      initial realese
    # 30.07.2013   - bervie-      added inidcator if end of cache was reached.
    # 15.08.2013   - bervie-      reverse row-idx list to become the newest items first
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def cutSlice( self ):
        try:
            totalyFound = len( self.rowIdxList )    # store the number of items in the list before cutting
            self.log.w2lgDvlp('CachedDataSource.cutSlice( self ) has been called , len of the result-list : ' + unicode( totalyFound))
            if totalyFound == 0 : return

            self.rowIdxList.sort(reverse=True)

            for dtRowIdx in self.rowIdxList : 
                row = self.appCch.dtSt.Tables["items"].Rows[dtRowIdx]
                self.log.w2lgDvlp('cutSlice( .. )  data-rows found in list                                        : ' + unicode( dtRowIdx ) + ' - _id ' + row['_id'] )

            # self.rowIdxList = self.rowIdxList[::-1]     # reverse the list to get newest items first and oldest last

            # get the first item where to start with the result-list by the mongo-ID
            # REMARK: the cache in the IIS memory chages while the requrest from the client comes. by using the mongoID we can be sure that this 
            #         will not affect the result. the items that we send to the client are sliced by the moment the first request was send. 
            #         regardless how much items were added to it in the meantime

            leftStart = 0
            if self.CrsCmd != System.String.Empty : 
                startRowIndex = self.appCch.dtSt.Tables["items"].Rows.IndexOf(self.appCch.dtSt.Tables["items"].Rows.Find( self.CrsCmd ))
                leftStart = self.rowIdxList.IndexOf( startRowIndex  )
                #self.log.w2lgDvlp('CachedDataSource.cutSlice( self ) left-start : ' + unicode( leftStart ) + '  for cursor-command  : ' + unicode( self.CrsCmd ) )
            else : 
                # remind the client where is conquer was started
                self.CrsCmd = self.appCch.dtSt.Tables["items"].Rows[self.rowIdxList[0]]['_id']
                #self.log.w2lgDvlp('CachedDataSource.cutSlice( self ) cursor-command  is string.empty . starting point set to ' + self.CrsCmd )

            sliceBegin = leftStart + ( self.ActvSliceIdx * self.AmntSnd )
            slicedEnd  = sliceBegin + self.AmntSnd
            if slicedEnd >= len(self.rowIdxList) : 
                slicedEnd = len(self.rowIdxList)
                self.CrsCmd = 'end_of_data'

            butchersKnife = self.rowIdxList[ sliceBegin : slicedEnd ]

            self.rowIdxList = butchersKnife

            #self.log.w2lgDvlp('cutSlice results before sending data - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  ' )
            #self.log.w2lgDvlp('cutSlice( .. )  start of the slice                  [sliceBegin]                : ' + unicode( sliceBegin ) )
            #self.log.w2lgDvlp('cutSlice( .. )  end   of the slice                  [slicedEnd ]                : ' + unicode( slicedEnd ) )
            #self.log.w2lgDvlp('cutSlice( .. )  amount of items to load             [self.AmntSnd ]             : ' + unicode( self.AmntSnd ) )
            #self.log.w2lgDvlp('cutSlice( .. )  results found before cutting        [len(self.rowIdxList)]      : ' + unicode( totalyFound ) )
            #self.log.w2lgDvlp('cutSlice( .. )  length of the cutted result-list    [self.rowIdxList]           : ' + unicode( len(self.rowIdxList)) )
            #self.log.w2lgDvlp('cutSlice( .. )  length defined by query-parameter   [self.AmntSnd]              : ' + unicode( self.AmntSnd ) )
            #self.log.w2lgDvlp('cutSlice( .. )  cursor-command (mongoid/string)     [self.CrsCmd]               : ' + unicode( self.CrsCmd     ) )
            #self.log.w2lgDvlp('cutSlice( .. )  slice active after load finished    [self.ActvSliceIdx]         : ' + unicode( self.ActvSliceIdx   ) )
            #for dtRowIdx in self.rowIdxList : self.log.w2lgDvlp('cutSlice( .. )  result item in list                                             : ' + unicode( dtRowIdx ) )
            #self.log.w2lgDvlp('CachedDataSource.cutSlice( .. ) - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ' )

            # increase slice-index. next round-trip will send next data because of this 
            self.ActvSliceIdx = self.ActvSliceIdx + 1

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # function checkParamMatch   this function is used by all 'idxLst'-functions to check if the URL-parameters 
    #                            does match the given data in the row.
    #                            this is currently the date-check and the check if all needed data for the data-type is available
    #
    # param : rowToCheck is the row to be analyzed
    #
    # returns : true mean the row matches the selection criterias
    #           false means the row does not match 
    #
    # 21.07.2013   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def checkParamMatch( self , rowIndx ):
        try:
            rowToCheck = self.appCch.dtSt.Tables["items"].Rows[rowIndx]
            if self.param['ItemType'] == 'list' : 
                # self.log.w2lgDvlp('CachedDataSource.checkParamMatch()    RETURN TRUE item-type = item found')
                if (rowToCheck['objectType'] != 1) : 
                    #self.log.w2lgDvlp('CachedDataSource.checkParamMatch()    RETURN False : not an debateitem : rowToCheck["objectType"] != 1)')
                    return False    

            # check if map-item has geo-data
            if self.param['ItemType'] == 'map':
                if (rowToCheck['lon'].ToString() == System.String.Empty) or (rowToCheck['lat'].ToString() == System.String.Empty):
                    #self.log.w2lgDvlp('CachedDataSource.checkParamMatch() missing geographical data for map for ' + rowToCheck['_ID'].ToString())
                    return False

            # date-items must have a date at least
            if self.param['ItemType'] == 'date':
                if rowToCheck['from'].CompareTo( System.DateTime.MinValue) == 0 :
                    #self.log.w2lgDvlp('CachedDataSource.checkParamMatch()    RETURNING FALSE  : no rowToCheck[from] given!')
                    return False

            if (self.param['StartDate'].CompareTo( System.DateTime.MinValue) == 0) : 
                # self.log.w2lgDvlp('CachedDataSource.checkParamMatch()    RETURNING FALSE  : URL-param Start-Date is not given')
                return True                            # if there were no parameter given for start-date we don not have to check 
            #if rowToCheck['from'].ToString() is System.DateTime.MinValue : return False      # if from is NULL the item has no date-information

            chckDateFlag = False

            #self.log.w2lgDvlp('CachedDataSource.checkParamMatch()    TimeSpan Compare just started ')
            #self.log.w2lgDvlp('CachedDataSource  self.param["EndDate"]' + self.param['EndDate'].ToString() )
            #self.log.w2lgDvlp('CachedDataSource  self.param["StartDate"]' + self.param['StartDate'].ToString() )
            #self.log.w2lgDvlp('CachedDataSource  rowToCheck["from"]' + rowToCheck['from'].ToString() )
            #self.log.w2lgDvlp('CachedDataSource  rowToCheck["till"]' + rowToCheck['till'].ToString() )

            # we compare only timespans !
            if (self.param['EndDate'].CompareTo( System.DateTime.MinValue) == 0) : self.param['EndDate'] = self.param['StartDate']
            if (rowToCheck['till'].CompareTo( System.DateTime.MinValue) == 0)    : rowToCheck['till'] = rowToCheck['from']

            # create date-comparing-result ONCE
            # < 0   :  first   BEFORE   CompareTo-Item
            # == 0  :  first   EQUAL    CompareTo-Item
            # > 0   :  first   AFTER    CompareTo-Item
            #
            startToFrom = self.param['StartDate'].CompareTo( rowToCheck['from'] )
            endToFrom = self.param['EndDate'].CompareTo( rowToCheck['from'] )
            startToTill = self.param['StartDate'].CompareTo( rowToCheck['till'] )
            endToTill = self.param['EndDate'].CompareTo( rowToCheck['till'] )

            if ( (startToFrom == 0) or (endToFrom == 0) or (startToTill == 0) or (endToTill == 0) ) : return True       # 0 equality 
            if (startToFrom > 0) and ( startToTill < 0 ) : return True                                                  # 1 start inbetween row_to_check
            if (endToFrom > 0  ) and ( endToTill < 0   ) : return True                                                  # 2 end   inbetween row_to_check
            if (startToFrom < 0) and ( endToTill > 0   ) : return True                                                  # 3 row inbetween user selection
            return False

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # function addDataItems               :   add the found data-items as JSON-code to the result-string-builder
    #
    # 21.07.2013   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def addDataItems( self ):
        try:
            self.log.w2lgDvlp('CachedDataSource.addDataItems( self ) has been called !')

            # nothing found
            self.Workbench.Append('\n"items":[\n')
            if len(self.rowIdxList) == 0:
                self.Workbench.Length = self.Workbench.Length - 1
                self.Workbench.Append('{}],')
                return

            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - DEVELOPMENT HELPER start
            #self.log.w2lgDvlp('CachedDataSource.addDataItems   # # # # # # # # # # # # # # # # # # start result-list of AJAX loader ')
            #for dtRowIdx in self.rowIdxList:
            #    row = self.appCch.dtSt.Tables["items"].Rows[dtRowIdx]
            #    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
            #    self.log.w2lgDvlp('CachedDataSource.addDataItems               : RowIndex : ' + str(dtRowIdx) + ' --  subject :' + row['subject'].ToString() + ' --  tagZero :' + row['tagZero'].ToString() )
            #    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
            #self.log.w2lgDvlp('CachedDataSource.addDataItems   # # # # # # # # # # # # # # # # # # end result-list of AJAX loader ')
            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - DEVELOPMENT HELPER end

            for dtRowIdx in self.rowIdxList:
                row = self.appCch.dtSt.Tables["items"].Rows[dtRowIdx]

                # change DateTime of the row to a useable string
                fromDate = ''
                tillDate = ''
                cratDate = ''
                if (row['from'] != System.DateTime.MinValue ):
                    fromDate = System.TimeZone.CurrentTimeZone.ToLocalTime(row['from']).ToString('dd MMMM yyyy')
                if (row['till'] != System.DateTime.MinValue ):
                    tillDate = System.TimeZone.CurrentTimeZone.ToLocalTime(row['till']).ToString('dd MMMM yyyy')
                if (row['creationTime'] != System.DateTime.MinValue  ):
                    cratDate = System.TimeZone.CurrentTimeZone.ToLocalTime(row['creationTime']).ToString('dd MMMM yyyy H:mm:ss')

                self.Workbench.Append( '{' )
                self.Workbench.Append( '"_ID":"' + row['_ID'].ToString() + '",' )
                #self.Workbench.Append( '"objectType":"' + row['objectType'].ToString() + '",\n' )
                self.Workbench.Append( '"_objectDetailID":"' + row['_objectDetailID'].ToString() + '",' )
                #self.Workbench.Append( '"_hostGUID":"' + row['_hostGUID'].ToString() + '",\n' )
                #self.Workbench.Append( '"_rootElemGUID":"' + row['_rootElemGUID'].ToString() + '",\n' )
                #self.Workbench.Append( '"_parentID":"' + row['_parentID'].ToString() + '",\n' )
                #self.Workbench.Append( '"_followerID":"' + row['_followerID'].ToString() + '",\n' )
                self.Workbench.Append( '"_creatorGUID":"' + row['_creatorGUID'].ToString() + '",' )
                self.Workbench.Append( '"creationTime":"' + cratDate + '",' )
                self.Workbench.Append( '"_locationID":"' + row['_locationID'].ToString() + '",' )
                self.Workbench.Append( '"from":"' + fromDate + '",' )
                self.Workbench.Append( '"till":"' + tillDate + '",' )
                self.Workbench.Append( '"subject":"' + row['subject'].ToString() + '",' )
                #self.Workbench.Append( '"body":"' + row['body'].ToString() + '",\n' )
                self.Workbench.Append( '"nickname":"' + row['nickname'].ToString() + '",' )
                self.Workbench.Append( '"locationname":"' + row['locationname'].ToString() + '",' )
                self.Workbench.Append( '"tagZero":"' + row['tagZero'].ToString() + '",' )
                self.Workbench.Append( '"lat":"' + row['lat'].ToString() + '",' )
                self.Workbench.Append( '"lon":"' + row['lon'].ToString() + '"},\n')

            # remove last chars because they are not used, gringo
            if self.Workbench.Length > len('"items":['):
               self.Workbench.Length = self.Workbench.Length - 2
            self.Workbench.Append('\n],')

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # createCityList   : define a list of postcode-areas in the neighbourhood . the function will add the list to the JSON-object 
    #
    # 10.03.2013  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def createCityList( self ):
        try:
            self.log.w2lgDvlp('CacheDataSource.createCityList( self ) has been called ! ')
            self.log.w2lgDvlp('CacheDataSource.createCityList( self ) loc url param   : ' + str(self.Page.Request.QueryString['Loc']))

            # check for country or city. if only a country is given we load all items 
            # for a given countrycode like 'de|' for germany or 'at|' for austria

            areaSize  = WebConfigurationManager.AppSettings["areaSize"].ToString()
            callParam = self.Page.Request.QueryString['Loc'].split(',')
            cntry     = callParam[0].ToString().strip()
            postcd    = callParam[1].ToString().strip()
            city      = self.Page.Request.QueryString['City'].strip()

            self.log.w2lgDvlp( 'createCityList parameter :   country : ' + unicode(cntry) + ' ; postcode : ' + unicode(postcd) + ' ; city : ' + unicode( city ) + ' ; areasize (form web.config ) : ' + str(areaSize) )
            self.LocationList = self.geoSrc.getPlacesByPlacename( cntry, postcd, city, areaSize )

            # if no cities were found LocationList is None 
            if ( self.LocationList == None ) or ( len( self.LocationList ) == 0 ):
                self.LocationList = None
                return False

            # the data of the cities in th neighbourhood are added to the result-string (which is a class-attribute)
            self.Workbench.Append('\n"places": [\n')
            if len(self.LocationList) == 0:
                self.Workbench.Append('{}\n]')
                return

            for loc in self.LocationList:
                dstnc = '"NULL"'
                if loc[8] != None:
                    dstnc = unicode(loc[8])

                self.Workbench.Append( '{' )
                self.Workbench.Append( '"locSelector":"' + unicode(loc[0]) + '",' )
                self.Workbench.Append( '"mongoID":"' + unicode(loc[1]) + '",' )
                self.Workbench.Append( '"countryCode":"' + unicode(loc[2]) + '",' )
                self.Workbench.Append( '"postCode":"' + unicode(loc[3]) + '",' )
                self.Workbench.Append( '"placeName":"' + unicode(loc[4]) + '",' )
                self.Workbench.Append( '"latitude":' + unicode(loc[5]) + ',' )
                self.Workbench.Append( '"longitude":' + unicode(loc[6]) + ',' )
                self.Workbench.Append( '"COUNTRYandCITY":"' + unicode(loc[7]) + '",' )
                self.Workbench.Append( '"distance":' + dstnc + '},\n')

            self.Workbench.Length = self.Workbench.Length -2
            self.Workbench.Append('\n],\n')

            return True

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # function .addConfigParam  :   add the configuration parametzer needed by the ListExtractor
    #
    # 21.07.2013   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def addConfigParam( self ):
        try:
            self.log.w2lgDvlp('CachedDataSource.addConfigParam() called !')

            self.Workbench.Append('\n"config":')
            self.Workbench.Append( '{' )

            self.CrsCmd
            self.ActvSliceIdx
            self.AmntSnd
            
            self.Workbench.Append( '"ItemType":"'    + self.param['ItemType'] + '",' )
            self.Workbench.Append( '"SliceActive":"' + self.ActvSliceIdx.ToString() + '",' )
            self.Workbench.Append( '"CrsCmd":"'      + self.CrsCmd.ToString() + '"' )

            self.Workbench.Append( '}\n' )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # createTagList  : generate a lsit of tags from the given url-parameter
    #
    # 10.03.2013  - bervie -     initial realese
    # 14.08.2013  - bervie -     add leading '§' to rubric-tags 
    #                            it was removed before transmission from client to server
    # 15.08.2013  - bervie -     ussing-tag-cache functions
    #
    # ***********************************************************************************************************************************************
    def createTagList( self ):
        try:
            tagIds = []
            tagLst = self.param['Tags'].strip().lower().split(',')

            if tagLst[0] != System.String.Empty : tagLst[0] = '§' + tagLst[0].upper()       # leading '§' are removed before transmission to AJAX-fnct. add it again and turn tag to upper. caommand-tags MUST be UPPER
            tagIds = self.taggs.askForTagIdxList( tagLst )

            return tagIds

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())














# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
#
# helper for dataSource__city.aspx.py : the autocomplete datasource for cities 
#  
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
class CachedCitySource( mongoDbMgr.mongoMgr ):
    '''
    todo

    '''


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # constructor. 
    #
    # 30.08.2013   -bervie-    initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def __init__(self, page ):
        try:
            mongoDbMgr.mongoMgr.__init__(self, page )                                                                       # wake up papa ; mother njbTools is included by inheritance!

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # pgLoad is called from PageLoad to create the data-collection
    #
    # 27.06.2013   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def pgLoad( self ):
        try:
            # self.log.w2lgDvlp('# # # CachedDataSource.pgLoad( self ) has been called !')

            # prepare UTF-8 output
            context = System.Web.HttpContext.Current
            context.Response.ContentType = "text/plain; charset=utf-8"
            context.Response.Charset = "utf-8"
            context.Response.Clear()
            context.Response.HeaderEncoding = System.Text.UTF8Encoding(False)
            context.Response.ContentEncoding = System.Text.UTF8Encoding(False)

            tagpart = self.Page.Request.QueryString['tagpart']
            query = self.Page.Request.QueryString['query'].lower()

            result = []
            for citySrc in self.geoSrc.locTable.Rows:
                city = citySrc['placename'].ToString().lower()
                
                if city.startswith(query):
                    itemToAdd = '"' + citySrc['placename'   ].ToString() + '"'
                    if itemToAdd not in result:
                        result.Add( itemToAdd )

            # generate result string
            rsltStrng = ', '.join(result)
            text = '{ "options": [' + rsltStrng + ']}'

            out = System.Text.Encoding.UTF8.GetBytes(text)
            context.Response.OutputStream.Write(out, 0, out.Length)
            context.Response.Flush()
            context.Response.End()

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())














# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
#
# helper for dataSource__hashtag.aspx.py : the autocomplete datasource for hashtags
#  
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
class CachedHashTagSource( mongoDbMgr.mongoMgr ):
    '''
    todo
    '''


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # constructor. 
    #
    # 30.08-2013  -bervie-  initial
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def __init__(self, page ):
        try:
            mongoDbMgr.mongoMgr.__init__(self, page )                                                                       # wake up papa ; mother njbTools is included by inheritance!

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # pgLoad is called from PageLoad to create the data-collection
    #
    # 30.08.2013   - bervie-      initial realese
    #
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def pgLoad( self ):
        try:
            # self.log.w2lgDvlp('# # # CachedDataSource.pgLoad( self ) has been called !')

            # prepare UTF-8 output
            context = System.Web.HttpContext.Current
            context.Response.ContentType = "text/plain; charset=utf-8"
            context.Response.Charset = "utf-8"
            context.Response.Clear()
            context.Response.HeaderEncoding = System.Text.UTF8Encoding(False)
            context.Response.ContentEncoding = System.Text.UTF8Encoding(False)

            result = []
            query = self.Page.Request.QueryString['query'].lower()
            for tg in self.taggs.TaggList:
                tag = tg.ToString().lower()
                if tag.startswith(query):
                    result.Add( '"' + tag + '"' )
            rsltStrng = ', '.join(result)
            text = '{ "options": [' + rsltStrng + ']}'

            out = System.Text.Encoding.UTF8.GetBytes(text)
            context.Response.OutputStream.Write(out, 0, out.Length)
            context.Response.Flush()
            context.Response.End()

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
#
# helper for dataSource__slctdRbrc.aspx.py : the datasource for rubric-matrix-manager 
#  
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
class CachedRubricSource( mongoDbMgr.mongoMgr ):
    '''
    todo

    '''
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # constructor. 
    #
    # 30.08.2013   -bervie-    initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def __init__(self, page ):
        try:
            mongoDbMgr.mongoMgr.__init__(self, page )                                                                       # wake up papa ; mother njbTools is included by inheritance!

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # pgLoad is called from PageLoad to create the data-collection
    #
    # 27.06.2013   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def pgLoad( self ):
        try:
            # self.log.w2lgDvlp('# # # CachedDataSource.pgLoad( self ) has been called !')
            # prepare UTF-8 output
            context = System.Web.HttpContext.Current
            context.Response.ContentType = "text/plain; charset=utf-8"
            context.Response.Charset = "utf-8"
            context.Response.Clear()
            context.Response.HeaderEncoding = System.Text.UTF8Encoding(False)
            context.Response.ContentEncoding = System.Text.UTF8Encoding(False)

            source = ''
            # the key is selected in the matrix-manager : $("a[id*='CoPlaBottom_hyli_select']").click(function (event) { ...............
            switchr = { 'EVT' : 'date_event_div' ,
                        'LOC' : 'location_div'   ,
                        'ANO' : 'annonce_div'    ,
                        'INI' : 'initiative_div' ,
                        'BUI' : 'business_div'    }

            if 'rbrc' in self.Page.Request.QueryString:
                rbrc = self.Page.Request.QueryString['rbrc'].strip()
                if rbrc in switchr.keys():
                    selctor = switchr[rbrc]
                    source = self.ui.rubricDict[selctor] 

            out = System.Text.Encoding.UTF8.GetBytes(source)
            context.Response.OutputStream.Write(out, 0, out.Length)
            context.Response.Flush()
            context.Response.End()

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())




# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# 
# helper for dataSource__countryPostCode.aspx.py : get place-list by country-code and city-name
#  
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
class GetCitiesByCountryAndName( mongoDbMgr.mongoMgr ):
    '''
    todo
    '''
    
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # constructor. 
    #
    # 30.08.2013   -bervie-    initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def __init__(self, page ):
        try:
            mongoDbMgr.mongoMgr.__init__(self, page )                                                                       # wake up papa ; mother njbTools is included by inheritance!

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # pgLoad is called from PageLoad to create the data-collection
    #
    # 27.06.2013   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def pgLoad( self ):
        try:
            # self.log.w2lgDvlp('# # # LOCALGetCitiesByCountryAndName->pgLoad has been called !')

            # prepare UTF-8 output
            context = System.Web.HttpContext.Current
            context.Response.ContentType = "text/plain; charset=utf-8"
            context.Response.Charset = "utf-8"
            context.Response.Clear()
            context.Response.HeaderEncoding = System.Text.UTF8Encoding(False)
            context.Response.ContentEncoding = System.Text.UTF8Encoding(False)

            cntryCode = self.Page.Request.QueryString['ctry'].upper()
            cityName = self.Page.Request.QueryString['city'].upper()

            queryKey = cntryCode + '|' + cityName

            temp = System.Text.StringBuilder()              # build the list with all cities
            result = ''
            result = []
            temp.Append('{"cities":[\n')

            for row in self.geoSrc.locTable.Rows:
                if row['keyCity'].ToString() == queryKey:
                    #tool.log.w2lgDvlp('dataSource__countryPostCode.aspx.py   found postcode     ' + row['postalCode'].ToString() )
                    #tool.log.w2lgDvlp('dataSource__countryPostCode.aspx.py   found placename    ' + row['placeName'].ToString() )
                    #tool.log.w2lgDvlp('dataSource__countryPostCode.aspx.py   found countrycode  ' + row['countryCode'].ToString() )
                    #tool.log.w2lgDvlp('dataSource__countryPostCode.aspx.py   found mongoID      ' + row['mngId'].ToString() )
                    #tool.log.w2lgDvlp('---------------------------------------------------------------------------------------------')

                    temp.Append( '{' )
                    temp.Append( '"postalCode":"' + row['postalCode'].ToString() + '",' )
                    temp.Append( '"placeName":"' + row['placeName'].ToString() + '",' )
                    temp.Append( '"countryCode":"' + row['countryCode'].ToString() + '",' )
                    temp.Append( '"mngId":"' + row['mngId'].ToString() + '",' )
                    temp.Append( '"lat":"' + row['latitude'].ToString() + '",' )
                    temp.Append( '"lon":"' + row['longitude'].ToString() + '"},\n')

            if temp.Length == 0:
                result = '{ "cities":[{}] }'
            else:
                temp.Length = temp.Length - 2
                temp.Append('\n]}')
                result = temp.ToString()

            out = System.Text.Encoding.UTF8.GetBytes( result )
            context.Response.OutputStream.Write(out, 0, out.Length)
            context.Response.Flush()
            context.Response.End()

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())




















# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# 
# JobSearch helper for jobs_search.aspx.py : the class takes a closer look into the available job-offers and creates a data-table bindable to a asp.net webctrl
#  
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
# --  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  -
class JobSearch( mongoDbMgr.mongoMgr ):
    # ***********************************************************************************************************************************************
    # constructor : store members for loading
    #
    # parameter :  
    #   pg      :       the pointer to the webform-page instance is stored in self.Page 
    #   locDef  :       the location-definer instance [type LocDefiner] used in the current web-page
    #
    # attributes:
    #   RsltTbl :       DataTable with the results found by last load-function
    #
    # 10.12.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def __init__(self, pg, locDef ):
        try:
            mongoDbMgr.mongoMgr.__init__(self, pg)      # wake up papa ; mother njbTools is included by inheritance!

            self.locDef = locDef                        # instance of LocDefinere
            self.prprTbl = None                         # DataTable with results of last load

            self.ui.getCtrlTree( self.Page.Master )
            # self.log.w2lgDvlp('constructor of class job_search.aspx.py->(Page, jobTag, LocId ) aufgefufen!')

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # loadJobsOfType : one kind of job is wanted for the givern postcode
    #
    # 10.12.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def loadJobsOfType( self ):
        try:
            # self.logMsg('job_search.aspx.py->JobSearch.loadJobsOfType called ' )
            tgLst = self.ui.convertTagsFromInput(self.jobTag)

            # create the link to the data-display webform
            destUrl = ''
            if not self.usrDt.isLoggedIn() : destUrl = WebConfigurationManager.AppSettings['DetailsForStrangers']       # use the detail-viewer for visitors that aren't looged in
            else : destUrl = WebConfigurationManager.AppSettings['AddToTrialThread']                                    # go to detail-viewer for logged in users

            #self.log.w2lgDvlp('job_search.aspx.py->JobSearch.loadJobsOfType locId    : ' + unicode( self.locId  ) )
            #self.log.w2lgDvlp('job_search.aspx.py->JobSearch.loadJobsOfType tgLst    : ' + unicode( tgLst ) )
            postCode = self.locDef.getCtryPstCd(self.locId)
            itmIds = self.taggs.loadBaseItems( postCode , tgLst, False )
            #self.log.w2lgDvlp('job_search.aspx.py->JobSearch.loadJobsOfType postcode : ' + unicode( postCode  ) )
            #self.log.w2lgDvlp('job_search.aspx.py->JobSearch.loadJobsOfType itmIds   : ' + unicode( itmIds ) )

            itemTable   = self.appCch.dtSt.Tables["items"]
            resultTble  = itemTable.Clone()

            for itm in itmIds:
                row = itemTable.Rows.Find(itm)
                resultTble.ImportRow(row)
                # HACK tagZero in the temporary result-table will store the link to the detailview  # added 11-08-2013 bervie
                itmLnk = destUrl + '?item=' + row['_ID'].ToString()
                resultTble.Rows[resultTble.Rows.Count - 1]['tagZero'] = itmLnk

            # store ids in order of apperance in the table into an array. we will get the _id by calling the index of this array
            #self.Page.ViewState['IdList'] = itmIds

            if resultTble.Rows.Count == 0:
                self.prprTbl = None
            else:
                self.prprTbl = resultTble

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # loadJbsOfLoctn : if no job-type is filtered ( jobtype == * ) this function crerates a list with all stuff of a given location
    #
    # 10.12.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def loadJbsOfLoctn( self ):
        try:
            # 1. search-parameter from the UI
            #    locations : get the selected location
            tagTable    = self.appCch.dtSt.Tables["itemTags"]
            itemTable   = self.appCch.dtSt.Tables["items"]
            resultTble  = itemTable.Clone()
            #minAmount = System.Convert.ToInt16( WebConfigurationManager.AppSettings["MinNumOfDebates"] )

            # create the link to the data-display webform
            destUrl = ''
            if not self.usrDt.isLoggedIn() : destUrl = WebConfigurationManager.AppSettings['DetailsForStrangers']       # use the detail-viewer for visitors that aren't looged in
            else : destUrl = WebConfigurationManager.AppSettings['AddToTrialThread']                                    # go to detail-viewer for logged in users

            # 2. create a list of locations ordered by the distance from selected value
            locList = self.locDef.loadCityArea( False )

            # helper-array to store all mongo-ids we have loaded from item-table
            # idList = []

            for location in locList:
                # select all jobs in this area
                rows = self.appCch.dtVwLoctn.FindRows( location )
                #self.logMsg('jobs_list.aspx.py-LoadAllJobs location_id : ' + str(location) )

                for row in rows:
                    if row['objectType'] == 0:              # get all jobs   objectType 0 = job is defined in the web.config
                        resultTble.ImportRow(row.Row)
                        #idList.Add( row['_ID'].ToString() )
                        #self.log.w2lgDvlp('jobs_list.aspx.py-LoadAllJobs item loaded : ' + row['_ID'].ToString() )
                        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                        # HACK tagZero in the temporary result-table will store the link to the detailview   # added 11-08-2013 bervie
                        itmLnk = destUrl + '?item=' + row['_ID'].ToString()
                        resultTble.Rows[resultTble.Rows.Count - 1]['tagZero'] = itmLnk

            # store ids in order of apperance in the table into an array. we will get the _id by calling the index of this array
            #self.Page.ViewState['IdList'] = idList            

            # 3. store the result in the class attribute
            if resultTble.Rows.Count == 0:
                self.prprTbl = None
            else:
                self.prprTbl = resultTble

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # loadWthoutLctn :  load all jobs without filtering for a postcode-area. this function is called when no country has been specified or a whole 
    #                   country should be displayed
    #
    # parameter : jobtag  : the internal job-type identifier
    #
    #
    # 17.12.2013   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def loadWthoutLctn( self, jobTag = None ):
        try:
            # get the current country-selection
            cntrySlctn = self.usrDt.userDict['LCDFNR_SLCTSTR'].split('|')[0].ToString()
            resultTble  = self.appCch.dtSt.Tables["items"].Clone()
            if jobTag is not None: jobTag = jobTag.upper()

            # create the link to the data-display webform
            destUrl = ''
            if not self.usrDt.isLoggedIn() : destUrl = WebConfigurationManager.AppSettings['DetailsForStrangers']       # use the detail-viewer for visitors that aren't looged in
            else : destUrl = WebConfigurationManager.AppSettings['AddToTrialThread']                                    # go to detail-viewer for logged in users

            #for cntr in range( self.appCch.dtSt.Tables["items"].Rows.Count )[::-1]:                 # go reverse through the list
            for cntr in range( self.appCch.dtSt.Tables["items"].Rows.Count ):
                row = self.appCch.dtSt.Tables["items"].Rows[cntr]
                
                # if row is not a job it is also not interesting
                if row['objectType'] != 0 : continue

                # if country is selected check if row is for same country : this is NOT a postcode-check ! this query is postcode independent
                if cntrySlctn != '*' :
                    cntryOfRow = self.locDef.getCtryPstCd( row['_locationID'] ).split('|')[0]
                    if cntryOfRow != cntrySlctn : 
                        continue

                # check if we have a matching job-type
                if (jobTag is not None) and (jobTag != '*'):
                    if row['tagZero'].ToString() != jobTag : 
                        continue

                resultTble.ImportRow(row)       # it seems to be a valid row !!  !!!!   !!!!!! follow the white rabbit

                # HACK tagZero in the temporary result-table will store the link-parameter to the detailview; the final redirection-link will be build in javascript
                LnkParam = destUrl + '?item=' + row['_ID'].ToString()
                resultTble.Rows[resultTble.Rows.Count - 1]['tagZero'] = LnkParam

            if resultTble.Rows.Count == 0:
                resultTble.Rows
                self.prprTbl = None
            else:
                self.prprTbl = resultTble

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # loadJobsByLctn : load-kickstarter : a data-table with all results will be created : self.resultTbl
    #  ++ remark ++ : the result of the load will be stored in the member-attribute self.resultTbl
    #
    #
    # 10.12.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def loadJobsByLctn(self, jobTag = None , locId = None ):
        try:
            self.jobTag = jobTag
            self.locId = locId

            # if something was selceted filter the job-types
            if self.jobTag != '*' : 
                self.loadJobsOfType()
            # if no job was selected we load all stuff
            else : 
                self.loadJbsOfLoctn()

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # getJobIdtfr() : get the real-name and the internal tag for a given job-type like : ('PC und Internet', '?*JTD01_computer' )
    #                 if the jobtype in the url is unknown it retunrs ('Ohne Filter', '*')
    #
    # 10.12.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def getJobIdtfr(self):
        try:
            # jobRealName is the real-name of the given job-type
            if self.Page.Request.QueryString['jobtype'] != None:
                jobRealName = self.Page.Request.QueryString['jobtype'] 
            else:
                return ('Ohne Filter', '*')

            seperator = WebConfigurationManager.AppSettings['stringSeperator']
            names = WebConfigurationManager.AppSettings['jobType_DE'].split(seperator)
            values = WebConfigurationManager.AppSettings['jobTypeValue'].split(seperator)

            #check if we have a valid parameter 
            if jobRealName not in names : return ('Ohne Filter', '*')

            jobTagName = values[ names.index(jobRealName) ]
            return (jobRealName,jobTagName)             # returns ('PC und Internet', '?*JTD01_computer' )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # load :   this functions loads the data as a slice.
    #
    # 27.12.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def load(self):
        try:
            self.log.w2lgDvlp('job_search.aspx.py->JobSearch.load(self) - - - - - - - - - - - - - - - ')

            # 1. check if location-selection was invalid. if so we cannot display jobs
            if self.usrDt.userDict['LCDFNR_MONGOID'] == 'not found' : 
                self.errorMessage(self.ui.getCtrl('msg_wrong_location').Text )
                return False

            locDbId = self.locDef.mongoId
            jbTg = self.getJobIdtfr()[1]

            #self.log.w2lgDvlp('job_search.aspx.py->JobSearch.load(self)  location-id DB :      ' + unicode(locDbId) )
            #self.log.w2lgDvlp('job_search.aspx.py->JobSearch.load(self)  job-tag        :      ' + unicode(jbTg) )


            # 2. if location was specified load with location; if not load without.
            if self.usrDt.userDict['LCDFNR_MONGOID'] == 'not available' : 
                self.loadWthoutLctn(jbTg)
            else:
                self.loadJobsByLctn(jbTg,locDbId)

            if self.prprTbl == None:
                return None

            # generate the part of result needed
            return self.createSlice()

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # createSlice :   generate a part of the self.result-table needed for the display (easy name for that is paging)
    #                 
    #
    # parameter : None ( the ViewState is used to figure out direction )
    # returns   : DataTable : The function creaes a data-table that can be bound as datasource to a ctrl/widget
    #
    # 27.12.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def createSlice(self):
        try:
            #return self.prprTbl

            # 1. get the rahmenbedingungen
            firstRow    = lastRow = rng = None
            pgngDrctn   = self.Page.ViewState['PAGING_DIRECTION']                       # what is the direction for the next page of data
            jbPgLngth   = int(WebConfigurationManager.AppSettings[ 'JobPageLength' ])    # the amount of job-items that should be displayed at once
            rsltLength  = self.prprTbl.Rows.Count                                        # length of the result-table

            if (self.Page.ViewState['NWST_ITM'] == System.String.Empty) and (self.Page.ViewState['OLDST_ITM'] == System.String.Empty):
                firstRow = rsltLength - jbPgLngth
                lastRow = rsltLength
            else :
                if pgngDrctn =='BACKWARD':
                    firstRow = self.Page.ViewState['OLDST_ITM'] - jbPgLngth
                    lastRow = firstRow + jbPgLngth
                if pgngDrctn =='FORWARD':
                    firstRow = self.Page.ViewState['OLDST_ITM'] + jbPgLngth
                    lastRow = firstRow + jbPgLngth

            # # # check bounds
            # 1. if result-table is shorter than the defined displayitem-amount display the whole table
            if rsltLength < jbPgLngth:
                firstRow = 0
                lastRow = rsltLength
            if lastRow > rsltLength : 
                lastRow = rsltLength
            if firstRow < 0 : 
                firstRow = 0

            self.Page.ViewState['OLDST_ITM'] = firstRow
            self.Page.ViewState['NWST_ITM'] = lastRow

            self.ui.getCtrl('hyLnk_pageOlderJobs').Visible = True
            self.ui.getCtrl('hyLnk_pageNewerJobs').Visible= True
            if firstRow <= 0:
                self.ui.getCtrl('hyLnk_pageOlderJobs').Visible = False
            if lastRow >= rsltLength:
                self.ui.getCtrl('hyLnk_pageNewerJobs').Visible = False
            self.log.w2lgDvlp('job_search.aspx.py- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ')
            self.log.w2lgDvlp('job_search.aspx.py->createSlice       : direction    ' + unicode( pgngDrctn ) )
            self.log.w2lgDvlp('job_search.aspx.py->createSlice       : firstRow     ' + unicode( firstRow ) )
            self.log.w2lgDvlp('job_search.aspx.py->createSlice       : lastRow      ' + unicode( lastRow ) )
            self.log.w2lgDvlp('job_search.aspx.py- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ')

            # copy the data in REVERSE order. the newest entry should be displayed as first entry
            outputTable = self.prprTbl.Clone()
            for idx in reversed(range( firstRow, lastRow )):
                #self.log.w2lgDvlp('job_search.aspx.py->createSlice       : import Index   ' + unicode(idx) )
                outputTable.ImportRow( self.prprTbl.Rows[idx] )
            return outputTable

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())

    # ***********************************************************************************************************************************************
    # HndlrButtonClick    : handler for button-click-events. chose button by ID
    #
    # 14.10.2013  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def HandlBtnClick(self, sender, e):
        try:
            urlNext = None
            if sender.ID not in ['btn_select_slct_loctn','btn_show_job_list','hyLnk_pageOlderJobs','hyLnk_pageNewerJobs'] : return False

            # # # BUTTON paging : display newer jobs ('forward-button') later in Page_PreRender
            if sender.ID == 'hyLnk_pageNewerJobs':
                self.Page.ViewState['PAGING_DIRECTION'] = 'FORWARD'
                return True

            # # # BUTTON paging : display older jobs ('backward-button') later in Page_PreRender
            elif sender.ID == 'hyLnk_pageOlderJobs':
                self.Page.ViewState['PAGING_DIRECTION'] = 'BACKWARD'
                return True

            # # # BUTTON location was changed ('Ort ?ndern')
            elif sender.ID == 'btn_select_slct_loctn':
                countryCode     = self.ui.getCtrl('sel_country').SelectedValue 
                cityIdentifier  = self.ui.getCtrl('txbx_city').Text
                self.locDef.setLocByInpt( countryCode , cityIdentifier ) 
                if self.locDef.getValidLoctn() is None:
                    self.errorMessage(self.ui.getCtrl('msg_noLocFound').Text )
                    return False

                # reset the paging
                self.Page.ViewState['PAGING_DIRECTION']  = System.String.Empty           # read data from beginning ...
                self.Page.ViewState['NWST_ITM'] = System.String.Empty
                self.Page.ViewState['OLDST_ITM'] = System.String.Empty

            # # # BUTTON . reload list data ('neu laden') : if all input valid just load the stuff again
            elif sender.ID == 'btn_show_job_list' :
                # check if input is correct
                if self.checkInput() is not True:
                    self.log.w2lgDvlp('job_search.aspx.py->HandlBtnClick : Input-Error  ')
                    return False
                self.Page.ViewState['PAGING_DIRECTION']  = System.String.Empty           # read data from beginning ...
                self.Page.ViewState['NWST_ITM']  = System.String.Empty                   # ... and resets the paging
                self.Page.ViewState['OLDST_ITM'] = System.String.Empty

            # page will be reloaded
            urlNext = WebConfigurationManager.AppSettings['SearchJob'] + '?jobtype='
            urlNext += self.Page.Server.UrlEncode( self.getJobIdtfr()[0] )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())
            return

        if urlNext != None :
            # self.usrDt.measurePeformance('HndlrButtonClick of webform Default.aspx before redirection')
            self.Page.Response.Redirect( self.Page.ResolveUrl( urlNext ) )


    # ***********************************************************************************************************************************************
    # HandlLnkBtn    : handler for the link-buttons. they call same webform with different parameter for job-type
    #
    # 10.12.2013  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def HandlLnkBtn(self, sender, e):
        try:
            urlNext = None

            # get the current job_type_tag from the link_id
            jobTypeTag = sender.ID.split('_')[-1].ToString().upper()
            jobTaggs =  WebConfigurationManager.AppSettings['jobTypeValue'].split(';')[1:]
            self.log.w2lgDvlp('job_search.aspx.py->HandlLnkBtn -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  ' )
            self.log.w2lgDvlp('job_search.aspx.py->HandlLnkBtn : jobTypeTag   :  ' +  jobTypeTag )
            self.log.w2lgDvlp('job_search.aspx.py->HandlLnkBtn : jobTaggs     :  ' +  unicode(jobTaggs) )

            jobName = '*'
            for tag in jobTaggs:
                if jobTypeTag in tag:
                    idx = jobTaggs.index(tag) + 1
                    jobName = WebConfigurationManager.AppSettings['jobType_DE'].split(';')[idx]

            self.log.w2lgDvlp('job_search.aspx.py->HandlLnkBtn : job_type selected :  ' +  jobName )
            self.log.w2lgDvlp('job_search.aspx.py->HandlLnkBtn -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  ' )
            # go to the listing of jobs with the search-parameter
            urlNext = WebConfigurationManager.AppSettings['SearchJob'] + '?jobtype='
            urlNext += self.Page.Server.UrlEncode( jobName )

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())
            return

        if urlNext != None :
            self.Page.Response.Redirect( self.Page.ResolveUrl( urlNext ) )

    # ***********************************************************************************************************************************************
    # checkInput() : checks user input 
    #
    # 29.12.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def checkInput(self):
        try:
            # check if a valid location is selcted
            if self.usrDt.userDict['LCDFNR_MONGOID'] == 'not found' : 
                self.errorMessage(self.ui.getCtrl('msg_wrong_location').Text )
                return False

            return True

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # getParamter() : store URL-parameter in the helper-ctrls
    #
    # checking this URL-Parameter:
    #  Loc        : the locationa as database-id
    #  jobtype    : the type of jobs that should be selected
    #
    # 10.12.2013    berndv  initial realese
    # ***********************************************************************************************************************************************
    def getParamter(self):
        try:
            # location can come as URL-parameter : re-initialyze the location-definer
            loctn = System.String.Empty
            if self.Page.Request.QueryString['Loc'] != None:
                loctn = self.Page.Request.QueryString['Loc']
                self.locDef.setLocByDbId( loctn )

            # check and store jobtype-parameter
            jobIdntfr = self.getJobIdtfr()
            self.ui.getCtrl('txbx_jobName').Text = jobIdntfr[0]
            self.ui.getCtrl('txbx_jobType').Text = jobIdntfr[1]
 
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # Page_Load        : initializer of the webpage
    #
    # 18.03.2012  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def Page_Load(self, sender, e):
        try:
            # hide the main-user-interface after a button-click and show  a please-wait sedativ
            self.ui.getCtrlTree( self.Page.Master )
            self.ui.hideFormAfterClick()
            self.errorMessage('')

            if( not self.Page.IsPostBack ):
                repeater = self.gtCtl('repJobList')                             # disable view-state for the repeater 
                repeater.EnableViewState = False                                # ...(!! only display the data from current search !!)

                self.Page.ViewState['NWST_ITM'] = System.String.Empty                # currently the job-display has a paging which is applied on the server. 
                self.Page.ViewState['OLDST_ITM'] = System.String.Empty               # these are the bounds of table that are displayed on screen

                self.Page.ViewState['PAGING_DIRECTION'] = System.String.Empty        # the direction of the paging [FORWARD]: show newer; [BACKWARD]: show older

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # Page_PreRender    : initializer after button_click
    #
    # 18.11.2013  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def Page_PreRender(self, sender, e):
        try:
            # insert curretn location from the session-cache
            self.getParamter()                                                  # use URL-parameter for data-select to make the page bookmarkable
            self.locDef.uiInitLocIntfc()                                             # init the location-select area

            # resultTble = getSlcOfJbs( getJobTable() , False )                 # get the data needed to fill the repeater  IT IS A DATA-VIEW, NOT A TABLE !!

            resultTble = self.load()                                            # load the data from the helper-class. 

            if (resultTble == None) or (resultTble.Rows.Count == 0):
                self.errorMessage(self.ui.getCtrl('msg_noDataFound').Text )
                return False
            else:
                repeater = self.gtCtl('repJobList')
                repeater.DataSource = resultTble
                repeater.DataBind()
                return True

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())
            return
